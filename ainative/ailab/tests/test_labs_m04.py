"""Tests for lab m04 (lesson 4.2, "Ship a small feature through the whole loop": REMIT-318, the daily-limit warning).

Four kinds of test live here:

1. the starter and the reference solution, and two different sound solutions (one with a helper in limits.py, integer
   arithmetic and the tests appended to an existing file; one that skips the optional paperwork);
2. the wrong services an agent (or a hurried person) really writes: a float threshold, a forgotten "plus this transfer",
   a rounded percentage, Western digits in Arabic, the notifier called directly, monthly instead of daily, fees in the
   total, "only the first crossing", a special-cased example, the wrong order, a warning on a refused transfer. Each is
   rejected by the hidden acceptance tests, and the ones that are style or house-rule violations by their own check;
3. the wrong tests and the wrong process: no tests, tests that pass without the feature, tests that notice only that
   "something" was sent, a weakened or deleted old test, unrelated files, an oversized change, one big commit, bad
   messages, an uncommitted tail, a secret, a red commit, the code before the spec;
4. the helpers one at a time, and the mutation plugin: each deliberate breakage is killed by the right test and only by it.

Most tests call one check, not the whole grader: the full grade takes several seconds, the single checks about one.
"""
from __future__ import annotations

import importlib
import shutil
import time
from pathlib import Path

import pytest

from ailab import checks, checks_m04 as m04, framework, gitutil
from conftest import learner_commit, start

LAB = importlib.import_module("ailab.labs.m04_limit_warning.lab")
SOLUTION = LAB.SOLUTION
HIDDEN_DIR = framework.load_lab("m04").hidden_dir
LAB_TASK = framework.load_lab("m04").task_file.read_text(encoding="utf-8").rstrip("\n")

ALL = {
    m04.N_TESTS, m04.N_ORIGINALS, m04.N_HIDDEN, m04.N_REMOVAL, m04.N_MUTANTS, m04.N_SCOPE, m04.N_SIZE, m04.N_FLOATS,
    m04.N_COMMIT_COUNT, m04.N_MESSAGES, m04.N_CLEAN, m04.N_SECRETS,
    m04.N_SPEC, m04.N_SPEC_FIRST, m04.N_GREEN, m04.N_SMALL, m04.N_EXCEPT, m04.N_LOG,
}
REQUIRED = {
    m04.N_TESTS, m04.N_ORIGINALS, m04.N_HIDDEN, m04.N_REMOVAL, m04.N_MUTANTS, m04.N_SCOPE, m04.N_SIZE, m04.N_FLOATS,
    m04.N_COMMIT_COUNT, m04.N_MESSAGES, m04.N_CLEAN, m04.N_SECRETS,
}
ADVISORY = ALL - REQUIRED

NOTIFY, SERVICE, LIMITS = "src/remit/notify.py", "src/remit/service.py", "src/remit/limits.py"


# ---------------------------------------------------------------------------------------------
# fixtures and builders
# ---------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def template(tmp_path_factory) -> Path:
    return start("m04", tmp_path_factory.mktemp("m04-template") / "work")


@pytest.fixture(scope="module")
def solved_template(tmp_path_factory) -> Path:
    path = start("m04", tmp_path_factory.mktemp("m04-solved") / "work")
    framework.solve_lab(framework.load_lab("m04"), path)
    return path


@pytest.fixture
def work(template, tmp_path) -> Path:
    target = tmp_path / "work"
    shutil.copytree(template, target)
    return target


@pytest.fixture
def solved(solved_template, tmp_path) -> Path:
    target = tmp_path / "work"
    shutil.copytree(solved_template, target)
    return target


def grade(work: Path) -> dict[str, framework.Check]:
    return {c.name: c for c in framework.grade_lab(framework.load_lab("m04"), work, catch=False)}


def failing(result: dict[str, framework.Check]) -> set[str]:
    return {name for name, check in result.items() if not check.ok}


def assert_only(result: dict[str, framework.Check], *expected: str) -> None:
    got = failing(result)
    detail = "\n".join(f"  {'ok  ' if c.ok else 'FAIL'} {n}: {c.detail}" for n, c in result.items())
    assert got == set(expected), f"expected failures {set(expected)}, got {got}\n{detail}"


def hidden(work: Path) -> checks.PytestResult:
    return checks.run_hidden_pytest(work, HIDDEN_DIR)


def cheap(work: Path) -> dict[str, framework.Check]:
    """The checks that take well under a second, called as lab.py calls them (the heavy ones are tested one at a time)."""
    result = [
        checks.tests_pass(work, name=m04.N_TESTS),
        m04.originals_intact(work),
        checks.files_changed_within(work, m04.ALLOWED, name=m04.N_SCOPE),
        m04.source_size(work),
        m04.no_floats(work),
        checks.commit_count(work, at_least=m04.MIN_COMMITS, at_most=m04.MAX_COMMITS, name=m04.N_COMMIT_COUNT),
        checks.conventional_commits(work, min_commits=1, name=m04.N_MESSAGES),
        checks.all_committed(work, name=m04.N_CLEAN),
        checks.no_secrets(work, name=m04.N_SECRETS),
    ]
    return {c.name: c for c in result}


