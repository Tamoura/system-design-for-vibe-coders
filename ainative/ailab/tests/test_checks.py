"""Tests for the reusable grader helpers in ailab/checks.py.

Most use a started m00 lab as the learner's repository (it is a real Remit copy with a git history).
"""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from ailab import checks, framework, gitutil
from conftest import learner_commit, start, tree_digest


@pytest.fixture
def work(tmp_path):
    """m00 as started: the typo is in place, two tests fail."""
    return start("m00", tmp_path / "work")


@pytest.fixture
def fixed(work):
    """m00 with the typo fixed but not committed (all visible tests pass)."""
    framework.edit_file(work, "src/remit/notify.py", "recieved", "received")
    return work


# =============================================================================
# pytest runners
# =============================================================================
def test_run_pytest_reports_failures_by_name(work):
    result = checks.run_pytest(work)
    assert not result.ok and result.passed == 97 and result.failed == 2 and result.errors == 0
    assert sorted(result.failure_names) == ["test_customer_send_and_history_share_a_database_file", "test_transfer_sent_in_english"]
    assert result.summary() == "97 passed, 2 failed" and result.total == 99


def test_run_pytest_passes_once_fixed_and_leaves_the_work_alone(fixed):
    before = tree_digest(fixed)
    status = gitutil.status_porcelain(fixed, ignore=())
    result = checks.run_pytest(fixed)
    assert result.ok and result.passed == 99 and result.failures == []
    assert tree_digest(fixed) == before and gitutil.status_porcelain(fixed, ignore=()) == status  # no caches, no pyc


def test_run_pytest_on_selected_paths(fixed):
    result = checks.run_pytest(fixed, ["tests/test_money.py"])
    assert result.ok and 10 < result.passed < 30


def test_run_pytest_uses_the_work_directorys_own_code(fixed):
    """PYTHONPATH is the copy's src: a change in the learner's code is what the tests see."""
    framework.edit_file(fixed, "src/remit/fees.py", "STD_A = FeeSchedule(\n    id=\"STD-A\"", "STD_A = FeeSchedule(\n    id=\"STD-A \"")
    assert not checks.run_pytest(fixed).ok


def test_a_timeout_stops_the_run(fixed):
    (fixed / "tests" / "test_slow.py").write_text("import time\n\ndef test_slow():\n    time.sleep(30)\n")
    result = checks.run_pytest(fixed, ["tests/test_slow.py"], timeout=2)
    assert result.timed_out and not result.ok and result.duration < 15
    assert "did not finish" in result.summary()


def test_collection_errors_and_missing_tests_are_failures_not_crashes(fixed):
    (fixed / "tests" / "test_broken.py").write_text("def test_x(:\n")
    broken = checks.run_pytest(fixed, ["tests/test_broken.py"])
    assert not broken.ok and broken.errors == 1
    nothing = checks.run_pytest(fixed, ["tests/nothing_here"])
    assert not nothing.ok and nothing.total == 0
    assert "no tests ran" in nothing.summary()


def test_the_learners_environment_does_not_leak_into_the_run(fixed, monkeypatch):
    monkeypatch.setenv("REMIT_DB", "/definitely/not/writable.db")
    monkeypatch.setenv("NAJMKIT_AUDIT_LOG", "/definitely/not/writable.jsonl")
    monkeypatch.setenv("PYTEST_ADDOPTS", "-x --maxfail=1 -k nothing_matches")
    assert checks.run_pytest(fixed).ok


def test_tests_pass_check_names_the_failing_tests(work):
    check = checks.tests_pass(work)
    assert not check.ok and "97 passed, 2 failed" in check.detail and "test_transfer_sent_in_english" in check.detail
    assert "pytest -q" in check.hint
    assert checks.tests_pass(work, name="Custom", required=False).required is False


HIDDEN = '''
def test_service_still_sends(service):
    result = service.send("C001", __import__("remit.money", fromlist=["Money"]).Money("500", "QAR"), "INR", "Ravi Kumar")
    assert result.transfer.fee.amount == 12

def test_failing_on_purpose():
    assert 1 == 2, "SECRET-EXPECTED-VALUE"
'''


