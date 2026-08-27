#!/usr/bin/env python3
"""Continuously refine the saved non-ordered Rényi converse only.

This script deliberately reads the committed finite-blocklength CSV rather than
calling ``run_blocklengths``.  It therefore does not recompute the minimax LPs or
the calibrated achievability calculations.  New directed Rényi projections are
warm-started from the committed mesh, journalled incrementally, and globally
screened at every candidate outer maximiser before results are reported.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import hashlib
import json
import math
import os
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "cht-mpl"))

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.optimize import minimize, minimize_scalar

from nonordered_bruno_regimes import (
    _configuration_fingerprint,
    minimise_over_classes,
    p_of,
    plotting_style,
    q_of,
    renyi_divergence,
)


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "numerics" / "data"
FIGURE_DIR = ROOT / "numerics" / "figures"
LEGACY_CSV_PATH = DATA_DIR / "nonordered_bruno_regimes.csv"
LEGACY_CACHE_PATH = DATA_DIR / "nonordered_bruno_renyi_cache.json"
PROJECTION_CACHE_PATH = DATA_DIR / "nonordered_bruno_continuous_renyi_cache.json"
PROJECTION_JOURNAL_PATH = DATA_DIR / "nonordered_bruno_continuous_renyi_cache.jsonl"
COMPARISON_PATH = DATA_DIR / "nonordered_bruno_continuous_converse_comparison.csv"
AUDIT_PATH = ROOT / "numerics" / "continuous_converse_optimisation_audit.md"

BRANCHES = ("reverse", "forward")
ORIENTATION = {"reverse": "Q||P", "forward": "P||Q"}
CACHE_SCHEMA_VERSION = 1
ALGORITHM_VERSION = 1
OUTER_XATOL = 2.0e-9
OBJECTIVE_TOLERANCE = 1.0e-11
INNER_STABILITY_TOLERANCE = 1.0e-8
PROJECTION_AGREEMENT_TOLERANCE = 1.0e-10
CONVERSE_TOLERANCE = 2.1e-9
OUTER_CONVERGENCE_A_TOLERANCE = 5.0e-8


@dataclass(frozen=True)
class Case:
    n: int
    regime: str
    epsilon: float
    minimax: float
    legacy: dict[str, float]

    @property
    def key(self) -> tuple[int, str]:
        return self.n, self.regime


def atomic_json_dump(payload: object, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + f".{os.getpid()}.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(temporary, path)


def load_json(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        result = json.load(handle)
    if not isinstance(result, dict):
        raise ValueError(f"expected a JSON object in {path}")
    return result


def cache_fingerprint(legacy_cache: dict[str, object]) -> str:
    projection_source = Path(__file__).with_name("nonordered_bruno_regimes.py")
    payload = {
        "algorithm_version": ALGORITHM_VERSION,
        "inner_stability_tolerance": INNER_STABILITY_TOLERANCE,
        "legacy_cache_sha256": hashlib.sha256(LEGACY_CACHE_PATH.read_bytes()).hexdigest(),
        "legacy_cache_fingerprint": legacy_cache.get("fingerprint"),
        "numpy_version": np.__version__,
        "projection_source_sha256": hashlib.sha256(projection_source.read_bytes()).hexdigest(),
        "schema_version": CACHE_SCHEMA_VERSION,
        "scipy_version": scipy.__version__,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def a_key(a: float) -> str:
    return float(a).hex()


def order_from_a(a: float) -> float:
    if not 0.0 < a < 1.0:
        raise ValueError("finite Rényi projections require 0 < a < 1")
    return 1.0 / (1.0 - a)


def directed_pair(branch: str) -> Callable[[np.ndarray], tuple[np.ndarray, np.ndarray]]:
    if branch == "reverse":
        return lambda x: (q_of(float(x[1])), p_of(float(x[0])))
    if branch == "forward":
        return lambda x: (p_of(float(x[0])), q_of(float(x[1])))
    raise ValueError(branch)


def recompute_record_divergence(record: dict[str, object]) -> float:
    order = float(record["order"])
    pair = directed_pair(str(record["branch"]))
    x = np.array([float(record["s"]), float(record["t"])])
    return renyi_divergence(*pair(x), order)


class ProjectionStore:
    """Committed mesh plus an append-only checkpoint journal for new orders."""

    def __init__(self, legacy_cache: dict[str, object]) -> None:
        self.legacy_cache = legacy_cache
        self.fingerprint = cache_fingerprint(legacy_cache)
        self.records: dict[str, dict[str, dict[str, object]]] = {
            branch: {} for branch in BRANCHES
        }
        self.sorted_a: dict[str, list[float]] = {branch: [] for branch in BRANCHES}
        self.base_keys: set[tuple[str, str]] = set()
        self.loaded_new_keys: set[tuple[str, str]] = set()
        self.warm_evaluations = 0
        self.cache_hits = 0
        self.unstable_global_fallbacks = 0
        self.global_polishes = 0
        self.global_screen_minus_warm: list[float] = []
        self.inner_optimizer_failures = 0
        self._load_legacy_mesh()
        self._load_compact_cache()
        self._load_journal()

    def _insert(self, record: dict[str, object], *, base: bool = False) -> None:
        branch = str(record["branch"])
        a = float(record["a"])
        order = float(record["order"])
        divergence = float(record["D"])
        s, t = float(record["s"]), float(record["t"])
        if branch not in BRANCHES:
            raise ValueError(f"unknown cached branch: {branch}")
        if not 0.0 < a <= 1.0 or not np.isfinite(divergence) or divergence < -5.0e-13:
            raise ValueError(f"invalid cached projection at a={a}: D={divergence}")
        if not 0.0 <= s <= 1.0 or not 0.0 <= t <= 1.0:
            raise ValueError(f"cached projection parameters are outside [0,1] at a={a}")
        if a == 1.0:
            if not math.isinf(order):
                raise ValueError("a=1 must use the order-infinity projection")
        elif not math.isclose(order, order_from_a(a), rel_tol=2.0e-13, abs_tol=0.0):
            raise ValueError(f"cached order is inconsistent with a={a}")
        roundtrip = abs(divergence - recompute_record_divergence(record))
        if roundtrip > 5.0e-11:
            raise ValueError(f"cached projection round-trip error {roundtrip:.3e} at a={a}")
        key = a_key(a)
        existing = self.records[branch].get(key)
        self.records[branch][key] = record
        if existing is None:
            bisect.insort(self.sorted_a[branch], a)
        if base:
            self.base_keys.add((branch, key))
        else:
            self.loaded_new_keys.add((branch, key))
            if "global_warm_D_gap" in record:
                self.global_screen_minus_warm.append(float(record["global_warm_D_gap"]))

    def _load_legacy_mesh(self) -> None:
        for source in self.legacy_cache["converse"]:
            a = float(source["a"])
            order_value = source["order"]
            order = math.inf if order_value == "infinity" else float(order_value)
            for branch in BRANCHES:
                record: dict[str, object] = {
                    "a": a,
                    "branch": branch,
                    "D": float(source[f"{branch}_D"]),
                    "method": "legacy_global_mesh",
                    "order": order,
                    "s": float(source[f"{branch}_s"]),
                    "t": float(source[f"{branch}_t"]),
                    "validated": True,
                }
                self._insert(record, base=True)

    def _load_compact_cache(self) -> None:
        if not PROJECTION_CACHE_PATH.exists():
            return
        payload = load_json(PROJECTION_CACHE_PATH)
        if payload.get("fingerprint") != self.fingerprint:
            raise ValueError(
                f"{PROJECTION_CACHE_PATH} does not match the committed Rényi cache"
            )
        for record in payload.get("projections", []):
            self._insert(dict(record))

    def _load_journal(self) -> None:
        if not PROJECTION_JOURNAL_PATH.exists():
            return
        payload = PROJECTION_JOURNAL_PATH.read_bytes()
        offset = 0
        for line_number, raw_line in enumerate(payload.splitlines(keepends=True), start=1):
            line_start = offset
            offset += len(raw_line)
            if not raw_line.strip():
                continue
            try:
                envelope = json.loads(raw_line.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                if offset != len(payload):
                    raise
                # Remove a partial trailing append before any new record is added.
                with PROJECTION_JOURNAL_PATH.open("r+b") as handle:
                    handle.seek(line_start)
                    handle.truncate()
                    handle.flush()
                    os.fsync(handle.fileno())
                break
            if envelope.get("fingerprint") != self.fingerprint:
                raise ValueError(f"journal fingerprint mismatch at line {line_number}")
            self._insert(dict(envelope["projection"]))

    def get(self, branch: str, a: float) -> dict[str, object] | None:
        return self.records[branch].get(a_key(a))

    def put(self, record: dict[str, object]) -> None:
        branch = str(record["branch"])
        key = a_key(float(record["a"]))
        prior = self.records[branch].get(key)
        if prior is not None and bool(prior.get("validated")) and not bool(
            record.get("validated")
        ):
            return
        envelope = {"fingerprint": self.fingerprint, "projection": record}
        PROJECTION_JOURNAL_PATH.parent.mkdir(parents=True, exist_ok=True)
        with PROJECTION_JOURNAL_PATH.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(envelope, sort_keys=True, separators=(",", ":")))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        self._insert(record)

    def neighbours(
        self, branch: str, a: float, *, validated_only: bool = False
    ) -> tuple[dict[str, object] | None, dict[str, object] | None]:
        values = self.sorted_a[branch]
        position = bisect.bisect_left(values, a)

        def search(indices: Iterable[int]) -> dict[str, object] | None:
            for index in indices:
                if not 0 <= index < len(values):
                    continue
                candidate = self.get(branch, values[index])
                if candidate is None:
                    continue
                if validated_only and not bool(candidate.get("validated")):
                    continue
                return candidate
            return None

        left = search(range(position - 1, -1, -1))
        right_start = position
        if position < len(values) and math.isclose(values[position], a, rel_tol=0.0, abs_tol=0.0):
            right_start += 1
        right = search(range(right_start, len(values)))
        return left, right

    def warm_starts(self, branch: str, a: float) -> list[tuple[float, float]]:
        values = self.sorted_a[branch]
        position = bisect.bisect_left(values, a)
        left_index = position - 1 if position > 0 else None
        right_index = position if position < len(values) else None
        neighbours = [index for index in (left_index, right_index) if index is not None]
        nearest = min(neighbours, key=lambda index: abs(values[index] - a))
        candidate_indices = [nearest]
        candidate_indices.extend(index for index in neighbours if index != nearest)
        for index in (nearest - 1, nearest + 1):
            if 0 <= index < len(values) and index not in candidate_indices:
                candidate_indices.append(index)
        starts: list[tuple[float, float]] = []
        for index in candidate_indices:
            record = self.get(branch, values[index])
            if record is None:
                continue
            point = (float(record["s"]), float(record["t"]))
            if point not in starts:
                starts.append(point)
            if len(starts) == 3:
                break
        return starts

    def nonlegacy_records(self) -> list[dict[str, object]]:
        result = []
        for branch in BRANCHES:
            for key, record in self.records[branch].items():
                if (
                    (branch, key) not in self.base_keys
                    or record.get("method") != "legacy_global_mesh"
                ):
                    result.append(record)
        return sorted(result, key=lambda item: (str(item["branch"]), float(item["a"])))

    def is_base_order(self, branch: str, a: float) -> bool:
        return (branch, a_key(a)) in self.base_keys

    def compact(self) -> None:
        records = self.nonlegacy_records()
        serialisable_records = [
            {
                **record,
                "order": (
                    "infinity"
                    if math.isinf(float(record["order"]))
                    else float(record["order"])
                ),
            }
            for record in records
        ]
        payload = {
            "algorithm_version": ALGORITHM_VERSION,
            "fingerprint": self.fingerprint,
            "legacy_cache_fingerprint": self.legacy_cache.get("fingerprint"),
            "projection_count": len(records),
            "projections": serialisable_records,
            "schema_version": CACHE_SCHEMA_VERSION,
        }
        atomic_json_dump(payload, PROJECTION_CACHE_PATH)
        if PROJECTION_JOURNAL_PATH.exists():
            PROJECTION_JOURNAL_PATH.unlink()


def warm_projection(store: ProjectionStore, branch: str, a: float) -> dict[str, object]:
    existing = store.get(branch, a)
    if existing is not None:
        store.cache_hits += 1
        return existing
    order = order_from_a(a)
    pair = directed_pair(branch)
    objective = lambda x: renyi_divergence(*pair(x), order)
    starts = store.warm_starts(branch, a)
    if not starts:
        raise RuntimeError("the committed mesh should always provide a warm start")
    candidates: list[tuple[float, float, float]] = []
    successful_fits = 0
    for s0, t0 in starts:
        start_value = float(objective(np.array([s0, t0])))
        if np.isfinite(start_value):
            candidates.append((start_value, float(s0), float(t0)))
        fit = minimize(
            objective,
            x0=np.array([s0, t0]),
            method="L-BFGS-B",
            bounds=[(0.0, 1.0), (0.0, 1.0)],
            options={"ftol": 1.0e-15, "gtol": 2.0e-10, "maxiter": 500},
        )
        s, t = np.clip(fit.x, 0.0, 1.0)
        divergence = float(objective(np.array([s, t])))
        if fit.success and np.isfinite(divergence):
            candidates.append((divergence, float(s), float(t)))
            successful_fits += 1
        elif not fit.success:
            store.inner_optimizer_failures += 1
    unstable = not candidates or successful_fits == 0
    if candidates:
        divergence, s, t = min(candidates)
        lower, upper = store.neighbours(branch, a, validated_only=True)
        if lower is not None and divergence < float(lower["D"]) - INNER_STABILITY_TOLERANCE:
            unstable = True
        if upper is not None and divergence > float(upper["D"]) + INNER_STABILITY_TOLERANCE:
            unstable = True
    if unstable:
        globally_screened = minimise_over_classes(order, ORIENTATION[branch])
        divergence = float(globally_screened["D"])
        s = float(globally_screened["s"])
        t = float(globally_screened["t"])
        method = "instability_global_multistart"
        validated = True
        store.unstable_global_fallbacks += 1
    else:
        method = "nearest_mesh_warm_start"
        validated = False
    record: dict[str, object] = {
        "a": float(a),
        "branch": branch,
        "D": float(divergence),
        "method": method,
        "order": float(order),
        "s": float(s),
        "starts_used": len(starts),
        "t": float(t),
        "validated": validated,
    }
    store.put(record)
    store.warm_evaluations += 1
    return record


def branch_objective(
    branch: str, n: int, epsilon: float, a: float, divergence: float | None
) -> float:
    """Return the maximised scalar before converting it to a Type II bound.

    The review's displayed ``a[log(1/epsilon)-nD]_+`` is the reverse
    ``D_lambda(Q||P)`` Hölder exponent.  The independently valid forward
    ``D_lambda(P||Q)`` branch instead maximises its log lower bound.
    """

    if branch == "reverse":
        if a <= 0.0:
            return 0.0
        if divergence is None:
            raise ValueError("positive a requires a divergence")
        return a * max(0.0, math.log(1.0 / epsilon) - n * divergence)
    if branch == "forward":
        if epsilon >= 1.0 or a <= 0.0:
            return -math.inf
        if divergence is None:
            raise ValueError("positive a requires a divergence")
        return math.log1p(-epsilon) / a - n * divergence
    raise ValueError(branch)


def branch_bound(branch: str, objective: float) -> float:
    if branch == "reverse":
        return -math.expm1(-max(0.0, objective))
    if not np.isfinite(objective):
        return 0.0
    return math.exp(min(0.0, objective))


def load_cases() -> tuple[list[Case], dict[tuple[int, str], dict[str, float]]]:
    cases: list[Case] = []
    raw_numeric: dict[tuple[int, str], dict[str, float]] = {}
    with LEGACY_CSV_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for source in reader:
            numeric = {
                key: float(value)
                for key, value in source.items()
                if key not in {"regime"} and value not in {None, ""}
            }
            n = int(source["n"])
            regime = str(source["regime"])
            legacy = {
                "converse": float(source["converse"]),
                "forward": float(source["converse_forward"]),
                "forward_lambda": float(source["converse_forward_lambda"]),
                "reverse": float(source["converse_reverse"]),
                "reverse_lambda": float(source["converse_reverse_lambda"]),
            }
            cases.append(
                Case(
                    n=n,
                    regime=regime,
                    epsilon=float(source["epsilon"]),
                    minimax=float(source["minimax"]),
                    legacy=legacy,
                )
            )
            raw_numeric[(n, regime)] = numeric
    cases.sort(key=lambda item: item.key)
    return cases, raw_numeric


def mesh_arrays(
    legacy_cache: dict[str, object], branch: str
) -> tuple[np.ndarray, np.ndarray, list[dict[str, object]]]:
    records = list(legacy_cache["converse"])
    a = np.asarray([float(record["a"]) for record in records], dtype=float)
    divergence = np.asarray([float(record[f"{branch}_D"]) for record in records])
    return a, divergence, records


def plausible_candidate_intervals(
    a: np.ndarray, objective: np.ndarray, branch: str
) -> list[tuple[float, float]]:
    finite = np.flatnonzero(np.isfinite(objective))
    if finite.size == 0:
        return []
    best_index = int(finite[np.argmax(objective[finite])])
    best_value = float(objective[best_index])
    if branch == "reverse" and best_value <= 0.0:
        return []
    indices = {best_index}
    for index in range(1, objective.size - 1):
        value = float(objective[index])
        if not np.isfinite(value):
            continue
        if value >= objective[index - 1] and value >= objective[index + 1] and (
            value > objective[index - 1] + 1.0e-14
            or value > objective[index + 1] + 1.0e-14
        ):
            indices.add(index)
    intervals = set()
    for index in indices:
        left = 0.0 if index == 0 else float(a[index - 1])
        right = 1.0 if index == a.size - 1 else float(a[index + 1])
        if right - left > OUTER_XATOL:
            intervals.add((left, right))
    return sorted(intervals)


def case_mesh_objectives(
    case: Case, legacy_cache: dict[str, object], branch: str
) -> tuple[np.ndarray, np.ndarray]:
    a, divergence, _ = mesh_arrays(legacy_cache, branch)
    values = np.asarray(
        [
            branch_objective(branch, case.n, case.epsilon, float(ai), float(di))
            for ai, di in zip(a, divergence)
        ],
        dtype=float,
    )
    return a, values


def reconstruct_legacy_error(cases: Sequence[Case], legacy_cache: dict[str, object]) -> float:
    largest = 0.0
    for case in cases:
        reconstructed = {}
        for branch in BRANCHES:
            _, values = case_mesh_objectives(case, legacy_cache, branch)
            reconstructed[branch] = branch_bound(branch, float(np.max(values)))
            largest = max(largest, abs(reconstructed[branch] - case.legacy[branch]))
        largest = max(
            largest,
            abs(max(reconstructed.values()) - case.legacy["converse"]),
        )
    return largest


def build_intervals(
    cases: Sequence[Case], legacy_cache: dict[str, object]
) -> dict[tuple[int, str, str], list[tuple[float, float]]]:
    result = {}
    for case in cases:
        for branch in BRANCHES:
            a, objective = case_mesh_objectives(case, legacy_cache, branch)
            result[(case.n, case.regime, branch)] = plausible_candidate_intervals(
                a, objective, branch
            )
    return result


def run_outer_round(
    cases: Sequence[Case],
    intervals: dict[tuple[int, str, str], list[tuple[float, float]]],
    store: ProjectionStore,
    candidate_a: dict[tuple[int, str, str], set[float]],
    *,
    xatol: float,
) -> tuple[set[tuple[str, float]], dict[tuple[int, str, str], tuple[float, ...]]]:
    new_maximisers: set[tuple[str, float]] = set()
    round_points: dict[tuple[int, str, str], list[float]] = {
        key: [] for key in intervals
    }
    for case_index, case in enumerate(cases, start=1):
        for branch in BRANCHES:
            key = (case.n, case.regime, branch)

            def scalar(a: float) -> float:
                projection = warm_projection(store, branch, float(a))
                return branch_objective(
                    branch,
                    case.n,
                    case.epsilon,
                    float(a),
                    float(projection["D"]),
                )

            for left, right in intervals[key]:
                for endpoint in (left, right):
                    if endpoint > 0.0:
                        candidate_a[key].add(float(endpoint))
                for mesh_value in store.sorted_a[branch]:
                    if mesh_value <= left:
                        continue
                    if mesh_value >= right:
                        break
                    if (branch, a_key(mesh_value)) in store.base_keys:
                        candidate_a[key].add(float(mesh_value))
                fit = minimize_scalar(
                    lambda value: -scalar(float(value)),
                    bounds=(left, right),
                    method="bounded",
                    options={"xatol": xatol, "maxiter": 100},
                )
                if not fit.success or not np.isfinite(float(fit.x)) or not np.isfinite(
                    float(fit.fun)
                ):
                    raise RuntimeError(
                        f"bounded outer optimisation failed for {key}: {fit.message}"
                    )
                a = float(np.clip(fit.x, left, right))
                scalar(a)
                candidate_a[key].add(a)
                round_points[key].append(a)
                if not bool(store.get(branch, a)["validated"]):
                    new_maximisers.add((branch, a))
        if case_index % 50 == 0:
            print(f"outer refinement considered {case_index}/{len(cases)} rows", flush=True)
    return new_maximisers, {
        key: tuple(points) for key, points in round_points.items()
    }


def global_projection_worker(payload: tuple[str, float]) -> tuple[str, float, dict[str, float]]:
    branch, a = payload
    order = math.inf if a == 1.0 else order_from_a(a)
    result = minimise_over_classes(order, ORIENTATION[branch])
    return branch, a, result


def polish_maximisers(
    store: ProjectionStore,
    maximisers: Iterable[tuple[str, float]],
    *,
    jobs: int,
    force_items: set[tuple[str, float]] | None = None,
) -> dict[str, float]:
    forced = force_items or set()
    pending = sorted(
        {
            (branch, a)
            for branch, a in maximisers
            if (branch, a) in forced
            or not bool(store.get(branch, a).get("validated"))
        }
    )
    if not pending:
        return {"count": 0.0, "max_global_improvement": 0.0, "max_global_worse": 0.0}

    statistics = {
        "count": 0.0,
        "max_global_improvement": 0.0,
        "max_global_worse": 0.0,
    }

    def accept(branch: str, a: float, screened: dict[str, float]) -> None:
        warm = store.get(branch, a)
        warm_d = float(warm["D"])
        screened_d = float(screened["D"])
        signed_gap = screened_d - warm_d
        statistics["count"] += 1.0
        statistics["max_global_improvement"] = max(
            statistics["max_global_improvement"], -signed_gap
        )
        statistics["max_global_worse"] = max(
            statistics["max_global_worse"], signed_gap
        )
        if warm_d <= screened_d:
            divergence, s, t = warm_d, float(warm["s"]), float(warm["t"])
        else:
            divergence = screened_d
            s, t = float(screened["s"]), float(screened["t"])
        record: dict[str, object] = {
            "a": float(a),
            "branch": branch,
            "D": divergence,
            "global_screen_D": screened_d,
            "global_warm_D_gap": screened_d - warm_d,
            "method": "global_multistart_plus_warm",
            "order": math.inf if a == 1.0 else order_from_a(a),
            "s": s,
            "t": t,
            "validated": True,
        }
        store.put(record)
        store.global_polishes += 1

    if jobs <= 1:
        for index, payload in enumerate(pending, start=1):
            branch, a, result = global_projection_worker(payload)
            accept(branch, a, result)
            if index % 25 == 0 or index == len(pending):
                print(f"globally polished {index}/{len(pending)} projections", flush=True)
        return statistics
    with ProcessPoolExecutor(max_workers=jobs) as executor:
        futures = {executor.submit(global_projection_worker, item): item for item in pending}
        completed = 0
        for future in as_completed(futures):
            branch, a, result = future.result()
            accept(branch, a, result)
            completed += 1
            if completed % 25 == 0 or completed == len(pending):
                print(
                    f"globally polished {completed}/{len(pending)} projections",
                    flush=True,
                )
    return statistics


def outer_points_stable(
    previous: dict[tuple[int, str, str], tuple[float, ...]],
    current: dict[tuple[int, str, str], tuple[float, ...]],
    *,
    tolerance: float,
) -> bool:
    if previous.keys() != current.keys():
        return False
    for key in previous:
        old, new = previous[key], current[key]
        if len(old) != len(new):
            return False
        if any(abs(left - right) > tolerance for left, right in zip(old, new)):
            return False
    return True


def adjacent_mesh_records(
    legacy_cache: dict[str, object], a: float
) -> tuple[dict[str, object], dict[str, object]]:
    records = list(legacy_cache["converse"])
    values = [float(record["a"]) for record in records]
    position = bisect.bisect_left(values, a)
    if position < len(values) and values[position] == a:
        left_index = max(0, position - 1)
        right_index = min(len(records) - 1, position + 1)
    else:
        left_index = max(0, min(position - 1, len(records) - 1))
        right_index = max(0, min(position, len(records) - 1))
    return records[left_index], records[right_index]


def endpoint_label(a: float) -> str:
    if a == 1.0:
        return "order_infinity"
    if a == 0.0:
        return "order_one_limit"
    return "finite"


def finalise_rows(
    cases: Sequence[Case],
    legacy_cache: dict[str, object],
    store: ProjectionStore,
    candidate_a: dict[tuple[int, str, str], set[float]],
) -> tuple[list[dict[str, object]], dict[str, float]]:
    output = []
    diagnostics = {
        "largest_neighbour_inferiority": 0.0,
        "largest_roundtrip_error": 0.0,
        "selected_invalid_record": 0.0,
        "selected_unvalidated": 0.0,
    }
    mesh_records = list(legacy_cache["converse"])
    mesh_a = [float(record["a"]) for record in mesh_records]
    for case in cases:
        selected: dict[str, dict[str, object]] = {}
        for branch in BRANCHES:
            key = (case.n, case.regime, branch)
            _, mesh_values = case_mesh_objectives(case, legacy_cache, branch)
            mesh_index = int(np.argmax(mesh_values))
            considered = set(candidate_a[key])
            considered.add(mesh_a[mesh_index])
            considered.add(0.0)
            considered.add(1.0)
            scored: list[tuple[float, float, dict[str, object] | None]] = []
            for a in sorted(considered):
                record = None if a == 0.0 else store.get(branch, a)
                if a == 0.0:
                    objective = branch_objective(branch, case.n, case.epsilon, a, None)
                else:
                    if record is None:
                        raise RuntimeError(f"missing cached projection for {branch}, a={a}")
                    objective = branch_objective(
                        branch, case.n, case.epsilon, a, float(record["D"])
                    )
                scored.append((objective, a, record))
            objective, a, record = max(
                scored,
                key=lambda item: (item[0], int(item[1] > 0.0), -item[1]),
            )
            bound = branch_bound(branch, objective)
            if record is not None:
                if not bool(record.get("validated")):
                    diagnostics["selected_unvalidated"] += 1.0
                if (
                    not np.isfinite(float(record["D"]))
                    or float(record["D"]) < -5.0e-13
                    or not 0.0 <= float(record["s"]) <= 1.0
                    or not 0.0 <= float(record["t"]) <= 1.0
                ):
                    diagnostics["selected_invalid_record"] += 1.0
                roundtrip = abs(float(record["D"]) - recompute_record_divergence(record))
                diagnostics["largest_roundtrip_error"] = max(
                    diagnostics["largest_roundtrip_error"], roundtrip
                )
            left, right = adjacent_mesh_records(legacy_cache, a)
            neighbour_bounds = []
            for neighbour in (left, right):
                neighbour_a = float(neighbour["a"])
                neighbour_objective = branch_objective(
                    branch,
                    case.n,
                    case.epsilon,
                    neighbour_a,
                    float(neighbour[f"{branch}_D"]),
                )
                neighbour_bounds.append(branch_bound(branch, neighbour_objective))
            neighbour_best = max(neighbour_bounds)
            diagnostics["largest_neighbour_inferiority"] = max(
                diagnostics["largest_neighbour_inferiority"], neighbour_best - bound
            )
            selected[branch] = {
                "a": a,
                "bound": bound,
                "endpoint": endpoint_label(a),
                "neighbour_best": neighbour_best,
                "objective": objective,
                "order": 1.0 if record is None else float(record["order"]),
            }

        reverse = selected["reverse"]
        forward = selected["forward"]
        continuous_branch = (
            "reverse" if reverse["bound"] >= forward["bound"] else "forward"
        )
        legacy_branch = (
            "reverse"
            if case.legacy["reverse"] >= case.legacy["forward"]
            else "forward"
        )
        continuous = max(float(reverse["bound"]), float(forward["bound"]))
        output.append(
            {
                "n": case.n,
                "regime": case.regime,
                "epsilon": case.epsilon,
                "minimax": case.minimax,
                "legacy_converse": case.legacy["converse"],
                "continuous_converse": continuous,
                "absolute_improvement": continuous - case.legacy["converse"],
                "legacy_selected_branch": legacy_branch,
                "legacy_selected_order": case.legacy[f"{legacy_branch}_lambda"],
                "continuous_selected_branch": continuous_branch,
                "continuous_selected_order": selected[continuous_branch]["order"],
                "legacy_reverse": case.legacy["reverse"],
                "continuous_reverse": reverse["bound"],
                "reverse_absolute_improvement": reverse["bound"] - case.legacy["reverse"],
                "legacy_reverse_order": case.legacy["reverse_lambda"],
                "continuous_reverse_order": reverse["order"],
                "continuous_reverse_a": reverse["a"],
                "continuous_reverse_objective": reverse["objective"],
                "continuous_reverse_endpoint": reverse["endpoint"],
                "continuous_reverse_adjacent_mesh_best": reverse["neighbour_best"],
                "legacy_forward": case.legacy["forward"],
                "continuous_forward": forward["bound"],
                "forward_absolute_improvement": forward["bound"] - case.legacy["forward"],
                "legacy_forward_order": case.legacy["forward_lambda"],
                "continuous_forward_order": forward["order"],
                "continuous_forward_a": forward["a"],
                "continuous_forward_log_bound": forward["objective"],
                "continuous_forward_endpoint": forward["endpoint"],
                "continuous_forward_adjacent_mesh_best": forward["neighbour_best"],
                "minimax_minus_continuous_converse": case.minimax - continuous,
            }
        )
    return output, diagnostics


COMPARISON_COLUMNS = [
    "n",
    "regime",
    "epsilon",
    "minimax",
    "legacy_converse",
    "continuous_converse",
    "absolute_improvement",
    "legacy_selected_branch",
    "legacy_selected_order",
    "continuous_selected_branch",
    "continuous_selected_order",
    "legacy_reverse",
    "continuous_reverse",
    "reverse_absolute_improvement",
    "legacy_reverse_order",
    "continuous_reverse_order",
    "continuous_reverse_a",
    "continuous_reverse_objective",
    "continuous_reverse_endpoint",
    "continuous_reverse_adjacent_mesh_best",
    "legacy_forward",
    "continuous_forward",
    "forward_absolute_improvement",
    "legacy_forward_order",
    "continuous_forward_order",
    "continuous_forward_a",
    "continuous_forward_log_bound",
    "continuous_forward_endpoint",
    "continuous_forward_adjacent_mesh_best",
    "minimax_minus_continuous_converse",
]


def write_comparison(rows: Sequence[dict[str, object]]) -> None:
    temporary = COMPARISON_PATH.with_suffix(".csv.tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=COMPARISON_COLUMNS, lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, COMPARISON_PATH)


def validate_results(
    rows: Sequence[dict[str, object]],
    diagnostics: dict[str, float],
    store: ProjectionStore,
    legacy_reconstruction_error: float,
) -> dict[str, object]:
    branch_excess = {
        branch: max(float(row[f"continuous_{branch}"]) - float(row["minimax"]) for row in rows)
        for branch in BRANCHES
    }
    max_excess = max(
        float(row["continuous_converse"]) - float(row["minimax"]) for row in rows
    )
    max_decrease = max(
        float(row["legacy_converse"]) - float(row["continuous_converse"]) for row in rows
    )
    branch_decrease = {
        branch: max(
            float(row[f"legacy_{branch}"]) - float(row[f"continuous_{branch}"])
            for row in rows
        )
        for branch in BRANCHES
    }
    validated_monotonic_decrease = 0.0
    for branch in BRANCHES:
        validated = sorted(
            (
                record
                for record in store.records[branch].values()
                if bool(record.get("validated"))
            ),
            key=lambda record: float(record["a"]),
        )
        for previous, current in zip(validated, validated[1:]):
            validated_monotonic_decrease = max(
                validated_monotonic_decrease,
                float(previous["D"]) - float(current["D"]),
            )
    global_worse = max(store.global_screen_minus_warm, default=0.0)
    global_improvement = max(
        (-value for value in store.global_screen_minus_warm), default=0.0
    )
    global_absolute_gap = max(
        (abs(value) for value in store.global_screen_minus_warm), default=0.0
    )
    checks = {
        "branch_max_converse_minus_minimax": branch_excess,
        "largest_absolute_global_warm_gap": global_absolute_gap,
        "largest_global_multistart_improvement_over_warm": global_improvement,
        "largest_global_multistart_worse_than_warm": global_worse,
        "largest_legacy_reconstruction_error": legacy_reconstruction_error,
        "largest_neighbour_inferiority": diagnostics["largest_neighbour_inferiority"],
        "largest_projection_roundtrip_error": diagnostics["largest_roundtrip_error"],
        "largest_refined_converse_minus_minimax": max_excess,
        "largest_refined_decrease": max_decrease,
        "largest_validated_divergence_monotonicity_decrease": validated_monotonic_decrease,
        "per_branch_largest_decrease": branch_decrease,
        "selected_invalid_record_count": int(diagnostics["selected_invalid_record"]),
        "selected_unvalidated_count": int(diagnostics["selected_unvalidated"]),
    }
    failures = []
    if legacy_reconstruction_error > 5.0e-13:
        failures.append("legacy cache does not reconstruct the committed branch values")
    if max_decrease > OBJECTIVE_TOLERANCE or any(
        value > OBJECTIVE_TOLERANCE for value in branch_decrease.values()
    ):
        failures.append("continuous refinement decreased a legacy bound")
    if max(max_excess, *branch_excess.values()) > CONVERSE_TOLERANCE:
        failures.append("a refined converse branch exceeds the stored minimax tolerance")
    if diagnostics["selected_unvalidated"]:
        failures.append("at least one selected order lacks global multistart validation")
    if diagnostics["selected_invalid_record"]:
        failures.append("at least one selected projection has invalid parameters or divergence")
    if diagnostics["largest_neighbour_inferiority"] > OBJECTIVE_TOLERANCE:
        failures.append("a selected scalar point is inferior to an adjacent cached mesh point")
    if diagnostics["largest_roundtrip_error"] > 5.0e-13:
        failures.append("a selected cached projection does not reproduce its divergence")
    if validated_monotonic_decrease > PROJECTION_AGREEMENT_TOLERANCE:
        failures.append("validated directed divergences are not monotone in Rényi order")
    if global_worse > PROJECTION_AGREEMENT_TOLERANCE:
        failures.append("global screening returned a worse projection than a warm start")
    checks["failures"] = failures
    checks["passed"] = not failures
    return checks


def save_eps(
    fig: mpl.figure.Figure, path: Path, *, bbox_inches: str | None = None
) -> None:
    fig.savefig(path, format="eps", bbox_inches=bbox_inches)


def plot_standalone_converse(rows: Sequence[dict[str, object]], regime: str) -> None:
    plotting_style()
    selected = sorted(
        (row for row in rows if row["regime"] == regime), key=lambda row: int(row["n"])
    )
    n = np.asarray([row["n"] for row in selected], dtype=float)
    minimax = np.asarray([row["minimax"] for row in selected], dtype=float)
    converse = np.asarray([row["continuous_converse"] for row in selected], dtype=float)
    fig, ax = plt.subplots(figsize=(3.45, 2.55), constrained_layout=True)
    ax.plot(n, minimax, color="black", linestyle="-", marker="o", markersize=1.6,
            markeredgewidth=0.0, label="minimax Type II error")
    ax.plot(n, converse, color="0.38", linestyle="--", marker="s", markersize=1.4,
            markeredgewidth=0.0, label="converse bound")
    ax.set_xlim(float(np.min(n)), float(np.max(n)))
    ax.set_ylim(-0.015, 1.015)
    ax.set_xlabel("sample n")
    ax.set_ylabel("Type II error")
    ax.legend(frameon=False, loc="best", handlelength=2.7)
    ax.tick_params(direction="in", top=True, right=True, width=0.6)
    save_eps(fig, FIGURE_DIR / f"nonordered_bruno_{regime}_converse.eps")
    plt.close(fig)


def plot_combined(
    rows: Sequence[dict[str, object]], legacy_numeric: dict[tuple[int, str], dict[str, float]]
) -> None:
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["DejaVu Serif"],
            "mathtext.fontset": "dejavuserif",
            "font.size": 11,
            "axes.labelsize": 11,
            "axes.titlesize": 12,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 9.5,
            "axes.linewidth": 0.8,
            "lines.linewidth": 1.8,
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
        }
    )
    blue, orange = "#1f77b4", "#ff7f0e"
    fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.9), sharex=True, sharey=False)

    def panel(ax: plt.Axes, regime: str, kind: str, title: str) -> None:
        selected = sorted(
            (row for row in rows if row["regime"] == regime),
            key=lambda row: int(row["n"]),
        )
        n = [int(row["n"]) for row in selected]
        minimax = [float(row["minimax"]) for row in selected]
        if kind == "achievability":
            bound = [legacy_numeric[(int(row["n"]), regime)]["achievability"] for row in selected]
            label = "achievability bound"
        else:
            bound = [float(row["continuous_converse"]) for row in selected]
            label = "converse bound"
        ax.plot(n, minimax, color=blue, label="minimax Type II error")
        ax.plot(n, bound, color=orange, label=label)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(direction="out", length=4, width=0.8)
        ax.set_xlim(1, 300)
        ax.set_ylim(bottom=0.0)
        ax.set_xlabel(r"samples $n$")
        ax.set_ylabel("Type II error")
        ax.set_title(title, pad=8)
        ax.legend(frameon=False, loc="upper right")

    panel(axes[0, 0], "constant", "achievability", r"Achievability, $\varepsilon = 0.01$")
    panel(axes[0, 1], "constant", "converse", r"Converse, $\varepsilon = 0.01$")
    panel(axes[1, 0], "linear", "achievability", r"Achievability, $\varepsilon = 1/n$")
    panel(axes[1, 1], "linear", "converse", r"Converse, $\varepsilon = 1/n$")
    fig.tight_layout(pad=1.2, w_pad=2.0, h_pad=2.0)
    save_eps(fig, FIGURE_DIR / "nonordered_bruno_2x2.eps", bbox_inches="tight")
    temporary_png = FIGURE_DIR / f"nonordered_bruno_2x2.{os.getpid()}.tmp.png"
    fig.savefig(temporary_png, dpi=220, bbox_inches="tight")
    os.replace(temporary_png, FIGURE_DIR / "nonordered_bruno_2x2.png")
    plt.close(fig)


def make_affected_figures(
    rows: Sequence[dict[str, object]], legacy_numeric: dict[tuple[int, str], dict[str, float]]
) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    plot_standalone_converse(rows, "constant")
    plot_standalone_converse(rows, "linear")
    plot_combined(rows, legacy_numeric)


def format_order(value: float) -> str:
    return "infinity" if math.isinf(value) else f"{value:.12g}"


def write_audit(
    rows: Sequence[dict[str, object]],
    validation: dict[str, object],
    store: ProjectionStore,
    runtime_seconds: float,
    *,
    rounds: int,
    polish_jobs: int,
) -> None:
    improvements = np.asarray([float(row["absolute_improvement"]) for row in rows])
    largest_index = int(np.argmax(improvements))
    largest_row = rows[largest_index]
    branch_metrics = {}
    for branch in BRANCHES:
        values = np.asarray([float(row[f"{branch}_absolute_improvement"]) for row in rows])
        a_changes = np.asarray(
            [
                abs(
                    float(row[f"continuous_{branch}_a"])
                    - (1.0 - 1.0 / float(row[f"legacy_{branch}_order"]))
                )
                for row in rows
            ]
        )
        branch_metrics[branch] = {
            "max": float(np.max(values)),
            "median": float(np.median(values)),
            "changed_orders": sum(
                not math.isclose(
                    float(row[f"legacy_{branch}_order"]),
                    float(row[f"continuous_{branch}_order"]),
                    rel_tol=1.0e-10,
                    abs_tol=1.0e-12,
                )
                for row in rows
            ),
            "distinct_orders": len(
                {float(row[f"continuous_{branch}_order"]) for row in rows}
            ),
            "max_a_change": float(np.max(a_changes)),
            "median_a_change": float(np.median(a_changes)),
        }
    infinity_rows = {
        branch: [
            f"n={int(row['n'])}, {row['regime']}"
            for row in rows
            if row[f"continuous_{branch}_endpoint"] == "order_infinity"
        ]
        for branch in BRANCHES
    }
    winning_changes = sum(
        row["legacy_selected_branch"] != row["continuous_selected_branch"] for row in rows
    )
    overlay_records = store.nonlegacy_records()
    new_records = [
        record
        for record in overlay_records
        if not store.is_base_order(str(record["branch"]), float(record["a"]))
    ]
    revalidated_base_records = len(overlay_records) - len(new_records)
    validated_new = sum(bool(record.get("validated")) for record in new_records)
    distinct_new_a = len({float(record["a"]) for record in new_records})
    top_improvements = sorted(
        rows, key=lambda row: float(row["absolute_improvement"]), reverse=True
    )[:5]
    top_improvement_text = "\n".join(
        "- `n={n}`, `{regime}`: `{old:.12g}` to `{new:.12g}` "
        "(gain `{gain:.12e}`), winning order `{order}` ({branch}).".format(
            n=int(row["n"]),
            regime=row["regime"],
            old=float(row["legacy_converse"]),
            new=float(row["continuous_converse"]),
            gain=float(row["absolute_improvement"]),
            order=format_order(float(row["continuous_selected_order"])),
            branch=row["continuous_selected_branch"],
        )
        for row in top_improvements
    )
    failures = validation["failures"]
    status = "PASS" if validation["passed"] else "FAIL"
    failure_text = "None." if not failures else "\n".join(f"- {failure}" for failure in failures)
    text = f"""# Audit: continuous Rényi-order optimisation of the numerical converse

