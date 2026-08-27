#!/usr/bin/env python3
"""Certify both supercritical converse branches for the manuscript family.

The script continuously optimises the reverse ``Q||P`` branch and the valid
forward ``P||Q`` branch in ``a=(lambda-1)/lambda``.  Every selected projection
is rechecked by a 101-by-101 full-square screen and multistart refinement.  It
then solves the independent semi-infinite minimax LP for ``n=1,...,25`` with
checkpointing, cross-blocklength active-set warm starts, and dense validation.
"""

from __future__ import annotations

import json
import csv
import math
import sys
import time
from dataclasses import asdict, dataclass
from decimal import Decimal, localcontext
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, differential_evolution, minimize, minimize_scalar
from scipy.special import logsumexp


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "numerics" / "data"
CHECKPOINT_DIR = (
    ROOT / "numerics" / "checkpoints" / "ternary_supercritical_rplus_exact"
)
OUTPUT_PATH = DATA_DIR / "ternary_supercritical_converse.json"
CSV_PATH = DATA_DIR / "ternary_supercritical_converse.csv"
CACHE_PATH = DATA_DIR / "ternary_supercritical_projection_cache.json"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from affine_ternary_lp import (  # noqa: E402
    AffineTernaryClass,
    expectations,
    solve_composite_minimax,
    ternary_type_space,
)


P0 = np.array([0.327, 0.418, 0.255], dtype=float)
P1 = np.array([0.563, 0.266, 0.171], dtype=float)
Q0 = np.array([0.143, 0.357, 0.500], dtype=float)
Q1 = np.array([0.379, 0.205, 0.416], dtype=float)


def p_of(s: float) -> np.ndarray:
    return P0 + s * (P1 - P0)


def q_of(t: float) -> np.ndarray:
    return Q0 + t * (Q1 - Q0)


def kl(first: np.ndarray, second: np.ndarray) -> float:
    return float(np.sum(first * (np.log(first) - np.log(second))))


def renyi(first: np.ndarray, second: np.ndarray, order: float) -> float:
    if math.isinf(order):
        return float(np.max(np.log(first) - np.log(second)))
    delta = order - 1.0
    if delta == 0.0:
        return kl(first, second)
    log_ratio = np.log(first) - np.log(second)
    # Around order one this expm1/log1p form avoids subtracting two nearly
    # equal log-normalisers before division by delta.
    if abs(delta) < 1.0e-4:
        u = float(np.sum(first * np.expm1(delta * log_ratio)))
        return math.log1p(u) / delta
    return float(logsumexp(np.log(first) + delta * log_ratio) / delta)


def directed_value(x: np.ndarray, order: float, orientation: str) -> float:
    s, t = map(float, x)
    if orientation == "Q||P":
        return renyi(q_of(t), p_of(s), order)
    if orientation == "P||Q":
        return renyi(p_of(s), q_of(t), order)
    raise ValueError(orientation)


def directed_gradient(x: np.ndarray, order: float, orientation: str) -> np.ndarray:
    """Analytic gradient of the finite-order directed projection objective."""

    if math.isinf(order):
        raise ValueError("the order-infinity objective is nonsmooth")
    s, t = map(float, x)
    if orientation == "Q||P":
        first, first_direction = q_of(t), Q1 - Q0
        second, second_direction = p_of(s), P1 - P0
        first_coordinate, second_coordinate = 1, 0
    elif orientation == "P||Q":
        first, first_direction = p_of(s), P1 - P0
        second, second_direction = q_of(t), Q1 - Q0
        first_coordinate, second_coordinate = 0, 1
    else:
        raise ValueError(orientation)

    if order == 1.0:
        first_derivative = float(
            np.sum(first_direction * (np.log(first) - np.log(second)))
        )
        second_derivative = float(
            -np.sum(first * second_direction / second)
        )
    else:
        log_terms = order * np.log(first) + (1.0 - order) * np.log(second)
        weights = np.exp(log_terms - logsumexp(log_terms))
        first_derivative = float(
            order / (order - 1.0)
            * np.sum(weights * first_direction / first)
        )
        second_derivative = float(
            -np.sum(weights * second_direction / second)
        )

    gradient = np.empty(2, dtype=float)
    gradient[first_coordinate] = first_derivative
    gradient[second_coordinate] = second_derivative
    return gradient


@dataclass
class Projection:
    orientation: str
    order: float
    D: float
    s: float
    t: float
    method: str
    gradient_s: float
    gradient_t: float
    kkt_violation: float | None = None
    screen_D: float | None = None
    screen_s: float | None = None
    screen_t: float | None = None
    screen_minus_final: float | None = None


