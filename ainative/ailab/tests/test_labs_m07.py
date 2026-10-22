"""Negative and alternative-solution tests for m07 (the legacy ledger, the refactor and the najmkit migration).

Each test starts from a copy of the started lab (or of the lab after the reference solution), makes the kind of
change a learner or an agent really makes, grades it and says exactly which checks fail. The expensive checks
(the mutation run and the per-commit test runs) are stubbed in the tests that are not about them, so that the
suite stays fast; the tests that are about them run them for real.
"""
from __future__ import annotations

import shutil
import subprocess
import textwrap
from pathlib import Path

import pytest

from ailab import checks_m07 as m07, framework, gitutil
from ailab.labs.m07_legacy import lab as lab_module
from ailab.labs.m07_legacy.lab import (
    C_AUDIT, C_BASELINE, C_CLEAN, C_COUNT, C_DOCS, C_GREEN, C_KEPT, C_LEGACY, C_MEMORY, C_MESSAGES, C_MUTANTS,
    C_MUTANTS_ALL, C_PLAN, C_QUIRKS, C_SCOPE, C_SECRETS, C_SERVICE, C_STATE, C_SUITE, C_V1CALLS, C_V1GONE, C_WROTE,
)
from conftest import learner_commit, start

HERE = Path(framework.LABS_DIR) / "m07_legacy"
LEDGER = "src/remit/ledger.py"
SERVICE = "src/remit/service.py"
ALL = {
    C_WROTE, C_BASELINE, C_MUTANTS, C_MUTANTS_ALL, C_SUITE, C_KEPT, C_QUIRKS, C_SERVICE, C_STATE, C_LEGACY, C_V1CALLS, C_V1GONE,
    C_AUDIT, C_DOCS, C_SCOPE, C_MESSAGES, C_COUNT, C_GREEN, C_CLEAN, C_SECRETS, C_PLAN, C_MEMORY,
}


# --------------------------------------------------------------------------------------------
# fixtures and helpers
# --------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def started(tmp_path_factory) -> Path:
    return start("m07", tmp_path_factory.mktemp("m07-start") / "work")


@pytest.fixture(scope="module")
def solved(tmp_path_factory) -> Path:
    work = start("m07", tmp_path_factory.mktemp("m07-solved") / "work")
    framework.solve_lab(framework.load_lab("m07"), work)
    return work


@pytest.fixture
def work(started, tmp_path) -> Path:
    target = tmp_path / "work"
    shutil.copytree(started, target)
    return target


@pytest.fixture
def done(solved, tmp_path) -> Path:
    target = tmp_path / "work"
    shutil.copytree(solved, target)
    return target


@pytest.fixture
def cheap(monkeypatch):
    """Stub the two expensive checks (mutation run, one suite run per commit) with their passing answers."""
    real_report, real_green = m07.characterization_report, m07.green_commits
    monkeypatch.setattr(m07, "characterization_report", cheap_report)
    monkeypatch.setattr(m07, "green_commits", lambda work, **kw: ([], len(gitutil.commits_since(work))))
    return real_report, real_green


def grade(work: Path) -> dict[str, framework.Check]:
    result = framework.grade_lab(framework.load_lab("m07"), work, catch=False)
    return {c.name: c for c in result}


def failing(result: dict[str, framework.Check]) -> set[str]:
    return {name for name, check in result.items() if not check.ok}


def assert_only(result: dict[str, framework.Check], *expected: str) -> None:
    got = failing(result)
    detail = "\n".join(f"  {'ok  ' if c.ok else 'FAIL'} {n}: {c.detail}" for n, c in result.items())
    assert got == set(expected), f"expected failures {set(expected)}, got {got}\n{detail}"


def write(work: Path, rel: str, text: str) -> None:
    framework.write_file(work, rel, textwrap.dedent(text))


def edit(work: Path, rel: str, old: str, new: str, count: int = 1) -> None:
    framework.edit_file(work, rel, old, new, count=count)


def commit(work: Path, message: str) -> None:
    learner_commit(work, message)


def reference_suite() -> str:
    return (HERE / "solution" / "01-characterization-tests" / "tests" / "test_ledger_characterization.py").read_text(encoding="utf-8")


def reference_port() -> str:
    return (HERE / "assets" / "ledger_port.py").read_text(encoding="utf-8")


def legacy_work_with_tests(work: Path, test_source: str, *, name: str = "tests/test_ledger_characterization.py", port: bool = True) -> None:
    """The started repository plus a learner's test file (and the seam), uncommitted-then-committed as one commit."""
    if port:
        write(work, "tests/ledger_port.py", reference_port())
    write(work, name, test_source)
    commit(work, "test(ledger): pin the ledger's behaviour")


