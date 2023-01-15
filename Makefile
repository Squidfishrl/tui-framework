.PHONY: test
test:
	PYTHONPATH=. pytest ./test -vv

.PHONY: lint
lint:
	flake8 ./test ./src
	pylint ./test ./src
