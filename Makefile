.PHONY: default
default:

formatSources = "src"

# Reformat all code
.PHONY: fmt
fmt:
	python -m black $(formatSources)

check: lint

# Check code formatting
.PHONY: lint
lint:
	python.exe -m black --check $(formatSources)