# --------------------------------------------------------------------------------------------
# the lab as a whole
# --------------------------------------------------------------------------------------------
def test_the_starter_fails_for_the_right_reasons_and_leaks_no_answers(started, tmp_path):
    work = tmp_path / "work"
    shutil.copytree(started, work)
    result = grade(work)
    assert set(result) == ALL
    expected = {C_WROTE, C_BASELINE, C_MUTANTS, C_MUTANTS_ALL, C_QUIRKS, C_SERVICE, C_STATE, C_LEGACY, C_V1CALLS, C_V1GONE,
                C_DOCS, C_SCOPE, C_MESSAGES, C_COUNT, C_GREEN, C_PLAN}
    if lab_module.stale_memory_lines(work):  # the reference project memory of lab m02 calls the ledger untested
        expected.add(C_MEMORY)
    assert_only(result, *expected)
    # the visible suite is green at the start: the v1 wrappers keep every old call working
    assert result[C_SUITE].ok and result[C_KEPT].ok and result[C_AUDIT].ok
    assert all(c.hint for c in result.values() if not c.ok and c.required)
    text = " ".join(c.detail + c.hint for c in result.values())
    for secret in ("ROUND_HALF_EVEN", "0.35", "half-even", "Decimal('3.04')"):
        assert secret not in text, f"a check leaks {secret!r}"


def test_the_reference_solution_passes_every_check(done):
    assert_only(grade(done))


def test_the_seed_adds_najmkit_2_beside_the_old_names(started):
    for name in ("ids.py", "clock.py", "audit.py"):
        assert "deprecated v1 names" in (started / "src" / "najmkit" / name).read_text(encoding="utf-8")
    assert (started / "docs" / "najmkit-v2-migration.md").is_file()
    assert (started / "lab-assets" / "ledger_port.py").is_file() and (started / "lab-assets" / "refactoring-plan-template.md").is_file()
    assert "API_VERSION = \"v2\"" in (started / "src" / "najmkit" / "__init__.py").read_text(encoding="utf-8")


def test_the_deprecated_names_work_but_warn(started):
    code = (
        "import warnings\n"
        "from najmkit import ids, clock, audit\n"
        "with warnings.catch_warnings(record=True) as seen:\n"
        "    warnings.simplefilter('always')\n"
        "    ids.use_generator(ids.SequentialIds()); a = ids.new_id('TRF'); b = ids.make_id('TRF')\n"
        "    print(a, b, audit.log_event('x.y', n=object().__class__.__name__)['n'], len(seen))\n"
    )
    result = subprocess.run(["python", "-c", code], cwd=started, env={"PYTHONPATH": str(started / "src"), "PATH": __import__("os").environ["PATH"]},
                            capture_output=True, text=True)
    assert result.stdout.split() == ["TRF-000001", "TRF-000002", "object", "3"], result.stderr


def test_every_mutant_applies_exactly_once_to_the_original_ledger(started):
    original = (started / LEDGER).read_text(encoding="utf-8")
    for mutant in m07.MUTANTS:
        assert original.count(mutant.old) == mutant.count, mutant.id
        assert mutant.description and "_" not in mutant.description.split()[0], f"{mutant.id}: describe behaviour, not code"
    assert len({m.id for m in m07.MUTANTS}) == len(m07.MUTANTS) == 16


# --------------------------------------------------------------------------------------------
# Part 1: the characterization tests
# --------------------------------------------------------------------------------------------
def test_the_reference_suite_kills_every_mutant_and_an_alternative_compact_suite_kills_enough(work):
    legacy_work_with_tests(work, reference_suite())
    report = m07.characterization_report(work)
    assert report.baseline_ok and len(report.killed) == 16 and not report.survived and not report.not_applied


