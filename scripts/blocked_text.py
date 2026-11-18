#!/usr/bin/env python3
"""Load scripts/blocked-text.b64: text this library must not publish, and the agentic rewrite rules.

The file holds base64-encoded JSON so that the real organisation's name and the source-specific phrases do
not appear in plain text in the public repository. That is obfuscation, not secrecy: anyone can decode it.

    python3 scripts/blocked_text.py --blocked   print the phrases sync-agentic.sh refuses to publish
    python3 scripts/blocked_text.py --show      print the decoded JSON (for maintainers)

From Python: `from blocked_text import load` (scripts/ on sys.path) returns the decoded dict with keys
name_regex, lint_patterns, lint_prefilter, blocked and rules. scripts/agentic-neutral.mjs reads the same file.
"""
from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

FILE = Path(__file__).resolve().parent / "blocked-text.b64"


def load() -> dict:
    text = "".join(line for line in FILE.read_text(encoding="utf-8").splitlines() if not line.startswith("#"))
    return json.loads(base64.b64decode(text).decode("utf-8"))


def main() -> int:
    data = load()
    if "--blocked" in sys.argv:
        print("\n".join(data["blocked"]))
    elif "--show" in sys.argv:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