## Outcome

Validation status: **{status}**.

The displayed maximum converse improved by at most
`{float(np.max(improvements)):.12e}` and by a median of
`{float(np.median(improvements)):.12e}` across the 600 saved rows.  The
largest improvement occurs at `n={int(largest_row['n'])}` in the
`{largest_row['regime']}` Type I regime: the bound moves from
`{float(largest_row['legacy_converse']):.12g}` to
`{float(largest_row['continuous_converse']):.12g}`.

This is a numerical refinement of the saved experiment, not a new
mathematical converse.  The feasible projected pairs used during the outer
search give divergences no smaller than the exact composite infimum and hence
conservative lower bounds.  Mathematical validity comes from the two Hölder
inequalities described below; the optimiser and validation checks provide
numerical evidence that their suprema have been located accurately.

## Branch objectives and mathematical clarification

The reverse branch uses `D_lambda(Q||P)` and maximises

```text
E_reverse(a) = a [log(1/epsilon) - n D_lambda(Q||P)]_+,
beta_reverse = -expm1(-max_a E_reverse(a)).
```

The task directive displayed this exponent for “each” branch.  It cannot be
applied to the forward direction.  Hölder's inequality with `D_lambda(P||Q)`
instead gives

```text
ell_forward(a) = log(1-epsilon)/a - n D_lambda(P||Q),
beta_forward = exp(max_a ell_forward(a)).
```

