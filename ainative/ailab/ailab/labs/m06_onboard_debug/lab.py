"""Lab m06 (lesson 6.2): "Onboard to the codebase and fix a production bug from its logs".

The story
---------
Part 1. The learner is new to the Payments Platform team. Before touching money logic they write
``docs/onboarding.md``: a short tour of the Remit repository (graded structurally, and against facts the
code can confirm: the files exist, the transfer steps are in the order the code runs them, nothing is
invented, the stale claims in docs/ARCHITECTURE.md are not repeated).

Part 2. A production bug. A refactor released on 12 March replaced Qatar time with UTC in the two window
helpers of ``remit/limits.py``, so the "day" and the "month" of the limits begin at 00:00 UTC (03:00 in Qatar)
instead of 00:00 in Qatar. Customers are refused just after Qatar midnight, and (the direction nobody has
noticed) some are let through over their limit in the small hours. The refactor also deleted the four tests
that would have caught it, so the starter suite is GREEN: the learner has to reproduce the problem with a
test of their own, from ``lab-assets/prod.log`` and the incident note, then fix it minimally, keep the test as
the regression test, and write the root-cause note.

The seed builds a small believable history (six commits after "Initial state"), in which the bad commit is
not the one that looks most suspicious (a behaviour-preserving refactor of ``month_window`` sits just before
it), so that ``git bisect`` with the learner's own reproduction test is worth doing.

What the grader can and cannot tell
-----------------------------------
It checks the RESULT: hidden boundary tests over a whole week of instants; that the learner's tests fail on the
starter code, notice the daily defect and (advisory) the monthly one, and pass on the fix; that no existing test
was edited; that the fix is a few lines in limits.py; that the tour and the note exist, have their sections and
are consistent with the repository; commit hygiene. It cannot tell whether the learner understood, whether an
agent wrote the tour, or whether the note is *good*. The facts it can check, it checks.

Files
-----
    lab.py                this file
    task.md               the ticket (REMIT-231) as Hessa wrote it
    make_prod_log.py      author tool: rebuilds assets/prod.log by running the real service (not given to learners)
    assets/               incident.md, prod.log, kyc_tiers.csv, redact_log.py, README.md  -> lab-assets/ in the learner's repo
    hidden/               hidden acceptance tests
    solution/             the reference solution (tour, test, note, agent log)
    ../../checks_m06.py   the grader helpers for this lab
"""
from __future__ import annotations

import re
from pathlib import Path

from ailab import checks, checks_m06 as m06, framework, gitutil
from ailab.framework import Check, Lab
from ailab.labs.m06_onboard_debug import make_prod_log as prodlog

HERE = Path(__file__).resolve().parent
LIMITS = m06.LIMITS_FILE
TESTS_LIMITS = "tests/test_limits.py"

# The four boundary tests the bad commit deletes (KIT_NOTES section 8 names them).
REMOVED_TESTS = (
    "test_the_day_ends_at_midnight_in_qatar_not_in_utc",
    "test_a_transfer_after_qatar_midnight_but_before_utc_midnight_belongs_to_the_new_day",
    "test_the_month_changes_at_midnight_in_qatar",
    "test_windows_are_local_calendar_windows",
)
OLD_IMPORT = """from remit.limits import (
    DAILY_EXCEEDED,
    LIMITS,
    MONTHLY_EXCEEDED,
    QATAR_TZ,
    check_limits,
    day_window,
    month_window,
    to_local,
)
"""
NEW_IMPORT = "from remit.limits import DAILY_EXCEEDED, LIMITS, MONTHLY_EXCEEDED, check_limits\n"

# Where the files that the learner may touch live.
ALLOWED = [LIMITS, "tests/**", "docs/**", "scripts/**", "CLAUDE.md", "AGENTS.md", ".claude/**"]


# ---------------------------------------------------------------------------------------------
# seed: a short history, and in it the commit that breaks the limits
# ---------------------------------------------------------------------------------------------
def _ci_timeout(work: Path) -> None:
    framework.edit_file(work, ".github/workflows/ci.yml", "    runs-on: ubuntu-latest\n",
                        "    runs-on: ubuntu-latest\n    timeout-minutes: 10\n")


def _fees_example(work: Path) -> None:
    framework.edit_file(
        work, "src/remit/fees.py",
        'in QAR, the send currency of every corridor today.\n"""',
        "in QAR, the send currency of every corridor today.\n\n"
        "Example: 500.00 QAR on STD-A (QAR to INR) costs 12.00, or 27.00 with express.\n\"\"\"",
    )


