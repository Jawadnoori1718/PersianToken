"""The tokeniser adapter interface.

Every backend (tiktoken, Hugging Face, and so on) implements this one small
interface, so the rest of the code never imports a tokeniser library directly.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Tokeniser(ABC):
    name: str
    family: str
    # approximate is True when I can't run the real tokeniser and the count is a stand-in.
    approximate: bool = False

    @abstractmethod
    def count(self, text: str) -> int:
        """Number of tokens this tokeniser turns `text` into."""
