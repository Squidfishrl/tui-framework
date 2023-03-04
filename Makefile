SRC  = ./src
TEST = ./test

.PHONY: all
all: test lint

.PHONY: test
test:
	PYTHONPATH=. pytest ./test -vv --cov-report term --cov=./src/tui

.PHONY: lint
lint: flake8 pylint

.PHONY: flake8 
flake8:
	flake8 $(TEST) $(SRC) --per-file-ignore $(TEST)/test_area.py,$(TEST)/test_label.py:W293,W291

.PHONY: pylint
pylint:
	pylint $(TEST) --disable=R0801
	pylint $(SRC) --disable=C0103