ALTERNATIVE_SUITE = '''
"""A different learner, a different style: fewer, denser tests, no parametrize, a helper that posts."""
from decimal import Decimal

import pytest

from ledger_port import ledger_of, make_ledger
from remit.errors import CurrencyMismatch, DuplicatePosting, InvalidAmount
from remit.money import Money


def q(v, cur="QAR"):
    return Money(v, cur)


def books(fee="12.00", send="500.00", tid="T1", cust="C9"):
    book = make_ledger()
    entries = book.post_transfer(tid, cust, q(send), q(fee))
    return book, entries


def test_postings_in_order():
    _, e = books()
    assert [(x["account"], x["side"], str(x["amount"])) for x in e] == [
        ("CUSTOMER:C9", "D", "512.00"), ("PAYOUT_CLEARING", "C", "500.00"), ("FEE_INCOME", "C", "8.40"), ("PARTNER_PAYABLE", "C", "3.60")]


def test_entry_metadata():
    _, e = books()
    assert [x["entry_id"] for x in e] == ["JNL-000001", "JNL-000002", "JNL-000003", "JNL-000004"]
    assert {x["posted_at"] for x in e} == {"2026-03-02T09:00:00+00:00"} and {x["transfer_id"] for x in e} == {"T1"}


def test_time_moves_with_the_clock(clock):
    book = make_ledger()
    clock.advance(minutes=5)
    assert book.post_transfer("T1", "C", q(10), q(1))[0]["posted_at"] == "2026-03-02T09:05:00+00:00"


def test_balances():
    book, _ = books()
    assert [book.balance(a) for a in book.accounts()] == [Decimal("-512.00"), Decimal("8.40"), Decimal("3.60"), Decimal("500.00")]


def test_ties_go_to_the_even_cent():
    book, _ = books(fee="10.15")
    assert (book.balance("PARTNER_PAYABLE"), book.balance("FEE_INCOME")) == (Decimal("3.04"), Decimal("7.11"))
    book, _ = books(fee="10.25")
    assert (book.balance("PARTNER_PAYABLE"), book.balance("FEE_INCOME")) == (Decimal("3.08"), Decimal("7.17"))


def test_share_is_thirty_percent():
    book, _ = books(fee="100.00")
    assert book.balance("PARTNER_PAYABLE") == Decimal("30.00")


def test_zero_legs_are_not_posted():
    book, e = books(fee="0.00")
    assert len(e) == 2 and book.accounts() == ["CUSTOMER:C9", "PAYOUT_CLEARING"]
    book, e = books(fee="0.01")
    assert [x["account"] for x in e][-1] == "FEE_INCOME" and len(e) == 3


def test_refusals():
    book = make_ledger()
    for send, fee, err in [(q(5, "EGP"), q(1), CurrencyMismatch), (q(5), q(1, "EGP"), CurrencyMismatch), (q(0), q(1), InvalidAmount),
                           (q(5), q(-1), InvalidAmount)]:
        with pytest.raises(err):
            book.post_transfer("X", "C", send, fee)
    assert book.journal() == []


def test_duplicates():
    book, _ = books()
    with pytest.raises(DuplicatePosting):
        book.post_transfer("T1", "C9", q(1), q(1))
    assert len(book.journal()) == 4


def test_reading_creates_and_lists_sorted():
    book, _ = books()
    assert book.balance("ZZZ") == 0 and book.accounts()[-1] == "ZZZ" and book.accounts() == sorted(book.accounts())


def test_journal_is_a_copy():
    book, _ = books()
    book.journal().clear()
    assert len(book.journal()) == 4


def test_service_posts(service):
    service.send("C001", q(500), "INR", "Ravi Kumar")
    book = ledger_of(service)
    assert book.balance("CUSTOMER:C001") == Decimal("-512.00") and book.balance("PARTNER_PAYABLE") == Decimal("3.60")
'''


def test_an_alternative_compact_suite_is_accepted(work):
    legacy_work_with_tests(work, ALTERNATIVE_SUITE, name="tests/test_ledger_quirks.py")
    report = m07.characterization_report(work)
    assert report.baseline_ok and len(report.killed) >= m07.MIN_KILLED, [m.description for m in report.survived]


def test_tests_that_assert_nothing_pass_on_the_original_and_catch_nothing(work, cheap):
    body = "\n".join(
        f"def test_posting_{i}():\n    ledger = make_ledger()\n    ledger.post_transfer('T{i}', 'C1', Money('500', 'QAR'), Money('12', 'QAR'))\n"
        for i in range(12)
    )
    legacy_work_with_tests(work, "from ledger_port import make_ledger\nfrom remit.money import Money\n\n" + body)
    report = cheap[0](work)
    assert report.baseline_ok and not report.killed and len(report.survived) == 16


def test_a_suite_that_only_checks_the_happy_path_misses_the_quirks(work):
    happy = textwrap.dedent('''
        from decimal import Decimal
        from ledger_port import make_ledger
        from remit.money import Money

        def test_a(): assert len(make_ledger().post_transfer("T1", "C", Money("500", "QAR"), Money("12", "QAR"))) == 4
        def test_b(): assert make_ledger().post_transfer("T1", "C", Money("500", "QAR"), Money("12", "QAR"))[0]["side"] == "D"
        def test_c(): assert make_ledger().post_transfer("T1", "C", Money("500", "QAR"), Money("12", "QAR"))[1]["amount"] == Decimal("500")
        def test_d():
            book = make_ledger(); book.post_transfer("T1", "C", Money("500", "QAR"), Money("12", "QAR"))
            assert book.balance("PAYOUT_CLEARING") == Decimal("500")
        def test_e():
            book = make_ledger(); book.post_transfer("T1", "C", Money("500", "QAR"), Money("12", "QAR"))
            assert book.balance("PARTNER_PAYABLE") == Decimal("3.60")
        ''') + "\n".join(f"def test_more_{i}(): assert make_ledger().journal() == []" for i in range(6))
    legacy_work_with_tests(work, happy)
    result = grade(work)
    assert result[C_WROTE].ok and result[C_BASELINE].ok
    assert not result[C_MUTANTS].ok and "they miss:" in result[C_MUTANTS].detail
    assert not result[C_MUTANTS_ALL].ok


