"""Tiny deterministic secret scan, standing in for the Session 2 gate.

Scans tracked files for strings shaped like credentials and exits 1 on a hit.
On a real repo use a maintained scanner such as gitleaks; this one is short
enough to read on a slide.

    python scripts/secret_scan.py
"""
from __future__ import annotations

import re
import subprocess
import sys

PATTERNS = {
    "Google API key": re.compile(r"AIza[0-9A-Za-z_\-]{35}"),
    "GitHub token": re.compile(r"gh[pousr]_[0-9A-Za-z]{36,}"),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "Private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "Stripe-style key": re.compile(r"sk_(?:live|test)_[0-9A-Za-z]{10,}"),
    "Hardcoded secret": re.compile(
        r"(?i)\b(?:secret|password|passwd|api_?key|token)\w*\s*=\s*[\"'][^\"'\s]{12,}[\"']"
    ),
}
SKIP = ("scripts/secret_scan.py", "tests/test_scripts.py")


def scan(paths: list[str]) -> list[str]:
    hits = []
    for path in paths:
        if path in SKIP:
            continue
        try:
            with open(path, encoding="utf-8") as handle:
                for number, line in enumerate(handle, 1):
                    for name, pattern in PATTERNS.items():
                        if pattern.search(line):
                            hits.append(f"{path}:{number}: {name}")
        except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
            continue
    return hits


if __name__ == "__main__":
    tracked = subprocess.run(
        ["git", "ls-files"], check=True, capture_output=True, text=True
    ).stdout.splitlines()
    found = scan(tracked)
    for hit in found:
        print(f"::error::{hit}")
    print(f"secret scan: {len(tracked)} files, {len(found)} hit(s)")
    sys.exit(1 if found else 0)
