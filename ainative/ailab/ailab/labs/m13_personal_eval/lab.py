"""Lab m13 (lesson 13.2): "Your personal eval and your 90-day plan".

The story
---------
Tariq asks the learner for two things to keep: a small eval of their own (eight or more tasks, each with a check that
a script can run) and a 90-day plan with measurable goals. There is nothing to repair, so the seed plants nothing: the
learner starts from the Remit repository as it is, plus ``lab-assets/`` (the runner, a plan template and four worked
example tasks) and ``TASK.md``.

What the grader does (see ``ailab/checks_m13.py``)
--------------------------------------------------
* eval/tasks.jsonl: valid JSON Lines, at least eight different tasks (copies count once, the course's examples not at
  all, tasks from the learner's own project do), at least six of them about the Remit repository, well-formed fields;
* it RUNS the checks it can, in throw-away copies of the ``lab-start`` state (a git repository with one commit): every
  check must be runnable, must FAIL on the untouched repository, every guard must PASS there, every Remit task must have
  a reference that makes its check pass, and lazy answers must not (a placeholder, filler text, the prompt handed back,
  a test that asserts nothing, a stray edit): the same logic the learner has in ``lab-assets/eval_runner.py``;
* plan.md: required sections, a start date, a skills map, a realistic weekly routine, measurable goals;
* the repository: only eval/ and plan.md changed, committed in steps, CONTRIBUTING.md commit messages, no secrets.

What it cannot do: judge whether the tasks are the right ones, whether a check measures what its prompt asks (only that
it fails on nothing and passes on the reference), or whether the plan is wise.

The reference solution is in ``solution/`` (an eval with nine tasks, the checks, the patches, and plan.md). It is
never shown in the lesson.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from ailab import checks_m13, gitutil
from ailab.framework import Check, Lab

HERE = Path(__file__).resolve().parent
LEARNER = ("Najm Learner", "learner@najm.example")


def seed(work: Path) -> None:
    """Nothing to plant. The learner builds new files; the framework adds lab-assets/ and TASK.md."""


def grade(work: Path) -> list[Check]:
    return checks_m13.grade(work)


def solve(work: Path) -> None:
    """Copy the reference eval and plan in, as two commits (the eval, then the plan)."""
    source = HERE / "solution"
    shutil.copytree(source / "eval", work / "eval", dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    gitutil.commit_all(work, "test(eval): add a personal eval for Najm Remit", author=LEARNER, date="2026-11-02T09:30:00+00:00")
    shutil.copyfile(source / "plan.md", work / "plan.md")
    gitutil.commit_all(work, "docs(plan): add my 90-day plan", author=LEARNER, date="2026-11-02T10:00:00+00:00")


LAB = Lab(
    id="m13",
    title="Your personal eval and your 90-day plan",
    lesson="13.2",
    needs_agent=False,  # an agent can write tasks, checks and patches; the grader looks at the result
    seed=seed,
    grade=grade,
    solve=solve,
)
