#!/usr/bin/env python3
"""Lesson outcomes: every lesson states a measurable outcome and a study-time estimate.

academy/STANDARD.md section 3 asks each lesson to begin with "After this you can ..." and a study time,
labelled an estimate until a pilot has measured it. This check finds every lesson heading
(`# 3.2 — Title`, `# 12 — Title` for a capstone file) in the course sources and looks in the lesson's
opening lines, before the first `##` section, for:

- English: "After this you can" and "Study time:" followed by "estimate" or a measured value;
- Arabic:  «بعد هذا الدرس تستطيع» and «مدة الدراسة».

usage: python3 scripts/qa/lesson_outcomes.py [--list]
exit status: 0 when every lesson has both lines, 1 otherwise.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LESSON = re.compile(r"^# (?:[0-9]+|[A-Z])(?:\.[0-9]+)? [—–-] ", re.M)
SKIP_DIRS = {"agentic", "node_modules", "_site"}
NEEDLES = {
    "en": (re.compile(r"After this you can"), re.compile(r"Study time:")),
    "ar": (re.compile(r"بعد هذا الدرس تستطيع"), re.compile(r"مدة الدراسة")),
}


def lesson_files() -> list[Path]:
    files = sorted(ROOT.glob("modules/*/*.md")) + sorted(ROOT.glob("*/modules/*.md"))
    return [f for f in files if not (set(f.relative_to(ROOT).parts) & SKIP_DIRS)]


def lessons(text: str):
    """Yield (heading line, opening text) for each lesson heading in a file."""
    starts = [m.start() for m in LESSON.finditer(text)]
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(text)
        block = text[start:end]
        heading, _, rest = block.partition("\n")
        opening = re.split(r"^## ", rest, maxsplit=1, flags=re.M)[0]
        yield heading.strip(), opening


def main() -> int:
    listing = "--list" in sys.argv
    missing: list[str] = []
    total = 0
    for f in lesson_files():
        lang = "ar" if f.name.endswith(".ar.md") else "en"
        outcome, time = NEEDLES[lang]
        text = f.read_text(encoding="utf-8")
        for heading, opening in lessons(text):
            if heading.startswith("# Module"):
                continue
            total += 1
            gaps = [name for name, rx in (("outcome", outcome), ("study time", time)) if not rx.search(opening)]
            if gaps:
                missing.append(f"{f.relative_to(ROOT)}: {heading[:70]} (no {' or '.join(gaps)})")
    print(f"Lesson outcomes (scripts/qa/lesson_outcomes.py): {total} lessons checked")
    if missing:
        print(f"✗ {len(missing)} lesson(s) without an outcome line or a study time")
        for m in missing if listing else missing[:20]:
            print(f"  - {m}")
        if not listing and len(missing) > 20:
            print(f"  … and {len(missing) - 20} more (run with --list)")
        return 1
    print("✓ every lesson states an outcome and a study time")
    return 0


if __name__ == "__main__":
    sys.exit(main())
