"""PostToolUse hook for Najm Remit: check the Python file an agent has just edited.

Claude Code runs this after a successful Edit or Write and writes one JSON document to standard input.
Exit 0: nothing to report. Exit 2: the work is wrong, and standard error tells the agent what.
Exit 1: this hook is broken (unreadable input); the agent is not blamed and carries on.

Two rules: a .py file must parse, and a file under src/remit/ must not contain a float (money is Decimal).
"""
import ast
import json
import os
import sys
from pathlib import Path


def project_root(document):
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or document.get("cwd") or os.getcwd()).resolve()


def float_findings(tree):
    """Float literals and calls of float(); mentions in comments, strings and isinstance() are not findings."""
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, float):
            found.append((node.lineno, f"the float literal {node.value!r}"))
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "float":
            found.append((node.lineno, "a call to float()"))
    return sorted(found)


def check_file(path, root):
    if path.suffix != ".py" or not path.is_file():
        return None
    try:
        tree = ast.parse(path.read_bytes(), filename=str(path))
    except (SyntaxError, ValueError) as problem:
        line = getattr(problem, "lineno", None) or 0
        return f"{path.name}:{line}: this file does not parse ({getattr(problem, 'msg', problem)}). Fix the syntax."
    if (root / "src" / "remit") in path.parents:
        found = float_findings(tree)
        if found:
            lines = "; ".join(f"line {number}: {what}" for number, what in found[:5])
            return f"{path.name}: float in money code ({lines}). Money is Decimal, never float: use Money or Decimal('...')."
    return None


def main():
    try:
        document = json.load(sys.stdin)
        raw = document["tool_input"].get("file_path")
    except (ValueError, KeyError, TypeError, AttributeError):
        print("post_edit: could not read the hook input", file=sys.stderr)
        sys.exit(1)  # the hook's problem, not the agent's
    if not isinstance(raw, str) or not raw:
        sys.exit(0)
    cwd = document.get("cwd")
    base = Path(cwd) if isinstance(cwd, str) and cwd else Path.cwd()
    root = project_root(document)
    path = Path(raw)
    path = (path if path.is_absolute() else base / path).resolve()
    problem = check_file(path, root)
    if problem:
        print(problem, file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
