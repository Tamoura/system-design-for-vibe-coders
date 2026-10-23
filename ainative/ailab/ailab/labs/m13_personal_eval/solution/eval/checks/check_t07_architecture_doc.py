"""T07: docs/ARCHITECTURE.md describes the modules and the limits rule that exist today."""
import pathlib
import sys

text = pathlib.Path("docs/ARCHITECTURE.md").read_text(encoding="utf-8")
lower = text.lower()
problems = []
if "risk.py" in lower:
    problems.append("still describes risk.py, which does not exist")
for name in ("limits.py", "screening.py"):
    if name not in text:
        problems.append(f"does not mention {name}")
if "T3" not in text:
    problems.append("does not mention the T3 tier")
if "no monthly limit" in lower:
    problems.append("still says there is no monthly limit")
if problems:
    sys.exit("; ".join(problems))
