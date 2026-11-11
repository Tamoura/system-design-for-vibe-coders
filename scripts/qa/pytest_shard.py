#!/usr/bin/env python3
"""Print the pytest node ids of one shard of a test suite, one per line, for a CI matrix.

Collects the suite in the current directory (pytest --collect-only -q, with the suite's own pytest.ini)
and deals the test ids out round-robin, so every shard gets a similar mix of slow and fast tests.

usage (from the kit's folder):
  python ../../scripts/qa/pytest_shard.py SHARD TOTAL > shard.txt     # SHARD counts from 1
  python -m pytest -n auto @shard.txt                                  # pytest reads arguments from the file

exit status: 0, or the collection's exit status when collection fails (its output goes to stderr).
"""
from __future__ import annotations

import subprocess
import sys


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    shard, total = int(sys.argv[1]), int(sys.argv[2])
    if not 1 <= shard <= total:
        print(f"shard must be between 1 and {total}", file=sys.stderr)
        return 2
    proc = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:randomly"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stdout + proc.stderr)
        return proc.returncode
    # The node ids come first, one per line, and end at the first blank line. Anything after it (the
    # "N tests collected" line, a warnings summary that repeats node ids or quotes "::") is not a test id.
    ids = []
    for line in proc.stdout.splitlines():
        if not line.strip():
            break
        if "::" in line:
            ids.append(line.strip())
    mine = ids[shard - 1::total]
    print("\n".join(mine))
    print(f"shard {shard} of {total}: {len(mine)} of {len(ids)} tests", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
