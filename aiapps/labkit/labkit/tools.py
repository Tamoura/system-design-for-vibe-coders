"""Small, safe tool implementations used by the labs. Fake data only."""
from __future__ import annotations

import ast
import json
import operator
from pathlib import Path

DATA = Path(__file__).parent / "data"
TICKETS = json.loads((DATA / "tickets.json").read_text(encoding="utf-8"))
EMPLOYEES = json.loads((DATA / "employees.json").read_text(encoding="utf-8"))


def get_ticket_status(ticket_id: str) -> str:
    t = TICKETS.get(str(ticket_id))
    return f"Ticket {t['id']}: {t['status']} ({t['category']}, {t['priority']}): {t['summary']}" if t else f"No ticket {ticket_id} found"


_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Pow: operator.pow,
        ast.USub: operator.neg, ast.Mod: operator.mod}


def calculator(expression: str) -> str:
    """Evaluate + - * / ** % and parentheses on numbers. Anything else is refused (never use eval on model output)."""
    def ev(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](ev(node.operand))
        raise ValueError("unsupported expression")
    try:
        return str(ev(ast.parse(expression, mode="eval").body))
    except (ValueError, SyntaxError, ZeroDivisionError) as e:
        return f"Error: {e}"


def get_weather(city: str) -> str:
    fake = {"Doha": "39 C, clear", "Dubai": "41 C, humid", "Paris": "17 C, light rain"}
    return fake.get(city, f"No forecast for {city}")


def lookup_employee(name: str) -> str:
    for e in EMPLOYEES:
        if e["name"].lower() == name.lower():
            return f"{e['name']}: {e['team']}, {e['email']}"
    return f"No employee named {name}"
