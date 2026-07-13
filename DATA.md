# Data

Two things live here: a small sample I wrote by hand, and a script that builds
the full corpus from FLORES+.

## The hand-authored sample (`data/sample.jsonl`)

I wrote these 45 English and Persian sentence pairs myself so the pipeline runs
the moment you clone the repo, with no download and no account. They are
everyday sentences, translated by me, and they carry the usual Persian
typography (the zero width non-joiner, joined letters, and so on) so the
tokenisers see realistic text.

Treat the sample as illustrative. It is small and it is mine, not drawn from a
standard benchmark, so I do not lean on it for the headline number. It is here
to make the code runnable and testable out of the box.

- Licence: released under the project's MIT licence, same as the code.
- Format: one JSON object per line, with the fields `id`, `en`, `fa`.

## The full corpus (FLORES+)

For the headline numbers I use FLORES+, the openly maintained successor to
Meta's FLORES-200. It is a genuinely parallel evaluation set: the English and
Persian sentences that share an id are translations of one another, so the
pairing is trustworthy.

- Source: `openlanguagedata/flores_plus` on the Hugging Face Hub.
- Languages I use: English (`eng_Latn`) and Western Persian (`pes_Arab`).
- Split: `devtest` by default (1012 sentences), of which I take the first 500.
- Licence: CC BY-SA 4.0. That means attribution and share alike, so I do not
  commit the FLORES sentences into this repository. I keep the repo's own data
  under MIT and build the FLORES corpus locally instead.

### Building it

FLORES+ asks you to accept its terms once, so you need a free Hugging Face
account:

```bash
pip install -e ".[data]"
huggingface-cli login
python scripts/build_corpus.py --limit 500
```

That writes `data/corpus.jsonl` (which is gitignored). Everything downstream
uses `data/corpus.jsonl` when it is present, and falls back to
`data/sample.jsonl` when it is not.

## Attribution

FLORES+ is maintained by the Open Language Data Initiative and derives from
Meta's No Language Left Behind work. If you use the FLORES corpus, cite
FLORES-200 and FLORES+ in line with their licence.
