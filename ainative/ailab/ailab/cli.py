"""``python -m ailab``: list, doctor, start, grade, solve.

Exit codes: 0 success; 1 the work does not pass the grader (or doctor found a problem);
2 the command could not run (unknown lab, bad directory, broken lab).
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TextIO

from ailab import framework, gitutil
from ailab.framework import Check, LabError


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m ailab",
        description="The offline lab kit for 'A Practical Guide to Becoming an AI-Native Engineer'. "
        "It grades your work; it never runs an AI model and never uses the network.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list", help="show the labs")
    p.add_argument("--json", action="store_true", help="machine-readable output")

    p = sub.add_parser("doctor", help="check Python, git, pytest and that you can write files")
    p.add_argument("--dir", default=None, help="the directory you will work in (default: here)")

    p = sub.add_parser("start", help="create the work directory for a lab")
    p.add_argument("lab", help="lab id, for example m04")
    p.add_argument("--dir", default=None, help="where to create it (must be new or empty; default ./<lab id>)")

    p = sub.add_parser("grade", help="check your work")
    p.add_argument("lab", nargs="?", help="lab id (default: the lab this directory was started for)")
    p.add_argument("--dir", default=".", help="the work directory (default: here)")
    p.add_argument("--json", action="store_true", help="machine-readable output")

    p = sub.add_parser("solve", help="apply the reference solution (a peek: try the lab yourself first)")
    p.add_argument("lab", nargs="?")
    p.add_argument("--dir", default=".")
    p.add_argument("--force", action="store_true", help="apply even though you already changed files")
    return parser


def _quote(path: Path | str) -> str:
    """Quote a path for the learner's shell: shlex rules on Linux and macOS, double quotes on Windows."""
    return f'"{path}"' if os.name == "nt" else shlex.quote(str(path))


def grade_command(lab_id: str, work: Path) -> str:
    """The grade command for ``work`` that works from ANY directory.

    The kit is not installed as a package, so ``python -m ailab`` only finds it from the folder that
    holds the ``ailab`` package (``ainative/ailab``). Putting that folder on ``PYTHONPATH`` for the one
    command removes the restriction. Paths are absolute, so the command can be pasted anywhere.
    """
    kit = framework.KIT_DIR.parent
    if os.name == "nt":  # pragma: no cover - Windows PowerShell
        return f'$env:PYTHONPATH = "{kit}"; python -m ailab grade {lab_id} --dir "{work}"'
    return f"PYTHONPATH={_quote(kit)} python -m ailab grade {lab_id} --dir {_quote(work)}"


def _line(check: Check) -> list[str]:
    mark = "PASS" if check.ok else "FAIL"
    tag = "" if check.required else " (advisory)"
    text = f"[{mark}] {check.name}{tag}" + (f": {check.detail}" if check.detail else "")
    lines = [text]
    if not check.ok and check.hint:
        lines.append(f"       hint: {check.hint}")
    return lines


def _resolve_lab(args: argparse.Namespace, work: Path | None) -> framework.Lab:
    lab_id = args.lab
    if lab_id is None and work is not None:
        lab_id = framework.started_lab_id(work)
    if not lab_id:
        raise LabError("which lab? give its id, for example: python -m ailab grade m04 --dir <your directory>")
    lab = framework.load_lab(lab_id)
    if work is not None:
        started = framework.started_lab_id(work)
        if started and started != lab.id:
            raise LabError(f"this directory was started for {started}, not {lab.id}")
    return lab