def read(name: str) -> str:
    return (SOLUTION / name).read_text(encoding="utf-8")


GOOD_METHOD = LAB.SERVICE_METHOD_NEW
GOOD_CALL = LAB.SERVICE_CALL_NEW


def put_template(work: Path) -> None:
    framework.edit_file(work, NOTIFY, LAB.TEMPLATE_OLD, LAB.TEMPLATE_NEW)


def put_service(work: Path, method: str = GOOD_METHOD, *, call: str = GOOD_CALL, imports: str = LAB.SERVICE_IMPORT_NEW) -> None:
    framework.edit_file(work, SERVICE, LAB.SERVICE_IMPORT_OLD, imports)
    framework.edit_file(work, SERVICE, LAB.SERVICE_CONSTANT_OLD, LAB.SERVICE_CONSTANT_NEW)
    framework.edit_file(work, SERVICE, LAB.SERVICE_CALL_OLD, call)
    framework.edit_file(work, SERVICE, LAB.SERVICE_METHOD_OLD, method)


def variant(old: str, new: str, *, method: str = GOOD_METHOD) -> str:
    assert old in method, old
    return method.replace(old, new)


def commit(work: Path, message: str) -> None:
    learner_commit(work, message)


def build(work: Path, *, method: str = GOOD_METHOD, call: str = GOOD_CALL, imports: str = LAB.SERVICE_IMPORT_NEW,
          tests: str | None = None, spec: bool = True, log: bool = True) -> None:
    """The reference route in five commits, with the service (and the tests) swapped for the variant under test."""
    if spec:
        framework.write_file(work, m04.SPEC_FILE, read("spec.md"))
        commit(work, "docs(specs): spec the daily limit warning")
    put_template(work)
    framework.write_file(work, "tests/test_limit_warning.py", read("tests_stage1.py"))
    commit(work, "feat(notify): add the limit_warning message in English and Arabic")
    put_service(work, method, call=call, imports=imports)
    framework.write_file(work, "tests/test_limit_warning.py", read("tests_stage2.py"))
    commit(work, "feat(service): warn at 80% of the daily limit after a transfer")
    framework.write_file(work, "tests/test_limit_warning.py", tests if tests is not None else read("tests_stage3.py"))
    commit(work, "test(service): pin the Arabic text, refusals and a failed delivery")
    if log:
        framework.write_file(work, m04.LOG_FILE, read("agent-log.md"))
        commit(work, "docs(agent): log the session for REMIT-318")


# ---------------------------------------------------------------------------------------------
# 1. the starter and the right answers
# ---------------------------------------------------------------------------------------------
def test_the_starter_fails_for_the_right_reasons(work):
    result = grade(work)
    assert set(result) == ALL
    assert failing(result) == {
        m04.N_HIDDEN, m04.N_REMOVAL, m04.N_MUTANTS, m04.N_SCOPE, m04.N_SIZE, m04.N_COMMIT_COUNT, m04.N_MESSAGES,
        m04.N_SPEC, m04.N_SPEC_FIRST, m04.N_GREEN, m04.N_LOG,
    }
    assert result[m04.N_TESTS].ok and "99 passed" in result[m04.N_TESTS].detail  # the starter suite is green: nothing to fix first
    assert {n for n, c in result.items() if c.required} == REQUIRED
    assert all(c.hint for c in result.values() if not c.ok)
    text = "\n".join(c.detail + c.hint for c in result.values())
    assert "ROUND_FLOOR" not in text and "Decimal(\"0.80\")" not in text and "80.75" not in text  # no hidden answers in any message


def test_the_starter_contains_what_the_lesson_says_it_does(work):
    assert (work / "specs" / "TEMPLATE.md").read_text(encoding="utf-8").startswith("# TODO")
    assert (work / "agent-log.md").read_text(encoding="utf-8").startswith("# Agent log")
    assert "limit_warning" not in (work / NOTIFY).read_text(encoding="utf-8")
    memory = (work / "CLAUDE.md")  # the reference project memory from lab 2.2 (a no-op until that lab exists)
    if memory.exists():
        assert "pytest -q" in memory.read_text(encoding="utf-8")
    assert gitutil.is_clean(work)


def test_the_ticket_states_the_interface(work):
    task = (work / "TASK.md").read_text(encoding="utf-8")
    for needle in ("{name}", "{percent}", "{remaining}", "character for character", "80%", "rounded down", "Arabic-Indic",
                   "Best effort", "SendResult", "REMIT-318", "specs/REMIT-318.md", "agent-log.md", "python -m ailab grade m04"):
        assert needle in task, needle
    assert "hidden" not in task.lower() and "/home/" not in task


def test_the_reference_solution_passes_every_check_quickly(solved):
    began = time.monotonic()
    result = grade(solved)
    assert_only(result)
    assert time.monotonic() - began < 15
    assert "11 new tests" in result[m04.N_REMOVAL].detail
    assert "7 of 7" in result[m04.N_MUTANTS].detail
    assert "5 new commits" in result[m04.N_COMMIT_COUNT].detail