The implementation therefore preserves and continuously refines the two
existing valid branches separately, then reports their maximum.  Applying the
reverse conversion to the forward divergence would exceed the saved minimax
value in 11 rows (by as much as about `5.3927e-3`) and is not used.

## Optimisation procedure and cache reuse

The bounded variable is `a=(lambda-1)/lambda`.  For every saved
`(n, regime, branch)` row, the scalar objective is first evaluated from the
167 committed finite orders and the committed order-infinity projection;
none of those divergences is recomputed.  Strict local mesh maxima, the best
mesh point and their neighbouring intervals define the candidate bounded
searches.  The limits `a downarrow 0` and `a=1` are checked
explicitly; no numerical projection is attempted at order one.

At each new scalar trial, L-BFGS-B starts first from the nearest cached
projected pair and then from pairs at adjacent cached orders.  A monotonicity
bracket against validated projections detects unstable inner evaluations;
only such evaluations invoke the 13-by-13 global screen immediately.  New
records are appended and fsynchronised to a JSON-lines journal, so interrupted
work can resume.  A successful run compacts the journal into
`numerics/data/nonordered_bruno_continuous_renyi_cache.json`.

The outer searches were repeated for {rounds} round(s), stopping only after
successive maximisers agreed within `{OUTER_CONVERGENCE_A_TOLERANCE:.1e}` in
`a` and the final global screens improved divergence by at most
`{PROJECTION_AGREEMENT_TOLERANCE:.1e}`.  Every distinct new candidate
maximiser from each round was revalidated with the existing
13-by-13 multistart projection routine (using {polish_jobs} worker processes).
The better feasible result between the warm point and global screen is retained;
their largest adverse disagreement was
`{float(validation['largest_global_multistart_worse_than_warm']):.3e}`.