def test_too_few_tests_do_not_count_as_a_suite(work):
    legacy_work_with_tests(work, "from ledger_port import make_ledger\n\ndef test_it(): assert make_ledger().accounts() == []\n")
    assert not grade(work)[C_WROTE].ok


def test_tests_written_against_the_new_class_do_not_describe_the_original(done):
    """Written after the refactor, against Ledger() directly: they cannot pass on the code the learner started from."""
    write(done, "tests/test_ledger_direct.py", "\n".join(
        ["from remit.ledger import Ledger", ""] + [f"def test_direct_{i}(): assert Ledger().accounts() == []" for i in range(12)]))
    commit(done, "test(ledger): add direct tests")
    result = grade(done)
    assert not result[C_BASELINE].ok and "original code" in result[C_BASELINE].detail
    assert not result[C_MUTANTS].ok and "not checked yet" in result[C_MUTANTS].detail


def test_tests_that_depend_on_an_edited_conftest_do_not_describe_the_original(work):
    edit(work, "tests/conftest.py", "@pytest.fixture\ndef now():", "@pytest.fixture\ndef book():\n    from ledger_port import make_ledger\n    return make_ledger()\n\n\n@pytest.fixture\ndef now():")
    write(work, "tests/ledger_port.py", reference_port())
    write(work, "tests/test_ledger_fixture.py", "\n".join(f"def test_fixture_{i}(book): assert book.accounts() == []" for i in range(12)))
    commit(work, "test(ledger): use a fixture")
    result = grade(work)
    assert not result[C_BASELINE].ok


def test_tests_that_pin_what_the_learner_thinks_is_right_instead_of_what_the_code_does(work):
    wrong = reference_suite().replace('("10.15", "3.04", "7.11"),  # 3.045 -> 3.04 (half-up would say 3.05)', '("10.15", "3.05", "7.10"),')
    assert wrong != reference_suite()
    legacy_work_with_tests(work, wrong)
    result = grade(work)
    assert not result[C_BASELINE].ok and "test_the_partner_share" in result[C_BASELINE].detail
    assert not result[C_MUTANTS].ok


def test_a_hung_characterization_test_cannot_hang_the_grader(work):
    legacy_work_with_tests(work, "from ledger_port import make_ledger\n\n" + "\n".join(
        f"def test_loop_{i}():\n    while True:\n        pass\n" for i in range(11)))
    report = m07.characterization_report(work, timeout=3)
    assert not report.baseline_ok and "time" in report.baseline_detail


# --------------------------------------------------------------------------------------------
# Part 2: the refactor
# --------------------------------------------------------------------------------------------
def test_improving_the_unknown_account_quirk_is_caught_by_the_hidden_suite_and_the_learners_own_tests(done, cheap):
    edit(done, LEDGER, '        if account not in self._balances:\n            self._balances[account] = Decimal("0")\n        return self._balances[account]',
         '        return self._balances.get(account, Decimal("0"))')
    commit(done, "fix(ledger): stop balance() from creating accounts")
    result = grade(done)
    assert_only(result, C_SUITE, C_QUIRKS)
    assert "test_asking_for_an_unknown_account" in result[C_QUIRKS].detail


def test_rounding_the_partner_share_half_up_during_the_refactor(done, cheap):
    edit(done, LEDGER, "rounding=ROUND_HALF_EVEN)", 'rounding="ROUND_HALF_UP")')
    commit(done, "refactor(ledger): round everything the same way")
    result = grade(done)
    assert_only(result, C_SUITE, C_QUIRKS, C_SERVICE)


def test_float_arithmetic_for_the_partner_share(done, cheap):
    edit(done, LEDGER, "partner = (fee.amount * PARTNER_SHARE).quantize(_CENT, rounding=ROUND_HALF_EVEN)  # Q-LED-1",
         "partner = Decimal(str(round(float(fee.amount) * 0.30, 2)))")
    commit(done, "refactor(ledger): simplify the partner share")
    assert {C_QUIRKS, C_SUITE} <= failing(grade(done))


