import pandas as pd

from persiantokenbench.metrics import add_ratio, summarise


def _counts():
    rows = [
        # id, tokeniser, family, approximate, en_tokens, fa_tokens
        ("a", "t1", "f", False, 1, 2),
        ("b", "t1", "f", False, 2, 2),
        ("a", "t2", "g", False, 1, 4),
        ("b", "t2", "g", False, 1, 2),
    ]
    cols = ["id", "tokeniser", "family", "approximate", "en_tokens", "fa_tokens"]
    return pd.DataFrame(rows, columns=cols)


def test_add_ratio_is_fa_over_en():
    df = add_ratio(_counts())
    assert list(df["ratio"]) == [2.0, 1.0, 4.0, 2.0]


def test_summarise_point_estimates():
    s = summarise(_counts()).set_index("tokeniser")
    # t1: ratios [2, 1] -> mean 1.5, median 1.5, weighted (2+2)/(1+2) = 4/3
    assert s.loc["t1", "n"] == 2
    assert s.loc["t1", "mean_ratio"] == 1.5
    assert s.loc["t1", "median_ratio"] == 1.5
    assert abs(s.loc["t1", "weighted_ratio"] - 4 / 3) < 1e-9
    # t2: ratios [4, 2] -> mean 3, weighted (4+2)/(1+1) = 3
    assert s.loc["t2", "mean_ratio"] == 3.0
    assert s.loc["t2", "weighted_ratio"] == 3.0


def test_summarise_sorted_by_mean_desc():
    s = summarise(_counts())
    assert list(s["tokeniser"]) == ["t2", "t1"]
