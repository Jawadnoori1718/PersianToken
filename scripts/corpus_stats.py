"""Print basic stats about the corpus: how many pairs there are, and how long
the sentences run on each side. I use this to sanity check the data before I
start counting tokens.

Note this counts characters and words, not tokens. The interesting gap shows up
later, once the tokenisers get involved.
"""

from __future__ import annotations

import argparse
import statistics
from pathlib import Path

from persiantokenbench.corpus import default_corpus_path, load_corpus


def _row(label: str, en: float, fa: float) -> None:
    print(f"{label:<16}{en:>10}{fa:>10}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Print basic corpus stats.")
    parser.add_argument("--path", type=Path, default=None)
    args = parser.parse_args()

    path = args.path or default_corpus_path()
    pairs = load_corpus(path)

    en_chars = [len(pair.en) for pair in pairs]
    fa_chars = [len(pair.fa) for pair in pairs]
    en_words = [len(pair.en.split()) for pair in pairs]
    fa_words = [len(pair.fa.split()) for pair in pairs]

    print(f"corpus: {path}")
    print(f"pairs:  {len(pairs)}")
    print()
    print(f"{'':<16}{'english':>10}{'persian':>10}")
    _row("chars total", sum(en_chars), sum(fa_chars))
    _row("chars mean", round(statistics.mean(en_chars), 1), round(statistics.mean(fa_chars), 1))
    _row("chars median", statistics.median(en_chars), statistics.median(fa_chars))
    _row("chars min", min(en_chars), min(fa_chars))
    _row("chars max", max(en_chars), max(fa_chars))
    _row("words mean", round(statistics.mean(en_words), 1), round(statistics.mean(fa_words), 1))
    print()
    print(f"persian/english characters: {sum(fa_chars) / sum(en_chars):.2f}")


if __name__ == "__main__":
    main()