def test_state_moved_into_a_class_attribute_is_still_shared_state(done, cheap):
    edit(done, LEDGER, "    def __init__(self) -> None:\n        self._balances: dict[str, Decimal] = {}  # account -> credits minus debits\n        self._journal: list[dict[str, Any]] = []  # every posted entry, oldest first\n",
         "    _balances: dict[str, Decimal] = {}\n    _journal: list[dict[str, Any]] = []\n\n    def __init__(self) -> None:\n        pass\n")
    commit(done, "refactor(ledger): keep the books on the class")
    result = grade(done)
    assert not result[C_STATE].ok and "class attribute" in result[C_STATE].detail
    assert not result[C_QUIRKS].ok  # two ledgers share their books


def test_leaving_the_module_level_wrappers_and_a_default_instance(started, tmp_path, cheap):
    """The state of the reference solution after step 2: Ledger exists, the module functions still wrap one shared instance."""
    work = tmp_path / "work"
    shutil.copytree(started, work)
    for step in lab_module.solution_steps()[:3]:  # tests, Ledger class, service owns a ledger
        for rel in step["files"]:
            target = work / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(lab_module.step_file(step, rel), target)
        commit(work, step["message"])
    result = grade(work)
    assert not result[C_STATE].ok and "_DEFAULT" in result[C_STATE].detail
    assert not result[C_LEGACY].ok and "reset" in result[C_LEGACY].detail
    assert result[C_SERVICE].ok and result[C_SUITE].ok  # the intermediate state is a good place to stop for lunch, not to ship


def test_a_service_whose_default_ledger_is_shared_by_every_service(done, cheap):
    edit(done, LEDGER, "def customer_account(customer_id: str) -> str:", "_SHARED: list = []\n\n\ndef customer_account(customer_id: str) -> str:")
    edit(done, SERVICE, "self.ledger = ledger if ledger is not None else Ledger()  # one set of books per service",
         "self.ledger = ledger if ledger is not None else (ledger_module._SHARED or ledger_module._SHARED.append(Ledger()) or ledger_module._SHARED)[0]")
    edit(done, SERVICE, "from remit.ledger import Ledger\n", "from remit import ledger as ledger_module\nfrom remit.ledger import Ledger\n")
    commit(done, "refactor(service): share the default ledger")
    result = grade(done)
    assert not result[C_SERVICE].ok and not result[C_STATE].ok


def test_giving_each_ledger_its_own_id_counter_changes_the_ids(done, cheap):
    edit(done, LEDGER, '"entry_id": ids.make_id("JNL"),', '"entry_id": f"JNL-{len(self._journal) + 1:06d}",')
    commit(done, "refactor(ledger): number entries per ledger")
    result = grade(done)
    assert not result[C_QUIRKS].ok and not result[C_SERVICE].ok
    assert "test_entry_ids_still_come_from_one_process_wide_sequence" in result[C_QUIRKS].detail or "more" in result[C_QUIRKS].detail


def test_making_send_atomic_changes_a_documented_limitation(done, cheap):
    """'Fixing' D-SVC-1 while refactoring: the store is written before the ledger, so a store failure posts nothing."""
    text = (done / SERVICE).read_text(encoding="utf-8")
    ledger_line = "        self.ledger.post_transfer(transfer_id, customer.id, send_amount, fee)\n"
    save_line = "        self.store.save_transfer(transfer)\n"
    assert ledger_line in text and save_line in text
    text = text.replace(ledger_line, "")
    text = text.replace(save_line, save_line + ledger_line)
    (done / SERVICE).write_text(text, encoding="utf-8")
    commit(done, "refactor(service): save before posting")
    result = grade(done)
    assert not result[C_SERVICE].ok and "test_a_store_failure" in result[C_SERVICE].detail


def test_the_ledger_class_may_take_extra_optional_arguments_and_a_different_internal_layout(done, cheap):
    """An alternative sound refactor: keyword-only options, __slots__, a dict of lists. The interface in the ticket still holds."""
    text = (done / LEDGER).read_text(encoding="utf-8")
    text = text.replace("class Ledger:\n    \"\"\"One set of books: balances and a journal.\"\"\"\n\n    def __init__(self) -> None:",
                        "class Ledger:\n    \"\"\"One set of books: balances and a journal.\"\"\"\n\n    __slots__ = (\"_balances\", \"_journal\", \"label\")\n\n    def __init__(self, *, label: str = \"main\") -> None:\n        self.label = label")
    assert "__slots__" in text
    (done / LEDGER).write_text(text, encoding="utf-8")
    commit(done, "refactor(ledger): slots and an optional label")
    assert_only(grade(done))