def test_hidden_tests_run_against_a_copy_with_the_projects_fixtures(fixed, tmp_path):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    (hidden / "test_hidden_demo.py").write_text(HIDDEN)
    before = tree_digest(fixed)
    result = checks.run_hidden_pytest(fixed, hidden)
    assert (result.passed, result.failed) == (1, 1) and result.failure_names == ["test_failing_on_purpose"]
    assert tree_digest(fixed) == before  # the hidden file was never put into the learner's directory
    assert not (fixed / "tests" / "_hidden").exists()


def test_hidden_check_never_reveals_assertion_text(fixed, tmp_path):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    (hidden / "test_hidden_demo.py").write_text(HIDDEN)
    shown = checks.hidden_tests_pass(fixed, hidden)
    assert not shown.ok and "1 of 2 hidden checks failed: test_failing_on_purpose" in shown.detail
    assert "SECRET-EXPECTED-VALUE" not in shown.detail + shown.hint
    counted = checks.hidden_tests_pass(fixed, hidden, reveal="count")
    assert counted.detail == "1 of 2 hidden checks failed"
    (hidden / "test_hidden_demo.py").write_text(HIDDEN.split("def test_failing")[0])
    assert checks.hidden_tests_pass(fixed, hidden).ok


def test_hidden_tests_accept_a_single_file_and_report_collection_trouble(fixed, tmp_path):
    single = tmp_path / "test_hidden_one.py"
    single.write_text("def test_ok():\n    assert True\n")
    assert checks.run_hidden_pytest(fixed, single).ok
    single.write_text("import module_that_is_not_there\n")
    check = checks.hidden_tests_pass(fixed, [single])
    assert not check.ok and "could not run" in check.detail or "failed" in check.detail


# =============================================================================
# git-based checks
# =============================================================================
def test_files_changed_within(work):
    check = checks.files_changed_within(work, ["src/remit/notify.py"])
    assert not check.ok and "no files have changed" in check.detail
    framework.edit_file(work, "src/remit/notify.py", "recieved", "received")
    assert checks.files_changed_within(work, ["src/remit/notify.py"]).ok
    (work / "README.md").write_text("changed\n")
    outside = checks.files_changed_within(work, ["src/remit/*.py"])
    assert not outside.ok and "README.md" in outside.detail and outside.hint
    assert checks.files_changed_within(work, ["src/**", "*.md"]).ok
    assert checks.files_changed_within(checks_work := work, [], require_change=False, ignore=("**",)).ok
    assert checks_work is work


def test_files_changed_within_sees_committed_changes_too(fixed):
    learner_commit(fixed, "fix(notify): x")
    assert checks.files_changed_within(fixed, ["src/remit/notify.py"]).ok


def test_files_unchanged(fixed):
    assert checks.files_unchanged(fixed, ["tests/**"]).ok
    (fixed / "tests" / "test_money.py").write_text("# weakened\n")
    (fixed / "tests" / "test_new.py").write_text("def test_n():\n    pass\n")
    check = checks.files_unchanged(fixed, ["tests/**"])
    assert not check.ok and "tests/test_money.py" in check.detail and "tests/test_new.py" in check.detail


def test_diff_size(work):
    assert not checks.diff_size(work, max_lines=6, min_lines=1).ok  # nothing yet
    assert checks.diff_size(work, max_lines=6).ok  # zero is within "at most"
    framework.edit_file(work, "src/remit/notify.py", "recieved", "received")
    assert checks.diff_size(work, max_lines=2, max_files=1, min_lines=1).ok
    assert checks.diff_size(work, max_lines=2).detail == "1 file, +1 -1 lines"
    (work / "extra.txt").write_text("a\nb\nc\n")
    too_big = checks.diff_size(work, max_lines=4)
    assert not too_big.ok and "limit 4 changed lines" in too_big.detail and too_big.hint
    too_many = checks.diff_size(work, max_lines=50, max_files=1)
    assert not too_many.ok and "limit 1 file" in too_many.detail


def test_commit_count(fixed):
    assert not checks.commit_count(fixed, exactly=1).ok
    learner_commit(fixed, "fix(notify): a")
    assert checks.commit_count(fixed, exactly=1).ok
    assert checks.commit_count(fixed, at_least=1, at_most=3).ok
    (fixed / "x.txt").write_text("x\n")
    learner_commit(fixed, "chore(x): b")
    two = checks.commit_count(fixed, exactly=1)
    assert not two.ok and "2 new commits" in two.detail and "Squash" in two.hint
    assert checks.commit_count(fixed, at_most=1).ok is False and checks.commit_count(fixed, at_least=2).ok
    assert "exactly 1" in checks.commit_count(fixed, exactly=1).name


