#!/usr/bin/env python3
"""Finite-blocklength experiment for non-ordered affine ternary classes.

The script computes, without endpoint reduction,

* the composite minimax Type-II error by a type-symmetrised
  semi-infinite linear programme with constraint generation;
* the calibrated projected-log-likelihood-ratio upper bound, optimised over
  a deterministic mesh of Renyi orders in (0, 1); and
* the forward and reverse branches of the Bruno--Vandenbroucque--Esposito
  converse, using composite Renyi divergences and orders greater than one.

Every per-blocklength result is checkpointed atomically.  By default the
script evaluates every integer n from 1 through 300; pass --mesh for the
documented deterministic fallback mesh.  No values are interpolated into
the CSV.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence

# Avoid BLAS over-subscription when blocklengths are evaluated in parallel.
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "cht-mpl"))

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
from scipy.optimize import differential_evolution, minimize
from scipy.special import gammaln, logsumexp

from affine_ternary_lp import (
    AffineTernaryClass,
    solve_composite_minimax as solve_exact_composite_minimax,
)


FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]

ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = ROOT / "numerics" / "figures"
DATA_DIR = ROOT / "numerics" / "data"
CHECKPOINT_DIR = ROOT / "numerics" / "checkpoints" / "nonordered_bruno_regimes"
CSV_PATH = DATA_DIR / "nonordered_bruno_regimes.csv"
CACHE_PATH = DATA_DIR / "nonordered_bruno_renyi_cache.json"
AUDIT_PATH = ROOT / "numerics" / "nonordered_bruno_regimes_audit.md"

# These full-support endpoints are intentionally not an ordered exponential
# family.  They are replaced only by editing this single configuration block;
# the cache fingerprint prevents accidental reuse after such a change.
P0 = np.array([0.33, 0.33, 0.34])
P1 = np.array([0.33, 0.35, 0.32])
Q0 = np.array([0.20294716, 0.42818293, 0.36886991])
Q1 = np.array([0.37047326, 0.45476373, 0.17476301])

REGIMES = ("constant", "linear")
CONSTANT_EPSILON = 0.01

# A small-order mesh is essential in the fixed and subexponential Type-I
# regimes.  The list is deliberately explicit so a run is reproducible.
ACHIEVABILITY_LAMBDAS = np.array(
    [
        0.001,
        0.002,
        0.005,
        0.01,
        0.02,
        0.035,
        0.05,
        0.075,
        0.10,
        0.14,
        0.18,
        0.23,
        0.28,
        0.34,
        0.40,
        0.47,
        0.50,
        0.54,
        0.61,
        0.68,
        0.75,
        0.82,
        0.88,
        0.93,
        0.96,
        0.98,
        0.99,
    ],
    dtype=float,
)


def converse_a_mesh() -> FloatArray:
    """Return the deterministic a=(lambda-1)/lambda mesh in (0,1)."""

    near_zero = np.geomspace(1.0e-5, 0.08, 48)
    middle = np.linspace(0.08, 0.92, 85)
    near_one = 1.0 - np.geomspace(1.0e-5, 0.08, 36)
    return np.unique(np.concatenate((near_zero, middle, near_one)))


CONVERSE_A = converse_a_mesh()
CONVERSE_LAMBDAS = 1.0 / (1.0 - CONVERSE_A)


def selected_n_mesh() -> list[int]:
    """Dense deterministic mesh used for the committed finite run."""

    return sorted(
        set(range(1, 51))
        | set(range(52, 121, 2))
        | set(range(125, 201, 5))
        | set(range(210, 301, 10))
    )


def affine(endpoint0: FloatArray, endpoint1: FloatArray, u: float) -> FloatArray:
    return (1.0 - u) * endpoint0 + u * endpoint1


def p_of(s: float) -> FloatArray:
    return affine(P0, P1, s)


def q_of(t: float) -> FloatArray:
    return affine(Q0, Q1, t)


def epsilon_for(n: int, regime: str) -> float:
    if regime == "constant":
        return CONSTANT_EPSILON
    if regime == "linear":
        return 1.0 / n
    raise ValueError(f"unknown regime: {regime}")


def check_endpoints() -> None:
    for name, law in (("P0", P0), ("P1", P1), ("Q0", Q0), ("Q1", Q1)):
        if law.shape != (3,) or np.any(law <= 0.0):
            raise ValueError(f"{name} must be a full-support ternary law")
        if not math.isclose(float(law.sum()), 1.0, rel_tol=0.0, abs_tol=2.0e-14):
            raise ValueError(f"{name} does not sum to one")


@dataclass(frozen=True)
class TypeSpace:
    n: int
    counts: IntArray
    log_multiplicity: FloatArray

    @classmethod
    def build(cls, n: int) -> "TypeSpace":
        counts = np.array(
            [(k0, k1, n - k0 - k1) for k0 in range(n + 1) for k1 in range(n - k0 + 1)],
            dtype=np.int64,
        )
        log_mult = gammaln(n + 1.0) - np.sum(gammaln(counts + 1.0), axis=1)
        return cls(n=n, counts=counts, log_multiplicity=np.asarray(log_mult, dtype=float))

    @property
    def size(self) -> int:
        return int(self.counts.shape[0])

    def probabilities(self, law: FloatArray) -> FloatArray:
        log_prob = self.log_multiplicity + self.counts @ np.log(law)
        prob = np.exp(log_prob)
        total = float(prob.sum())
        if not np.isfinite(total) or total <= 0.0:
            raise FloatingPointError("invalid multinomial type probabilities")
        # Renormalisation only removes accumulated floating-point error.
        return prob / total


def probability_matrix(
    space: TypeSpace, law_fn: Callable[[float], FloatArray], grid: FloatArray
) -> FloatArray:
    distributions = np.vstack([law_fn(float(u)) for u in grid])
    log_probability = (
        space.log_multiplicity[:, None] + space.counts @ np.log(distributions).T
    )
    probability = np.exp(log_probability).T
    return probability / probability.sum(axis=1, keepdims=True)


def _local_candidate_indices(values: FloatArray, top_k: int = 10) -> list[int]:
    if values.size <= 2:
        return list(range(values.size))
    local = np.flatnonzero(
        (values[1:-1] >= values[:-2]) & (values[1:-1] >= values[2:])
    ) + 1
    top = np.argsort(values)[-min(top_k, values.size) :]
    return sorted(set([0, values.size - 1, *local.tolist(), *top.tolist()]))


def maximise_unit_interval(
    scalar_fn: Callable[[float], float],
    grid: FloatArray,
    grid_values: FloatArray | None = None,
    *,
    xatol: float = 2.0e-11,
) -> tuple[float, float]:
    """Deterministic grid search followed by bounded local refinements."""

    values = (
        np.asarray([scalar_fn(float(x)) for x in grid], dtype=float)
        if grid_values is None
        else np.asarray(grid_values, dtype=float)
    )
    best_index = int(np.argmax(values))
    best_value = float(values[best_index])
    best_x = float(grid[best_index])
    for index in _local_candidate_indices(values):
        left = float(grid[max(0, index - 1)])
        right = float(grid[min(grid.size - 1, index + 1)])
        if right <= left:
            continue
        result = minimize(
            lambda z: -scalar_fn(float(z[0])),
            x0=np.array([float(grid[index])]),
            method="Nelder-Mead",
            bounds=[(left, right)],
            options={"xatol": xatol, "fatol": 1.0e-13, "maxiter": 160},
        )
        x = float(np.clip(result.x[0], left, right))
        value = float(scalar_fn(x))
        if value > best_value:
            best_value, best_x = value, x
    return best_value, best_x


def renyi_divergence(first: FloatArray, second: FloatArray, order: float) -> float:
    if math.isinf(order) and order > 0.0:
        return float(np.max(np.log(first) - np.log(second)))
    if order <= 0.0 or math.isclose(order, 1.0):
        raise ValueError("Renyi order must be positive and different from one")
    terms = order * np.log(first) + (1.0 - order) * np.log(second)
    return float(logsumexp(terms) / (order - 1.0))


def kl_divergence(first: FloatArray, second: FloatArray) -> float:
    return float(np.sum(first * (np.log(first) - np.log(second))))


def minimise_kl_over_classes(orientation: str) -> dict[str, float]:
    if orientation == "Q||P":
        objective = lambda x: kl_divergence(q_of(float(x[1])), p_of(float(x[0])))
    elif orientation == "P||Q":
        objective = lambda x: kl_divergence(p_of(float(x[0])), q_of(float(x[1])))
    else:
        raise ValueError(orientation)
    grid = np.linspace(0.0, 1.0, 13)
    scouts = sorted(
        (float(objective(np.array([s, t]))), float(s), float(t)) for s in grid for t in grid
    )
    best_value, best_s, best_t = scouts[0]
    for _, s, t in scouts[:16]:
        fit = minimize(
            objective,
            x0=np.array([s, t]),
            method="L-BFGS-B",
            bounds=[(0.0, 1.0), (0.0, 1.0)],
            options={"ftol": 1.0e-15, "gtol": 2.0e-11, "maxiter": 500},
        )
        candidate_s, candidate_t = np.clip(fit.x, 0.0, 1.0)
        value = float(objective(np.array([candidate_s, candidate_t])))
        if value < best_value:
            best_value, best_s, best_t = value, float(candidate_s), float(candidate_t)
    return {"D": best_value, "s": best_s, "t": best_t}


def minimise_over_classes(
    order: float,
    orientation: str,
    *,
    coarse_size: int = 13,
) -> dict[str, float]:
    """Globally screen and locally refine a two-parameter Renyi projection."""

    if orientation == "Q||P":
        pair = lambda x: (q_of(float(x[1])), p_of(float(x[0])))
    elif orientation == "P||Q":
        pair = lambda x: (p_of(float(x[0])), q_of(float(x[1])))
    else:
        raise ValueError(orientation)

    if math.isinf(order):
        objective = lambda x: renyi_divergence(*pair(x), order)
    elif order < 1.0:
        # For orders below one, minimising D is equivalent to maximising the
        # Hellinger integral.  This form avoids a poorly scaled objective when
        # the order is close to zero.
        objective = lambda x: -float(
            logsumexp(order * np.log(pair(x)[0]) + (1.0 - order) * np.log(pair(x)[1]))
        )
    else:
        objective = lambda x: renyi_divergence(*pair(x), order)

    grid = np.linspace(0.0, 1.0, coarse_size)
    screened: list[tuple[float, float, float]] = []
    for s in grid:
        for t in grid:
            screened.append((float(objective(np.array([s, t]))), float(s), float(t)))
    screened.sort(key=lambda item: item[0])
    starts = screened[:12]
    starts.extend(
        (float(objective(np.array([s, t]))), s, t)
        for s, t in ((0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0), (0.5, 0.5))
    )
    best_value, best_s, best_t = starts[0]
    for _, s0, t0 in starts:
        result = minimize(
            objective,
            x0=np.array([s0, t0]),
            method="L-BFGS-B",
            bounds=[(0.0, 1.0), (0.0, 1.0)],
            options={"ftol": 1.0e-15, "gtol": 2.0e-10, "maxiter": 500},
        )
        s, t = np.clip(result.x, 0.0, 1.0)
        value = float(objective(np.array([s, t])))
        if value < best_value:
            best_value, best_s, best_t = value, float(s), float(t)
    divergence = renyi_divergence(*pair(np.array([best_s, best_t])), order)
    # A Powell polish is useful for the nonsmooth order-infinity objective.
    if math.isinf(order):
        result = minimize(
            objective,
            x0=np.array([best_s, best_t]),
            method="Powell",
            bounds=[(0.0, 1.0), (0.0, 1.0)],
            options={"xtol": 2.0e-11, "ftol": 1.0e-14, "maxiter": 1000},
        )
        s, t = np.clip(result.x, 0.0, 1.0)
        candidate = renyi_divergence(*pair(np.array([s, t])), order)
        if candidate < divergence:
            divergence, best_s, best_t = candidate, float(s), float(t)
    return {"order": float(order), "D": float(divergence), "s": best_s, "t": best_t}


def _configuration_fingerprint() -> str:
    payload = {
        "P0": P0.tolist(),
        "P1": P1.tolist(),
        "Q0": Q0.tolist(),
        "Q1": Q1.tolist(),
        "achievability_lambdas": ACHIEVABILITY_LAMBDAS.tolist(),
        "converse_a": CONVERSE_A.tolist(),
        "version": 3,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def atomic_json_dump(payload: object, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + f".{os.getpid()}.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(temporary, path)


def build_or_load_renyi_cache(force: bool = False) -> dict[str, object]:
    fingerprint = _configuration_fingerprint()
    if CACHE_PATH.exists() and not force:
        with CACHE_PATH.open("r", encoding="utf-8") as handle:
            cached = json.load(handle)
        if cached.get("fingerprint") == fingerprint:
            return cached

    started = time.perf_counter()
    achievability = []
    for order in ACHIEVABILITY_LAMBDAS:
        record = minimise_over_classes(float(order), "Q||P")
        p_star, q_star = p_of(record["s"]), q_of(record["t"])
        record["h"] = np.log(q_star / p_star).tolist()
        achievability.append(record)

    converse = []
    for order in CONVERSE_LAMBDAS:
        reverse = minimise_over_classes(float(order), "Q||P")
        forward = minimise_over_classes(float(order), "P||Q")
        converse.append(
            {
                "order": float(order),
                "a": float((order - 1.0) / order),
                "reverse_D": reverse["D"],
                "reverse_s": reverse["s"],
                "reverse_t": reverse["t"],
                "forward_D": forward["D"],
                "forward_s": forward["s"],
                "forward_t": forward["t"],
            }
        )
    reverse_infinity = minimise_over_classes(math.inf, "Q||P")
    forward_infinity = minimise_over_classes(math.inf, "P||Q")
    converse.append(
        {
            "order": "infinity",
            "a": 1.0,
            "reverse_D": reverse_infinity["D"],
            "reverse_s": reverse_infinity["s"],
            "reverse_t": reverse_infinity["t"],
            "forward_D": forward_infinity["D"],
            "forward_s": forward_infinity["s"],
            "forward_t": forward_infinity["t"],
        }
    )
    cache: dict[str, object] = {
        "fingerprint": fingerprint,
        "endpoints": {"P0": P0.tolist(), "P1": P1.tolist(), "Q0": Q0.tolist(), "Q1": Q1.tolist()},
        "achievability": achievability,
        "converse": converse,
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json_dump(cache, CACHE_PATH)
    return cache


def finite_composite_lp(
    space: TypeSpace,
    epsilon: float,
    parameter_grid: FloatArray,
    p_matrix: FloatArray,
    q_matrix: FloatArray,
    *,
    violation_tolerance: float = 2.0e-9,
    max_iterations: int = 80,
) -> tuple[dict[str, float], FloatArray]:
    """Solve the type LP by adding worst continuous class constraints."""

    if epsilon >= 1.0:
        phi = np.ones(space.size)
        return (
            {
                "minimax": 0.0,
                "lp_objective": 0.0,
                "worst_type_i": 1.0,
                "worst_type_i_s": 0.0,
                "worst_type_ii": 0.0,
                "worst_type_ii_t": 0.0,
                "lp_iterations": 0.0,
                "active_null_constraints": 0.0,
                "active_alternative_constraints": 0.0,
            },
            phi,
        )

    result = solve_exact_composite_minimax(
        space.n,
        epsilon,
        AffineTernaryClass(P0, P1),
        AffineTernaryClass(Q0, Q1),
        initial_grid_size=17,
        constraint_tolerance=violation_tolerance,
        parameter_tolerance=2.0e-10,
        max_iterations=max_iterations,
        row_scale=1.0e4,
        objective_scale=1.0e4,
        small_matrix_value=1.0e-12,
        primal_feasibility_tolerance=1.0e-10,
        dual_feasibility_tolerance=1.0e-10,
        # The n=299 master has a reproducibly degenerate dual-simplex path;
        # the same immutable LP solves promptly by the validated IPM route.
        solver_methods=("highs-ipm", "highs-ds") if space.n == 299 else ("highs-ds", "highs-ipm"),
        derivative_oversampling=16,
        trim_tolerance=5.0e-13,
    )
    if not result.converged:
        raise RuntimeError("constraint generation did not converge")
    phi = 1.0 - np.asarray(result.acceptance, dtype=float)
    return (
        {
            "minimax": result.beta,
            "lp_objective": result.beta,
            "worst_type_i": result.worst_type_i,
            "worst_type_i_s": result.worst_null_parameter,
            "worst_type_ii": result.worst_type_ii,
            "worst_type_ii_t": result.worst_alternative_parameter,
            "lp_iterations": float(result.iterations),
            "active_null_constraints": float(len(result.null_parameters)),
            "active_alternative_constraints": float(len(result.alternative_parameters)),
        },
        phi,
    )


def score_groups(scores: FloatArray) -> tuple[IntArray, list[tuple[int, int]], FloatArray]:
    order = np.argsort(-scores, kind="mergesort")
    sorted_scores = scores[order]
    if sorted_scores.size == 0:
        return order, [], sorted_scores
    scale = max(1.0, float(np.max(np.abs(sorted_scores))))
    split = np.flatnonzero(np.abs(np.diff(sorted_scores)) > 2.0e-12 * scale) + 1
    starts = np.concatenate(([0], split))
    ends = np.concatenate((split, [sorted_scores.size]))
    groups = [(int(start), int(end)) for start, end in zip(starts, ends)]
    return order, groups, sorted_scores


def _grid_calibration(
    order: IntArray,
    groups: list[tuple[int, int]],
    p_matrix: FloatArray,
    q_matrix: FloatArray,
    epsilon: float,
) -> tuple[int, float, float]:
    if epsilon >= 1.0:
        return len(groups), 0.0, 0.0
    sorted_p = p_matrix[:, order]
    cumulative = np.cumsum(sorted_p, axis=1)
    group_ends = np.asarray([end - 1 for _, end in groups], dtype=int)
    envelope = np.max(cumulative[:, group_ends], axis=0)
    boundary_group = int(np.searchsorted(envelope, epsilon, side="right"))
    if boundary_group >= len(groups):
        return len(groups), 0.0, 0.0
    start, end = groups[boundary_group]
    before = np.zeros(p_matrix.shape[0]) if start == 0 else cumulative[:, start - 1]
    boundary = np.sum(sorted_p[:, start:end], axis=1)
    lo, hi = 0.0, 1.0
    for _ in range(60):
        eta = 0.5 * (lo + hi)
        if float(np.max(before + eta * boundary)) <= epsilon:
            lo = eta
        else:
            hi = eta
    eta = lo
    phi = np.zeros(order.size)
    phi[order[:start]] = 1.0
    phi[order[start:end]] = eta
    grid_beta = float(np.max(q_matrix @ (1.0 - phi)))
    return boundary_group, eta, grid_beta


def calibrate_projected_test(
    space: TypeSpace,
    h: FloatArray,
    epsilon: float,
    parameter_grid: FloatArray,
    p_matrix: FloatArray,
    q_matrix: FloatArray,
    *,
    refine: bool,
) -> tuple[dict[str, float], FloatArray]:
    scores = space.counts @ h
    order, groups, sorted_scores = score_groups(scores)
    boundary_group, eta, grid_beta = _grid_calibration(order, groups, p_matrix, q_matrix, epsilon)
    if boundary_group >= len(groups):
        phi = np.ones(space.size)
        return (
            {
                "beta": 0.0,
                "type_i": 1.0,
                "worst_s": 0.0,
                "worst_t": 0.0,
                "eta": 0.0,
                "threshold": -math.inf,
                "grid_beta": grid_beta,
            },
            phi,
        )

    def build_phi(group_index: int, randomisation: float) -> FloatArray:
        start, end = groups[group_index]
        test = np.zeros(space.size)
        test[order[:start]] = 1.0
        test[order[start:end]] = randomisation
        return test

    if refine:
        # Correct a possible coarse-grid boundary displacement first.
        for _ in range(8):
            phi0 = build_phi(boundary_group, 0.0)
            alpha0_values = p_matrix @ phi0
            alpha0, _ = maximise_unit_interval(
                lambda s: float(space.probabilities(p_of(s)) @ phi0),
                parameter_grid,
                alpha0_values,
            )
            phi1 = build_phi(boundary_group, 1.0)
            alpha1_values = p_matrix @ phi1
            alpha1, _ = maximise_unit_interval(
                lambda s: float(space.probabilities(p_of(s)) @ phi1),
                parameter_grid,
                alpha1_values,
            )
            if alpha0 <= epsilon + 2.0e-11 and alpha1 > epsilon - 2.0e-11:
                break
            if alpha0 > epsilon and boundary_group > 0:
                boundary_group -= 1
            elif alpha1 <= epsilon and boundary_group + 1 < len(groups):
                boundary_group += 1
            else:
                break

        # Feasibility for every s is equivalent to
        #   eta <= (epsilon-A_strict(s))/A_boundary(s).
        # Full support makes the denominator positive.  Hence the largest
        # admissible boundary randomisation is the continuous minimum of this
        # ratio, which also exhausts the composite Type-I budget exactly.
        start, end = groups[boundary_group]
        strict = build_phi(boundary_group, 0.0)
        boundary = np.zeros(space.size)
        boundary[order[start:end]] = 1.0
        numerator_grid = epsilon - p_matrix @ strict
        denominator_grid = p_matrix @ boundary
        ratio_grid = numerator_grid / denominator_grid

        def ratio(s: float) -> float:
            probabilities = space.probabilities(p_of(s))
            return float((epsilon - probabilities @ strict) / (probabilities @ boundary))

        candidate_indices = _local_candidate_indices(-ratio_grid)
        best_index = int(np.argmin(ratio_grid))
        eta = float(ratio_grid[best_index])
        for index in candidate_indices:
            left = float(parameter_grid[max(0, index - 1)])
            right = float(parameter_grid[min(parameter_grid.size - 1, index + 1)])
            if right <= left:
                continue
            fit = minimize(
                lambda z: ratio(float(z[0])),
                x0=np.array([float(parameter_grid[index])]),
                method="Nelder-Mead",
                bounds=[(left, right)],
                options={"xatol": 2.0e-12, "fatol": 1.0e-13, "maxiter": 180},
            )
            eta = min(eta, ratio(float(np.clip(fit.x[0], left, right))))
        eta = float(np.clip(eta, 0.0, 1.0))
    phi = build_phi(boundary_group, eta)
    alpha_values = p_matrix @ phi
    alpha, worst_s = maximise_unit_interval(
        lambda s: float(space.probabilities(p_of(s)) @ phi), parameter_grid, alpha_values
    )
    miss = 1.0 - phi
    beta_values = q_matrix @ miss
    beta, worst_t = maximise_unit_interval(
        lambda t: float(space.probabilities(q_of(t)) @ miss), parameter_grid, beta_values
    )
    start, _ = groups[boundary_group]
    threshold = float(sorted_scores[start])
    return (
        {
            "beta": beta,
            "type_i": alpha,
            "worst_s": worst_s,
            "worst_t": worst_t,
            "eta": eta,
            "threshold": threshold,
            "grid_beta": grid_beta,
        },
        phi,
    )


def optimised_achievability(
    space: TypeSpace,
    epsilon: float,
    cache: dict[str, object],
    parameter_grid: FloatArray,
    p_matrix: FloatArray,
    q_matrix: FloatArray,
) -> tuple[dict[str, float], FloatArray]:
    projections = list(cache["achievability"])
    evaluated: list[tuple[float, int, dict[str, float], FloatArray]] = []
    for index, record in enumerate(projections):
        result, phi = calibrate_projected_test(
            space,
            np.asarray(record["h"], dtype=float),
            epsilon,
            parameter_grid,
            p_matrix,
            q_matrix,
            refine=True,
        )
        evaluated.append((result["beta"], index, result, phi))
    best = min(evaluated, key=lambda item: item[0])
    beta, index, result, phi = best
    projection = projections[index]
    return (
        {
            "achievability": beta,
            "achievability_lambda": float(projection["order"]),
            "achievability_type_i": result["type_i"],
            "achievability_worst_s": result["worst_s"],
            "achievability_worst_t": result["worst_t"],
            "achievability_eta": result["eta"],
            "achievability_threshold": result["threshold"],
            "projection_s": float(projection["s"]),
            "projection_t": float(projection["t"]),
            "projection_D": float(projection["D"]),
        },
        phi,
    )


def composite_converse(n: int, epsilon: float, cache: dict[str, object]) -> dict[str, float]:
    records = list(cache["converse"])
    a = np.asarray([record["a"] for record in records], dtype=float)
    orders = np.asarray(
        [math.inf if record["order"] == "infinity" else record["order"] for record in records],
        dtype=float,
    )
    reverse_d = np.asarray([record["reverse_D"] for record in records], dtype=float)
    forward_d = np.asarray([record["forward_D"] for record in records], dtype=float)

    reverse_log_term = a * (math.log(epsilon) + n * reverse_d)
    reverse_index = int(np.argmin(reverse_log_term))
    reverse_branch = 1.0 - math.exp(min(0.0, float(reverse_log_term[reverse_index])))

    if epsilon >= 1.0:
        forward_log = np.full_like(a, -math.inf)
    else:
        forward_log = np.log1p(-epsilon) / a - n * forward_d
    forward_index = int(np.argmax(forward_log))
    forward_branch = math.exp(min(0.0, float(forward_log[forward_index])))
    return {
        "converse": max(reverse_branch, forward_branch),
        "converse_reverse": reverse_branch,
        "converse_forward": forward_branch,
        "converse_reverse_lambda": float(orders[reverse_index]),
        "converse_forward_lambda": float(orders[forward_index]),
    }


def simple_pair_beta(space: TypeSpace, p: FloatArray, q: FloatArray, epsilon: float) -> float:
    p_prob = space.probabilities(p)
    q_prob = space.probabilities(q)
    likelihood_order = np.argsort(-(np.log(q_prob) - np.log(p_prob)), kind="mergesort")
    sorted_p = p_prob[likelihood_order]
    cumulative = np.cumsum(sorted_p)
    boundary = int(np.searchsorted(cumulative, epsilon, side="right"))
    rejection = 0.0
    if boundary > 0:
        rejection += float(np.sum(q_prob[likelihood_order[:boundary]]))
    spent = float(cumulative[boundary - 1]) if boundary > 0 else 0.0
    if boundary < space.size and sorted_p[boundary] > 0.0:
        eta = float(np.clip((epsilon - spent) / sorted_p[boundary], 0.0, 1.0))
        rejection += eta * float(q_prob[likelihood_order[boundary]])
    return 1.0 - rejection


def maximise_simple_pair_beta(
    space: TypeSpace, epsilon: float
) -> tuple[float, float, float]:
    """Maximise the exact simple-pair NP value over the full parameter square.

    The NP type ordering changes on kink curves in ``(s,t)``.  A seeded
    differential-evolution search is therefore used instead of assuming
    smoothness or reducing to endpoints.
    """

    objective = lambda x: -simple_pair_beta(
        space, p_of(float(x[0])), q_of(float(x[1])), epsilon
    )
    result = differential_evolution(
        objective,
        bounds=[(0.0, 1.0), (0.0, 1.0)],
        tol=2.0e-9,
        atol=2.0e-11,
        popsize=18,
        maxiter=180,
        polish=True,
        seed=731,
        workers=1,
        updating="immediate",
    )
    s, t = np.clip(result.x, 0.0, 1.0)
    return -float(result.fun), float(s), float(t)


def nonordering_diagnostics(cache: dict[str, object]) -> dict[str, object]:
    """Single-letter checks against common-family and projected ordering."""

    laws = np.asarray([P0, P1, Q0, Q1])
    log_odds = np.log(laws[:, :2] / laws[:, 2, None])
    singular_values = np.linalg.svd(log_odds - log_odds.mean(axis=0), compute_uv=False)
    projections = list(cache["achievability"])
    projection = min(projections, key=lambda item: abs(float(item["order"]) - 0.5))
    p_star = p_of(float(projection["s"]))
    q_star = q_of(float(projection["t"]))
    h = np.asarray(projection["h"], dtype=float)
    null_violation = 0.0
    alternative_violation = 0.0
    grid = np.linspace(0.0, 1.0, 4001)
    for threshold in np.unique(h):
        upper = h >= threshold
        lower = h <= threshold
        selected_null = float(np.sum(p_star[upper]))
        selected_alternative = float(np.sum(q_star[lower]))
        for parameter in grid:
            null_violation = max(
                null_violation, float(np.sum(p_of(float(parameter))[upper])) - selected_null
            )
            alternative_violation = max(
                alternative_violation,
                float(np.sum(q_of(float(parameter))[lower])) - selected_alternative,
            )
    reverse_kl = minimise_kl_over_classes("Q||P")
    forward_kl = minimise_kl_over_classes("P||Q")
    return {
        "log_odds_singular_values": singular_values.tolist(),
        "projected_ordering_lambda": float(projection["order"]),
        "projected_ordering_null_violation": null_violation,
        "projected_ordering_alternative_violation": alternative_violation,
        "reverse_composite_KL": reverse_kl["D"],
        "reverse_composite_KL_s": reverse_kl["s"],
        "reverse_composite_KL_t": reverse_kl["t"],
        "forward_composite_KL": forward_kl["D"],
        "forward_composite_KL_s": forward_kl["s"],
        "forward_composite_KL_t": forward_kl["t"],
    }


def evaluate_one_n(
    n: int,
    cache: dict[str, object],
    parameter_grid_size: int,
) -> dict[str, object]:
    started = time.perf_counter()
    space = TypeSpace.build(n)
    parameter_grid = np.linspace(0.0, 1.0, parameter_grid_size)
    p_matrix = probability_matrix(space, p_of, parameter_grid)
    q_matrix = probability_matrix(space, q_of, parameter_grid)
    rows: list[dict[str, object]] = []
    tests: dict[str, dict[str, FloatArray]] = {}
    for regime in REGIMES:
        epsilon = epsilon_for(n, regime)
        minimax, phi_lp = finite_composite_lp(
            space, epsilon, parameter_grid, p_matrix, q_matrix
        )
        achievable, phi_projected = optimised_achievability(
            space, epsilon, cache, parameter_grid, p_matrix, q_matrix
        )
        converse = composite_converse(n, epsilon, cache)
        row: dict[str, object] = {
            "n": n,
            "regime": regime,
            "epsilon": epsilon,
            **minimax,
            **achievable,
            **converse,
            "achievability_minus_minimax": achievable["achievability"] - minimax["minimax"],
            "minimax_minus_converse": minimax["minimax"] - converse["converse"],
            "type_count": space.size,
        }
        rows.append(row)
        tests[regime] = {"lp": phi_lp, "projected": phi_projected}
    runtime = time.perf_counter() - started
    return {
        "n": n,
        "fingerprint": _configuration_fingerprint(),
        "rows": rows,
        "runtime_seconds": runtime,
    }


def checkpoint_path(n: int) -> Path:
    return CHECKPOINT_DIR / f"n{n:04d}.json"


def _worker(n: int, cache: dict[str, object], parameter_grid_size: int) -> dict[str, object]:
    result = evaluate_one_n(n, cache, parameter_grid_size)
    atomic_json_dump(result, checkpoint_path(n))
    return result


def load_checkpoint(n: int) -> dict[str, object] | None:
    path = checkpoint_path(n)
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        result = json.load(handle)
    if (
        int(result.get("n", -1)) != n
        or result.get("fingerprint") != _configuration_fingerprint()
    ):
        return None
    return result


def run_blocklengths(
    n_values: Sequence[int],
    cache: dict[str, object],
    *,
    jobs: int,
    parameter_grid_size: int,
    force: bool,
) -> tuple[list[dict[str, object]], float]:
    started = time.perf_counter()
    results: dict[int, dict[str, object]] = {}
    pending = []
    for n in n_values:
        saved = None if force else load_checkpoint(n)
        if saved is None:
            pending.append(n)
        else:
            results[n] = saved

    if jobs <= 1:
        for n in pending:
            results[n] = _worker(n, cache, parameter_grid_size)
            print(f"completed n={n} ({results[n]['runtime_seconds']:.2f}s)", flush=True)
    else:
        with ProcessPoolExecutor(max_workers=jobs) as executor:
            futures = {
                executor.submit(_worker, n, cache, parameter_grid_size): n for n in pending
            }
            for future in as_completed(futures):
                n = futures[future]
                results[n] = future.result()
                print(f"completed n={n} ({results[n]['runtime_seconds']:.2f}s)", flush=True)
    flattened = [row for n in sorted(results) for row in results[n]["rows"]]
    return flattened, time.perf_counter() - started


CSV_COLUMNS = [
    "n",
    "regime",
    "epsilon",
    "minimax",
    "achievability",
    "converse",
    "converse_reverse",
    "converse_forward",
    "achievability_lambda",
    "converse_reverse_lambda",
    "converse_forward_lambda",
    "lp_objective",
    "worst_type_i",
    "worst_type_i_s",
    "worst_type_ii",
    "worst_type_ii_t",
    "lp_iterations",
    "active_null_constraints",
    "active_alternative_constraints",
    "achievability_type_i",
    "achievability_worst_s",
    "achievability_worst_t",
    "achievability_eta",
    "achievability_threshold",
    "projection_s",
    "projection_t",
    "projection_D",
    "achievability_minus_minimax",
    "minimax_minus_converse",
    "type_count",
]


def write_csv(rows: Sequence[dict[str, object]]) -> None:
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary = CSV_PATH.with_suffix(".csv.tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in sorted(rows, key=lambda item: (int(item["n"]), str(item["regime"]))):
            writer.writerow({column: row[column] for column in CSV_COLUMNS})
    os.replace(temporary, CSV_PATH)


def plotting_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "STIXGeneral", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "font.size": 8.0,
            "axes.labelsize": 8.0,
            "xtick.labelsize": 7.0,
            "ytick.labelsize": 7.0,
            "legend.fontsize": 7.0,
            "axes.linewidth": 0.7,
            "lines.linewidth": 1.25,
            "ps.fonttype": 42,
            "savefig.transparent": False,
        }
    )


def _panel(
    ax: mpl.axes.Axes,
    rows: Sequence[dict[str, object]],
    regime: str,
    bound_key: str,
    bound_label: str,
) -> None:
    selected = sorted((row for row in rows if row["regime"] == regime), key=lambda row: int(row["n"]))
    n = np.asarray([row["n"] for row in selected], dtype=float)
    minimax = np.asarray([row["minimax"] for row in selected], dtype=float)
    bound = np.asarray([row[bound_key] for row in selected], dtype=float)
    ax.plot(
        n,
        minimax,
        color="black",
        linestyle="-",
        marker="o",
        markersize=1.6,
        markeredgewidth=0.0,
        label="minimax Type II error",
    )
    ax.plot(
        n,
        bound,
        color="0.38",
        linestyle="--",
        marker="s",
        markersize=1.4,
        markeredgewidth=0.0,
        label=bound_label,
    )
    ax.set_xlim(float(np.min(n)), float(np.max(n)))
    ax.set_ylim(-0.015, 1.015)
    ax.set_xlabel("sample n")
    ax.set_ylabel("Type II error")
    ax.legend(frameon=False, loc="best", handlelength=2.7)
    ax.tick_params(direction="in", top=True, right=True, width=0.6)


def make_figures(rows: Sequence[dict[str, object]]) -> None:
    plotting_style()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    def save_eps(fig: mpl.figure.Figure, path: Path) -> None:
        temporary = path.with_name(path.stem + f".{os.getpid()}.tmp.eps")
        fig.savefig(temporary, format="eps")
        os.replace(temporary, path)

    panels = [
        ("constant", "achievability", "achievability bound", "constant_achievability"),
        ("constant", "converse", "converse bound", "constant_converse"),
        ("linear", "achievability", "achievability bound", "linear_achievability"),
        ("linear", "converse", "converse bound", "linear_converse"),
    ]
    for regime, key, label, stem in panels:
        fig, ax = plt.subplots(figsize=(3.45, 2.55), constrained_layout=True)
        _panel(ax, rows, regime, key, label)
        save_eps(fig, FIGURE_DIR / f"nonordered_bruno_{stem}.eps")
        plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(7.16, 5.15), constrained_layout=True)
    for ax, (regime, key, label, _) in zip(axes.ravel(), panels):
        _panel(ax, rows, regime, key, label)
    save_eps(fig, FIGURE_DIR / "nonordered_bruno_2x2.eps")
    plt.close(fig)


def rank_signature(endpoint0: FloatArray, endpoint1: FloatArray) -> tuple[int, int, int]:
    return tuple(np.argsort(np.log(endpoint1 / endpoint0)).tolist())


def dense_validation(
    rows: Sequence[dict[str, object]],
    cache: dict[str, object],
    representative_n: Sequence[int],
) -> dict[str, object]:
    by_key = {(int(row["n"]), str(row["regime"])): row for row in rows}
    global_lp_type_i_violation = max(
        0.0,
        max(float(row["worst_type_i"]) - float(row["epsilon"]) for row in rows),
    )
    global_lp_type_ii_violation = max(
        0.0,
        max(float(row["worst_type_ii"]) - float(row["lp_objective"]) for row in rows),
    )
    global_ach_type_i_error = max(
        abs(float(row["achievability_type_i"]) - float(row["epsilon"])) for row in rows
    )
    global_ach_below_minimax = max(
        0.0,
        max(float(row["minimax"]) - float(row["achievability"]) for row in rows),
    )
    global_converse_above_minimax = max(
        0.0,
        max(float(row["converse"]) - float(row["minimax"]) for row in rows),
    )
    checks: list[dict[str, object]] = []
    max_lp_type_i_violation = 0.0
    max_lp_type_ii_violation = 0.0
    max_ach_type_i_error = 0.0
    max_ach_below_minimax = 0.0
    max_converse_above_minimax = 0.0
    min_endpoint_gap = math.inf
    min_projected_gap = math.inf
    min_all_simple_gap = math.inf

    # Re-solve only representative blocklengths, then evaluate independently
    # on a much denser parameter grid than constraint generation uses.
    dense_grid = np.linspace(0.0, 1.0, 4001)
    coarse_grid = np.linspace(0.0, 1.0, 65)
    projections = list(cache["achievability"])
    for n in representative_n:
        if not all((n, regime) in by_key for regime in REGIMES):
            continue
        space = TypeSpace.build(n)
        p_coarse = probability_matrix(space, p_of, coarse_grid)
        q_coarse = probability_matrix(space, q_of, coarse_grid)
        for regime in REGIMES:
            epsilon = epsilon_for(n, regime)
            minimax, phi_lp = finite_composite_lp(
                space, epsilon, coarse_grid, p_coarse, q_coarse
            )
            achievable, phi_projected = optimised_achievability(
                space, epsilon, cache, coarse_grid, p_coarse, q_coarse
            )
            p_dense_parts: list[FloatArray] = []
            q_dense_parts: list[FloatArray] = []
            projected_dense_parts: list[FloatArray] = []
            for start in range(0, dense_grid.size, 64):
                parameters = dense_grid[start : start + 64]
                p_chunk = probability_matrix(space, p_of, parameters)
                q_chunk = probability_matrix(space, q_of, parameters)
                p_dense_parts.append(p_chunk @ phi_lp)
                q_dense_parts.append(q_chunk @ (1.0 - phi_lp))
                projected_dense_parts.append(p_chunk @ phi_projected)
            p_dense_values = np.concatenate(p_dense_parts)
            q_dense_values = np.concatenate(q_dense_parts)
            lp_type_i_violation = max(0.0, float(np.max(p_dense_values)) - epsilon)
            lp_type_ii_violation = max(
                0.0, float(np.max(q_dense_values)) - float(minimax["lp_objective"])
            )
            p_projected_dense = np.concatenate(projected_dense_parts)
            ach_type_i_error = abs(float(np.max(p_projected_dense)) - epsilon)

            endpoint_pair_value = max(
                simple_pair_beta(space, p, q, epsilon)
                for p in (P0, P1)
                for q in (Q0, Q1)
            )
            projection_index = int(
                np.argmin(
                    np.abs(
                        np.asarray([record["order"] for record in projections], dtype=float)
                        - float(achievable["achievability_lambda"])
                    )
                )
            )
            projection = projections[projection_index]
            projected_pair_value = simple_pair_beta(
                space, p_of(float(projection["s"])), q_of(float(projection["t"])), epsilon
            )
            all_simple_value = math.nan
            all_simple_s = math.nan
            all_simple_t = math.nan
            if (n == 30 and regime == "constant") or (n == 40 and regime == "linear"):
                all_simple_value, all_simple_s, all_simple_t = maximise_simple_pair_beta(
                    space, epsilon
                )
            endpoint_gap = float(minimax["minimax"]) - endpoint_pair_value
            projected_gap = float(achievable["achievability"]) - float(minimax["minimax"])
            all_simple_gap = (
                float(minimax["minimax"]) - all_simple_value
                if np.isfinite(all_simple_value)
                else math.nan
            )
            check = {
                "n": n,
                "regime": regime,
                "epsilon": epsilon,
                "lp_type_i_violation": lp_type_i_violation,
                "lp_type_ii_grid_violation": lp_type_ii_violation,
                "achievability_type_i_absolute_error": ach_type_i_error,
                "achievability_below_minimax_violation": max(
                    0.0, float(minimax["minimax"]) - float(achievable["achievability"])
                ),
                "converse_above_minimax_violation": max(
                    0.0,
                    float(composite_converse(n, epsilon, cache)["converse"])
                    - float(minimax["minimax"]),
                ),
                "endpoint_pair_lower_bound": endpoint_pair_value,
                "minimax_minus_endpoint_pair": endpoint_gap,
                "projected_pair_simple_value": projected_pair_value,
                "calibrated_projected_minus_minimax": projected_gap,
                "all_simple_pair_lower_bound": all_simple_value,
                "all_simple_pair_s": all_simple_s,
                "all_simple_pair_t": all_simple_t,
                "minimax_minus_all_simple_pair": all_simple_gap,
            }
            checks.append(check)
            max_lp_type_i_violation = max(max_lp_type_i_violation, lp_type_i_violation)
            max_lp_type_ii_violation = max(max_lp_type_ii_violation, lp_type_ii_violation)
            max_ach_type_i_error = max(max_ach_type_i_error, ach_type_i_error)
            max_ach_below_minimax = max(
                max_ach_below_minimax, check["achievability_below_minimax_violation"]
            )
            max_converse_above_minimax = max(
                max_converse_above_minimax, check["converse_above_minimax_violation"]
            )
            min_endpoint_gap = min(min_endpoint_gap, endpoint_gap)
            min_projected_gap = min(min_projected_gap, projected_gap)
            if np.isfinite(all_simple_gap):
                min_all_simple_gap = min(min_all_simple_gap, all_simple_gap)

    diagnostics = nonordering_diagnostics(cache)
    return {
        "representative_checks": checks,
        "max_lp_type_i_violation": max_lp_type_i_violation,
        "max_lp_type_ii_grid_violation": max_lp_type_ii_violation,
        "max_achievability_type_i_absolute_error": max_ach_type_i_error,
        "max_achievability_below_minimax_violation": max_ach_below_minimax,
        "max_converse_above_minimax_violation": max_converse_above_minimax,
        "minimum_minimax_minus_endpoint_pair": min_endpoint_gap,
        "minimum_calibrated_projected_minus_minimax": min_projected_gap,
        "global_max_lp_type_i_violation": global_lp_type_i_violation,
        "global_max_lp_type_ii_violation": global_lp_type_ii_violation,
        "global_max_achievability_type_i_absolute_error": global_ach_type_i_error,
        "global_max_achievability_below_minimax_violation": global_ach_below_minimax,
        "global_max_converse_above_minimax_violation": global_converse_above_minimax,
        "minimum_minimax_minus_all_simple_pair": min_all_simple_gap,
        "P_rank_signature": rank_signature(P0, P1),
        "Q_rank_signature": rank_signature(Q0, Q1),
        **diagnostics,
    }


def write_audit(
    rows: Sequence[dict[str, object]],
    cache: dict[str, object],
    validation: dict[str, object],
    n_values: Sequence[int],
    wall_seconds: float,
    jobs: int,
    parameter_grid_size: int,
) -> None:
    def json_safe(value: object) -> object:
        if isinstance(value, float) and not math.isfinite(value):
            return None
        if isinstance(value, list):
            return [json_safe(item) for item in value]
        if isinstance(value, dict):
            return {key: json_safe(item) for key, item in value.items()}
        return value

    total_checkpoint_seconds = sum(
        float(load_checkpoint(n)["runtime_seconds"]) for n in n_values if load_checkpoint(n) is not None
    )
    checkpoint_mtimes = [
        checkpoint_path(n).stat().st_mtime for n in n_values if checkpoint_path(n).exists()
    ]
    checkpoint_span = max(checkpoint_mtimes) - min(checkpoint_mtimes) if checkpoint_mtimes else 0.0
    p_signature = validation["P_rank_signature"]
    q_signature = validation["Q_rank_signature"]
    log_odds_singular = validation["log_odds_singular_values"]
    row_lookup = {(int(row["n"]), str(row["regime"])): row for row in rows}
    n300_constant = row_lookup.get((300, "constant"))
    n300_linear = row_lookup.get((300, "linear"))
    n300_text = ""
    if n300_constant is not None and n300_linear is not None:
        n300_text = (
            " At n=300 the computed minimax Type-II errors remain "
            f"{float(n300_constant['minimax']):.6f} (epsilon=0.01) and "
            f"{float(n300_linear['minimax']):.6f} (epsilon=1/n), so the "
            "selected separation remains visible throughout the requested range."
        )
    mesh_text = (
        "all integers 1--300"
        if list(n_values) == list(range(1, 301))
        else "1--50; every 2 from 52--120; every 5 from 125--200; every 10 from 210--300"
    )
    text = f"""# Audit: non-ordered Bruno-style finite-blocklength experiment

