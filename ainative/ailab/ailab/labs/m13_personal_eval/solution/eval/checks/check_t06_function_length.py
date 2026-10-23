"""T06: no function in src/remit/service.py is longer than 70 lines (send is 89 today)."""
import ast
import pathlib
import sys

LIMIT = 70
tree = ast.parse(pathlib.Path("src/remit/service.py").read_text(encoding="utf-8"))
long = [(node.name, node.end_lineno - node.lineno + 1) for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.end_lineno - node.lineno + 1 > LIMIT]
if long:
    sys.exit("too long: " + ", ".join(f"{name} ({lines} lines)" for name, lines in long))
