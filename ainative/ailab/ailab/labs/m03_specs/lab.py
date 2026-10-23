"""Lab m03 (lesson 3.2): "Turn three vague tickets into specs an agent can build from".

The story
---------
Hessa wrote three tickets in a hurry (``lab-assets/tickets/T1.md`` to ``T3.md``). Each one hides questions that
money software must answer before anyone writes code. The learner writes ``specs/T1.md`` to ``T3.md`` on the
template ``specs/TEMPLATE.md`` (goal, context, behaviour as examples, acceptance criteria, constraints,
non-goals, decisions, risks, test plan and a plan). Nothing is built: the spec is the deliverable.

* T1 REMIT-341, 15% off the fee to Egypt: the express surcharge, the minimum fee, a rounding tie, and "Egypt"
  (a corridor) versus the fee schedule it shares with Pakistan.
* T2 REMIT-342, type what the family receives: the currency of the typed number, the direction of the rounding,
  a fee-tier boundary crossed by one hundredth, the corridor limits on the derived amount.
* T3 REMIT-343, cash pickup after the cut-off: whose 6pm, the exact second, what "tomorrow" means, which
  deliveries are affected, the Arabic sentence (written, or its supplier named) and its digits.

What is graded, and what cannot be
----------------------------------
The grader (``ailab/checks_m03.py``) reads the specs as a reviewer would: the sections, the placeholders and
filler, worked examples (exact amounts, times or dates in any common form), checkable acceptance criteria, files that
exist (or are said to be new), the hidden ambiguities (keyword groups, tolerant of wording; one sentence resolves one of
them; a question is not an answer; any section may answer, at least half in Decisions), the house rules of
CONTRIBUTING.md, a second reviewer for money logic, copies, and a plan of small numbered steps (test first, a pytest run,
a rollback). It never runs an agent and never runs learner code, and it cannot tell whether a decision is right,
whether the Arabic is good Arabic, whether the examples are correct or who wrote the file.

Files
-----
    seed(work)    writes ``specs/TEMPLATE.md`` and the agent-log template; the tickets and Hessa's notes arrive in
                  ``lab-assets/`` from ``assets/``.
    grade(work)   pure Python plus one pytest run on a copy; it never imports learner code.
    solve(work)   copies the reference specs into place, one commit per spec, and a log entry.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from ailab import checks, checks_m03, gitutil
from ailab.framework import Check, Lab

HERE = Path(__file__).resolve().parent
LEARNER = ("Najm Learner", "learner@najm.example")


def seed(work: Path) -> None:
    """The starting situation is the base repository plus the spec template and an empty agent log."""
    work = Path(work)
    (work / checks_m03.SPEC_DIR).mkdir(exist_ok=True)
    shutil.copyfile(HERE / "templates" / "spec-template.md", work / checks_m03.TEMPLATE_FILE)
    shutil.copyfile(HERE / "templates" / "agent-log.md", work / checks_m03.LOG_FILE)


COMMIT_HINT = ("Use `type(scope): subject` from CONTRIBUTING.md; any lower-case scope works, for example "
               "docs(specs): write the three specs. `git commit --amend` fixes only the newest message; to redo several, "
               "run `git reset --soft lab-start` and commit again.")
NO_COMMIT_HINT = ("Commit the specs, for example `git add -A && git commit -m \"docs(specs): write the three specs\"` "
                  "(type(scope): subject, as CONTRIBUTING.md says).")


def commit_check(work: Path) -> Check:
    """The kit's commit check, with hints that fit this lab (it commits specs, and a message may be several commits back)."""
    check = checks.conventional_commits(work, name=checks_m03.N_COMMITS)
    if not check.ok:
        check.hint = NO_COMMIT_HINT if check.detail.startswith("found 0 commit") else COMMIT_HINT
    return check


def grade(work: Path) -> list[Check]:
    return [
        checks.files_changed_within(
            work,
            checks_m03.ALLOWED_FILES,
            name=checks_m03.N_SCOPE,
            require_change=False,
            hint="This lab changes specs/ and agent-log.md only. Writing the spec is the job; building it is the next "
                 "module's. Undo a file you edited with `git restore --source=lab-start <file>` (committed or not) and delete "
                 "a file you added, then commit the undo.",
        ),
        checks.tests_pass(work, name=checks_m03.N_TESTS),
        *checks_m03.spec_checks(work),
        commit_check(work),
        checks.all_committed(work, name=checks_m03.N_CLEAN),
        checks.no_secrets(work),
    ]


def solve(work: Path) -> None:
    """The reference solution: one commit per spec, then the agent log."""
    work = Path(work)
    for ticket, subject, date in (
        ("T1", "docs(specs): spec the Egypt fee discount", "2026-03-02T10:00:00+00:00"),
        ("T2", "docs(specs): spec the reverse quote", "2026-03-02T11:00:00+00:00"),
        ("T3", "docs(specs): spec the cash pickup note", "2026-03-02T12:00:00+00:00"),
    ):
        shutil.copyfile(HERE / "solution" / f"{ticket}.md", work / checks_m03.SPEC_DIR / f"{ticket}.md")
        gitutil.commit_all(work, subject, author=LEARNER, date=date)
    shutil.copyfile(HERE / "solution" / "agent-log.md", work / checks_m03.LOG_FILE)
    gitutil.commit_all(work, "docs(specs): log how the specs were written", author=LEARNER, date="2026-03-02T13:00:00+00:00")


LAB = Lab(
    id="m03",
    title="Specs an agent can build from: three vague tickets",
    lesson="3.2",
    needs_agent=False,  # an agent can interview you or review a draft, but the task is doable by hand and the grader cannot tell
    seed=seed,
    grade=grade,
    solve=solve,
)
