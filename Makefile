.PHONY: default
default:

formatSources = "src"

.PHONY: install
install:
	pip install -r requirements.txt

# Reformat all code
.PHONY: fmt
fmt:
	python -m isort .
	python -m black $(formatSources)

check: lint

# Check code formatting
.PHONY: lint
lint:
	python -m isort --check .
	python -m black --check $(formatSources)

.PHONY: build
build:
	python -m nuitka --standalone src/main.py
