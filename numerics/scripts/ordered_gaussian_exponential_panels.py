#!/usr/bin/env python3
"""Reproduce the ordered Gaussian and exponential numerical figures.

This script generates the two publication figures used in the numerical
illustration:

    Fig_01.eps  Gaussian family
    Fig_02.eps  Exponential family

Each figure is a 3 x 2 panel layout. The left column shows the calibrated
joint-Renyi projected test against the exact minimax Type II error, and the
right column shows the Renyi and Fano-style converses. Rows correspond to

    1. epsilon_n = 0.01,
    2. epsilon_n = 1/n,
    3. epsilon_n = exp(-nr), with r = 0.75 r_c on the left and
       r = 1.90 r_c on the right.

The displayed sample range begins at n=10. For the separated one-parameter
families below, the joint Renyi projection is the least-favourable endpoint
pair at every sample size, so the calibrated projected test coincides with
the exact Neyman-Pearson test for that pair.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import gamma, norm


ROOT = Path(__file__).resolve().parent
N_MIN = 10
N_MAX = 600
NS = np.arange(N_MIN, N_MAX + 1)

# -----------------------------------------------------------------------------
# Chosen separated one-parameter families
# -----------------------------------------------------------------------------

# Gaussian: N(mu, 1)
# C0 = {N(mu,1): mu in [0, 0.5]}
# C1 = {N(mu,1): mu in [1, 1.5]}
# Least-favourable / projected endpoint pair: N(0.5,1), N(1,1)
GAUSSIAN = {
    "p_mean": 0.5,
    "q_mean": 1.0,
    "sigma": 1.0,
}

# Exponential rate parametrisation f_rho(x)=rho exp(-rho x), x>=0.
# C0 = {Exp(rho): rho in [1.5, 2.0]}
# C1 = {Exp(rho): rho in [0.75, 1.0]}
# Natural parameter is -rho.
# Least-favourable / projected endpoint pair: Exp(1.5), Exp(1.0)
EXPONENTIAL = {
    "p_rate": 1.5,
    "q_rate": 1.0,
}


# -----------------------------------------------------------------------------
# Divergences and exact endpoint tests
# -----------------------------------------------------------------------------

def gaussian_rc() -> float:
    p = GAUSSIAN["p_mean"]
    q = GAUSSIAN["q_mean"]
    sigma = GAUSSIAN["sigma"]
    return (q - p) ** 2 / (2.0 * sigma**2)


def renyi_gaussian(alpha: float) -> float:
    # Equal-variance Gaussian D_alpha(Q||P).
    return alpha * gaussian_rc()


def beta_gaussian(n: int, epsilon: float) -> float:
    if epsilon >= 1.0:
        return 0.0
    if epsilon <= 0.0:
        return 1.0
    p = GAUSSIAN["p_mean"]
    q = GAUSSIAN["q_mean"]
    sigma = GAUSSIAN["sigma"]
    z = norm.isf(epsilon)
    return float(norm.cdf(z - (q - p) * math.sqrt(n) / sigma))


def renyi_exponential(q_rate: float, p_rate: float, alpha: float) -> float:
    denom = alpha * q_rate + (1.0 - alpha) * p_rate
    if denom <= 0.0:
        return math.inf
    log_h = (
        alpha * math.log(q_rate)
        + (1.0 - alpha) * math.log(p_rate)
        - math.log(denom)
    )
    return log_h / (alpha - 1.0)


def exponential_rc() -> float:
    q = EXPONENTIAL["q_rate"]
    p = EXPONENTIAL["p_rate"]
    return math.log(q / p) + p / q - 1.0


def beta_exponential(n: int, epsilon: float) -> float:
    if epsilon >= 1.0:
        return 0.0
    if epsilon <= 0.0:
        return 1.0
    p = EXPONENTIAL["p_rate"]
    q = EXPONENTIAL["q_rate"]
    threshold = gamma.isf(epsilon, a=n, scale=1.0 / p)
    return float(gamma.cdf(threshold, a=n, scale=1.0 / q))


# -----------------------------------------------------------------------------
# Converse bounds
# -----------------------------------------------------------------------------

def maximise_over_alpha(objective, alpha_max: float) -> tuple[float, float]:
    """Robust one-dimensional maximisation over alpha>1."""
    deltas = np.geomspace(1.0e-8, alpha_max - 1.0, 700)
    grid = 1.0 + deltas
    values = np.asarray([objective(alpha) for alpha in grid], dtype=float)
    i = int(np.nanargmax(values))
    best = float(values[i])
    alpha_star = float(grid[i])

    left = float(grid[max(0, i - 2)])
    right = float(grid[min(len(grid) - 1, i + 2)])
    if right > left:
        result = minimize_scalar(
            lambda alpha: -objective(alpha),
            bounds=(left, right),
            method="bounded",
            options={"xatol": 1.0e-11},
        )
        if result.success and -float(result.fun) > best:
            best = -float(result.fun)
            alpha_star = float(result.x)
    return best, alpha_star


def reverse_renyi_converse(
    n: int,
    epsilon: float,
    d_qp,
    alpha_max: float,
) -> float:
    """Finite-sample Renyi converse from the main theorem."""
    if epsilon >= 1.0:
        return 0.0
    log_inv_epsilon = math.log(1.0 / epsilon)

    def exponent(alpha: float) -> float:
        d = d_qp(alpha)
        if not math.isfinite(d):
            return 0.0
        gap = log_inv_epsilon - n * d
        if gap <= 0.0:
            return 0.0
        return (alpha - 1.0) / alpha * gap

    best, _ = maximise_over_alpha(exponent, alpha_max)
    return 1.0 - math.exp(-max(0.0, best))


def forward_renyi_converse(
    n: int,
    epsilon: float,
    d_pq,
    alpha_max: float = 10000.0,
) -> float:
    """Opposite-direction finite-sample Renyi converse used numerically."""
    if epsilon >= 1.0:
        return 0.0
    log_one_minus_epsilon = math.log1p(-epsilon)

    def log_bound(alpha: float) -> float:
        d = d_pq(alpha)
        if not math.isfinite(d):
            return -math.inf
        return alpha / (alpha - 1.0) * log_one_minus_epsilon - n * d

    best, _ = maximise_over_alpha(log_bound, alpha_max)
    return math.exp(min(0.0, best))


def fano_converse(n: int, epsilon: float, d_qp: float) -> float:
    """Fano/data-processing converse used in the repository numerics."""
    if epsilon >= 1.0:
        return 0.0
    if epsilon <= 0.0:
        return 1.0
    denominator = math.log(1.0 / epsilon)
    return max(0.0, 1.0 - (n * d_qp + 1.0) / denominator)


# -----------------------------------------------------------------------------
# Numerical curves
# -----------------------------------------------------------------------------

def epsilon_for(regime: str, n: int, rc: float) -> float:
    if regime == "fixed":
        return 0.01
    if regime == "one_over_n":
        return 1.0 / n
    if regime == "exp_achievable":
        return math.exp(-n * 0.75 * rc)
    if regime == "exp_converse":
        return math.exp(-n * 1.90 * rc)
    raise ValueError(regime)


def family_curves(family: str, regime: str) -> dict[str, np.ndarray]:
    if family == "gaussian":
        rc = gaussian_rc()
        exact_beta = beta_gaussian
        d_qp = renyi_gaussian
        d_pq = renyi_gaussian
        reverse_alpha_max = 100.0
    elif family == "exponential":
        rc = exponential_rc()
        exact_beta = beta_exponential
        p = EXPONENTIAL["p_rate"]
        q = EXPONENTIAL["q_rate"]
        d_qp = lambda alpha: renyi_exponential(q, p, alpha)
        d_pq = lambda alpha: renyi_exponential(p, q, alpha)
        # D_alpha(Exp(1)||Exp(1.5)) diverges at alpha >= 3.
        reverse_alpha_max = 2.999999
    else:
        raise ValueError(family)

    epsilon = np.asarray(
        [epsilon_for(regime, int(n), rc) for n in NS],
        dtype=float,
    )
    exact = np.asarray(
        [exact_beta(int(n), float(eps)) for n, eps in zip(NS, epsilon)],
        dtype=float,
    )

    # For these separated one-parameter families, endpoint reduction makes the
    # calibrated projected test exactly equal to the endpoint NP test.
    projected = exact.copy()

    reverse = np.asarray(
        [
            reverse_renyi_converse(
                int(n), float(eps), d_qp, reverse_alpha_max
            )
            for n, eps in zip(NS, epsilon)
        ],
        dtype=float,
    )
    forward = np.asarray(
        [
            forward_renyi_converse(int(n), float(eps), d_pq)
            for n, eps in zip(NS, epsilon)
        ],
        dtype=float,
    )
    renyi = np.maximum(reverse, forward)
    fano = np.asarray(
        [fano_converse(int(n), float(eps), rc) for n, eps in zip(NS, epsilon)],
        dtype=float,
    )

    tolerance = 2.0e-9
    if np.any(renyi > exact + tolerance):
        raise RuntimeError(f"Renyi converse exceeds exact beta for {family}, {regime}")
    if np.any(fano > exact + tolerance):
        raise RuntimeError(f"Fano converse exceeds exact beta for {family}, {regime}")

    return {
        "n": NS.astype(float),
        "epsilon": epsilon,
        "exact": exact,
        "projected": projected,
        "renyi": renyi,
        "fano": fano,
    }


# -----------------------------------------------------------------------------
# Figure style and layout
# -----------------------------------------------------------------------------

plt.rcParams.update(
    {
        "font.family": "DejaVu Serif",
        "mathtext.fontset": "dejavuserif",
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 9,
        "axes.linewidth": 0.8,
        "lines.linewidth": 1.8,
        "savefig.facecolor": "white",
    }
)


def style_axis(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="out", length=4, width=0.8)
    ax.set_xlabel("samples n")
    ax.set_ylabel("Type II error")


def tight_achievability_ylim(values: np.ndarray) -> tuple[float, float]:
    ymin = float(np.min(values))
    ymax = float(np.max(values))
    span = ymax - ymin
    if span < 1.0e-6:
        pad = max(0.02 * max(abs(ymax), 1.0), 1.0e-4)
    else:
        pad = max(0.08 * span, 1.0e-4)
    low = max(0.0, ymin - pad)
    high = min(1.0, ymax + pad)
    if high - low < 5.0e-4:
        midpoint = 0.5 * (high + low)
        low = max(0.0, midpoint - 2.5e-4)
        high = min(1.0, midpoint + 2.5e-4)
    return low, high


def make_figure(family: str, output_name: str) -> None:
    fig, axes = plt.subplots(3, 2, figsize=(8.6, 11.2), sharex=False)

    row_specs = [
        (
            "fixed",
            "fixed",
            r"Achievability, $\varepsilon = 0.01$",
            r"Converse, $\varepsilon = 0.01$",
        ),
        (
            "one_over_n",
            "one_over_n",
            r"Achievability, $\varepsilon = 1/n$",
            r"Converse, $\varepsilon = 1/n$",
        ),
        (
            "exp_achievable",
            "exp_converse",
            r"Achievability, $\varepsilon_n = e^{-0.75 r_c n}$",
            r"Converse, $\varepsilon_n = e^{-1.90 r_c n}$",
        ),
    ]

    for row, (left_regime, right_regime, left_title, right_title) in enumerate(row_specs):
        left = family_curves(family, left_regime)
        ax = axes[row, 0]
        ax.plot(left["n"], left["exact"], label="Optimal Type II error")
        ax.plot(
            left["n"],
            left["projected"],
            "--",
            label=r"R\'enyi achievability bound",
        )
        style_axis(ax)
        ax.set_title(left_title, pad=8)
        ax.set_ylim(*tight_achievability_ylim(left["exact"]))
        ax.legend(frameon=False, loc="best")

        right = family_curves(family, right_regime)
        ax = axes[row, 1]
        ax.plot(right["n"], right["exact"], label="Optimal Type II error")
        ax.plot(right["n"], right["renyi"], label=r"R\'enyi converse")
        ax.plot(right["n"], right["fano"], label="Fano-style converse")
        style_axis(ax)
        ax.set_title(right_title, pad=8)
        ax.set_ylim(0.0, 1.0)
        ax.legend(frameon=False, loc="best")

    title = "Gaussian" if family == "gaussian" else "Exponential"
    fig.suptitle(title, y=0.995, fontsize=13)
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.985))
    fig.savefig(ROOT / output_name, format="eps")
    plt.close(fig)


def main() -> None:
    make_figure("gaussian", "Fig_01.eps")
    make_figure("exponential", "Fig_02.eps")
    print(f"Gaussian r_c = {gaussian_rc():.12f}")
    print(f"Exponential r_c = {exponential_rc():.12f}")
    print(f"Wrote {ROOT / 'Fig_01.eps'}")
    print(f"Wrote {ROOT / 'Fig_02.eps'}")


if __name__ == "__main__":
    main()
