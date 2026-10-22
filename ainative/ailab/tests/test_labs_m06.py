"""Tests for lab m06 (lesson 6.2, "Onboard to the codebase and fix a production bug from its logs").

Four kinds of test live here:

1. the seed: the history, the green starter suite, the bad commit, and that ``git bisect`` with a reproduction test
   finds it;
2. the assets: prod.log is exactly what the real (buggy) service writes, the ground truth about who was affected is
   what a replay through the corrected service says, and nothing in the ticket or the note gives the cause away;
3. the grader: the reference solution and two different sound solutions pass, and every wrong answer a learner or an
   agent really produces (no reproduction, a test that passes on the starter, only the day fixed, a symptom patch in
   the service, a special case, a constant shift, weakened tests, unrelated files, an oversized patch, a vague note,
   a tour that repeats the stale architecture document) is rejected for the right reason;
4. the document checkers, one at a time.
"""
from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from ailab import checks, checks_m06 as m06, framework, gitutil, runner
from ailab.labs.m06_onboard_debug import make_prod_log as prodlog
from conftest import LEARNER, learner_commit, start

LAB = framework.load_lab("m06")
SOLUTION = LAB.solution_dir
LIMITS = m06.LIMITS_FILE
BAD, GOOD = m06.BAD_CONVERSION, m06.GOOD_CONVERSION

# --- check names (pinned: the lesson quotes some of them) ---------------------------------------------------------
T_SECTIONS = "The tour exists and has its sections"
T_LENGTH = "The tour is a sensible length"
T_FILES = "Every file the tour names exists"
T_FLOW = "The tour lists the transfer steps in the order the code runs them"
T_CLAIMS = "The tour makes no claim the code contradicts"
T_ESSENTIALS = "The tour covers the entry points, the tests, the gaps and the house rules"
SUITE = "Your tests pass (the old ones and yours)"
HIDDEN = "The limits behave as limits.py documents them"
FAILS_ON_STARTER = "Your new tests fail on the original code"
DAILY = "Your tests notice the daily-limit problem"
TWIN = "Your tests catch every place the defect lives"
UNTOUCHED = "The existing tests were not edited or removed"
FIXTURES = "The shared test fixtures were not edited"
SCOPE = "Only the expected files changed"
SMALL = "The fix is a few lines in one place"
N_SECTIONS = "The root-cause note exists and has its sections"
N_CAUSE = "The root-cause note names the cause"
N_BOTH = "The note covers every place the defect lived"
N_REPRO = "The note's reproduction points at your own test"
N_IMPACT = "The note lists who was affected"
COMMITS = "You made at least two commits"
MESSAGES = "Commit messages follow CONTRIBUTING.md"
CLEAN = "Everything is committed (nothing left over)"
SEPARATE = "The tour and the fix are separate commits"
SECRETS = "No secrets in the change"
LOG = "Your agent log is in docs/agent-log.md"
ALL = {T_SECTIONS, T_LENGTH, T_FILES, T_FLOW, T_CLAIMS, T_ESSENTIALS, SUITE, HIDDEN, FAILS_ON_STARTER, DAILY, TWIN,
       UNTOUCHED, FIXTURES, SCOPE, SMALL, N_SECTIONS, N_CAUSE, N_BOTH, N_REPRO, N_IMPACT, COMMITS, MESSAGES, CLEAN,
       SEPARATE, SECRETS, LOG}
ADVISORY = {TWIN, N_BOTH, N_REPRO, N_IMPACT, SEPARATE, LOG}

REAL_TOUR = (SOLUTION / "onboarding.md").read_text(encoding="utf-8")
REAL_NOTE = (SOLUTION / "root-cause.md").read_text(encoding="utf-8")
REAL_LOG = (SOLUTION / "agent-log.md").read_text(encoding="utf-8")
REAL_TEST = (SOLUTION / "test_limits_qatar_midnight.py").read_text(encoding="utf-8")


# --- helpers ---------------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def template(tmp_path_factory) -> Path:
    return start("m06", tmp_path_factory.mktemp("m06-template") / "work")


@pytest.fixture(scope="module")
def solved_template(tmp_path_factory) -> Path:
    work = start("m06", tmp_path_factory.mktemp("m06-solved") / "work")
    framework.solve_lab(LAB, work)
    return work


@pytest.fixture
def work(template, tmp_path) -> Path:
    """A private copy of the started lab (the .git folder and the lab-start tag come with it)."""
    target = tmp_path / "work"
    shutil.copytree(template, target)
    return target


@pytest.fixture
def solved(solved_template, tmp_path) -> Path:
    """A private copy of the lab after the reference solution (three commits)."""
    target = tmp_path / "solved"
    shutil.copytree(solved_template, target)
    return target


def grade(work: Path) -> dict[str, framework.Check]:
    return {c.name.removesuffix(" (advisory)"): c for c in framework.grade_lab(LAB, work, catch=False)}


def failing(result: dict[str, framework.Check]) -> set[str]:
    return {name for name, check in result.items() if not check.ok}


def describe(result) -> str:
    return "\n".join(f"  {'ok  ' if c.ok else 'FAIL'} {n}: {c.detail}" for n, c in result.items())


def assert_only(result: dict[str, framework.Check], *expected_failures: str) -> None:
    got = failing(result)
    assert got == set(expected_failures), f"expected failures {set(expected_failures)}, got {got}\n{describe(result)}"


def edit(work: Path, rel: str, old: str, new: str, count: int = 1) -> None:
    framework.edit_file(work, rel, old, new, count=count)


def commit(work: Path, message: str, **kwargs) -> str:
    return learner_commit(work, message, **kwargs)


def fix_both(work: Path) -> None:
    edit(work, LIMITS, BAD, GOOD, count=2)


def fix_day_only(work: Path) -> None:
    text = (work / LIMITS).read_text(encoding="utf-8")
    first = text.index(BAD)
    framework.write_file(work, LIMITS, text[:first] + GOOD + text[first + len(BAD):])


def put(work: Path, rel: str, text: str) -> None:
    framework.write_file(work, rel, text)


CHEAP_COMMITS = {
    "tour": "docs(onboarding): add a tour of the Remit repository",
    "fix": "fix(limits): start the day and the month at midnight in Qatar",
    "note": "docs(limits): add the root-cause note for REMIT-231",
}


