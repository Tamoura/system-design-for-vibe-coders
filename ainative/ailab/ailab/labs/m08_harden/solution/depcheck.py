#!/usr/bin/env python3
"""Dependency check for Najm Remit (reference solution of lab m08): a guard against invented or unvetted packages.

    python scripts/depcheck.py [ROOT]        ROOT defaults to the current directory

A package is fine when it is in `deps-allowlist.txt` or pinned in `requirements.lock`. Anything declared in
`pyproject.toml` or `requirements*.txt`, or imported under `src/` and `tests/`, that is in neither is reported as
`FLAG <name>: <reason>` and the exit code is 1. A package installed from a URL is always reported. The script only
READS files: it never imports the project, never installs anything and never uses the network.
"""
import ast
import re
import sys
import tomllib
from pathlib import Path

NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def normalise(name):
    """PEP 503: lower case, and runs of - _ . become a single -."""
    return re.sub(r"[-_.]+", "-", name).lower()


def requirement(line):
    """(name, from_url) for one requirement line, or None when the line holds no requirement."""
    line = re.sub(r"(^|\s)#.*$", "", line).strip().rstrip("\\").strip()
    if not line or line.startswith("-"):
        return None  # blank, a comment, or an option (-r, --index-url, --hash=...)
    if "://" in line:
        egg = re.search(r"#egg=([A-Za-z0-9._-]+)", line)
        found = NAME.match(line)
        return (egg.group(1) if egg else found.group(0) if found else line), True
    found = NAME.match(line)
    return (found.group(0), False) if found else (line, False)


def lines_of(path):
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return []


def read_allowlist(root):
    names, modules = set(), set()
    for raw in lines_of(root / "deps-allowlist.txt"):
        text = raw.split("#", 1)[0].strip()
        if not text:
            continue
        name, _, aliases = text.partition(":")
        names.add(normalise(name.strip()))
        modules |= {normalise(m.strip()) for m in aliases.split(",") if m.strip()}
    return names, modules


def read_lock(root):
    return {normalise(found[0]) for line in lines_of(root / "requirements.lock") if (found := requirement(line))}


def declared(root):
    """Yield (name, from_url, where) for everything the project says it depends on."""
    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        try:
            project = tomllib.loads(pyproject.read_text(encoding="utf-8")).get("project", {})
        except (tomllib.TOMLDecodeError, UnicodeDecodeError):
            project = {}
        groups = [project.get("dependencies", [])] + list(project.get("optional-dependencies", {}).values())
        for group in groups:
            for item in group:
                if found := requirement(item):
                    yield found[0], found[1], "pyproject.toml"
    for path in sorted(root.glob("requirements*.txt")):
        for line in lines_of(path):
            if found := requirement(line):
                yield found[0], found[1], path.name


def python_files(root):
    for folder in ("src", "tests"):
        for path in sorted((root / folder).rglob("*.py")):
            if not any(part.startswith((".", "__pycache__")) for part in path.relative_to(root).parts):
                yield path


def imports(root):
    """Yield (top-level module, file) for every absolute import; files that do not parse are skipped."""
    for path in python_files(root):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, ValueError, UnicodeDecodeError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    yield alias.name.split(".")[0], path.relative_to(root).as_posix()
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                yield node.module.split(".")[0], path.relative_to(root).as_posix()


def first_party(root):
    names = set()
    for folder in ("src", "tests"):
        base = root / folder
        if base.is_dir():
            names |= {p.stem if p.is_file() else p.name for p in base.iterdir() if p.suffix == ".py" or p.is_dir()}
    return names


def main(argv):
    root = Path(argv[1] if len(argv) > 1 else ".")
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2
    listed, aliases = read_allowlist(root)
    locked = read_lock(root)
    known = listed | locked
    own = first_party(root)
    flags = {}  # normalised name -> (display name, reason)
    checked = 0

    for name, from_url, where in declared(root):
        checked += 1
        key = normalise(name)
        if from_url:
            flags[key] = (name, f"installed from a URL ({where}), not from the package index")
        elif key not in known and key not in flags:
            flags[key] = (name, f"declared in {where} but in neither deps-allowlist.txt nor requirements.lock")
    for module, where in imports(root):
        key = normalise(module)
        if module in sys.stdlib_module_names or module in own or key in known or key in aliases or key in flags:
            continue
        flags[key] = (module, f"imported in {where} but in neither deps-allowlist.txt nor requirements.lock")

    for display, reason in sorted(flags.values()):
        print(f"FLAG {display}: {reason}")
    if flags:
        print(f"FAILED: {len(flags)} package(s) to look at before this merges")
        return 1
    print(f"OK: {checked} declared packages checked, nothing unlisted")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