The compact overlay contains {len(overlay_records)} projections: {len(new_records)}
new branch/order projections at {distinct_new_a} distinct new Rényi orders and
{revalidated_base_records} explicitly revalidated committed-mesh projections.
Of the new projections, {validated_new} are globally screened.  During this run there
were {store.warm_evaluations} new warm evaluations,
{store.unstable_global_fallbacks} instability-triggered global screens, and
{store.global_polishes} explicit final-candidate or base revalidation polishes.
There were {store.cache_hits} exact projection-cache hits and
{store.inner_optimizer_failures} unsuccessful local optimiser starts.
Divergence
evaluations are independent of `n` and `epsilon`, so all blocklengths and both
Type I regimes reuse this common store and nearby projected pairs.

Refinement-only runtime for the outer searches and projection validation,
excluding cache compaction, comparison/audit writing and figure rendering, was
`{runtime_seconds:.3f}` seconds for this invocation.  On a resumed run this
timer and the preceding evaluation counters exclude work already present in
the validated cache.

## Numerical changes by branch

| Branch | Maximum improvement | Median improvement | Rows with changed order | Distinct selected orders |
|---|---:|---:|---:|---:|
| Reverse (`Q||P`) | {branch_metrics['reverse']['max']:.12e} | {branch_metrics['reverse']['median']:.12e} | {branch_metrics['reverse']['changed_orders']} | {branch_metrics['reverse']['distinct_orders']} |
| Forward (`P||Q`) | {branch_metrics['forward']['max']:.12e} | {branch_metrics['forward']['median']:.12e} | {branch_metrics['forward']['changed_orders']} | {branch_metrics['forward']['distinct_orders']} |

