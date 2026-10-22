"""Lab m04 (lesson 4.2): "Ship a small feature through the whole loop".

The story
---------
Hessa's ticket REMIT-318: when a successful transfer takes a customer to 80% or more of their daily limit, send
a second notification (a new ``limit_warning`` template, English or Arabic according to the customer's language)
straight after ``transfer_sent``. The ticket (``task.md``) states the public interface exactly, down to the approved
wording, so the hidden acceptance tests are fair. The learner works the whole loop: explore the repository, write
a spec with a plan (``specs/REMIT-318.md`` on ``specs/TEMPLATE.md``), build in small commits that each leave
``pytest -q`` green, add tests that would catch the feature being removed, and keep an agent log.

Where an agent usually goes wrong here (each is graded)
-------------------------------------------------------
* ``ratio >= 0.8``: a Decimal compared with a float is compared exactly, and ``Decimal("0.8") >= 0.8`` is False, so exactly 80%
  gets no warning. Also caught by the "no floats" check.
* ``daily_used`` is the position BEFORE the transfer: forgetting to add the amount just sent warns one transfer late.
* Rounding the percentage instead of rounding it down ("100%" at 99.95%, a warning at 79.9995%).
* Western digits in the Arabic text (an ``int`` percentage is not localised by ``render``; a ``Decimal`` is).
* Counting fees, yesterday, the monthly total or the UTC day; warning on a refused transfer.
* Calling the notifier directly: a failed warning then raises out of ``send`` after the transfer was saved.
* Special-casing the example amounts; editing an existing test; touching ``fees.py`` or ``money.py`` on the way.

What is graded (and what cannot be)
-----------------------------------
Required: the whole suite passes; no original test, fixture or constant was edited; the hidden acceptance tests (the
approved wording, the 80% line from both sides, rounding down, three tiers, the Qatar day, Arabic digits, refusals, best
effort, the unchanged interface, the money untouched, the command line); the learner's NEW tests fail when the code
outside tests/ is the starting code (the feature "removed"); the new tests catch at least five of seven deliberate
breakages of the warning (``checks_m04.mutation_check``); only expected files changed; a small source change; no float
added; at least three commits with messages as CONTRIBUTING.md says; nothing left uncommitted; no secrets.
Advisory: a spec and plan exist in the template's shape; the spec was committed before the code; every commit is green on
its own; no commit is large; no blanket ``except``; an agent log entry.
It cannot tell who wrote the code, whether the spec's decisions are good, whether the learner read the diff, or whether the
approved Arabic wording is good Arabic (the content team's copy is supplied in the ticket).

Files
-----
    lab.py                this file
    task.md               the ticket as Hessa wrote it
    templates/            spec-template.md and agent-log.md, seeded as specs/TEMPLATE.md and agent-log.md
    hidden/               the hidden acceptance tests
    mutation/             a pytest plugin that breaks the warning on purpose (used only by the grader)
    solution/             the reference solution: spec, three stages of tests, an agent log (the source edits are below)
    ../../checks_m04.py   the grader helpers for this lab
"""
from __future__ import annotations

import shutil
from pathlib import Path

from ailab import checks, checks_m04 as m04, framework, gitutil
from ailab.framework import Check, Lab

HERE = Path(__file__).resolve().parent
SOLUTION = HERE / "solution"
LEARNER = ("Najm Learner", "learner@najm.example")


# ---------------------------------------------------------------------------------------------
# seed: the base repository plus the spec template, an empty agent log and the project memory
# ---------------------------------------------------------------------------------------------
def seed(work: Path) -> None:
    work = Path(work)
    (work / "specs").mkdir(exist_ok=True)
    shutil.copyfile(HERE / "templates" / "spec-template.md", work / m04.TEMPLATE_FILE)
    shutil.copyfile(HERE / "templates" / "agent-log.md", work / m04.LOG_FILE)
    framework.add_reference_memory(work)  # the agent starts with project memory; lab 2.2 is where you write your own


# ---------------------------------------------------------------------------------------------
# grade
# ---------------------------------------------------------------------------------------------
def grade(work: Path) -> list[Check]:
    return [
        checks.tests_pass(work, name=m04.N_TESTS),
        m04.originals_intact(work),
        checks.hidden_tests_pass(
            work, HERE / "hidden", name=m04.N_HIDDEN,
            hint="Re-read the ticket line by line: the rules, the interface and the approved wording. Which one do your tests not check?",
        ),
        m04.removal_check(work),
        m04.mutation_check(work),
        checks.files_changed_within(
            work, m04.ALLOWED, name=m04.N_SCOPE,
            hint="The warning needs notify.py and service.py (limits.py if you add a helper), tests, your spec and docs. Revert the rest "
                 "(git restore <file>, or git rm for a new file).",
        ),
        m04.source_size(work),
        m04.no_floats(work),
        checks.commit_count(
            work, at_least=m04.MIN_COMMITS, at_most=m04.MAX_COMMITS, name=m04.N_COMMIT_COUNT,
            hint="Work in small steps and commit each one when `pytest -q` is green: the spec, the message, the decision, the edge-case tests.",
        ),
        checks.conventional_commits(work, min_commits=1, name=m04.N_MESSAGES),
        checks.all_committed(work, name=m04.N_CLEAN),
        checks.no_secrets(work, name=m04.N_SECRETS),
        # --- advisory: the shape of the loop -------------------------------------------------------
        m04.spec_check(work),
        m04.spec_first(work),
        m04.green_checkpoints(work),
        m04.small_commits(work),
        m04.blanket_except(work),
        m04.agent_log(work),
    ]


