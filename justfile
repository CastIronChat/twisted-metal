set windows-shell := ["C:/Program Files/Git/bin/bash.exe", "-c"]

# List commands
default:
    just --list

formatSources := "src"

# Reformat all code
fmt:
    python -m black {{formatSources}}

alias check := lint

# Check code formatting
lint:
    python -m black --check {{formatSources}}