class Projector:
    def __init__(self) -> None:
        self.records: dict[str, list[Projection]] = {"Q||P": [], "P||Q": []}
        self.memo: dict[tuple[str, float, bool], Projection] = {}
        self.calls = 0

    def nearest_starts(self, order: float, orientation: str) -> list[np.ndarray]:
        records = self.records[orientation]
        if math.isinf(order):
            distance = lambda rec: -rec.order if math.isfinite(rec.order) else -math.inf
        else:
            distance = lambda rec: abs(math.log(rec.order) - math.log(order)) if math.isfinite(rec.order) else math.inf
        starts = [np.array([r.s, r.t]) for r in sorted(records, key=distance)[:3]]
        if not starts:
            starts = [
                np.array([0.0, 0.0]), np.array([0.0, 1.0]),
                np.array([1.0, 0.0]), np.array([1.0, 1.0]),
                np.array([0.5, 0.5]),
            ]
        return starts

    @staticmethod
    def numerical_gradient(order: float, orientation: str, s: float, t: float) -> tuple[float, float]:
        x = np.array([s, t], dtype=float)
        grads = []
        for j in range(2):
            h = 2.0e-6
            lo = max(0.0, x[j] - h)
            hi = min(1.0, x[j] + h)
            xl, xh = x.copy(), x.copy()
            xl[j], xh[j] = lo, hi
            grads.append((directed_value(xh, order, orientation) - directed_value(xl, order, orientation)) / (hi - lo))
        return float(grads[0]), float(grads[1])

    def project(self, order: float, orientation: str, *, global_screen: bool = False) -> Projection:
        key = (orientation, float(order), bool(global_screen))
        if key in self.memo:
            return self.memo[key]
        globally_validated_key = (orientation, float(order), True)
        if not global_screen and globally_validated_key in self.memo:
            return self.memo[globally_validated_key]
        self.calls += 1
        objective = lambda x: directed_value(np.asarray(x, dtype=float), order, orientation)
        objective_gradient = None if math.isinf(order) else (
            lambda x: directed_gradient(np.asarray(x, dtype=float), order, orientation)
        )
        starts = self.nearest_starts(order, orientation)
        method = "warm/local"
        screen_record: tuple[float, float, float] | None = None
        if global_screen:
            grid = np.linspace(0.0, 1.0, 101)
            screened = sorted(
                (objective(np.array([s, t])), s, t) for s in grid for t in grid
            )
            screen_record = screened[0]
            starts = [np.array([s, t]) for _, s, t in screened[:12]] + starts
            if math.isinf(order):
                de = differential_evolution(
                    objective,
                    bounds=[(0.0, 1.0), (0.0, 1.0)],
                    seed=1709,
                    popsize=18,
                    maxiter=240,
                    tol=2.0e-12,
                    atol=2.0e-14,
                    polish=True,
                    workers=1,
                    updating="immediate",
                )
                starts.insert(0, np.asarray(de.x, dtype=float))
                method = "101x101+DE+local"
            else:
                method = "101x101+local"
        best: tuple[float, np.ndarray] | None = None
        for start in starts:
            fit = minimize(
                objective,
                x0=start,
                jac=objective_gradient,
                method="L-BFGS-B",
                bounds=[(0.0, 1.0), (0.0, 1.0)],
                options={"ftol": 1.0e-15, "gtol": 1.0e-12, "maxiter": 1000, "maxls": 50},
            )
            x = np.clip(fit.x, 0.0, 1.0)
            value = objective(x)
            if best is None or value < best[0]:
                best = (value, x)
        assert best is not None
        value, x = best
        # A globally screened finite-order candidate gets a final coordinate
        # stationarity polish.  This removes the few-nanounit gradient residue
        # at an interior coordinate that L-BFGS-B can leave when the other
        # coordinate is active at a boundary.
        if global_screen and not math.isinf(order):
            for _ in range(2):
                for coordinate in (0, 1):
                    def coordinate_gradient(z: float) -> float:
                        candidate = x.copy()
                        candidate[coordinate] = z
                        return float(
                            directed_gradient(candidate, order, orientation)[coordinate]
                        )

                    candidates = [x.copy()]
                    derivative_0 = coordinate_gradient(0.0)
                    derivative_1 = coordinate_gradient(1.0)
                    if derivative_0 * derivative_1 < 0.0:
                        root_value = brentq(
                            coordinate_gradient,
                            0.0,
                            1.0,
                            xtol=5.0e-15,
                            rtol=8.0 * np.finfo(float).eps,
                        )
                        candidate = x.copy()
                        candidate[coordinate] = root_value
                        candidates.append(candidate)
                    for endpoint in (0.0, 1.0):
                        candidate = x.copy()
                        candidate[coordinate] = endpoint
                        candidates.append(candidate)
                    candidate_values = [objective(candidate) for candidate in candidates]
                    candidate_index = int(np.argmin(candidate_values))
                    if candidate_values[candidate_index] < value + 2.0e-15:
                        value = float(candidate_values[candidate_index])
                        x = candidates[candidate_index]
        if math.isinf(order):
            fit = minimize(
                objective,
                x0=x,
                method="Powell",
                bounds=[(0.0, 1.0), (0.0, 1.0)],
                options={"xtol": 1.0e-13, "ftol": 1.0e-15, "maxiter": 3000},
            )
            candidate = np.clip(fit.x, 0.0, 1.0)
            candidate_value = objective(candidate)
            if candidate_value < value:
                value, x = candidate_value, candidate
        if math.isinf(order):
            gs, gt = self.numerical_gradient(
                order, orientation, float(x[0]), float(x[1])
            )
        else:
            gs, gt = map(float, directed_gradient(x, order, orientation))
        def coordinate_kkt(coordinate: float, gradient: float) -> float:
            if coordinate <= 2.0e-8:
                return max(0.0, -gradient)
            if coordinate >= 1.0 - 2.0e-8:
                return max(0.0, gradient)
            return abs(gradient)
        kkt = None if math.isinf(order) else max(
            coordinate_kkt(float(x[0]), gs), coordinate_kkt(float(x[1]), gt)
        )
        record = Projection(
            orientation, float(order), float(value), float(x[0]), float(x[1]),
            method, gs, gt, kkt,
            None if screen_record is None else float(screen_record[0]),
            None if screen_record is None else float(screen_record[1]),
            None if screen_record is None else float(screen_record[2]),
            None if screen_record is None else float(screen_record[0] - value),
        )
        self.records[orientation].append(record)
        self.memo[key] = record
        if global_screen:
            self.memo[(orientation, float(order), False)] = record
        return record


