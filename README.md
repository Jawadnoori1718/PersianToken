# PersianTokenBench

I'm measuring how much more it costs to process Persian (Farsi) text than
English, purely at the tokeniser level. Language models charge and compute per
token, so if the same meaning turns into far more tokens in Persian, Persian
speakers pay more, wait longer, and run out of context sooner.

This is a local measurement project. It does not call any paid model APIs — the
tokenisers all run locally and for free.

Work in progress. Fuller notes, method, and results to follow.