def test_an_alternative_solution_with_a_helper_integer_arithmetic_and_tests_in_an_existing_file(work):
    """Different structure, different route: a helper in limits.py, integer comparison, the tests appended to test_service.py."""
    framework.write_file(work, m04.SPEC_FILE, read("spec.md"))
    commit(work, "docs(specs): plan the daily limit warning")
    put_template(work)
    commit(work, "feat(notify): add the limit_warning template\n\nApproved wording from the content team, copied as it is.")
    framework.edit_file(work, LIMITS, "def limits_for(tier: str) -> TierLimits:", '''def warning_percent(used: Money, limit: Money) -> int | None:
    """The whole-number share of ``limit`` that ``used`` is, rounded down, or None below 80%."""
    if used.amount * 5 < limit.amount * 4:
        return None
    return int(used.amount * 100 // limit.amount)


def limits_for(tier: str) -> TierLimits:''')
    framework.edit_file(work, SERVICE, "from remit.limits import LimitResult, check_limits", "from decimal import Decimal\nfrom remit.limits import LimitResult, check_limits, warning_percent")
    framework.edit_file(work, SERVICE, LAB.SERVICE_CALL_OLD, '''        warning = warning_percent(limits.daily_used + send_amount, limits.daily_limit)
        if warning is not None:
            self._notify(
                customer,
                "limit_warning",
                percent=Decimal(warning),
                remaining=limits.daily_limit - (limits.daily_used + send_amount),
            )
        audit.log_event(
            "transfer.sent",''')
    extra = '''

import pytest as _pytest
from decimal import Decimal as _Decimal
from remit.notify import render as _render


@_pytest.mark.parametrize("amount,warned", [("1599.99", False), ("1600.00", True), ("1999.99", True)])
def test_limit_warning_line(service, notifier, amount, warned):
    service.send("C002", Money(amount, "QAR"), "INR", "Ravi Kumar")
    assert (len(notifier.sent) == 2) is warned
    if warned:
        assert notifier.sent[1].template_id == "limit_warning"


def test_limit_warning_arabic_digits(service, notifier):
    service.send("C003", Money("24000.00", "QAR"), "INR", "Ravi Kumar")
    assert notifier.sent[1].text.startswith("مرحباً Mariam Saleh، بهذا التحويل وصلت إلى ٨٠٪")
    assert not any(ch in notifier.sent[1].text for ch in "0123456789")


def test_limit_warning_english_text():
    text = _render("limit_warning", "en", name="Bilal", percent=_Decimal(85), remaining=Money("300.00", "QAR"))
    assert text.endswith("You can send 300.00 QAR more today.") and "85%" in text


def test_limit_warning_is_absent_after_a_refusal(service, notifier):
    service.send("C002", Money("1500.00", "QAR"), "INR", "Ravi Kumar")
    with pytest.raises(LimitExceeded):
        service.send("C002", Money("600.00", "QAR"), "INR", "Ravi Kumar")
    assert [n.template_id for n in notifier.sent] == ["transfer_sent", "transfer_failed"]


def test_limit_warning_wording_exact_in_both_languages_and_percent_rounds_down(service, notifier):
    service.send("C002", Money("1615.00", "QAR"), "INR", "Ravi Kumar")
    assert "80%" in notifier.sent[1].text and "385.00 QAR" in notifier.sent[1].text
'''
    path = work / "tests" / "test_service.py"
    path.write_text(path.read_text(encoding="utf-8") + extra, encoding="utf-8")
    commit(work, "feat(service): warn at 80% of the daily limit")
    framework.write_file(work, m04.LOG_FILE, "# Agent log\n\nEntry: REMIT-318\nPrompt: no agent used; I wrote it by hand to compare with the course.\nMinutes: 70\n")
    commit(work, "docs(agent): log REMIT-318")
    assert_only(grade(work))


def test_a_sound_solution_without_the_optional_paperwork_passes_the_required_checks(work):
    build(work, spec=False, log=False)
    result = grade(work)
    assert_only(result, m04.N_SPEC, m04.N_SPEC_FIRST, m04.N_LOG)
    assert framework.passed(list(result.values()))  # advisory lines never decide the grade
    assert all(not result[n].required for n in (m04.N_SPEC, m04.N_SPEC_FIRST, m04.N_LOG))


def test_tool_noise_does_not_count_against_the_learner(solved):
    (solved / ".claude").mkdir()
    (solved / ".claude" / "settings.local.json").write_text("{}")
    (solved / ".DS_Store").write_bytes(b"\0\0")
    (solved / ".pytest_cache").mkdir()
    (solved / ".pytest_cache" / "README.md").write_text("cache")
    assert_only(grade(solved))


# ---------------------------------------------------------------------------------------------
# 2. the wrong services (the hidden acceptance tests and the house rules)
# ---------------------------------------------------------------------------------------------
def hidden_failures(work: Path) -> set[str]:
    result = hidden(work)
    assert not result.timed_out
    return {name.split("[")[0] for name in result.failure_names}