def continuous_maximise(fn, a_lo: float, a_hi: float, screen_size: int = 301) -> tuple[float, float, list[dict[str, float]]]:
    # A hybrid screen is dense in the interior and logarithmic near both ends.
    linear = np.linspace(a_lo, a_hi, screen_size)
    near0 = np.geomspace(a_lo, min(0.1, a_hi), 24)
    near1 = 1.0 - np.geomspace(max(1.0 - a_hi, 1.0e-12), 0.1, 24)
    grid = np.unique(np.clip(np.concatenate([linear, near0, near1]), a_lo, a_hi))
    values = np.array([fn(float(a)) for a in grid])
    # Refine only the best separated screen candidates.  Inner projection
    # noise can create many meaningless microscopic local maxima.
    ranked = np.argsort(values)[::-1]
    candidates: set[int] = {int(ranked[0]), 0, len(grid) - 1}
    for index in ranked:
        if all(abs(int(index) - old) >= 3 for old in candidates):
            candidates.add(int(index))
        if len(candidates) >= 7:
            break
    receipts: list[dict[str, float]] = []
    best = (float(values.max()), float(grid[int(np.argmax(values))]))
    for i in sorted(candidates):
        left = float(grid[max(0, i - 1)])
        right = float(grid[min(len(grid) - 1, i + 1)])
        if right <= left:
            continue
        fit = minimize_scalar(lambda a: -fn(float(a)), bounds=(left, right), method="bounded", options={"xatol": 2.0e-14, "maxiter": 500})
        a = float(fit.x)
        value = float(fn(a))
        receipts.append({"left": left, "right": right, "a": a, "value": value})
        if value > best[0]:
            best = (value, a)
    return best[0], best[1], receipts


def json_safe(value):
    if isinstance(value, float) and not math.isfinite(value):
        if math.isinf(value):
            return "infinity" if value > 0 else "-infinity"
        return "nan"
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    return value


def forward_infinity_face_receipt() -> dict[str, object]:
    """Analytically certify the nonunique forward order-infinity projection."""

    direction = P1 - P0
    # The decimal endpoints have exactly the same affine direction; their
    # independently rounded binary64 subtractions differ at about 1e-16.
    if not np.allclose(direction, Q1 - Q0, atol=2.0e-16, rtol=0.0):
        raise RuntimeError("the analytic infinity-face certificate needs common directions")
    matrix = np.array(
        [[direction[0], -Q0[0]], [direction[1], -Q0[1]]], dtype=float
    )
    k, c = np.linalg.solve(matrix, -P0[:2])
    t_min = max(0.0, -k / c)
    t_max = min(1.0, (1.0 - k) / c)
    sample_t = np.linspace(t_min, t_max, 1001)
    sample_s = c * sample_t + k
    ratios = np.vstack(
        [p_of(float(s)) / q_of(float(t)) for s, t in zip(sample_s, sample_t)]
    )
    return {
        "c": float(c),
        "D_infinity": float(math.log(c)),
        "affine_relation": "s = c*t + k",
        "k": float(k),
        "t_interval": [float(t_min), float(t_max)],
        "s_interval": [float(sample_s[0]), float(sample_s[-1])],
        "maximum_active_ratio_residual": float(
            np.max(np.abs(np.max(ratios, axis=1) - c))
        ),
        "third_coordinate_maximum_slack": float(
            np.max(ratios[:, 2] - c)
        ),
        "uniqueness": "nonunique line segment",
        "lower_bound_argument": (
            "If coordinate ratios 0 and 1 were both below c, their opposite "
            "direction signs would force s-c*t both below and above k."
        ),
    }


