"""The ratio maths.

The token inflation ratio is Persian tokens over English tokens for the same
sentence. I compute it per sentence, then aggregate a few ways: the mean and
median of the per-sentence ratios, and the token-weighted ratio (all Persian
tokens over all English tokens). I keep several because the per-sentence ratios
are skewed, so no single number tells the whole story.

For the mean I also bootstrap a confidence interval, since the ratios are skewed
and I would rather not assume they are normal.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def load_counts(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)


def add_ratio(counts: pd.DataFrame) -> pd.DataFrame:
    out = counts.copy()
    out["ratio"] = out["fa_tokens"] / out["en_tokens"]
    return out


def bootstrap_mean_ci(
    values, n_boot: int = 10000, level: float = 0.95, seed: int = 0
) -> tuple[float, float]:
    # I resample the per-sentence ratios with replacement and take the spread of
    # the resampled means. Seeded, so the interval is reproducible.
    rng = np.random.default_rng(seed)
    values = np.asarray(values, dtype=float)
    n = len(values)
    means = values[rng.integers(0, n, size=(n_boot, n))].mean(axis=1)
    lo = (1.0 - level) / 2.0 * 100.0
    hi = (1.0 + level) / 2.0 * 100.0
    return float(np.percentile(means, lo)), float(np.percentile(means, hi))


def summarise(counts: pd.DataFrame, n_boot: int = 10000, seed: int = 0) -> pd.DataFrame:
    df = add_ratio(counts)
    grouped = df.groupby(["tokeniser", "family", "approximate"], sort=False)
    summary = grouped.agg(
        n=("ratio", "size"),
        mean_ratio=("ratio", "mean"),
        median_ratio=("ratio", "median"),
        en_total=("en_tokens", "sum"),
        fa_total=("fa_tokens", "sum"),
    ).reset_index()
    summary["weighted_ratio"] = summary["fa_total"] / summary["en_total"]

    cis = {
        name: bootstrap_mean_ci(group["ratio"].to_numpy(), n_boot=n_boot, seed=seed)
        for name, group in df.groupby("tokeniser", sort=False)
    }
    summary["ci_low"] = summary["tokeniser"].map(lambda t: cis[t][0])
    summary["ci_high"] = summary["tokeniser"].map(lambda t: cis[t][1])

    cols = [
        "tokeniser",
        "family",
        "approximate",
        "n",
        "mean_ratio",
        "ci_low",
        "ci_high",
        "median_ratio",
        "weighted_ratio",
    ]
    return summary[cols].sort_values("mean_ratio", ascending=False, ignore_index=True)
