.PHONY: default
default:

formatSources = "src"

# Reformat all code
.PHONY: fmt
fmt:
	python.exe -m isort .
	python.exe -m black $(formatSources)

check: lint

# Check code formatting
.PHONY: lint
lint:
	python.exe -m isort --check .
	python.exe -m black --check $(formatSources)
