"""The ptb command line.

A small argparse CLI: tokenise the corpus to raw counts, summarise them into
per-tokeniser ratios, and turn those ratios into the extra cost Persian pays.
More subcommands (context, plots) join it as those pieces land.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from persiantokenbench.adapters import load_available
from persiantokenbench.corpus import default_corpus_path, load_corpus
from persiantokenbench.cost import cost_table
from persiantokenbench.measure import tokenise_corpus, write_counts
from persiantokenbench.metrics import load_counts, summarise

DEFAULT_COUNTS = Path("results/token_counts.csv")
DEFAULT_SUMMARY = Path("results/summary.csv")
DEFAULT_COST = Path("results/cost.csv")


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


def _render_cost(table, price: float, tokens: float) -> str:
    show = table.copy()
    for col in ("english_cost", "persian_cost", "extra_cost"):
        show[col] = show[col].map(lambda x: f"${x:,.2f}")
    show["ratio"] = show["ratio"].map(lambda x: f"{x:.2f}")
    show["extra_pct"] = show["extra_pct"].map(lambda x: f"+{x:.0f}%")
    header = f"price ${price:g}/1M tokens, workload {int(tokens):,} english tokens\n"
    return header + show.to_string(index=False)


def _cmd_cost(args: argparse.Namespace) -> None:
    summary = pd.read_csv(args.summary)
    table = cost_table(summary, args.price, args.tokens)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(args.out, index=False)
    print(_render_cost(table, args.price, args.tokens))
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

    c = sub.add_parser("cost", help="turn the ratios into extra cost for persian")
    c.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY, help="input summary csv")
    c.add_argument("--out", type=Path, default=DEFAULT_COST, help="output cost csv")
    c.add_argument("--price", type=float, default=3.0, help="price per million tokens")
    c.add_argument("--tokens", type=float, default=1_000_000, help="workload in english tokens")
    c.set_defaults(func=_cmd_cost)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
