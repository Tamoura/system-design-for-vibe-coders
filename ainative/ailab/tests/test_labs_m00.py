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

from ailab import checks_m00, framework, gitutil
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
    assert "rebase -i" not in "".join(c.hint for c in result.values())  # beginners do not get an interactive rebase


def test_the_reference_solution_passes_every_check(work):
    framework.solve_lab(framework.load_lab("m00"), work)
    assert_only(grade(work))


def test_an_alternative_correct_solution_by_hand_is_accepted(work, tmp_path):
    """Different route, different author, a message with a body: still correct."""
    empty_config = tmp_path / "empty.gitconfig"  # the learner's own git config must not matter
    empty_config.write_text("")
    path = work / NOTIFY
    path.write_text(path.read_text(encoding="utf-8").replace("recieved", "received"), encoding="utf-8")
    subprocess.run(["git", "add", NOTIFY], cwd=work, check=True)
    subprocess.run(
        ["git", "-c", "user.name=Lujain", "-c", "user.email=lujain@najm.example", "commit", "-q", "-m",
         "fix(notify): spell received correctly in the sent message", "-m", "Reported by a customer (REMIT-212).\n\nAI-assisted."],
        cwd=work, check=True, env={**__import__("os").environ, "GIT_CONFIG_GLOBAL": str(empty_config), "GIT_CONFIG_SYSTEM": str(empty_config)},
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
    assert "git commit" in result[ONE_COMMIT].hint
    assert "git commit" in result[CLEAN].hint


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
    learner_commit(work, "fix(notify): correct the spelling once more", allow_empty=True)
    result = grade(work)
    assert_only(result, ONE_COMMIT)
    assert "2 new commits" in result[ONE_COMMIT].detail
    assert "git reset --soft lab-start" in result[ONE_COMMIT].hint
    assert "rebase" not in result[ONE_COMMIT].hint


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
    result = grade(work)
    assert_only(result, SCOPE, TINY, CLEAN)
    assert "--amend" in result[CLEAN].hint and "second commit" in result[CLEAN].hint


# --------------------------------------------------------------------------------------------
# wrong fixes
# --------------------------------------------------------------------------------------------
def test_editing_the_test_instead_of_the_code(work):
    framework.edit_file(work, "tests/test_notify.py", "Ravi Kumar received 11,286.00 INR", "Ravi Kumar recieved 11,286.00 INR")
    framework.edit_file(work, "tests/test_config_cli.py", "Ravi Kumar received 11,286.00 INR", "Ravi Kumar recieved 11,286.00 INR")
    learner_commit(work, "fix(notify): match the current wording")
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
    assert_only(result, HIDDEN, TINY)
    # only the source-tree check fails (the customer-visible text is right), so the hint must not send the
    # learner to compare messages
    assert "test_the_misspelling_is_gone_from_the_whole_source_tree" in result[HIDDEN].detail
    assert "Compare your customers" not in result[HIDDEN].hint and "src/" in result[HIDDEN].hint
    assert "recieve" not in result[HIDDEN].hint


def test_rewriting_the_sentence_instead_of_fixing_the_word(work):
    framework.edit_file(work, NOTIFY, "{recipient} recieved {receive_amount}. ", "{recipient} got {receive_amount}. ")
    learner_commit(work, "fix(notify): simplify the wording")
    assert_only(grade(work), TESTS, HIDDEN, TINY)


def test_breaking_the_arabic_message_while_fixing_the_english(work):
    fix_typo(work)
    framework.edit_file(work, NOTIFY, "تم استلام مبلغ {receive_amount} من قبل {recipient}. ", "تم استلام مبلغ {receive_amount}. ")
    learner_commit(work, GOOD_MESSAGE)
    result = grade(work)
    assert {HIDDEN, TINY} <= failing(result)
    assert "Arabic" in result[HIDDEN].hint


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
    assert_only(result, SECRETS, TINY)  # the extra line is also "more than the one word"
    assert "9f8e7d6c" not in result[SECRETS].detail + result[SECRETS].hint


def test_doing_nothing_but_committing_nothing_changed(work):
    gitutil.commit_all(work, GOOD_MESSAGE, allow_empty=True, author=LEARNER)
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


# --------------------------------------------------------------------------------------------
# which branch is graded, merges, and the way back to one commit (findings of the learner dry-run)
# --------------------------------------------------------------------------------------------
TASK_BRANCH = "remit-212-typo"


def commit_on_task_branch(work: Path) -> None:
    gitutil.create_branch(work, TASK_BRANCH)
    fix_typo(work)
    learner_commit(work, GOOD_MESSAGE)


def test_a_fix_committed_on_a_task_branch_passes_while_that_branch_is_checked_out(work):
    commit_on_task_branch(work)
    assert_only(grade(work))


def test_grading_from_main_after_committing_on_the_task_branch_points_at_the_branch(work):
    """The commit exists, on another branch: the grader must say so instead of 'commit your change'."""
    commit_on_task_branch(work)
    gitutil.checkout(work, "main")
    result = grade(work)
    assert_only(result, TESTS, HIDDEN, SCOPE, TINY, ONE_COMMIT, MESSAGE)
    for name in (ONE_COMMIT, MESSAGE):
        assert TASK_BRANCH in result[name].detail
    for name, check in result.items():  # every failing line says the one useful thing, none says "make the change"
        if not check.ok:
            assert f"git switch {TASK_BRANCH}" in check.hint, name
            assert "Commit your" not in check.hint and "Make the change" not in check.hint, name


def test_uncommitted_work_on_main_while_a_branch_has_a_commit_keeps_the_ordinary_hints(work):
    commit_on_task_branch(work)
    gitutil.checkout(work, "main")
    fix_typo(work)  # real, unfinished work here: do not claim the answer is on the other branch
    result = grade(work)
    assert "git switch" not in result[TESTS].hint + result[SCOPE].hint + result[TINY].hint + result[CLEAN].hint


def test_fast_forwarding_the_task_branch_into_main_passes(work):
    commit_on_task_branch(work)
    gitutil.checkout(work, "main")
    gitutil.merge(work, TASK_BRANCH)
    assert_only(grade(work))


def test_a_merge_commit_is_not_a_second_commit(work):
    """`git merge --no-ff` into main is an ordinary way to integrate; the merge is not counted."""
    commit_on_task_branch(work)
    gitutil.checkout(work, "main")
    gitutil.merge(work, TASK_BRANCH, no_ff=True, author=LEARNER, date="2026-03-02T10:00:00+00:00")
    result = grade(work)
    assert_only(result)
    assert "merge commit is not counted" in result[ONE_COMMIT].detail


def test_a_fix_committed_straight_on_main_also_passes(work):
    """The branch name is a habit the lesson teaches, not something the grader checks."""
    fix_typo(work)
    learner_commit(work, GOOD_MESSAGE)
    assert gitutil.current_branch(work) == "main"
    assert_only(grade(work))


def test_amending_gets_back_to_one_commit_and_a_good_message(work):
    fix_typo(work)
    learner_commit(work, "fixed the typo")
    assert_only(grade(work), MESSAGE)
    gitutil.git(work, "commit", "-q", "--amend", "-m", GOOD_MESSAGE, env={"GIT_AUTHOR_NAME": "L", "GIT_AUTHOR_EMAIL": "l@x.example",
                                                                        "GIT_COMMITTER_NAME": "L", "GIT_COMMITTER_EMAIL": "l@x.example"})
    assert_only(grade(work))


def test_reset_soft_to_lab_start_is_the_documented_way_back_to_one_commit(work):
    fix_typo(work)
    learner_commit(work, GOOD_MESSAGE)
    framework.edit_file(work, NOTIFY, '"""Customer notifications', '"""Customer notifications (English and Arabic)')
    learner_commit(work, "docs(notify): say which languages")
    assert ONE_COMMIT in failing(grade(work))
    gitutil.git(work, "reset", "--soft", "lab-start")
    framework.edit_file(work, NOTIFY, '"""Customer notifications (English and Arabic)', '"""Customer notifications')
    learner_commit(work, GOOD_MESSAGE)
    assert_only(grade(work))


# --------------------------------------------------------------------------------------------
# the commit message: shape (CONTRIBUTING.md) and fit (this ticket)
# --------------------------------------------------------------------------------------------
HEADER_CASES = [
    ("feat(notify): correct the spelling of received", "the type is `fix`"),
    ("revert(notify): correct the spelling of received", "the type is `fix`"),
    ("fix(docs): correct the spelling of received", "not the module you changed"),
    ("fix(limits): correct the spelling of received", "not the module you changed"),
    ("fix(cli,notify): correct the spelling of received", "one lower-case word"),
    ("fix(cli notify): correct the spelling of received", "one lower-case word"),
    ("fix(Notify): correct the spelling of received", "one lower-case word"),
    ("Fix(notify): correct the spelling of received", "type must be lower case"),
    ("fix(notify):correct the spelling of received", "space after the colon"),
    ("fix(notify): x", "a few words"),
    ("fix(notify): typo", "a few words"),
    ("fix(notify): fixed the typo in the message", "imperative"),
    ("fix(notify): Corrected the spelling of received", "imperative"),
    ("fix(notify): correcting the spelling of received", "imperative"),
    ("fix(notify): correct the spelling of received:", "punctuation"),
    ("fix(notify): correct the spelling of received...", "full stop"),
    ("fix(notify): correct the spelling of received\u2026", "punctuation"),
    ("fix(notify): " + "correct the spelling of received " * 3, "limit is 72"),
    ("fix: correct the spelling of received", "no scope"),
    ("fixed the typo", "does not look like"),
]
SOUND_HEADERS = [
    "fix(notify): correct the spelling of received",
    "fix(notify): Correct the spelling of received",  # a capital letter is not a rule in CONTRIBUTING.md
    "fix(notify): spell received correctly in the sent message",
    "fix(notify): fix typo in sent message",
    "fix(notify): address the customer's spelling report",  # imperative verbs ending in -ss are fine
    "fix(notify): embed no typo in the sent message",  # so are the few that end in -ed ("embed", "need", "speed")
    'fix(notify): correct the spelling of "received" in transfer_sent',
]


@pytest.mark.parametrize("message, expected", HEADER_CASES, ids=[m[:40] for m, _ in HEADER_CASES])
def test_headers_with_the_wrong_type_scope_or_subject_get_a_specific_reason(message, expected):
    problems = checks_m00.header_problems(message.strip())
    assert problems and expected in " ".join(problems), problems


@pytest.mark.parametrize("message", SOUND_HEADERS)
def test_sound_headers_have_no_problems(message):
    assert checks_m00.header_problems(message) == []


@pytest.mark.parametrize(
    "message, expected",
    [HEADER_CASES[0], HEADER_CASES[4], HEADER_CASES[11], HEADER_CASES[14]],
    ids=["wrong-type", "two-scopes", "past-tense", "trailing-colon"],
)
def test_a_wrong_type_scope_or_subject_fails_only_the_message_check(work, message, expected):
    fix_typo(work)
    learner_commit(work, message.strip())
    result = grade(work)
    assert_only(result, MESSAGE)
    assert expected in result[MESSAGE].detail
    assert "CONTRIBUTING.md" in result[MESSAGE].hint and "--amend" in result[MESSAGE].hint


def test_a_capitalised_subject_and_a_task_specific_verb_are_accepted_end_to_end(work):
    fix_typo(work)
    learner_commit(work, "fix(notify): Spell received correctly in the sent message")
    assert_only(grade(work))


def test_a_73_character_header_is_rejected_and_72_is_not(work):
    fix_typo(work)
    ok = "fix(notify): " + "correct the spelling of received".ljust(59, "d")[:59]
    assert len(ok) == 72
    learner_commit(work, ok + "x")
    assert_only(grade(work), MESSAGE)
    gitutil.git(work, "commit", "-q", "--amend", "-m", ok,
                env={"GIT_AUTHOR_NAME": "L", "GIT_AUTHOR_EMAIL": "l@x.example",
                     "GIT_COMMITTER_NAME": "L", "GIT_COMMITTER_EMAIL": "l@x.example"})
    assert_only(grade(work))


def test_a_body_and_trailers_are_fine(work):
    fix_typo(work)
    learner_commit(work, GOOD_MESSAGE + "\n\nCustomers saw the wrong spelling in the 'transfer sent' text, reported in REMIT-212; this is a very long line that goes well past seventy-two characters in the body.\n\nAI-assisted.\nCo-Authored-By: Some Agent <agent@example.com>")
    assert_only(grade(work))


# --------------------------------------------------------------------------------------------
# "tiny" means one word: nothing else in the file may change
# --------------------------------------------------------------------------------------------
UNRELATED_EDITS = {
    "a customer-visible wording elsewhere in the file": (
        "We need to review it before it can go ahead. Please contact us.", "Under review."),
    "the Arabic name of a currency": ("روبية باكستانية", "روبية باكستان"),
    "an error message": ("unsupported language {lang!r}; expected one of {LANGUAGES}", "language {lang!r} is not supported"),
    "a docstring": ("Replace ASCII digits with Arabic-Indic digits when ``lang`` is Arabic.", "Swap the digits for Arabic ones."),
}


@pytest.mark.parametrize("old, new", UNRELATED_EDITS.values(), ids=list(UNRELATED_EDITS))
def test_fixing_the_word_and_also_editing_something_else_in_the_file(work, old, new):
    """Six changed lines or fewer used to pass; the file must now equal the starter with only the word fixed."""
    fix_typo(work)
    framework.edit_file(work, NOTIFY, old, new)
    learner_commit(work, GOOD_MESSAGE)
    result = grade(work)
    assert TINY in failing(result)
    assert "besides the misspelled word" in result[TINY].detail and "differs from the starter at line" in result[TINY].detail
    assert "recieve" not in result[TINY].detail + result[TINY].hint
    assert not framework.passed(list(result.values()))


def test_splitting_the_literal_and_repairing_it_when_rendered_is_not_a_fix(work):
    framework.edit_file(work, NOTIFY, "{recipient} recieved {receive_amount}. ", "{recipient} reci\" \"eved {receive_amount}. ")
    framework.edit_file(work, NOTIFY, "    return template.format(**shown)", '    return template.format(**shown).replace("reci" + "eved", "rece" + "ived")')
    learner_commit(work, GOOD_MESSAGE)
    result = grade(work)
    assert TINY in failing(result)


def test_invisible_whitespace_differences_do_not_count_as_extra_edits(work):
    """An editor that adds a final blank line or trims spaces must not turn a right answer into a wrong one."""
    path = work / NOTIFY
    text = path.read_text(encoding="utf-8").replace("recieved", "received")
    path.write_text(text.replace("\n\n", "\n \n", 1) + "\n\n", encoding="utf-8")
    learner_commit(work, GOOD_MESSAGE)
    assert_only(grade(work))


def test_windows_line_endings_on_the_changed_line_alone_are_not_extra_edits(work):
    path = work / NOTIFY
    text = path.read_text(encoding="utf-8").replace("recieved", "received")
    path.write_bytes(text.replace("received {receive_amount}. \"\n", "received {receive_amount}. \"\r\n").encode("utf-8"))
    learner_commit(work, GOOD_MESSAGE)
    assert_only(grade(work))


def test_a_regression_test_file_is_not_wanted_here(work):
    """CONTRIBUTING.md says new behaviour comes with a test; this ticket has none and says do not add tests."""
    fix_typo(work)
    (work / "tests" / "test_notify_spelling.py").write_text(
        "from remit.notify import render\n\n\ndef test_spelling():\n    assert 'received' in render('transfer_sent', 'en', name='A', transfer_id='T', recipient='R', "
        "send_amount=1, fee=1, receive_amount=1)\n", encoding="utf-8")
    learner_commit(work, GOOD_MESSAGE)
    result = grade(work)
    assert_only(result, UNEDITED, SCOPE, TINY)
    assert "do not add or edit tests" in result[UNEDITED].hint
    assert "tests/test_notify_spelling.py" in result[UNEDITED].detail


def test_the_hint_for_a_broken_arabic_message_is_about_the_arabic_message(work):
    fix_typo(work)
    framework.edit_file(work, NOTIFY, "المبلغ المرسل: {send_amount}، والرسوم: {fee}.", "المبلغ المرسل: {send_amount}.")
    learner_commit(work, GOOD_MESSAGE)
    result = grade(work)
    assert HIDDEN in failing(result)
    assert "Arabic message" in result[HIDDEN].hint and "Compare your customers" not in result[HIDDEN].hint


def test_nothing_changed_yet_gives_hints_that_fit(work):
    result = grade(work)
    assert "nothing has changed yet" in result[TINY].detail and "Fix the misspelled word" in result[TINY].hint
    assert "src/" in result[HIDDEN].hint  # the rule that the wrong spelling goes from comments and docstrings too
