#!/usr/bin/env python3
"""Answer-cue audit: can a reader score well on the multiple-choice items without reading the question?

For every course, instrument and language this script scores a few content-free strategies:

  longest   pick the option that is uniquely the longest (in characters)
  shortest  pick the option that is uniquely the shortest
  mid       share of items whose key is neither the unique longest nor the unique shortest
            option. A reader who drops those two keeps the key this often. Chance is about 50%.
  midguess  drop the unique longest and unique shortest, guess among the rest: the expected score.
            Chance is about 25%. With four options it can never pass 50%.
  latin     Arabic only: pick the option with uniquely the most Latin letters (the English glosses
            can give the key away)
  key       share of the most common key letter (A-D). For the self-assessments the pages shuffle
            the options for each reader, so this number only describes the source files.

Instruments:
  quiz   the "Check yourself" questions in <course>/modules/*.md and *.ar.md
  exam   the practice or mock exam section in the same files ("## ✍️ Practice exam" / "Mock exam")
  self   the self-assessment items in <course>/assessment/data/*.json (the vibe course: assessment/data/)

Open-answer items (no lettered options) are counted but not scored.

Ratchet (default mode): compare with scripts/qa/cue-baseline.json and fail if
  - a strategy's score for a course/instrument/language in the baseline rises by more than 2
    percentage points, or
  - a course/instrument/language that is not in the baseline scores above the limit for new
    instruments: 35% for longest, shortest, midguess, latin and key; 62.5% for mid.

usage:
  python3 scripts/qa/quiz_cues.py                    # print the table, check against the baseline
  python3 scripts/qa/quiz_cues.py --update-baseline  # write the current scores as the new baseline
  python3 scripts/qa/quiz_cues.py --items aigp/exam/en --strategy longest
                                                     # list the items a strategy gets right
  python3 scripts/qa/quiz_cues.py --json             # the scores as JSON
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASELINE = Path(__file__).resolve().with_name("cue-baseline.json")
TOLERANCE_PP = 2.0
SKIP_DIRS = {"node_modules", "agentic", "beacon", "videos", "dist", "_site", ".git", ".github"}

# name, short description, limit for a new course/instrument/language (percent)
STRATEGIES = [
    ("longest", "pick the unique longest option", 35.0),
    ("shortest", "pick the unique shortest option", 35.0),
    ("mid", "key survives dropping the unique longest and shortest (chance about 50%)", 62.5),
    ("midguess", "drop the unique longest and shortest, guess among the rest (expected score)", 35.0),
    ("latin", "Arabic: pick the option with the unique most Latin letters", 35.0),
    ("key", "share of the most common key letter", 35.0),
]
LIMIT = {name: limit for name, _, limit in STRATEGIES}
INSTRUMENTS = ("quiz", "exam", "self")
LETTERS = "ABCDEFGH"

QUESTION = re.compile(r"^\*\*(\d+)\.\s")
OPTION = re.compile(r"^- ([A-H])\.\s+(.*?)\s*$")
KEY = re.compile(r"^\*\*([A-H])\.\*\*")
LATIN = re.compile(r"[A-Za-z]")


# ------------------------------------------------------------------ parsing

def course_of(rel: Path) -> str:
    """The course id: the first folder, or 'vibe' for the course whose sources sit at the repo root."""
    return "vibe" if rel.parts[0] in ("modules", "assessment") else rel.parts[0]


def module_files() -> list[Path]:
    files = sorted(ROOT.glob("*/modules/*.md")) + sorted(ROOT.glob("modules/*/*.md"))
    return [f for f in files if f.relative_to(ROOT).parts[0] not in SKIP_DIRS]


def parse_markdown(path: Path) -> list[dict]:
    """Items under '## ✍️ ...' headings. An exam heading names an exam; any other ✍️ heading is a lesson quiz.

    A question is a bold numbered line, its options are '- A. text' lines before the answer block,
    and the key is the bold letter that opens the <details> answer block.
    """
    rel = path.relative_to(ROOT)
    section = lesson = None
    items: list[dict] = []
    cur = None
    in_answer = in_fence = False
    for lineno, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("# "):
            section, cur = None, None
            m = re.match(r"# (\d+\.\d+)\b", line)
            lesson = m.group(1) if m else lesson
            continue
        if line.startswith("## "):
            cur = None
            if "✍️" in line:
                section = "exam" if re.search(r"exam|امتحان", line, re.I) else "quiz"
            else:
                section = None
            continue
        if section is None:
            continue
        m = QUESTION.match(line)
        if m:
            cur = {"course": course_of(rel), "instrument": section, "lang": "ar" if path.name.endswith(".ar.md") else "en",
                   "where": f"{rel}:{lineno}", "id": f"{lesson or '?'} Q{m.group(1)}", "options": [], "key": None}
            items.append(cur)
            in_answer = False
            continue
        if cur is None:
            continue
        if line.startswith("<details"):
            in_answer = True
            continue
        if line.startswith("</details"):
            in_answer = False
            continue
        m = OPTION.match(line)
        if m and not in_answer and cur["key"] is None:
            cur["options"].append((m.group(1), m.group(2)))
            continue
        m = KEY.match(line)
        if m and in_answer and cur["key"] is None:
            cur["key"] = m.group(1)
    return items


def assessment_files() -> list[Path]:
    files = sorted(ROOT.glob("*/assessment/data/*.json")) + sorted(ROOT.glob("assessment/data/*.json"))
    return [f for f in files if f.relative_to(ROOT).parts[0] not in SKIP_DIRS]


def parse_assessment(path: Path) -> list[dict]:
    """Self-assessment items: {"questions": [{"id", "lesson", "o": {"en": [...], "ar": [...]}, "a": index}]}."""
    rel = path.relative_to(ROOT)
    data = json.loads(path.read_text(encoding="utf-8"))
    items = []
    for q in data.get("questions", []):
        for lang, opts in (q.get("o") or {}).items():
            a = q.get("a")
            items.append({"course": course_of(rel), "instrument": "self", "lang": lang, "where": str(rel),
                          "id": f"{q.get('id', '?')} (lesson {q.get('lesson', '?')})",
                          "options": [(LETTERS[i], t) for i, t in enumerate(opts)],
                          "key": LETTERS[a] if isinstance(a, int) and 0 <= a < len(opts) else None})
    return items


def collect() -> list[dict]:
    items = []
    for f in module_files():
        items += parse_markdown(f)
    for f in assessment_files():
        items += parse_assessment(f)
    return items


# ------------------------------------------------------------------ scoring

def unique_extreme(values: dict[str, float], pick) -> str | None:
    best = pick(values.values())
    hits = [k for k, v in values.items() if v == best]
    return hits[0] if len(hits) == 1 else None


def item_flags(item: dict) -> dict[str, float]:
    """What each strategy scores on one item (1, 0 or an expected fraction)."""
    opts = dict(item["options"])
    key = item["key"]
    lengths = {k: len(t.strip()) for k, t in opts.items()}
    longest = unique_extreme(lengths, max)
    shortest = unique_extreme(lengths, min)
    rest = [k for k in opts if k not in (longest, shortest)] or list(opts)
    latin_counts = {k: len(LATIN.findall(t)) for k, t in opts.items()}
    latin = unique_extreme(latin_counts, max) if max(latin_counts.values()) > 0 else None
    return {
        "longest": float(longest == key),
        "shortest": float(shortest == key),
        "mid": float(key in rest),
        "midguess": (1.0 / len(rest)) if key in rest else 0.0,
        "latin": float(latin == key),
    }


def score(items: list[dict]) -> dict[str, dict]:
    """Rows keyed 'course/instrument/lang' with n, skipped and each strategy's score in percent."""
    groups: dict[str, list[dict]] = collections.defaultdict(list)
    skipped: collections.Counter = collections.Counter()
    for it in items:
        row = f"{it['course']}/{it['instrument']}/{it['lang']}"
        if it["key"] is None or len(it["options"]) < 3 or it["key"] not in dict(it["options"]):
            skipped[row] += 1
            continue
        groups[row].append(it)
    rows = {}
    for row in sorted(set(groups) | set(skipped)):
        its = groups.get(row, [])
        n = len(its)
        r: dict = {"n": n, "open": skipped.get(row, 0)}
        if n:
            sums = collections.Counter()
            for it in its:
                sums.update(item_flags(it))
            for name in ("longest", "shortest", "mid", "midguess"):
                r[name] = round(100.0 * sums[name] / n, 1)
            if row.endswith("/ar"):
                r["latin"] = round(100.0 * sums["latin"] / n, 1)
            keys = collections.Counter(it["key"] for it in its)
            letter, count = keys.most_common(1)[0]
            r["key"] = round(100.0 * count / n, 1)
            r["key_letter"] = letter
        rows[row] = r
    return rows