def scenario(work: Path, *, fix=None, tests: dict[str, str] | None = None, tour: str | None = REAL_TOUR,
             note: str | None = REAL_NOTE, log: str | None = REAL_LOG) -> Path:
    """Three commits like a learner's: the tour, the fix with its tests, the note. Any part can be changed or left out."""
    if tour is not None:
        put(work, m06.ONBOARDING, tour)
        commit(work, CHEAP_COMMITS["tour"])
    if fix is not None:
        fix(work)
    for rel, text in (tests or {}).items():
        put(work, rel, text)
    if fix is not None or tests:
        commit(work, CHEAP_COMMITS["fix"])
    if note is not None:
        put(work, m06.ROOT_CAUSE, note)
    if log is not None:
        put(work, m06.AGENT_LOG, log)
    if note is not None or log is not None:
        commit(work, CHEAP_COMMITS["note"])
    return work


# Small tests a learner could write (each is a different, partial, answer).
HEADER = '''from datetime import datetime, timedelta, timezone
from decimal import Decimal

from remit.limits import check_limits, month_window
from remit.models import Transfer
from remit.money import Money


def utc(*parts):
    return datetime(*parts, tzinfo=timezone.utc)


def sent(amount, when):
    return Transfer(id="T-" + when.isoformat(), customer_id="C1", corridor="QAR-INR", send_amount=Money(amount, "QAR"),
                    fee=Money("5", "QAR"), receive_amount=Money("1", "INR"), rate=Decimal("1"), recipient_name="R",
                    delivery_method="bank_deposit", created_at=when)

'''
DAILY_TEST = HEADER + '''
def test_c2207_after_qatar_midnight():
    history = [sent("1200.00", utc(2026, 3, 13, 16, 42, 7))]
    assert check_limits("T1", history, Money("1000.00", "QAR"), utc(2026, 3, 13, 22, 18, 9)).allowed
'''
MONTH_TEST = HEADER + '''
def test_month_rolls_over_at_qatar_midnight():
    assert month_window(utc(2026, 3, 31, 22, 30))[0] == datetime(2026, 4, 1, tzinfo=timezone(timedelta(hours=3)))
'''
USELESS_TEST = HEADER + '''
def test_limits_work():
    history = [sent("1200.00", utc(2026, 3, 13, 10, 0))]
    assert check_limits("T1", history, Money("100.00", "QAR"), utc(2026, 3, 13, 12, 0)).allowed
'''
TEST_PATH = "tests/test_limits_midnight.py"


# ======================================================================================================================
# 1. the seed
# ======================================================================================================================
def test_the_history_is_the_one_the_lesson_describes(work):
    log = gitutil.out(work, "log", "--reverse", "--format=%an|%as|%s").splitlines()
    assert log == [
        "Najm Payments Platform|2026-03-02|Initial state",
        "Salem|2026-03-03|ci(ci): stop runaway test jobs after ten minutes",
        "Nada|2026-03-04|docs(fees): add a worked example to the module docstring",
        "Tariq|2026-03-05|refactor(limits): compute the month end without the December branch",
        "Lujain|2026-03-10|refactor(limits): simplify the window helpers and their tests",
        "Tariq|2026-03-11|docs(readme): show how to run a single test file",
        "Salem|2026-03-12|ci(ci): cancel superseded runs on the same branch",
        "Najm Payments Platform|2026-03-02|Lab starting state",
    ]


def test_the_starter_suite_is_green_and_has_lost_exactly_four_tests(work):
    result = checks.run_pytest(work)
    assert result.ok and result.passed == 95 and result.failed == 0
    text = (work / "tests" / "test_limits.py").read_text(encoding="utf-8")
    for name in ("test_the_day_ends_at_midnight_in_qatar_not_in_utc", "test_the_month_changes_at_midnight_in_qatar",
                 "test_windows_are_local_calendar_windows",
                 "test_a_transfer_after_qatar_midnight_but_before_utc_midnight_belongs_to_the_new_day"):
        assert name not in text
    assert text.count("\ndef test_") == 7
    # the cleanup left no unused imports behind, so the file looks tidy
    assert "QATAR_TZ" not in text and "day_window" not in text and "to_local" not in text


def test_the_seeded_defect_is_two_identical_lines_and_to_local_is_still_defined(work):
    source = (work / LIMITS).read_text(encoding="utf-8")
    assert source.count(BAD) == 2 and GOOD not in source
    assert "def to_local(" in source and source.count("to_local(") == 1  # defined, never called: a clue
    assert gitutil.file_at(work, "lab-start~6", LIMITS).count(GOOD) == 2  # the Initial state had it right


def test_the_innocent_looking_month_refactor_changes_no_behaviour(tmp_path, template):
    """The decoy commit before the bad one must be a pure refactor: same month windows for every month of 2026-2028."""
    program = (
        "from datetime import datetime, timedelta, timezone\n"
        "from remit.limits import month_window\n"
        "for year in (2026, 2027, 2028):\n"
        "    for month in range(1, 13):\n"
        "        for day, hour in ((1, 0), (15, 12), (28, 23)):\n"
        "            start, end = month_window(datetime(year, month, day, hour, tzinfo=timezone.utc))\n"
        "            print(start.isoformat(), end.isoformat())\n"
    )
    outputs = []
    for ref in ("lab-start~6", "lab-start~4"):  # before the month refactor, and just after it (before the bad commit)
        target = tmp_path / ref.replace("~", "-")
        target.mkdir()
        archive = subprocess.run(["git", "archive", ref, "src"], cwd=template, capture_output=True, check=True)
        subprocess.run(["tar", "-x", "-C", str(target)], input=archive.stdout, check=True)
        run = runner.run_python(["-c", program], pythonpath=[target / "src"], timeout=30)
        assert run.ok, run.stderr
        outputs.append(run.stdout)
    assert outputs[0] == outputs[1] and len(outputs[0].splitlines()) == 108
    assert gitutil.file_at(template, "lab-start~6", LIMITS) != gitutil.file_at(template, "lab-start~4", LIMITS)


def test_git_bisect_with_a_reproduction_test_finds_the_bad_commit(work):
    """The point of the history: a reproduction test (not the green suite) makes `git bisect` work, and it names the
    commit that deleted the tests, not the month refactor that looks suspicious."""
    put(work, "tests/test_repro_midnight.py", DAILY_TEST)  # untracked, so it survives every checkout
    initial = gitutil.out(work, "rev-list", "--max-parents=0", "HEAD")
    gitutil.git(work, "bisect", "start", "HEAD", initial)
    outcome = gitutil.git(work, "bisect", "run", sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                          "tests/test_repro_midnight.py")
    assert "is the first bad commit" in outcome.stdout
    first_bad = outcome.stdout.split(" is the first bad commit")[0].split()[-1]
    gitutil.git(work, "bisect", "reset")
    assert gitutil.git(work, "log", "-1", "--format=%s", first_bad).stdout.strip() == \
        "refactor(limits): simplify the window helpers and their tests"


