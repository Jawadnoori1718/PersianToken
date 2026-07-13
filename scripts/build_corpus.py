"""Build the parallel English/Persian corpus from FLORES+.

I keep the big corpus out of the repo, so I fetch it here on demand. FLORES+ is
the maintained successor to FLORES-200: it is index aligned across languages, so
the English and Persian rows that share an id are translations of each other.

FLORES+ asks you to accept its terms once, so you need a free Hugging Face
account and `huggingface-cli login` before this will download. See DATA.md.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DATASET = "openlanguagedata/flores_plus"
EN_CODE = "eng_Latn"
FA_CODE = "pes_Arab"  # Western Persian in the Arabic script


def build(out_path: Path, split: str, limit: int) -> int:
    from datasets import load_dataset  # heavy dependency, so I import it here

    en = load_dataset(DATASET, EN_CODE, split=split)
    fa = load_dataset(DATASET, FA_CODE, split=split)

    en_by_id = {row["id"]: row["text"] for row in en}
    fa_by_id = {row["id"]: row["text"] for row in fa}
    shared = sorted(set(en_by_id) & set(fa_by_id))[:limit]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for sid in shared:
            row = {"id": f"flores-{sid:04d}", "en": en_by_id[sid], "fa": fa_by_id[sid]}
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return len(shared)


def main() -> None:
    p = argparse.ArgumentParser(description="Build the EN/FA corpus from FLORES+.")
    p.add_argument("--out", type=Path, default=Path("data/corpus.jsonl"))
    p.add_argument("--split", default="devtest", choices=["dev", "devtest"])
    p.add_argument("--limit", type=int, default=500)
    args = p.parse_args()

    n = build(args.out, args.split, args.limit)
    print(f"wrote {n} pairs to {args.out}")


if __name__ == "__main__":
    main()
