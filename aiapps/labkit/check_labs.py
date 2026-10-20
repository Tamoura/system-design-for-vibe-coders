#!/usr/bin/env python3
"""Check that every lab code block in the lessons equals its reference file.

A lab block starts with a first-line comment naming its path, e.g. `# labs/m01/chat.py`.
usage: python labkit/check_labs.py [modules_dir]   (run from aiapps/)"""
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
mods = Path(sys.argv[1]) if len(sys.argv) > 1 else root.parent / "modules"
PATH = re.compile(r"^#\s+(labs/[\w./-]+)\s*$")
bad = ok = 0
seen: set[str] = set()
for md in sorted(mods.glob("*.md")):
    if md.name.endswith(".ar.md"):
        continue
    for m in re.finditer(r"```(\w*)\n(.*?)```", md.read_text(encoding="utf-8"), flags=re.S):
        lang, body = m.groups()
        first = body.split("\n", 1)[0]
        p = PATH.match(first)
        if not p:
            continue
        rel = p.group(1)
        seen.add(rel)
        f = root / rel
        if not f.exists():
            print(f"✗ {md.name}: {rel} does not exist"); bad += 1; continue
        if f.read_text(encoding="utf-8").rstrip("\n") != body.rstrip("\n"):
            print(f"✗ {md.name}: block for {rel} differs from the file"); bad += 1
        else:
            ok += 1
unused = sorted(str(p.relative_to(root)) for p in (root / "labs").rglob("*.py") if str(p.relative_to(root)) not in seen)
print(f"{ok} lab blocks match their files, {bad} problems; {len(unused)} lab files not shown in any lesson" + (f": {unused[:5]}" if unused else ""))
sys.exit(1 if bad else 0)