def test_all_committed(fixed):
    check = checks.all_committed(fixed)
    assert not check.ok and "src/remit/notify.py" in check.detail
    learner_commit(fixed, "fix(notify): a")
    assert checks.all_committed(fixed).ok
    (fixed / ".claude").mkdir()
    (fixed / ".claude" / "settings.local.json").write_text("{}")
    assert checks.all_committed(fixed).ok  # tool noise is not the learner's work
    (fixed / "left-over.txt").write_text("x")
    assert not checks.all_committed(fixed).ok


@pytest.mark.parametrize(
    "header, problem",
    [
        ("fix(notify): correct the spelling of received", None),
        ("feat(fees)!: charge fees on the receive side", None),
        ("test(limits): cover the exact boundary", None),
        ("refactor(ledger,service): split posting", "does not look like"),  # one scope only
        ("fix: correct the spelling", "no scope"),
        ("fixed the typo", "does not look like"),
        ("Fix(notify): correct the spelling", "does not look like"),
        ("fix(Notify): correct the spelling", "does not look like"),
        ("fix(notify):correct the spelling", "does not look like"),
        ("fix(notify): ", "does not look like"),
        ("fix(notify): correct the spelling.", "full stop"),
        ("bugfix(notify): correct the spelling", "not one of"),
        ("fix(notify): " + "x" * 70, "limit is 72"),
        ("", "does not look like"),
    ],
)
def test_commit_header_rules(header, problem):
    problems = checks.commit_header_problems(header)
    if problem is None:
        assert problems == []
    else:
        assert problems and problem in problems[0], problems


def test_scope_can_be_made_optional():
    assert checks.commit_header_problems("fix: correct the spelling", require_scope=False) == []


def test_conventional_commits_check(fixed):
    none_yet = checks.conventional_commits(fixed)
    assert not none_yet.ok and "expected at least 1" in none_yet.detail
    learner_commit(fixed, "fixed the typo")
    bad = checks.conventional_commits(fixed)
    assert not bad.ok and '"fixed the typo"' in bad.detail and "CONTRIBUTING.md" in bad.hint
    (fixed / "x.txt").write_text("x\n")
    learner_commit(fixed, "chore(x): add x")
    assert not checks.conventional_commits(fixed).ok  # one bad commit among the good is still bad
    assert checks.conventional_commits(fixed, since="HEAD~1").ok  # only the last commit counts from there


def test_merge_commits_are_not_judged_by_conventional_commits(repo_with_merge):
    assert checks.conventional_commits(repo_with_merge).ok


@pytest.fixture
def repo_with_merge(fixed):
    gitutil.create_branch(fixed, "feature")
    (fixed / "f.txt").write_text("f\n")
    learner_commit(fixed, "feat(f): add f")
    gitutil.checkout(fixed, "main")
    (fixed / "m.txt").write_text("m\n")
    learner_commit(fixed, "feat(m): add m")
    gitutil.merge(fixed, "feature", message="Merge branch 'feature'", no_ff=True)
    return fixed


# =============================================================================
# secrets
# =============================================================================
def fake(*parts: str) -> str:
    """Assemble a fake key from pieces so that this test file itself holds no key-like string."""
    return "".join(parts)


KEYS = {
    "AWS access key id": fake("AKIA", "QWERTYUIOPASDFGH"),
    "private key block": fake("-----BEGIN RSA ", "PRIVATE KEY-----"),
    "GitHub token": fake("ghp_", "a1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6q7R8"),
    "Slack token": fake("xoxb-", "123456789012-abcdefghijkl"),
    "API key (sk-...)": fake("sk-", "live-9f8e7d6c5b4a3f2e1d0c"),
    "payment key (sk_live_...)": fake("sk_live_", "4eC39HqLyjWDarjtT1zdp7dc"),
    "Google API key": fake("AIza", "SyA1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6q"),
    "bearer token": fake("Authorization: Bearer ", "eyJhbGciOiJIUzI1NiJ9abcdef123456"),
    "hard-coded credential": fake('API_', 'KEY = "', 'h7Gd92kLmQ03xZpW"'),
}


