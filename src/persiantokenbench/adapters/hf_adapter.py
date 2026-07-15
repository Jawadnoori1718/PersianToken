"""Open-model tokenisers via Hugging Face.

Same interface as the GPT ones. I load the tokeniser lazily, and I count content
tokens only (no BOS/EOS) so the number lines up with how tiktoken counts.
"""

from __future__ import annotations

from persiantokenbench.adapters.base import Tokeniser


class HFAdapter(Tokeniser):
    def __init__(self, model_id: str, name: str, family: str) -> None:
        self.model_id = model_id
        self.name = name
        self.family = family
        self._tok = None  # loaded lazily; the download only happens on first use

    def _tokeniser(self):
        if self._tok is None:
            from transformers import AutoTokenizer

            self._tok = AutoTokenizer.from_pretrained(self.model_id)
        return self._tok

    def count(self, text: str) -> int:
        # No special tokens: I want the content length, the same basis as tiktoken.
        return len(self._tokeniser().encode(text, add_special_tokens=False))
