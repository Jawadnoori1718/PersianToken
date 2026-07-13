# PersianTokenBench

**Token Tariffs**: measuring the tax Persian speakers quietly pay per token.

## What this is

I'm measuring how much more it costs to process Persian (Farsi) text than
English, purely at the tokeniser level. Language models charge and compute per
token. If the same meaning turns into far more tokens in Persian than in
English, then Persian speakers pay more, wait longer, and hit context limits
sooner for identical content. I want to measure that gap precisely and turn it
into real numbers: extra cost, and lost context.

This is a local measurement project. It does not call any paid model APIs. Every
tokeniser here runs locally and for free, so anyone can reproduce the numbers
without a bill.

## Why it matters

Prices and context windows are quoted in tokens, not in words or in meaning.
That quietly favours English, because most tokenisers learned from mostly
English text and tend to split other scripts into more pieces. Persian uses the
Arabic script, reads right to left, joins its letters, and often gets broken
into many small tokens. So a Persian sentence and its English translation can
carry the same meaning at very different token costs.

I call this the token tariff: a surcharge you pay per token simply for writing in
Persian. This project puts a number on it.

## What I measure

- The **token inflation ratio**: Persian tokens divided by English tokens for
  the same sentence. I report it per sentence and in aggregate, with proper
  summary statistics and bootstrap confidence intervals, because the
  per-sentence ratios are skewed.
- The **cost gap**: given a price per token, how much extra a Persian speaker
  pays for the same content.
- The **context gap**: given a context window, how much less Persian actually
  fits, measured in English-equivalent meaning.

## Tokenisers

I run several tokenisers so the finding does not rest on any one vendor:

- The GPT family via `tiktoken` (cl100k_base and o200k_base).
- Open models via Hugging Face: Llama 3, Qwen2.5, Mistral, Gemma, and a
  multilingual model (Aya or BLOOM) as a contrast.

Claude's exact tokeniser is not public, so I will not fake counts for it. I say
plainly how I handle that as the code for the tokeniser layer lands.

## Method, briefly

1. Take a small, openly licensed parallel corpus of English and Persian.
2. Tokenise every sentence with each tokeniser and record the counts.
3. Compute the inflation ratio per sentence and in aggregate, with confidence
   intervals.
4. Translate the ratio into cost and context consequences.
5. Produce figures and a short, honest written summary.

Every number is reproducible from the raw data with one command.

## Status

Work in progress. I'm building the repository up in small steps: the data
first, then the tokeniser layer, then the measurement, then the real cost and
context impact, then the write-up. Results, figures, and a quickstart will land
as those pieces go in.