def test_the_hidden_tests_pass_on_the_reference_service(solved):
    result = hidden(solved)
    assert result.ok and result.passed == 46, result.summary()


def test_a_float_threshold_misses_exactly_eighty_percent(work):
    """`ratio >= 0.8`: a Decimal compared with a float is compared exactly, and Decimal('0.8') >= 0.8 is False."""
    method = variant("""        if used_after < before.daily_limit * WARNING_LEVEL:
            return
""", """        if used_after / before.daily_limit < 0.8:
            return
""")
    put_template(work)
    put_service(work, method)
    got = hidden_failures(work)
    assert "test_exactly_eighty_percent_is_warned_and_one_cent_less_is_not" in got
    assert "test_the_decision_and_the_numbers_match_the_rule_for_many_amounts" in got
    commit(work, "feat(service): warn at 80%")
    assert not m04.no_floats(work).ok  # and the house-rule check names it too
    assert "service.py" in m04.no_floats(work).detail


def test_forgetting_to_add_the_transfer_just_made_warns_one_transfer_late(work):
    method = variant("used_after = before.daily_used + amount  # ``before`` is the position *before* this transfer",
                     "used_after = before.daily_used")
    put_template(work)
    put_service(work, method)
    got = hidden_failures(work)
    assert "test_exactly_eighty_percent_is_warned_and_one_cent_less_is_not" in got
    assert "test_the_total_includes_what_was_already_sent_today" in got


def test_rounding_the_percentage_instead_of_rounding_it_down(work):
    method = variant("""        if used_after < before.daily_limit * WARNING_LEVEL:
            return
        percent = (used_after.amount * 100 / before.daily_limit.amount).to_integral_value(rounding=ROUND_FLOOR)
""", """        percent = (used_after.amount * 100 / before.daily_limit.amount).to_integral_value(rounding=ROUND_HALF_UP)
        if percent < 80:
            return
""")
    put_template(work)
    put_service(work, method, imports="from dataclasses import dataclass\nfrom decimal import ROUND_FLOOR, ROUND_HALF_UP, Decimal\n")
    got = hidden_failures(work)
    assert "test_the_percentage_is_rounded_down_never_up" in got
    assert "test_exactly_eighty_percent_is_warned_and_one_cent_less_is_not" in got  # 1,599.99 rounds to 80 and is warned


def test_an_int_percentage_prints_western_digits_in_the_arabic_text(work):
    method = variant("percent=percent,", "percent=int(percent),")
    put_template(work)
    put_service(work, method)
    got = hidden_failures(work)
    assert "test_an_arabic_customer_gets_the_arabic_warning_with_arabic_digits" in got
    assert "test_the_english_wording_is_the_approved_wording" not in got


def test_calling_the_notifier_directly_lets_a_failed_warning_escape_after_the_transfer_was_saved(work):
    method = variant("self._notify(customer, \"limit_warning\",", "self.notifier.notify(customer, \"limit_warning\",")
    put_template(work)
    put_service(work, method)
    assert "test_a_warning_that_cannot_be_delivered_does_not_undo_the_transfer" in hidden_failures(work)


def test_using_the_monthly_figures_instead_of_the_daily_ones(work):
    method = GOOD_METHOD.replace("daily_used", "monthly_used").replace("daily_limit", "monthly_limit")
    put_template(work)
    put_service(work, method)
    got = hidden_failures(work)
    assert "test_the_decision_and_the_numbers_match_the_rule_for_many_amounts" in got


def test_counting_the_fee_in_the_total(work):
    put_template(work)
    put_service(work, call=GOOD_CALL.replace("limits, send_amount)", "limits, send_amount + fee)"))
    assert "test_fees_do_not_count_towards_the_total" in hidden_failures(work)


def test_warning_only_the_first_transfer_to_cross_the_line(work):
    method = variant("""        if used_after < before.daily_limit * WARNING_LEVEL:
            return
""", """        if used_after < before.daily_limit * WARNING_LEVEL or before.daily_used >= before.daily_limit * WARNING_LEVEL:
            return
""")
    put_template(work)
    put_service(work, method)
    assert "test_every_transfer_past_the_line_is_warned_not_only_the_first" in hidden_failures(work)


def test_special_casing_the_example_amounts(work):
    method = variant("""        if used_after < before.daily_limit * WARNING_LEVEL:
            return
""", """        if amount not in (Money("1600.00", "QAR"), Money("1700.00", "QAR")):
            return
""")
    put_template(work)
    put_service(work, method)
    got = hidden_failures(work)
    assert "test_the_decision_and_the_numbers_match_the_rule_for_many_amounts" in got  # the sweep over tiers and amounts


def test_the_warning_before_the_sent_message(work):
    call = GOOD_CALL.replace("        self._warn_near_limit(customer, limits, send_amount)\n", "")
    put_template(work)
    put_service(work, call=call)
    framework.edit_file(work, SERVICE, "        # 8. notify (best effort), then the audit trail\n",
                        "        # 8. notify (best effort), then the audit trail\n        self._warn_near_limit(customer, limits, send_amount)\n")
    assert "test_the_warning_comes_straight_after_transfer_sent_exactly_once" in hidden_failures(work)