def _month_end_refactor(work: Path) -> None:
    """A refactor that changes no behaviour (it is a decoy: it touches the same function as the bug)."""
    framework.edit_file(
        work, LIMITS,
        "    if start.month == 12:\n"
        "        end = start.replace(year=start.year + 1, month=1)\n"
        "    else:\n"
        "        end = start.replace(month=start.month + 1)\n"
        "    return start, end\n",
        "    # Day 1 plus 32 days is always in the next month; snap back to its first day.\n"
        "    end = (start + timedelta(days=32)).replace(day=1)\n"
        "    return start, end\n",
    )


def _drop_function(text: str, name: str) -> str:
    """Remove the top-level function ``name`` (and the blank lines before it) from a module's text."""
    marker = f"\n\n\ndef {name}("
    if text.count(marker) != 1:
        raise framework.LabError(f"the base tests changed: expected exactly one {name} in {TESTS_LIMITS}")
    start = text.index(marker)
    following = text.find("\n\n\ndef ", start + 3)
    end = following if following != -1 else len(text.rstrip("\n"))
    return text[:start] + text[end:]


def _simplify_window_helpers(work: Path) -> None:
    """THE BAD COMMIT: both helpers now work in UTC, and the four tests that pinned Qatar midnight are gone."""
    framework.edit_file(work, LIMITS, m06.GOOD_CONVERSION, m06.BAD_CONVERSION, count=2)
    text = framework.read_file(work, TESTS_LIMITS)
    for name in REMOVED_TESTS:
        text = _drop_function(text, name)
    if text.count(OLD_IMPORT) != 1:
        raise framework.LabError(f"the base tests changed: the import block of {TESTS_LIMITS} is not what the seed expects")
    framework.write_file(work, TESTS_LIMITS, text.replace(OLD_IMPORT, NEW_IMPORT))


def _readme_single_file(work: Path) -> None:
    framework.edit_file(work, "README.md", "pytest -q\n```\n\nPython 3.11 or newer.",
                        "pytest -q\npytest -q tests/test_fees.py   # one file\n```\n\nPython 3.11 or newer.")


def _ci_concurrency(work: Path) -> None:
    framework.edit_file(work, ".github/workflows/ci.yml", "\njobs:\n",
                        "\nconcurrency:\n  group: ci-${{ github.ref }}\n  cancel-in-progress: true\n\njobs:\n")


SALEM = ("Salem", "salem@najm.example")
NADA = ("Nada", "nada@najm.example")
TARIQ = ("Tariq", "tariq@najm.example")
LUJAIN = ("Lujain", "lujain@najm.example")

# (author, ISO date, commit message, the change). Oldest first. The dates follow "Initial state" (2 March 2026).
HISTORY = (
    (SALEM, "2026-03-03T07:42:10+00:00", "ci(ci): stop runaway test jobs after ten minutes", _ci_timeout),
    (NADA, "2026-03-04T09:15:30+00:00", "docs(fees): add a worked example to the module docstring", _fees_example),
    (TARIQ, "2026-03-05T11:02:44+00:00", "refactor(limits): compute the month end without the December branch", _month_end_refactor),
    (LUJAIN, "2026-03-10T10:48:05+00:00",
     "refactor(limits): simplify the window helpers and their tests\n\nSmaller code to review next time. Tests still green.",
     _simplify_window_helpers),
    (TARIQ, "2026-03-11T08:20:12+00:00", "docs(readme): show how to run a single test file", _readme_single_file),
    (SALEM, "2026-03-12T06:55:31+00:00", "ci(ci): cancel superseded runs on the same branch", _ci_concurrency),
)


def seed(work: Path) -> None:
    """Replay the history. Every edit is strict (``edit_file``), so if the base ever changes the seed fails loudly."""
    for author, date, message, change in HISTORY:
        change(work)
        gitutil.commit_all(work, message, author=author, date=date)