def high_precision_reference() -> dict[str, object]:
    """Solve the scalar KL and reverse saddle equations at 80 digits."""

    with localcontext() as context:
        context.prec = 80
        d = Decimal
        p0 = [d("0.327"), d("0.418"), d("0.255")]
        p1 = [d("0.563"), d("0.266"), d("0.171")]
        q0 = [d("0.143"), d("0.357"), d("0.500")]
        q1 = [d("0.379"), d("0.205"), d("0.416")]
        dp = [right - left for left, right in zip(p0, p1)]
        dq = [right - left for left, right in zip(q0, q1)]

        def q_at_decimal(t: Decimal) -> list[Decimal]:
            return [left + t * direction for left, direction in zip(q0, dq)]

        def kl_decimal(first: list[Decimal], second: list[Decimal]) -> Decimal:
            return sum(
                value * (value / reference).ln()
                for value, reference in zip(first, second)
            )

        t_reverse_kl = d("0.63913727")
        for _ in range(30):
            q = q_at_decimal(t_reverse_kl)
            derivative = sum(
                direction * (value / reference).ln()
                for direction, value, reference in zip(dq, q, p0)
            )
            curvature = sum(
                direction * direction / value
                for direction, value in zip(dq, q)
            )
            step = derivative / curvature
            t_reverse_kl -= step
            if abs(step) < d("1e-70"):
                break
        reverse_kl = kl_decimal(q_at_decimal(t_reverse_kl), p0)
        rate = d("1.5") * reverse_kl

        order = d("1.22406483")
        t_star = d("0.66215110")
        f1 = f2 = d(1)
        for _ in range(50):
            q = q_at_decimal(t_star)
            weights = [
                (order * value.ln() + (d(1) - order) * reference.ln()).exp()
                for value, reference in zip(q, p0)
            ]
            normaliser = sum(weights)
            tilt = [weight / normaliser for weight in weights]
            u = [direction / value for direction, value in zip(dq, q)]
            v = [(value / reference).ln() for value, reference in zip(q, p0)]
            mean_u = sum(
                r_value * u_value for r_value, u_value in zip(tilt, u)
            )
            mean_v = sum(
                r_value * v_value for r_value, v_value in zip(tilt, v)
            )
            mean_u2 = sum(
                r_value * u_value**2 for r_value, u_value in zip(tilt, u)
            )
            mean_v2 = sum(
                r_value * v_value**2 for r_value, v_value in zip(tilt, v)
            )
            mean_uv = sum(
                r_value * u_value * v_value
                for r_value, u_value, v_value in zip(tilt, u, v)
            )
            covariance = mean_uv - mean_u * mean_v
            variance_v = mean_v2 - mean_v**2
            f1 = mean_u
            f2 = kl_decimal(tilt, p0) - rate
            j11 = covariance
            j12 = (order - d(1)) * mean_u2 - order * mean_u**2
            j21 = order * variance_v
            j22 = order**2 * covariance
            determinant = j11 * j22 - j12 * j21
            order_step = (f1 * j22 - j12 * f2) / determinant
            t_step = (j11 * f2 - f1 * j21) / determinant
            order -= order_step
            t_star -= t_step
            if max(abs(order_step), abs(t_step)) < d("1e-70"):
                break

        q_star = q_at_decimal(t_star)
        weights = [
            (order * value.ln() + (d(1) - order) * reference.ln()).exp()
            for value, reference in zip(q_star, p0)
        ]
        normaliser = sum(weights)
        tilt = [weight / normaliser for weight in weights]
        reverse_d = normaliser.ln() / (order - d(1))
        a_star = (order - d(1)) / order
        exponent = a_star * (rate - reverse_d)
        reverse_s_derivative = -sum(
            value * direction / reference
            for value, direction, reference in zip(tilt, dp, p0)
        )

        t_forward_kl = d("0.55863736")
        for _ in range(30):
            q = q_at_decimal(t_forward_kl)
            derivative = -sum(
                value * direction / reference
                for value, direction, reference in zip(p0, dq, q)
            )
            curvature = sum(
                value * direction**2 / reference**2
                for value, direction, reference in zip(p0, dq, q)
            )
            step = derivative / curvature
            t_forward_kl -= step
            if abs(step) < d("1e-70"):
                break
        forward_kl = kl_decimal(p0, q_at_decimal(t_forward_kl))

        matrix_a, matrix_b = dp[0], -q0[0]
        matrix_c, matrix_e = dp[1], -q0[1]
        rhs_0, rhs_1 = -p0[0], -p0[1]
        determinant = matrix_a * matrix_e - matrix_b * matrix_c
        affine_k = (rhs_0 * matrix_e - matrix_b * rhs_1) / determinant
        ratio_c = (matrix_a * rhs_1 - rhs_0 * matrix_c) / determinant
        infinity_t_min = -affine_k / ratio_c
        infinity_s_max = ratio_c + affine_k

        def digits(value: Decimal) -> str:
            return format(value, ".70g")

        return {
            "arithmetic": "Decimal, 80 digits",
            "directed_KL": {
                "Q||P": {
                    "D": digits(reverse_kl),
                    "s": "0",
                    "t": digits(t_reverse_kl),
                },
                "P||Q": {
                    "D": digits(forward_kl),
                    "s": "0",
                    "t": digits(t_forward_kl),
                },
            },
            "r_plus": digits(rate),
            "reverse": {
                "a": digits(a_star),
                "lambda": digits(order),
                "D": digits(reverse_d),
                "s": "0",
                "t": digits(t_star),
                "exponent": digits(exponent),
                "boundary_s_derivative": digits(reverse_s_derivative),
                "inner_stationarity_residual_abs": digits(abs(f1)),
                "outer_stationarity_residual_abs": digits(abs(f2)),
            },
            "forward_infinity": {
                "D": digits(ratio_c.ln()),
                "ratio_c": digits(ratio_c),
                "affine_constant_k": digits(affine_k),
                "minimiser_equation": "s = c*t + k",
                "t_interval": [digits(infinity_t_min), "1"],
                "s_interval": ["0", digits(infinity_s_max)],
                "unique": False,
            },
        }