def cmd_list(args: argparse.Namespace, out: TextIO) -> int:
    entries = framework.discover()
    if args.json:
        rows = [
            {"id": e.id, "dir": e.dirname, "broken": e.broken, "error": e.error,
             **({"title": e.lab.title, "lesson": e.lab.lesson, "needs_agent": e.lab.needs_agent} if e.lab else {})}
            for e in entries
        ]
        print(json.dumps(rows, indent=2), file=out)
        return 0
    if not entries:
        print("No labs found.", file=out)
        return 0
    print(f"{'ID':<5} {'Lesson':<7} {'Agent':<6} Title", file=out)
    for entry in entries:
        if entry.lab is None:
            print(f"{entry.id:<5} {'-':<7} {'-':<6} BROKEN ({entry.dirname}): {entry.error}", file=out)
        else:
            lab = entry.lab
            print(f"{lab.id:<5} {lab.lesson:<7} {'yes' if lab.needs_agent else 'no':<6} {lab.title}", file=out)
    return 0


def cmd_doctor(args: argparse.Namespace, out: TextIO) -> int:
    checks = framework.doctor_checks(args.dir)
    for check in checks:
        for line in _line(check):
            print(line, file=out)
    ok = framework.passed(checks)
    print("Everything needed is in place." if ok else "Fix the FAIL lines above, then run doctor again.", file=out)
    return 0 if ok else 1


def cmd_start(args: argparse.Namespace, out: TextIO) -> int:
    lab = framework.load_lab(args.lab)
    dest = Path(args.dir) if args.dir else Path.cwd() / lab.id
    work = framework.start_lab(lab, dest)
    agent = "yes" if lab.needs_agent else "no (you may still use one; the grader only looks at the result)"
    print(f"Lab {lab.id}: {lab.title} (lesson {lab.lesson})", file=out)
    print(f"Needs an agent: {agent}", file=out)
    print(f"Work directory: {work}", file=out)
    print("", file=out)
    print(lab.task_file.read_text(encoding="utf-8").rstrip(), file=out)
    print("", file=out)
    print(f"Your work directory is {work}. Edit files and run git and pytest there:", file=out)
    print(f"  cd {_quote(work)}", file=out)
    print("When you are ready, grade from any directory:", file=out)
    print(f"  {grade_command(lab.id, work)}", file=out)
    return 0


def cmd_grade(args: argparse.Namespace, out: TextIO) -> int:
    work = framework.check_work_dir(args.dir)
    lab = _resolve_lab(args, work)
    checks = framework.grade_lab(lab, work)
    required = [c for c in checks if c.required]
    done = sum(1 for c in required if c.ok)
    ok = framework.passed(checks)
    if args.json:
        payload = {
            "lab": lab.id,
            "passed": ok,
            "required_passed": done,
            "required_total": len(required),
            "checks": [
                {"name": c.name, "ok": c.ok, "detail": c.detail, "hint": c.hint, "required": c.required} for c in checks
            ],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False), file=out)
    else:
        for check in checks:
            for line in _line(check):
                print(line, file=out)
        verdict = "PASSED" if ok else "NOT YET"
        print(f"\nLab {lab.id}: {done}/{len(required)} required checks passed: {verdict}", file=out)
    return 0 if ok else 1


def cmd_solve(args: argparse.Namespace, out: TextIO) -> int:
    work = framework.check_work_dir(args.dir)
    lab = _resolve_lab(args, work)
    framework.solve_lab(lab, work, force=args.force)
    print(f"Applied the reference solution for {lab.id} in {work}.", file=out)
    print("Now grade it, from any directory:", file=out)
    print(f"  {grade_command(lab.id, work)}", file=out)
    return 0


_COMMANDS = {"list": cmd_list, "doctor": cmd_doctor, "start": cmd_start, "grade": cmd_grade, "solve": cmd_solve}


def main(argv: Sequence[str] | None = None, *, out: TextIO | None = None, err: TextIO | None = None) -> int:
    out = out or sys.stdout
    err = err or sys.stderr
    try:
        args = _parser().parse_args(argv)
    except SystemExit as exc:  # argparse printed its message
        return int(exc.code) if isinstance(exc.code, int) else 2
    try:
        return _COMMANDS[args.command](args, out)
    except LabError as exc:
        print(f"error: {exc}", file=err)
        return 2
    except gitutil.GitError as exc:
        print(f"error: git failed: {exc}", file=err)
        return 2
