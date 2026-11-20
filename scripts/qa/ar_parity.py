#!/usr/bin/env python3
"""Arabic content parity: the Arabic edition keeps the content the English carries, not only its meaning.

The November 2026 content audit found that an automated gloss-trimming pass had deleted formula parts
("TP ÷ (TP + FP)" became "TP ÷."), quiz option letters and research citations from the Arabic lessons, and that
no check noticed. This check compares each English lesson with its Arabic twin (`X.md` and `X.ar.md`), and each
English string of a self-assessment item with its Arabic string, on tokens a translation must carry over unchanged:

- option letters in parentheses: (A) (B) (C) (D), or the Arabic (أ) (ب) (ج) (د);
- formula operators: ÷ × = ≈ ≤ ≥ and "+" or "−" between two operands;
- citations: "et al." (or «وزملاؤه», «وآخرون») and "Name, 2024" or "Name، 2024" (also after an attached Arabic
  «و», as in «Forsgren وHumble وKim، 2018»).

Each count in the Arabic must be at least the English count. Code fences, inline code and Mermaid blocks are left
out on both sides. Known, reviewed differences live in scripts/qa/ar-parity-baseline.json as
"path": {"token": allowed_shortfall}; a shortfall above that fails.

usage: python3 scripts/qa/ar_parity.py [--list] [--update-baseline]
exit status: 0 pass, 1 fail.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / "scripts" / "qa" / "ar-parity-baseline.json"
SKIP_DIRS = {"agentic", "node_modules", "_site", "videos", ".git"}
FENCE = re.compile(r"^[ \t]*(?:>[ \t]*)*```.*?^[ \t]*(?:>[ \t]*)*```", re.S | re.M)
CODE = re.compile(r"`[^`\n]*`")
TOKENS = {
    "option letter": re.compile(r"\([A-Dأبجد]\)"),
    "operator": re.compile(r"[÷×=≈≤≥]|(?<=[\w)\]%])\s[+−]\s(?=[\w(])"),
    "citation": re.compile(r"et al\.|وزملاؤه|وآخرون|(?<![A-Za-z0-9_])[A-Z][a-z]+[,،]\s*(?:19|20)\d{2}\b"),
}


def strip(text: str) -> str:
    return CODE.sub(" ", FENCE.sub(" ", text))


def counts(text: str) -> dict[str, int]:
    t = strip(text)
    return {name: len(rx.findall(t)) for name, rx in TOKENS.items()}


def pairs():
    for ar in sorted(ROOT.rglob("*.ar.md")):
        rel = ar.relative_to(ROOT)
        if set(rel.parts) & SKIP_DIRS or ar.name in ("COURSE.ar.md",):
            continue
        en = ar.with_name(ar.name[:-6] + ".md")
        if en.exists():
            yield str(rel), en.read_text(encoding="utf-8"), ar.read_text(encoding="utf-8")
    for js in sorted(ROOT.glob("**/assessment/data/*.json")):
        rel = js.relative_to(ROOT)
        if set(rel.parts) & SKIP_DIRS:
            continue
        en_all, ar_all = [], []

        def walk(node):
            if isinstance(node, dict):
                if isinstance(node.get("en"), (str, list)) and isinstance(node.get("ar"), (str, list)):
                    en_all.append(json.dumps(node["en"], ensure_ascii=False))
                    ar_all.append(json.dumps(node["ar"], ensure_ascii=False))
                for v in node.values():
                    walk(v)
            elif isinstance(node, list):
                for v in node:
                    walk(v)

        try:
            walk(json.loads(js.read_text(encoding="utf-8")))
        except ValueError:
            continue
        yield str(rel), "\n".join(en_all), "\n".join(ar_all)


def shortfalls() -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for rel, en, ar in pairs():
        ce, ca = counts(en), counts(ar)
        gap = {k: ce[k] - ca[k] for k in TOKENS if ce[k] > ca[k]}
        if gap:
            out[rel] = gap
    return out


def main() -> int:
    gaps = shortfalls()
    if "--update-baseline" in sys.argv:
        BASELINE.write_text(json.dumps(gaps, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote {BASELINE.relative_to(ROOT)} with {len(gaps)} file(s)")
        return 0
    base = json.loads(BASELINE.read_text(encoding="utf-8")) if BASELINE.exists() else {}
    bad, better = [], []
    for rel, gap in sorted(gaps.items()):
        for tok, n in gap.items():
            allowed = base.get(rel, {}).get(tok, 0)
            if n > allowed:
                bad.append(f"{rel}: Arabic has {n} fewer {tok}(s) than the English (baseline allows {allowed})")
    for rel, gap in base.items():
        for tok, n in gap.items():
            if gaps.get(rel, {}).get(tok, 0) < n:
                better.append(f"{rel}: {tok} shortfall below the baseline ({gaps.get(rel, {}).get(tok, 0)} < {n})")
    print(f"Arabic content parity (scripts/qa/ar_parity.py): {sum(1 for _ in pairs())} EN/AR pairs compared")
    if "--list" in sys.argv:
        for rel, gap in sorted(gaps.items()):
            print(f"  {rel}: {gap}")
    for b in better:
        print(f"  ↓ {b} — run with --update-baseline to lock it in")
    if bad:
        print(f"✗ {len(bad)} Arabic shortfall(s): formula parts, option letters or citations missing from the Arabic")
        for b in bad:
            print(f"  - {b}")
        return 1
    print("✓ the Arabic keeps every formula operator, option letter and citation the English has")
    return 0


if __name__ == "__main__":
    sys.exit(main())