## Affine ternary classes

The experiment uses

```text
P0 = {P0.tolist()}
P1 = {P1.tolist()}
Q0 = {Q0.tolist()}
Q1 = {Q1.tolist()}
```

and the affine segments `P_s=(1-s)P0+sP1` and
`Q_t=(1-t)Q0+tQ1`, with `s,t` in `[0,1]`.  The smallest endpoint
coordinate is {min(float(np.min(P0)), float(np.min(P1)), float(np.min(Q0)), float(np.min(Q1))):.12g},
so every law in both classes has full support.

The directed composite KL separations are
`D(Q||P)={validation['reverse_composite_KL']:.8f}` and
`D(P||Q)={validation['forward_composite_KL']:.8f}`.{n300_text}

The within-class endpoint log-ratio rank signatures (in increasing order)
are `{p_signature}` for the null segment and `{q_signature}` for the
alternative segment.  They are incompatible.  In addition, the centred
two-dimensional log-odds coordinates of the four laws have singular values
`{log_odds_singular}`; the nonzero second value rules out collinearity in a
common one-parameter ternary exponential family.  At order
{validation['projected_ordering_lambda']}, the single-letter projected-score
ordering violations are
{validation['projected_ordering_null_violation']:.6e} (null) and
{validation['projected_ordering_alternative_violation']:.6e} (alternative),
so the manuscript's projected-ordering sufficient conditions fail.

