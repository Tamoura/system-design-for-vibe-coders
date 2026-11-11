#!/usr/bin/env python3
"""Run the four content checks in scripts/qa/ one after another and summarise.

Every check runs even when an earlier one fails, so one run shows everything that needs fixing.

usage: python3 scripts/qa/run_all.py        (or: npm run qa)
exit status: 0 when all four pass, 1 otherwise.
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKS = [
    ("Arabic lesson checkers", "check_ar_all.py"),
    ("Answer-cue audit", "quiz_cues.py"),
    ("Arabic rules", "arabic_rules.py"),
    ("Claims lint", "claims_lint.py"),
]


def main() -> int:
    results = []
    for title, script in CHECKS:
        print(f"\n===== {title} (scripts/qa/{script}) =====", flush=True)
        start = time.monotonic()
        code = subprocess.run([sys.executable, str(ROOT / "scripts" / "qa" / script)], cwd=ROOT).returncode
        results.append((title, script, code, time.monotonic() - start))
    print("\n===== Summary =====")
    for title, script, code, secs in results:
        print(f"{'✓' if code == 0 else '✗'} {title:<24} scripts/qa/{script:<16} {secs:5.1f}s")
    failed = [r for r in results if r[2] != 0]
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
