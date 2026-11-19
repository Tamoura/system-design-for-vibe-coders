#!/usr/bin/env python3
"""Trim over-glossed Arabic: keep an English gloss only for a real technical term, once per lesson.

The owner's standing rule is an English term in parentheses beside an Arabic technical term. Earlier work
applied it to nearly every phrase ("(the same channel)", "(at the time of writing)"), which made the Arabic
hard to read. This tool applies the rule as written. For one Arabic Markdown file or JSON item file it keeps a
parenthesised English gloss only when ALL of these hold, and deletes the rest (the Arabic is unchanged):

  * it is not nested inside another parenthesis (a gloss that holds inline code, a link or a digit is never removed);
  * it does not start with a function word (the, a, to, of, ...);
  * it has at most two words, or at most five words and the same text is used as a gloss at least three
    times in the whole library (a recurring technical term such as "human in the loop");
  * it is the first use of that text in the file (prose); later uses of the same term stay bare.

Quiz, exam and self-assessment option lines keep their terms wherever they appear (each item must read on its
own) and only lose phrase-like glosses. Code fences, inline code, link targets, URLs, HTML tags and Mermaid
diagrams are never touched.

usage:
  python3 scripts/qa/trim_glosses.py --dry-run          # per-file before/after density, nothing written
  python3 scripts/qa/trim_glosses.py                    # rewrite the files
  python3 scripts/qa/trim_glosses.py --show FILE        # print one file's changes as a diff-like list
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {"node_modules", "agentic", "beacon", "videos", "dist", "_site", ".git"}
GLOSS = re.compile(r"(\s*)\(([^()\n]*[A-Za-z][^()\n]*)\)")
FENCE = re.compile(r"^[ \t]*(?:>[ \t]*)*```[^\n]*\n.*?^[ \t]*(?:>[ \t]*)*```[ \t]*$", re.S | re.M)
PROTECT = [
    re.compile(r"`[^`\n]*`"),
    re.compile(r"\]\([^)\s]*\)"),
    re.compile(r"https?://[^\s)<>\"]+"),
    re.compile(r"<[^>\n]+>"),
]
OPTION_LINE = re.compile(r"^\s*(?:[-*]\s+)?\**[A-D][.)]\**\s")
STOP = {"the", "a", "an", "to", "of", "in", "on", "for", "with", "at", "by", "from", "and", "or", "is", "are", "was",
        "were", "be", "it", "its", "this", "that", "these", "those", "your", "our", "their", "his", "her", "we", "you",
        "they", "not", "no", "if", "when", "while", "as", "into", "than", "so", "do", "does", "did", "can", "will",
        "should", "must", "may", "i", "my", "how", "what", "why", "which", "who", "there", "here", "any", "all", "some"}
TERM_MIN_USES = 3
# Content, not a gloss: never removed. Formula parts ("(TP + FP)", "(1 − p)"), option and sub-point letters ("(A)",
# "Art. 6(1)(f)"), citations ("(Hines et al., 2024)", "(Willison, 2025)"), lesson and standard pointers
# ("(Evaluate · 6.1)", "(RFC 8555)", "(OWASP LLM05)"). The November 2026 content audit found that an earlier run had
# deleted all of these from the Arabic editions; scripts/qa/ar_parity.py now catches that class of loss.
CONTENT = re.compile(r"[÷×=+<>≈≤≥−%]|^\s*(?:[A-Za-z]|[ivx]{1,4})\s*$|et al\.|[A-Z][a-z]+[,،]\s*\d{4}\s*$|\bRFC\s*\d+"
                     r"|\b(?:LLM|ASI|API|A)\d{2}\b|§|·\s*\d+\.\d+")


def files() -> list[Path]:
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    res = []
    for p in out.split("\0"):
        if not p:
            continue
        f = ROOT / p
        parts = f.relative_to(ROOT).parts
        if set(parts) & SKIP_DIRS:
            continue
        if f.name.endswith(".ar.md") and ((len(parts) == 3 and parts[1] == "modules") or (len(parts) == 3 and parts[0] == "modules")
                                          or (len(parts) == 2 and f.name == "README.ar.md")):
            res.append(f)
    return sorted(res)


def norm(g: str) -> str:
    return re.sub(r"\s+", " ", g.strip().lower())


def mask(text: str) -> tuple[str, list[str]]:
    """Replace protected regions with placeholders that contain no parentheses or Latin letters."""
    store: list[str] = []

    def put(m: re.Match) -> str:
        store.append(m.group(0))
        return f"\u0001{len(store) - 1}\u0002"

    text = FENCE.sub(put, text)
    for pat in PROTECT:
        text = pat.sub(put, text)
    return text, store


def unmask(text: str, store: list[str]) -> str:
    return re.sub(r"\u0001(\d+)\u0002", lambda m: store[int(m.group(1))], text)


def corpus_counts(paths: list[Path]) -> collections.Counter:
    c: collections.Counter = collections.Counter()
    for f in paths:
        text, _ = mask(f.read_text(encoding="utf-8"))
        for m in GLOSS.finditer(text):
            c[norm(m.group(2))] += 1
    return c


def is_term(g: str, counts: collections.Counter) -> bool:
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9\-/'.+&]*", g)
    if not words:
        return False
    if words[0].lower() in STOP:
        return False
    if len(words) <= 2:
        return True
    return len(words) <= 5 and counts[norm(g)] >= TERM_MIN_USES


def trim_text(text: str, counts: collections.Counter) -> tuple[str, int, int]:
    masked, store = mask(text)
    seen: set[str] = set()
    removed = kept = 0
    out_lines = []
    for line in masked.split("\n"):
        option = bool(OPTION_LINE.match(line))

        def sub(m: re.Match) -> str:
            nonlocal removed, kept
            g = m.group(2)
            nested = (line[m.end():m.end() + 1] == ")" and "(" in line[:m.start()]
                      and not re.fullmatch(r"[A-Z][A-Z0-9/+&-]{1,7}s?", g.strip()))   # nested acronym, e.g. "...system (ATS))", stays
            in_bold = line[:m.start()].count("**") % 2 == 1          # an English bold name in a table cell, e.g. **Service level objective (SLO)**
            pinned = in_bold or bool(CONTENT.search(g)) or bool(re.search(r"[\u0001\d]|(?:^|[\s,.])[IVX]{1,4}(?:[.,\s\u2013\u2014-]|$)", g))   # inline code, link or URL inside; a code such as I.A, LLM01 or "I, IV"
            keep = pinned or ((not nested) and is_term(g, counts) and (option or norm(g) not in seen))
            if keep:
                if not option:
                    seen.add(norm(g))
                kept += 1
                return m.group(0)
            removed += 1
            return ""

        out_lines.append(GLOSS.sub(sub, line))
    return unmask("\n".join(out_lines), store), removed, kept


JSON_STRING = re.compile(r'"(?:[^"\\\n]|\\.)*"')


def trim_json_text(text: str, counts):
    """Arabic strings of an item file: keep terms, drop phrase glosses. Only the string literals that contain
    Arabic are rewritten, in place, so the file's own formatting and its English strings stay as they are."""
    stats = [0, 0]

    def sub(m: re.Match) -> str:
        lit = m.group(0)
        try:
            value = json.loads(lit)
        except ValueError:
            return lit
        if not re.search(r"[\u0600-\u06FF]", value):
            return lit
        new, r, k = trim_text(value, counts)
        stats[0] += r
        stats[1] += k
        if new == value:
            return lit
        enc = json.dumps(new, ensure_ascii=False)
        return enc

    return JSON_STRING.sub(sub, text), stats[0], stats[1]