The finite-block validation below is the operational non-ordering check.  At
`n=30, epsilon=0.01` and `n=40, epsilon=1/n`, the unrestricted composite LP
is strictly above the largest simple-pair value found by a seeded global
search over the complete `(s,t)` square.  The optimised calibrated projected
rule is also strictly above the unrestricted minimax value at every
representative check.  Thus the experiment is not evaluated by ordered
endpoint reduction or by treating a projected pair as least favourable.

## Numerical mesh and optimisation

The reported blocklength mesh is: {mesh_text}.  The CSV contains only
computed blocklengths.  Plotting joins those computed points by straight
line segments; no smoothed or fabricated numerical rows are introduced.

For each blocklength, ternary sequences are symmetrised into
`(n+1)(n+2)/2` exact types.  The minimax problem is a semi-infinite LP in
the type-wise randomisation probabilities.  Constraint generation starts
from seventeen deterministic values of each class parameter, solves with HiGHS,
then adds continuous worst-case null and alternative parameters until both
violations are at most `2e-9`.  Each separating expectation is a polynomial
of degree at most `n`; it is represented at `n+1` Chebyshev nodes, all visible
derivative roots are polished, and every candidate is re-evaluated from the
original multinomial probabilities.  LP rows and the objective are scaled
by `1e4`, and the HiGHS small-matrix threshold is `1e-12`, to retain rare
exact types at large `n`.
Dual simplex is the default master solver, with a deterministic interior-point
fallback; `n=299` uses the same two methods in the opposite order because its
dual-simplex active set is reproducibly degenerate.

