"""The ptb command line.

A small argparse CLI. It tokenises the corpus to raw counts, and turns those
counts into the per-tokeniser summary. More subcommands (cost, plots) join it as
those pieces land.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from persiantokenbench.adapters import load_available
from persiantokenbench.corpus import default_corpus_path, load_corpus
from persiantokenbench.measure import tokenise_corpus, write_counts
from persiantokenbench.metrics import load_counts, summarise

DEFAULT_COUNTS = Path("results/token_counts.csv")
DEFAULT_SUMMARY = Path("results/summary.csv")


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


def _render_summary(summary) -> str:
    show = summary.copy()
    show["95% ci"] = show.apply(lambda r: f"[{r['ci_low']:.2f}, {r['ci_high']:.2f}]", axis=1)
    for col in ("mean_ratio", "median_ratio", "weighted_ratio"):
        show[col] = show[col].map(lambda x: f"{x:.2f}")
    cols = ["tokeniser", "family", "n", "mean_ratio", "95% ci", "median_ratio", "weighted_ratio"]
    return show[cols].to_string(index=False)


def _cmd_metrics(args: argparse.Namespace) -> None:
    summary = summarise(load_counts(args.counts), seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.out, index=False)
    print(_render_summary(summary))
    print(f"\nwrote {args.out}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="ptb", description="Persian vs English token costs.")
    sub = parser.add_subparsers(dest="command", required=True)

    t = sub.add_parser("tokenise", help="tokenise the corpus to a csv of raw counts")
    t.add_argument("--corpus", type=Path, default=None, help="corpus jsonl path")
    t.add_argument("--out", type=Path, default=DEFAULT_COUNTS, help="output counts csv")
    t.set_defaults(func=_cmd_tokenise)

    m = sub.add_parser("metrics", help="summarise the counts into per-tokeniser ratios")
    m.add_argument("--counts", type=Path, default=DEFAULT_COUNTS, help="input counts csv")
    m.add_argument("--out", type=Path, default=DEFAULT_SUMMARY, help="output summary csv")
    m.add_argument("--seed", type=int, default=0, help="bootstrap seed")
    m.set_defaults(func=_cmd_metrics)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