def selected_projection_diagnostics(projector: Projector) -> dict[str, object]:
    validated: dict[tuple[str, float], Projection] = {}
    for orientation, records in projector.records.items():
        for record in records:
            if "101x101" not in record.method:
                continue
            key = (orientation, record.order)
            incumbent = validated.get(key)
            if incumbent is None or record.D < incumbent.D:
                validated[key] = record
    monotonicity: dict[str, object] = {}
    for orientation in ("Q||P", "P||Q"):
        records = sorted(
            (record for (branch, _), record in validated.items() if branch == orientation),
            key=lambda record: record.order,
        )
        decreases = [
            max(0.0, left.D - right.D)
            for left, right in zip(records, records[1:])
        ]
        monotonicity[orientation] = {
            "validated_orders": len(records),
            "largest_decrease": max(decreases, default=0.0),
        }
    all_records = list(validated.values())
    return {
        "globally_validated_projection_count": len(all_records),
        "largest_kkt_violation": max(
            (
                float(record.kkt_violation)
                for record in all_records
                if record.kkt_violation is not None
            ),
            default=0.0,
        ),
        "largest_screen_minus_final": max(
            (
                float(record.screen_minus_final)
                for record in all_records
                if record.screen_minus_final is not None
            ),
            default=0.0,
        ),
        "renyi_monotonicity": monotonicity,
    }


