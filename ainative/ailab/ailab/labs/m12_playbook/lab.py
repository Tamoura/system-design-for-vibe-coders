"""Lab m12 (lesson 12.2): "Write the team's AI engineering playbook".

The story
---------
Payments Platform has no written AI practice. Everyone uses the tools a little differently, and the bank's
six rules and ``CONTRIBUTING.md`` say what must hold but not how the team makes it so. Tariq asks for
``playbook.md``: ten sections, rules that can be checked, concrete review norms and a metrics plan with
definitions two people could compute the same way.

What is graded, and what cannot be
----------------------------------
The grader is a *lint* (``ailab/checks_m12.py``) of one Markdown file. It never needs an agent and it
cannot tell who or what wrote the file. It asks:

* are the ten sections there, with substance and no template text left?
* are there at least twelve rules in the ``MUST ... Check: ...`` shape, spread over the areas that need
  them, each with a mechanism and none with a weasel word?
* are the review norms concrete: the label, a diff limit in lines, the second human for the six money
  modules, a response time, what the author explains?
* do the sections say the specific things a good one says (tools, data, memory, verification, security,
  automation, incident, onboarding)?
* is the metrics plan measurable: six fields per ``###`` block, three DORA-style delivery metrics, a guard
  with a threshold and a response, definitions with events and periods, baselines from the facts file,
  no vanity measures?
* is it honest: nothing that contradicts the bank's rules or CONTRIBUTING.md, no files that do not exist,
  no unsourced productivity claims?
* is the change clean: only ``playbook.md`` changed, no secrets, Conventional Commits, all committed?

It does NOT judge whether the policy is wise or whether the team will follow it. A playbook that passes
can still be a bad one; the group session is where people argue about that.

Files
-----
    seed(work)    writes the skeleton ``playbook.md`` at the repository root; the facts arrive in
                  ``lab-assets/team-context.md`` from ``assets/``.
    grade(work)   pure Python on the learner's files and git; it never imports learner code.
    solve(work)   copies ``solution/playbook.md`` into place and commits it (one commit).
"""
from __future__ import annotations

import shutil
from pathlib import Path

from ailab import checks_m12, gitutil
from ailab.framework import Check, Lab

HERE = Path(__file__).resolve().parent
LEARNER = ("Najm Learner", "learner@najm.example")
COMMIT_MESSAGE = "docs(playbook): write the Payments Platform AI engineering playbook"


def seed(work: Path) -> None:
    """The starting situation: the base repository plus the playbook skeleton."""
    shutil.copyfile(HERE / "templates" / "playbook.md", Path(work) / checks_m12.PLAYBOOK_FILE)


def grade(work: Path) -> list[Check]:
    return checks_m12.all_checks(work)


def solve(work: Path) -> None:
    """The reference solution, in one commit."""
    work = Path(work)
    shutil.copyfile(HERE / "solution" / "playbook.md", work / checks_m12.PLAYBOOK_FILE)
    gitutil.commit_all(work, COMMIT_MESSAGE, author=LEARNER, date="2026-03-02T10:00:00+00:00")


LAB = Lab(
    id="m12",
    title="The team's AI engineering playbook: rules you can check, metrics you can compute",
    lesson="12.2",
    needs_agent=False,  # an assistant can draft it; the grader never runs one and cannot tell
    seed=seed,
    grade=grade,
    solve=solve,
)