# ======================================================================================================================
# 2. the assets
# ======================================================================================================================
def run_log_generator(src: Path) -> str:
    result = runner.run([sys.executable, str(LAB.home / "make_prod_log.py"), str(src)], timeout=60, env=runner.clean_env())
    assert result.ok, result.stderr
    return result.stdout


def parse(text: str) -> list[dict]:
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def test_prod_log_is_exactly_what_the_buggy_service_writes(template):
    assert run_log_generator(template / "src") == (LAB.assets_dir / "prod.log").read_text(encoding="utf-8")
    assert (template / "lab-assets" / "prod.log").read_text(encoding="utf-8") == (LAB.assets_dir / "prod.log").read_text(encoding="utf-8")


def test_prod_log_has_the_shape_the_incident_note_promises(template):
    events = parse((template / "lab-assets" / "prod.log").read_text(encoding="utf-8"))
    assert len(events) == 56  # incident.md says 56 lines
    assert {e["event"] for e in events} == {"transfer.sent", "transfer.rejected", "notification.failed"}
    assert all(list(e) == sorted(e) for e in events)  # keys sorted, as najmkit.audit writes them
    stamps = [e["ts"] for e in events]
    assert stamps == sorted(stamps) and stamps[0].startswith("2026-03-13T06:") and stamps[-1].startswith("2026-03-17T02:")
    assert not any(k in e for e in events for k in ("name", "recipient", "phone"))  # identifiers only


def test_the_ground_truth_is_what_a_replay_through_the_fixed_service_says(solved_template, template):
    buggy = parse(run_log_generator(template / "src"))
    fixed = parse(run_log_generator(solved_template / "src"))
    assert len(buggy) == len(fixed)
    refused, allowed = [], []
    for before, after in zip(buggy, fixed):
        assert (before["ts"], before["customer_id"]) == (after["ts"], after["customer_id"])
        if before["event"] == "transfer.rejected" and after["event"] == "transfer.sent":
            refused.append(before["customer_id"])
        if before["event"] == "transfer.sent" and after["event"] == "transfer.rejected":
            allowed.append(before["customer_id"])
    assert sorted(refused) == sorted(prodlog.WRONGLY_REFUSED) and sorted(allowed) == sorted(prodlog.WRONGLY_ALLOWED)
    assert all(abs(int(e["ts"][11:13]) - 22) <= 1 or e["ts"][11:13] in ("21", "00", "01") for e in buggy
               if e["customer_id"] in prodlog.WRONGLY_REFUSED and e["event"] == "transfer.rejected")


def test_the_decoys_are_refused_correctly_in_both_worlds(solved_template, template):
    for src in (template / "src", solved_template / "src"):
        events = parse(run_log_generator(src))
        rejected = {e["customer_id"] for e in events if e["event"] == "transfer.rejected"}
        assert set(prodlog.CORRECT_REFUSALS) <= rejected and "C9003" in rejected


def test_the_kyc_extract_covers_every_customer_and_matches_the_service_setup(template):
    rows = list(csv.DictReader((template / "lab-assets" / "kyc_tiers.csv").open(encoding="utf-8")))
    tiers = {row["customer_id"]: row["kyc_tier"] for row in rows}
    in_log = {e["customer_id"] for e in parse((template / "lab-assets" / "prod.log").read_text(encoding="utf-8"))}
    assert in_log <= set(tiers) and set(tiers) == set(prodlog.CUSTOMERS)
    assert all(tiers[c] == prodlog.CUSTOMERS[c][1] for c in tiers)


def test_nothing_the_learner_reads_first_gives_the_cause_away(template):
    giveaways = ("to_local", "astimezone", "day_window", "month_window", "timezone.utc", "wrong time zone", "wrong timezone",
                 "instead of Qatar", "instead of local", "deleted", "removed the four", "four tests")
    for rel in ("TASK.md", "lab-assets/incident.md", "lab-assets/README.md", "lab-assets/kyc_tiers.csv"):
        text = (template / rel).read_text(encoding="utf-8")
        for phrase in giveaways:
            assert phrase.lower() not in text.lower(), f"{rel} mentions {phrase!r}"
    assert "/home/" not in (template / "TASK.md").read_text(encoding="utf-8")


def test_the_assets_say_they_are_constructed_for_teaching(template):
    for rel in ("lab-assets/README.md", "lab-assets/incident.md"):
        assert "constructed for teaching" in (template / rel).read_text(encoding="utf-8").lower()


def test_the_lab_asset_files_are_committed_with_the_starting_state(template):
    tracked = gitutil.out(template, "ls-files").splitlines()
    for rel in ("TASK.md", "lab-assets/prod.log", "lab-assets/incident.md", "lab-assets/kyc_tiers.csv", "lab-assets/README.md"):
        assert rel in tracked
    assert "make_prod_log.py" not in " ".join(tracked)  # the author tool is not handed to learners


# ======================================================================================================================
# 3. the grader
# ======================================================================================================================
def test_the_starter_fails_for_the_right_reasons(work):
    result = grade(work)
    assert set(result) == ALL
    required_failures = {n for n in failing(result) if n not in ADVISORY}
    assert required_failures == (ALL - ADVISORY) - {SUITE, UNTOUCHED, FIXTURES, CLEAN, SECRETS}
    assert result[SUITE].ok and "95 passed" in result[SUITE].detail  # the premise: the visible suite is green
    assert result[UNTOUCHED].ok and result[FIXTURES].ok and result[CLEAN].ok and result[SECRETS].ok
    assert all(c.hint for c in result.values() if not c.ok and c.name in (ALL - ADVISORY))
    # nothing on the very first screen gives the answer away
    shown = " ".join(f"{c.name} {c.detail} {c.hint}" for c in result.values()).lower()
    for phrase in ("utc", "to_local", "astimezone", "day_window", "month_window", "limits.py has"):
        assert phrase not in shown.replace("the limits behave as limits.py documents them", ""), phrase
    assert "test_the_day_ends" not in shown  # the names of the hidden tests are not shown


def test_the_reference_solution_passes_every_check_even_the_advisory_ones(solved):
    assert_only(grade(solved))
    assert framework.passed(framework.grade_lab(LAB, solved, catch=False))