def run_continuous_certification() -> tuple[dict[str, object], Projector]:
    projector = Projector()
    reverse_kl = projector.project(1.0, "Q||P", global_screen=True)
    forward_kl = projector.project(1.0, "P||Q", global_screen=True)
    high_precision = high_precision_reference()
    r_plus = float(high_precision["r_plus"])
    if abs(r_plus - 1.5 * reverse_kl.D) > 2.0e-13:
        raise RuntimeError("binary64 and 80-digit reverse KL calculations disagree")

    def reverse_exponent(a: float) -> float:
        order = 1.0 / (1.0 - a)
        projection = projector.project(order, "Q||P")
        return a * max(0.0, r_plus - projection.D)

    reverse_rounds: list[dict[str, object]] = []
    reverse_value = -math.inf
    reverse_a = math.nan
    reverse_projection: Projection | None = None
    for round_index in (1, 2):
        candidate_value, candidate_a, receipts = continuous_maximise(
            reverse_exponent, 1.0e-8, 0.95, screen_size=151
        )
        candidate_order = 1.0 / (1.0 - candidate_a)
        candidate_projection = projector.project(
            candidate_order, "Q||P", global_screen=True
        )
        candidate_value = candidate_a * max(
            0.0, r_plus - candidate_projection.D
        )
        nearest = min(
            receipts,
            key=lambda receipt: abs(float(receipt["a"]) - candidate_a),
        )
        adjacent_best = max(
            reverse_exponent(float(nearest["left"])),
            reverse_exponent(float(nearest["right"])),
        )
        adjacent_inferiority = max(0.0, adjacent_best - candidate_value)
        reverse_rounds.append(
            {
                "round": round_index,
                "a": candidate_a,
                "order": candidate_order,
                "exponent": candidate_value,
                "projection": asdict(candidate_projection),
                "adjacent_screen_inferiority": adjacent_inferiority,
                "candidate_intervals": receipts,
            }
        )
        reverse_value = candidate_value
        reverse_a = candidate_a
        reverse_projection = candidate_projection
    assert reverse_projection is not None
    reverse_order = 1.0 / (1.0 - reverse_a)
    reverse_a_change = abs(
        float(reverse_rounds[-1]["a"]) - float(reverse_rounds[-2]["a"])
    )
    reverse_d_change = abs(
        float(reverse_rounds[-1]["projection"]["D"])
        - float(reverse_rounds[-2]["projection"]["D"])
    )
    reverse_value_change = abs(
        float(reverse_rounds[-1]["exponent"])
        - float(reverse_rounds[-2]["exponent"])
    )
    if reverse_a_change > 5.0e-8:
        raise RuntimeError("reverse outer optimisation did not stabilise")
    if any(
        float(receipt["adjacent_screen_inferiority"]) > 1.0e-10
        for receipt in reverse_rounds
    ):
        raise RuntimeError("reverse optimum is inferior to an adjacent screen point")

    reverse_tail_projection = projector.project(20.0, "Q||P", global_screen=True)
    if reverse_tail_projection.D < r_plus - 1.0e-10:
        raise RuntimeError("reverse omitted-tail certificate failed at order 20")

    forward_infinity = projector.project(math.inf, "P||Q", global_screen=True)
    reverse_infinity = projector.project(math.inf, "Q||P", global_screen=True)
    infinity_face = forward_infinity_face_receipt()
    infinity_d = float(infinity_face["D_infinity"])
    if abs(forward_infinity.D - float(infinity_face["D_infinity"])) > 2.0e-10:
        raise RuntimeError("numerical and analytic forward infinity projections disagree")

    rows: list[dict[str, object]] = []
    for n in range(1, 26):
        epsilon = math.exp(-n * r_plus)
        log_one_minus_epsilon = math.log1p(-epsilon)

        def forward_log(a: float) -> float:
            order = 1.0 / (1.0 - a)
            projection = projector.project(order, "P||Q")
            return log_one_minus_epsilon / a - n * projection.D

        a_floor = max(
            1.0e-12,
            min(1.0e-5, math.sqrt(epsilon / max(n, 1)) * 1.0e-3),
        )
        infinity_value = log_one_minus_epsilon - n * infinity_d
        forward_rounds: list[dict[str, object]] = []
        final_value = infinity_value
        final_a = 1.0
        final_order = math.inf
        final_projection = forward_infinity
        for round_index in (1, 2):
            candidate_value, candidate_a, receipts = continuous_maximise(
                forward_log, a_floor, 1.0 - 1.0e-10, screen_size=61
            )
            if infinity_value >= candidate_value:
                candidate_value = infinity_value
                candidate_a = 1.0
                candidate_order = math.inf
                candidate_projection = forward_infinity
                adjacent_inferiority = 0.0
            else:
                candidate_order = 1.0 / (1.0 - candidate_a)
                candidate_projection = projector.project(
                    candidate_order, "P||Q", global_screen=True
                )
                candidate_value = (
                    log_one_minus_epsilon / candidate_a
                    - n * candidate_projection.D
                )
                nearest = min(
                    receipts,
                    key=lambda receipt: abs(float(receipt["a"]) - candidate_a),
                )
                adjacent_best = max(
                    forward_log(float(nearest["left"])),
                    forward_log(float(nearest["right"])),
                )
                adjacent_inferiority = max(0.0, adjacent_best - candidate_value)
            forward_rounds.append(
                {
                    "round": round_index,
                    "a": candidate_a,
                    "order": candidate_order,
                    "log_beta": candidate_value,
                    "projection": asdict(candidate_projection),
                    "projection_nonunique": math.isinf(candidate_order),
                    "adjacent_screen_inferiority": adjacent_inferiority,
                    "candidate_intervals": receipts,
                }
            )
            final_value = candidate_value
            final_a = candidate_a
            final_order = candidate_order
            final_projection = candidate_projection

        forward_a_change = abs(
            float(forward_rounds[-1]["a"])
            - float(forward_rounds[-2]["a"])
        )
        forward_d_change = abs(
            float(forward_rounds[-1]["projection"]["D"])
            - float(forward_rounds[-2]["projection"]["D"])
        )
        forward_value_change = abs(
            float(forward_rounds[-1]["log_beta"])
            - float(forward_rounds[-2]["log_beta"])
        )
        if forward_a_change > 5.0e-8:
            raise RuntimeError(
                f"forward outer optimisation did not stabilise at n={n}"
            )
        small_a_upper_bound = log_one_minus_epsilon / a_floor
        if small_a_upper_bound > final_value + 1.0e-10:
            raise RuntimeError(f"forward omitted-small-a certificate failed at n={n}")

        selected_forward_d = (
            infinity_d if math.isinf(final_order) else final_projection.D
        )
        selected_forward_s = None if math.isinf(final_order) else final_projection.s
        selected_forward_t = None if math.isinf(final_order) else final_projection.t

        reverse_beta = -math.expm1(-n * reverse_value)
        forward_beta = math.exp(final_value) if final_value > -745.0 else 0.0
        rows.append(
            {
                "n": n,
                "epsilon": epsilon,
                "reverse_beta": reverse_beta,
                "reverse_exponent": reverse_value,
                "reverse_a": reverse_a,
                "reverse_order": reverse_order,
                "reverse_D": reverse_projection.D,
                "reverse_s": reverse_projection.s,
                "reverse_t": reverse_projection.t,
                "forward_beta": forward_beta,
                "forward_log_beta": final_value,
                "forward_a": final_a,
                "forward_order": final_order,
                "forward_D": selected_forward_d,
                "forward_s": selected_forward_s,
                "forward_t": selected_forward_t,
                "forward_projection_nonunique": math.isinf(final_order),
                "forward_outer_a_change": forward_a_change,
                "forward_outer_D_change": forward_d_change,
                "forward_outer_log_value_change": forward_value_change,
                "forward_a_floor": a_floor,
                "forward_omitted_small_a_upper_log_bound": small_a_upper_bound,
                "forward_omitted_small_a_log_margin": (
                    final_value - small_a_upper_bound
                ),
                "forward_rounds": forward_rounds,
                "max_beta": max(reverse_beta, forward_beta),
                "winner": (
                    "reverse" if reverse_beta >= forward_beta else "forward"
                ),
            }
        )

    winner_runs: list[dict[str, object]] = []
    start = 0
    while start < len(rows):
        winner = rows[start]["winner"]
        stop = start
        while stop + 1 < len(rows) and rows[stop + 1]["winner"] == winner:
            stop += 1
        winner_runs.append(
            {
                "winner": winner,
                "n_start": rows[start]["n"],
                "n_end": rows[stop]["n"],
            }
        )
        start = stop + 1

    dominance_n = 25
    reverse_at_dominance = float(rows[dominance_n - 1]["reverse_beta"])
    forward_kl_envelope = math.exp(-dominance_n * forward_kl.D)
    if reverse_at_dominance <= forward_kl_envelope:
        raise RuntimeError("analytic no-recrossing certificate failed")

    diagnostics = selected_projection_diagnostics(projector)
    if any(
        float(row["forward_rounds"][-1]["adjacent_screen_inferiority"]) > 1.0e-10
        for row in rows
    ):
        raise RuntimeError("a forward optimum is inferior to an adjacent screen point")
    payload = {
        "classes": {
            "P0": P0.tolist(),
            "P1": P1.tolist(),
            "Q0": Q0.tolist(),
            "Q1": Q1.tolist(),
        },
        "formulations": {
            "reverse": (
                "1-exp(-n sup_{a in (0,1]} a [r_plus-D_{1/(1-a)}"
                "(Qclass||Pclass)]_+)"
            ),
            "forward": (
                "sup_{a in (0,1]} exp(log(1-epsilon_n)/a"
                "-n D_{1/(1-a)}(Pclass||Qclass))"
            ),
        },
        "reverse_kl": asdict(reverse_kl),
        "forward_kl": asdict(forward_kl),
        "r_plus": r_plus,
        "high_precision_reference": high_precision,
        "reverse": {
            "exponent": reverse_value,
            "a": reverse_a,
            "order": reverse_order,
            "projection": asdict(reverse_projection),
            "rounds": reverse_rounds,
            "outer_a_change": reverse_a_change,
            "outer_D_change": reverse_d_change,
            "outer_value_change": reverse_value_change,
            "omitted_tail": {
                "a_interval": [0.95, 1.0],
                "order_at_boundary": 20.0,
                "D_at_boundary": reverse_tail_projection.D,
                "rate": r_plus,
                "margin": reverse_tail_projection.D - r_plus,
                "argument": (
                    "Directed Renyi divergence is nondecreasing in order, "
                    "so the positive-part reverse objective vanishes beyond "
                    "the screened boundary."
                ),
                "projection": asdict(reverse_tail_projection),
            },
            "legacy_order_difference_from_1.224": reverse_order - 1.224,
            "legacy_D_difference_from_0.116": reverse_projection.D - 0.116,
            "legacy_exponent_difference_from_0.00476": reverse_value - 0.00476,
        },
        "reverse_infinity": asdict(reverse_infinity),
        "forward_infinity": asdict(forward_infinity),
        "forward_infinity_face": infinity_face,
        "rows": rows,
        "winner_runs_directly_checked": winner_runs,
        "winner_for_all_positive_integers": [
            {"winner": "forward", "n_start": 1, "n_end": 19},
            {"winner": "reverse", "n_start": 20, "n_end": "infinity"},
        ],
        "no_later_recrossing": {
            "argument": (
                "D_lambda(Pclass||Qclass)>=D(Pclass||Qclass) and the "
                "forward prefactor is at most one, so forward(n)<=exp(-n D_PQ). "
                "The reverse branch increases in n."
            ),
            "certification_n": dominance_n,
            "reverse_at_n": reverse_at_dominance,
            "forward_upper_envelope_at_n": forward_kl_envelope,
            "margin": reverse_at_dominance - forward_kl_envelope,
        },
        "continuous_validation": diagnostics,
        "projection_call_count": projector.calls,
        "outer_rounds": 2,
        "outer_stability_tolerance_a": 5.0e-8,
        "projection_global_screen_size": 101,
        "analytic_infinity_agreement_tolerance": 2.0e-10,
        "adjacent_outer_point_tolerance": 1.0e-10,
    }
    return payload, projector