def test_a_warning_on_a_refused_transfer(work):
    put_template(work)
    put_service(work)
    framework.edit_file(work, SERVICE, "        if not limits.allowed:\n",
                        "        if not limits.allowed:\n            self._warn_near_limit(customer, limits, Money.zero(\"QAR\"))\n")
    assert "test_a_refused_transfer_gets_no_warning" in hidden_failures(work)


def test_a_warning_for_every_transfer_whatever_its_size(work):
    method = variant("""        if used_after < before.daily_limit * WARNING_LEVEL:
            return
""", "")
    put_template(work)
    put_service(work, method)
    assert "test_the_decision_and_the_numbers_match_the_rule_for_many_amounts" in hidden_failures(work)


def test_the_utc_day_instead_of_the_qatar_day(work):
    """A service that re-implements the window with the UTC calendar day instead of the limits module's Qatar day."""
    method = variant("""        used_after = before.daily_used + amount  # ``before`` is the position *before* this transfer
""", """        today = self.clock.now().date()  # UTC date: wrong, the day is the Qatar day
        earlier = sum((t.send_amount for t in self.store.list_transfers(customer.id) if t.created_at.date() == today), Money.zero("QAR"))
        used_after = earlier
""")
    put_template(work)
    put_service(work, method)
    assert "test_the_day_is_the_qatar_day_not_the_utc_day" in hidden_failures(work)


def test_an_unchanged_message_text_is_checked_by_the_wording_tests(work):
    framework.edit_file(work, NOTIFY, LAB.TEMPLATE_OLD, LAB.TEMPLATE_NEW.replace("this transfer takes you to", "you have used"))
    put_service(work)
    got = hidden_failures(work)
    assert "test_the_english_wording_is_the_approved_wording" in got


def test_changing_the_signature_or_the_result_fields(work):
    put_template(work)
    put_service(work)
    framework.edit_file(work, SERVICE, "    notified: bool  # False if the \"transfer_sent\" notification could not be delivered\n",
                        "    notified: bool  # False if the \"transfer_sent\" notification could not be delivered\n    warned: bool = False\n")
    assert "test_send_keeps_its_signature_and_its_result_keeps_its_fields" in hidden_failures(work)


# ---------------------------------------------------------------------------------------------
# 3. the wrong tests and the wrong process
# ---------------------------------------------------------------------------------------------
WEAK_PRESENCE = '''from remit.money import Money


def test_a_warning_is_sent(service, notifier):
    service.send("C002", Money("1700.00", "QAR"), "INR", "Ravi Kumar")
    assert "limit_warning" in [n.template_id for n in notifier.sent]
'''
PASSES_WITHOUT_THE_FEATURE = '''from remit.money import Money


def test_the_sent_message_is_still_sent(service, notifier):
    service.send("C002", Money("100.00", "QAR"), "INR", "Ravi Kumar")
    assert [n.template_id for n in notifier.sent] == ["transfer_sent"]
'''
FAILS_ON_ITS_OWN_CODE = '''from remit.money import Money


def test_a_warning_with_a_wrong_expectation(service, notifier):
    service.send("C002", Money("1700.00", "QAR"), "INR", "Ravi Kumar")
    assert notifier.sent[1].text == "this is not the message"
'''


def test_correct_code_with_no_new_tests(work):
    put_template(work)
    put_service(work)
    commit(work, "feat(service): warn at 80% of the daily limit")
    result = grade(work)
    assert {m04.N_REMOVAL, m04.N_MUTANTS} <= failing(result)
    assert result[m04.N_HIDDEN].ok
    assert "no new tests" in result[m04.N_REMOVAL].detail


def test_tests_that_pass_without_the_feature_prove_nothing(work):
    build(work, tests=PASSES_WITHOUT_THE_FEATURE)  # the last commit replaces the file, so the final state is judged
    removal = m04.removal_check(work)
    assert not removal.ok and "pass even without the warning" in removal.detail
    assert not m04.mutation_check(work).ok


def test_tests_that_only_notice_that_something_was_sent_miss_most_deliberate_breakages(work):
    build(work, tests=WEAK_PRESENCE)
    assert m04.removal_check(work).ok  # it does fail without the feature
    mutants = m04.mutation_check(work)
    assert not mutants.ok and "1 of 7" in mutants.detail
    for survivor in ("the warning text loses its numbers", "the percentage shown is one too high", "Arabic customers get the English text"):
        assert survivor in mutants.detail  # three survivors are named, the rest summarised
    assert "(+3 more)" in mutants.detail and "never delivered" not in mutants.detail  # the one it catches is not listed as missed
    assert mutants.hint and "ROUND" not in mutants.hint


def test_tests_that_fail_on_the_learners_own_code_are_reported_as_such(work):
    build(work, tests=FAILS_ON_ITS_OWN_CODE)
    mutants = m04.mutation_check(work)
    assert not mutants.ok and "do not pass on your own code" in mutants.detail


