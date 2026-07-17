"""Tokenise the corpus and write raw per-sentence counts.

One row per (sentence, tokeniser): the English and Persian token counts side by
side. Everything downstream reads this CSV, so the raw numbers stay inspectable.
"""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path

from persiantokenbench.adapters.base import Tokeniser
from persiantokenbench.corpus import Pair

FIELDS = ["id", "tokeniser", "family", "approximate", "en_tokens", "fa_tokens"]


@dataclass(frozen=True)
class Count:
    id: str
    tokeniser: str
    family: str
    approximate: bool
    en_tokens: int
    fa_tokens: int


def tokenise_corpus(pairs: list[Pair], tokenisers: list[Tokeniser]) -> list[Count]:
    rows: list[Count] = []
    for tok in tokenisers:
        for pair in pairs:
            rows.append(
                Count(
                    id=pair.id,
                    tokeniser=tok.name,
                    family=tok.family,
                    approximate=tok.approximate,
                    en_tokens=tok.count(pair.en),
                    fa_tokens=tok.count(pair.fa),
                )
            )
    return rows


def write_counts(rows: list[Count], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