@pytest.mark.parametrize("rule", sorted(KEYS))
def test_find_secrets_recognises_each_kind(rule):
    found = checks.find_secrets(f"line one\nvalue = {KEYS[rule]}\n") if rule != "hard-coded credential" else \
        checks.find_secrets(f"line one\n{KEYS[rule]}\n")
    assert (rule, 2) in found, found


def test_find_secrets_ignores_placeholders_and_environment_lookups():
    clean = [
        'password = "changeme"',
        'API_KEY = os.environ["REMIT_API_KEY"]',
        'api_key = "your-key-here-please"',
        "token: ${GITHUB_TOKEN_VALUE_HERE}",
        'secret = "<put the secret here>"',
        "REMIT_API_KEY=",
        'password = "xxxxxxxxxxxxxxxx"',
        "AKIAIOSFODNN7EXAMPLE",
        "the word password and api key in a sentence",
        'TOKEN_URL = "https://auth.najmbank.qa/oauth/token"',
        'token_expiry = "2026-03-02T09:00:00+00:00"',
        'secret_name = "remit-signing-secret-name"',
    ]
    for line in clean:
        assert checks.find_secrets(line) == [], line


def test_no_secrets_looks_at_what_was_added(fixed):
    assert checks.no_secrets(fixed).ok
    (fixed / "src" / "remit" / "settings.py").write_text(f'KEY = "{KEYS["API key (sk-...)"]}"\n')
    check = checks.no_secrets(fixed)
    assert not check.ok and "API key (sk-...) in src/remit/settings.py" in check.detail
    assert KEYS["API key (sk-...)"] not in check.detail + check.hint  # never echoes the secret
    assert "environment variable" in check.hint
    learner_commit(fixed, "feat(x): add settings")
    assert not checks.no_secrets(fixed).ok  # committed does not make it go away


def test_no_secrets_scans_modified_lines_and_commit_messages(fixed):
    framework.edit_file(fixed, "src/remit/config.py", "ENVIRONMENTS = (", f'API_TOKEN = "{fake("Zq8rT5uV2wX9yA3b")}"\nENVIRONMENTS = (')
    assert not checks.no_secrets(fixed).ok
    framework.edit_file(fixed, "src/remit/config.py", f'API_TOKEN = "{fake("Zq8rT5uV2wX9yA3b")}"\n', "")
    assert checks.no_secrets(fixed).ok
    learner_commit(fixed, f"fix(x): use {KEYS['GitHub token']}")
    assert "message of commit" in checks.no_secrets(fixed).detail


def test_no_secrets_scan_all_includes_files_the_learner_did_not_touch(fixed):
    assert checks.no_secrets(fixed, scan="all").ok  # the pristine base is clean
    (fixed / "docs" / "notes.md").write_text(f"token {KEYS['Slack token']}\n")
    assert checks.no_secrets(fixed, scan="added").ok is False
    assert "docs/notes.md:1" in checks.no_secrets(fixed, scan="all").detail


# =============================================================================
# mutation checking
# =============================================================================
CAP_MUTANT = checks.Mutant("M-cap", "src/remit/fees.py", "min(max(raw, minimum), cap)", "max(raw, minimum)", "the fee cap")
MESSAGE_MUTANT = checks.Mutant("M-msg", "src/remit/fees.py", "amount must be greater than zero", "x", "an error message")
STALE_MUTANT = checks.Mutant("M-gone", "src/remit/fees.py", "this text is not in the file", "y", "something removed")


def test_mutants_killed_by_existing_tests(fixed):
    before = tree_digest(fixed)
    report = checks.mutants_killed(fixed, [CAP_MUTANT, MESSAGE_MUTANT, STALE_MUTANT], ["tests/test_fees.py"])
    assert report.baseline_ok
    assert [m.id for m in report.killed] == ["M-cap"]  # the cap is tested
    assert [m.id for m in report.survived] == ["M-msg"]  # the wording of an error is not
    assert [m.id for m in report.not_applied] == ["M-gone"]
    assert report.total == 3
    assert tree_digest(fixed) == before  # mutants were applied to a copy and nothing leaked back


def test_plain_tuples_are_accepted_and_numbered(fixed):
    report = checks.mutants_killed(fixed, [("src/remit/fees.py", "min(max(raw, minimum), cap)", "max(raw, minimum)")],
                                   ["tests/test_fees.py"])
    assert [m.id for m in report.killed] == ["M1"]