# --------------------------------------------------------------------------------------------
# Part 3: the migration
# --------------------------------------------------------------------------------------------
def test_a_rename_only_migration_breaks_on_the_stricter_audit_values(done, cheap):
    edit(done, SERVICE, "send_amount=str(send_amount),\n            fee=str(fee),", "send_amount=send_amount,\n            fee=fee,")
    commit(done, "fix(service): pass the money objects to the audit trail")
    result = grade(done)
    assert not result[C_SUITE].ok and not result[C_AUDIT].ok


def test_a_tidy_conversion_in_the_rarely_tested_event_changes_the_audit_line(done, cheap):
    """The visible suite asserts the transfer.sent line but not transfer.rejected: a 'cleaner' amount slips through it."""
    edit(done, SERVICE, "            send_amount=str(amount),\n", "            send_amount=str(amount.amount),\n")
    commit(done, "refactor(service): audit plain amounts")
    result = grade(done)
    assert result[C_SUITE].ok  # green, and wrong
    assert_only(result, C_AUDIT)
    assert "600.00 QAR" not in result[C_AUDIT].detail + result[C_AUDIT].hint


def test_a_blind_replace_of_dot_now_breaks_the_injected_clock(done, cheap):
    edit(done, SERVICE, "now = self.clock.now()", "now = self.clock.utc_now()")
    commit(done, "refactor(service): use utc_now everywhere")
    result = grade(done)
    assert not result[C_SUITE].ok


def test_a_call_site_left_on_the_old_name_is_found_even_in_a_test_file(done, cheap):
    write(done, "tests/test_extra.py", """
        from najmkit import ids


        def test_old_name():
            assert ids.new_id("TRF").startswith("TRF-")
        """)
    commit(done, "test(ledger): add an id test")
    result = grade(done)
    assert not result[C_V1CALLS].ok and "tests/test_extra.py" in result[C_V1CALLS].detail
    assert not result[C_SUITE].ok  # the contract step removed the name, so the test fails too


def test_a_clock_object_or_fixture_called_clock_is_not_a_v1_call(done, cheap):
    write(done, "tests/test_extra.py", """
        from najmkit import clock


        def test_a_fixture_named_clock_has_a_now_method(clock):
            assert clock.now().year == 2026


        def test_the_module_function_has_a_new_name():
            assert clock.utc_now().year == 2026
        """)
    commit(done, "test(ledger): add clock tests")
    assert m07.v1_calls_left(done) == []


def test_skipping_the_contract_step_leaves_the_deprecated_names_in_najmkit(done, cheap):
    """Restore the wrappers (as at lab-start) after the call sites were moved."""
    for name in ("ids.py", "clock.py", "audit.py"):
        original = gitutil.file_at(done, "lab-start", f"src/najmkit/{name}")
        (done / "src" / "najmkit" / name).write_text(original, encoding="utf-8")
    commit(done, "chore(najmkit): keep the old names for now")
    result = grade(done)
    assert_only(result, C_V1GONE)
    assert "new_id" in result[C_V1GONE].detail


def test_stale_najmkit_docs_are_an_advisory_finding(done, cheap):
    gitutil_text = gitutil.file_at(done, "lab-start", "docs/najmkit.md")
    (done / "docs" / "najmkit.md").write_text(gitutil_text, encoding="utf-8")
    commit(done, "docs(najmkit): revert my edit")
    result = grade(done)
    assert_only(result, C_DOCS)
    assert not result[C_DOCS].ok and not [c for c in result.values() if not c.ok and c.required]


def test_stale_project_memory_is_an_advisory_finding(done, cheap):
    if not (done / "CLAUDE.md").is_file():
        pytest.skip("no reference project memory in this kit yet (m02)")
    with (done / "CLAUDE.md").open("a", encoding="utf-8") as handle:
        handle.write("- `ledger.py` keeps its state in module-level variables.\n")
    commit(done, "docs(ledger): note the module state")
    assert lab_module.stale_memory_lines(done)
    assert_only(grade(done), C_MEMORY)


# --------------------------------------------------------------------------------------------
# process
# --------------------------------------------------------------------------------------------
def test_one_big_commit_for_everything(done, cheap):
    subprocess.run(["git", "reset", "--soft", "lab-start"], cwd=done, check=True)
    commit(done, "refactor(ledger): ledger class and najmkit 2")
    result = grade(done)
    assert_only(result, C_COUNT)
    assert "1 new commit" in result[C_COUNT].detail


def test_a_codemod_script_kept_in_scripts_is_allowed(done, cheap):
    write(done, "scripts/codemod_najmkit.py", """
        \"\"\"The rename table as a script, so the migration can be re-run and reviewed.\"\"\"
        RENAMES = {"new_id": "make_id", "use_generator": "use_source", "log_event": "emit"}
        """)
    commit(done, "chore(najmkit): keep the codemod I used")
    assert_only(grade(done))


