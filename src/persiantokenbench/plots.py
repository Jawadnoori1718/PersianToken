"""The figures.

Three plain horizontal bar charts: the inflation ratio (with its confidence
interval), the extra cost, and the context a window loses. I keep them minimal,
with honest axes from zero, one colour, direct labels, a parity line where it
helps, and a short caption that states the assumptions. No display is needed, so
I render straight to files.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

plt.switch_backend("Agg")

BAR = "#4C78A8"
REF = "#E45756"
INK = "#333333"
MUTED = "#666666"
GRID = "#DDDDDD"


def _barchart(
    labels,
    values,
    path: Path,
    *,
    xlabel: str,
    title: str,
    caption: str,
    value_fmt,
    xerr=None,
    ref=None,
) -> None:
    n = len(labels)
    y = list(range(n))
    fig, ax = plt.subplots(figsize=(7.4, 0.6 * n + 1.9))
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

    for yi, v, end in zip(y, values, ends, strict=True):
        ax.text(end + right * 0.02, yi, value_fmt(v), va="center", fontsize=9, color=INK)

    ax.set_yticks(y, labels)
    ax.set_xlabel(xlabel)
    ax.set_title(title, loc="left", fontweight="bold", fontsize=13)
    ax.set_xlim(0, right * 1.15)
    ax.invert_yaxis()
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(length=0)
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, color=GRID, linewidth=0.8)
    ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))

    ax.annotate(
        caption,
        xy=(0, 0),
        xycoords="axes fraction",
        xytext=(0, -44),
        textcoords="offset points",
        fontsize=8,
        color=MUTED,
        ha="left",
        va="top",
    )
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_ratio(summary: pd.DataFrame, path: Path) -> None:
    n = int(summary["n"].iloc[0])
    lo = (summary["mean_ratio"] - summary["ci_low"]).tolist()
    hi = (summary["ci_high"] - summary["mean_ratio"]).tolist()
    _barchart(
        summary["tokeniser"].tolist(),
        summary["mean_ratio"].tolist(),
        path,
        xlabel="Persian tokens per English token",
        title="Token inflation by tokeniser",
        caption=(
            f"Mean over {n} sentence pairs; whiskers are the bootstrap 95% CI. "
            "The dashed line marks English parity (1.0)."
        ),
        value_fmt=lambda v: f"{v:.2f}x",
        xerr=[lo, hi],
        ref=1.0,
    )


def plot_cost(cost: pd.DataFrame, path: Path) -> None:
    _barchart(
        cost["tokeniser"].tolist(),
        cost["extra_cost"].tolist(),
        path,
        xlabel="extra $ for the same content, per 1M English tokens",
        title="Extra cost for Persian",
        caption=(
            "A flat price of $3 per 1M tokens, so the gap reflects the tokeniser, "
            "not one vendor's price list."
        ),
        value_fmt=lambda v: f"${v:,.2f}",
    )


def plot_context(context: pd.DataFrame, path: Path) -> None:
    window = int(context["window"].iloc[0])
    _barchart(
        context["tokeniser"].tolist(),
        context["effective_window"].tolist(),
        path,
        xlabel="effective context in English-equivalent tokens",
        title="Context a window holds in Persian",
        caption=(
            f"English-equivalent meaning that fits a {window:,}-token window. "
            "The dashed line is the full window."
        ),
        value_fmt=lambda v: f"{v:,.0f}",
        ref=float(context["window"].iloc[0]),
    )