def json_files() -> list[Path]:
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    res = []
    for p in out.split("\0"):
        f = ROOT / p
        if p.endswith(".json") and f.parent.name == "data" and f.parent.parent.name == "assessment":
            res.append(f)
    return sorted(res)


def density(text: str) -> float:
    masked, _ = mask(text)
    words = sum(1 for w in masked.split() if re.search(r"[؀-ۿ]", w))
    return 100.0 * len(GLOSS.findall(masked)) / words if words else 0.0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--show", type=Path)
    args = ap.parse_args()
    md = files()
    counts = corpus_counts(md)
    if args.show:
        f = args.show.resolve()
        before = f.read_text(encoding="utf-8")
        after, r, k = trim_text(before, counts)
        a, b = before.split("\n"), after.split("\n")
        for x, y in zip(a, b):
            if x != y:
                print("-", x[:400])
                print("+", y[:400])
                print()
        print(f"removed {r}, kept {k}")
        return 0
    tot_r = tot_k = 0
    for f in md:
        before = f.read_text(encoding="utf-8")
        after, r, k = trim_text(before, counts)
        tot_r += r
        tot_k += k
        print(f"{density(before):5.1f} -> {density(after):5.1f}  removed {r:5} kept {k:5}  {f.relative_to(ROOT)}")
        if not args.dry_run and after != before:
            f.write_text(after, encoding="utf-8")
    for f in json_files():
        before = f.read_text(encoding="utf-8")
        after, r, k = trim_json_text(before, counts)
        tot_r += r
        tot_k += k
        if not args.dry_run and after != before:
            f.write_text(after, encoding="utf-8")
    print(f"total removed {tot_r}, kept {tot_k}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