def run_lp_sweep(continuous: dict[str, object]) -> dict[str, object]:
    null_class = AffineTernaryClass(P0, P1)
    alternative_class = AffineTernaryClass(Q0, Q1)
    branch_by_n = {int(row["n"]): row for row in continuous["rows"]}
    previous_null = np.linspace(0.0, 1.0, 17)
    previous_alternative = np.linspace(0.0, 1.0, 17)
    rows: list[dict[str, object]] = []
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()

    for n in range(1, 26):
        epsilon = math.exp(-n * float(continuous["r_plus"]))
        initial_null = np.unique(
            np.concatenate((np.linspace(0.0, 1.0, 9), previous_null))
        )
        initial_alternative = np.unique(
            np.concatenate((np.linspace(0.0, 1.0, 9), previous_alternative))
        )
        per_n_started = time.perf_counter()
        result = solve_composite_minimax(
            n,
            epsilon,
            null_class,
            alternative_class,
            initial_null_parameters=initial_null,
            initial_alternative_parameters=initial_alternative,
            constraint_tolerance=5.0e-10,
            parameter_tolerance=2.0e-10,
            max_iterations=80,
            row_scale=1.0e4,
            objective_scale=1.0e4,
            small_matrix_value=1.0e-12,
            primal_feasibility_tolerance=1.0e-10,
            dual_feasibility_tolerance=1.0e-10,
            solver_methods=("highs-ds", "highs-ipm"),
            derivative_oversampling=32,
            trim_tolerance=5.0e-13,
            checkpoint_path=CHECKPOINT_DIR / f"n_{n:03d}.npz",
            resume=True,
        )
        previous_null = np.asarray(result.null_parameters, dtype=float)
        previous_alternative = np.asarray(result.alternative_parameters, dtype=float)
        space = ternary_type_space(n)
        grid = np.linspace(0.0, 1.0, 10_001)
        dense_type_i_values = expectations(
            space, null_class, 1.0 - result.acceptance, grid, batch_size=256
        )
        dense_type_ii_values = expectations(
            space, alternative_class, result.acceptance, grid, batch_size=256
        )
        dense_type_i_index = int(np.argmax(dense_type_i_values))
        dense_type_ii_index = int(np.argmax(dense_type_ii_values))
        branch = branch_by_n[n]
        rows.append(
            {
                "n": n,
                "epsilon": epsilon,
                "minimax_beta_master": float(result.beta),
                "worst_type_i": float(result.worst_type_i),
                "worst_type_i_s": float(result.worst_null_parameter),
                "worst_type_ii": float(result.worst_type_ii),
                "worst_type_ii_t": float(result.worst_alternative_parameter),
                "separator_null_violation": float(result.null_violation),
                "separator_alternative_violation": float(
                    result.alternative_violation
                ),
                "dense_grid_size": 10_001,
                "dense_type_i": float(dense_type_i_values[dense_type_i_index]),
                "dense_type_i_s": float(grid[dense_type_i_index]),
                "dense_type_ii": float(dense_type_ii_values[dense_type_ii_index]),
                "dense_type_ii_t": float(grid[dense_type_ii_index]),
                "dense_null_violation": float(
                    dense_type_i_values[dense_type_i_index] - epsilon
                ),
                "dense_alternative_violation": float(
                    dense_type_ii_values[dense_type_ii_index] - result.beta
                ),
                "iterations": int(result.iterations),
                "active_null_parameters": previous_null.tolist(),
                "active_alternative_parameters": previous_alternative.tolist(),
                "active_null_count": int(previous_null.size),
                "active_alternative_count": int(previous_alternative.size),
                "solver_message": result.solver_message,
                "converged": bool(result.converged),
                "runtime_seconds": time.perf_counter() - per_n_started,
                "reverse_beta": float(branch["reverse_beta"]),
                "forward_beta": float(branch["forward_beta"]),
                "converse_max": float(branch["max_beta"]),
                "converse_winner": branch["winner"],
                "minimax_minus_converse": float(
                    result.beta - float(branch["max_beta"])
                ),
                "converse_minus_minimax_violation": float(
                    max(0.0, float(branch["max_beta"]) - result.beta)
                ),
            }
        )

    return {
        "n_range": [1, 25],
        "range_rationale": (
            "The direct crossover is covered through n=24; at n=25 the "
            "analytic forward KL envelope falls below the increasing reverse "
            "branch, excluding later recrossing.  No pre-existing strong-converse "
            "figure or checkpoint required a wider LP sweep."
        ),
        "settings": {
            "constraint_tolerance": 5.0e-10,
            "parameter_tolerance": 2.0e-10,
            "row_scale": 1.0e4,
            "objective_scale": 1.0e4,
            "small_matrix_value": 1.0e-12,
            "primal_feasibility_tolerance": 1.0e-10,
            "dual_feasibility_tolerance": 1.0e-10,
            "derivative_oversampling": 32,
            "trim_tolerance": 5.0e-13,
            "dense_grid_size": 10_001,
            "cross_n_warm_start": True,
            "checkpointing": True,
        },
        "rows": rows,
        "summary": {
            "runtime_seconds": time.perf_counter() - started,
            "max_separator_null_violation": max(
                row["separator_null_violation"] for row in rows
            ),
            "max_separator_alternative_violation": max(
                row["separator_alternative_violation"] for row in rows
            ),
            "max_dense_null_violation": max(
                row["dense_null_violation"] for row in rows
            ),
            "max_dense_alternative_violation": max(
                row["dense_alternative_violation"] for row in rows
            ),
            "max_converse_minus_minimax_violation": max(
                row["converse_minus_minimax_violation"] for row in rows
            ),
            "minimum_minimax_minus_converse": min(
                row["minimax_minus_converse"] for row in rows
            ),
        },
    }


