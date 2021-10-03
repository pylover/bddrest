PIP = pip
TEST_DIR = tests
PRJ = bddrest
PYTEST_FLAGS = -v


.PHONY: test
test:
	pytest $(PYTEST_FLAGS) $(TEST_DIR)


.PHONY: cover
cover:
	pytest $(PYTEST_FLAGS) --cov=$(PRJ) $(TEST_DIR)


.PHONY: lint
lint:
	flake8


.PHONY: env
env:
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .


.PHONY: sdist
sdist:
	python3 setup.py sdist


.PHONY: bdist
bdist:
	python3 setup.py bdist_egg


.PHONY: dist
dist: sdist bdist
