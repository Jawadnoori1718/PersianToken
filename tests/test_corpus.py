import json
from pathlib import Path

import pytest

from persiantokenbench.corpus import DATA_DIR, CorpusError, Pair, load_corpus


def _write(tmp_path: Path, rows: list[str]) -> Path:
    p = tmp_path / "c.jsonl"
    p.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return p


def test_loads_valid_rows(tmp_path):
    rows = [
        json.dumps({"id": "a", "en": "hello", "fa": "سلام"}),
        json.dumps({"id": "b", "en": "world", "fa": "جهان"}),
    ]
    pairs = load_corpus(_write(tmp_path, rows))
    assert pairs == [Pair("a", "hello", "سلام"), Pair("b", "world", "جهان")]


def test_missing_field_fails(tmp_path):
    rows = [json.dumps({"id": "a", "en": "hi"})]
    with pytest.raises(CorpusError):
        load_corpus(_write(tmp_path, rows))


def test_empty_field_fails(tmp_path):
    rows = [json.dumps({"id": "a", "en": "hi", "fa": "   "})]
    with pytest.raises(CorpusError):
        load_corpus(_write(tmp_path, rows))


def test_duplicate_id_fails(tmp_path):
    rows = [
        json.dumps({"id": "a", "en": "hi", "fa": "سلام"}),
        json.dumps({"id": "a", "en": "bye", "fa": "خداحافظ"}),
    ]
    with pytest.raises(CorpusError):
        load_corpus(_write(tmp_path, rows))


def test_bad_json_fails(tmp_path):
    rows = ["{not valid json}"]
    with pytest.raises(CorpusError):
        load_corpus(_write(tmp_path, rows))


def test_sample_corpus_loads():
    pairs = load_corpus(DATA_DIR / "sample.jsonl")
    assert len(pairs) == 45
    assert all(p.en and p.fa for p in pairs)
