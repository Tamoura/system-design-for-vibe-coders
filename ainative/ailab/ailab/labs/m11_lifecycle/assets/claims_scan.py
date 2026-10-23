# ailab/labs/m11_lifecycle/assets/claims_scan.py
"""Claims scan: the mechanical half of a Claims check.

Run it from the root of your work directory:

    python lab-assets/claims_scan.py docs/ARCHITECTURE.md
    python lab-assets/claims_scan.py docs/postmortems/INC-2031.md --record lab-assets/incident.json

It reads a Markdown file and looks up every claim that can be looked up:
  * a backticked path (src/..., tests/..., docs/..., or any *.py name) must exist;
  * a backticked module.name (limits.QATAR_TZ, najmkit.audit.log_event) must be defined in src/;
  * with --record: every clock time (10:11) and event id (E7) must appear in the incident record.
It cannot tell whether a sentence is TRUE. It only finds claims that point at nothing.
Exit status: 0 when every pointer resolves, 1 when some do not.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

ROOTS = ("src", "tests", "docs", "lab-assets", ".github")
FILE_EXTENSIONS = {"py", "md", "json", "jsonl", "log", "txt", "toml", "yml", "yaml", "cfg", "ini", "csv", "lock"}
# A line that says the thing it names is not there ("the old page names `risk.py`, which does not exist") is a true claim.
SAYS_MISSING = re.compile(r"does(?:n't| not) exist|no longer exists?|no such\b|non-?existent|never existed|there is no\b|not a real\b", re.I)
PATH = re.compile(r"^(?:\./)?((?:[\w.-]+/)*[\w.-]+\.(?:py|md|json|toml|ya?ml|txt))(?::\d+)?$")
DOTTED = re.compile(r"^[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+$")


def definitions(root: Path) -> dict[str, set[str]]:
    """Every module under src/ (as 'limits' and 'remit.limits') -> the names it defines, classes' members included."""
    found: dict[str, set[str]] = {}
    for path in sorted((root / "src").rglob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)}
        names |= {n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
        package = path.parent.name
        found[path.stem] = names
        found[f"{package}.{path.stem}"] = names
    return found


def path_exists(root: Path, token: str) -> bool:
    name = PATH.match(token).group(1)
    if (root / name).exists():
        return True
    if "/" not in name:  # a bare file name: look in the usual places
        return any(root.glob(f"src/**/{name}")) or any((root / d / name).exists() for d in ("tests", "docs", "."))
    return False


def claims_in(text: str):
    """(line number, token) for every backticked token outside fenced code blocks."""
    fenced = False
    for number, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            for token in re.findall(r"`([^`\n]+)`", line):
                yield number, token.strip()


def scan(root: Path, doc: Path, record: Path | None) -> tuple[int, list[str]]:
    text = doc.read_text(encoding="utf-8")
    defined = definitions(root)
    problems, checked = [], 0
    lines = text.splitlines()
    for number, token in claims_in(text):
        token = re.sub(r"\(.*$", "", token)  # limits.to_local(now) -> limits.to_local
        says_missing = bool(SAYS_MISSING.search(lines[number - 1]))
        match = PATH.match(token)
        if match:
            name = match.group(1)
            if name.endswith((".py", ".md")) or name.split("/")[0] in ROOTS or (root / name).exists():
                checked += 1
                if not path_exists(root, token) and not says_missing:
                    problems.append(f"{doc}:{number}  `{token}`  no such file")
            continue
        if DOTTED.match(token):
            parts = token.split(".")
            if parts[0] in ("remit", "najmkit") and len(parts) > 1:
                module, rest = ".".join(parts[:2]), parts[2:]
            else:
                module, rest = parts[0], parts[1:]
            if module in defined and not (rest and rest[-1].lower() in FILE_EXTENSIONS and rest[-1] not in defined[module]):
                checked += 1  # `audit.jsonl` is a file name, not a name defined in the module `audit`
                if rest and rest[0] not in defined[module] and not says_missing:
                    problems.append(f"{doc}:{number}  `{token}`  {module} defines no '{rest[0]}'")
    if record is not None:
        events = json.loads(record.read_text(encoding="utf-8"))["timeline"]
        known_ids = {e["id"] for e in events}
        known_times = {e["time"][:5] for e in events}
        for number, line in enumerate(text.splitlines(), start=1):
            for hh, mm in re.findall(r"(?<![\d:.-])(\d{1,2}):(\d{2})(?::\d{2})?(?![\d:])", line):
                checked += 1
                if f"{int(hh):02d}:{mm}" not in known_times:
                    problems.append(f"{doc}:{number}  {hh}:{mm}  no event in the record at that time")
            for event_id in re.findall(r"\bE\d+\b", line):
                checked += 1
                if event_id not in known_ids:
                    problems.append(f"{doc}:{number}  {event_id}  no such event in the record")
    return checked, problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Find claims in a Markdown file that point at nothing.")
    parser.add_argument("doc", type=Path, help="the Markdown file to scan")
    parser.add_argument("--root", type=Path, default=Path("."), help="the repository root (default: .)")
    parser.add_argument("--record", type=Path, help="an incident record (JSON) to check times and event ids against")
    args = parser.parse_args(argv)
    if not args.doc.is_file():
        print(f"error: {args.doc} is not a file", file=sys.stderr)
        return 2
    checked, problems = scan(args.root, args.doc, args.record)
    for line in problems:
        print(line)
    print(f"{args.doc}: {checked} claims looked up, {len(problems)} do not resolve")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
