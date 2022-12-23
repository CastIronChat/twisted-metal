from __future__ import annotations

f = open(".git/hooks/pre-commit", "w")
f.write("#!/usr/bin/env bash\n")
f.write("make pre-commit")
f.close()