def test_uncommitted_work_is_reported(done, cheap):
    (done / "docs" / "notes.md").write_text("notes\n", encoding="utf-8")
    assert_only(grade(done), C_CLEAN)


@pytest.mark.parametrize("message", ["fixed the ledger", "refactor: move the books", "Refactor(ledger): Move the books", "refactor(ledger): move the books."],
                         ids=["no-convention", "no-scope", "wrong-case", "full-stop"])
def test_commit_messages_that_ignore_contributing_md(done, cheap, message):
    (done / "docs" / "notes.md").write_text("notes\n", encoding="utf-8")
    commit(done, message)
    assert_only(grade(done), C_MESSAGES)


def test_touching_an_unrelated_module_while_tidying(done, cheap):
    edit(done, "src/remit/fees.py", '"""', '"""(tidied) ', count=done.joinpath("src/remit/fees.py").read_text().count('"""'))
    commit(done, "refactor(fees): tidy the docstrings")
    result = grade(done)
    assert not result[C_SCOPE].ok and "src/remit/fees.py" in result[C_SCOPE].detail


def test_deleting_a_test_to_make_the_suite_green(done, cheap):
    text = (done / "tests" / "test_najmkit.py").read_text(encoding="utf-8")
    cut = text.index("def test_module_level_now_follows_the_installed_clock")
    end = text.index("def test_log_event_returns_the_record")
    (done / "tests" / "test_najmkit.py").write_text(text[:cut] + text[end:], encoding="utf-8")
    commit(done, "test(najmkit): drop a test that kept failing")
    result = grade(done)
    assert not result[C_KEPT].ok and "test_module_level_now_follows_the_installed_clock" in result[C_KEPT].detail


def test_a_red_commit_in_the_middle_is_an_advisory_finding(started, tmp_path, monkeypatch):
    """Step 4 of the reference solution without the conftest edit: reset() is gone but conftest still calls it."""
    work = tmp_path / "work"
    shutil.copytree(started, work)
    for index, step in enumerate(lab_module.solution_steps()):
        files = [f for f in step["files"] if not (index == 3 and f == "tests/conftest.py")]
        for rel in files:
            target = work / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(lab_module.step_file(step, rel), target)
        commit(work, step["message"])
        if index == 3:  # the red commit, then the repair
            shutil.copyfile(lab_module.step_file(step, "tests/conftest.py"), work / "tests" / "conftest.py")
            # conftest as of step 4 already uses the old najmkit names, which still exist at this point
            lab_module._update_memory(work)
            commit(work, "test(ledger): stop resetting the module-level ledger")
    monkeypatch.setattr(m07, "characterization_report", cheap_report)
    result = grade(work)
    assert_only(result, C_GREEN)
    assert "refactor(ledger): remove the module-level ledger state" in result[C_GREEN].detail


def cheap_report(work, *args, **kwargs):
    report = m07.CharacterizationReport(tests=["tests/test_ledger_characterization.py"], n_tests=28, baseline_ok=True)
    report.killed = list(m07.MUTANTS)
    return report


def test_a_secret_next_to_the_change(done, cheap):
    edit(done, "src/remit/store.py", "from najmkit import ids\n", 'from najmkit import ids\n\nGATEWAY_KEY = "sk-live-' + "9f8e7d6c5b4a3f2e1d0c" + '"\n')
    commit(done, "refactor(store): add a key")
    result = grade(done)
    assert not result[C_SECRETS].ok and "9f8e7d6c" not in result[C_SECRETS].detail + result[C_SECRETS].hint


def test_an_unfilled_plan_template_is_flagged_only_as_advisory(done, cheap):
    (done / "docs" / "refactoring-plan.md").write_text((HERE / "assets" / "refactoring-plan-template.md").read_text(encoding="utf-8"), encoding="utf-8")
    commit(done, "docs(refactoring): add the plan")
    result = grade(done)
    assert result[C_PLAN].ok  # structurally complete (the grader cannot judge the thinking); the lesson says so


def test_state_hidden_in_another_module_is_found(done, cheap):
    write(done, "src/remit/books.py", '"""A helper."""\n\n_BOOKS = {}\n')
    commit(done, "refactor(ledger): add a helper module")
    result = grade(done)
    assert not result[C_STATE].ok and "books.py" in result[C_STATE].detail


def test_a_constant_lookup_table_in_another_module_is_not_state(done, cheap):
    write(done, "src/remit/tables.py", '"""Constants."""\n\nSIGN = {"C": 1, "D": -1}\n')
    commit(done, "refactor(ledger): move the sign table to its own module")
    assert grade(done)[C_STATE].ok


