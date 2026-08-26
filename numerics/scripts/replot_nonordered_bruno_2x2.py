#!/usr/bin/env python3
"""Replot the non-ordered Bruno 2x2 figure from the saved CSV only.

This script performs no minimax, projected-test, or Renyi optimisation. It reads
``numerics/data/nonordered_bruno_regimes.csv`` and redraws the four saved curves.
For the converse panels it additionally evaluates the elementary Fano-style
converse from the already-audited composite KL separation.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "numerics" / "data" / "nonordered_bruno_regimes.csv"
FANO_DATA_PATH = ROOT / "numerics" / "data" / "nonordered_bruno_fano_converse.csv"
FIGURE_DIR = ROOT / "numerics" / "figures"

BLUE = "#1f77b4"
ORANGE = "#ff7f0e"
GREEN = "#2ca02c"

# Audited value produced by minimise_kl_over_classes("Q||P") for the fixed
# affine ternary classes used by nonordered_bruno_regimes.py.
COMPOSITE_KL_QP = 0.01739677970744148


plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["DejaVu Serif"],
        "mathtext.fontset": "dejavuserif",
        "font.size": 11,
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 9.0,
        "axes.linewidth": 0.8,
        "lines.linewidth": 1.8,
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
    }
)


def fano_converse(n: int, epsilon: float) -> float:
    """Return the same coarse Fano/data-processing converse used previously.

    Binary data processing gives

        n D >= (1-beta) log(1/epsilon) - 1,

    after using binary entropy <= 1. Hence

        beta >= [1 - (n D + 1)/log(1/epsilon)]_+.

    At epsilon=1 the constraint is vacuous, so the lower bound is zero.
    """
    if epsilon >= 1.0:
        return 0.0
    if epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    denominator = math.log(1.0 / epsilon)
    if denominator <= 0.0:
        return 0.0
    return max(0.0, 1.0 - (n * COMPOSITE_KL_QP + 1.0) / denominator)


def load_saved_curves() -> dict[str, list[dict[str, float]]]:
    """Read the saved numerical results and append the Fano-style converse."""
    curves: dict[str, list[dict[str, float]]] = {"constant": [], "linear": []}
    with DATA_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            regime = row["regime"]
            if regime not in curves:
                continue
            n = int(row["n"])
            epsilon = float(row["epsilon"])
            curves[regime].append(
                {
                    "n": n,
                    "epsilon": epsilon,
                    "minimax": float(row["minimax"]),
                    "achievability": float(row["achievability"]),
                    "converse": float(row["converse"]),
                    "fano_converse": fano_converse(n, epsilon),
                }
            )

    for regime in curves:
        curves[regime].sort(key=lambda row: row["n"])
        for row in curves[regime]:
            if row["fano_converse"] > row["minimax"] + 5.0e-10:
                raise RuntimeError(
                    "Fano-style converse exceeds numerical minimax value at "
                    f"n={int(row['n'])}, regime={regime}"
                )
    return curves


def write_fano_data(curves: dict[str, list[dict[str, float]]]) -> None:
    """Write the inexpensive third converse result as an auditable CSV."""
    FANO_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with FANO_DATA_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=(
                "n",
                "regime",
                "epsilon",
                "minimax",
                "renyi_converse",
                "fano_converse",
            ),
        )
        writer.writeheader()
        for regime in ("constant", "linear"):
            for row in curves[regime]:
                writer.writerow(
                    {
                        "n": int(row["n"]),
                        "regime": regime,
                        "epsilon": row["epsilon"],
                        "minimax": row["minimax"],
                        "renyi_converse": row["converse"],
                        "fano_converse": row["fano_converse"],
                    }
                )


def style_axis(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="out", length=4, width=0.8)
    ax.set_xlim(1, 300)
    ax.set_ylim(bottom=0.0)
    ax.set_xlabel(r"samples $n$")
    ax.set_ylabel("Type II error")


def plot_achievability_panel(
    ax: plt.Axes,
    rows: list[dict[str, float]],
    title: str,
) -> None:
    n = [row["n"] for row in rows]
    minimax = [row["minimax"] for row in rows]
    achievability = [row["achievability"] for row in rows]

    ax.plot(n, minimax, color=BLUE, label="minimax Type II error")
    ax.plot(n, achievability, color=ORANGE, label="achievability bound")
    style_axis(ax)
    ax.set_title(title, pad=8)
    ax.legend(frameon=False, loc="upper right")


def plot_converse_panel(
    ax: plt.Axes,
    rows: list[dict[str, float]],
    title: str,
) -> None:
    n = [row["n"] for row in rows]
    minimax = [row["minimax"] for row in rows]
    renyi = [row["converse"] for row in rows]
    fano = [row["fano_converse"] for row in rows]

    ax.plot(n, minimax, color=BLUE, label="minimax Type II error")
    ax.plot(n, renyi, color=ORANGE, label=r"R\'enyi converse")
    ax.plot(n, fano, color=GREEN, label="Fano-style converse")
    style_axis(ax)
    ax.set_title(title, pad=8)
    ax.legend(frameon=False, loc="best")


def main() -> None:
    curves = load_saved_curves()
    write_fano_data(curves)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.9), sharex=True, sharey=False)

    plot_achievability_panel(
        axes[0, 0],
        curves["constant"],
        r"Achievability, $\varepsilon = 0.01$",
    )
    plot_converse_panel(
        axes[0, 1],
        curves["constant"],
        r"Converse, $\varepsilon = 0.01$",
    )
    plot_achievability_panel(
        axes[1, 0],
        curves["linear"],
        r"Achievability, $\varepsilon = 1/n$",
    )
    plot_converse_panel(
        axes[1, 1],
        curves["linear"],
        r"Converse, $\varepsilon = 1/n$",
    )

    fig.tight_layout(pad=1.2, w_pad=2.0, h_pad=2.0)

    fig.savefig(FIGURE_DIR / "nonordered_bruno_2x2.eps", format="eps", bbox_inches="tight")
    fig.savefig(FIGURE_DIR / "nonordered_bruno_2x2.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
