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
pre-commit:
	@python scripts/pre-commit.py

.PHONY: serve
serve:
	python src/serve.py

.PHONY: serve-ec2
serve-ec2:
	docker kill game || true
	docker run --name game --rm -v $$(pwd):/game --network host python:3.10 python /game/src/serve.py

.PHONY: connect
connect:
	python src/connect.py

.PHONY: create-server-env
create-server-env:
	sudo yum update -y
	# sudo yum groupinstall "Development Tools" -y
	# sudo yum erase openssl-devel -y
	# sudo yum install openssl11 openssl11-devel  libffi-devel bzip2-devel wget -y
	sudo yum install docker -y
	sudo systemctl start docker.service
	sudo usermod -a -G docker ec2-user
	python3 -m venv .venv
	echo 'Do this: source .venv/bin/activate'