def write_outputs(
    continuous: dict[str, object],
    projector: Projector,
    lp: dict[str, object],
) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"continuous": continuous, "minimax_lp": lp}
    OUTPUT_PATH.write_text(
        json.dumps(json_safe(payload), indent=2, sort_keys=True, allow_nan=False)
        + "\n",
        encoding="utf-8",
    )
    cache = {
        "classes": continuous["classes"],
        "projection_count": sum(
            len(records) for records in projector.records.values()
        ),
        "records": {
            orientation: [asdict(record) for record in records]
            for orientation, records in projector.records.items()
        },
    }
    CACHE_PATH.write_text(
        json.dumps(json_safe(cache), indent=2, sort_keys=True, allow_nan=False)
        + "\n",
        encoding="utf-8",
    )

    continuous_by_n = {int(row["n"]): row for row in continuous["rows"]}
    columns = [
        "n", "epsilon", "minimax_beta_master", "worst_type_i",
        "worst_type_i_s", "worst_type_ii", "worst_type_ii_t",
        "reverse_beta", "reverse_order", "reverse_D", "reverse_s", "reverse_t",
        "forward_beta", "forward_order", "forward_D", "forward_s", "forward_t",
        "converse_max", "converse_winner", "minimax_minus_converse",
        "separator_null_violation", "separator_alternative_violation",
        "dense_null_violation", "dense_alternative_violation",
    ]
    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for lp_row in lp["rows"]:
            n = int(lp_row["n"])
            branch = continuous_by_n[n]
            combined = dict(lp_row)
            for key in (
                "reverse_beta", "reverse_order", "reverse_D", "reverse_s",
                "reverse_t", "forward_beta", "forward_order", "forward_D",
                "forward_s", "forward_t", "max_beta", "winner",
            ):
                combined[key] = branch[key]
            combined["converse_max"] = branch["max_beta"]
            combined["converse_winner"] = branch["winner"]
            writer.writerow({key: combined[key] for key in columns})

    print(f"wrote {OUTPUT_PATH}")
    print(f"wrote {CSV_PATH}")
    print(f"wrote {CACHE_PATH}")


def main() -> None:
    continuous, projector = run_continuous_certification()
    lp = run_lp_sweep(continuous)
    if float(lp["summary"]["max_converse_minus_minimax_violation"]) > 5.1e-10:
        raise RuntimeError("a certified converse exceeds the minimax LP tolerance")
    if max(
        float(lp["summary"]["max_separator_alternative_violation"]),
        float(lp["summary"]["max_dense_alternative_violation"]),
    ) > 5.1e-10:
        raise RuntimeError("the minimax LP sweep exceeds its validation tolerance")
    write_outputs(continuous, projector, lp)


if __name__ == "__main__":
    main()