def test_default_test_files_are_the_ones_the_learner_added(fixed):
    assert checks.new_test_files(fixed) == []
    report = checks.mutants_killed(fixed, [CAP_MUTANT])
    assert not report.baseline_ok and "no test files" in report.baseline_summary
    (fixed / "tests" / "test_my_fee.py").write_text(textwrap.dedent('''
        from remit.corridors import get_corridor
        from remit.fees import quote_fee
        from remit.money import Money

        def test_big_amounts_are_capped():
            assert quote_fee(Money("20000", "QAR"), get_corridor("QAR", "INR")) == Money("150", "QAR")
    '''))
    assert checks.new_test_files(fixed) == ["tests/test_my_fee.py"]
    report = checks.mutants_killed(fixed, [CAP_MUTANT])
    assert report.baseline_ok and [m.id for m in report.killed] == ["M-cap"]


def test_a_test_that_asserts_nothing_kills_nothing(fixed):
    (fixed / "tests" / "test_nothing.py").write_text(textwrap.dedent('''
        from remit.corridors import get_corridor
        from remit.fees import quote_fee
        from remit.money import Money

        def test_runs_without_crashing():
            quote_fee(Money("20000", "QAR"), get_corridor("QAR", "INR"))
    '''))
    report = checks.mutants_killed(fixed, [CAP_MUTANT])
    assert report.baseline_ok and [m.id for m in report.survived] == ["M-cap"]


def test_if_the_learners_tests_fail_no_mutant_is_tried(work):
    report = checks.mutants_killed(work, [CAP_MUTANT], ["tests/test_notify.py"])  # m00 starter: a failing test
    assert not report.baseline_ok and "failed" in report.baseline_summary
    assert report.killed == report.survived == []


def test_a_mutant_that_hangs_counts_as_killed(fixed):
    hang = checks.Mutant("M-hang", "src/remit/fees.py", "min(max(raw, minimum), cap)", "(lambda: [__import__('time').sleep(60)])() or cap")
    report = checks.mutants_killed(fixed, [hang], ["tests/test_fees.py"], timeout=3)
    assert [m.id for m in report.killed] == ["M-hang"]


def test_mutation_check_wraps_the_report(fixed):
    check = checks.mutation_check(fixed, [CAP_MUTANT, MESSAGE_MUTANT], ["tests/test_fees.py"], min_killed=1)
    assert check.ok and check.detail == "your tests catch 1 of 2 deliberate defects"
    strict = checks.mutation_check(fixed, [CAP_MUTANT, MESSAGE_MUTANT], ["tests/test_fees.py"])
    assert not strict.ok and "they miss: an error message" in strict.detail and strict.hint
    broken = checks.mutation_check(fixed, [CAP_MUTANT], ["tests/does_not_exist.py"])
    assert not broken.ok and "do not pass" in broken.detail


# =============================================================================
# JSON helpers
# =============================================================================
SCHEMA = {
    "type": "object",
    "required": ["cases"],
    "additionalProperties": False,
    "properties": {
        "cases": {
            "type": "array",
            "minItems": 2,
            "items": {
                "type": "object",
                "required": ["mode", "turn"],
                "properties": {
                    "mode": {"enum": ["context-rot", "runaway-loop"]},
                    "turn": {"type": "integer", "minimum": 1, "maximum": 20},
                    "note": {"type": "string", "minLength": 5, "maxLength": 40, "pattern": r"^[a-z]"},
                },
            },
        }
    },
}


def test_validate_accepts_good_data_and_explains_bad_data():
    good = {"cases": [{"mode": "context-rot", "turn": 4}, {"mode": "runaway-loop", "turn": 20, "note": "all right"}]}
    assert checks.validate(good, SCHEMA) == []
    bad = {"cases": [{"mode": "sycophancy", "turn": 0}], "extra": 1}
    errors = checks.validate(bad, SCHEMA)
    assert any("unexpected 'extra'" in e for e in errors)
    assert any("$.cases: needs at least 2 items" in e for e in errors)
    assert any("$.cases[0].mode: must be one of" in e for e in errors)
    assert any("$.cases[0].turn: must be at least 1" in e for e in errors)
    assert checks.validate({}, SCHEMA) == ["$: missing 'cases'"]
    assert checks.validate([], SCHEMA) == ["$: expected object, got list"]


