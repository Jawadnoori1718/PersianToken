import pandas as pd

from persiantokenbench.cost import cost_table


def _summary():
    return pd.DataFrame({"tokeniser": ["a", "b"], "family": ["f", "g"], "mean_ratio": [3.0, 1.5]})


def test_cost_scales_with_ratio():
    # $2 per million english tokens, one million tokens of content -> $2 in english
    t = cost_table(_summary(), price_per_million=2.0, en_tokens=1_000_000).set_index("tokeniser")
    assert t.loc["a", "english_cost"] == 2.0
    assert t.loc["a", "persian_cost"] == 6.0  # 3x
    assert t.loc["a", "extra_cost"] == 4.0
    assert t.loc["a", "extra_pct"] == 200.0
    assert t.loc["b", "persian_cost"] == 3.0  # 1.5x
    assert t.loc["b", "extra_pct"] == 50.0


def test_extra_cost_is_persian_minus_english():
    t = cost_table(_summary(), price_per_million=5.0, en_tokens=250_000)
    assert (t["extra_cost"] == t["persian_cost"] - t["english_cost"]).all()
