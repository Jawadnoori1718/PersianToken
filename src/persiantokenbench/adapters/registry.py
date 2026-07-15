"""The set of tokenisers I measure, and a loader that skips any I can't run.

Some Hugging Face tokenisers are gated (Llama, Mistral, Gemma) and need a
`huggingface-cli login` plus accepting the model's terms once. Rather than sink
the whole run, I skip a tokeniser that will not load and carry on with the rest.
"""

from __future__ import annotations

import warnings

from persiantokenbench.adapters.base import Tokeniser
from persiantokenbench.adapters.hf_adapter import HFAdapter
from persiantokenbench.adapters.tiktoken_adapter import gpt_tokenisers

# model id, label, family. Llama, Mistral and Gemma are gated: they need a
# huggingface-cli login and accepting the model's terms once. Qwen and BLOOM are
# open. BLOOM is here as a deliberately multilingual contrast.
HF_MODELS = [
    ("meta-llama/Meta-Llama-3-8B", "llama-3", "llama"),
    ("Qwen/Qwen2.5-7B", "qwen2.5", "qwen"),
    ("mistralai/Mistral-7B-v0.1", "mistral", "mistral"),
    ("google/gemma-2-9b", "gemma-2", "gemma"),
    ("bigscience/bloom", "bloom", "bloom"),
]


def all_tokenisers() -> list[Tokeniser]:
    hf = [HFAdapter(model_id, name, family) for model_id, name, family in HF_MODELS]
    return [*gpt_tokenisers(), *hf]


def load_available(tokenisers: list[Tokeniser] | None = None) -> list[Tokeniser]:
    tokenisers = tokenisers if tokenisers is not None else all_tokenisers()
    ready: list[Tokeniser] = []
    for tok in tokenisers:
        try:
            tok.count("ok")  # force the load; a failure here should skip, not crash
        except Exception as e:
            warnings.warn(f"skipping {tok.name}: {e}", stacklevel=2)
            continue
        ready.append(tok)
    return ready
