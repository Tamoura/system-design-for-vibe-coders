"""Negative and alternative-solution tests for m00 (the exemplar lab).

Every test starts from the same started lab, makes the kind of change a learner or an agent really
makes, grades it, and says exactly which checks must pass and which must fail. The point of the file is
as much the *habit* as the cases: a grader is only trusted once it has been shown to reject wrong
answers for the right reason and to accept a right answer reached a different way.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from ailab import framework, gitutil
from conftest import LEARNER, learner_commit, start

ENV = "Your environment passes `ailab doctor`"
TESTS = "Your tests pass"
HIDDEN = "The message is right in English and Arabic"
UNEDITED = "The tests were not edited"
SCOPE = "Only the template file changed"
TINY = "The change is tiny"
ONE_COMMIT = "Exactly one new commit"
MESSAGE = "Commit messages follow CONTRIBUTING.md"
CLEAN = "The fix is committed (nothing left over)"
SECRETS = "No secrets in the change"
ALL = {ENV, TESTS, HIDDEN, UNEDITED, SCOPE, TINY, ONE_COMMIT, MESSAGE, CLEAN, SECRETS}

NOTIFY = "src/remit/notify.py"
GOOD_MESSAGE = 'fix(notify): correct the spelling of "received"'


@pytest.fixture(scope="module")
def template(tmp_path_factory) -> Path:
    return start("m00", tmp_path_factory.mktemp("m00-template") / "work")


@pytest.fixture
def work(template, tmp_path) -> Path:
    """A private copy of the started lab (the .git folder and the lab-start tag come with it)."""
    target = tmp_path / "work"
    shutil.copytree(template, target)
    return target


def grade(work: Path) -> dict[str, framework.Check]:
    checks = framework.grade_lab(framework.load_lab("m00"), work, catch=False)
    return {c.name: c for c in checks}


def fix_typo(work: Path) -> None:
    framework.edit_file(work, NOTIFY, "recieved", "received")


def failing(result: dict[str, framework.Check]) -> set[str]:
    return {name for name, check in result.items() if not check.ok}


def assert_only(result: dict[str, framework.Check], *expected_failures: str) -> None:
    got = failing(result)
    detail = "\n".join(f"  {'ok  ' if c.ok else 'FAIL'} {n}: {c.detail}" for n, c in result.items())
    assert got == set(expected_failures), f"expected failures {set(expected_failures)}, got {got}\n{detail}"


# --------------------------------------------------------------------------------------------
# the starter and the right answers
# --------------------------------------------------------------------------------------------
def test_the_starter_fails_for_the_right_reasons(work):
    result = grade(work)
    assert set(result) == ALL
    assert_only(result, TESTS, HIDDEN, SCOPE, TINY, ONE_COMMIT, MESSAGE)
    assert "test_transfer_sent_in_english" in result[TESTS].detail  # the learner is pointed at the failing test
    assert "recieved" not in "".join(c.detail + c.hint for c in result.values())  # never leaks the answer
    assert all(c.hint for c in result.values() if not c.ok)


def test_the_reference_solution_passes_every_check(work):
    framework.solve_lab(framework.load_lab("m00"), work)
    assert_only(grade(work))


def test_an_alternative_correct_solution_by_hand_is_accepted(work):
    """Different route, different author, a message with a body: still correct."""
    path = work / NOTIFY
    path.write_text(path.read_text(encoding="utf-8").replace("recieved", "received"), encoding="utf-8")
    subprocess.run(["git", "add", NOTIFY], cwd=work, check=True)
    subprocess.run(
        ["git", "-c", "user.name=Lujain", "-c", "user.email=lujain@najm.example", "commit", "-q", "-m",
         "fix(notify): spell received correctly in the sent message", "-m", "Reported by a customer (REMIT-212).\n\nAI-assisted."],
        cwd=work, check=True, env={**__import__("os").environ, "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null"},
    )
    assert_only(grade(work))


def test_tool_noise_does_not_count_against_the_learner(work):
    fix_typo(work)
    learner_commit(work, GOOD_MESSAGE)
    (work / ".claude").mkdir()
    (work / ".claude" / "settings.local.json").write_text("{}")
    (work / ".DS_Store").write_bytes(b"\0\0")
    (work / "src" / "remit" / "__pycache__").mkdir()
    (work / "src" / "remit" / "__pycache__" / "notify.cpython-311.pyc").write_bytes(b"\0")
    (work / ".pytest_cache").mkdir()
    (work / ".pytest_cache" / "README.md").write_text("cache")
    assert_only(grade(work))


# --------------------------------------------------------------------------------------------
# right fix, wrong hygiene
# --------------------------------------------------------------------------------------------
def test_a_fix_that_is_not_committed(work):
    fix_typo(work)
    result = grade(work)
    assert_only(result, ONE_COMMIT, MESSAGE, CLEAN)
    assert "git commit" in result[ONE_COMMIT].hint or "Commit" in result[ONE_COMMIT].hint


@pytest.mark.parametrize(
    "message",
    ["fixed the typo", "fix: correct the spelling", "Fix(notify): Correct the spelling", "fix(notify): correct the spelling."],
    ids=["no-convention", "no-scope", "wrong-case", "full-stop"],
)
def test_commit_messages_that_ignore_contributing_md(work, message):
    fix_typo(work)
    learner_commit(work, message)
    result = grade(work)
    assert_only(result, MESSAGE)
    assert message.split(":")[0] in result[MESSAGE].detail or message in result[MESSAGE].detail
    assert "CONTRIBUTING.md" in result[MESSAGE].hint


def test_two_commits_instead_of_one(work):
    fix_typo(work)
    learner_commit(work, GOOD_MESSAGE)
    framework.edit_file(work, NOTIFY, '"""Customer notifications', '"""Customer notifications (English and Arabic)')
    learner_commit(work, "docs(notify): say which languages")
    result = grade(work)
    assert_only(result, ONE_COMMIT)
    assert "2 new commits" in result[ONE_COMMIT].detail


def test_a_correct_fix_squashed_with_unrelated_work(work):
    fix_typo(work)
    (work / "README.md").write_text((work / "README.md").read_text() + "\nTODO: write more docs.\n")
    learner_commit(work, GOOD_MESSAGE)
    result = grade(work)
    assert_only(result, SCOPE, TINY)  # a second file is also "not tiny" (the ticket says one message, nothing else)
    assert "README.md" in result[SCOPE].detail


def test_an_oversized_change_to_the_right_file(work):
    fix_typo(work)
    path = work / NOTIFY
    path.write_text(path.read_text(encoding="utf-8") + "".join(f"# note {i}\n" for i in range(40)), encoding="utf-8")
    learner_commit(work, GOOD_MESSAGE)
    result = grade(work)
    assert_only(result, TINY)
    assert "limit 6 changed lines" in result[TINY].detail


def test_a_stray_new_file_next_to_the_fix(work):
    fix_typo(work)
    (work / "notes.txt").write_text("what I did\n")
    learner_commit(work, GOOD_MESSAGE)
    assert_only(grade(work), SCOPE, TINY)


def test_leaving_an_untracked_file_behind(work):
    fix_typo(work)
    learner_commit(work, GOOD_MESSAGE)
    (work / "scratch.py").write_text("print('debug')\n")
    assert_only(grade(work), SCOPE, TINY, CLEAN)


# --------------------------------------------------------------------------------------------
# wrong fixes
# --------------------------------------------------------------------------------------------
def test_editing_the_test_instead_of_the_code(work):
    framework.edit_file(work, "tests/test_notify.py", "Ravi Kumar received 11,286.00 INR", "Ravi Kumar recieved 11,286.00 INR")
    framework.edit_file(work, "tests/test_config_cli.py", "Ravi Kumar received 11,286.00 INR", "Ravi Kumar recieved 11,286.00 INR")
    learner_commit(work, "test(notify): match the current wording")
    result = grade(work)
    assert result[TESTS].ok  # the visible suite is green: that is exactly the trap
    assert_only(result, HIDDEN, UNEDITED, SCOPE, TINY)
    assert "tests/test_notify.py" in result[UNEDITED].detail


def test_patching_the_output_instead_of_the_template(work):
    """A 'fix' that makes the tests pass by rewriting the rendered text, leaving the typo in the source."""
    framework.edit_file(work, NOTIFY, "    return template.format(**shown)", '    return template.format(**shown).replace("recieved", "received")')
    learner_commit(work, "fix(notify): repair the rendered text")
    result = grade(work)
    assert result[TESTS].ok
    assert_only(result, HIDDEN)


def test_rewriting_the_sentence_instead_of_fixing_the_word(work):
    framework.edit_file(work, NOTIFY, "{recipient} recieved {receive_amount}. ", "{recipient} got {receive_amount}. ")
    learner_commit(work, "fix(notify): simplify the wording")
    assert_only(grade(work), TESTS, HIDDEN)


def test_breaking_the_arabic_message_while_fixing_the_english(work):
    fix_typo(work)
    framework.edit_file(work, NOTIFY, "تم استلام مبلغ {receive_amount} من قبل {recipient}. ", "تم استلام مبلغ {receive_amount}. ")
    learner_commit(work, GOOD_MESSAGE)
    result = grade(work)
    assert HIDDEN in failing(result)


def test_a_fix_that_breaks_the_code(work):
    framework.edit_file(work, NOTIFY, "recieved {receive_amount}", "received {receive_amount")
    learner_commit(work, GOOD_MESSAGE)
    result = grade(work)
    assert {TESTS, HIDDEN} <= failing(result)


def test_hard_coding_a_credential_next_to_the_fix(work):
    fix_typo(work)
    framework.edit_file(work, NOTIFY, "ARABIC_INDIC_DIGITS =", 'GATEWAY_KEY = "sk-live-' + "9f8e7d6c5b4a3f2e1d0c" + '"\nARABIC_INDIC_DIGITS =')
    learner_commit(work, GOOD_MESSAGE)
    result = grade(work)
    assert_only(result, SECRETS)
    assert "9f8e7d6c" not in result[SECRETS].detail + result[SECRETS].hint


def test_doing_nothing_but_committing_nothing_changed(work):
    gitutil.commit_all(work, "chore(notify): nothing", allow_empty=True, author=LEARNER)
    result = grade(work)
    assert_only(result, TESTS, HIDDEN, SCOPE, TINY)


def test_an_endless_loop_in_the_code_cannot_hang_the_grader(work):
    fix_typo(work)
    framework.edit_file(work, NOTIFY, "def render(template_id: str, lang: str, **values: Any) -> str:",
                        "def render(template_id: str, lang: str, **values: Any) -> str:\n    while True:\n        pass")
    learner_commit(work, GOOD_MESSAGE)
    from ailab import checks

    # run the two pytest-based checks with short timeouts, as the grader does with long ones
    assert not checks.tests_pass(work, timeout=3).ok
    assert not checks.hidden_tests_pass(work, framework.load_lab("m00").hidden_dir, timeout=3).ok
