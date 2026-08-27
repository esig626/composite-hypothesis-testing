#!/usr/bin/env python3
"""Reproduce and certify the subcritical ternary saddle and n=20 gap table.

The driver imports the repository's semi-infinite LP implementation, performs
continuous cached outer-order optimisation with globally screened selected
projections, and independently solves the saddle equations at 80 digits.

Example (from the repository root):

    python numerics/scripts/ternary_subcritical_certification.py

The default run adds the 1001-by-1001 global KL/Rényi screens, cached continuous
outer search, nested min-max check, and 100-order Rényi monotonicity diagnostic.
The LP, projected-test envelopes, corrected bound, and dense checks always run.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import sys
from decimal import Decimal, localcontext
from pathlib import Path
from types import ModuleType
from typing import Callable

import numpy as np
from scipy.optimize import (
    brentq,
    differential_evolution,
    minimize,
    minimize_scalar,
    root,
)


P0 = np.asarray([0.327, 0.418, 0.255], dtype=float)
P1 = np.asarray([0.563, 0.266, 0.171], dtype=float)
Q0 = np.asarray([0.143, 0.357, 0.500], dtype=float)
Q1 = np.asarray([0.379, 0.205, 0.416], dtype=float)
DP = P1 - P0
DQ = Q1 - Q0
N = 20
ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "numerics" / "data"
DEFAULT_JSON = DATA_DIR / "ternary_subcritical_certification.json"
DEFAULT_CSV = DATA_DIR / "ternary_subcritical_n20_gap.csv"
DEFAULT_CACHE = DATA_DIR / "ternary_subcritical_projection_cache.json"


def p_at(s: float | np.ndarray) -> np.ndarray:
    return P0 + np.asarray(s)[..., None] * DP


def q_at(t: float | np.ndarray) -> np.ndarray:
    return Q0 + np.asarray(t)[..., None] * DQ


def kl(q: np.ndarray, p: np.ndarray) -> float:
    return float(np.dot(q, np.log(q / p)))


def renyi(order: float, q: np.ndarray, p: np.ndarray) -> float:
    z = float(np.sum(q**order * p ** (1.0 - order)))
    return math.log(z) / (order - 1.0)


def load_affine_solver(path: Path) -> ModuleType:
    path = path.resolve()
    if not path.is_file():
        raise FileNotFoundError(f"LP solver not found: {path}")
    spec = importlib.util.spec_from_file_location("part_a_affine_ternary_lp", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot import LP solver: {path}")
    module = importlib.util.module_from_spec(spec)
    # Dataclasses inspect sys.modules while the module body is executing.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def solve_stationary_saddle() -> dict[str, object]:
    # At the numerically selected lower boundary s=0, the KL derivative in t is
    # sum_i DQ_i log(Q_t(i)/P0(i)), because sum_i DQ_i=0.
    t_kl = brentq(
        lambda t: float(np.dot(DQ, np.log(q_at(t) / P0))),
        0.0,
        1.0,
        xtol=5.0e-15,
        rtol=8.0 * np.finfo(float).eps,
    )
    d_kl = kl(q_at(t_kl), P0)
    rate = 0.35 * d_kl

    # The two saddle equations are the t projection stationarity condition and
    # Hoeffding rate matching D(R_lambda || P0)=r.
    def equations(x: np.ndarray) -> np.ndarray:
        order, t = map(float, x)
        q = q_at(t)
        unnormalised = q**order * P0 ** (1.0 - order)
        tilt = unnormalised / unnormalised.sum()
        return np.asarray(
            [
                np.dot(tilt, DQ / q),
                kl(tilt, P0) - rate,
            ]
        )

    stationary = root(
        equations,
        np.asarray([0.60143751, 0.60284348]),
        method="lm",
        options={"ftol": 1.0e-15, "xtol": 1.0e-15, "gtol": 1.0e-15, "maxiter": 5000},
    )
    if not stationary.success:
        raise RuntimeError(stationary.message)
    order, t_star = map(float, stationary.x)
    q_star = q_at(t_star)
    z = float(np.sum(q_star**order * P0 ** (1.0 - order)))
    d_order = math.log(z) / (order - 1.0)
    exponent = (1.0 - order) / order * (d_order - rate)
    tilt = q_star**order * P0 ** (1.0 - order) / z

    # Local curvature/directional-derivative receipts used only as numerical
    # evidence of uniqueness.  They are not a theorem.
    kl_s_direction = -float(np.dot(q_at(t_kl), DP / P0))
    kl_t_curvature = float(np.dot(DQ * DQ, 1.0 / q_at(t_kl)))
    renyi_s_direction = -float(np.dot(tilt, DP / P0))
    renyi_t_curvature = order * float(np.dot(tilt, (DQ / q_star) ** 2))

    h = 3.0e-5

    def fixed_pair_objective(candidate_order: float) -> float:
        return (1.0 - candidate_order) / candidate_order * (
            renyi(candidate_order, q_star, P0) - rate
        )

    outer_curvature = (
        fixed_pair_objective(order + h)
        - 2.0 * fixed_pair_objective(order)
        + fixed_pair_objective(order - h)
    ) / h**2

    return {
        "kl_t": t_kl,
        "kl_divergence": d_kl,
        "rate": rate,
        "lambda": order,
        "s_star": 0.0,
        "t_star": t_star,
        "renyi_divergence": d_order,
        "exponent": exponent,
        "tilt": tilt.tolist(),
        "tilt_D_to_P": kl(tilt, P0),
        "tilt_D_to_Q": kl(tilt, q_star),
        "stationarity_residual": np.asarray(equations(stationary.x)).tolist(),
        "kl_s_boundary_derivative": kl_s_direction,
        "kl_t_curvature": kl_t_curvature,
        "renyi_s_boundary_derivative": renyi_s_direction,
        "renyi_t_curvature": renyi_t_curvature,
        "outer_curvature": outer_curvature,
    }


def solve_stationary_saddle_decimal() -> dict[str, str]:
    """Repeat the stationarity solve at 80-decimal-digit precision.

    Decimal supplies correctly rounded logarithm and exponential operations.
    The two-by-two Newton Jacobian is analytic.  These strings certify the
    double-precision values subsequently used to enumerate ternary types.
    """

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

        def kl_decimal(q: list[Decimal], p: list[Decimal]) -> Decimal:
            return sum(value * (value / reference).ln() for value, reference in zip(q, p))

        t_kl = d("0.63913727")
        for _ in range(30):
            q = q_at_decimal(t_kl)
            derivative = sum(
                direction * (value / reference).ln()
                for direction, value, reference in zip(dq, q, p0)
            )
            curvature = sum(direction * direction / value for direction, value in zip(dq, q))
            step = derivative / curvature
            t_kl -= step
            if abs(step) < d("1e-70"):
                break
        d_kl = kl_decimal(q_at_decimal(t_kl), p0)
        rate = d("0.35") * d_kl

        order = d("0.60143752")
        t_star = d("0.60284346")
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
            mean_u = sum(r_value * u_value for r_value, u_value in zip(tilt, u))
            mean_v = sum(r_value * v_value for r_value, v_value in zip(tilt, v))
            mean_u2 = sum(r_value * u_value**2 for r_value, u_value in zip(tilt, u))
            mean_v2 = sum(r_value * v_value**2 for r_value, v_value in zip(tilt, v))
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
        d_order = normaliser.ln() / (order - d(1))
        exponent = (d(1) - order) / order * (d_order - rate)

        def digits(value: Decimal) -> str:
            return format(value, ".70g")

        return {
            "kl_t": digits(t_kl),
            "kl_divergence": digits(d_kl),
            "rate": digits(rate),
            "lambda": digits(order),
            "s_star": "0",
            "t_star": digits(t_star),
            "renyi_divergence": digits(d_order),
            "exponent": digits(exponent),
            "tilt_0": digits(tilt[0]),
            "tilt_1": digits(tilt[1]),
            "tilt_2": digits(tilt[2]),
            "tilt_D_to_P": digits(kl_decimal(tilt, p0)),
            "tilt_D_to_Q": digits(kl_decimal(tilt, q_star)),
        }


def full_square_screen(
    objective: Callable[[np.ndarray, np.ndarray], np.ndarray],
    grid_size: int = 1001,
) -> dict[str, float]:
    grid = np.linspace(0.0, 1.0, grid_size)
    best = (math.inf, math.nan, math.nan)
    for s_start in range(0, grid_size, 25):
        s_values = grid[s_start : s_start + 25]
        p = P0[None, None, :] + s_values[:, None, None] * DP[None, None, :]
        for t_start in range(0, grid_size, 100):
            t_values = grid[t_start : t_start + 100]
            q = Q0[None, None, :] + t_values[None, :, None] * DQ[None, None, :]
            values = objective(q, p)
            index = np.unravel_index(int(np.argmin(values)), values.shape)
            value = float(values[index])
            if value < best[0]:
                best = (value, float(s_values[index[0]]), float(t_values[index[1]]))
    return {"value": best[0], "s": best[1], "t": best[2], "grid_size": grid_size}


def global_projection_receipts(saddle: dict[str, object]) -> dict[str, object]:
    order = float(saddle["lambda"])

    kl_screen = full_square_screen(
        lambda q, p: np.sum(q * np.log(q / p), axis=-1)
    )
    renyi_screen = full_square_screen(
        lambda q, p: np.log(np.sum(q**order * p ** (1.0 - order), axis=-1))
        / (order - 1.0)
    )

    def kl_pair(x: np.ndarray) -> float:
        return kl(q_at(float(x[1])), p_at(float(x[0])))

    def renyi_pair(x: np.ndarray) -> float:
        return renyi(order, q_at(float(x[1])), p_at(float(x[0])))

    polished: dict[str, object] = {}
    for name, objective in (("kl", kl_pair), ("renyi", renyi_pair)):
        result = differential_evolution(
            objective,
            [(0.0, 1.0), (0.0, 1.0)],
            tol=1.0e-12,
            atol=1.0e-14,
            popsize=40,
            maxiter=2000,
            polish=False,
            seed=20260827,
        )
        polished[name] = {
            "value": float(result.fun),
            "s": float(result.x[0]),
            "t": float(result.x[1]),
            "evaluations": int(result.nfev),
        }
    return {"kl_screen": kl_screen, "renyi_screen": renyi_screen, "global_de": polished}


class SubcriticalProjectionCache:
    """Nearest-order warm starts and receipts for the Q-class || P-class profile."""

    def __init__(self) -> None:
        self.records: dict[float, dict[str, object]] = {}
        self.projection_calls = 0
        self.cache_hits = 0
        self.global_polishes = 0

    def nearest_starts(self, order: float) -> list[np.ndarray]:
        records = sorted(
            self.records.values(),
            key=lambda record: abs(float(record["order"]) - order),
        )
        starts = [
            np.asarray([float(record["s"]), float(record["t"])])
            for record in records[:3]
        ]
        if not starts:
            starts = [
                np.asarray([0.0, 0.0]),
                np.asarray([0.0, 1.0]),
                np.asarray([1.0, 0.0]),
                np.asarray([1.0, 1.0]),
                np.asarray([0.5, 0.5]),
            ]
        return starts

    def project(self, order: float, *, global_screen: bool = False) -> dict[str, object]:
        if not 0.0 < order < 1.0:
            raise ValueError("subcritical projections require 0 < order < 1")
        prior = self.records.get(float(order))
        if prior is not None and (not global_screen or bool(prior["globally_screened"])):
            self.cache_hits += 1
            return prior

        self.projection_calls += 1
        objective = lambda x: renyi(
            order, q_at(float(x[1])), p_at(float(x[0]))
        )
        starts = self.nearest_starts(order)
        screen: dict[str, float] | None = None
        de_evaluations = 0
        method = "nearest-three-plus-local"
        if global_screen:
            self.global_polishes += 1
            screen = full_square_screen(
                lambda q, p: np.log(
                    np.sum(q**order * p ** (1.0 - order), axis=-1)
                )
                / (order - 1.0),
                grid_size=1001,
            )
            starts.insert(0, np.asarray([screen["s"], screen["t"]]))
            global_result = differential_evolution(
                objective,
                [(0.0, 1.0), (0.0, 1.0)],
                tol=1.0e-12,
                atol=1.0e-14,
                popsize=30,
                maxiter=1000,
                polish=False,
                seed=1907,
            )
            starts.insert(0, np.asarray(global_result.x, dtype=float))
            de_evaluations = int(global_result.nfev)
            method = "1001x1001-plus-DE-plus-local"

        best_value = math.inf
        best_x = np.asarray([math.nan, math.nan])
        for start in starts:
            result = minimize(
                objective,
                start,
                method="L-BFGS-B",
                bounds=[(0.0, 1.0), (0.0, 1.0)],
                options={
                    "ftol": 1.0e-15,
                    "gtol": 1.0e-12,
                    "maxiter": 1000,
                    "maxls": 50,
                },
            )
            x = np.clip(result.x, 0.0, 1.0)
            value = objective(x)
            if value < best_value:
                best_value, best_x = float(value), x

        record: dict[str, object] = {
            "order": float(order),
            "D": best_value,
            "s": float(best_x[0]),
            "t": float(best_x[1]),
            "method": method,
            "globally_screened": global_screen,
            "global_DE_evaluations": de_evaluations,
        }
        if screen is not None:
            record.update(
                {
                    "screen_grid_size": int(screen["grid_size"]),
                    "screen_D": float(screen["value"]),
                    "screen_s": float(screen["s"]),
                    "screen_t": float(screen["t"]),
                    "screen_minus_final": float(screen["value"] - best_value),
                }
            )
        self.records[float(order)] = record
        return record

    def payload(self) -> dict[str, object]:
        return {
            "classes": {
                "P0": P0.tolist(),
                "P1": P1.tolist(),
                "Q0": Q0.tolist(),
                "Q1": Q1.tolist(),
            },
            "orientation": "Qclass||Pclass",
            "record_count": len(self.records),
            "projection_calls": self.projection_calls,
            "cache_hits": self.cache_hits,
            "global_polishes": self.global_polishes,
            "records": sorted(self.records.values(), key=lambda record: record["order"]),
        }


def continuous_outer_receipt(
    saddle: dict[str, object],
) -> tuple[dict[str, object], dict[str, object]]:
    """Continuously maximise the cached max-min profile in two polish rounds."""

    rate = float(saddle["rate"])
    cache = SubcriticalProjectionCache()

    def objective(order: float) -> float:
        projection = cache.project(float(order))
        return (1.0 - order) / order * (float(projection["D"]) - rate)

    screen_orders = np.unique(
        np.concatenate(
            (
                np.linspace(0.02, 0.98, 81),
                np.asarray([float(saddle["lambda"])]),
            )
        )
    )
    rounds: list[dict[str, object]] = []
    for round_index in (1, 2):
        values = np.asarray([objective(float(order)) for order in screen_orders])
        screen_index = int(np.argmax(values))
        left = float(screen_orders[max(0, screen_index - 1)])
        right = float(screen_orders[min(len(screen_orders) - 1, screen_index + 1)])
        refined = minimize_scalar(
            lambda order: -objective(float(order)),
            bounds=(left, right),
            method="bounded",
            options={"xatol": 2.0e-13, "maxiter": 1000},
        )
        selected_order = float(refined.x)
        before_global = cache.project(selected_order)
        selected_projection = cache.project(selected_order, global_screen=True)
        selected_value = (1.0 - selected_order) / selected_order * (
            float(selected_projection["D"]) - rate
        )
        adjacent_best = max(objective(left), objective(right))
        rounds.append(
            {
                "round": round_index,
                "order": selected_order,
                "value": selected_value,
                "projection": selected_projection,
                "global_D_improvement": float(before_global["D"])
                - float(selected_projection["D"]),
                "screen_bracket": [left, right],
                "adjacent_screen_inferiority": max(0.0, adjacent_best - selected_value),
            }
        )

    order_change = abs(float(rounds[-1]["order"]) - float(rounds[-2]["order"]))
    divergence_change = abs(
        float(rounds[-1]["projection"]["D"])
        - float(rounds[-2]["projection"]["D"])
    )
    value_change = abs(float(rounds[-1]["value"]) - float(rounds[-2]["value"]))
    largest_global_improvement = max(
        abs(float(receipt["global_D_improvement"])) for receipt in rounds
    )
    if order_change > 5.0e-8 or largest_global_improvement > 1.0e-10:
        raise RuntimeError(
            "subcritical continuous outer optimisation did not stabilise: "
            f"order change={order_change:.3e}, global D improvement="
            f"{largest_global_improvement:.3e}, "
            f"rounds={rounds}"
        )
    if any(float(receipt["adjacent_screen_inferiority"]) > 1.0e-10 for receipt in rounds):
        raise RuntimeError("subcritical optimum is inferior to an adjacent screen point")
    if abs(float(rounds[-1]["value"]) - float(saddle["exponent"])) > 2.0e-11:
        raise RuntimeError("cached outer optimisation and stationarity solve disagree")

    receipt = {
        "formulation": (
            "max_{0<lambda<1} (1-lambda)/lambda "
            "[min_{s,t} D_lambda(Q_t||P_s)-r_minus]"
        ),
        "screen_order_count": int(len(screen_orders)),
        "screen_interval": [0.02, 0.98],
        "outer_rounds": rounds,
        "outer_xatol": 2.0e-13,
        "outer_order_stability_tolerance": 5.0e-8,
        "inner_D_stability_tolerance": 1.0e-10,
        "adjacent_point_tolerance": 1.0e-10,
        "order_change": order_change,
        "divergence_change": divergence_change,
        "value_change": value_change,
        "largest_global_D_improvement": largest_global_improvement,
        "order_one_limit": {
            "D": float(saddle["kl_divergence"]),
            "objective": 0.0,
        },
        "order_zero_limit": "minus infinity because all coordinates have full support and r_minus>0",
        "new_order_count": len(cache.records),
        "projection_calls": cache.projection_calls,
        "cache_hits": cache.cache_hits,
        "global_polishes": cache.global_polishes,
    }
    return receipt, cache.payload()


def equivalent_minmax_receipt(saddle: dict[str, object]) -> dict[str, object]:
    rate = float(saddle["rate"])

    def fixed_pair_maximum(x: np.ndarray, include_order: bool = False):
        s, t = map(float, x)

        def negative_objective(order: float) -> float:
            return -(1.0 - order) / order * (
                renyi(order, q_at(t), p_at(s)) - rate
            )

        result = minimize_scalar(
            negative_objective,
            bounds=(1.0e-8, 1.0 - 1.0e-10),
            method="bounded",
            options={"xatol": 2.0e-13, "maxiter": 1000},
        )
        value = -float(result.fun)
        if include_order:
            return value, float(result.x)
        return value

    global_result = differential_evolution(
        fixed_pair_maximum,
        [(0.0, 1.0), (0.0, 1.0)],
        tol=1.0e-10,
        atol=1.0e-13,
        popsize=25,
        maxiter=500,
        polish=False,
        seed=987,
    )
    local = minimize(
        fixed_pair_maximum,
        global_result.x,
        method="Nelder-Mead",
        bounds=[(0.0, 1.0), (0.0, 1.0)],
        options={"xatol": 1.0e-12, "fatol": 1.0e-14, "maxiter": 5000},
    )
    value, order = fixed_pair_maximum(local.x, include_order=True)
    return {
        "value": value,
        "lambda": order,
        "s": float(local.x[0]),
        "t": float(local.x[1]),
        "global_evaluations": int(global_result.nfev),
        "difference_from_max_min": value - float(saddle["exponent"]),
    }


def renyi_monotonicity_receipt() -> dict[str, object]:
    orders = np.concatenate(
        (
            np.linspace(0.001, 0.1, 10),
            np.linspace(0.11, 0.9, 80),
            np.linspace(0.91, 0.999, 10),
        )
    )
    values = []
    t_values = []
    global_differences = []
    for index, order in enumerate(orders):
        boundary = minimize_scalar(
            lambda t: renyi(float(order), q_at(float(t)), P0),
            bounds=(0.0, 1.0),
            method="bounded",
            options={"xatol": 2.0e-14, "maxiter": 1000},
        )
        values.append(float(boundary.fun))
        t_values.append(float(boundary.x))
        if index % 10 == 0 or index == len(orders) - 1:
            global_result = differential_evolution(
                lambda x: renyi(float(order), q_at(float(x[1])), p_at(float(x[0]))),
                [(0.0, 1.0), (0.0, 1.0)],
                tol=1.0e-10,
                atol=1.0e-13,
                popsize=20,
                polish=True,
                seed=int(order * 1.0e6) + 1,
            )
            global_differences.append(float(boundary.fun - global_result.fun))
    increments = np.diff(np.asarray(values))
    return {
        "orders_checked": int(len(orders)),
        "minimum_increment": float(increments.min()),
        "maximum_decrease": float(max(0.0, -increments.min())),
        "maximum_absolute_global_crosscheck_difference": float(
            np.max(np.abs(global_differences))
        ),
        "first": {"lambda": float(orders[0]), "value": values[0], "t": t_values[0]},
        "last": {"lambda": float(orders[-1]), "value": values[-1], "t": t_values[-1]},
    }


def maximum_receipt(
    solver: ModuleType,
    type_space,
    affine_class,
    values: np.ndarray,
    dense_grid_size: int,
) -> dict[str, float | int]:
    separated = solver.maximise_affine_expectation(
        type_space,
        affine_class,
        values,
        trim_tolerance=5.0e-13,
        derivative_oversampling=64,
        interpolation_check_points=101,
    )
    dense = solver.dense_grid_maximum(
        type_space,
        affine_class,
        values,
        grid_size=dense_grid_size,
    )
    return {
        "value": float(separated.value),
        "parameter": float(separated.parameter),
        "interpolation_error": float(separated.interpolation_error),
        "effective_degree": int(separated.effective_degree),
        "candidate_count": int(separated.candidate_count),
        "dense_value": float(dense.value),
        "dense_parameter": float(dense.parameter),
        "separator_minus_dense": float(separated.value - dense.value),
        "dense_grid_size": int(dense_grid_size),
    }


def finite_block_receipts(
    solver: ModuleType,
    saddle: dict[str, object],
) -> dict[str, object]:
    rate = float(saddle["rate"])
    order = float(saddle["lambda"])
    t_star = float(saddle["t_star"])
    d_order = float(saddle["renyi_divergence"])
    epsilon = math.exp(-N * rate)

    null_class = solver.AffineTernaryClass(P0, P1)
    alternative_class = solver.AffineTernaryClass(Q0, Q1)
    lp = solver.solve_composite_minimax(
        N,
        epsilon,
        null_class,
        alternative_class,
        initial_grid_size=33,
        constraint_tolerance=3.0e-14,
        parameter_tolerance=3.0e-15,
        max_iterations=100,
        row_scale=1.0e4,
        objective_scale=1.0e4,
        verbose=False,
    )
    type_space = solver.ternary_type_space(N)

    lp_null = maximum_receipt(
        solver,
        type_space,
        null_class,
        1.0 - lp.acceptance,
        500001,
    )
    lp_alternative = maximum_receipt(
        solver,
        type_space,
        alternative_class,
        lp.acceptance,
        500001,
    )

    p_star = P0
    q_star = q_at(t_star)
    scores = type_space.counts @ np.log(q_star / p_star)
    tau_min = N * (rate - (1.0 - order) * d_order) / order
    deterministic = (scores >= tau_min).astype(float)

    # Locate the calibrated boundary.  In this example all 231 type scores are
    # distinct and the verified null envelope is attained at s=0.
    p0_types = solver.type_probability_matrix(type_space, null_class, [0.0])[0]
    descending = np.argsort(-scores, kind="stable")
    above = np.zeros(type_space.size)
    cumulative = 0.0
    boundary_index = None
    for index in descending:
        if cumulative <= epsilon <= cumulative + p0_types[index]:
            boundary_index = int(index)
            break
        above[index] = 1.0
        cumulative += float(p0_types[index])
    if boundary_index is None:
        raise RuntimeError("failed to locate calibrated score boundary")
    eta = (epsilon - cumulative) / float(p0_types[boundary_index])
    calibrated = above.copy()
    calibrated[boundary_index] = eta

    projected = {
        "deterministic_type_i": maximum_receipt(
            solver, type_space, null_class, deterministic, 100001
        ),
        "deterministic_type_ii": maximum_receipt(
            solver, type_space, alternative_class, 1.0 - deterministic, 100001
        ),
        "calibrated_type_i": maximum_receipt(
            solver, type_space, null_class, calibrated, 100001
        ),
        "calibrated_type_ii": maximum_receipt(
            solver, type_space, alternative_class, 1.0 - calibrated, 100001
        ),
    }

    weighted_values = np.exp((order - 1.0) * scores) * (1.0 - deterministic)
    weighted = maximum_receipt(
        solver,
        type_space,
        alternative_class,
        weighted_values,
        100001,
    )
    prefactor = math.exp((1.0 - order) * tau_min)
    corrected_bound = prefactor * float(weighted["value"])
    raw_bound = math.exp(
        (1.0 - order) * tau_min + N * (order - 1.0) * d_order
    )

    score_gaps = np.diff(np.sort(scores))
    return {
        "epsilon": epsilon,
        "lp": {
            "master_objective": float(lp.beta),
            "validated_type_i": lp_null,
            "validated_type_ii": lp_alternative,
            "objective_to_envelope_gap": float(lp_alternative["value"] - lp.beta),
            "iterations": int(lp.iterations),
            "converged": bool(lp.converged),
            "solver_message": lp.solver_message,
            "settings": {
                "initial_grid_size": 33,
                "constraint_tolerance": 3.0e-14,
                "parameter_tolerance": 3.0e-15,
                "max_iterations": 100,
                "row_scale": 1.0e4,
                "objective_scale": 1.0e4,
                "separator_trim_tolerance": 5.0e-13,
                "separator_derivative_oversampling": 64,
                "dense_grid_size": 500001,
            },
        },
        "projected": {
            "tau_min": tau_min,
            "tau_distance_to_nearest_score": float(np.min(np.abs(scores - tau_min))),
            "deterministic_rejected_type_count": int(deterministic.sum()),
            "calibrated_tau": float(scores[boundary_index]),
            "calibrated_eta": float(eta),
            "calibrated_boundary_type": type_space.counts[boundary_index].tolist(),
            "calibrated_strictly_above_type_count": int(above.sum()),
            "distinct_score_count": int(np.unique(scores).size),
            "minimum_score_gap": float(score_gaps.min()),
            **projected,
            "weighted_alternative_envelope": weighted,
            "corrected_bound_prefactor": prefactor,
            "corrected_bound": corrected_bound,
            "raw_exponential_bound": raw_bound,
            "raw_bound_from_exponent": math.exp(-N * float(saddle["exponent"])),
            "settings": {
                "separator_trim_tolerance": 5.0e-13,
                "separator_derivative_oversampling": 64,
                "separator_interpolation_check_points": 101,
                "dense_grid_size": 100001,
            },
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--solver",
        type=Path,
        default=Path("numerics/scripts/affine_ternary_lp.py"),
        help="path to the repository affine_ternary_lp.py",
    )
    parser.add_argument(
        "--skip-full-validation",
        action="store_true",
        help="skip the publication-certification global screens and min-max check",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--gap-csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--projection-cache", type=Path, default=DEFAULT_CACHE)
    args = parser.parse_args()

    solver = load_affine_solver(args.solver)
    saddle = solve_stationary_saddle()
    output: dict[str, object] = {
        "classes": {
            "P0": P0.tolist(),
            "P1": P1.tolist(),
            "Q0": Q0.tolist(),
            "Q1": Q1.tolist(),
        },
        "saddle": saddle,
        "saddle_high_precision": solve_stationary_saddle_decimal(),
        "n20": finite_block_receipts(solver, saddle),
    }
    if not args.skip_full_validation:
        outer_receipt, projection_cache = continuous_outer_receipt(saddle)
        output["continuous_outer_optimisation"] = outer_receipt
        output["global_projection_validation"] = global_projection_receipts(saddle)
        output["equivalent_minmax"] = equivalent_minmax_receipt(saddle)
        output["renyi_monotonicity"] = renyi_monotonicity_receipt()
        args.projection_cache.parent.mkdir(parents=True, exist_ok=True)
        args.projection_cache.write_text(
            json.dumps(projection_cache, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    lp = output["n20"]["lp"]
    projected = output["n20"]["projected"]
    deterministic_i = projected["deterministic_type_i"]
    deterministic_ii = projected["deterministic_type_ii"]
    calibrated_i = projected["calibrated_type_i"]
    calibrated_ii = projected["calibrated_type_ii"]
    rows = [
        {
            "quantity": "minimax_type_ii",
            "value": lp["validated_type_ii"]["value"],
            "attained_type_i": lp["validated_type_i"]["value"],
            "worst_null_s": lp["validated_type_i"]["parameter"],
            "actual_type_ii": lp["validated_type_ii"]["value"],
            "worst_alternative_t": lp["validated_type_ii"]["parameter"],
            "analytical_envelope_t": "",
        },
        {
            "quantity": "calibrated_projected_type_ii",
            "value": calibrated_ii["value"],
            "attained_type_i": calibrated_i["value"],
            "worst_null_s": calibrated_i["parameter"],
            "actual_type_ii": calibrated_ii["value"],
            "worst_alternative_t": calibrated_ii["parameter"],
            "analytical_envelope_t": "",
        },
        {
            "quantity": "projected_type_ii_at_tau_min",
            "value": deterministic_ii["value"],
            "attained_type_i": deterministic_i["value"],
            "worst_null_s": deterministic_i["parameter"],
            "actual_type_ii": deterministic_ii["value"],
            "worst_alternative_t": deterministic_ii["parameter"],
            "analytical_envelope_t": "",
        },
        {
            "quantity": "bound_slack_rejection",
            "value": projected["corrected_bound"],
            "attained_type_i": deterministic_i["value"],
            "worst_null_s": deterministic_i["parameter"],
            "actual_type_ii": deterministic_ii["value"],
            "worst_alternative_t": deterministic_ii["parameter"],
            "analytical_envelope_t": projected["weighted_alternative_envelope"]["parameter"],
        },
        {
            "quantity": "raw_projected_exponential_bound",
            "value": projected["raw_exponential_bound"],
            "attained_type_i": deterministic_i["value"],
            "worst_null_s": deterministic_i["parameter"],
            "actual_type_ii": deterministic_ii["value"],
            "worst_alternative_t": deterministic_ii["parameter"],
            "analytical_envelope_t": "uniform moment relaxation",
        },
    ]
    args.gap_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.gap_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "quantity",
                "value",
                "attained_type_i",
                "worst_null_s",
                "actual_type_ii",
                "worst_alternative_t",
                "analytical_envelope_t",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {args.output}")
    print(f"wrote {args.gap_csv}")
    if not args.skip_full_validation:
        print(f"wrote {args.projection_cache}")


if __name__ == "__main__":
    main()
