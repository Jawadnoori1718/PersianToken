"""GPT tokenisers via tiktoken.

I wire up both encodings that matter in practice: cl100k_base (GPT-3.5 and
GPT-4) and o200k_base (GPT-4o and the o-series). tiktoken runs locally and free.
"""

from __future__ import annotations

from persiantokenbench.adapters.base import Tokeniser

# encoding -> the label I show, tagged with a representative model
ENCODINGS = {
    "cl100k_base": "gpt-4 cl100k_base",
    "o200k_base": "gpt-4o o200k_base",
}


class TiktokenAdapter(Tokeniser):
    family = "gpt"

    def __init__(self, encoding: str, name: str | None = None) -> None:
        self.encoding = encoding
        self.name = name or f"gpt {encoding}"
        self._enc = None  # loaded lazily so importing this module stays cheap

    def _encoder(self):
        if self._enc is None:
            import tiktoken

            self._enc = tiktoken.get_encoding(self.encoding)
        return self._enc

    def count(self, text: str) -> int:
        return len(self._encoder().encode(text))


def gpt_tokenisers() -> list[TiktokenAdapter]:
    return [TiktokenAdapter(enc, name=label) for enc, label in ENCODINGS.items()]
