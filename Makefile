HERE = $(shell readlink -f `dirname .`)
PKG = $(shell basename $(HERE))
VENVPATH := $(HOME)/.virtualenvs/$(PKG)
PYTEST_FLAGS = -v
TEST_DIR = tests
PY = $(VENVPATH)/bin/python3
PIP = $(VENVPATH)/bin/pip3
PYTEST = $(VENVPATH)/bin/pytest
COVERAGE = $(VENVPATH)/bin/coverage
FLAKE8 = $(VENVPATH)/bin/flake8
TWINE = $(VENVPATH)/bin/twine


ifdef F
  TEST_FILTER = $(F)
else
  TEST_FILTER = $(TEST_DIR)
endif


.PHONY: test
test:
	$(PYTEST) $(PYTEST_FLAGS) $(TEST_FILTER)


.PHONY: cover
cover:
	$(PYTEST) $(PYTEST_FLAGS) --cov=$(PKG) $(TEST_FILTER)


.PHONY: cover-html
cover-html: cover
	$(COVERAGE) html
	@echo "Browse htmlcov/index.html for the covearge report"


.PHONY: lint
lint:
	$(FLAKE8)


.PHONY: venv
venv:
	python3 -m venv $(VENV)


.PHONY: env
env:
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .


.PHONY: venv-delete
venv-delete: clean
	rm -rf $(VENV)


.PHONY: sdist
sdist:
	$(PY) -m build --sdist


.PHONY: bdist
wheel:
	$(PY) -m build --wheel


.PHONY: dist
dist: sdist wheel


.PHONY: pypi
pypi: dist
	$(TWINE) upload dist/*.gz dist/*.whl


.PHONY: clean
clean:
	rm -rf dist/*
	rm -rf build/*
