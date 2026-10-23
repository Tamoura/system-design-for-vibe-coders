#!/usr/bin/env python3
"""Check that lesson code blocks that show a kit file are byte-identical to that file.

A lesson block counts as showing a kit file when its first line is a comment naming the
file's path relative to ``ainative/ailab/``, for example::

    ```python
    # ailab/labs/m08_harden/assets/guard_skeleton.py
    ...
    ```

The block (first line included) must equal the file, which therefore starts with the same
comment line. The script also checks the other direction for the kit itself: a kit file
whose first line names a path must live at that path.

usage (from ainative/):   python3 ailab/check_blocks.py [modules_dir] [--english-only]
exit status: 0 when everything matches, 1 when there are problems.
Blocks of formats without comments (JSON, Markdown) are not byte-checked; the lesson names
the path in a sentence instead (see AUTHORING.md, rule 8).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent  # ainative/ailab
PATH_COMMENT = re.compile(r"^#\s+(ailab/[\w./-]+)\s*$")
FENCE = re.compile(r"```(\w*)[^\n]*\n(.*?)```", flags=re.S)
KIT_SUFFIXES = {".py", ".sh", ".yml", ".yaml", ".toml", ".cfg", ".ini"}
SKIP_DIRS = {"__pycache__", ".git", ".pytest_cache", "node_modules"}


def kit_file(rel: str) -> Path:
    """``ailab/labs/x.py`` -> ainative/ailab/ailab/labs/x.py (the path is relative to ainative/ailab/)."""
    return ROOT / rel


def check_lessons(modules: Path, english_only: bool) -> tuple[int, int, set[str]]:
    ok = bad = 0
    seen: set[str] = set()
    for md in sorted(modules.glob("*.md")):
        if english_only and md.name.endswith(".ar.md"):
            continue
        text = md.read_text(encoding="utf-8")
        for match in FENCE.finditer(text):
            body = match.group(2)
            found = PATH_COMMENT.match(body.split("\n", 1)[0])
            if not found:
                continue
            rel = found.group(1)
            seen.add(rel)
            target = kit_file(rel)
            if not target.is_file():
                print(f"x {md.name}: {rel} does not exist")
                bad += 1
            elif target.read_text(encoding="utf-8").rstrip("\n") != body.rstrip("\n"):
                print(f"x {md.name}: the block for {rel} differs from the file")
                bad += 1
            else:
                ok += 1
    return ok, bad, seen


def check_kit_files() -> tuple[int, set[str]]:
    """Kit files that declare a path on their first line must be at that path. Returns (problems, declared)."""
    bad = 0
    declared: set[str] = set()
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in KIT_SUFFIXES or SKIP_DIRS & set(path.parts):
            continue
        try:
            first = path.read_text(encoding="utf-8").split("\n", 1)[0]
        except UnicodeDecodeError:
            continue
        found = PATH_COMMENT.match(first)
        if not found:
            continue
        declared.add(found.group(1))
        actual = path.relative_to(ROOT).as_posix()
        if found.group(1) != actual:
            print(f"x {actual}: its first line says {found.group(1)}")
            bad += 1
    return bad, declared


def main(argv: list[str]) -> int:
    english_only = "--english-only" in argv
    args = [a for a in argv if not a.startswith("--")]
    modules = Path(args[0]) if args else ROOT.parent / "modules"
    ok, bad, seen = check_lessons(modules, english_only)
    kit_bad, declared = check_kit_files()
    unused = sorted(declared - seen)
    line = f"{ok} lesson blocks match their kit files, {bad + kit_bad} problems"
    line += f"; {len(unused)} kit files that name their path are not shown in any lesson"
    print(line + (f": {unused[:5]}" if unused else ""))
    return 1 if bad or kit_bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