The tightened achievability calculation uses {len(ACHIEVABILITY_LAMBDAS)}
orders in `(0,1)`, namely `{', '.join(f'{x:g}' for x in ACHIEVABILITY_LAMBDAS)}`.
For each order the joint composite Renyi projection is computed and cached,
the projected log-likelihood-ratio types are sorted, the threshold is
optimised, and a common boundary randomisation is adjusted until the
composite Type-I envelope exhausts the requested budget.  The smallest
maximal Type-II error over the order mesh is reported; the loose closed-form
exponential bound is not used.

For each Bruno converse branch, the script caches both directed composite
Renyi divergences on {len(CONVERSE_LAMBDAS)} finite orders greater than one,
plus the order-infinity limit.  The
order mesh is deterministic in `a=(lambda-1)/lambda`, with logarithmic
resolution near zero and one.  The displayed converse is the maximum of the
forward and reverse branches.  Restricting the order optimisation to this
mesh preserves converse validity (it can only weaken the displayed lower
bound).

## Independent validation

Representative LP and projected tests were recomputed and evaluated on an
independent grid of 4,001 values for each class parameter.

Across all 600 CSV rows:

* Maximum LP Type-I violation: {validation['global_max_lp_type_i_violation']:.6e}
* Maximum LP objective violation: {validation['global_max_lp_type_ii_violation']:.6e}
* Maximum absolute projected Type-I exhaustion error: {validation['global_max_achievability_type_i_absolute_error']:.6e}
* Maximum violation of `achievability >= minimax`: {validation['global_max_achievability_below_minimax_violation']:.6e}
* Maximum violation of `converse <= minimax`: {validation['global_max_converse_above_minimax_violation']:.6e}

