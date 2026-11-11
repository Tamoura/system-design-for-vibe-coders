#!/usr/bin/env python3
"""Claims lint: fail on wording the library must not publish.

Checked everywhere (sources and generated pages), except agentic/ (a published copy of another
repository), scripts/sync-agentic.sh (it lists blocked text on purpose) and scripts/qa/ (these checks):

  - the name of a real organisation: "Qatar Development Bank", the token QDB, «بنك قطر للتنمية»
  - exam-pass promises: "pass the AIGP", "ready for the AIGP exam", "sit the real exam", and their
    Arabic forms found in the sources on the day this check was written:
      «اجتياز امتحان شهادة (certification exam) AIGP», «اجتز امتحان AIGP», «جاهز لامتحان AIGP»,
      «تقدّم للامتحان الحقيقي»
  - in aigp/ only: "pass the exam" and «اجتياز الامتحان»

And landing.html must not link to the agentic/ pages.

Matching is per line, after removing HTML tags, Markdown emphasis and Arabic diacritics, so
"pass the **AIGP**" and "pass the <strong>AIGP</strong>" are caught. There is no baseline: every hit fails.

usage: python3 scripts/qa/claims_lint.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXCLUDE_DIRS = ("agentic/", "scripts/qa/", "node_modules/", ".git/")
EXCLUDE_FILES = {"scripts/sync-agentic.sh"}
BINARY = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".mp4", ".webm", ".mp3", ".wav", ".pdf", ".epub",
          ".zip", ".gz", ".woff", ".woff2", ".ttf", ".otf", ".pyc", ".sqlite", ".db"}

I = re.I
# (label, pattern, path prefix it applies to or None for everywhere)
RULES = [
    ("organisation name", re.compile(r"Qatar\s+Development\s+Bank", I), None),
    ("organisation name", re.compile(r"\bQDB\b"), None),
    ("organisation name", re.compile(r"بنك\s+قطر\s+للتنمية"), None),
    ("exam promise", re.compile(r"\bpass\s+the\s+AIGP\b", I), None),
    ("exam promise", re.compile(r"\bready\s+for\s+the\s+AIGP\s+exam\b", I), None),
    ("exam promise", re.compile(r"\bsit\s+the\s+real\s+exam\b", I), None),
    ("exam promise", re.compile(r"(?:اجتياز|اجتز|تجتاز)\s+امتحان\s+(?:شهادة\b[^\n.؛]{0,40}?)?AIGP"), None),
    ("exam promise", re.compile(r"جاهز\S{0,3}\s+لامتحان\s+AIGP"), None),
    ("exam promise", re.compile(r"(?:تقدم|خض)\s+(?:لل|ال)امتحان\s+الحقيقي"), None),
    ("exam promise (aigp)", re.compile(r"\bpass\s+the\s+exam\b", I), "aigp/"),
    ("exam promise (aigp)", re.compile(r"(?:اجتياز|اجتز)\s+الامتحان(?!\s+(?:التجريبي|التدريبي))"), "aigp/"),
]
DIACRITICS = re.compile(r"[ـً-ْٰ]")   # tatweel, harakat, shadda, sukun, dagger alif
# Every rule needs one of these words, so only lines that contain one are checked. The pattern is
# spelled out instead of using re.I, which is several times slower on the 150 MB of generated pages.
# The Arabic words may carry diacritics between their letters (the sources do write «المقطَّرة»), and
# the prefilter runs before they are removed, so it lets them through.
_D = "[ـً-ْٰ]*"
PREFILTER = re.compile(r"QDB|Qatar|QATAR|qatar|AIGP|Aigp|aigp|[Ee]xam|EXAM|"
                       + _D.join("قطر") + "|" + _D.join("امتحان"))
HREF = re.compile(r"""\b(?:href|src|action|formaction)\s*=\s*["']([^"']*)["']""", I)
AGENTIC_LINK = re.compile(r"(?:^|/)agentic(?:/|$|[?#])")


def files() -> list[str]:
    try:
        out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout
        paths = [p for p in out.split("\0") if p]
    except (OSError, subprocess.CalledProcessError):
        paths = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file()]
    keep = []
    for p in sorted(paths):
        if p.startswith(EXCLUDE_DIRS) or p in EXCLUDE_FILES or Path(p).suffix.lower() in BINARY:
            continue
        if (ROOT / p).is_file():
            keep.append(p)
    return keep


def normalise(line: str) -> str:
    line = re.sub(r"<[^>]{0,400}>", "", line)          # HTML tags (bdi, strong, b, em, a ...)
    line = re.sub(r"\*\*|__|(?<!\w)[*_]|[*_](?!\w)", "", line)   # Markdown emphasis
    line = line.replace("&nbsp;", " ").replace(" ", " ")
    line = DIACRITICS.sub("", line)
    return line


def main() -> int:
    hits = []
    scanned = 0
    for p in files():
        try:
            text = (ROOT / p).read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if "\0" in text:
            continue
        scanned += 1
        prev_start, lineno, visited = 0, 1, -1
        for hit in PREFILTER.finditer(text):           # visit only the lines that contain a candidate word
            start = text.rfind("\n", 0, hit.start()) + 1
            if start == visited:                      # matches come in order: same line as the last one
                continue
            lineno += text.count("\n", prev_start, start)
            prev_start = visited = start
            end = text.find("\n", hit.end())
            raw = text[start:] if end < 0 else text[start:end]
            if len(raw) > 20000:            # minified or inlined assets: check in slices to keep the regexes fast
                pieces = [raw[i:i + 20000] for i in range(0, len(raw), 19000)]
            else:
                pieces = [raw]
            for piece in pieces:
                line = normalise(piece)
                for label, rx, scope in RULES:
                    if scope and not p.startswith(scope):
                        continue
                    for m in rx.finditer(line):
                        s = max(0, m.start() - 50)
                        hits.append((p, lineno, label, re.sub(r"\s+", " ", line[s:m.end() + 30]).strip()))
    # landing page links
    landing = ROOT / "landing.html"
    link_hits = []
    if landing.exists():
        for lineno, line in enumerate(landing.read_text(encoding="utf-8").split("\n"), 1):
            for m in HREF.finditer(line):
                if AGENTIC_LINK.search(m.group(1)):
                    link_hits.append(("landing.html", lineno, "link to agentic/", m.group(0)))
    hits += link_hits

    print(f"Claims lint (scripts/qa/claims_lint.py): {scanned} text files scanned")
    seen = set()
    for p, lineno, label, ctx in hits:
        if (p, lineno, label, ctx) in seen:
            continue
        seen.add((p, lineno, label, ctx))
        print(f"  ✗ {p}:{lineno}  [{label}]  …{ctx}…")
    if hits:
        by_file = sorted({h[0] for h in hits})
        print(f"\n✗ {len(seen)} hit(s) in {len(by_file)} file(s). Remove the wording from the source, rebuild the "
              f"generated pages, and run this again.")
        return 1
    print("✓ no banned names, exam-pass promises or landing links to agentic/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