# --------------------------------------------------------------------------------------------
# the helpers on their own
# --------------------------------------------------------------------------------------------
STATE = {
    "module dict": "_B = {}\n",
    "module list": "_J: list = []\n",
    "module instance": "_D = Ledger()\n",
    "defaultdict": "from collections import defaultdict\n_B = defaultdict(int)\n",
    "global statement": "def reset():\n    global _X\n    _X = 1\n",
    "class attribute": "class L:\n    books = {}\n",
    "augmented": "N = 0\nN += 1\n",
    "import-time call": "register()\n",
    # a lookup table is only state when the module changes it
    "a table that a function fills": '_B = {"a": 1}\ndef add(key):\n    _B[key] = 2\n',
    "a list that a function appends to": '_J = ["x"]\ndef add(entry):\n    _J.append(entry)\n',
    "a table that is cleared": '_B = {"a": 1}\ndef wipe():\n    _B.clear()\n',
    "a class table that is changed through self": 'class L:\n    books = {"a": 1}\n    def add(self, key):\n        self.books[key] = 2\n',
}
CLEAN = {
    "constants": 'from decimal import Decimal\nA = "x"\nS = Decimal("0.30")\nT = ("a", "b")\nF = frozenset(["a"])\n',
    "instance state": "class L:\n    def __init__(self):\n        self._b = {}\n",
    "annotation only": "x: int\n",
    "docstring and defs": '"""doc"""\n\ndef f():\n    return {}\n',
    "dunder all and a logger": 'import logging\n__all__ = ["Ledger"]\nlog = logging.getLogger(__name__)\n',
    # sound designs a learner or an agent may well choose
    "type aliases": "from typing import Any\nEntry = dict[str, Any]\nEntries = list[Entry]\n",
    "a lookup table that nothing changes": '_SIGN = {"C": 1, "D": -1}\nSIDES = {"D", "C"}\n_ORDER = ["a", "b"]\n',
    "a class constant table": 'class L:\n    SIGN = {"C": 1, "D": -1}\n    def sign(self, side):\n        return self.SIGN[side]\n',
    "a read-only view of a table": 'from types import MappingProxyType\nM = MappingProxyType({"C": 1, "D": -1})\n',
    "a key function": '_by_account = lambda entry: entry["account"]\n',
}


@pytest.mark.parametrize("source", STATE.values(), ids=STATE.keys())
def test_module_state_is_found(source):
    assert m07.module_state_problems(source)


@pytest.mark.parametrize("source", CLEAN.values(), ids=CLEAN.keys())
def test_code_without_module_state_is_accepted(source):
    assert m07.module_state_problems(source) == []


def test_the_original_ledger_is_full_of_module_state_and_the_reference_ledger_is_clean(started, done):
    assert len(m07.module_state_problems((started / LEDGER).read_text(encoding="utf-8"))) >= 2
    assert m07.module_state_problems((done / LEDGER).read_text(encoding="utf-8")) == []
    assert m07.legacy_functions_left((started / LEDGER).read_text(encoding="utf-8")) == ["accounts", "balance", "journal", "post_transfer", "reset"]
    assert m07.legacy_functions_left((done / LEDGER).read_text(encoding="utf-8")) == []


def test_the_v1_finder_is_import_aware(tmp_path):
    (tmp_path / "src" / "remit").mkdir(parents=True)
    (tmp_path / "tests").mkdir()
    (tmp_path / "src" / "remit" / "a.py").write_text(
        "from najmkit import ids, clock as najm_clock, audit\n"
        "import najmkit.clock as c2\n"
        "from najmkit.ids import new_id\n"
        "def f(self):\n"
        "    self.clock.now()\n"          # an injected clock object: fine
        "    najm_clock.now()\n"           # the module function: v1
        "    c2.get_clock()\n"             # v1 through another alias
        "    audit.emit('a.b')\n"          # v2: fine
        "    ids.make_id('TRF')\n"
        "def g(clock):\n"
        "    return clock.now()\n"
        "def h():\n"
        "    clock = FixedClock('2026-03-02T09:00:00+00:00')\n"   # a local variable called clock
        "    return clock.now()\n", encoding="utf-8")
    hits = m07.v1_calls_left(tmp_path)
    assert [h.split(" ", 1)[1] for h in hits] == ["from najmkit.ids import new_id", "najm_clock.now", "c2.get_clock"]


def test_tests_not_deleted_tolerates_renames_but_not_deletions(done):
    assert m07.tests_not_deleted(done) == []  # the reference migration renamed one test: a close name is a rename
    (done / "tests" / "test_money.py").unlink()
    gone = m07.tests_not_deleted(done)
    assert gone and all("test_money.py" in line for line in gone)