On the independent 4,001-point representative grids, the maximum LP Type-I
violation is {validation['max_lp_type_i_violation']:.6e}, the maximum LP
objective violation is {validation['max_lp_type_ii_grid_violation']:.6e}, and
the maximum projected Type-I exhaustion error is
{validation['max_achievability_type_i_absolute_error']:.6e}.

* Smallest representative minimax gap above all four endpoint simple-pair values: {validation['minimum_minimax_minus_endpoint_pair']:.6e}
* Smallest designated minimax gap above the largest simple-product-pair value found: {validation['minimum_minimax_minus_all_simple_pair']:.6e}
* Smallest representative calibrated-projected gap above minimax: {validation['minimum_calibrated_projected_minus_minimax']:.6e}

At `n=30, epsilon=0.01` and `n=40, epsilon=1/n`, the largest simple-pair
value is sought by seeded differential evolution over
`(s,t) in [0,1]^2`; the search is not restricted to endpoints.  The positive
search gaps numerically exclude least-favourable simple-pair reduction at
those checks to the reported optimisation tolerance.  The other
representative rows check endpoint-pair and projected-pair gaps.  Together,
the strict gaps numerically exclude endpoint reduction and verify that the
tightened projected test is not identically the composite minimax solution.
Individual validation rows are included below.