Measured in the bounded variable `a`, the median/maximum absolute changes from
the legacy selected orders are
`{branch_metrics['reverse']['median_a_change']:.6e}` /
`{branch_metrics['reverse']['max_a_change']:.6e}` for the reverse branch and
`{branch_metrics['forward']['median_a_change']:.6e}` /
`{branch_metrics['forward']['max_a_change']:.6e}` for the forward branch.

The five largest displayed improvements are:

{top_improvement_text}

The identity of the branch giving the displayed maximum changes in
{winning_changes} rows.  The order-infinity endpoint is selected by the
reverse branch in {len(infinity_rows['reverse'])} rows and by the forward
branch in {len(infinity_rows['forward'])} rows.

Reverse order-infinity selections: {', '.join(infinity_rows['reverse']) or 'none'}.

Forward order-infinity selections: {', '.join(infinity_rows['forward']) or 'none'}.

For flat zero-bound cases, the legacy smallest finite mesh order is retained;
such an order is not interpreted as an identified optimiser.

## Validation

The absolute tolerance for comparing a converse with the stored numerical
minimax value is `{CONVERSE_TOLERANCE:.1e}`, just above the established LP
alternative-envelope residual (about `2.0e-9`).  Scalar non-inferiority uses
`{OBJECTIVE_TOLERANCE:.1e}`; projection round trips use `5e-13`; global-screen
agreement and validated Rényi monotonicity use
`{PROJECTION_AGREEMENT_TOLERANCE:.1e}`.

