"""A quick by-hand sanity check.

I tokenise a couple of pairs and look at how the Persian actually gets split,
rather than trusting the counts blind. See notes/sanity_check.md for what I found.
"""

from __future__ import annotations

import tiktoken

from persiantokenbench.corpus import DATA_DIR, load_corpus

EXAMPLE_IDS = ["sample-001", "sample-011"]
WORDS = [("today", "امروز"), ("language", "زبان")]


def main() -> None:
    pairs = {p.id: p for p in load_corpus(DATA_DIR / "sample.jsonl")}
    examples = [pairs[i] for i in EXAMPLE_IDS]

    for name in ["cl100k_base", "o200k_base"]:
        enc = tiktoken.get_encoding(name)
        print(f"===== {name} =====")
        for pair in examples:
            e, f = enc.encode(pair.en), enc.encode(pair.fa)
            print(f"  EN {len(e):>2} tok | {pair.en}")
            print(f"  FA {len(f):>2} tok | {pair.fa}   -> ratio {len(f) / len(e):.2f}")
        for word_en, word_fa in WORDS:
            te, tf = enc.encode(word_en), enc.encode(word_fa)
            bpt = [len(enc.decode_single_token_bytes(t)) for t in tf]
            print(
                f"  word: {word_en!r} {len(word_en)}c -> {len(te)} tok ; "
                f"{word_fa!r} {len(word_fa)}c -> {len(tf)} tok (bytes/token {bpt})"
            )
        print()


if __name__ == "__main__":
    main()