def test_every_deliberate_breakage_is_caught_by_the_reference_tests(solved):
    ok, summary, killed, survived = m04.mutation_report(solved)
    assert ok and survived == [] and len(killed) == len(m04.MUTANTS), (summary, survived)


@pytest.mark.parametrize("mutant,description", m04.MUTANTS)
def test_each_breakage_is_killed_by_a_test_of_that_behaviour(solved, mutant, description):
    """Run the reference tests with only this plugin mutant on: they fail, and with 'control' they pass."""
    ids = m04.new_test_ids(solved)
    with checks.work_copy(solved) as root:
        control = m04._run(root, ids, args=("-p", m04.PLUGIN), env=m04._mutant_env(root, "control"))  # noqa: SLF001
        broken = m04._run(root, ids, args=("-p", m04.PLUGIN), env=m04._mutant_env(root, mutant))  # noqa: SLF001
    assert control.ok and not broken.ok and broken.failed + broken.errors >= 1, description


def test_an_old_test_weakened_to_go_green(solved):
    framework.edit_file(solved, "tests/test_service.py",
                        'assert [n.template_id for n in notifier.sent] == ["transfer_sent", "transfer_failed"]',
                        'assert "transfer_failed" in [n.template_id for n in notifier.sent]')
    commit(solved, "test(service): relax the notification assertion")
    result = cheap(solved)
    assert_only(result, m04.N_ORIGINALS)
    assert "tests/test_service.py::test_limits_are_enforced_and_the_customer_is_told" in result[m04.N_ORIGINALS].detail


def test_an_old_test_deleted(solved):
    path = solved / "tests" / "test_service.py"
    text = path.read_text(encoding="utf-8")
    start_at = text.index("def test_history_lists_transfers_oldest_first")
    end_at = text.index("def test_invalid_requests_are_rejected_before_anything_is_saved")
    path.write_text(text[:start_at] + text[end_at:], encoding="utf-8")
    commit(solved, "test(service): drop a flaky test")
    result = cheap(solved)
    assert_only(result, m04.N_ORIGINALS)
    assert "test_history_lists_transfers_oldest_first" in result[m04.N_ORIGINALS].detail


def test_a_changed_shared_fixture_or_constant(solved):
    framework.edit_file(solved, "tests/conftest.py", "NOW = datetime(2026, 3, 2, 9, 0, tzinfo=timezone.utc)", "NOW = datetime(2026, 3, 3, 9, 0, tzinfo=timezone.utc)")
    commit(solved, "test(service): move the fixed clock")
    assert "tests/conftest.py::NOW" in m04.originals_intact(solved).detail


def test_adding_tests_reformatting_and_new_fixtures_is_not_editing(solved):
    path = solved / "tests" / "test_service.py"
    path.write_text(path.read_text(encoding="utf-8").replace("def qar(value):\n    return Money(value, \"QAR\")",
                                                             "def qar(value):\n    # shorthand\n    return Money(value, 'QAR')"), encoding="utf-8")
    conftest = solved / "tests" / "conftest.py"
    conftest.write_text(conftest.read_text(encoding="utf-8") + "\n\n@pytest.fixture\ndef arabic_customer(store):\n    return None\n", encoding="utf-8")
    commit(solved, "test(service): add a fixture and tidy a helper")
    assert m04.originals_intact(solved).ok


def test_an_unrelated_file_changed_on_the_way(solved):
    path = solved / "src" / "remit" / "fees.py"
    path.write_text(path.read_text(encoding="utf-8") + "\n# tidy\n", encoding="utf-8")
    commit(solved, "refactor(fees): tidy up")
    result = cheap(solved)
    assert_only(result, m04.N_SCOPE)
    assert "fees.py" in result[m04.N_SCOPE].detail


def test_readme_and_contributing_are_out_of_scope_too(solved):
    (solved / "README.md").write_text((solved / "README.md").read_text(encoding="utf-8") + "\nNew: limit warning.\n", encoding="utf-8")
    commit(solved, "docs(docs): mention the warning")
    assert_only(cheap(solved), m04.N_SCOPE)


def test_an_oversized_source_change(solved):
    path = solved / "src" / "remit" / "notify.py"
    path.write_text(path.read_text(encoding="utf-8") + "".join(f"# note {i}\n" for i in range(150)), encoding="utf-8")
    commit(solved, "docs(notify): add notes")
    result = cheap(solved)
    assert_only(result, m04.N_SIZE)
    assert "limit 120 changed lines" in result[m04.N_SIZE].detail


def test_too_many_source_files_even_if_each_change_is_small(solved):
    for name in ("fees", "fx", "ledger"):
        path = solved / "src" / "remit" / f"{name}.py"
        path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    commit(solved, "chore(service): whitespace")
    result = cheap(solved)
    assert {m04.N_SCOPE, m04.N_SIZE} <= failing(result)


