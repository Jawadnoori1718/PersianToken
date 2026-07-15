"""Loading and validating the parallel corpus.

I want bad data to fail loudly and early, with a line number, rather than
quietly skewing a token count later on.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = _REPO_ROOT / "data"


@dataclass(frozen=True)
class Pair:
    id: str
    en: str
    fa: str


class CorpusError(ValueError):
    pass


def default_corpus_path() -> Path:
    # I prefer the built FLORES corpus when it exists, and fall back to the sample.
    built = DATA_DIR / "corpus.jsonl"
    return built if built.exists() else DATA_DIR / "sample.jsonl"


def load_corpus(path: Path | None = None) -> list[Pair]:
    path = Path(path) if path is not None else default_corpus_path()
    pairs: list[Pair] = []
    seen: set[str] = set()
    with path.open(encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            raw = raw.strip()
            if not raw:
                continue
            pair = _parse_row(raw, lineno)
            if pair.id in seen:
                raise CorpusError(f"{path} line {lineno}: duplicate id {pair.id!r}")
            seen.add(pair.id)
            pairs.append(pair)
    if not pairs:
        raise CorpusError(f"{path}: no rows found")
    return pairs


def _parse_row(raw: str, lineno: int) -> Pair:
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        raise CorpusError(f"line {lineno}: invalid json: {e}") from e
    if not isinstance(obj, dict):
        raise CorpusError(f"line {lineno}: expected a json object")
    for key in ("id", "en", "fa"):
        if key not in obj:
            raise CorpusError(f"line {lineno}: missing field {key!r}")
        value = obj[key]
        if not isinstance(value, str) or not value.strip():
            raise CorpusError(f"line {lineno}: field {key!r} must be a non-empty string")
    return Pair(id=obj["id"], en=obj["en"], fa=obj["fa"])
