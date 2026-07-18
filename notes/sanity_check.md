# A quick sanity check by hand

Before trusting the aggregate numbers, I tokenised a couple of pairs by hand and
looked at how the Persian actually gets split. The counts below come straight
from tiktoken, and you can reproduce them with `scripts/sanity_check.py`.

## Two sentence pairs

With cl100k_base (the older GPT-4 encoding):

| sentence | english | persian | ratio |
| --- | --- | --- | --- |
| The weather is very cold today. | 7 | 15 | 2.14 |
| Learning a new language takes time and patience. | 9 | 31 | 3.44 |

With o200k_base (the newer GPT-4o encoding):

| sentence | english | persian | ratio |
| --- | --- | --- | --- |
| The weather is very cold today. | 7 | 7 | 1.00 |
| Learning a new language takes time and patience. | 9 | 14 | 1.56 |

## Zooming into single words

The clearest way to see what is going on is one word at a time.

| word | characters | cl100k tokens | o200k tokens |
| --- | --- | --- | --- |
| today | 5 | 1 | 1 |
| امروز (today) | 5 | 3 | 2 |
| language | 8 | 1 | 1 |
| زبان (language) | 4 | 3 | 2 |

A whole English word like "language" is a single token. Its Persian equivalent,
which is actually shorter on the page, becomes two or three.

## What surprised me

- The Persian tokens are byte fragments, not word pieces. Each Persian letter is
  two bytes in UTF-8, and the tokeniser chops the word into pieces of a few bytes
  each. For "امروز" under cl100k the three tokens cover 4, 4 and 2 bytes. English
  is packed into learned word pieces instead. So the tokeniser has learned
  English words, but sees Persian as close to raw bytes.
- The tokeniser matters far more than I expected. On the very same first sentence,
  cl100k charges 15 Persian tokens and o200k charges 7. o200k even lands on a
  ratio of exactly 1.00 there, the same count as English. A newer, more
  multilingual vocabulary closes a lot of the gap on its own.
- These two examples line up with the corpus-wide table (cl100k near 3.0, o200k
  near 1.45), which is reassuring. But two sentences are only two sentences. The
  point of this check is to understand the mechanism, not to replace the wider
  numbers.

## Reproduce

```
python scripts/sanity_check.py
```