def test_one_big_commit_instead_of_small_steps(work):
    framework.write_file(work, m04.SPEC_FILE, read("spec.md"))
    put_template(work)
    put_service(work)
    framework.write_file(work, "tests/test_limit_warning.py", read("tests_stage3.py"))
    commit(work, "feat(service): add the limit warning")
    result = cheap(work)
    assert_only(result, m04.N_COMMIT_COUNT)
    assert "1 new commit" in result[m04.N_COMMIT_COUNT].detail and result[m04.N_COMMIT_COUNT].required
    spec_first = m04.spec_first(work)
    assert not spec_first.ok and not spec_first.required  # the spec and the code arrived together
    assert not m04.agent_log(work).ok



def test_commit_messages_that_ignore_contributing_md(solved):
    framework.write_file(solved, m04.LOG_FILE, read("agent-log.md") + "\nlater\n")
    commit(solved, "WIP: more notes")
    result = cheap(solved)
    assert_only(result, m04.N_MESSAGES)
    assert "WIP: more notes" in result[m04.N_MESSAGES].detail and "CONTRIBUTING.md" in result[m04.N_MESSAGES].hint


def test_an_uncommitted_tail(solved):
    framework.write_file(solved, "specs/notes.md", "scratch\n")
    result = cheap(solved)
    assert_only(result, m04.N_CLEAN)
    assert "specs/notes.md" in result[m04.N_CLEAN].detail


def test_a_secret_next_to_the_feature(solved):
    framework.edit_file(solved, NOTIFY, "ARABIC_INDIC_DIGITS =", 'GATEWAY_KEY = "sk-live-' + "9f8e7d6c5b4a3f2e1d0c" + '"\nARABIC_INDIC_DIGITS =')
    commit(solved, "feat(notify): add the gateway key")
    result = cheap(solved)
    assert m04.N_SECRETS in failing(result)
    assert "9f8e7d6c" not in result[m04.N_SECRETS].detail + result[m04.N_SECRETS].hint


def test_a_red_commit_is_reported_by_name_and_is_advisory(work):
    framework.write_file(work, m04.SPEC_FILE, read("spec.md"))
    commit(work, "docs(specs): spec the daily limit warning")
    put_template(work)
    framework.edit_file(work, NOTIFY, '        "ar": (\n            "مرحباً {name}، بهذا التحويل', '        "ar_not_yet": (\n            "مرحباً {name}، بهذا التحويل')
    commit(work, "feat(notify): add the English message only")  # the repository's own template test needs both languages
    framework.edit_file(work, NOTIFY, '"ar_not_yet"', '"ar"')
    commit(work, "feat(notify): add the Arabic message")
    check = m04.green_checkpoints(work)
    assert not check.ok and not check.required
    assert "add the English message only" in check.detail and "1 commit" in check.detail


def test_the_code_before_the_spec(work):
    put_template(work)
    commit(work, "feat(notify): add the limit_warning message")
    framework.write_file(work, m04.SPEC_FILE, read("spec.md"))
    commit(work, "docs(specs): write the spec afterwards")
    check = m04.spec_first(work)
    assert not check.ok and not check.required and "no later than the spec" in check.detail


def test_a_spec_that_is_still_the_template_is_not_a_spec(work):
    shutil.copyfile(work / "specs" / "TEMPLATE.md", work / m04.SPEC_FILE)
    check = m04.spec_check(work)
    assert not check.ok and "TODO" in check.detail


def test_a_spec_without_a_numbered_plan(work):
    text = read("spec.md")
    cut = text[: text.index("1. Commit this spec and plan.")] + "Just do it carefully.\n"
    framework.write_file(work, m04.SPEC_FILE, cut)
    assert "0 numbered steps" in m04.spec_check(work).detail


def test_a_plan_of_three_steps_is_too_thin_and_four_is_enough(work):
    """Module 3 and the spec template say four to ten numbered steps; the advisory check agrees."""
    text = read("spec.md")
    head = text[: text.index("1. Commit this spec and plan.")]
    steps = ["1. Commit this spec. Check: none.", "2. Add the template. Check: `pytest -q`.", "3. Add the decision. Check: `pytest -q`.",
             "4. Add the edge tests. Check: `pytest -q`."]
    framework.write_file(work, m04.SPEC_FILE, head + "\n".join(steps[:3]) + "\n")
    thin = m04.spec_check(work)
    assert not thin.ok and "3 numbered steps (4 to 10 expected)" in thin.detail
    framework.write_file(work, m04.SPEC_FILE, head + "\n".join(steps) + "\n")
    assert m04.spec_check(work).ok


def test_a_large_commit_is_reported_but_advisory(solved):
    big = read("tests_stage3.py") + "\n\n" + "\n".join(f"def test_filler_{i}():\n    assert {i} == {i}\n" for i in range(120))
    framework.write_file(solved, "tests/test_limit_warning.py", big)
    commit(solved, "test(service): add many small tests")
    check = m04.small_commits(solved)
    assert not check.ok and not check.required and "many small tests" in check.detail


