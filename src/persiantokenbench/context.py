"""The context-window model.

A context window is quoted in tokens, but Persian spends more tokens per unit of
meaning. So a window that holds a long English document holds a much shorter
Persian one. I measure the effective window, in English-equivalent tokens, and
how much of it Persian loses.
"""

from __future__ import annotations

import pandas as pd


def context_table(
    summary: pd.DataFrame,
    window: float,
    ratio_col: str = "mean_ratio",
) -> pd.DataFrame:
    out = summary[["tokeniser", "family", ratio_col]].copy()
    out = out.rename(columns={ratio_col: "ratio"})
    out["window"] = window
    # effective window: how much english-equivalent meaning fits when writing persian
    out["effective_window"] = window / out["ratio"]
    out["lost_tokens"] = window - out["effective_window"]
    out["lost_pct"] = (1.0 - 1.0 / out["ratio"]) * 100.0
    return out
