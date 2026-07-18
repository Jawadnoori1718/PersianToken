import pandas as pd

from persiantokenbench.metrics import add_ratio, bootstrap_mean_ci, summarise


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


def test_bootstrap_is_deterministic_with_seed():
    vals = [1.0, 2.0, 3.0, 4.0, 5.0]
    a = bootstrap_mean_ci(vals, n_boot=2000, seed=7)
    b = bootstrap_mean_ci(vals, n_boot=2000, seed=7)
    assert a == b


def test_bootstrap_brackets_the_mean():
    vals = [1.0, 2.0, 2.0, 3.0, 10.0]
    lo, hi = bootstrap_mean_ci(vals, n_boot=5000, seed=0)
    assert lo <= sum(vals) / len(vals) <= hi
    assert lo < hi


def test_bootstrap_zero_variance_collapses():
    assert bootstrap_mean_ci([2.0, 2.0, 2.0], n_boot=100, seed=0) == (2.0, 2.0)


def test_summarise_has_ci_around_mean():
    row = summarise(_counts(), n_boot=500).set_index("tokeniser").loc["t1"]
    assert row["ci_low"] <= row["mean_ratio"] <= row["ci_high"]
