import pandas as pd

from persiantokenbench.context import context_table


def test_effective_window_and_loss():
    summary = pd.DataFrame({"tokeniser": ["a"], "family": ["f"], "mean_ratio": [4.0]})
    row = context_table(summary, window=128_000).iloc[0]
    assert row["effective_window"] == 32_000.0  # 128000 / 4
    assert row["lost_tokens"] == 96_000.0
    assert row["lost_pct"] == 75.0  # 1 - 1/4


def test_lost_is_window_minus_effective():
    summary = pd.DataFrame(
        {"tokeniser": ["a", "b"], "family": ["f", "g"], "mean_ratio": [2.0, 1.25]}
    )
    t = context_table(summary, window=100_000)
    assert (t["lost_tokens"] == t["window"] - t["effective_window"]).all()
