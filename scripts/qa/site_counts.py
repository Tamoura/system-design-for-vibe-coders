#!/usr/bin/env python3
"""Site counts: the published module and lesson counts must match academy/catalogue.json.

The catalogue is the one source for how many courses, modules and lessons the library has.
This check fails when a hand-written page disagrees with it:

- landing.html: each course card's first two numbers (modules, lessons);
- about/index.html and about/index.ar.html: the number of courses and the total lesson count;
- each course's `assurance` level (academy/STANDARD.md section 5): a level above "draft" needs its sign-off
  records in academy/reviews/<course>/.

usage: python3 scripts/qa/site_counts.py
exit status: 0 when every count matches, 1 otherwise.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CARD = re.compile(r'<article class="course[^"]*" data-course="([a-z0-9-]+)".*?</article>', re.S)
META_NUMBERS = re.compile(r'<div class="meta">(.*?)</div>', re.S)
BOLD = re.compile(r"<b>(\d+)</b>")


def main() -> int:
    catalogue = json.loads((ROOT / "academy" / "catalogue.json").read_text(encoding="utf-8"))
    courses = {c["id"]: c for c in catalogue["courses"]}
    problems: list[str] = []

    landing = (ROOT / "landing.html").read_text(encoding="utf-8")
    seen = set()
    for match in CARD.finditer(landing):
        cid = match.group(1)
        seen.add(cid)
        if cid not in courses:
            problems.append(f"landing.html: card '{cid}' is not in academy/catalogue.json")
            continue
        meta = META_NUMBERS.search(match.group(0))
        numbers = [int(n) for n in BOLD.findall(meta.group(1))] if meta else []
        if len(numbers) < 2:
            problems.append(f"landing.html: card '{cid}' has no modules/lessons numbers")
            continue
        want = (courses[cid]["modules"], courses[cid]["lessons"])
        if tuple(numbers[:2]) != want:
            problems.append(f"landing.html: card '{cid}' shows {numbers[0]} modules / {numbers[1]} lessons; "
                            f"catalogue says {want[0]} / {want[1]}")
    for cid in courses:
        if cid not in seen:
            problems.append(f"landing.html: no card for catalogue course '{cid}'")

    levels = ["draft", "technically-reviewed", "assessment-validated", "pilot-tested", "professionally-validated"]
    needs = {1: "subject-expert", 2: "assessment-lead", 3: "pilot", 4: "assessor"}
    for cid, c in courses.items():
        level = c.get("assurance")
        if level not in levels:
            problems.append(f"academy/catalogue.json: course '{cid}' has assurance {level!r}; expected one of {levels}")
            continue
        for rank in range(1, levels.index(level) + 1):
            role = needs[rank]
            if not list((ROOT / "academy" / "reviews" / cid).glob(f"{role}-*.md")):
                problems.append(f"academy/catalogue.json: course '{cid}' claims '{level}' but academy/reviews/{cid}/ "
                                f"has no {role}-*.md record")

    total = sum(c["lessons"] for c in courses.values())
    count = len(courses)
    for page in ("about/index.html", "about/index.ar.html"):
        text = (ROOT / page).read_text(encoding="utf-8")
        if not re.search(rf"\b{total}\b", text):
            problems.append(f"{page}: does not state the catalogue's lesson total ({total})")
        if not re.search(rf"\b{count}\b", text):
            problems.append(f"{page}: does not state the catalogue's course count ({count})")

    print(f"Site counts (scripts/qa/site_counts.py): {count} courses, {total} lessons in the catalogue")
    for p in problems:
        print(f"  ✗ {p}")
    if problems:
        print("Fix the page, or academy/catalogue.json if the catalogue is the one that is wrong.")
        return 1
    print("✓ landing cards and about pages match the catalogue")
    return 0


if __name__ == "__main__":
    sys.exit(main())