def test_an_alternative_correct_solution_restores_the_deleted_tests_and_inlines_the_conversion(work):
    """What a sensible learner (or an agent) does: put the four removed tests back from history, fix the two lines with
    astimezone(QATAR_TZ), write a different tour and note, and group the commits differently. No agent log."""
    initial = gitutil.out(work, "rev-list", "--max-parents=0", "HEAD")
    original = gitutil.file_at(work, initial, "tests/test_limits.py")
    wanted = ("test_the_day_ends_at_midnight_in_qatar_not_in_utc", "test_a_transfer_after_qatar_midnight_but_before_utc_midnight_belongs_to_the_new_day",
              "test_the_month_changes_at_midnight_in_qatar", "test_windows_are_local_calendar_windows")
    blocks = []
    for name in wanted:
        match = re.search(rf"\n\n\ndef {name}\(.*?(?=\n\n\ndef |\Z)", original, flags=re.S)
        blocks.append(match.group(0))
    alt_tour = """# Onboarding

## 1. What Remit is
Remit is the fictional Najm Bank's transfer service for customers in Qatar: quotes, fees, exchange rates, limits,
screening, ledger postings and notifications in English and Arabic. Python 3.11, standard library only, SQLite, pytest.

## 2. Entry points
| Where | What |
|---|---|
| `python -m remit` | the command line, `src/remit/cli.py` (set `PYTHONPATH=src`) |
| `RemitService` in `src/remit/service.py` | `quote()` prices, `send()` runs a transfer |

## 3. Data flow
`send()` goes: validate (corridors.py), limits (limits.py), screening (screening.py), fee (fees.py), fx (fx.py),
ledger (ledger.py), store (store.py), notify (notify.py), and stops at the first failure.

## 4. Tests
`pytest -q` from the root. `tests/conftest.py` fixes the clock and the ids. Money is Decimal. The ledger and screening
modules have no tests; najmkit provides ids, clock and audit.

## 5. Risks and gaps
Ledger and screening are untested legacy code. docs/ARCHITECTURE.md is outdated: it mentions a risk.py that does not exist.

## 6. Open questions
I did not run the command line; I only read cli.py and the README to understand it. I also could not tell from the code
who owns the watchlist, or whether the notification texts have been reviewed by a native Arabic speaker. The first
thing I would ask Tariq on Monday is which of these gaps he wants closed before anyone refactors the ledger.

The house rules are in CONTRIBUTING.md: Conventional Commits with a scope, a second reviewer for money logic, a label on
AI-assisted pull requests, and no float in money. The fixed clock in the fixtures is Monday 2 March 2026 at 09:00 UTC.
"""
    alt_note = """# Incident REMIT-231

## Symptom
Customers were refused just after midnight in Qatar although a new day had started for them.

## Reproduction
Run `pytest -q tests/test_limits.py::test_the_day_ends_at_midnight_in_qatar_not_in_utc`, or the C2207 case from the log.

## 1. Root cause
`day_window` and `month_window` in limits.py converted `now` to UTC, not to Qatar time (UTC+3), so each window started at
00:00 UTC, which is 03:00 in Qatar.

## Why it was missed
A refactor removed the four boundary tests in the same commit, so CI was green.

## Fix
Both helpers convert to Qatar time again (day and month).

## Impact
Refused wrongly: C1190, C2207, C3042, C4410, C5521, C6003. Let through wrongly: C7788, C8120.

## Prevention
Never delete tests in a change that alters the behaviour they pin.
"""
    scenario(work, fix=None, tour=alt_tour, note=None, log=None)  # commit 1: the tour only
    path = work / "tests" / "test_limits.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace("from remit.limits import DAILY_EXCEEDED, LIMITS, MONTHLY_EXCEEDED, check_limits\n",
                        "from remit.limits import DAILY_EXCEEDED, LIMITS, MONTHLY_EXCEEDED, QATAR_TZ, check_limits, day_window, month_window, to_local\n")
    path.write_text(text.rstrip("\n") + "\n" + "".join(blocks) + "\n", encoding="utf-8")
    edit(work, LIMITS, BAD, "    local = now.astimezone(QATAR_TZ)\n", count=2)
    put(work, m06.ROOT_CAUSE, alt_note)
    commit(work, "fix(limits): use Qatar time again and restore the boundary tests")  # commit 2: fix, tests and note
    result = grade(work)
    assert_only(result, LOG)  # the only thing missing is the (advisory) agent log
    assert framework.passed(framework.grade_lab(LAB, work, catch=False))


def test_another_sound_solution_a_helper_a_bigger_patch_and_service_level_tests(work):
    """Fix through a helper (about a dozen changed lines), test through the service only, one commit per concern."""
    helper = '''def _qatar_floor(moment: datetime, *, month: bool = False) -> datetime:
    """The Qatar midnight that starts the day (or the month) containing ``moment``."""
    local = to_local(moment)
    return local.replace(day=1, hour=0, minute=0, second=0, microsecond=0) if month else local.replace(hour=0, minute=0, second=0, microsecond=0)


def day_window(now: datetime) -> tuple[datetime, datetime]:
    """Start (inclusive) and end (exclusive) of the Qatar calendar day containing ``now``."""
    start = _qatar_floor(now)
    return start, start + timedelta(days=1)


def month_window(now: datetime) -> tuple[datetime, datetime]:
    """Start (inclusive) and end (exclusive) of the Qatar calendar month containing ``now``."""
    start = _qatar_floor(now, month=True)
    # Day 1 plus 32 days is always in the next month; snap back to its first day.
    end = (start + timedelta(days=32)).replace(day=1)
    return start, end
'''
    text = (work / LIMITS).read_text(encoding="utf-8")
    first = text.index("def day_window(")
    last = text.index("def check_limits(")
    framework.write_file(work, LIMITS, text[:first] + helper + "\n\n" + text[last:])
    service_test = '''from datetime import datetime, timezone

import pytest

from remit.errors import LimitExceeded
from remit.money import Money


def at(*parts):
    return datetime(*parts, tzinfo=timezone.utc)


def test_a_customer_sending_after_qatar_midnight_is_not_refused(service, clock):
    clock.set(at(2026, 3, 13, 16, 42, 7))
    service.send("C002", Money("1200.00", "QAR"), "INR", "Ravi Kumar")
    clock.set(at(2026, 3, 13, 22, 18, 9))
    assert service.send("C002", Money("1000.00", "QAR"), "INR", "Ravi Kumar").transfer.status == "completed"


def test_a_customer_cannot_use_two_days_of_limit_in_one_qatar_day(service, clock):
    clock.set(at(2026, 3, 14, 21, 40))
    service.send("C002", Money("1800.00", "QAR"), "INR", "Ravi Kumar")
    clock.set(at(2026, 3, 15, 0, 40))
    with pytest.raises(LimitExceeded):
        service.send("C002", Money("1500.00", "QAR"), "INR", "Ravi Kumar")
'''
    scenario(work, fix=lambda w: None, tests={"tests/test_service_midnight.py": service_test})
    # scenario() committed the helper rewrite together with the test (the fix lambda changed nothing itself)
    result = grade(work)
    assert result[HIDDEN].ok and result[SUITE].ok and result[FAILS_ON_STARTER].ok and result[DAILY].ok, describe(result)
    assert result[SMALL].ok, result[SMALL].detail
    assert framework.passed(framework.grade_lab(LAB, work, catch=False))
    # service-level tests are a legitimate way in; only the month (needs a long month of transfers) is not covered
    assert not result[TWIN].ok  # advisory: a month boundary needs a month of transfers, so the learner may skip it