# ---------------------------------------------------------------------------------------------
# solve: five commits, the way the lesson teaches it
# ---------------------------------------------------------------------------------------------
TEMPLATE_OLD = '''}

# Customer-facing reasons for transfer_failed.'''
TEMPLATE_NEW = '''    "limit_warning": {
        "en": (
            "Hi {name}, this transfer takes you to {percent}% of your daily sending limit. "
            "You can send {remaining} more today."
        ),
        "ar": (
            "مرحباً {name}، بهذا التحويل وصلت إلى {percent}٪ من حد الإرسال اليومي. "
            "يمكنك اليوم إرسال مبلغ إضافي أقصاه {remaining}."
        ),
    },
}

# Customer-facing reasons for transfer_failed.'''

SERVICE_IMPORT_OLD = "from dataclasses import dataclass\n"
SERVICE_IMPORT_NEW = "from dataclasses import dataclass\nfrom decimal import ROUND_FLOOR, Decimal\n"
SERVICE_CONSTANT_OLD = "@dataclass(frozen=True)\nclass Quote:"
SERVICE_CONSTANT_NEW = '''# REMIT-318: warn the customer once a transfer takes the day's total to 80% of the daily limit or more.
WARNING_LEVEL = Decimal("0.80")


@dataclass(frozen=True)
class Quote:'''
SERVICE_CALL_OLD = '''        audit.log_event(
            "transfer.sent",'''
SERVICE_CALL_NEW = '''        self._warn_near_limit(customer, limits, send_amount)
        audit.log_event(
            "transfer.sent",'''
SERVICE_METHOD_OLD = "    def _reject(self,"
SERVICE_METHOD_NEW = '''    def _warn_near_limit(self, customer: Customer, before: LimitResult, amount: Money) -> None:
        """After a successful send: tell the customer when today's total reached 80% of the daily limit."""
        used_after = before.daily_used + amount  # ``before`` is the position *before* this transfer
        if used_after < before.daily_limit * WARNING_LEVEL:
            return
        percent = (used_after.amount * 100 / before.daily_limit.amount).to_integral_value(rounding=ROUND_FLOOR)
        self._notify(customer, "limit_warning", percent=percent, remaining=before.daily_limit - used_after)

    def _reject(self,'''

DOCS_OLD = "Notifiers deliver in the customer's language: `InMemoryNotifier` for tests,\n`ConsoleNotifier` for the CLI.\n"
DOCS_NEW = DOCS_OLD + '''
**Limit warning.** After a successful transfer, if the customer's total for the Qatar
day (the amounts sent, not the fees) has reached 80% of their tier's daily limit, the
service sends a second notification, `limit_warning`, with the percentage used (rounded
down) and the amount still available today. Like `transfer_sent` it is best effort.
'''


def _commit(work: Path, message: str, date: str) -> None:
    gitutil.commit_all(work, message, author=LEARNER, date=date)


def solve(work: Path) -> None:
    work = Path(work)
    # 1. the spec and the plan, before any code
    framework.write_file(work, m04.SPEC_FILE, (SOLUTION / "spec.md").read_text(encoding="utf-8"))
    _commit(work, "docs(specs): spec the daily limit warning", "2026-03-18T08:30:00+00:00")

    # 2. the message, with its wording tests
    framework.edit_file(work, "src/remit/notify.py", TEMPLATE_OLD, TEMPLATE_NEW)
    framework.write_file(work, "tests/test_limit_warning.py", (SOLUTION / "tests_stage1.py").read_text(encoding="utf-8"))
    _commit(work, "feat(notify): add the limit_warning message in English and Arabic", "2026-03-18T09:10:00+00:00")

    # 3. the decision, with the tests for the 80% line
    framework.edit_file(work, "src/remit/service.py", SERVICE_IMPORT_OLD, SERVICE_IMPORT_NEW)
    framework.edit_file(work, "src/remit/service.py", SERVICE_CONSTANT_OLD, SERVICE_CONSTANT_NEW)
    framework.edit_file(work, "src/remit/service.py", SERVICE_CALL_OLD, SERVICE_CALL_NEW)
    framework.edit_file(work, "src/remit/service.py", SERVICE_METHOD_OLD, SERVICE_METHOD_NEW)
    framework.write_file(work, "tests/test_limit_warning.py", (SOLUTION / "tests_stage2.py").read_text(encoding="utf-8"))
    _commit(work, "feat(service): warn at 80% of the daily limit after a transfer", "2026-03-18T10:05:00+00:00")

    # 4. the edge cases: Arabic customer, refused transfer, failed delivery
    framework.write_file(work, "tests/test_limit_warning.py", (SOLUTION / "tests_stage3.py").read_text(encoding="utf-8"))
    _commit(work, "test(service): pin the Arabic text, refusals and a failed delivery", "2026-03-18T10:40:00+00:00")

    # 5. the docs and the agent log
    framework.edit_file(work, "docs/ARCHITECTURE.md", DOCS_OLD, DOCS_NEW)
    framework.write_file(work, m04.LOG_FILE, (SOLUTION / "agent-log.md").read_text(encoding="utf-8"))
    _commit(work, "docs(architecture): describe the limit warning", "2026-03-18T11:15:00+00:00")


LAB = Lab(
    id="m04",
    title="Ship the daily-limit warning through the whole loop",
    lesson="4.2",
    needs_agent=False,  # recommended, not required: the grader cannot tell who typed the code
    seed=seed,
    grade=grade,
    solve=solve,
)
