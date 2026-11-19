#!/usr/bin/env python3
"""Study time: write each lesson's estimate as reading time plus hands-on time, and each course's total.

academy/STANDARD.md section 3 asks every lesson for a study time, labelled an estimate until a pilot measures it.
The November 2026 content audit found the same figure ("about 110 minutes") stamped on nearly every lesson,
whatever its workload. This tool replaces those lines:

- reading minutes come from the English lesson's words (prose only, code blocks left out) at 200 words a minute;
  the Arabic line uses the same figure;
- hands-on minutes (exercises, labs, quizzes) come from academy/study-times.json, keyed "<english file>#<lesson>",
  which the course authors estimate per lesson;
- each course README (English and Arabic) gets a total and a pace at 6 study hours a week, between the markers
  <!-- study-time --> and <!-- /study-time -->.

    python3 scripts/study_time.py            # rewrite lessons and READMEs
    python3 scripts/study_time.py --check    # exit 1 if any file would change, or a lesson has no estimate
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "academy" / "study-times.json"
LESSON = re.compile(r"^# ((?:[0-9]+|[A-Z])(?:\.[0-9]+)?) [—–-] ", re.M)
FENCE = re.compile(r"^```.*?^```", re.S | re.M)
EN_LINE = re.compile(r"\*Study time:[^*\n]*\*")
AR_LINE = re.compile(r"\*مدة الدراسة:[^*\n]*\*")
WPM = 200
WEEKLY_HOURS = 6
COURSES = ["vibe", "saas", "aigp", "aipm", "secai", "career", "data", "cloud", "testing", "aiapps", "ainative", "founder"]


def course_of(rel: str) -> str:
    first = rel.split("/")[0]
    return first if first in COURSES else "vibe"


def lesson_files() -> list[Path]:
    files = sorted(ROOT.glob("modules/*/*.md")) + sorted(ROOT.glob("*/modules/*.md"))
    return [f for f in files if not f.name.endswith(".ar.md") and "agentic" not in f.parts]


def blocks(text: str):
    starts = [(m.start(), m.group(1)) for m in LESSON.finditer(text)]
    for i, (s, lid) in enumerate(starts):
        e = starts[i + 1][0] if i + 1 < len(starts) else len(text)
        yield lid, s, e


def round5(x: float) -> int:
    return max(5, int(5 * round(x / 5)))


def fmt_total(minutes: int) -> tuple[str, str]:
    hours = round(minutes / 60)
    weeks = max(1, round(minutes / 60 / WEEKLY_HOURS))
    en = (f"**Study time for the whole course: about {hours} hours** (estimate: reading plus hands-on work, summed over "
          f"every lesson). At about {WEEKLY_HOURS} hours a week that is roughly {weeks} weeks. Each lesson shows its own "
          f"split; a pilot with real learners will replace these estimates.")
    ar = (f"**مدة دراسة الدورة كاملةً: نحو {hours} ساعة** (تقدير: القراءة مع العمل التطبيقي، مجموعًا على كل الدروس). "
          f"بمعدل {WEEKLY_HOURS} ساعات أسبوعيًا تقريبًا، يعني ذلك نحو {weeks} أسابيع. يبيّن كل درس تقسيمه الخاص، "
          f"وستحلّ محلّ هذه التقديرات قياساتٌ من تجربة مع متعلمين حقيقيين.")
    return en, ar


def put_block(text: str, body: str) -> str:
    block = f"<!-- study-time -->\n{body}\n<!-- /study-time -->"
    if "<!-- study-time -->" in text:
        return re.sub(r"<!-- study-time -->.*?<!-- /study-time -->", lambda _: block, text, flags=re.S)
    m = re.search(r"^## ", text, re.M)
    if not m:
        return text.rstrip("\n") + "\n\n" + block + "\n"
    return text[:m.start()] + block + "\n\n" + text[m.start():]


def main() -> int:
    check = "--check" in sys.argv
    hands = json.loads(DATA.read_text(encoding="utf-8"))
    changed, missing = [], []
    totals: dict[str, int] = {}
    for f in lesson_files():
        rel = str(f.relative_to(ROOT))
        text = f.read_text(encoding="utf-8")
        ar_path = f.with_name(f.name[:-3] + ".ar.md")
        ar = ar_path.read_text(encoding="utf-8") if ar_path.exists() else None
        lines_en, lines_ar = {}, {}
        for lid, s, e in blocks(text):
            if text[s:].startswith("# Module"):
                continue
            key = f"{rel}#{lid}"
            if key not in hands:
                missing.append(key)
                continue
            words = len(re.findall(r"\w+", FENCE.sub(" ", text[s:e])))
            read, hand = round5(words / WPM), int(hands[key])
            totals[course_of(rel)] = totals.get(course_of(rel), 0) + read + hand
            if hand:
                h_en, h_ar = (f"{hand} min", f"{hand} دقيقة") if hand < 180 else (f"{round(hand / 60)} h", f"{round(hand / 60)} ساعة")
                lines_en[lid] = f"*Study time: reading about {read} min, hands-on about {h_en} (estimate).*"
                lines_ar[lid] = f"*مدة الدراسة: قراءة نحو {read} دقيقة، وعمل تطبيقي نحو {h_ar} (تقدير).*"
            else:
                lines_en[lid] = f"*Study time: reading about {read} min, no hands-on work (estimate).*"
                lines_ar[lid] = f"*مدة الدراسة: قراءة نحو {read} دقيقة، دون عمل تطبيقي (تقدير).*"

        def rewrite(src: str, lines: dict, rx: re.Pattern) -> str:
            out, last = [], 0
            for lid, s, e in blocks(src):
                if lid not in lines:
                    continue
                head = src[s:e]
                opening_end = head.find("\n## ")
                opening = head if opening_end < 0 else head[:opening_end]
                new_open = rx.sub(lambda _: lines[lid], opening, count=1)
                out.append(src[last:s] + new_open + head[len(opening):])
                last = e
            out.append(src[last:])
            return "".join(out)

        new_en = rewrite(text, lines_en, EN_LINE)
        if new_en != text:
            changed.append(rel)
            if not check:
                f.write_text(new_en, encoding="utf-8")
        if ar is not None:
            new_ar = rewrite(ar, lines_ar, AR_LINE)
            if new_ar != ar:
                changed.append(str(ar_path.relative_to(ROOT)))
                if not check:
                    ar_path.write_text(new_ar, encoding="utf-8")
    for cid, minutes in totals.items():
        base = ROOT if cid == "vibe" else ROOT / cid
        en_body, ar_body = fmt_total(minutes)
        for name, body in (("README.md", en_body), ("README.ar.md", ar_body)):
            p = base / name
            if not p.exists():
                continue
            t = p.read_text(encoding="utf-8")
            n = put_block(t, body)
            if n != t:
                changed.append(str(p.relative_to(ROOT)))
                if not check:
                    p.write_text(n, encoding="utf-8")
    for cid in sorted(totals):
        print(f"  {cid:9} about {round(totals[cid] / 60)} h")
    if missing:
        print(f"✗ {len(missing)} lesson(s) with no hands-on estimate in {DATA.relative_to(ROOT)}:")
        for m in missing[:30]:
            print("  -", m)
        return 1
    if check and changed:
        print(f"✗ {len(changed)} file(s) out of date; run python3 scripts/study_time.py")
        return 1
    print(f"✓ study times {'checked' if check else 'written'} ({len(changed)} file(s) {'would change' if check else 'changed'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
