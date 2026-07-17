"""The ptb command line.

A small argparse CLI. For now it tokenises the corpus to a CSV of raw counts;
more subcommands (metrics, cost, plots) join it as those pieces land.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from persiantokenbench.adapters import load_available
from persiantokenbench.corpus import default_corpus_path, load_corpus
from persiantokenbench.measure import tokenise_corpus, write_counts

DEFAULT_COUNTS = Path("results/token_counts.csv")


def _cmd_tokenise(args: argparse.Namespace) -> None:
    corpus_path = args.corpus or default_corpus_path()
    pairs = load_corpus(corpus_path)
    tokenisers = load_available()
    if not tokenisers:
        raise SystemExit(
            "no tokenisers could be loaded; install the deps or log in to hugging face"
        )
    rows = tokenise_corpus(pairs, tokenisers)
    write_counts(rows, args.out)
    print(f"corpus: {corpus_path}")
    print(f"tokenised {len(pairs)} pairs with {len(tokenisers)} tokenisers")
    print(f"wrote {len(rows)} rows to {args.out}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="ptb", description="Persian vs English token costs.")
    sub = parser.add_subparsers(dest="command", required=True)

    t = sub.add_parser("tokenise", help="tokenise the corpus to a csv of raw counts")
    t.add_argument("--corpus", type=Path, default=None, help="corpus jsonl path")
    t.add_argument("--out", type=Path, default=DEFAULT_COUNTS, help="output counts csv")
    t.set_defaults(func=_cmd_tokenise)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
