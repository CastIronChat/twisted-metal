.PHONY: default
default:

sources = "src"

# Reformat all code
.PHONY: fmt
fmt:
	python -m black $(sources)

check: lint

# Check code formatting
lint: lint-fmt lint-typecheck

.PHONY: lint-fmt
lint-fmt:
	python -m black --check $(sources)

.PHONY: lint-typecheck
lint-typecheck:
	python -m mypy $(sources)