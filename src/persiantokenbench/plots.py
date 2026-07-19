"""The figures.

Three plain horizontal bar charts: the inflation ratio (with its confidence
interval), the extra cost, and the context a window loses. I keep them minimal,
with honest axes from zero, one colour, direct labels, and a parity line where it
helps. No display is needed, so I render straight to files.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

plt.switch_backend("Agg")

BAR = "#4C78A8"
REF = "#E45756"
INK = "#333333"
GRID = "#DDDDDD"


def _barchart(
    labels,
    values,
    path: Path,
    *,
    xlabel: str,
    title: str,
    value_fmt,
    xerr=None,
    ref=None,
    ref_label=None,
) -> None:
    n = len(labels)
    y = list(range(n))
    fig, ax = plt.subplots(figsize=(7.2, 0.55 * n + 1.4))
    ax.barh(
        y,
        values,
        height=0.62,
        color=BAR,
        zorder=3,
        xerr=xerr,
        error_kw={"ecolor": INK, "elinewidth": 1, "capsize": 3, "zorder": 4},
    )

    ends = values if xerr is None else [v + hi for v, hi in zip(values, xerr[1], strict=True)]
    right = max(ends)
    if ref is not None:
        right = max(right, ref)
        ax.axvline(ref, color=REF, linewidth=1.5, linestyle="--", zorder=2)
        if ref_label:
            ax.text(ref, -0.72, ref_label, color=REF, fontsize=8, ha="center", va="top")

    for yi, v, end in zip(y, values, ends, strict=True):
        ax.text(end + right * 0.02, yi, value_fmt(v), va="center", fontsize=9, color=INK)

    ax.set_yticks(y, labels)
    ax.set_xlabel(xlabel)
    ax.set_title(title, loc="left", fontweight="bold")
    ax.set_xlim(0, right * 1.15)
    ax.invert_yaxis()
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(length=0)
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, color=GRID, linewidth=0.8)

    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_ratio(summary: pd.DataFrame, path: Path) -> None:
    lo = (summary["mean_ratio"] - summary["ci_low"]).tolist()
    hi = (summary["ci_high"] - summary["mean_ratio"]).tolist()
    _barchart(
        summary["tokeniser"].tolist(),
        summary["mean_ratio"].tolist(),
        path,
        xlabel="Persian tokens per English token",
        title="Token inflation by tokeniser",
        value_fmt=lambda v: f"{v:.2f}x",
        xerr=[lo, hi],
        ref=1.0,
        ref_label="parity",
    )


def plot_cost(cost: pd.DataFrame, path: Path) -> None:
    _barchart(
        cost["tokeniser"].tolist(),
        cost["extra_cost"].tolist(),
        path,
        xlabel="extra $ for the same content, per 1M English tokens",
        title="Extra cost for Persian",
        value_fmt=lambda v: f"${v:,.2f}",
    )


def plot_context(context: pd.DataFrame, path: Path) -> None:
    _barchart(
        context["tokeniser"].tolist(),
        context["effective_window"].tolist(),
        path,
        xlabel="effective context in English-equivalent tokens",
        title="Context a window holds in Persian",
        value_fmt=lambda v: f"{v:,.0f}",
        ref=float(context["window"].iloc[0]),
        ref_label="full window",
    )
