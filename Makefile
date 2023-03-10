# system python interpreter. used only to create virtual environment
PY = python3
VENV = venv
BIN=$(VENV)/bin

all: lint unit_tests pkg

$(VENV): Makefile requirements.txt requirements-dev.txt pyproject.toml setup.py
	$(PY) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install --upgrade -r requirements.txt
	$(BIN)/pip install --upgrade -r requirements-dev.txt
	$(BIN)/pip install -e .
	touch $(VENV)

kentik_api/generated: $(VENV)
	$(BIN)/python setup.py grpc_stubs

.PHONY: unit_tests
unit_tests: kentik_api/generated
	$(BIN)/python setup.py pytest

.PHONY: lint
lint: $(VENV)
	$(BIN)/python setup.py format
	$(BIN)/python setup.py mypy

.PHONY: pkg
pkg: lint unit_tests kentik_api/generated
	$(BIN)/python -m build

clean:
	rm -rf $(VENV)
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
	find . -type d -name *.egg-info | xargs rm -rf
	rm -rf dist .mypy_cache .pytest_cache kentik_api/generated
