"""Negative and alternative-solution tests for m14 ("Capstone: the Bangladesh corridor through the full cycle").

The grader looks at a code change and at ten documents that must agree with it and with each other. So every test
here takes the reference solution, changes one thing the way a learner (or an agent) really would, grades it and
says exactly which checks must fail and which must still pass:

* wrong code: the existing schedule reused, an off-by-one-cent maximum, cash pickup allowed, a tier edge moved, a float
  literal in Decimal, a margin typo, a Western digit in the Arabic text, the rate forgotten, the new wording sent to
  every corridor, an unrelated file, a new dependency, a weakened old test, a float call;
* tests that prove nothing: they pass without the change, assert nothing, check only that the corridor exists, compute the
  expected value with the code under test, or do not name the criteria they claim to prove;
* documents: a template copied and not filled in, a spec without criteria, a plan that skips one or names a file
  that does not exist, an ADR without consequences, a review without the AI label, a settings file with a wide
  allow, a hook that allows everything or is a naive substring match or crashes on bad input, a corridors page that
  disagrees with the code, an architecture page that was not updated, a log whose total does not add up, a
  retrospective that cites no commit;
* hygiene: one big commit, a mixed commit, a bad message, a secret, a committed ``.env``, an uncommitted file;
* sound alternatives that must still pass: AGENTS.md instead of CLAUDE.md, the template chosen inline, a hook that
  answers with a JSON ``deny``, plain-number documents, worktrees and local settings lying around.
"""
from __future__ import annotations

import ast
import importlib
import json
import re
import shutil
from pathlib import Path

import pytest

from ailab import checks, checks_m14, framework, gitutil
from conftest import learner_commit, run_cli, start

framework.load_lab("m14")  # make sure the lab module is importable
LAB = importlib.import_module("ailab.labs.m14_capstone.lab")
SOL = LAB.SOLUTION
ASSETS = LAB.HERE / "assets"

CODE_TESTS = "Your tests pass"
CORRIDOR = "Corridor: code, minimum, maximum and delivery"
FEES = "Fees: the STD-C schedule"
FX = "Rate, margin and the 60-second quote"
WORDING = "Wording in English and Arabic"
TOGETHER = "Quote, send, ledger, KYC limits and the command line"
WEAKENED = "Existing tests were not weakened"
NEW_FAIL = "Your new tests fail without your change"
SCOPE = "Only the expected files changed"
MEMORY = "Project memory is short, true and useful"
SPEC = "Spec: sections, agreed numbers and acceptance criteria"
PLAN = "Plan: small steps that cover every acceptance criterion"
TRACE = "Tests are traced to the spec's acceptance criteria"
ADR = "ADR records one decision"
REVIEW = "Review notes cover this diff"
SETTINGS = "Settings: deny rules, a registered guard and no wide allows"
HOOK = "Guard hook blocks the dangerous and allows the harmless"
DOCS = "docs/corridors.md matches the code"
ARCH = "ARCHITECTURE.md is not made untrue by the change"
LOG = "Agent log has entries and an honest total"
RETRO = "Retrospective is complete and cites the evidence"
COMMITTED = "Everything is committed"
MESSAGES = "Commit messages follow CONTRIBUTING.md"
ONE_THING = "Each commit is about one thing"
SECRETS = "No secrets in the change"
DECIMAL = "Money stays Decimal; no clock, id, network or float shortcuts"
DEPS = "No new dependency"
LOCAL = "No local data or credential files in the repository"
TEETH = "Your tests have teeth"
TESTS_FIRST = "Tests came before or with the code"
PLAN_HISTORY = "The history follows your plan"
SMALL = "No commit is huge"
HOOK_HARDER = "Guard hook also sees through wrappers"
ASK = "Settings ask before editing the money files"

REQUIRED = {CODE_TESTS, CORRIDOR, FEES, FX, WORDING, TOGETHER, WEAKENED, NEW_FAIL, TEETH, SCOPE, MEMORY, SPEC, PLAN, TRACE, ADR,
            REVIEW, SETTINGS, HOOK, DOCS, ARCH, LOG, RETRO, COMMITTED, MESSAGES, ONE_THING, SECRETS, DECIMAL, DEPS, LOCAL}
ADVISORY = {TESTS_FIRST, PLAN_HISTORY, SMALL, HOOK_HARDER, ASK}
SPEC_PATH, PLAN_PATH = "specs/REMIT-414.md", "specs/REMIT-414-plan.md"
ADR_PATH = "docs/adr/0001-own-fee-schedule-for-bangladesh.md"
REVIEW_PATH, LOG_PATH, RETRO_PATH = "docs/review-REMIT-414.md", "docs/agent-log.md", "docs/retrospective.md"
TESTS_PATH = "tests/test_bdt_corridor.py"


# --------------------------------------------------------------------------------------------
# fixtures and helpers
# --------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def starter(tmp_path_factory) -> Path:
    return start("m14", tmp_path_factory.mktemp("m14-starter") / "work")


@pytest.fixture(scope="module")
def solved(tmp_path_factory) -> Path:
    work = start("m14", tmp_path_factory.mktemp("m14-solved") / "work")
    framework.solve_lab(framework.load_lab("m14"), work)
    return work


@pytest.fixture
def work(solved, tmp_path) -> Path:
    """A private copy of the finished reference solution (history included)."""
    target = tmp_path / "work"
    shutil.copytree(solved, target)
    return target


@pytest.fixture
def fresh(starter, tmp_path) -> Path:
    target = tmp_path / "fresh"
    shutil.copytree(starter, target)
    return target


def grade(work: Path) -> dict[str, framework.Check]:
    return {c.name: c for c in framework.grade_lab(framework.load_lab("m14"), work, catch=False)}


def failing(result: dict[str, framework.Check]) -> set[str]:
    return {name for name, check in result.items() if not check.ok}


def describe(result: dict[str, framework.Check]) -> str:
    return "\n".join(f"  {'ok  ' if c.ok else 'FAIL'} {n}: {c.detail}" for n, c in result.items())


def assert_failing(result: dict[str, framework.Check], *expected: str) -> None:
    got = failing(result)
    assert got == set(expected), f"expected failures {set(expected)}, got {got}\n{describe(result)}"


def assert_required_pass(result: dict[str, framework.Check]) -> None:
    bad = {n for n, c in result.items() if c.required and not c.ok}
    assert not bad, f"required checks failed: {bad}\n{describe(result)}"


def edit(work: Path, rel: str, old: str, new: str, count: int = 1) -> None:
    framework.edit_file(work, rel, old, new, count=count)


def commit(work: Path, message: str) -> None:
    learner_commit(work, message)