def sort_key(row: str):
    course, instrument, lang = row.split("/")
    return (course, INSTRUMENTS.index(instrument) if instrument in INSTRUMENTS else 9, lang)


# ------------------------------------------------------------------ ratchet

def check(rows: dict, baseline: dict) -> tuple[list[str], dict[str, set], list[str]]:
    """Failures, the cells to mark in the table, and notes about scores that fell."""
    base_rows = baseline.get("rows", {})
    fails, notes = [], []
    marks: dict[str, set] = collections.defaultdict(set)
    for row, r in rows.items():
        if not r["n"]:
            continue
        b = base_rows.get(row)
        for name, _, limit in STRATEGIES:
            if name not in r:
                continue
            v = r[name]
            if b is None or not b.get("n"):
                if v > limit:
                    fails.append(f"{row}: new instrument scores {v:.1f}% on '{name}' (limit {limit:g}%)")
                    marks[row].add(name)
            elif name in b:
                if v > b[name] + TOLERANCE_PP:
                    fails.append(f"{row}: '{name}' rose from {b[name]:.1f}% to {v:.1f}% (more than {TOLERANCE_PP:g} points)")
                    marks[row].add(name)
                elif v < b[name] - TOLERANCE_PP:
                    notes.append(f"{row}: '{name}' fell from {b[name]:.1f}% to {v:.1f}%")
    gone = sorted(set(base_rows) - set(rows))
    for row in gone:
        notes.append(f"{row}: in the baseline but no longer found")
    return fails, marks, notes


