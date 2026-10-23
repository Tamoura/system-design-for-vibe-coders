"""Lab m02 (lesson 2.2): "Write the project memory for Najm Remit and measure what it changes".

The story
---------
Remit has no ``CLAUDE.md``: every AI session on it starts from nothing, and every engineer re-types the same
paragraph. The learner writes the project memory (``CLAUDE.md``, or ``AGENTS.md``), then runs a second, small
ticket (REMIT-252, in ``lab-assets/ab-task.md``) twice, once without the memory and once with it, in two
throw-away copies, and records the difference in ``ab-notes.md``.

What is graded, and what cannot be
----------------------------------
The grader is a *lint* (``ailab/checks_m02.py``) plus a structure check on the notes. It never needs an agent,
and it cannot tell who or what wrote the file. It reads the memory the way a reviewer would:

* size band (imports count, because an import does not save context);
* the documented commands are EXECUTED, in a throw-away copy, and must exit 0 (``pytest ...`` and
  ``python -m remit ...`` only, as argument lists, never through a shell); commands for tools this repository
  does not have (make, npm, ruff ...) fail;
* conventions that match the repo: Decimal money, the test layout, the exact commit rule, najmkit;
* a short never-do list that names things true of this repository;
* every path it mentions exists (the trap: docs/ARCHITECTURE.md still describes a module that is gone);
* nothing stale copied from that document, no claim the code contradicts (rounding, decimal places, the ledger, the
  clock, dependencies), no filler, no restating of the docs;
* no credentials, customer data, invisible characters or instructions to ignore rules or fetch and run code (the kit's
  own ``checks.no_secrets`` also scans the diff for provider key formats).

It does NOT judge whether the file is *useful*: usefulness is what the A/B experiment is for, and the grader
cannot see the experiment. The notes are checked for completeness and for quoting real lines of the memory,
never for "B beat A": a grader that rewarded improvement would reward invented improvements.

Files
-----
    seed(work)    writes the notes template ``ab-notes.md`` at the repository root; the second ticket arrives in
                  ``lab-assets/ab-task.md`` from ``assets/``.
    grade(work)   pure Python plus subprocesses on a copy; it never imports learner code.
    solve(work)   copies ``solution/CLAUDE.md`` and ``solution/ab-notes.md`` into place, in two commits. The
                  reference CLAUDE.md is also what ``framework.add_reference_memory`` gives to later labs.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from ailab import checks, checks_m02, gitutil
from ailab.framework import Check, Lab

HERE = Path(__file__).resolve().parent
LEARNER = ("Najm Learner", "learner@najm.example")


def seed(work: Path) -> None:
    """The starting situation is the base repository plus a notes template the learner has to fill in."""
    shutil.copyfile(HERE / "templates" / "ab-notes.md", Path(work) / checks_m02.NOTES_FILE)


def grade(work: Path) -> list[Check]:
    return [
        checks.tests_pass(work, name="Your tests still pass"),
        checks.files_changed_within(
            work,
            checks_m02.ALLOWED_FILES,
            name="Only the memory file(s) and the notes changed",
            hint="This lab changes the memory file (CLAUDE.md or AGENTS.md, plus optional .claude/rules) and ab-notes.md "
                 "only; docs/ and .claude/settings.json count as unrelated too (a deny rule is lab m08's job). If you found a "
                 "mistake in a document, write it down for another ticket instead of fixing it here.",
        ),
        *checks_m02.memory_checks(work),
        checks.no_secrets(work),
        *checks_m02.notes_checks(work),
        checks.conventional_commits(work, name="Your commits follow CONTRIBUTING.md"),
        checks.all_committed(work, name="Everything is committed (nothing left over)"),
    ]


def solve(work: Path) -> None:
    """The reference solution: the memory first, the notes after the experiment, one commit each."""
    work = Path(work)
    shutil.copyfile(HERE / "solution" / "CLAUDE.md", work / "CLAUDE.md")
    gitutil.commit_all(work, "docs(memory): add CLAUDE.md for coding agents", author=LEARNER, date="2026-03-02T10:00:00+00:00")
    shutil.copyfile(HERE / "solution" / "ab-notes.md", work / checks_m02.NOTES_FILE)
    gitutil.commit_all(work, "docs(notes): record the memory A/B comparison", author=LEARNER, date="2026-03-02T11:00:00+00:00")


LAB = Lab(
    id="m02",
    title="Project memory for Remit: write it, lint it, measure it",
    lesson="2.2",
    needs_agent=True,  # the A/B part is built around an agent (a stand-in is allowed); the grader never runs one
    seed=seed,
    grade=grade,
    solve=solve,
)