# --- wrong answers -------------------------------------------------------------------------------------------------
def test_no_reproduction_at_all_only_a_fix(work):
    result = grade(scenario(work, fix=fix_both))
    assert {FAILS_ON_STARTER, DAILY, TWIN} <= failing(result)
    assert result[HIDDEN].ok and result[SUITE].ok and result[SMALL].ok
    assert not framework.passed(framework.grade_lab(LAB, work, catch=False))
    assert "no new or changed test files" in result[FAILS_ON_STARTER].detail


def test_a_test_that_passes_on_the_original_code_proves_nothing(work):
    result = grade(scenario(work, fix=fix_both, tests={TEST_PATH: USELESS_TEST}))
    assert {FAILS_ON_STARTER, DAILY} <= failing(result)
    assert "already pass on the original code" in result[FAILS_ON_STARTER].detail
    assert "Reproduce first" in result[FAILS_ON_STARTER].hint


def test_a_test_that_reproduces_only_the_month_does_not_reproduce_the_report(work):
    result = grade(scenario(work, fix=fix_both, tests={TEST_PATH: MONTH_TEST}))
    assert result[FAILS_ON_STARTER].ok and not result[DAILY].ok and result[TWIN].ok
    assert "daily-limit problem from the incident note" in result[DAILY].detail


def test_fixing_only_the_day_leaves_the_month_wrong(work):
    result = grade(scenario(work, fix=fix_day_only, tests={TEST_PATH: DAILY_TEST}))
    assert not result[HIDDEN].ok and "hidden checks failed" in result[HIDDEN].detail
    assert result[SUITE].ok and result[FAILS_ON_STARTER].ok and result[DAILY].ok
    assert not result[TWIN].ok  # the learner's tests do not notice the second place
    assert not framework.passed(framework.grade_lab(LAB, work, catch=False))
    assert "test_" not in result[HIDDEN].detail  # the hidden test names stay hidden


def test_the_hidden_tests_do_not_leak_the_answer_when_they_fail(work):
    result = grade(work)
    assert "of 19 hidden checks failed" in result[HIDDEN].detail
    assert "qatar" not in (result[HIDDEN].detail + result[HIDDEN].hint).lower()


def test_a_symptom_patch_in_the_service_is_out_of_scope_and_does_not_fix_the_windows(work):
    def patch_service(w: Path) -> None:
        edit(w, "src/remit/service.py", "limits = check_limits(customer.kyc_tier, self.store.list_transfers(customer.id), send_amount, now)",
             "limits = check_limits(customer.kyc_tier, self.store.list_transfers(customer.id), send_amount, now + timedelta(hours=3))")
        edit(w, "src/remit/service.py", "from collections.abc import Iterable\n", "from collections.abc import Iterable\nfrom datetime import timedelta\n")

    result = grade(scenario(work, fix=patch_service, tests={TEST_PATH: DAILY_TEST}))
    assert {SCOPE, SMALL, HIDDEN} <= failing(result)
    assert "service.py" in result[SCOPE].detail and "service.py" in result[SMALL].detail
    assert "Look there" in result[SMALL].hint


def test_special_casing_the_incident_moment_passes_the_learners_test_but_not_the_hidden_ones(work):
    """The classic agent shortcut: make the test go green without touching the cause."""
    def special_case(w: Path) -> None:
        edit(w, LIMITS, "    day_start, day_end = day_window(now)\n",
             "    if now == datetime(2026, 3, 13, 22, 18, 9, tzinfo=timezone.utc):\n        history = []  # the case from the incident\n"
             "    day_start, day_end = day_window(now)\n")

    result = grade(scenario(work, fix=special_case, tests={TEST_PATH: DAILY_TEST}))
    assert result[SUITE].ok and result[FAILS_ON_STARTER].ok and result[DAILY].ok  # the learner's own test is satisfied...
    assert not result[HIDDEN].ok  # ...but the windows are still wrong, and a whole week of instants shows it
    assert not framework.passed(framework.grade_lab(LAB, work, catch=False))


def test_adding_a_constant_shift_is_not_a_fix(work):
    def shift(w: Path) -> None:
        edit(w, LIMITS, BAD, "    local = now + timedelta(hours=3)\n", count=2)

    result = grade(scenario(work, fix=shift, tests={TEST_PATH: DAILY_TEST}))
    assert not result[HIDDEN].ok


def test_editing_existing_tests_to_match_the_bug_is_rejected(work):
    def weaken(w: Path) -> None:
        fix_both(w)
        edit(w, "tests/test_limits.py", "def test_old_months_do_not_count():", "@pytest.mark.skip(reason=\"flaky\")\ndef test_old_months_do_not_count():")
        edit(w, "tests/test_limits.py", "    assert check_limits(\"T2\", history, qar(\"100\"), NOW).allowed  # T2 has room\n", "")

    result = grade(scenario(work, fix=weaken, tests={TEST_PATH: DAILY_TEST}))
    assert not result[UNTOUCHED].ok
    assert "test_old_months_do_not_count" in result[UNTOUCHED].detail or "test_monthly_limit" in result[UNTOUCHED].detail
    assert "git restore tests" in result[UNTOUCHED].hint


def test_deleting_an_existing_test_file_is_rejected(work):
    def delete(w: Path) -> None:
        fix_both(w)
        (w / "tests" / "test_fx.py").unlink()

    result = grade(scenario(work, fix=delete, tests={TEST_PATH: DAILY_TEST}))
    assert not result[UNTOUCHED].ok and "test_fx.py was deleted" in result[UNTOUCHED].detail


def test_editing_the_shared_fixtures_is_rejected(work):
    def tamper(w: Path) -> None:
        fix_both(w)
        edit(w, "tests/conftest.py", "NOW = datetime(2026, 3, 2, 9, 0, tzinfo=timezone.utc)", "NOW = datetime(2026, 3, 2, 9, 1, tzinfo=timezone.utc)")

    result = grade(scenario(work, fix=tamper, tests={TEST_PATH: DAILY_TEST}))
    assert not result[FIXTURES].ok