def rewrite(work: Path, rel: str, fn) -> None:
    path = work / rel
    path.write_text(fn(path.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")


# --------------------------------------------------------------------------------------------
# the starter and the reference solution
# --------------------------------------------------------------------------------------------
def test_the_starter_fails_everything_that_needs_work_and_passes_what_needs_none(starter):
    result = grade(starter)
    passing = {n for n, c in result.items() if c.ok}
    assert passing == {CODE_TESTS, WEAKENED, COMMITTED, SECRETS, DECIMAL, DEPS, LOCAL, SMALL}, describe(result)
    assert set(result) == REQUIRED | ADVISORY
    for name, check in result.items():
        if not check.ok:
            assert check.detail and check.hint, name


def test_the_reference_solution_passes_every_check_including_the_advisory_ones(work):
    result = grade(work)
    assert_failing(result)
    assert set(result) == REQUIRED | ADVISORY
    assert {n for n, c in result.items() if c.required} == REQUIRED


def test_the_reference_history_is_what_the_lesson_describes(work):
    subjects = [c.subject for c in gitutil.commits_since(work)]
    assert len(subjects) == 15
    assert subjects[0].startswith("docs(specs)") and subjects[4].startswith("test(corridors)")
    assert [s.split("(")[0] for s in subjects[5:10]] == ["feat"] * 5
    assert subjects[-1].startswith("docs(docs): write the retrospective")


def test_the_whole_grade_takes_a_few_seconds_on_the_finished_work(work):
    import time

    began = time.monotonic()
    grade(work)
    assert time.monotonic() - began < 15


def test_the_lab_is_listed(tmp_path):
    code, out, _ = run_cli("list")
    assert code == 0 and "m14" in out and "14.1" in out


# --------------------------------------------------------------------------------------------
# wrong code
# --------------------------------------------------------------------------------------------
def test_reusing_the_std_b_schedule_for_bangladesh(work):
    edit(work, "src/remit/corridors.py", '("bank_deposit", "wallet"), "STD-C")', '("bank_deposit", "wallet"), "STD-B")')
    commit(work, "fix(corridors): reuse the STD-B schedule")
    # the learner's own tests, three of the five hidden groups and the corridors page (which still says STD-C) all notice
    assert_failing(grade(work), CODE_TESTS, CORRIDOR, FEES, TOGETHER, DOCS, TEETH)


def test_a_maximum_one_cent_too_high(work):
    edit(work, "src/remit/corridors.py", '_qar("12000.00")', '_qar("12000.01")')
    commit(work, "fix(corridors): allow a little more")
    assert_failing(grade(work), CODE_TESTS, CORRIDOR, TOGETHER, DOCS, TEETH)


def test_cash_pickup_allowed_on_bangladesh(work):
    edit(work, "src/remit/corridors.py", '("bank_deposit", "wallet"), "STD-C")', '("bank_deposit", "cash_pickup", "wallet"), "STD-C")')
    commit(work, "fix(corridors): allow cash pickup")
    assert_failing(grade(work), CODE_TESTS, CORRIDOR, TOGETHER, DOCS, TEETH)


def test_the_first_tier_edge_moved_by_a_cent(work):
    edit(work, "src/remit/fees.py", 'FeeTier(_D("1000.00"), _D("0.0220"), _D("3.50"))', 'FeeTier(_D("999.99"), _D("0.0220"), _D("3.50"))')
    commit(work, "fix(fees): move the tier edge")
    assert_failing(grade(work), CODE_TESTS, FEES, DOCS, TEETH)


def test_a_float_literal_inside_decimal_is_caught_by_the_security_checks(work):
    edit(work, "src/remit/fx.py", '"QAR-BDT": Decimal("33.46")', '"QAR-BDT": Decimal(33.46)')
    commit(work, "fix(fx): use the rate")
    # the rate still rounds to 32.8745 (the float is just above the tie), so the learner's own tests are green; the
    # agreed number is not exactly the agreed number, and the Decimal rule is what says so
    assert_failing(grade(work), FX, DOCS, DECIMAL)


def test_a_margin_typo(work):
    edit(work, "src/remit/fx.py", '"QAR-BDT": Decimal("0.0175")', '"QAR-BDT": Decimal("0.175")')
    commit(work, "fix(fx): set the margin")
    assert_failing(grade(work), CODE_TESTS, FX, TOGETHER, DOCS, TEETH)


def test_a_western_digit_in_the_arabic_wording(work):
    edit(work, "src/remit/notify.py", "بسعر صرف ١ ريال", "بسعر صرف 1 ريال")
    commit(work, "fix(notify): the digit")
    assert_failing(grade(work), CODE_TESTS, WORDING, TOGETHER, TEETH)


def test_the_rate_is_not_passed_to_the_notification(work):
    edit(work, "src/remit/service.py", "            receive_amount=fx.receive,\n            rate=fx.rate,\n        )",
         "            receive_amount=fx.receive,\n        )")
    commit(work, "fix(service): simplify the notification call")
    assert_failing(grade(work), CODE_TESTS, TOGETHER, TEETH)


def test_the_bangladesh_wording_sent_to_every_corridor(work):
    edit(work, "src/remit/service.py", 'SENT_TEMPLATES.get(corridor.code, "transfer_sent")', '"transfer_sent_bdt"')
    commit(work, "fix(service): use one template")
    assert_failing(grade(work), CODE_TESTS, TOGETHER, TEETH)


def test_an_unrelated_file_changed(work):
    edit(work, "src/remit/limits.py", "QATAR_UTC_OFFSET = timedelta(hours=3)", "QATAR_UTC_OFFSET = timedelta(hours=3)  # a tidy-up")
    commit(work, "refactor(limits): tidy a constant")
    assert_failing(grade(work), SCOPE)


def test_a_new_dependency(work):
    edit(work, "pyproject.toml", "dependencies = []", 'dependencies = ["requests"]')
    commit(work, "build(deps): add requests")
    assert_failing(grade(work), SCOPE, DEPS)


def test_an_old_test_weakened_to_make_something_pass(work):
    edit(work, "tests/test_corridors.py", "assert codes == sorted(codes)", "assert True")
    commit(work, "test(corridors): relax a check")
    assert_failing(grade(work), WEAKENED)


def test_a_float_call_in_the_service(work):
    edit(work, "src/remit/service.py", 'SENT_TEMPLATES: dict[str, str] = {"QAR-BDT": "transfer_sent_bdt"}',
         'SENT_TEMPLATES: dict[str, str] = {"QAR-BDT": "transfer_sent_bdt"}\nHALF = float(0.5)')
    commit(work, "feat(service): add a constant")
    assert_failing(grade(work), DECIMAL)


@pytest.mark.parametrize("snippet", ["datetime.now()", "uuid.uuid4()", "round(x, 2)", "eval(code)"])
def test_other_shortcuts_the_team_forbids(work, snippet):
    edit(work, "src/remit/service.py", 'SENT_TEMPLATES: dict[str, str] = {"QAR-BDT": "transfer_sent_bdt"}',
         'SENT_TEMPLATES: dict[str, str] = {"QAR-BDT": "transfer_sent_bdt"}\nUNUSED = lambda x=0, code="": ' + snippet)
    commit(work, "feat(service): add a constant")
    assert_failing(grade(work), DECIMAL)


# --------------------------------------------------------------------------------------------
# tests that prove nothing
# --------------------------------------------------------------------------------------------
def test_tests_that_assert_nothing_pass_on_the_original_code(work):
    body = "\n".join(f"def test_ac{n}_nothing():\n    assert True\n" for n in range(1, 10))
    (work / TESTS_PATH).write_text(body + "\n", encoding="utf-8")
    commit(work, "test(corridors): add tests")
    # they name every criterion and are green, but they would not notice the corridor being absent or wrong
    assert_failing(grade(work), NEW_FAIL, TEETH, TRACE)


def test_tests_that_do_not_name_the_criteria(work):
    rewrite(work, TESTS_PATH, lambda t: re.sub(r"(?i)ac(\d)", r"case\1", t))
    commit(work, "test(corridors): rename the tests")
    assert_failing(grade(work), TRACE)


def test_a_criterion_nobody_tests(work):
    rewrite(work, TESTS_PATH, lambda t: t.replace("ac9", "case9").replace("AC9", "case9"))
    commit(work, "test(corridors): rename one test")
    assert_failing(grade(work), TRACE)


def test_too_few_tests(work):
    (work / TESTS_PATH).write_text("def test_ac1():\n    pass\n\n\ndef test_ac2():\n    pass\n", encoding="utf-8")
    commit(work, "test(corridors): trim the tests")
    assert TRACE in failing(grade(work))


def test_tests_that_check_only_that_the_corridor_exists_miss_the_numbers(work):
    keep = '''"""AC1 to AC9, lightly."""
from remit.corridors import get_corridor


def test_ac1_exists():
    assert get_corridor("QAR", "BDT")


def test_ac2_code():
    assert get_corridor("QAR", "BDT").code == "QAR-BDT"


def test_ac3_schedule_is_named():
    assert get_corridor("QAR", "BDT").fee_schedule


def test_ac4_receive_currency():
    assert get_corridor("QAR", "BDT").receive_currency == "BDT"


def test_ac5_send_currency():
    assert get_corridor("QAR", "BDT").send_currency == "QAR"


def test_ac6_methods():
    assert get_corridor("QAR", "BDT").delivery_methods


def test_ac7_min():
    assert get_corridor("QAR", "BDT").min_send


def test_ac8_max():
    assert get_corridor("QAR", "BDT").max_send


def test_ac9_default():
    assert get_corridor("QAR", "BDT").default_delivery
'''
    (work / TESTS_PATH).write_text(keep, encoding="utf-8")
    commit(work, "test(corridors): check the corridor")
    result = grade(work)
    assert_failing(result, TEETH, TRACE)  # three comparisons are not enough assertions, and no deliberate defect is noticed
    assert "they miss" in result[TEETH].detail


# --------------------------------------------------------------------------------------------
# documents
# --------------------------------------------------------------------------------------------
TEMPLATES = {
    "memory.md": ("CLAUDE.md", MEMORY),
    "spec.md": (SPEC_PATH, SPEC),
    "plan.md": (PLAN_PATH, PLAN),
    "adr.md": (ADR_PATH, ADR),
    "review.md": (REVIEW_PATH, REVIEW),
    "agent-log.md": (LOG_PATH, LOG),
    "retrospective.md": (RETRO_PATH, RETRO),
    "corridors.md": ("docs/corridors.md", DOCS),
}


@pytest.mark.parametrize("template", sorted(TEMPLATES))
def test_a_template_copied_and_not_filled_in_never_passes(work, template):
    path, check_name = TEMPLATES[template]
    shutil.copyfile(ASSETS / "templates" / template, work / path)
    commit(work, "docs(docs): start the document")
    result = grade(work)
    assert check_name in failing(result)
    assert "TODO" in result[check_name].detail


def test_a_spec_without_numbered_criteria(work):
    rewrite(work, SPEC_PATH, lambda t: re.sub(r"AC(\d)", r"Criterion \1", t))
    commit(work, "docs(specs): rename the criteria")
    # the plan and the tests are traced to the criteria, so they cannot be traced to nothing
    assert_failing(grade(work), SPEC, PLAN, TRACE)


def behaviour_section(text: str, replacement: str) -> str:
    head, rest = text.split("### Behaviour\n", 1)
    return head + "### Behaviour\n" + replacement + "\n\n### Acceptance criteria" + rest.split("### Acceptance criteria", 1)[1]


COPIED_FROM_THE_TICKET = ("All amounts are QAR. A transfer is 100.00 to 12,000.00 inclusive. The minimum fee is 7.00, the cap 130.00 and "
                          "the express surcharge 18.00. The mid rate is 33.46 and the margin 0.0175. Tiers: 2.20% + 3.50 up to 1,000.00, "
                          "1.60% + 12.00 up to 5,000.00, 1.10% + 45.00 above. Cash pickup is refused.")


def test_a_spec_that_leaves_the_working_out_to_the_agent(work):
    rewrite(work, SPEC_PATH, lambda t: behaviour_section(t, COPIED_FROM_THE_TICKET))
    commit(work, "docs(specs): shorten the examples")
    result = grade(work)
    assert_failing(result, SPEC)
    assert "worked results" in result[SPEC].detail


def test_a_spec_with_wrong_worked_results_does_not_count_them(work):
    wrong = COPIED_FROM_THE_TICKET + " A fee for 300.00 is 10.11. A fee for 750.00 is 20.01. 300.00 QAR buys 9,862.36 BDT. The rate is 32.8744."
    rewrite(work, SPEC_PATH, lambda t: behaviour_section(t, wrong))
    commit(work, "docs(specs): worked examples")
    result = grade(work)
    assert_failing(result, SPEC)
    assert "0 correct worked results" in result[SPEC].detail


def test_a_spec_that_works_out_other_correct_amounts_is_a_sound_alternative(work):
    mine = (COPIED_FROM_THE_TICKET + " My own working, with Decimal and half up: a fee for 300.00 is 300.00 x 2.20% + 3.50 = 10.10. "
            "A fee for 750.00 is 20.00. The customer rate is 33.46 x (1 - 0.0175) = 32.8745 after rounding. 300.00 QAR buys 9,862.35 BDT.")
    rewrite(work, SPEC_PATH, lambda t: behaviour_section(t, mine))
    commit(work, "docs(specs): my own worked examples")
    assert_failing(grade(work))


def test_raw_and_rounded_forms_of_one_result_count_once():
    assert checks_m14.worked_results("A fee for 167.50 is 167.50 x 2.20% + 3.50 = 7.185, so 7.19.") == 1
    assert checks_m14.worked_results("500.00 buys 16,437.25 BDT at 32.8745. The fee for 500.00 is 14.50.") == 3
    assert checks_m14.worked_results("Minimum 7.00, cap 130.00, surcharge 18.00, rate 33.46, margin 0.0175, up to 12,000.00.") == 0


def test_a_spec_that_forgets_an_agreed_number(work):
    rewrite(work, SPEC_PATH, lambda t: t.replace("transfer_sent_bdt", "the new template"))
    commit(work, "docs(specs): edit the spec")
    result = grade(work)
    assert_failing(result, SPEC)
    assert "transfer_sent_bdt" in result[SPEC].detail


def test_a_plan_that_skips_a_criterion_and_has_no_commit_header(work):
    rewrite(work, PLAN_PATH, lambda t: t.replace("AC7, AC8", "AC7").replace("| AC7 |", "| AC2 |")
            .replace("`feat(corridors): open the QAR-BDT corridor`", "`Open the corridor.`"))
    commit(work, "docs(specs): edit the plan")
    result = grade(work)
    assert PLAN in failing(result)
    assert "commit header" in result[PLAN].detail


def test_a_plan_that_names_a_file_that_does_not_exist(work):
    rewrite(work, PLAN_PATH, lambda t: t.replace("`src/remit/fx.py`", "`src/remit/rates.py`"))
    commit(work, "docs(specs): edit the plan")
    result = grade(work)
    assert_failing(result, PLAN)
    assert "src/remit/rates.py" in result[PLAN].detail


def test_an_adr_without_consequences_or_the_ticket(work):
    rewrite(work, ADR_PATH, lambda t: t.replace("REMIT-414", "the ticket").split("### Consequences")[0])
    commit(work, "docs(adr): trim the record")
    assert_failing(grade(work), ADR)


def test_an_adr_that_points_at_no_code(work):
    rewrite(work, ADR_PATH, lambda t: re.sub(r"`[^`]*`", "it", t))
    commit(work, "docs(adr): trim the record")
    result = grade(work)
    assert_failing(result, ADR)
    assert "references to real code" in result[ADR].detail


def test_review_notes_without_the_ai_label_or_the_money_files(work):
    def trim(text: str) -> str:
        text = text.replace("AI-assisted: yes.", "Drafted with a helper.")
        return text.replace("`fees.py`", "the schedule").replace("`fx.py`", "the rates").replace("`service.py`", "the send flow")

    rewrite(work, REVIEW_PATH, trim)
    commit(work, "docs(review): trim the notes")
    assert_failing(grade(work), REVIEW)


def test_review_findings_that_point_at_files_that_do_not_exist(work):
    rewrite(work, REVIEW_PATH, lambda t: t.replace("`src/remit/service.py` | 55", "`src/remit/sender.py` | 55")
            .replace("`src/remit/fees.py` | 96", "`src/remit/prices.py` | 96"))
    commit(work, "docs(review): edit the notes")
    result = grade(work)
    assert_failing(result, REVIEW)
    assert "findings with a severity and a real file" in result[REVIEW].detail


def test_review_findings_written_with_plain_paths_and_line_suffixes_are_fine(work):
    rewrite(work, REVIEW_PATH, lambda t: t.replace("`src/remit/service.py` | 55", "src/remit/service.py:55 | 55")
            .replace("`src/remit/fees.py` | 96", "src/remit/fees.py | 96"))
    commit(work, "docs(review): plain paths")
    assert_failing(grade(work))


def test_settings_with_a_wide_allow_and_no_env_deny(work):
    path = work / ".claude/settings.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["permissions"]["allow"].append("Bash(*)")
    data["permissions"]["deny"] = [r for r in data["permissions"]["deny"] if ".env" not in r]
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    commit(work, "chore(claude): loosen the rules")
    result = grade(work)
    assert_failing(result, SETTINGS)
    assert ".env" in result[SETTINGS].detail and "Bash(*)" in result[SETTINGS].detail


@pytest.mark.parametrize("risky", ["Bash(rm *)", "Bash(curl *)", "Bash(pip install *)", "Bash(python *)", "Bash(git push *)", "Bash"])
def test_allow_rules_that_can_delete_publish_or_run_anything(work, risky):
    path = work / ".claude/settings.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["permissions"]["allow"].append(risky)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    commit(work, "chore(claude): allow one more thing")
    assert_failing(grade(work), SETTINGS)


@pytest.mark.parametrize("rule", ["Bash(rm -Rf *)", "Bash(rm -r *)", "Bash(rm -fr *)"])
def test_other_spellings_of_the_recursive_delete_deny_rule_are_sound(work, rule):
    path = work / ".claude/settings.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["permissions"]["deny"] = [rule if r.startswith("Bash(rm") else r for r in data["permissions"]["deny"]]
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    commit(work, "chore(claude): spell the delete rule another way")
    assert_failing(grade(work))


def test_settings_that_do_not_register_the_hook(work):
    path = work / ".claude/settings.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data.pop("hooks")
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    commit(work, "chore(claude): drop the hook")
    assert_failing(grade(work), SETTINGS)


def test_settings_that_are_not_json(work):
    (work / ".claude/settings.json").write_text("{ permissions: nope", encoding="utf-8")
    commit(work, "chore(claude): break the settings")
    assert_failing(grade(work), SETTINGS, ASK)


def test_a_hook_that_allows_everything_is_the_skeleton_bug(work):
    (work / ".claude/hooks/guard.py").write_text("import sys\nsys.exit(0)\n", encoding="utf-8")
    commit(work, "chore(claude): relax the hook")
    assert_failing(grade(work), HOOK, HOOK_HARDER)


def test_a_naive_substring_hook_blocks_the_harmless_and_misses_the_clever(work):
    (work / ".claude/hooks/guard.py").write_text('''import json, sys
cmd = json.load(sys.stdin).get("tool_input", {}).get("command", "")
for bad in ("rm -rf", "git push", "| sh", ".env", "pip install", "reset --hard"):
    if bad in cmd:
        print("Blocked: " + bad, file=sys.stderr)
        sys.exit(2)
''', encoding="utf-8")
    commit(work, "chore(claude): a simple hook")
    result = grade(work)
    assert_failing(result, HOOK, HOOK_HARDER)
    assert "cat .env.example" in result[HOOK].detail or "grep" in result[HOOK].detail


def test_a_hook_that_exits_with_one_on_bad_input_does_not_block(work):
    rewrite(work, ".claude/hooks/guard.py", lambda t: t.replace(
        'block("the hook input is not JSON, so it cannot be checked")', "sys.exit(1)"))
    commit(work, "chore(claude): exit quietly")
    result = grade(work)
    assert_failing(result, HOOK)
    assert "exit code 2" in result[HOOK].detail


def test_a_hook_that_answers_with_a_json_deny_is_a_sound_alternative(work):
    (work / ".claude/hooks/guard.py").write_text('''import json, re, shlex, sys


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": reason}}))
    sys.exit(0)


try:
    data = json.load(sys.stdin)
except ValueError:
    deny("not json")
if data.get("tool_name") != "Bash":
    sys.exit(0)
cmd = (data.get("tool_input") or {}).get("command")
if not isinstance(cmd, str) or not cmd.strip():
    deny("no command")
words = shlex.split(cmd.replace("|", " | "))
if "rm" in words and any(w.startswith("-") and "r" in w for w in words):
    deny("rm -r")
if "git" in words and "push" in words[words.index("git"):words.index("git") + 3]:
    deny("push")
if "git" in words and "reset" in words and "--hard" in words:
    deny("reset")
if words[:1] in (["pip"], ["pip3"]) and "install" in words:
    deny("install")
if ("curl" in words or "wget" in words) and "|" in words:
    deny("pipe to a shell")
if any(re.search(r"(^|/)\\.env($|\\.(?!example))", w) for w in words):
    deny("env")
sys.exit(0)
''', encoding="utf-8")
    commit(work, "chore(claude): a hook that answers in JSON")
    assert_failing(grade(work), HOOK_HARDER)  # the required behaviour is met; seeing through wrappers is the advisory part


def test_a_missing_hook_script(work):
    gitutil.git(work, "rm", "-q", ".claude/hooks/guard.py")
    commit(work, "chore(claude): remove the hook")
    assert_failing(grade(work), SETTINGS, HOOK, HOOK_HARDER)


def test_a_corridors_page_that_disagrees_with_the_code(work):
    def break_page(text: str) -> str:
        text = text.replace("| QAR-BDT | 100.00 | 12,000.00 |", "| QAR-BDT | 100.00 | 15,000.00 |")
        return "\n".join(line for line in text.splitlines() if not line.startswith("| STD-C")) + "\n"

    rewrite(work, "docs/corridors.md", break_page)
    commit(work, "docs(docs): edit the page")
    result = grade(work)
    assert_failing(result, DOCS)
    assert "maximum" in result[DOCS].detail and "STD-C" in result[DOCS].detail


def test_a_corridors_page_with_plain_numbers_is_a_sound_alternative(work):
    rewrite(work, "docs/corridors.md", lambda t: t.replace("12,000.00", "12000").replace("1,000.00", "1000").replace("5,000.00", "5000")
            .replace("2.2%", "2.20%").replace("1.1%", "1.10%").replace("0.0100", "0.01"))
    commit(work, "docs(docs): plainer numbers")
    assert_failing(grade(work))


def test_an_architecture_page_that_was_not_updated(work):
    gitutil.git(work, "checkout", "lab-start", "--", "docs/ARCHITECTURE.md")
    commit(work, "docs(docs): put the architecture page back")
    result = grade(work)
    assert_failing(result, ARCH)
    assert "two fee schedules" in result[ARCH].detail


def test_an_agent_log_whose_total_does_not_add_up(work):
    edit(work, LOG_PATH, "Total minutes: 180", "Total minutes: 200")
    commit(work, "docs(docs): fix the total")
    assert_failing(grade(work), LOG, RETRO)  # the retrospective still quotes the old total


def test_an_agent_log_with_two_rows(work):
    def trim(text: str) -> str:
        rows = text.splitlines()
        kept = [row for row in rows if not re.match(r"\| [3-7] \|", row)]
        return "\n".join(kept).replace("Total minutes: 180", "Total minutes: 45") + "\n"

    rewrite(work, LOG_PATH, trim)
    commit(work, "docs(docs): trim the log")
    assert_failing(grade(work), LOG, RETRO)  # the retrospective still quotes 180 minutes


def test_a_retrospective_that_cites_no_commit(work):
    rewrite(work, RETRO_PATH, lambda t: re.sub(r"\b[0-9a-f]{9}\b", "abcdef", t))
    commit(work, "docs(docs): edit the retrospective")
    result = grade(work)
    assert_failing(result, RETRO)
    assert "commit" in result[RETRO].detail


def test_a_retrospective_with_one_line_per_section(work):
    first = (work / RETRO_PATH).read_text(encoding="utf-8").split("### What went well")[0]
    (work / RETRO_PATH).write_text(first + "### What went well\nFine.\n### What went wrong\nSome.\n", encoding="utf-8")
    commit(work, "docs(docs): shorten the retrospective")
    assert_failing(grade(work), RETRO)


def test_a_memory_file_that_is_too_long_untrue_and_unfinished(work):
    path = work / "CLAUDE.md"
    path.write_text(path.read_text(encoding="utf-8") + "\nSee `docs/OLD.md` and `src/remit/risk.py`.\nTODO\n" + "filler\n" * 150, encoding="utf-8")
    commit(work, "chore(claude): grow the memory")
    result = grade(work)
    assert_failing(result, MEMORY)
    detail = result[MEMORY].detail
    assert "lines" in detail and "TODO" in detail and "docs/OLD.md" in detail


def test_a_memory_file_with_a_secret(work):
    path = work / "CLAUDE.md"
    path.write_text(path.read_text(encoding="utf-8") + '\nREMIT_API_KEY = "sk-live-9f8e7d6c5b4a39281716151413121110"\n', encoding="utf-8")
    commit(work, "chore(claude): note the key")
    assert_failing(grade(work), MEMORY, SECRETS)


def test_a_memory_file_that_documents_a_command_that_fails(work):
    edit(work, "CLAUDE.md", "`PYTHONPATH=src python -m remit quote QAR 500 BDT`", "`PYTHONPATH=src python -m remit quote QAR 5 BDT`")
    commit(work, "chore(claude): edit the command")
    result = grade(work)
    assert_failing(result, MEMORY)
    assert "fails" in result[MEMORY].detail


def test_a_memory_file_without_the_corridor_checklist_or_a_never_list(work):
    (work / "CLAUDE.md").write_text("# Remit\n\n" + "\n".join(f"Line {n} about the repository, in prose." for n in range(30)) + "\n`pytest -q`\n",
                                    encoding="utf-8")
    commit(work, "chore(claude): shorter memory")
    result = grade(work)
    assert_failing(result, MEMORY)
    assert "never list" in result[MEMORY].detail and "corridor checklist" in result[MEMORY].detail


def test_agents_md_instead_of_claude_md_is_a_sound_alternative(work):
    gitutil.git(work, "mv", "CLAUDE.md", "AGENTS.md")
    commit(work, "chore(claude): use AGENTS.md")
    assert_failing(grade(work))


# --------------------------------------------------------------------------------------------
# history and hygiene
# --------------------------------------------------------------------------------------------
def test_everything_in_one_commit(work):
    gitutil.git(work, "reset", "--soft", "lab-start")
    commit(work, "feat(corridors): open the Bangladesh corridor")
    result = grade(work)
    # one commit: too few, mixed, and the retrospective's commit no longer exists (the tests are in the same commit as the code)
    assert_failing(result, MESSAGES, ONE_THING, RETRO, PLAN_HISTORY)


def test_a_commit_that_mixes_code_and_documents(work):
    gitutil.git(work, "reset", "--soft", "HEAD~7")
    commit(work, "feat(service): the service and the documents")
    result = grade(work)
    assert_failing(result, ONE_THING, PLAN_HISTORY)
    assert "code and documents" in result[ONE_THING].detail


def test_code_and_tests_in_the_same_commit_are_fine_and_count_as_tests_with_the_code(work):
    gitutil.git(work, "reset", "-q", "--soft", "HEAD~11")  # keep the specs, the memory and the settings commits
    gitutil.git(work, "reset", "-q")
    gitutil.git(work, "add", "src", "tests")
    gitutil.git(work, "-c", "user.name=Najm Learner", "-c", "user.email=learner@najm.example", "commit", "-q", "-m",
                "feat(corridors): open the Bangladesh corridor with its tests")
    commit(work, "docs(docs): the decision, the page, the review, the log and the retrospective")
    result = grade(work)
    # six commits is too few and the retrospective's commit is gone; but code with its tests is one kind of change,
    # and CONTRIBUTING.md wants a green suite at every commit, so tests committed with their code are not "code first"
    assert_failing(result, MESSAGES, RETRO, PLAN_HISTORY)


def test_a_bad_commit_message(work):
    edit(work, LOG_PATH, "# Agent log: REMIT-414", "# Agent log: REMIT-414 ")
    commit(work, "Update the log.")
    result = grade(work)
    assert_failing(result, MESSAGES)
    assert "Update the log." in result[MESSAGES].detail
    assert "type(scope): subject" in result[MESSAGES].hint and "72" in result[MESSAGES].hint


def test_too_few_commits_get_a_hint_about_small_steps_not_commit_your_change(work):
    gitutil.git(work, "reset", "-q", "--soft", "HEAD~12")
    commit(work, "feat(corridors): open the Bangladesh corridor and write all the documents")
    few = grade(work)[MESSAGES]
    assert not few.ok and "expected at least 8" in few.detail
    assert "at least 8 commits" in few.hint and "Commit your change" not in few.hint


def test_an_uncommitted_file(work):
    (work / "docs/notes.md").write_text("scratch\n", encoding="utf-8")
    assert_failing(grade(work), COMMITTED)


def test_a_secret_in_a_document(work):
    path = work / REVIEW_PATH
    path.write_text(path.read_text(encoding="utf-8") + '\napi_key = "sk-live-9f8e7d6c5b4a39281716151413121110"\n', encoding="utf-8")
    commit(work, "docs(review): note the key")
    assert_failing(grade(work), SECRETS)


def test_a_committed_env_file(work):
    (work / ".env").write_text("REMIT_ENV=dev\n", encoding="utf-8")
    gitutil.git(work, "add", "-f", ".env")
    commit(work, "chore(config): add the environment")
    assert_failing(grade(work), SCOPE, LOCAL)


def test_a_huge_commit_is_only_advisory(work):
    path = work / "tests/test_bdt_corridor.py"
    path.write_text(path.read_text(encoding="utf-8") + "\n".join(f"# padding line {n}" for n in range(300)) + "\n", encoding="utf-8")
    commit(work, "test(corridors): pad the tests")
    result = grade(work)
    assert_failing(result, SMALL)
    assert_required_pass(result)


def test_a_plan_the_history_does_not_follow_is_only_advisory(work):
    rewrite(work, PLAN_PATH, lambda t: t.replace("`feat(", "`fix(").replace("`test(", "`chore("))
    commit(work, "docs(specs): rewrite the commit headers in the plan")
    result = grade(work)
    assert_failing(result, PLAN_HISTORY)
    assert_required_pass(result)


# --------------------------------------------------------------------------------------------
# sound alternatives
# --------------------------------------------------------------------------------------------
def test_choosing_the_template_inline_instead_of_with_a_table(work):
    edit(work, "src/remit/service.py", 'SENT_TEMPLATES.get(corridor.code, "transfer_sent")',
         '"transfer_sent_bdt" if corridor.code == "QAR-BDT" else "transfer_sent"')
    edit(work, "src/remit/service.py",
         '# Corridors that have their own "transfer sent" wording (notify.TEMPLATES); every other corridor uses "transfer_sent".\n'
         'SENT_TEMPLATES: dict[str, str] = {"QAR-BDT": "transfer_sent_bdt"}\n\n\n', "")
    commit(work, "refactor(service): choose the template inline")
    assert_failing(grade(work))


def test_worktrees_and_local_settings_lying_around_are_not_your_work(work):
    (work / ".claude/worktrees/feat-x").mkdir(parents=True)
    (work / ".claude/worktrees/feat-x/notes.txt").write_text("x\n", encoding="utf-8")
    (work / ".claude/settings.local.json").write_text("{}\n", encoding="utf-8")
    assert_failing(grade(work))


def test_tests_in_a_differently_named_file_with_the_plan_updated(work):
    rewrite(work, PLAN_PATH, lambda t: t.replace("tests/test_bdt_corridor.py", "tests/test_bangladesh.py"))
    commit(work, "docs(specs): the tests will live in another file")
    gitutil.git(work, "mv", TESTS_PATH, "tests/test_bangladesh.py")
    commit(work, "test(corridors): rename the test file")
    assert_failing(grade(work))


def test_a_stale_plan_after_a_rename_is_a_finding(work):
    gitutil.git(work, "mv", TESTS_PATH, "tests/test_bangladesh.py")
    commit(work, "test(corridors): rename the test file")
    assert_failing(grade(work), PLAN)


def test_a_readme_update_is_in_scope(work):
    path = work / "README.md"
    path.write_text(path.read_text(encoding="utf-8") + "\nSee docs/corridors.md for the corridors and fees.\n", encoding="utf-8")
    commit(work, "docs(docs): point the readme at the corridors page")
    assert_failing(grade(work))


# --------------------------------------------------------------------------------------------
# the kit itself: ticket, templates, assets and checks agree
# --------------------------------------------------------------------------------------------
def test_the_ticket_names_every_file_the_grader_asks_for():
    ticket = (LAB.HERE / "task.md").read_text(encoding="utf-8")
    for path in (checks_m14.SPEC, checks_m14.PLAN, checks_m14.REVIEW, checks_m14.AGENT_LOG, checks_m14.RETRO,
                 checks_m14.CORRIDORS_DOC, checks_m14.SETTINGS, checks_m14.GUARD, "CLAUDE.md", "docs/adr/0001-"):
        assert path in ticket, path
    for name in ("corridors.py", "fees.py", "fx.py", "notify.py", "service.py", "STD-C", "transfer_sent_bdt", "33.46", "0.0175",
                 "12,000.00", "100.00", "7.00", "130.00", "18.00", "AI-assisted"):
        assert name in ticket, name


def test_the_ticket_wording_and_the_hidden_tests_agree_word_for_word():
    ticket = (LAB.HERE / "task.md").read_text(encoding="utf-8")
    en = re.search(r"^\s*en: (.+)$", ticket, re.M).group(1)
    ar = re.search(r"^\s*ar: (.+)$", ticket, re.M).group(1)
    en_filled = en.format(name="Aisha Rahman", transfer_id="TRF-000001", recipient="Rahim Uddin", receive_amount="16,437.25 BDT",
                          send_amount="500.00 QAR", fee="14.50 QAR", rate="32.8745")
    ar_filled = ar.format(name="Mariam Saleh", transfer_id="TRF-000001", recipient="Rahim Uddin", receive_amount="٣٩٤٬٤٩٤٫٠٠ تاكا بنغلاديشية",
                          send_amount="١٢٬٠٠٠٫٠٠ ريال قطري", fee="١٣٠٫٠٠ ريال قطري", rate="٣٢٫٨٧٤٥")
    for module in ("test_m14_notify", "test_m14_together"):
        tree = ast.parse((LAB.HERE / "hidden" / f"{module}.py").read_text(encoding="utf-8"))
        constants = {}
        for node in tree.body:
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                try:
                    constants[node.targets[0].id] = ast.literal_eval(node.value)
                except ValueError:
                    pass
        english = constants.get("EN_EXPECTED") or constants.get("EN_AISHA")
        arabic = constants.get("AR_EXPECTED") or constants.get("AR_MARIAM")
        assert english == en_filled, module
        assert arabic == ar_filled, module


def test_the_numbers_in_the_ticket_are_the_numbers_the_reference_code_uses():
    ticket = (LAB.HERE / "task.md").read_text(encoding="utf-8")
    code = "".join((SOL / name).read_text(encoding="utf-8") for name in ("01_fees.patch", "02_fx.patch", "03_corridor.patch"))
    for needle in ('_D("1000.00"), _D("0.0220"), _D("3.50")', '_D("5000.00"), _D("0.0160"), _D("12.00")', 'None, _D("0.0110"), _D("45.00")',
                   'minimum=_D("7.00")', 'cap=_D("130.00")', 'express_surcharge=_D("18.00")', 'Decimal("33.46")', 'Decimal("0.0175")',
                   '_qar("100.00"), _qar("12000.00")', '("bank_deposit", "wallet"), "STD-C"'):
        assert needle in code, needle
    for needle in ("| 1,000.00 | 2.20% | 3.50 |", "| 5,000.00 | 1.60% | 12.00 |", "| no limit | 1.10% | 45.00 |",
                   "Minimum fee QAR 7.00, cap QAR 130.00, express surcharge QAR 18.00."):
        assert needle in ticket, needle


def test_every_template_has_todos_and_the_sections_the_grader_reads():
    templates = ASSETS / "templates"
    for name in ("memory.md", "spec.md", "plan.md", "adr.md", "review.md", "agent-log.md", "retrospective.md", "corridors.md"):
        text = (templates / name).read_text(encoding="utf-8")
        assert "TODO" in text and checks_m14._TODO.search(text), name  # noqa: SLF001 (every template is flagged as unfinished)
    spec = checks.markdown_sections(templates / "spec.md")
    assert not checks_m14.missing_sections(spec, checks_m14.SPEC_SECTIONS, min_words=1)
    retro = checks.markdown_sections(templates / "retrospective.md")
    assert not checks_m14.missing_sections(retro, checks_m14.RETRO_SECTIONS, min_words=1)
    review = checks.markdown_sections(templates / "review.md")
    assert not checks_m14.missing_sections(review, ["Verdict", "What I ran", "Findings", "Second reviewer"], min_words=1)
    adr = [checks._norm(s.title) for s in checks.markdown_outline(templates / "adr.md")]  # noqa: SLF001
    assert [t for t in adr if t in {"status", "context", "decision", "consequences"}] == ["status", "context", "decision", "consequences"]


def test_the_baseline_hardening_files_pass_the_grader_and_the_samples_behave(tmp_path):
    import subprocess
    import sys

    guard = ASSETS / "harden" / "guard.py"
    for sample in sorted((ASSETS / "hook-samples").glob("*.json")):
        done = subprocess.run([sys.executable, str(guard)], input=sample.read_text(encoding="utf-8"), capture_output=True, text=True)
        assert done.returncode == (2 if sample.name.startswith("block-") else 0), sample.name
        if sample.name.startswith("block-"):
            assert done.stderr.startswith("Blocked:")
    data = json.loads((ASSETS / "harden" / "settings.json").read_text(encoding="utf-8"))
    assert checks_m14._guard_registered(data)  # noqa: SLF001


def _guard_verdict(command: str) -> int:
    import subprocess
    import sys

    document = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
    return subprocess.run([sys.executable, str(ASSETS / "harden" / "guard.py")], input=document, capture_output=True, text=True).returncode


@pytest.mark.parametrize("command", checks_m14.HOOK_BLOCK + checks_m14.HOOK_BLOCK_HARDER + [
    'sh -ec "rm -rf x"', "find . -name '*.pyc' -delete", "git -c alias.p=push p", "xargs rm -rf"])
def test_the_baseline_guard_blocks_what_the_grader_asks_it_to_block(command):
    assert _guard_verdict(command) == 2, command


@pytest.mark.parametrize("command", checks_m14.HOOK_ALLOW + checks_m14.HOOK_ALLOW_HARDER + ["find . -name '*.py'", "uv run pytest -q"])
def test_the_baseline_guard_allows_the_harmless(command):
    assert _guard_verdict(command) == 0, command


def test_the_mutation_plugin_knows_every_mutant_the_grader_runs():
    import sys

    sys.path.insert(0, str(LAB.HERE / "plugins"))
    try:
        import m14_mutate
    finally:
        sys.path.remove(str(LAB.HERE / "plugins"))
    assert set(checks_m14.MUTANTS) == set(m14_mutate.DESCRIPTIONS)


def test_helpers_read_numbers_tables_and_paths_sensibly():
    assert checks_m14.numbers_in("a 1,000.00 b 12000 c 2.20% d AC3 e 0.0175") == {
        checks_m14.Decimal("1000"), checks_m14.Decimal("12000"), checks_m14.Decimal("2.2"), checks_m14.Decimal("0.0175")}
    rows = checks_m14.table_rows("| A | B |\n|---|---|\n| 1 | `x` |\n| 2 | y |\n\ntext\n")
    assert rows == [["1", "`x`"], ["2", "y"]]
    files = {"src/remit/fees.py", "docs/corridors.md"}
    assert checks_m14.resolves("fees.py", files) and checks_m14.resolves("src/remit/", files) and not checks_m14.resolves("risk.py", files)
    assert checks_m14.looks_like_path("docs/corridors.md") and not checks_m14.looks_like_path("pytest -q") and not checks_m14.looks_like_path("Decimal(1)")
    assert checks_m14.total_minutes("Total minutes: 42\n") == 42 and checks_m14.total_minutes("**Total minutes:** 7") == 7


# --------------------------------------------------------------------------------------------
# findings of the learner dry-run: rules that were hidden, brittle or misleading
# --------------------------------------------------------------------------------------------
def plan_rows(work: Path, extra: int) -> str:
    """The reference plan with ``extra`` more rows after step 9 (each a sound small step with its own commit header)."""
    text = (work / PLAN_PATH).read_text(encoding="utf-8")
    anchor = next(line for line in text.splitlines() if line.startswith("| 9 |"))
    rows = [f"| {9 + n} | Small step {n} | `docs/corridors.md` | AC1 | read the page | `docs(docs): tidy the corridors page, part {n}` |"
            for n in range(1, extra + 1)]
    return text.replace(anchor, "\n".join([anchor, *rows]))


def test_a_finer_plan_with_sixteen_steps_is_sound(work):
    (work / PLAN_PATH).write_text(plan_rows(work, 7), encoding="utf-8")
    commit(work, "docs(specs): plan in smaller steps")
    result = grade(work)
    assert PLAN not in failing(result), describe(result)
    assert failing(result) <= {PLAN_HISTORY}  # only the advisory "history follows the plan" can notice the extra steps


def test_a_plan_with_too_many_or_too_few_steps_says_the_range(work):
    original = (work / PLAN_PATH).read_text(encoding="utf-8")
    (work / PLAN_PATH).write_text(plan_rows(work, 22), encoding="utf-8")
    commit(work, "docs(specs): plan every keystroke")
    result = grade(work)
    assert PLAN in failing(result) and "31 numbered steps (5 to 30 expected" in result[PLAN].detail
    (work / PLAN_PATH).write_text("\n".join(ln for ln in original.splitlines() if not re.match(r"\| [4-9] \|", ln)) + "\n", encoding="utf-8")
    commit(work, "docs(specs): shorten the plan")
    assert "3 numbered steps (5 to 30 expected" in grade(work)[PLAN].detail


def test_a_plan_commit_header_that_is_too_long_is_explained(work):
    long_header = "`feat(fx): add the BDT mid rate and margin with a very long explanation of why it is needed`"
    rewrite(work, PLAN_PATH, lambda t: t.replace("`feat(fx): add the BDT mid rate and margin`", long_header))
    commit(work, "docs(specs): longer header")
    result = grade(work)
    assert PLAN in failing(result)
    assert "commit header" in result[PLAN].detail and "72" in result[PLAN].detail and "type(scope): subject" in result[PLAN].detail


def test_a_file_that_a_line_says_does_not_exist_is_not_a_claim_that_it_does(work):
    with open(work / "CLAUDE.md", "a", encoding="utf-8") as handle:
        handle.write("- `docs/ARCHITECTURE.md` sections 5 and 6 are stale (daily limits, `risk.py`, which does not exist): do not fix them here.\n")
    commit(work, "chore(claude): note the stale architecture text")
    rewrite(work, PLAN_PATH, lambda t: t.replace("### Stop rules\n", "### Stop rules\nThe `risk.py` text in the architecture page is stale: that file does not exist, and fixing it is another ticket.\n"))
    commit(work, "docs(specs): add a stop rule")
    assert_failing(grade(work))


def test_a_path_with_no_denial_on_its_line_is_still_a_claim(work):
    with open(work / "CLAUDE.md", "a", encoding="utf-8") as handle:
        handle.write("- Fees are priced by `src/remit/pricing.py`.\n")
    commit(work, "chore(claude): name a file")
    result = grade(work)
    assert_failing(result, MEMORY)
    assert "src/remit/pricing.py" in result[MEMORY].detail


def test_documents_may_be_named_before_they_exist_and_the_denial_rule_is_per_line():
    files = {"src/remit/fees.py"}
    assert checks_m14.unresolved_paths("See `docs/corridors.md`, `specs/REMIT-414.md` and `docs/adr/0001-x.md`.", files) == []
    assert checks_m14.unresolved_paths("See `docs/other.md` and `fees.py`.", files) == ["docs/other.md"]
    assert checks_m14.unresolved_paths("`risk.py` does not exist.\nBut `risk.py` is used here.", files) == ["risk.py"]
    assert checks_m14.unresolved_paths("The old `rates.py` is gone.", files) == []
    # the denial excuses its own sentence or table cell, not the whole line or row
    assert checks_m14.unresolved_paths("| 1 | `tests/old.py` | fails because the corridor does not exist yet |", files) == ["tests/old.py"]
    assert checks_m14.unresolved_paths("`a.py` does not exist. See `b.py`.", files) == ["b.py"]


def test_the_word_todo_in_a_sentence_is_fine_but_a_placeholder_is_not(work):
    with open(work / RETRO_PATH, "a", encoding="utf-8") as handle:
        handle.write("\nThe old TODO in the test helpers is not mine, and my prompt said: no TODO comments.\n")
    commit(work, "docs(docs): add a note to the retrospective")
    assert_failing(grade(work))
    todo = checks_m14._TODO  # noqa: SLF001
    for placeholder in ("TODO: write this", "| 1 | TODO | x |", "Total minutes: TODO (from the log)", "TODO", "`TODO`", "### Rollback\nTODO\n", "- TODO: later"):
        assert todo.search(placeholder), placeholder
    for prose in ("the old TODO in the helpers", "no TODO comments", "| a TODO comment | x |", "TODOs are tracked elsewhere"):
        assert not todo.search(prose), prose


def test_hollow_tests_that_only_call_the_code_do_not_pass(work):
    """The dry-run's false positive: seventeen tests that call get_corridor and assert nothing, with the criteria in docstrings."""
    body = "from remit.corridors import get_corridor\n\n\n" + "\n\n".join(
        f'def test_ac{n % 9 + 1}_hollow_{n}():\n    """AC{n % 9 + 1}: proved by calling the corridor."""\n    get_corridor("QAR", "BDT")\n' for n in range(17))
    (work / TESTS_PATH).write_text(body, encoding="utf-8")
    commit(work, "test(corridors): cover every criterion")
    result = grade(work)
    assert_failing(result, TRACE, TEETH)  # they do fail on the starter (no such corridor), but they check nothing
    assert "0 assertions in 17 new tests" in result[TRACE].detail
    assert "catch 0 of 6" in result[TEETH].detail


def test_hollow_tests_with_a_truth_test_of_the_corridor_do_not_pass(work):
    body = "from remit.corridors import get_corridor\n\n\n" + "\n\n".join(
        f'def test_ac{n % 9 + 1}_truthy_{n}():\n    assert get_corridor("QAR", "BDT")\n' for n in range(12))
    (work / TESTS_PATH).write_text(body, encoding="utf-8")
    commit(work, "test(corridors): cover every criterion")
    assert_failing(grade(work), TRACE, TEETH)


def test_tests_that_compute_the_expected_value_with_the_code_are_caught_by_the_deliberate_defects(work):
    head = ('"""AC1 to AC9, circular: every expected value comes from the code under test."""\n'
            "from remit.corridors import get_corridor\nfrom remit.fees import quote_fee\nfrom remit.money import Money\n\n\n")
    amounts = ["100", "500", "1000", "1000.01", "5000", "5000.01", "10000", "12000", "250", "300", "700", "900"]
    body = head + "\n\n".join(
        f'def test_ac{n % 9 + 1}_circular_{n}():\n    corridor = get_corridor("QAR", "BDT")\n    expected = quote_fee(Money("{a}", "QAR"), corridor)\n'
        f'    assert quote_fee(Money("{a}", "QAR"), corridor) == expected\n    assert corridor.max_send == get_corridor("QAR", "BDT").max_send\n'
        for n, a in enumerate(amounts))
    (work / TESTS_PATH).write_text(body, encoding="utf-8")
    commit(work, "test(corridors): cover every criterion")
    result = grade(work)
    assert_failing(result, TEETH)  # they fail on the starter, they pass on the learner's code, and no wrong number worries them
    assert "catch 0 of 6" in result[TEETH].detail and "they miss" in result[TEETH].detail


def test_a_guard_that_blocks_but_gives_no_reason_is_not_called_non_blocking(work):
    (work / ".claude/hooks/guard.py").write_text("import sys\nsys.stdin.read()\nsys.exit(2)\n", encoding="utf-8")
    commit(work, "chore(claude): block everything quietly")
    result = grade(work)
    assert HOOK in failing(result)
    assert "no reason" in result[HOOK].detail and "which does not block" not in result[HOOK].detail


def test_a_guard_that_reads_only_the_first_words_passes_the_required_check_but_not_the_wrapper_cases(work):
    (work / ".claude/hooks/guard.py").write_text('''import json
import shlex
import sys


def stop(reason):
    print("Blocked: " + reason, file=sys.stderr)
    sys.exit(2)


try:
    data = json.load(sys.stdin)
except ValueError:
    stop("not JSON")
if data.get("tool_name") != "Bash":
    sys.exit(0)
command = (data.get("tool_input") or {}).get("command")
if not isinstance(command, str) or not command.strip():
    stop("no command")
first, second = (shlex.split(command) + ["", ""])[:2]
if (first, second) in {("rm", "-rf"), ("git", "push"), ("git", "reset"), ("pip", "install")} or first in {"sudo", "curl"} or (first, second) == ("cat", ".env"):
    stop("not allowed")
''', encoding="utf-8")
    commit(work, "chore(claude): a first-words guard")
    assert_failing(grade(work), HOOK_HARDER)


def test_a_scratch_script_committed_in_the_repository_is_out_of_scope_and_the_hint_says_where_it_belongs(work):
    (work / "scratch").mkdir()
    (work / "scratch/find_ties.py").write_text("print(1)\n", encoding="utf-8")
    commit(work, "chore(scratch): add a throwaway script")
    result = grade(work)
    assert_failing(result, SCOPE)
    assert "scratch/find_ties.py" in result[SCOPE].detail and "outside the repository" in result[SCOPE].hint


def test_any_lower_case_scope_is_accepted_in_a_commit_header(work):
    with open(work / "CLAUDE.md", "a", encoding="utf-8") as handle:
        handle.write("- Never skip the corridor checklist.\n")
    commit(work, "chore(agent): add a never rule")
    assert_failing(grade(work))


def test_code_committed_before_any_test_is_not_test_first(work):
    gitutil.git(work, "reset", "-q", "--soft", "lab-start")
    gitutil.git(work, "reset", "-q")
    who = ["-c", "user.name=Najm Learner", "-c", "user.email=learner@najm.example"]
    gitutil.git(work, "add", "src")
    gitutil.git(work, *who, "commit", "-q", "-m", "feat(corridors): open the Bangladesh corridor")
    gitutil.git(work, "add", "tests")
    gitutil.git(work, *who, "commit", "-q", "-m", "test(corridors): pin the corridor")
    commit(work, "docs(docs): everything else")
    result = grade(work)
    assert TESTS_FIRST in failing(result)
    assert "Committing them alone leaves a red commit" in result[TESTS_FIRST].hint


def test_assertions_are_counted_by_what_they_say():
    count = checks_m14.assertion_count
    assert count("def test_a():\n    assert x == 1\n    assert 'a' in y\n    assert not z\n") == 3
    assert count("def test_a():\n    assert True\n    assert get_corridor('QAR', 'BDT')\n    assert 1 == 1\n") == 0
    assert count("def test_a():\n    with pytest.raises(ValueError):\n        f()\n    self.assertEqual(a, b)\n") == 2
    assert count("def test_a(:\n") == 0
