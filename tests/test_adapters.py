import pytest

from persiantokenbench.adapters import (
    Tokeniser,
    all_tokenisers,
    gpt_tokenisers,
    load_available,
)
from persiantokenbench.adapters.hf_adapter import HFAdapter
from persiantokenbench.adapters.tiktoken_adapter import TiktokenAdapter


def _require(adapter):
    # Skip rather than fail when a tokeniser can't load here (missing lib, no
    # network, or a gated model). CI should stay green on what it can actually run.
    try:
        adapter.count("ok")
    except Exception as e:
        pytest.skip(f"tokeniser unavailable: {e}")
    return adapter


def test_abstract_tokeniser_is_not_instantiable():
    with pytest.raises(TypeError):
        Tokeniser()


def test_registry_lists_every_tokeniser():
    toks = all_tokenisers()
    names = {t.name for t in toks}
    assert len(toks) == 7
    assert "gpt-4 cl100k_base" in names
    assert "gpt-4o o200k_base" in names
    assert "bloom" in names


class _Broken(Tokeniser):
    name = "broken"
    family = "x"

    def count(self, text: str) -> int:
        raise RuntimeError("nope")


def test_load_available_skips_a_broken_tokeniser():
    assert load_available([_Broken()]) == []


class _StubHFTokeniser:
    def encode(self, text, add_special_tokens):
        # the adapter must ask for content tokens only
        assert add_special_tokens is False
        return text.split()


def test_hf_adapter_counts_content_tokens():
    adapter = HFAdapter("fake/model", "fake", "fake")
    adapter._tok = _StubHFTokeniser()  # bypass the real download
    assert adapter.count("one two three") == 3


def test_tiktoken_known_count():
    adapter = _require(TiktokenAdapter("cl100k_base"))
    # the canonical tiktoken example: 6 tokens in cl100k_base
    assert adapter.count("tiktoken is great!") == 6


def test_tiktoken_empty_string_is_zero():
    adapter = _require(TiktokenAdapter("cl100k_base"))
    assert adapter.count("") == 0


def test_gpt_tokenisers_all_produce_counts():
    for adapter in gpt_tokenisers():
        _require(adapter)
        assert adapter.count("hello") >= 1
