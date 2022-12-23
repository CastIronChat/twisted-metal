.PHONY: default
default:

formatSources = "src"

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

# Run to install a git pre-commit hook.
# If installed, committing will error-out when code doesn't
# match the formatter.  `make fmt` or Ctrl+Shift+B can fix this.
.PHONY: install-git-hooks
install-git-hooks:
	python scripts/install-git-hooks.py

# Uninstall the pre-commit hook
.PHONY: uninstall-git-hooks
uninstall-git-hooks:
	python scripts/uninstall-git-hooks.py

# This is run by the pre-commit hook to verify formatting
.PHONY: pre-commit
pre-commit: check
