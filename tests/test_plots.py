import pandas as pd

from persiantokenbench.plots import plot_ratio


def test_plot_ratio_writes_a_png(tmp_path):
    summary = pd.DataFrame(
        {
            "tokeniser": ["a", "b"],
            "mean_ratio": [3.0, 1.5],
            "ci_low": [2.8, 1.4],
            "ci_high": [3.2, 1.6],
        }
    )
    out = tmp_path / "ratio.png"
    plot_ratio(summary, out)
    assert out.exists()
    assert out.stat().st_size > 0