def table(rows: dict, marks: dict[str, set]) -> str:
    cols = ["longest", "shortest", "mid", "midguess", "latin", "key"]
    head = f"{'course/instrument/lang':<24} {'n':>4} {'open':>4}  " + " ".join(f"{c:>9}" for c in cols)
    out = [head, "-" * len(head)]
    for row in sorted(rows, key=sort_key):
        r = rows[row]
        cells = []
        for c in cols:
            if c not in r:
                cells.append(f"{'-':>9}")
                continue
            text = f"{r[c]:.1f}" + (f" {r['key_letter']}" if c == "key" else "")
            flag = "!" if c in marks.get(row, ()) else ("*" if r[c] > LIMIT[c] else " ")
            cells.append(f"{text + flag:>9}")
        out.append(f"{row:<24} {r['n']:>4} {r['open']:>4}  " + " ".join(cells))
    out.append("")
    out.append("Scores are percentages. chance: longest, shortest, midguess, latin, key about 25%; mid about 50%.")
    out.append("* above the limit a new instrument must meet (35%; 62.5% for mid). ! fails the ratchet.")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--update-baseline", action="store_true", help="write the current scores to cue-baseline.json")
    ap.add_argument("--baseline", type=Path, default=BASELINE, help="baseline file (default: scripts/qa/cue-baseline.json)")
    ap.add_argument("--json", action="store_true", help="print the scores as JSON instead of the table")
    ap.add_argument("--items", metavar="COURSE/INSTRUMENT/LANG", help="list the items of one row that a strategy gets right")
    ap.add_argument("--strategy", default="longest", choices=["longest", "shortest", "latin"], help="strategy for --items")
    args = ap.parse_args()

    items = collect()
    rows = score(items)

    if args.items:
        want = args.items.strip("/")
        hits = 0
        for it in items:
            if f"{it['course']}/{it['instrument']}/{it['lang']}" != want or it["key"] is None or len(it["options"]) < 3:
                continue
            if item_flags(it)[args.strategy]:
                hits += 1
                print(f"{it['where']}  {it['id']}  key {it['key']}")
        print(f"{hits} item(s) in {want} where '{args.strategy}' finds the key")
        return 0

    if args.update_baseline:
        payload = {
            "about": "Written by scripts/qa/quiz_cues.py --update-baseline. Percent scores of content-free "
                     "strategies per course/instrument/language. See scripts/qa/README.md before changing it.",
            "tolerance_pp": TOLERANCE_PP,
            "rows": {row: rows[row] for row in sorted(rows, key=sort_key) if rows[row]["n"]},
        }
        lines = [f'  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}' for k, v in payload["rows"].items()]
        text = ('{\n "about": ' + json.dumps(payload["about"]) + ',\n "tolerance_pp": ' + json.dumps(TOLERANCE_PP)
                + ',\n "rows": {\n' + ",\n".join(lines) + "\n }\n}\n")
        json.loads(text)  # one row per line keeps the diffs readable; make sure it is still valid JSON
        args.baseline.write_text(text, encoding="utf-8")
        print(table(rows, {}))
        print(f"\nBaseline written: {args.baseline.relative_to(ROOT) if args.baseline.is_relative_to(ROOT) else args.baseline} "
              f"({len(payload['rows'])} rows)")
        return 0

    if not args.baseline.exists():
        print(f"error: no baseline at {args.baseline}; run with --update-baseline first", file=sys.stderr)
        return 2
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    fails, marks, notes = check(rows, baseline)

    if args.json:
        print(json.dumps({"rows": rows, "failures": fails, "notes": notes}, indent=1, ensure_ascii=False))
        return 1 if fails else 0

    print("Answer-cue audit (scripts/qa/quiz_cues.py)\n")
    print(table(rows, marks))
    if notes:
        print("\nLower than the baseline (run --update-baseline to lock the improvement in):")
        for n in notes:
            print(f"  - {n}")
    if fails:
        print(f"\n✗ {len(fails)} cue regression(s):")
        for f in fails:
            print(f"  - {f}")
        print("\nRewrite the options so length and glosses do not point at the key. "
              "See scripts/qa/README.md for when a baseline update is acceptable.")
        return 1
    print(f"\n✓ no cue regressions ({sum(r['n'] for r in rows.values())} scored items in "
          f"{sum(1 for r in rows.values() if r['n'])} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