def test_adding_a_test_next_to_the_old_ones_and_editing_the_import_block_is_fine(work):
    def add(w: Path) -> None:
        fix_both(w)
        text = (w / "tests" / "test_limits.py").read_text(encoding="utf-8")
        text = text.replace("from remit.limits import DAILY_EXCEEDED, LIMITS, MONTHLY_EXCEEDED, check_limits\n",
                            "from remit.limits import (\n    DAILY_EXCEEDED,\n    LIMITS,\n    MONTHLY_EXCEEDED,\n    check_limits,\n    month_window,\n)\n")
        (w / "tests" / "test_limits.py").write_text(text + "\n\ndef test_new_month_start():\n    assert month_window(NOW)[0].day == 1\n", encoding="utf-8")

    result = grade(scenario(work, fix=add, tests={TEST_PATH: DAILY_TEST}))
    assert result[UNTOUCHED].ok, result[UNTOUCHED].detail


def test_unrelated_files_changed_next_to_the_fix(work):
    def sprawl(w: Path) -> None:
        fix_both(w)
        (w / "README.md").write_text((w / "README.md").read_text(encoding="utf-8") + "\nTODO: more docs.\n", encoding="utf-8")
        edit(w, "pyproject.toml", 'version = "0.4.0"', 'version = "0.4.1"')

    result = grade(scenario(work, fix=sprawl, tests={TEST_PATH: DAILY_TEST, "tests/test_limits_midnight_more.py": MONTH_TEST}))
    assert not result[SCOPE].ok and "README.md" in result[SCOPE].detail and "pyproject.toml" in result[SCOPE].detail
    assert result[HIDDEN].ok


def test_an_oversized_but_correct_patch_is_flagged_as_not_minimal(work):
    def rewrite(w: Path) -> None:
        text = (w / LIMITS).read_text(encoding="utf-8")
        first = text.index("def day_window(")
        last = text.index("def check_limits(")
        padding = "".join(f"    # explanation line {i}\n" for i in range(25))
        body = ('def day_window(now: datetime) -> tuple[datetime, datetime]:\n    """Qatar day."""\n' + padding +
                '    local = to_local(now)\n    start = local.replace(hour=0, minute=0, second=0, microsecond=0)\n    return start, start + timedelta(days=1)\n\n\n'
                'def month_window(now: datetime) -> tuple[datetime, datetime]:\n    """Qatar month."""\n'
                '    local = to_local(now)\n    start = local.replace(day=1, hour=0, minute=0, second=0, microsecond=0)\n'
                '    end = (start + timedelta(days=32)).replace(day=1)\n    return start, end\n\n\n')
        framework.write_file(w, LIMITS, text[:first] + body + text[last:])

    result = grade(scenario(work, fix=rewrite, tests={"tests/test_limits_qatar_midnight.py": REAL_TEST}))
    assert_only(result, SMALL)
    assert "limit 20" in result[SMALL].detail and "five minutes" in result[SMALL].hint


def test_a_broken_fix_cannot_hang_the_grader(work):
    def hang(w: Path) -> None:
        edit(w, LIMITS, BAD, "    while True:\n        pass\n", count=2)

    scenario(work, fix=hang, tests={TEST_PATH: DAILY_TEST})
    assert not checks.hidden_tests_pass(work, LAB.hidden_dir, timeout=3).ok
    assert not checks.tests_pass(work, timeout=3).ok


# --- the note ---------------------------------------------------------------------------------------------------
def with_note(solved: Path, note: str) -> dict[str, framework.Check]:
    put(solved, m06.ROOT_CAUSE, note)
    commit(solved, "docs(limits): rewrite the root-cause note", allow_empty=True)
    return grade(solved)


def test_a_note_with_the_wrong_cause_is_rejected(solved):
    note = REAL_NOTE.replace("## Root cause\n", "## Root cause\n\nRounding: the fee was rounded half-even, which changed the amounts. ", 1)
    note = re.sub(r"(?s)(## Root cause\n\n)Rounding.*?(?=\n## Why)", r"\1The fee was rounded half-even, which changed the amount that counted against the limit. The service should round half up.\n", note)
    result = with_note(solved, note)
    assert_only(result, N_CAUSE)
    assert "which time zone the code used" in result[N_CAUSE].detail


def test_a_cause_that_says_utc_but_not_where_or_what_it_should_be_is_incomplete(solved):
    note = re.sub(r"(?s)(## Root cause\n\n).*?(?=\n## Why)", r"\1Something used UTC.\n", REAL_NOTE)
    result = with_note(solved, note)
    assert failing(result) <= {N_SECTIONS, N_CAUSE, N_BOTH}
    assert not result[N_CAUSE].ok and "which time zone it should have used" in result[N_CAUSE].detail


def test_a_note_whose_title_contains_the_words_root_cause_is_still_read_correctly(solved):
    # the first heading "REMIT-231 root cause: ..." must not be mistaken for the Root cause section
    assert REAL_NOTE.splitlines()[0].lower().count("root cause") == 1
    assert_only(with_note(solved, REAL_NOTE))


def test_numbered_headings_are_fine(solved):
    note = re.sub(r"(?m)^## (.*)$", lambda m: f"## {m.start() % 7 + 1}. {m.group(1)}", REAL_NOTE)
    assert_only(with_note(solved, note))


def test_a_note_with_missing_sections_is_rejected(solved):
    note = re.sub(r"(?s)## Why it was missed.*?(?=\n## Fix)", "", REAL_NOTE)
    result = with_note(solved, note)
    assert not result[N_SECTIONS].ok and "Why it was missed" in result[N_SECTIONS].detail


def test_a_note_without_the_affected_customers_is_only_an_advisory_failure(solved):
    note = re.sub(r"C\d{4}", "a customer", REAL_NOTE)
    result = with_note(solved, note)
    assert_only(result, N_IMPACT)
    assert framework.passed(framework.grade_lab(LAB, solved, catch=False))
    assert "kyc_tiers.csv" in result[N_IMPACT].hint


def test_a_note_that_names_no_test_in_its_reproduction_gets_an_advisory_nudge(solved):
    note = re.sub(r"(?s)(## Reproduction\n\n).*?(?=\n## Root cause)", r"\1I looked at the log and thought hard about it.\n", REAL_NOTE)
    result = with_note(solved, note)
    assert_only(result, N_REPRO)
    assert framework.passed(framework.grade_lab(LAB, solved, catch=False))


