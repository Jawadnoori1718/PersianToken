"""The ratio maths.

The token inflation ratio is Persian tokens over English tokens for the same
sentence. I compute it per sentence, then aggregate a few ways: the mean and
median of the per-sentence ratios, and the token-weighted ratio (all Persian
tokens over all English tokens). I keep several because the per-sentence ratios
are skewed, so no single number tells the whole story.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_counts(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)


def add_ratio(counts: pd.DataFrame) -> pd.DataFrame:
    out = counts.copy()
    out["ratio"] = out["fa_tokens"] / out["en_tokens"]
    return out


def summarise(counts: pd.DataFrame) -> pd.DataFrame:
    df = add_ratio(counts)
    grouped = df.groupby(["tokeniser", "family", "approximate"], sort=False)
    summary = grouped.agg(
        n=("ratio", "size"),
        mean_ratio=("ratio", "mean"),
        median_ratio=("ratio", "median"),
        en_total=("en_tokens", "sum"),
        fa_total=("fa_tokens", "sum"),
    ).reset_index()
    # token-weighted ratio: total Persian tokens over total English tokens
    summary["weighted_ratio"] = summary["fa_total"] / summary["en_total"]
    summary = summary.drop(columns=["en_total", "fa_total"])
    return summary.sort_values("mean_ratio", ascending=False, ignore_index=True)