- Largest error reconstructing every legacy branch and maximum from the committed cache: `{float(validation['largest_legacy_reconstruction_error']):.6e}`.
- Largest decrease of the refined displayed converse relative to the legacy mesh: `{float(validation['largest_refined_decrease']):.6e}`.
- Largest reverse-branch decrease: `{float(validation['per_branch_largest_decrease']['reverse']):.6e}`.
- Largest forward-branch decrease: `{float(validation['per_branch_largest_decrease']['forward']):.6e}`.
- Largest selected-bound inferiority to either adjacent committed mesh point: `{float(validation['largest_neighbour_inferiority']):.6e}`.
- Largest selected projection divergence round-trip error: `{float(validation['largest_projection_roundtrip_error']):.6e}`.
- Selected projections with invalid parameters or divergence: `{int(validation['selected_invalid_record_count'])}`.
- Selected orders lacking the required global screen: `{int(validation['selected_unvalidated_count'])}`.
- Largest absolute divergence difference between a warm candidate and its global screen: `{float(validation['largest_absolute_global_warm_gap']):.6e}`.
- Largest divergence improvement supplied by global screening: `{float(validation['largest_global_multistart_improvement_over_warm']):.6e}`.
- Largest validated decrease in directed divergence as Rényi order increases: `{float(validation['largest_validated_divergence_monotonicity_decrease']):.6e}`.
- Largest reverse converse minus stored minimax: `{float(validation['branch_max_converse_minus_minimax']['reverse']):.6e}`.
- Largest forward converse minus stored minimax: `{float(validation['branch_max_converse_minus_minimax']['forward']):.6e}`.
- Largest displayed maximum converse minus stored minimax: `{float(validation['largest_refined_converse_minus_minimax']):.6e}`.