def test_a_note_that_only_mentions_the_day_gets_an_advisory_nudge(solved):
    note = re.sub(r"(?i)month", "period", REAL_NOTE)
    result = with_note(solved, note)
    assert not result[N_BOTH].ok and result[N_CAUSE].ok
    assert framework.passed(framework.grade_lab(LAB, solved, catch=False))


# --- commits and hygiene ----------------------------------------------------------------------------------------
def test_everything_in_one_commit(work):
    scenario(work, fix=fix_both, tests={"tests/test_limits_qatar_midnight.py": REAL_TEST}, tour=None, note=None, log=None)
    put(work, m06.ONBOARDING, REAL_TOUR)
    put(work, m06.ROOT_CAUSE, REAL_NOTE)
    gitutil.git(work, "add", "-A")
    gitutil.git(work, "commit", "-q", "--amend", "--no-edit", "-m", CHEAP_COMMITS["fix"])
    result = grade(work)
    assert {COMMITS, MESSAGES, SEPARATE} <= failing(result)
    assert "CONTRIBUTING.md" in result[COMMITS].hint


@pytest.mark.parametrize("message", ["fixed the limits", "fix: use qatar time", "Fix(limits): Use Qatar time", "fix(limits): use Qatar time."],
                         ids=["no-convention", "no-scope", "wrong-case", "full-stop"])
def test_commit_messages_that_ignore_contributing_md(solved, message):
    (solved / "docs" / "extra.md").write_text("more words\n", encoding="utf-8")
    commit(solved, message)
    result = grade(solved)
    assert_only(result, MESSAGES)
    assert "CONTRIBUTING.md" in result[MESSAGES].hint


def test_leaving_work_uncommitted(solved):
    (solved / "scratch.py").write_text("print('debug')\n", encoding="utf-8")
    result = grade(solved)
    assert_only(result, SCOPE, CLEAN)
    assert "scratch.py" in result[SCOPE].detail


def test_the_tour_and_the_fix_in_one_commit_is_an_advisory_nudge(work):
    put(work, m06.ONBOARDING, REAL_TOUR)
    fix_both(work)
    put(work, "tests/test_limits_qatar_midnight.py", REAL_TEST)
    commit(work, CHEAP_COMMITS["fix"])
    put(work, m06.ROOT_CAUSE, REAL_NOTE)
    put(work, m06.AGENT_LOG, REAL_LOG)
    commit(work, CHEAP_COMMITS["note"])
    result = grade(work)
    assert_only(result, SEPARATE)
    assert framework.passed(framework.grade_lab(LAB, work, catch=False))
    assert "One logical change per commit" in result[SEPARATE].hint


def test_a_secret_next_to_the_fix_is_caught_without_being_repeated(solved):
    key = "sk-live-" + "9f8e7d6c5b4a3f2e1d0c"
    (solved / "docs" / "agent-log.md").write_text(REAL_LOG + f"\nI pasted the key {key} into the prompt by mistake.\n", encoding="utf-8")
    commit(solved, "docs(limits): extend the agent log")
    result = grade(solved)
    assert_only(result, SECRETS)
    assert "9f8e7d6c" not in result[SECRETS].detail + result[SECRETS].hint


def test_an_agent_log_is_advisory(solved):
    (solved / "docs" / "agent-log.md").unlink()
    commit(solved, "docs(limits): remove the agent log")
    result = grade(solved)
    assert_only(result, LOG)
    assert framework.passed(framework.grade_lab(LAB, solved, catch=False))


def test_tool_noise_does_not_count_against_the_learner(solved):
    (solved / ".claude").mkdir()
    (solved / ".claude" / "settings.local.json").write_text("{}")
    (solved / ".DS_Store").write_bytes(b"\0\0")
    (solved / ".pytest_cache").mkdir()
    (solved / ".pytest_cache" / "README.md").write_text("cache")
    assert_only(grade(solved))


def test_memory_files_for_the_agent_are_allowed(solved):
    (solved / "CLAUDE.md").write_text("# Remit\n\nRun pytest -q. Money is Decimal.\n", encoding="utf-8")
    commit(solved, "docs(limits): add a project memory file")
    assert_only(grade(solved))


def test_grading_twice_gives_the_same_report_and_does_not_touch_the_work(solved):
    before = {c.name: (c.ok, c.detail) for c in framework.grade_lab(LAB, solved, catch=False)}
    status = gitutil.status_porcelain(solved, ignore=())
    after = {c.name: (c.ok, c.detail) for c in framework.grade_lab(LAB, solved, catch=False)}
    assert before == after and gitutil.status_porcelain(solved, ignore=()) == status


# ======================================================================================================================
# 4. the tour checkers, one claim at a time
# ======================================================================================================================
def tour_result(work: Path, text: str) -> dict[str, framework.Check]:
    put(work, m06.ONBOARDING, text)
    return {c.name: c for c in m06.onboarding_checks(work)}


def test_the_reference_tour_passes_all_six_checks(work):
    assert not failing(tour_result(work, REAL_TOUR))


def test_no_tour_fails_all_six_with_one_clear_reason(work):
    result = {c.name: c for c in m06.onboarding_checks(work)}
    assert failing(result) == {T_SECTIONS, T_LENGTH, T_FILES, T_FLOW, T_CLAIMS, T_ESSENTIALS}
    assert all("does not exist" in c.detail for c in result.values())


def test_a_hallucinated_file_is_named_back_to_the_learner(work):
    text = REAL_TOUR.replace("## Entry points", "## Entry points\n\n- `src/remit/risk.py` runs the limits and screening checks.\n", 1)
    result = tour_result(work, text)
    assert failing(result) == {T_FILES} and "risk.py" in result[T_FILES].detail
    assert "the code wins" in result[T_FILES].hint


@pytest.mark.parametrize("sentence", [
    "`risk.py` no longer exists; docs/ARCHITECTURE.md is stale about it.",
    "There is no tests/test_ledger.py: the ledger has no tests.",
    "The README says `requirements.txt` but that file is missing.",
])
def test_a_missing_file_named_as_missing_is_not_a_false_claim(work, sentence):
    text = REAL_TOUR.replace("## Entry points", "## Entry points\n\n" + sentence + "\n", 1)
    assert T_FILES not in failing(tour_result(work, text))


@pytest.mark.parametrize("name", ["requirements.txt", "tests/test_ledger.py", "src/remit/utils.py", "pytest.ini", "src/remit/payments.py"])
def test_other_invented_files_are_caught(work, name):
    text = REAL_TOUR.replace("## Entry points", f"## Entry points\n\n- Configuration lives in `{name}`.\n", 1)
    assert T_FILES in failing(tour_result(work, text))


