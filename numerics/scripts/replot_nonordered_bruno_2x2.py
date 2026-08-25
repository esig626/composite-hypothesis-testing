#!/usr/bin/env python3
"""Replot the non-ordered Bruno 2x2 figure from the saved CSV only.

This script performs no optimisation or hypothesis-testing calculations.  It reads
``numerics/data/nonordered_bruno_regimes.csv`` and redraws the four saved curves
using the publication-style palette and typography requested for the figure.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "numerics" / "data" / "nonordered_bruno_regimes.csv"
FIGURE_DIR = ROOT / "numerics" / "figures"

BLUE = "#1f77b4"
ORANGE = "#ff7f0e"


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
        "legend.fontsize": 9.5,
        "axes.linewidth": 0.8,
        "lines.linewidth": 1.8,
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
    }
)


def load_saved_curves() -> dict[str, list[dict[str, float]]]:
    """Read only the columns required for plotting from the saved CSV."""
    curves: dict[str, list[dict[str, float]]] = {"constant": [], "linear": []}
    with DATA_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            regime = row["regime"]
            if regime not in curves:
                continue
            curves[regime].append(
                {
                    "n": int(row["n"]),
                    "minimax": float(row["minimax"]),
                    "achievability": float(row["achievability"]),
                    "converse": float(row["converse"]),
                }
            )

    for regime in curves:
        curves[regime].sort(key=lambda row: row["n"])
    return curves


def style_axis(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="out", length=4, width=0.8)
    ax.set_xlim(1, 300)
    ax.set_ylim(bottom=0.0)
    ax.set_xlabel(r"samples $n$")
    ax.set_ylabel("Type II error")


def plot_panel(
    ax: plt.Axes,
    rows: list[dict[str, float]],
    bound_key: str,
    bound_label: str,
    title: str,
) -> None:
    n = [row["n"] for row in rows]
    minimax = [row["minimax"] for row in rows]
    bound = [row[bound_key] for row in rows]

    ax.plot(n, minimax, color=BLUE, label="minimax Type II error")
    ax.plot(n, bound, color=ORANGE, label=bound_label)
    style_axis(ax)
    ax.set_title(title, pad=8)
    ax.legend(frameon=False, loc="upper right")


def main() -> None:
    curves = load_saved_curves()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.9), sharex=True, sharey=False)

    plot_panel(
        axes[0, 0],
        curves["constant"],
        "achievability",
        "achievability bound",
        r"Achievability, $\varepsilon = 0.01$",
    )
    plot_panel(
        axes[0, 1],
        curves["constant"],
        "converse",
        "converse bound",
        r"Converse, $\varepsilon = 0.01$",
    )
    plot_panel(
        axes[1, 0],
        curves["linear"],
        "achievability",
        "achievability bound",
        r"Achievability, $\varepsilon = 1/n$",
    )
    plot_panel(
        axes[1, 1],
        curves["linear"],
        "converse",
        "converse bound",
        r"Converse, $\varepsilon = 1/n$",
    )

    fig.tight_layout(pad=1.2, w_pad=2.0, h_pad=2.0)

    fig.savefig(FIGURE_DIR / "nonordered_bruno_2x2.eps", format="eps", bbox_inches="tight")
    fig.savefig(FIGURE_DIR / "nonordered_bruno_2x2.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