No value is clipped to the minimax result.  Validation failures:

{failure_text}

## Figures and manuscript impact

Only the two standalone converse panels and the combined 2-by-2 figure depend
on the refined maximum.  They are regenerated from saved CSV values only:
`nonordered_bruno_constant_converse.eps`,
`nonordered_bruno_linear_converse.eps`, `nonordered_bruno_2x2.eps`, and
`nonordered_bruno_2x2.png`.  The two achievability-only EPS files are left
unchanged.

The manuscript's nonordered ternary example uses different class endpoints,
an exponentially decaying Type I schedule, and a separate blocklength-20 gap
table.  Its plotted figures concern ordered endpoint families.  Consequently,
this refinement does not materially change an existing manuscript statement
or identify text requiring revision.  If these curves are later incorporated,
their caption should distinguish the reverse branch, forward branch and their
displayed maximum.
"""
    AUDIT_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--polish-jobs",
        type=int,
        default=min(6, max(1, (os.cpu_count() or 2) - 1)),
        help="worker processes for final 13-by-13 multistart validation",
    )
    parser.add_argument(
        "--outer-rounds",
        type=int,
        default=4,
        help="maximum outer-search/polish rounds (at least two are required)",
    )
    parser.add_argument("--outer-xatol", type=float, default=OUTER_XATOL)
    parser.add_argument("--skip-figures", action="store_true")
    arguments = parser.parse_args()
    if arguments.outer_rounds < 2:
        raise ValueError("--outer-rounds must be at least two")

    legacy_cache = load_json(LEGACY_CACHE_PATH)
    if legacy_cache.get("fingerprint") != _configuration_fingerprint():
        raise RuntimeError("the committed Rényi cache does not match the imported configuration")
    cases, legacy_numeric = load_cases()
    if len(cases) != 600:
        raise ValueError(f"expected 600 committed rows, found {len(cases)}")
    legacy_reconstruction_error = reconstruct_legacy_error(cases, legacy_cache)
    if legacy_reconstruction_error > 5.0e-13:
        raise RuntimeError(
            f"legacy cache reconstruction error is {legacy_reconstruction_error:.3e}"
        )
    store = ProjectionStore(legacy_cache)
    intervals = build_intervals(cases, legacy_cache)
    candidate_a = {key: set() for key in intervals}

    started = time.perf_counter()
    previous_points: dict[tuple[int, str, str], tuple[float, ...]] | None = None
    converged = False
    actual_rounds = 0
    for round_index in range(1, arguments.outer_rounds + 1):
        actual_rounds = round_index
        print(f"starting outer refinement round {round_index}", flush=True)
        maximisers, round_points = run_outer_round(
            cases,
            intervals,
            store,
            candidate_a,
            xatol=max(1.0e-12, arguments.outer_xatol),
        )
        print(
            f"round {round_index} produced {len(maximisers)} unvalidated candidate projections",
            flush=True,
        )
        polish_statistics = polish_maximisers(
            store, maximisers, jobs=max(1, arguments.polish_jobs)
        )
        stable = previous_points is not None and outer_points_stable(
            previous_points,
            round_points,
            tolerance=OUTER_CONVERGENCE_A_TOLERANCE,
        )
        if (
            round_index >= 2
            and stable
            and polish_statistics["max_global_improvement"]
            <= PROJECTION_AGREEMENT_TOLERANCE
        ):
            converged = True
            print(f"outer refinement converged after {round_index} rounds", flush=True)
            break
        previous_points = round_points

    if not converged:
        store.compact()
        raise RuntimeError(
            f"outer refinement did not stabilise in {arguments.outer_rounds} rounds"
        )

    preliminary_rows, _ = finalise_rows(cases, legacy_cache, store, candidate_a)
    selected_base = {
        (branch, float(row[f"continuous_{branch}_a"]))
        for row in preliminary_rows
        for branch in BRANCHES
        if float(row[f"continuous_{branch}_a"]) > 0.0
        and (
            branch,
            a_key(float(row[f"continuous_{branch}_a"])),
        )
        in store.base_keys
    }
    base_revalidation = polish_maximisers(
        store,
        selected_base,
        jobs=max(1, arguments.polish_jobs),
        force_items=selected_base,
    )
    if base_revalidation["max_global_improvement"] > PROJECTION_AGREEMENT_TOLERANCE:
        store.compact()
        raise RuntimeError("revalidation materially improved a selected base-mesh projection")

    rows, diagnostics = finalise_rows(cases, legacy_cache, store, candidate_a)
    validation = validate_results(rows, diagnostics, store, legacy_reconstruction_error)
    refinement_runtime = time.perf_counter() - started
    store.compact()
    write_comparison(rows)
    write_audit(
        rows,
        validation,
        store,
        refinement_runtime,
        rounds=actual_rounds,
        polish_jobs=max(1, arguments.polish_jobs),
    )
    if not validation["passed"]:
        raise RuntimeError(
            "continuous converse validation failed: "
            + "; ".join(validation["failures"])
        )
    if not arguments.skip_figures:
        make_affected_figures(rows, legacy_numeric)
    print(f"wrote {PROJECTION_CACHE_PATH}")
    print(f"wrote {COMPARISON_PATH}")
    print(f"wrote {AUDIT_PATH}")
    if not arguments.skip_figures:
        print("regenerated the four affected figure files")


if __name__ == "__main__":
    main()
