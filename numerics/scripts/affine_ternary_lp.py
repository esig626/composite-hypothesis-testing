#!/usr/bin/env python3
"""Exact-type/semi-infinite LP for affine ternary classes.

The test is symmetrised over ternary type classes.  Its variables are the
conditional probabilities ``a[k]`` of *accepting* the null on a type ``k``.
For finite active parameter sets S and T the master LP is

    minimise z
    subject to  -P_s^n[type] @ a <= -(1-epsilon),  s in S,
                 Q_t^n[type] @ a - z <= 0,         t in T,
                 0 <= a <= 1, 0 <= z <= 1.

The one-dimensional semi-infinite constraints are separated without an
endpoint assumption.  For fixed type values, their expectation along an
affine class is a polynomial of degree at most n.  We interpolate this
polynomial at n+1 Chebyshev nodes, locate all sign changes of its derivative
on an oversampled Chebyshev mesh, polish the roots, and evaluate the original
multinomial expectation at every candidate.  A separate dense-grid check is
available for validation.

This reusable solver underlies ``nonordered_bruno_regimes.py``.  It writes
only an optional NPZ checkpoint supplied by the caller.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
import warnings
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
from numpy.polynomial import chebyshev as cheb
from scipy.fft import dct
from scipy.optimize import OptimizeWarning, brentq, linprog
from scipy.special import gammaln


Array = np.ndarray


@dataclass(frozen=True)
class AffineTernaryClass:
    """Full-support affine line segment in the ternary simplex."""

    endpoint0: Array
    endpoint1: Array

    def __post_init__(self) -> None:
        p0 = np.asarray(self.endpoint0, dtype=float)
        p1 = np.asarray(self.endpoint1, dtype=float)
        if p0.shape != (3,) or p1.shape != (3,):
            raise ValueError("each endpoint must be a length-three vector")
        if np.any(p0 <= 0.0) or np.any(p1 <= 0.0):
            raise ValueError("the prototype requires full-support endpoints")
        if not np.isclose(p0.sum(), 1.0, atol=1e-13, rtol=0.0):
            raise ValueError("endpoint0 does not sum to one")
        if not np.isclose(p1.sum(), 1.0, atol=1e-13, rtol=0.0):
            raise ValueError("endpoint1 does not sum to one")
        object.__setattr__(self, "endpoint0", p0)
        object.__setattr__(self, "endpoint1", p1)

    def at(self, parameters: Sequence[float] | Array) -> Array:
        u = np.asarray(parameters, dtype=float).reshape(-1)
        if np.any((u < 0.0) | (u > 1.0)):
            raise ValueError("affine parameters must lie in [0,1]")
        return self.endpoint0 + u[:, None] * (self.endpoint1 - self.endpoint0)


@dataclass(frozen=True)
class TernaryTypeSpace:
    n: int
    counts: Array
    log_multinomial_coefficients: Array

    @property
    def size(self) -> int:
        return int(self.counts.shape[0])


@dataclass(frozen=True)
class MaximumResult:
    value: float
    parameter: float
    interpolation_error: float
    effective_degree: int
    candidate_count: int


@dataclass
class MinimaxResult:
    n: int
    epsilon: float
    beta: float
    acceptance: Array
    null_parameters: Array
    alternative_parameters: Array
    worst_null_parameter: float
    worst_alternative_parameter: float
    worst_type_i: float
    worst_type_ii: float
    null_violation: float
    alternative_violation: float
    iterations: int
    runtime_seconds: float
    solver_message: str
    converged: bool

    def summary(self) -> dict[str, object]:
        result = asdict(self)
        for key in ("acceptance", "null_parameters", "alternative_parameters"):
            result[key] = np.asarray(result[key]).tolist()
        return result


def ternary_type_space(n: int) -> TernaryTypeSpace:
    """Return all ``(k0,k1,k2)`` with sum n and their log coefficients."""

    if n < 1:
        raise ValueError("n must be positive")
    k0 = np.repeat(np.arange(n + 1), n + 1 - np.arange(n + 1))
    k1 = np.concatenate([np.arange(n - i + 1) for i in range(n + 1)])
    counts = np.column_stack((k0, k1, n - k0 - k1)).astype(np.int32)
    log_coefficients = gammaln(n + 1.0) - gammaln(counts + 1.0).sum(axis=1)
    expected_size = (n + 1) * (n + 2) // 2
    if counts.shape != (expected_size, 3):
        raise RuntimeError("internal type enumeration error")
    return TernaryTypeSpace(n, counts, log_coefficients)


def type_probability_matrix(
    type_space: TernaryTypeSpace,
    affine_class: AffineTernaryClass,
    parameters: Sequence[float] | Array,
    *,
    batch_size: int = 32,
) -> Array:
    """Rows are normalised multinomial probabilities over ternary types.

    Log probabilities avoid overflow in the multinomial coefficient and
    underflow is harmless for terms below the double-precision range.  Each
    row is renormalised, which removes the roughly 1e-13 accumulated error in
    ``exp(gammaln(...))`` at n=300.
    """

    u = np.asarray(parameters, dtype=float).reshape(-1)
    if u.size == 0:
        return np.empty((0, type_space.size), dtype=float)
    probabilities = affine_class.at(u)
    output = np.empty((u.size, type_space.size), dtype=float)
    for start in range(0, u.size, batch_size):
        stop = min(start + batch_size, u.size)
        log_weights = (
            type_space.log_multinomial_coefficients[:, None]
            + type_space.counts @ np.log(probabilities[start:stop]).T
        )
        weights = np.exp(log_weights)
        normalisers = weights.sum(axis=0)
        if np.any(~np.isfinite(normalisers)) or np.any(normalisers <= 0.0):
            raise FloatingPointError("invalid multinomial normaliser")
        weights /= normalisers
        output[start:stop] = weights.T
    return output


def expectations(
    type_space: TernaryTypeSpace,
    affine_class: AffineTernaryClass,
    type_values: Array,
    parameters: Sequence[float] | Array,
    *,
    batch_size: int = 32,
) -> Array:
    """Evaluate expectations without retaining a parameter-by-type matrix.

    This streamed implementation is important for independent validation:
    at n=300 a 10,001-point grid times 45,451 types would otherwise occupy
    about 3.6 GB in float64 before any solver storage is counted.
    """

    values = np.asarray(type_values, dtype=float)
    if values.shape != (type_space.size,):
        raise ValueError("type_values has the wrong length")
    u = np.asarray(parameters, dtype=float).reshape(-1)
    if u.size == 0:
        return np.empty(0, dtype=float)
    probabilities = affine_class.at(u)
    output = np.empty(u.size, dtype=float)
    for start in range(0, u.size, batch_size):
        stop = min(start + batch_size, u.size)
        log_weights = (
            type_space.log_multinomial_coefficients[:, None]
            + type_space.counts @ np.log(probabilities[start:stop]).T
        )
        weights = np.exp(log_weights)
        normalisers = weights.sum(axis=0)
        if np.any(~np.isfinite(normalisers)) or np.any(normalisers <= 0.0):
            raise FloatingPointError("invalid multinomial normaliser")
        weights /= normalisers
        output[start:stop] = values @ weights
    return output


def _chebyshev_coefficients(
    type_space: TernaryTypeSpace,
    affine_class: AffineTernaryClass,
    type_values: Array,
    *,
    trim_tolerance: float,
    batch_size: int,
) -> tuple[Array, Array, Array]:
    """Interpolate the degree-at-most-n expectation polynomial."""

    n = type_space.n
    # First-kind (Gauss) nodes, ordered from +1 to -1.  The DCT-II formula
    # below is exactly the one used for Chebyshev interpolation at these nodes.
    x = np.cos(np.pi * (np.arange(n + 1) + 0.5) / (n + 1))
    u = 0.5 * (x + 1.0)
    y = expectations(
        type_space, affine_class, type_values, u, batch_size=batch_size
    )
    coefficients = dct(y, type=2) / (n + 1)
    coefficients[0] *= 0.5
    coefficients = cheb.chebtrim(coefficients, tol=trim_tolerance)
    return coefficients, x, y


def maximise_affine_expectation(
    type_space: TernaryTypeSpace,
    affine_class: AffineTernaryClass,
    type_values: Array,
    *,
    trim_tolerance: float = 5e-13,
    derivative_oversampling: int = 16,
    interpolation_check_points: int = 17,
    batch_size: int = 32,
) -> MaximumResult:
    """Numerically maximise an expectation over the full affine segment.

    The expectation is a polynomial of degree at most n.  Candidate stationary
    points come from sign changes of the derivative on an oversampled
    Chebyshev mesh and are polished with Brent's method.  Endpoints and sampled
    local maxima are included defensively.  Final values are always evaluated
    from the multinomial probabilities, not from the interpolant.
    """

    if derivative_oversampling < 4:
        raise ValueError("derivative_oversampling must be at least four")
    values = np.asarray(type_values, dtype=float)
    if values.shape != (type_space.size,):
        raise ValueError("type_values has the wrong length")

    coefficients, interpolation_nodes, interpolation_values = (
        _chebyshev_coefficients(
            type_space,
            affine_class,
            values,
            trim_tolerance=trim_tolerance,
            batch_size=batch_size,
        )
    )
    derivative = cheb.chebder(coefficients)
    mesh_size = max(65, derivative_oversampling * type_space.n + 1)
    # Increasing x mesh with O(n^-2) resolution near both endpoints.
    x_mesh = -np.cos(np.linspace(0.0, np.pi, mesh_size))
    polynomial_values = cheb.chebval(x_mesh, coefficients)

    candidates: list[float] = [-1.0, 1.0]
    if derivative.size > 1 or derivative[0] != 0.0:
        derivative_values = cheb.chebval(x_mesh, derivative)
        for i in range(mesh_size - 1):
            left_value = derivative_values[i]
            right_value = derivative_values[i + 1]
            if left_value == 0.0:
                candidates.append(float(x_mesh[i]))
            if left_value * right_value < 0.0:
                try:
                    root = brentq(
                        lambda x: float(cheb.chebval(x, derivative)),
                        float(x_mesh[i]),
                        float(x_mesh[i + 1]),
                        xtol=2e-14,
                        rtol=8 * np.finfo(float).eps,
                        maxiter=100,
                    )
                    candidates.append(float(root))
                except ValueError:
                    # A derivative evaluation can be perturbed at the last bit;
                    # the sampled local-maximum fallback below still covers it.
                    pass
        if derivative_values[-1] == 0.0:
            candidates.append(float(x_mesh[-1]))

    sampled_maxima = np.flatnonzero(
        (polynomial_values[1:-1] >= polynomial_values[:-2])
        & (polynomial_values[1:-1] >= polynomial_values[2:])
    ) + 1
    candidates.extend(x_mesh[sampled_maxima].tolist())
    candidate_x = np.unique(np.clip(np.asarray(candidates), -1.0, 1.0))
    candidate_u = 0.5 * (candidate_x + 1.0)
    candidate_values = expectations(
        type_space, affine_class, values, candidate_u, batch_size=batch_size
    )
    best = int(np.argmax(candidate_values))

    check_count = max(3, interpolation_check_points)
    # Shifted deterministic points avoid reusing the interpolation nodes.
    check_x = -np.cos(
        np.pi * (np.arange(check_count) + 0.371) / check_count
    )
    direct_check = expectations(
        type_space,
        affine_class,
        values,
        0.5 * (check_x + 1.0),
        batch_size=batch_size,
    )
    interpolation_error = max(
        float(
            np.max(
                np.abs(
                    cheb.chebval(interpolation_nodes, coefficients)
                    - interpolation_values
                )
            )
        ),
        float(np.max(np.abs(cheb.chebval(check_x, coefficients) - direct_check))),
    )
    return MaximumResult(
        value=float(candidate_values[best]),
        parameter=float(candidate_u[best]),
        interpolation_error=interpolation_error,
        effective_degree=int(coefficients.size - 1),
        candidate_count=int(candidate_u.size),
    )


def dense_grid_maximum(
    type_space: TernaryTypeSpace,
    affine_class: AffineTernaryClass,
    type_values: Array,
    *,
    grid_size: int = 10001,
    batch_size: int = 32,
) -> MaximumResult:
    """Independent deterministic-grid maximum; no interpolation is applied."""

    if grid_size < 2:
        raise ValueError("grid_size must be at least two")
    grid = np.linspace(0.0, 1.0, grid_size)
    grid_values = expectations(
        type_space, affine_class, type_values, grid, batch_size=batch_size
    )
    best = int(np.argmax(grid_values))
    return MaximumResult(
        value=float(grid_values[best]),
        parameter=float(grid[best]),
        interpolation_error=float("nan"),
        effective_degree=type_space.n,
        candidate_count=grid_size,
    )


def _unique_parameters(values: Iterable[float], tolerance: float) -> list[float]:
    result: list[float] = []
    for raw_value in sorted(float(value) for value in values):
        value = min(1.0, max(0.0, raw_value))
        if not result or abs(value - result[-1]) > tolerance:
            result.append(value)
    return result


def _problem_digest(
    n: int,
    epsilon: float,
    null_class: AffineTernaryClass,
    alternative_class: AffineTernaryClass,
) -> str:
    payload = np.concatenate(
        (
            np.asarray([n, epsilon], dtype=np.float64),
            null_class.endpoint0,
            null_class.endpoint1,
            alternative_class.endpoint0,
            alternative_class.endpoint1,
        )
    )
    return hashlib.sha256(payload.tobytes()).hexdigest()


def _save_checkpoint(
    path: Path,
    *,
    digest: str,
    iteration: int,
    null_parameters: Sequence[float],
    alternative_parameters: Sequence[float],
    beta: float,
    acceptance: Array,
    converged: bool,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    metadata = json.dumps(
        {
            "digest": digest,
            "iteration": int(iteration),
            "beta": float(beta),
            "converged": bool(converged),
        },
        sort_keys=True,
    )
    with temporary.open("wb") as handle:
        np.savez_compressed(
            handle,
            metadata=np.asarray(metadata),
            null_parameters=np.asarray(null_parameters, dtype=float),
            alternative_parameters=np.asarray(alternative_parameters, dtype=float),
            acceptance=np.asarray(acceptance, dtype=float),
        )
    os.replace(temporary, path)


def _load_checkpoint(path: Path, digest: str) -> dict[str, object]:
    with np.load(path, allow_pickle=False) as archive:
        metadata = json.loads(str(archive["metadata"]))
        if metadata.get("digest") != digest:
            raise ValueError(f"checkpoint {path} belongs to another LP problem")
        return {
            **metadata,
            "null_parameters": archive["null_parameters"].copy(),
            "alternative_parameters": archive["alternative_parameters"].copy(),
            "acceptance": archive["acceptance"].copy(),
        }


def solve_composite_minimax(
    n: int,
    epsilon: float,
    null_class: AffineTernaryClass,
    alternative_class: AffineTernaryClass,
    *,
    initial_grid_size: int = 17,
    initial_null_parameters: Sequence[float] | None = None,
    initial_alternative_parameters: Sequence[float] | None = None,
    constraint_tolerance: float = 2e-9,
    parameter_tolerance: float = 2e-10,
    max_iterations: int = 40,
    row_scale: float = 1e4,
    objective_scale: float | None = None,
    small_matrix_value: float = 1e-12,
    primal_feasibility_tolerance: float = 1e-10,
    dual_feasibility_tolerance: float = 1e-10,
    solver_methods: Sequence[str] = ("highs-ds", "highs-ipm"),
    derivative_oversampling: int = 16,
    trim_tolerance: float = 5e-13,
    checkpoint_path: str | Path | None = None,
    resume: bool = True,
    verbose: bool = False,
) -> MinimaxResult:
    """Solve the symmetrised semi-infinite LP by constraint generation."""

    if not 0.0 < epsilon < 1.0:
        raise ValueError("epsilon must lie strictly between zero and one")
    if initial_grid_size < 2:
        raise ValueError("initial_grid_size must be at least two")
    if row_scale <= 0.0:
        raise ValueError("row_scale must be positive")
    if objective_scale is None:
        objective_scale = row_scale
    if objective_scale <= 0.0:
        raise ValueError("objective_scale must be positive")
    if not solver_methods or any(method not in {"highs-ds", "highs-ipm"} for method in solver_methods):
        raise ValueError("solver_methods may contain only highs-ds and highs-ipm")

    started = time.perf_counter()
    type_space = ternary_type_space(n)
    digest = _problem_digest(n, epsilon, null_class, alternative_class)
    checkpoint = Path(checkpoint_path) if checkpoint_path is not None else None
    base_grid = np.linspace(0.0, 1.0, initial_grid_size)
    null_parameters = _unique_parameters(
        base_grid if initial_null_parameters is None else initial_null_parameters,
        parameter_tolerance,
    )
    alternative_parameters = _unique_parameters(
        base_grid
        if initial_alternative_parameters is None
        else initial_alternative_parameters,
        parameter_tolerance,
    )
    starting_iteration = 0
    if checkpoint is not None and resume and checkpoint.exists():
        state = _load_checkpoint(checkpoint, digest)
        null_parameters = _unique_parameters(
            state["null_parameters"], parameter_tolerance
        )
        alternative_parameters = _unique_parameters(
            state["alternative_parameters"], parameter_tolerance
        )
        starting_iteration = int(state["iteration"]) + 1

    last_acceptance = np.ones(type_space.size)
    last_beta = 1.0
    last_null = MaximumResult(1.0, 0.0, np.nan, 0, 0)
    last_alternative = MaximumResult(1.0, 0.0, np.nan, 0, 0)
    solver_message = "not started"
    converged = False
    iterations_used = starting_iteration

    for iteration in range(starting_iteration, max_iterations):
        null_matrix = type_probability_matrix(
            type_space, null_class, null_parameters
        )
        alternative_matrix = type_probability_matrix(
            type_space, alternative_class, alternative_parameters
        )
        number_of_types = type_space.size
        number_of_rows = len(null_parameters) + len(alternative_parameters)
        lhs = np.zeros((number_of_rows, number_of_types + 1), dtype=float)
        rhs = np.concatenate(
            (
                np.full(len(null_parameters), -(1.0 - epsilon)),
                np.zeros(len(alternative_parameters)),
            )
        )
        lhs[: len(null_parameters), :number_of_types] = -null_matrix
        lhs[len(null_parameters) :, :number_of_types] = alternative_matrix
        lhs[len(null_parameters) :, -1] = -1.0
        objective = np.zeros(number_of_types + 1)
        # Scaling the objective matters when beta is around 1e-7: with an
        # unscaled coefficient HiGHS' dual feasibility tolerance can swamp the
        # reduced cost of z, causing non-monotone master objectives.  A common
        # row/objective scale leaves the mathematical LP unchanged.
        objective[-1] = objective_scale

        # SciPy does not list small_matrix_value in linprog's public options,
        # but passes it to HiGHS.  Suppress only that expected wrapper warning.
        # A rare HiGHS dual-simplex Status 0 was reproducible for one n=300
        # active set at scale 1e5; the identical LP solved with HiGHS IPM.
        # Retrying the same immutable master problem is safe and deterministic.
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message="Unrecognized options detected.*small_matrix_value",
                category=OptimizeWarning,
            )
            solver_failures: list[str] = []
            solution = None
            selected_method = ""
            for method in solver_methods:
                candidate = linprog(
                    objective,
                    A_ub=row_scale * lhs,
                    b_ub=row_scale * rhs,
                    bounds=[(0.0, 1.0)] * (number_of_types + 1),
                    method=method,
                    options={
                        "primal_feasibility_tolerance": primal_feasibility_tolerance,
                        "dual_feasibility_tolerance": dual_feasibility_tolerance,
                        "ipm_optimality_tolerance": 1e-12,
                        "small_matrix_value": small_matrix_value,
                    },
                )
                if candidate.success:
                    solution = candidate
                    selected_method = method
                    break
                solver_failures.append(f"{method}: {candidate.message}")
        if solution is None:
            raise RuntimeError(
                "finite master LP failed with both HiGHS methods: "
                + " | ".join(solver_failures)
            )
        solver_message = f"{selected_method}: {solution.message}"

        last_acceptance = np.clip(solution.x[:-1], 0.0, 1.0)
        last_beta = float(solution.x[-1])
        last_null = maximise_affine_expectation(
            type_space,
            null_class,
            1.0 - last_acceptance,
            trim_tolerance=trim_tolerance,
            derivative_oversampling=derivative_oversampling,
        )
        last_alternative = maximise_affine_expectation(
            type_space,
            alternative_class,
            last_acceptance,
            trim_tolerance=trim_tolerance,
            derivative_oversampling=derivative_oversampling,
        )
        null_violation = last_null.value - epsilon
        alternative_violation = last_alternative.value - last_beta
        iterations_used = iteration + 1

        if verbose:
            print(
                f"iteration={iteration:02d} types={number_of_types} "
                f"active=({len(null_parameters)},{len(alternative_parameters)}) "
                f"beta={last_beta:.12g} "
                f"violations=({null_violation:.3e},{alternative_violation:.3e}) "
                f"argmax=({last_null.parameter:.9f},"
                f"{last_alternative.parameter:.9f})",
                flush=True,
            )

        converged = max(null_violation, alternative_violation) <= constraint_tolerance
        if checkpoint is not None:
            _save_checkpoint(
                checkpoint,
                digest=digest,
                iteration=iteration,
                null_parameters=null_parameters,
                alternative_parameters=alternative_parameters,
                beta=last_beta,
                acceptance=last_acceptance,
                converged=converged,
            )
        if converged:
            break

        added = False
        if null_violation > constraint_tolerance:
            if min(abs(last_null.parameter - np.asarray(null_parameters))) > parameter_tolerance:
                null_parameters.append(last_null.parameter)
                null_parameters.sort()
                added = True
        if alternative_violation > constraint_tolerance:
            if (
                min(
                    abs(
                        last_alternative.parameter
                        - np.asarray(alternative_parameters)
                    )
                )
                > parameter_tolerance
            ):
                alternative_parameters.append(last_alternative.parameter)
                alternative_parameters.sort()
                added = True
        if not added:
            raise RuntimeError(
                "constraint generation stalled at an existing parameter; "
                "increase row_scale or relax the numerical tolerances"
            )

    runtime = time.perf_counter() - started
    return MinimaxResult(
        n=n,
        epsilon=epsilon,
        beta=last_beta,
        acceptance=last_acceptance,
        null_parameters=np.asarray(null_parameters),
        alternative_parameters=np.asarray(alternative_parameters),
        worst_null_parameter=last_null.parameter,
        worst_alternative_parameter=last_alternative.parameter,
        worst_type_i=last_null.value,
        worst_type_ii=last_alternative.value,
        null_violation=last_null.value - epsilon,
        alternative_violation=last_alternative.value - last_beta,
        iterations=iterations_used,
        runtime_seconds=runtime,
        solver_message=solver_message,
        converged=converged,
    )


def validate_result_on_grid(
    result: MinimaxResult,
    null_class: AffineTernaryClass,
    alternative_class: AffineTernaryClass,
    *,
    grid_size: int = 10001,
) -> dict[str, float]:
    """Independently re-evaluate both constraints on a uniform dense grid."""

    type_space = ternary_type_space(result.n)
    null_check = dense_grid_maximum(
        type_space,
        null_class,
        1.0 - result.acceptance,
        grid_size=grid_size,
    )
    alternative_check = dense_grid_maximum(
        type_space,
        alternative_class,
        result.acceptance,
        grid_size=grid_size,
    )
    return {
        "grid_size": float(grid_size),
        "worst_type_i_grid": null_check.value,
        "worst_type_i_grid_parameter": null_check.parameter,
        "type_i_grid_violation": null_check.value - result.epsilon,
        "worst_type_ii_grid": alternative_check.value,
        "worst_type_ii_grid_parameter": alternative_check.parameter,
        "type_ii_grid_violation": alternative_check.value - result.beta,
        "separator_minus_grid_type_i": result.worst_type_i - null_check.value,
        "separator_minus_grid_type_ii": result.worst_type_ii
        - alternative_check.value,
    }


def simple_pair_beta(
    type_space: TernaryTypeSpace,
    null_distribution: Array,
    alternative_distribution: Array,
    epsilon: float,
) -> float:
    """Exact randomised Neyman--Pearson Type-II value for one simple pair."""

    p = np.asarray(null_distribution, dtype=float)
    q = np.asarray(alternative_distribution, dtype=float)
    if p.shape != (3,) or q.shape != (3,) or np.any(p <= 0) or np.any(q <= 0):
        raise ValueError("simple-pair distributions must have full ternary support")
    p_types = np.exp(
        type_space.log_multinomial_coefficients
        + type_space.counts @ np.log(p)
    )
    q_types = np.exp(
        type_space.log_multinomial_coefficients
        + type_space.counts @ np.log(q)
    )
    p_types /= p_types.sum()
    q_types /= q_types.sum()
    scores = type_space.counts @ (np.log(q) - np.log(p))
    order = np.argsort(-scores, kind="stable")
    p_sorted = p_types[order]
    q_sorted = q_types[order]
    cumulative_p = np.cumsum(p_sorted)
    boundary = int(np.searchsorted(cumulative_p, epsilon, side="right"))
    q_rejected = float(q_sorted[:boundary].sum())
    p_used = float(p_sorted[:boundary].sum())
    if boundary < type_space.size and p_used < epsilon:
        fraction = (epsilon - p_used) / p_sorted[boundary]
        q_rejected += float(fraction * q_sorted[boundary])
    return max(0.0, min(1.0, 1.0 - q_rejected))


def _parse_distribution(text: str) -> Array:
    values = np.asarray([float(item) for item in text.split(",")], dtype=float)
    if values.shape != (3,):
        raise argparse.ArgumentTypeError("use three comma-separated probabilities")
    return values


def _self_test() -> None:
    distribution = np.asarray([0.2, 0.3, 0.5])
    identical = AffineTernaryClass(distribution, distribution)
    result = solve_composite_minimax(
        8,
        0.01,
        identical,
        identical,
        initial_grid_size=3,
        constraint_tolerance=2e-9,
    )
    if not result.converged or abs(result.beta - 0.99) > 2e-8:
        raise AssertionError(f"identical-law check failed: beta={result.beta}")
    grid = validate_result_on_grid(result, identical, identical, grid_size=1001)
    if max(grid["type_i_grid_violation"], grid["type_ii_grid_violation"]) > 2e-8:
        raise AssertionError(f"dense-grid check failed: {grid}")
    type_space = ternary_type_space(8)
    pair_value = simple_pair_beta(type_space, distribution, distribution, 0.01)
    if abs(pair_value - 0.99) > 2e-12:
        raise AssertionError(f"simple-pair check failed: beta={pair_value}")
    print("self-test passed")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=20)
    parser.add_argument("--epsilon", type=float, default=0.01)
    parser.add_argument("--p0", type=_parse_distribution, default="0.327,0.418,0.255")
    parser.add_argument("--p1", type=_parse_distribution, default="0.563,0.266,0.171")
    parser.add_argument("--q0", type=_parse_distribution, default="0.143,0.357,0.500")
    parser.add_argument("--q1", type=_parse_distribution, default="0.379,0.205,0.416")
    parser.add_argument("--initial-grid-size", type=int, default=17)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--validation-grid-size", type=int, default=0)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        _self_test()
        return

    null_class = AffineTernaryClass(args.p0, args.p1)
    alternative_class = AffineTernaryClass(args.q0, args.q1)
    result = solve_composite_minimax(
        args.n,
        args.epsilon,
        null_class,
        alternative_class,
        initial_grid_size=args.initial_grid_size,
        checkpoint_path=args.checkpoint,
        verbose=args.verbose,
    )
    output: dict[str, object] = {"result": result.summary()}
    # The full decision vector is in a checkpoint when one was requested; do
    # not flood standard output with O(n^2) entries.
    output["result"].pop("acceptance")
    if args.validation_grid_size:
        output["validation"] = validate_result_on_grid(
            result,
            null_class,
            alternative_class,
            grid_size=args.validation_grid_size,
        )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