def test_validate_types_are_strict_about_bool_and_numbers():
    assert checks.validate(True, {"type": "integer"}) and not checks.validate(3, {"type": ["integer", "null"]})
    assert not checks.validate(None, {"type": ["integer", "null"]}) and not checks.validate(2.5, {"type": "number"})
    assert checks.validate("ab", {"type": "string", "minLength": 3}) and checks.validate("Ab", {"type": "string", "pattern": "^[a-z]"})
    assert checks.validate("x" * 5, {"maxLength": 3}) and checks.validate(5, {"const": 6})


def test_json_has_and_get_path():
    data = {"a": {"b": [{"c": "x"}, {"c": 7}]}, "empty": "", "flag": True}
    assert checks.get_path(data, "a.b[1].c") == 7 and checks.get_path(data, "a.b[5].c", "dflt") == "dflt"
    assert checks.json_has(data, "a.b[0].c", equals="x") and not checks.json_has(data, "a.b[0].c", equals="y")
    assert checks.json_has(data, "a.b[1].c", type_=int) and not checks.json_has(data, "flag", type_=int)
    assert checks.json_has(data, "a.b[0].c", one_of=["x", "z"]) and not checks.json_has(data, "a.b[0].c", one_of=["q"])
    assert not checks.json_has(data, "empty", non_empty=True) and checks.json_has(data, "a", non_empty=True)
    assert not checks.json_has(data, "nope") and checks.json_has(data, "flag", equals=False) is False
    assert checks.json_has({"x": None}, "x") and checks.json_has({"x": 0}, "x", equals=0)


def test_json_check_reports_missing_invalid_and_wrong_files(tmp_path):
    path = tmp_path / "diagnosis.json"
    check = checks.json_check(tmp_path, "diagnosis.json", SCHEMA)
    assert not check.ok and "does not exist" in check.detail
    path.write_text("{not json")
    assert "not valid JSON" in checks.json_check(tmp_path, "diagnosis.json", SCHEMA).detail
    path.write_text(json.dumps({"cases": []}))
    wrong = checks.json_check(tmp_path, "diagnosis.json", SCHEMA, name="Diagnosis file", hint="see the task")
    assert not wrong.ok and wrong.name == "Diagnosis file" and "at least 2 items" in wrong.detail and wrong.hint == "see the task"
    path.write_text(json.dumps({"cases": [{"mode": "context-rot", "turn": 1}] * 2}))
    assert checks.json_check(tmp_path, "diagnosis.json", SCHEMA).ok
    data, error = checks.load_json(path)
    assert error is None and data["cases"][0]["turn"] == 1


# =============================================================================
# Markdown helpers
# =============================================================================
DOC = textwrap.dedent('''
    # Review of agent/loyalty-discount

    Intro line.

    ## Findings

    ```bash
    # this is a comment inside a code fence, not a heading
    ## nor is this
    ```

    The discount uses float arithmetic in `fees.py` which breaks the money rule.

    ### Finding 2: `Swallowed Exception`
    The handler returns None.

    ## Findings
    Second findings section.

    ## Verdict ##
    Do not merge until the tests are real and the float is gone.
''')


def test_markdown_outline_ignores_headings_inside_code_fences():
    outline = checks.markdown_outline(DOC)
    assert [(s.level, s.title) for s in outline] == [
        (1, "Review of agent/loyalty-discount"), (2, "Findings"), (3, "Finding 2: `Swallowed Exception`"),
        (2, "Findings"), (2, "Verdict"),
    ]
    assert "comment inside a code fence" in outline[1].body and "float arithmetic" in outline[1].body


def test_markdown_sections_normalises_titles_and_numbers_repeats(tmp_path):
    path = tmp_path / "review.md"
    path.write_text(DOC)
    sections = checks.markdown_sections(path)
    assert list(sections) == ["review of agent/loyalty-discount", "findings", "finding 2: swallowed exception", "findings #2", "verdict"]
    assert sections["verdict"].startswith("Do not merge") and sections["findings #2"] == "Second findings section."


