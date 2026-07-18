"""The cost model.

I turn the inflation ratio into money. Given a price per million tokens and a
workload measured in English tokens, I work out what the same content costs in
Persian and how much extra that is. The price stays a single knob, so the number
reflects the tokeniser rather than one vendor's price list.
"""

from __future__ import annotations

import pandas as pd


def cost_table(
    summary: pd.DataFrame,
    price_per_million: float,
    en_tokens: float,
    ratio_col: str = "mean_ratio",
) -> pd.DataFrame:
    out = summary[["tokeniser", "family", ratio_col]].copy()
    out = out.rename(columns={ratio_col: "ratio"})
    english = en_tokens / 1_000_000 * price_per_million
    out["english_cost"] = english
    out["persian_cost"] = english * out["ratio"]
    out["extra_cost"] = out["persian_cost"] - out["english_cost"]
    out["extra_pct"] = (out["ratio"] - 1.0) * 100.0
    return out
