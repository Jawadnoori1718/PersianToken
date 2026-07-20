# Findings

## The headline

For the same meaning, Persian costs more tokens than English on every tokeniser I
tested. The tariff runs from about 1.45 times as many tokens at best to about
3.93 times at worst. Even the best case is a 45 per cent surcharge on Persian;
the worst case nearly quadruples the bill. No tokeniser here escapes it.

These numbers come from a sample of 45 English and Persian sentence pairs, which
is small but enough to show the effect plainly. The pipeline rebuilds everything
from raw data with one command, so the larger FLORES-200 run is a rebuild away. I
report the sample I actually ran rather than a number I did not.

## The numbers

Persian tokens per English token, worst to best:

| tokeniser | ratio | 95% CI |
| --- | --- | --- |
| mistral | 3.93 | 3.71 to 4.18 |
| gpt-4 (cl100k_base) | 3.00 | 2.81 to 3.19 |
| qwen2.5 | 2.40 | 2.24 to 2.57 |
| bloom | 1.61 | 1.49 to 1.74 |
| gpt-4o (o200k_base) | 1.45 | 1.37 to 1.54 |

The confidence intervals are tight and mostly do not overlap, so the ranking is
real rather than noise. The one honest caveat is that bloom and o200k sit close,
and I would not claim a firm winner between them.

## What it costs

At a flat three dollars per million tokens, for content that is one million
English tokens, Persian pays this much extra for exactly the same meaning:

| tokeniser | extra cost | extra |
| --- | --- | --- |
| mistral | $8.80 | +293% |
| gpt-4 (cl100k_base) | $5.99 | +200% |
| qwen2.5 | $4.20 | +140% |
| bloom | $1.84 | +61% |
| gpt-4o (o200k_base) | $1.35 | +45% |

I hold the price flat on purpose. That way the gap reflects the tokeniser, not
one vendor's price list.

## What it costs in context

A context window is quoted in tokens, so Persian fills it faster and holds less
meaning. For a 128,000 token window, this is how much English-equivalent content
actually fits in Persian:

| tokeniser | effective window | lost |
| --- | --- | --- |
| mistral | 32,530 | 75% |
| gpt-4 (cl100k_base) | 42,710 | 67% |
| qwen2.5 | 53,351 | 58% |
| bloom | 79,287 | 38% |
| gpt-4o (o200k_base) | 88,252 | 31% |

On the worst tokeniser a Persian speaker loses three quarters of the window to
the script alone.

## Why it happens

I tokenised a few sentences by hand to see the mechanism (notes/sanity_check.md).
The tokenisers have learned English word pieces, but they treat Persian as close
to raw bytes. Each Persian letter is two bytes in UTF-8, and the vocabulary chops
Persian words into a few bytes each. So a whole English word like "language" is a
single token, while its Persian equivalent, which is shorter on the page, becomes
two or three.

## What actually helps

The divide is less about old versus new and more about English-first versus
multilingual. The two tokenisers that treat Persian most fairly are gpt-4o's
o200k, built with a broader vocabulary, and bloom, which is multilingual by
design. The English-first tokenisers, cl100k and mistral, are the most expensive
for Persian.

So the tariff is not a law of nature. It is a design choice, and a bigger, more
multilingual vocabulary closes most of the gap.

## Limitations

I would rather be plain about what this does not show.

- Corpus size. The headline runs on 45 sentence pairs that I wrote and translated
  myself. That is enough to show the effect and to exercise the pipeline, but it
  is small, and it is not a standard benchmark. The confidence intervals here are
  wider than a large run would give. For firmer numbers, build the FLORES-200
  corpus and rerun; the pipeline does this from one command.

- Dialect and register. I use standard written Iranian Persian. Other varieties
  such as Dari and Tajik, and colloquial or heavily informal registers, may
  tokenise differently. My sample is everyday prose, not code, poetry, or
  technical text, all of which can shift the ratio.

- The price is a single flat knob. I hold it flat on purpose, to isolate the
  tokeniser. Real bills combine the tokeniser with each vendor's own price, so
  the cost figures show the size of the tokeniser effect, not a price comparison
  between products.

- English is the baseline, not a neutral yardstick. The tariff is measured
  against English, which is itself the favoured case. These numbers say how much
  more Persian costs than English, not how Persian compares to some neutral ideal.

- Not every tokeniser ran. Llama 3 and Gemma are gated on Hugging Face, so they
  were skipped in my run unless you log in and accept their terms. The set here
  is a sensible spread, not the whole field.

- I count content tokens only, with no special or chat tokens. Real requests add
  a handful of those. They barely move the ratio, but they do nudge the absolute
  counts.
