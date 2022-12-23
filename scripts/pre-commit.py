from __future__ import annotations

import subprocess

result = subprocess.run("make check", capture_output=True)
if result.returncode != 0:
    print(
        "Pre-commit hook found unformatted code.  Running the formatter should fix it. Ctrl+Shift+B in VSCode, or run 'make fmt' in your terminal."
    )
    print("")
    print(result.stdout.decode("utf-8"))
    print(result.stderr.decode("utf-8"))
    exit(result.returncode)
