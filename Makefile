SRC  = ./src
TEST = ./test

.PHONY: all
all: test lint

.PHONY: test
test:
	PYTHONPATH=. pytest ./test -vv

.PHONY: lint
lint: flake8 pylint

.PHONY: flake8 
flake8:
	flake8 $(TEST) $(SRC) --per-file-ignore $(TEST)/test_area.py:W293,W291

.PHONY: pylint
pylint:
	pylint $(TEST) --disable=R0801
	pylint $(SRC) 