def test_sections_check(tmp_path):
    (tmp_path / "review.md").write_text(DOC)
    assert checks.sections_check(tmp_path, "review.md", ["Findings", "verdict"]).ok
    check = checks.sections_check(tmp_path, "review.md", ["Findings", "Root cause", "Summary"], min_words=3)
    assert not check.ok and "missing: Root cause, Summary" in check.detail
    thin = checks.sections_check(tmp_path, "review.md", ["Finding 2"], min_words=10)
    assert not thin.ok and "too short: Finding 2" in thin.detail
    assert "does not exist" in checks.sections_check(tmp_path, "nope.md", ["x"]).detail


# =============================================================================
# small file checks and copying
# =============================================================================
def test_files_exist_and_python_compiles(fixed):
    assert checks.files_exist(fixed, ["README.md", "src/remit/money.py"]).ok
    missing = checks.files_exist(fixed, ["README.md", "specs/T1.md", "specs/T2.md"])
    assert not missing.ok and "specs/T1.md, specs/T2.md" in missing.detail
    assert checks.python_compiles(fixed).ok
    (fixed / "src" / "remit" / "oops.py").write_text("def broken(:\n")
    bad = checks.python_compiles(fixed)
    assert not bad.ok and "oops.py" in bad.detail
    assert not list(fixed.rglob("__pycache__"))  # compiling wrote nothing
    assert not checks.python_compiles(fixed, ["nowhere"]).ok


def test_copy_work_skips_git_and_caches(fixed):
    (fixed / "__pycache__").mkdir()
    (fixed / "__pycache__" / "x.pyc").write_text("x")
    (fixed / ".venv").mkdir()
    (fixed / ".venv" / "big").write_text("x")
    with checks.work_copy(fixed) as copy:
        names = {p.name for p in copy.iterdir()}
        assert "src" in names and "tests" in names
        assert ".git" not in names and "__pycache__" not in names and ".venv" not in names
        kept = copy
    assert not kept.exists()  # removed on exit


# =============================================================================
# "fails on the starter", forbidden patterns, the static API lister
# =============================================================================
REGRESSION_TEST = textwrap.dedent('''
    from remit.notify import render
    from remit.money import Money

    def test_english_receipt_is_spelled_right():
        text = render("transfer_sent", "en", name="A", transfer_id="T", recipient="R",
                      send_amount=Money("1", "QAR"), fee=Money("1", "QAR"), receive_amount=Money("1", "INR"))
        assert "received" in text
''')


def test_tests_fail_on_starter_distinguishes_a_real_regression_test_from_a_useless_one(fixed):
    check = checks.tests_fail_on_starter(fixed)
    assert not check.ok and "no new or changed test files" in check.detail
    (fixed / "tests" / "test_receipt.py").write_text(REGRESSION_TEST)
    good = checks.tests_fail_on_starter(fixed)
    assert good.ok and "1 test fail on the original code" in good.detail
    assert checks.tests_pass(fixed, ["tests/test_receipt.py"]).ok  # and it passes on the fix
    (fixed / "tests" / "test_useless.py").write_text("def test_nothing():\n    assert True\n")
    useless = checks.tests_fail_on_starter(fixed, ["tests/test_useless.py"])
    assert not useless.ok and "already pass" in useless.detail and useless.hint


def test_tests_fail_on_starter_puts_the_original_files_back_before_running(fixed):
    (fixed / "src" / "remit" / "helper_added.py").write_text("X = 1\n")
    (fixed / "src" / "remit" / "limits.py").unlink()
    (fixed / "tests" / "test_uses_limits.py").write_text(
        "from remit import limits\n\ndef test_limits_exist():\n    assert limits.LIMITS\n")
    assert checks.tests_pass(fixed, ["tests/test_uses_limits.py"]).ok is False  # limits.py is gone in the learner's tree
    ok = checks.tests_fail_on_starter(fixed, ["tests/test_uses_limits.py"])
    assert not ok.ok  # on the starter limits.py is back, so the test passes there: not a regression test