# ---------------------------------------------------------------------------------------------
# grade
# ---------------------------------------------------------------------------------------------
def grade(work: Path) -> list[Check]:
    new_tests = checks.new_test_files(work)
    result: list[Check] = []

    # --- Part 1: the tour --------------------------------------------------------------------------------------
    result += m06.onboarding_checks(work)

    # --- Part 2: the fix and the tests -------------------------------------------------------------------------
    result += [
        checks.tests_pass(work, name="Your tests pass (the old ones and yours)"),
        checks.hidden_tests_pass(
            work, HERE / "hidden",
            name="The limits behave as limits.py documents them",
            reveal="count",  # the names of the hidden tests would give the answer away
            hint="Re-read the incident note and limits.py. What exactly did the customers see, and which code decides it?",
        ),
        checks.tests_fail_on_starter(
            work, new_tests or None,
            name="Your new tests fail on the original code",
            hint="Reproduce first: a test that passes before the fix proves nothing. Write one that fails today, for the reason in the incident note.",
        ),
        m06.variant_check(
            work, name="Your tests notice the daily-limit problem", fix_day=False, fix_month=True, required=True,
            success="your tests fail when the daily limit is still wrong",
            failure="your tests do not notice the daily-limit problem from the incident note",
            hint="Your test must reproduce what the customers reported, on the daily limit, with moments taken from prod.log.",
        ),
        m06.variant_check(
            work, name="Your tests catch every place the defect lives", fix_day=True, fix_month=False, required=False,
            success="your tests fail when the defect is left in its second place",
            failure="your tests pass when the defect is still present in a second place",
            hint="When one line is wrong, look for its twin: where else does the code make the same mistake? Test that too.",
        ),
        m06.tests_not_weakened(work),
        checks.files_unchanged(work, ["tests/conftest.py"], name="The shared test fixtures were not edited",
                               hint="The fixtures are right. Undo your edit (git restore tests/conftest.py)."),
        checks.files_changed_within(
            work, ALLOWED, name="Only the expected files changed",
            hint="The fix belongs in the code, tests in tests/, writing in docs/, a helper script in scripts/. Revert the rest (git restore <file>).",
        ),
        m06.fix_is_small(work),
        *m06.root_cause_checks(work, prodlog.WRONGLY_REFUSED, prodlog.WRONGLY_ALLOWED),
    ]

    # --- hygiene -------------------------------------------------------------------------------------------------
    result += [
        checks.commit_count(
            work, at_least=2, at_most=10, name="You made at least two commits",
            hint="Commit as you go: the tour is one logical change, the fix with its regression test another, the note a third (CONTRIBUTING.md).",
        ),
        checks.conventional_commits(work, min_commits=2),
        checks.all_committed(work, name="Everything is committed (nothing left over)"),
        m06.one_concern_per_commit(work),
        checks.no_secrets(work),
        m06.agent_log_check(work),
    ]
    return result


# ---------------------------------------------------------------------------------------------
# solve: three commits - the tour, the fix with its regression tests, the note (and the agent log)
# ---------------------------------------------------------------------------------------------
SOLUTION = HERE / "solution"
LEARNER = ("Najm Learner", "learner@najm.example")


def solve(work: Path) -> None:
    framework.write_file(work, m06.ONBOARDING, (SOLUTION / "onboarding.md").read_text(encoding="utf-8"))
    gitutil.commit_all(work, "docs(onboarding): add a tour of the Remit repository", author=LEARNER,
                       date="2026-03-18T08:30:00+00:00")

    framework.edit_file(work, LIMITS, m06.BAD_CONVERSION, m06.GOOD_CONVERSION, count=2)
    framework.write_file(work, "tests/test_limits_qatar_midnight.py",
                         (SOLUTION / "test_limits_qatar_midnight.py").read_text(encoding="utf-8"))
    gitutil.commit_all(work, "fix(limits): start the day and the month at midnight in Qatar", author=LEARNER,
                       date="2026-03-18T10:15:00+00:00")

    framework.write_file(work, m06.ROOT_CAUSE, (SOLUTION / "root-cause.md").read_text(encoding="utf-8"))
    framework.write_file(work, m06.AGENT_LOG, (SOLUTION / "agent-log.md").read_text(encoding="utf-8"))
    gitutil.commit_all(work, "docs(limits): add the root-cause note and agent log for REMIT-231", author=LEARNER,
                       date="2026-03-18T11:40:00+00:00")


LAB = Lab(
    id="m06",
    title="Onboard to the codebase and fix a production bug from its logs",
    lesson="6.2",
    needs_agent=False,  # recommended, not required: the grader checks the result, not who or what produced it
    seed=seed,
    grade=grade,
    solve=solve,
)