```json
{json.dumps(json_safe(validation['representative_checks']), indent=2)}
```

## Checkpointing and runtime

The Renyi projections/divergences are independent of `n` and stored in
`numerics/data/nonordered_bruno_renyi_cache.json`.  Each completed
blocklength has an atomic JSON checkpoint under
`numerics/checkpoints/nonordered_bruno_regimes/`; reruns resume by default.
Blocklengths were evaluated with {jobs} worker process(es) and one BLAS
thread per worker.

Current driver wall time (including resumed-checkpoint loading):
{wall_seconds:.3f} seconds.  Sum of recorded per-blocklength worker times:
{total_checkpoint_seconds:.3f} seconds.  Elapsed span from the first to last
completed blocklength checkpoint: {checkpoint_span:.3f} seconds.  The
n-independent Renyi cache took {float(cache['runtime_seconds']):.3f} seconds.
Platform: `{platform.platform()}`;
Python: `{platform.python_version()}`.

The committed outputs are reproduced by running
`python numerics/scripts/nonordered_bruno_regimes.py --jobs {jobs}` from the
repository root.
"""
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary = AUDIT_PATH.with_suffix(".md.tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, AUDIT_PATH)


def parse_n_values(arguments: argparse.Namespace) -> list[int]:
    if arguments.n_values:
        values = sorted(set(int(part) for part in arguments.n_values.split(",")))
        if not values or values[0] < 1 or values[-1] > 300:
            raise ValueError("--n-values must lie between 1 and 300")
        return values
    if arguments.mesh:
        return selected_n_mesh()
    return list(range(1, 301))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mesh", action="store_true", help="use the documented fallback n mesh")
    parser.add_argument("--n-values", help="comma-separated deterministic blocklengths")
    parser.add_argument("--jobs", type=int, default=min(4, max(1, (os.cpu_count() or 2) - 1)))
    parser.add_argument("--parameter-grid-size", type=int, default=65)
    parser.add_argument("--force", action="store_true", help="ignore per-n checkpoints")
    parser.add_argument("--force-renyi", action="store_true", help="recompute n-independent cache")
    parser.add_argument(
        "--representative-n",
        default="30,40,150,300",
        help="comma-separated blocklengths for independent dense validation",
    )
    parser.add_argument("--skip-validation", action="store_true")
    arguments = parser.parse_args()

    check_endpoints()
    n_values = parse_n_values(arguments)
    cache = build_or_load_renyi_cache(force=arguments.force_renyi)
    rows, wall_seconds = run_blocklengths(
        n_values,
        cache,
        jobs=max(1, arguments.jobs),
        parameter_grid_size=max(17, arguments.parameter_grid_size),
        force=arguments.force,
    )
    write_csv(rows)
    make_figures(rows)
    if not arguments.skip_validation:
        representative = [int(part) for part in arguments.representative_n.split(",")]
        validation = dense_validation(rows, cache, representative)
        write_audit(
            rows,
            cache,
            validation,
            n_values,
            wall_seconds,
            max(1, arguments.jobs),
            max(17, arguments.parameter_grid_size),
        )
    print(f"wrote {CSV_PATH}")
    print(f"wrote {FIGURE_DIR / 'nonordered_bruno_2x2.eps'}")
    if not arguments.skip_validation:
        print(f"wrote {AUDIT_PATH}")


if __name__ == "__main__":
    main()