def test_forbid_patterns_only_looks_at_added_lines_and_chosen_files(fixed):
    patterns = {"float arithmetic": r"\bfloat\s*\(", "bare except": r"except\s*:"}
    assert checks.forbid_patterns(fixed, patterns).ok
    (fixed / "src" / "remit" / "bad.py").write_text("total = float(1)\ntry:\n    pass\nexcept:\n    pass\n")
    (fixed / "docs" / "notes.md").write_text("float(1) is bad\n")
    check = checks.forbid_patterns(fixed, patterns)
    assert not check.ok and check.detail == "float arithmetic in src/remit/bad.py, bare except in src/remit/bad.py"
    assert checks.forbid_patterns(fixed, patterns, globs=["docs/**"]).ok is False
    assert checks.forbid_patterns(fixed, {"x": "zzz-not-there"}).ok
    # a pre-existing match in the repository is not the learner's doing
    assert checks.forbid_patterns(fixed, {"decimal import": r"from decimal import"}, globs=["src/remit/money.py"]).ok


def test_public_api_lists_functions_classes_and_methods_without_importing(tmp_path):
    (tmp_path / "src" / "pkg").mkdir(parents=True)
    (tmp_path / "src" / "pkg" / "__init__.py").write_text("def top(a: int) -> int: ...\n")
    (tmp_path / "src" / "pkg" / "mod.py").write_text(textwrap.dedent('''
        import this_module_does_not_exist_and_is_never_imported

        def new_id(prefix: str, *, n: int = 1) -> str: ...
        def _private(): ...

        class Thing:
            def __init__(self, x): ...
            def method(self, a, b=2): ...
            def _hidden(self): ...
            @classmethod
            def make(cls, kind: str) -> "Thing": ...
        class _Hidden: ...
    '''))
    api = checks.public_api(tmp_path)
    assert api == {
        "pkg.top": "(a: int) -> int",
        "pkg.mod.new_id": "(prefix: str, *, n: int=1) -> str",
        "pkg.mod.Thing": "class",
        "pkg.mod.Thing.method": "(a, b=2)",
        "pkg.mod.Thing.make": "(kind: str) -> 'Thing'",
    }


def test_public_api_of_the_real_najmkit(fixed):
    api = checks.public_api(fixed)
    assert api["najmkit.ids.new_id"] == "(prefix: str) -> str"
    assert api["najmkit.clock.FixedClock.advance"] == "(**delta: int) -> datetime"
    assert "najmkit.audit.log_event" in api and "remit.service.RemitService.send" in api


def test_git_branch_helpers(fixed):
    gitutil.create_branch(fixed, "feature/a")
    (fixed / "a.txt").write_text("a\n")
    learner_commit(fixed, "feat(a): add a")
    gitutil.checkout(fixed, "main")
    gitutil.create_branch(fixed, "feature/b")
    (fixed / "b.txt").write_text("b\n")
    learner_commit(fixed, "feat(b): add b")
    gitutil.checkout(fixed, "main")
    assert gitutil.merged_branches(fixed) == []
    gitutil.merge(fixed, "feature/a")
    assert gitutil.merged_branches(fixed) == ["feature/a"]
    assert gitutil.is_ancestor(fixed, "feature/a", "main") and not gitutil.is_ancestor(fixed, "feature/b", "main")
    assert gitutil.show_bytes(fixed, "lab-start", "README.md").startswith(b"# Najm Remit")
    assert gitutil.show_bytes(fixed, "lab-start", "a.txt") is None


def test_the_recipe_in_kit_notes_for_running_learner_scripts_works(fixed, tmp_path):
    """KIT_NOTES 6.1: a copy, a scrubbed environment with a stub first on PATH, stdin, a timeout."""
    import os
    import sys

    from ailab import runner

    stub_dir = tmp_path / "stubs"
    stub_dir.mkdir()
    stub = stub_dir / "claude"
    stub.write_text("#!/bin/sh\necho stub-claude-ran\n")
    stub.chmod(0o755)
    (fixed / "triage.py").write_text(
        "import subprocess, sys, remit\n"
        "print(sys.stdin.read().upper(), subprocess.run(['claude'], capture_output=True, text=True).stdout.strip())\n"
    )
    with checks.work_copy(fixed) as root:
        env = runner.clean_env(pythonpath=[root / "src"], extra={"PATH": f"{stub_dir}{os.pathsep}{os.environ['PATH']}"})
        result = runner.run([sys.executable, "triage.py"], cwd=root, env=env, timeout=20, input="hello")
        slow = runner.run([sys.executable, "-c", "import time; time.sleep(30)"], cwd=root, env=env, timeout=1)
    assert result.ok and result.stdout.strip() == "HELLO stub-claude-ran"
    assert slow.timed_out
