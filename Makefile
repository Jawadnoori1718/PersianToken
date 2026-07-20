# I run everything through PYTHONPATH=src so it works even when the editable
# install link drops (a known Homebrew venv quirk). Override PYTHON to point at a
# different interpreter, e.g. make all PYTHON=python.
PYTHON ?= .venv/bin/python
RUFF ?= .venv/bin/ruff
PTB := PYTHONPATH=src $(PYTHON) -m persiantokenbench.cli

.PHONY: all install relink corpus tokenise metrics cost context plot test lint format clean

all:
	$(PTB) tokenise
	$(PTB) metrics
	$(PTB) cost
	$(PTB) context
	$(PTB) plot

install:
	$(PYTHON) -m pip install -e ".[dev]"

relink:
	$(PYTHON) -m pip install -e . --no-deps

corpus:
	PYTHONPATH=src $(PYTHON) scripts/build_corpus.py --limit 500

tokenise:
	$(PTB) tokenise

metrics:
	$(PTB) metrics

cost:
	$(PTB) cost

context:
	$(PTB) context

plot:
	$(PTB) plot

test:
	PYTHONPATH=src $(PYTHON) -m pytest -q

lint:
	$(RUFF) check .
	$(RUFF) format --check .

format:
	$(RUFF) format .

clean:
	rm -rf .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