def test_a_blanket_exception_handler_is_advisory(solved):
    path = solved / "src" / "remit" / "service.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace('        self._notify(customer, "limit_warning", percent=percent, remaining=before.daily_limit - used_after)\n',
                        '        try:\n            self._notify(customer, "limit_warning", percent=percent, remaining=before.daily_limit - used_after)\n'
                        '        except Exception:\n            pass\n')
    path.write_text(text, encoding="utf-8")
    commit(solved, "fix(service): never let the warning fail")
    check = m04.blanket_except(solved)
    assert not check.ok and not check.required and "service.py" in check.detail
    assert_only(cheap(solved))  # the required checks do not mind



def test_the_agent_log_may_say_no_agent_was_used(solved):
    framework.write_file(solved, m04.LOG_FILE, "# Agent log\n\nNo agent used: I did this by hand to learn the loop.\n")
    commit(solved, "docs(agent): note that no agent was used")
    assert m04.agent_log(solved).ok


def test_an_untouched_agent_log_is_reported(work):
    check = m04.agent_log(work)
    assert not check.ok and not check.required and "no entry" in check.detail


def test_an_endless_loop_in_the_code_cannot_hang_the_grader(solved):
    framework.edit_file(solved, SERVICE, "        used_after = before.daily_used + amount", "        while True:\n            pass\n        used_after = before.daily_used + amount")
    commit(solved, "fix(service): spin")
    assert not checks.tests_pass(solved, timeout=2).ok
    began = time.monotonic()
    ok, summary, _, _ = m04.mutation_report(solved, timeout=2)
    assert not ok and time.monotonic() - began < 15


# ---------------------------------------------------------------------------------------------
# 4. the helpers
# ---------------------------------------------------------------------------------------------
def test_new_test_ids_lists_added_and_changed_functions_only(solved):
    path = solved / "tests" / "test_service.py"
    path.write_text(path.read_text(encoding="utf-8") + "\n\ndef test_one_more(service):\n    assert service\n\n\nclass TestGroup:\n    def test_inside(self):\n        assert True\n", encoding="utf-8")
    ids = m04.new_test_ids(solved)
    assert "tests/test_service.py::test_one_more" in ids and "tests/test_service.py::TestGroup::test_inside" in ids
    assert not any(i.startswith("tests/test_money.py") for i in ids)
    assert "tests/test_service.py::test_send_runs_the_whole_flow" not in ids
    assert any(i.startswith("tests/test_limit_warning.py::") for i in ids)


def test_a_test_file_that_does_not_parse_is_still_run_and_reported(work):
    framework.write_file(work, "tests/test_broken.py", "def test_x(:\n")
    assert "tests/test_broken.py" in m04.new_test_ids(work)
    assert not m04.mutation_check(work).ok


def test_the_plugin_leaves_the_files_alone(solved):
    before = {p: p.read_bytes() for p in sorted((solved / "src").rglob("*.py"))}
    m04.mutation_report(solved)
    assert before == {p: p.read_bytes() for p in sorted((solved / "src").rglob("*.py"))}
    assert gitutil.is_clean(solved)


def test_check_names_are_unique_and_the_advisory_ones_are_not_required(solved):
    checks_ = framework.grade_lab(framework.load_lab("m04"), solved, catch=False)
    names = [c.name for c in checks_]
    assert len(names) == len(set(names)) == len(ALL)
    assert {c.name for c in checks_ if c.required} == REQUIRED


# ---------------------------------------------------------------------------------------------
# 5. the lesson quotes the kit: the ticket and the sample output are the real ones
# ---------------------------------------------------------------------------------------------
LESSON = Path(__file__).resolve().parents[2] / "modules" / "04-loop.md"


def lesson_text() -> str:
    if not LESSON.is_file():
        pytest.skip("modules/04-loop.md is not written yet")
    return LESSON.read_text(encoding="utf-8")


def test_the_lesson_quotes_the_ticket_exactly():
    quoted = "\n".join(("> " + line if line.strip() else ">") for line in LAB_TASK.splitlines())
    assert quoted in lesson_text(), "the ticket in lesson 4.2 differs from labs/m04_limit_warning/task.md"


def test_the_sample_output_in_the_lesson_is_what_the_grader_prints(work, template, tmp_path):
    """Every [PASS]/[FAIL] line the lesson shows is a line `ailab grade` really prints, on the starter or on the weak-tests variant."""
    text = lesson_text()
    weak = tmp_path / "weak"
    shutil.copytree(template, weak)
    build(weak, tests=WEAK_PRESENCE)
    printed = {line.rstrip() for line in _printed(work) + _printed(weak)}
    shown = [line.rstrip() for line in text.splitlines() if line.startswith(("[PASS] ", "[FAIL] ")) and "(advisory)" not in line]
    assert len(shown) >= 6, "the lesson shows no sample output"
    for line in shown:
        assert line in printed, f"not real output: {line}"
    last = "Lab m04: 5/12 required checks passed: NOT YET"
    assert last in text and last in printed


def _printed(work: Path) -> list[str]:
    """The lines `ailab grade` prints for a started lab (the CLI's own format), captured in-process."""
    from conftest import run_cli

    code, out, _ = run_cli("grade", "m04", "--dir", str(work))
    assert code == 1
    return out.splitlines()

