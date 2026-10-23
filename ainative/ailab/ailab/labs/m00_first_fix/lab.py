"""Lab m00 (lesson 0.2): "First fix". THE EXEMPLAR LAB: copy this folder when you write a new one.

The story
---------
A one-word typo ("recieved") has crept into the English "transfer sent" notification. The repo's
own tests already describe the right text, so they fail. The learner finds the typo (by hand or with
an agent), fixes it, runs the tests, and commits with a Conventional Commits message as the repo's
CONTRIBUTING.md requires. It is the smallest possible lap of the whole loop.

How a lab is put together (every lab has these)
-----------------------------------------------
    lab.py        this file: defines ``LAB = Lab(...)`` with seed / grade / solve
    task.md       the ticket the learner sees (also copied to TASK.md in their work directory)
    assets/       (optional) files copied to ``lab-assets/`` in the work directory; m00 has none
    hidden/       (optional) hidden pytest files, run by the grader against the learner's code
    solution/     the reference solution's data files (here: a patch and a commit message)

The three functions
-------------------
seed(work)   Runs once inside ``ailab start``, after the base repository has been copied and
             committed as "Initial state". Edit/add files here; do NOT commit (the framework commits
             everything as "Lab starting state" and tags it ``lab-start``).
grade(work)  Returns a list of ``Check``. Called by ``ailab grade``. It must not change ``work``
             and must run learner code only in a subprocess (the ``checks`` helpers do that).
solve(work)  Produces a state that passes grade(), including any commits the grader requires. The
             kit's tests run start -> grade (must FAIL) -> solve -> grade (must PASS) for every lab.

Habits worth copying
--------------------
* Grade behaviour through the public interface the ticket names, not through your own solution.
* Give every check a short name, a ``detail`` the learner can act on and a ``hint`` that nudges
  without revealing the answer.
* Be deterministic and fast (the whole lab, start to solved, must take well under 20 seconds).
* Write negative tests (tests/test_labs_m00.py) for the wrong answers people really produce.
* Every rule the grader enforces is written in task.md or the lesson (type, scope, branch, "no new tests"),
  and a hint never contradicts what the learner did. A first lab's hints are the most-read text in the course:
  ``checks_m00.py`` shows how to make them depend on the actual state (the other branch that holds the commit,
  which hidden test failed).
"""
from __future__ import annotations

import tempfile
from pathlib import Path

from ailab import checks, checks_m00, framework, gitutil
from ailab.framework import Check, Lab

HERE = Path(__file__).resolve().parent

# The one file a correct fix touches.
TEMPLATE_FILE = checks_m00.TEMPLATE_FILE

# The English "transfer sent" sentence, before and after the typo is planted.
CORRECT = "{recipient} received {receive_amount}. "
TYPO = "{recipient} recieved {receive_amount}. "


# ---------------------------------------------------------------------------------------------
# seed: make the starting situation
# ---------------------------------------------------------------------------------------------
def seed(work: Path) -> None:
    """Plant the typo. ``edit_file`` insists the text occurs exactly once, so if the base repo ever
    changes under this seed, the lab fails loudly at ``start`` instead of silently doing nothing."""
    framework.edit_file(work, TEMPLATE_FILE, CORRECT, TYPO)


# ---------------------------------------------------------------------------------------------
# grade: look at the learner's work and say what is right and what is not
# ---------------------------------------------------------------------------------------------
def grade(work: Path) -> list[Check]:
    # The 0.2 lesson starts with `ailab doctor`, so the grader also confirms the environment. (The temp
    # directory is the "writable folder" probe: grading must not depend on, or write into, the learner's folder.)
    env_ok = framework.passed(framework.doctor_checks(tempfile.gettempdir()))

    results = [
        Check(
            "Your environment passes `ailab doctor`",
            env_ok,
            "" if env_ok else "python -m ailab doctor reports a problem",
            "Run python -m ailab doctor and fix the FAIL lines.",
        ),
        # 1. The repo's own (visible) tests, run on a throw-away copy in a subprocess.
        checks.tests_pass(
            work,
            hint="Run `pytest -q` in your lab directory (not the ailab folder) and read the first failure from the top.",
        ),
        # 2. The hidden acceptance tests in hidden/: they test the customer-visible text, so any sound way of
        #    fixing it passes. The hint depends on WHICH hidden test failed (checks_m00.hidden).
        checks_m00.hidden(work, HERE / "hidden"),
        # 3. The tests were not "fixed" by weakening them, and no test was added either (the ticket says so).
        checks.files_unchanged(
            work,
            ["tests/**"],
            name=checks_m00.NAME_UNEDITED,
            hint="The ticket says do not add or edit tests. Undo every change under tests/ (edited, added or "
                 "deleted files; `git diff lab-start --stat -- tests` lists them) and fix the message instead.",
        ),
        # 4. Scope: only the template file may change.
        checks.files_changed_within(
            work,
            [TEMPLATE_FILE],
            name="Only the template file changed",
            hint="Only the file that holds the message should change. `git diff lab-start --stat` lists what you "
                 "changed; undo the rest.",
        ),
        # 5. Size: the file must equal the starter with the one misspelling corrected (and at most 6 changed lines).
        checks_m00.tiny(work),
        # 6. Commit hygiene: exactly one new commit (merge commits are not counted), whose message follows
        #    CONTRIBUTING.md and fits this ticket (type fix, scope = the module).
        checks_m00.one_commit(work),
        checks_m00.message(work),
        checks_m00.left_over(work),
        # 7. Safety net used by every lab.
        checks.no_secrets(work),
    ]
    # Graded from the wrong branch (the commit is on the task branch, `main` is checked out): say so on every line.
    branch = checks_m00.wrong_branch(work)
    return checks_m00.point_at_branch(results, branch) if branch else results


# ---------------------------------------------------------------------------------------------
# solve: the reference solution (used by the kit's own tests, and as a peek for stuck learners)
# ---------------------------------------------------------------------------------------------
def solve(work: Path) -> None:
    """Apply solution/fix.patch and commit it with the message in solution/commit_message.txt.

    A patch is one way to ship a solution; calling ``framework.edit_file(work, TEMPLATE_FILE, TYPO,
    CORRECT)`` would be just as good. The solution must include the commit, because the grader asks
    for exactly one."""
    gitutil.apply_patch(work, HERE / "solution" / "fix.patch")
    message = (HERE / "solution" / "commit_message.txt").read_text(encoding="utf-8").strip()
    gitutil.commit_all(work, message, author=("Najm Learner", "learner@najm.example"), date="2026-03-02T09:30:00+00:00")


LAB = Lab(
    id="m00",
    title="Your first fix: a typo, the tests, a commit",
    lesson="0.2",
    needs_agent=False,  # an agent can help, but the task is easy by hand; the grader cannot tell
    seed=seed,
    grade=grade,
    solve=solve,
)
