#!/usr/bin/env python3
"""Run every course's Arabic checker on every lesson pair and summarise.

Each course with Arabic lessons has <course>/check_ar.py, which compares one Arabic lesson file with its
English source (headings, quiz letters, details blocks, code and Mermaid blocks, links, share of Arabic
script). This script finds every <course>/modules/NN-*.md, runs the course's checker on it and its
.ar.md twin, and prints one line per course. An English lesson without an Arabic twin also counts as a
failure.

usage: python3 scripts/qa/check_ar_all.py [course ...]     (default: every course with a check_ar.py)
exit status: 0 when every pair passes, 1 otherwise.
"""
from __future__ import annotations

import concurrent.futures
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def pairs(course: Path) -> list[tuple[Path, Path]]:
    out = []
    for en in sorted((course / "modules").glob("[0-9][0-9]-*.md")):
        if en.name.endswith(".ar.md"):
            continue
        out.append((en, en.with_name(en.name[:-3] + ".ar.md")))
    return out


def run(checker: Path, en: Path, ar: Path) -> tuple[bool, str]:
    if not ar.exists():
        return False, f"✗ {ar.relative_to(ROOT)}: missing (English source {en.relative_to(ROOT)})"
    proc = subprocess.run([sys.executable, str(checker), str(en.relative_to(ROOT)), str(ar.relative_to(ROOT))],
                          cwd=ROOT, capture_output=True, text=True)
    return proc.returncode == 0, (proc.stdout + proc.stderr).strip()


def main() -> int:
    wanted = set(sys.argv[1:])
    courses = sorted(p.parent for p in ROOT.glob("*/check_ar.py") if not wanted or p.parent.name in wanted)
    if not courses:
        print("no course has a check_ar.py" + (f" among {sorted(wanted)}" if wanted else ""))
        return 1
    total = failed = 0
    failures: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for course in courses:
            checker = course / "check_ar.py"
            jobs = [(en, ar, pool.submit(run, checker, en, ar)) for en, ar in pairs(course)]
            ok = 0
            for en, ar, job in jobs:
                passed, text = job.result()
                total += 1
                if passed:
                    ok += 1
                else:
                    failed += 1
                    failures.append(text)
            mark = "✓" if ok == len(jobs) else "✗"
            print(f"{mark} {course.name:<10} {ok}/{len(jobs)} Arabic lessons pass {course.name}/check_ar.py")
    if failures:
        print("\nFailures:")
        for text in failures:
            print(text)
        print(f"\n✗ {failed} of {total} Arabic lesson files fail their course checker")
        return 1
    print(f"\n✓ all {total} Arabic lesson files pass ({len(courses)} courses)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