def test_short_paths_and_urls_are_handled(work):
    text = REAL_TOUR + "\nSee `remit/limits.py`, `limits.py`, `.github/workflows/ci.yml` and https://example.com/docs/guide.md for more.\n"
    assert T_FILES not in failing(tour_result(work, text))


def test_the_flow_in_the_wrong_order_is_caught(work):
    steps = ["validate", "limits", "screening", "fee", "fx", "ledger", "store", "notify"]
    wrong = ["validate", "screening", "limits", "fee", "fx", "ledger", "store", "notify"]
    def tour_with(order):
        flow = "## Data flow\n\nThe steps of `send()`: " + ", then ".join(order) + ". It stops at the first failure. Time and ids come from `najmkit`.\n\n"
        return re.sub(r"(?s)## Data flow\n.*?(?=## Tests)", flow, REAL_TOUR)
    assert T_FLOW not in failing(tour_result(work, tour_with(steps)))
    result = tour_result(work, tour_with(wrong))
    assert failing(result) == {T_FLOW}
    assert "service.py" in result[T_FLOW].hint


def test_flow_in_order_unit():
    good = "validate, then limits, then screening, then the fee, then fx, then the ledger, then store, then notify"
    assert m06.flow_in_order(good) == (True, "")
    ok, why = m06.flow_in_order("validate, then screening, then limits, then the fee, fx, the ledger, store, notify")
    assert not ok and "screening" in why
    ok, why = m06.flow_in_order("validate, limits, screening, fee, fx, ledger, store")
    assert not ok and "notify" in why
    ok, why = m06.flow_in_order("validate, limits, screening, fx, fee, ledger, store, notify")
    assert not ok


def test_an_invented_function_or_technology_is_caught(work):
    text = REAL_TOUR.replace("## Tests", "## Tests\n\nThe `process_transfer()` helper in `service.py` talks to a FastAPI server and Redis.\n", 1)
    result = tour_result(work, text)
    assert failing(result) == {T_CLAIMS}
    assert "process_transfer" in result[T_CLAIMS].detail and "FastAPI" in result[T_CLAIMS].detail and "Redis" in result[T_CLAIMS].detail


def test_real_functions_and_library_calls_are_not_flagged(work):
    text = REAL_TOUR + "\nUseful calls: `check_limits(tier, history, amount, now)`, `RemitService.send()`, `limits.day_window()`, `Money(\"5\", \"QAR\")`, `ids.new_id(\"TRF\")`, `datetime.now()`, `pytest.raises(ValueError)`, `len(items)`.\n"
    assert T_CLAIMS not in failing(tour_result(work, text))


def test_a_function_that_exists_in_a_different_module_is_caught(work):
    text = REAL_TOUR + "\nThe fee comes from `limits.quote_fee()`.\n"
    assert "limits.quote_fee" in tour_result(work, text)[T_CLAIMS].detail


def test_a_technology_the_repo_does_not_use_is_fine_when_the_tour_says_so(work):
    text = REAL_TOUR + "\nThere is no Redis and no Kafka: it is a library plus SQLite.\n"
    assert T_CLAIMS not in failing(tour_result(work, text))


@pytest.mark.parametrize("claim", [
    "- T1 customers may send up to 5,000 QAR a day.",
    "- T2 customers may send up to 25,000 QAR a day.",
    "- There is no monthly limit.",
    "- Remit has two KYC tiers.",
])
def test_the_stale_claims_of_the_architecture_document_are_caught(work, claim):
    result = tour_result(work, REAL_TOUR + "\n" + claim + "\n")
    assert T_CLAIMS in failing(result) and "contradict" in result[T_CLAIMS].detail


@pytest.mark.parametrize("claim", [
    "- docs/ARCHITECTURE.md says T1 may send 5,000 a day; that is outdated.",
    "- The architecture document claims there is no monthly limit, which is wrong.",
    "- The corridor QAR-INR allows up to 25,000 per transfer, and T2 customers can do that in one go.",
])
def test_stale_claims_that_are_marked_as_stale_are_fine(work, claim):
    assert T_CLAIMS not in failing(tour_result(work, REAL_TOUR + "\n" + claim + "\n"))


def test_the_essentials_are_all_required(work):
    def without(*patterns: str, replacement: str = "the thing") -> str:
        text = REAL_TOUR
        for pattern in patterns:
            text = re.sub(pattern, replacement, text)
        return text

    cases = {
        "the command line entry point": without(r"python -m remit", r"src/remit/cli\.py", r"cli\.py", r"remit\.cli"),
        "how to run the tests": without(r"(?i)pytest"),
        "the shared test fixtures": without(r"(?i)conftest(\.py)?"),
        "the money rule (Decimal, never float)": without(r"Decimal"),
        "najmkit": without(r"(?i)najmkit"),
    }
    for expected, text in cases.items():
        result = tour_result(work, text)
        assert T_ESSENTIALS in failing(result), expected
        assert expected in result[T_ESSENTIALS].detail, (expected, result[T_ESSENTIALS].detail)


def test_the_untested_modules_must_be_called_out_in_the_tests_or_risks_sections(work):
    text = REAL_TOUR.replace("**`ledger.py` and `screening.py` have no tests of their own**; they are only exercised through `send()`.", "Everything is well covered.")
    text = text.replace("untested modules", "modules").replace("legacy, untested", "legacy")
    result = tour_result(work, text)
    assert "that the ledger and screening modules have no tests" in result[T_ESSENTIALS].detail


def test_length_and_headings(work):
    assert not tour_result(work, REAL_TOUR)[T_LENGTH].hint
    short = tour_result(work, "# Tour\n\n## What Remit is\nA service.\n")
    assert not short[T_LENGTH].ok and "250" in short[T_LENGTH].detail
    assert not short[T_SECTIONS].ok and "missing" in short[T_SECTIONS].detail
    long = tour_result(work, REAL_TOUR + "\nfiller " * 1500)
    assert not long[T_LENGTH].ok and "1500" in long[T_LENGTH].detail


def test_a_title_containing_a_section_word_is_not_mistaken_for_the_section(work):
    text = REAL_TOUR.replace("# A tour of Najm Remit for the next new engineer", "# Data flow, tests and entry points: a tour")
    assert T_SECTIONS not in failing(tour_result(work, text))


def test_the_lab_pins_its_own_shape():
    assert LAB.id == "m06" and LAB.lesson == "6.2" and LAB.needs_agent is False
    assert LAB.task_file.read_text(encoding="utf-8").startswith("# REMIT-231")
    assert (LAB.assets_dir / "prod.log").is_file() and (LAB.hidden_dir / "test_m06_windows.py").is_file()
