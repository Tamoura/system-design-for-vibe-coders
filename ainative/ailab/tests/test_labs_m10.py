"""Negative and alternative-solution tests for m10 ("Split a change across branches and integrate it").

The grader looks at a *result*: a merged main, the branches that were merged, the history. So every test
here builds a history the way a learner (or a team of agents) really would, grades it, and says exactly
which checks must fail and which must still pass:

* the reference route, and other sound routes (worktrees, rebase and fast-forward, another merge order,
  merged branches deleted afterwards, tests added to old files);
* the typical wrong routes: everything on main, squashed branches, a conflict committed unresolved, one side
  of the conflict dropped, "keep both sides" without fixing the shared ``return 0``, the Qatar day computed
  in UTC, a corridors command that creates a database, a hard-coded ``describe``, unrelated files, a weakened
  test, mixed commits, bad commit messages, secrets.
"""
from __future__ import annotations

import importlib
import re
import shutil
from pathlib import Path

import pytest

from ailab import checks, framework, gitutil, runner
from conftest import LEARNER, learner_commit, start

framework.load_lab("m10")  # make sure the lab module is importable
LAB = importlib.import_module("ailab.labs.m10_parallel.lab")
SOL = LAB.HERE / "solution"

ON_MAIN = "You finished on main"
COMMITTED = "Everything is committed"
OWN_TESTS = "Your own tests pass"
TASK_A = "Task A: the delay notice works"
TASK_B = "Task B: the corridors command works"
TASK_C = "Task C: the limits command works"
TASK_D = "Task D: the runbook is there"
TOGETHER = "The pieces work together after the merge"
MARKERS = "No conflict markers are left in the code"
BRANCHES = "At least 3 branches were merged into main"
ONE_TASK = "Each commit is about one task"
MESSAGES = "Commit messages follow CONTRIBUTING.md"
SCOPE = "Only the expected files changed"
WEAKENED = "Existing tests were not weakened"
SECRETS = "No secrets in the change"
NEW_TESTS = "Your new tests fail on the original code"
PLAN = "A plan was committed first (docs/parallel-plan.md)"
LOG = "A short log exists (docs/agent-log.md)"
HISTORY = "No commit in the history contains conflict markers"
REQUIRED = {ON_MAIN, COMMITTED, OWN_TESTS, TASK_A, TASK_B, TASK_C, TASK_D, TOGETHER, MARKERS, BRANCHES, ONE_TASK, MESSAGES,
            SCOPE, WEAKENED, SECRETS}
ADVISORY = {NEW_TESTS, PLAN, LOG, HISTORY}
CLI = "src/remit/cli.py"


# --------------------------------------------------------------------------------------------
# fixtures and helpers
# --------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def template(tmp_path_factory) -> Path:
    return start("m10", tmp_path_factory.mktemp("m10-template") / "work")


@pytest.fixture
def work(template, tmp_path) -> Path:
    target = tmp_path / "work"
    shutil.copytree(template, target)
    return target


def grade(work: Path) -> dict[str, framework.Check]:
    return {c.name: c for c in framework.grade_lab(framework.load_lab("m10"), work, catch=False)}


def failing(result: dict[str, framework.Check]) -> set[str]:
    return {name for name, check in result.items() if not check.ok}


def assert_failing(result: dict[str, framework.Check], *expected: str) -> None:
    got = failing(result)
    detail = "\n".join(f"  {'ok  ' if c.ok else 'FAIL'} {n}: {c.detail}" for n, c in result.items())
    assert got == set(expected), f"expected failures {set(expected)}, got {got}\n{detail}"


def assert_required_pass(result: dict[str, framework.Check]) -> None:
    bad = {n for n, c in result.items() if c.required and not c.ok}
    detail = "\n".join(f"  {'ok  ' if c.ok else 'FAIL'} {n}: {c.detail}" for n, c in result.items())
    assert not bad, f"required checks failed: {bad}\n{detail}"


def git(work: Path, *args: str, check: bool = True):
    return gitutil.git(work, *args, check=check)


def patches(names: list[str]) -> list[tuple[str, str]]:
    """The reference patches (by file name) paired with the reference commit messages."""
    messages = {p: m for _, steps in LAB.FIRST_WAVE + LAB.SECOND_WAVE for p, m in steps}
    return [(n, messages[n]) for n in names]


PART = {  # branch name -> the reference steps
    "a": ("feat/delay-notice", patches(["a1_template.patch", "a2_tests.patch"])),
    "b": ("feat/corridors-command", patches(["b1_describe.patch", "b2_command.patch", "b3_tests.patch"])),
    "c": ("feat/limits-command", patches(["c1_usage_line.patch", "c2_command.patch", "c3_tests.patch"])),
    "d": ("docs/care-runbook", patches(["d1_runbook.patch"])),
}


def build_branch(work: Path, key: str, *, steps=None, branch: str | None = None) -> str:
    """Cut a branch from main, apply the part's patches as commits, and return to main."""
    name, reference = PART[key]
    name = branch or name
    gitutil.checkout(work, "main")
    gitutil.create_branch(work, name)
    for patch, message in steps or reference:
        gitutil.apply_patch(work, SOL / patch)
        learner_commit(work, message)
    gitutil.checkout(work, "main")
    return name


def merge(work: Path, branch: str, *, resolve: str = "reference") -> bool:
    """``git merge --no-ff``; on a conflict resolve it as asked. Returns True when there was a conflict.

    resolve: "reference" (the stored union), "markers" (commit the markers), "ours", "naive" (delete the marker
    lines and keep both sides' lines, which loses a shared ``return 0``).
    """
    result = gitutil.merge(work, branch, no_ff=True, message=f"Merge branch '{branch}'", author=LEARNER, check=False)
    if result.ok:
        return False
    conflicted = git(work, "diff", "--name-only", "--diff-filter=U").stdout.split()
    assert conflicted == [CLI], conflicted  # the planted conflict, and only that one
    if resolve == "reference":
        framework.write_file(work, CLI, (SOL / "cli_resolved.txt").read_text(encoding="utf-8"))
    elif resolve == "ours":
        git(work, "checkout", "--ours", "--", CLI)
    elif resolve == "naive":
        text = (work / CLI).read_text(encoding="utf-8")
        kept = [line for line in text.splitlines(keepends=True) if not re.match(r"(<{7}|={7}|>{7})( |$)", line)]
        framework.write_file(work, CLI, "".join(kept))
    elif resolve != "markers":
        raise AssertionError(resolve)
    learner_commit(work, f"Merge branch '{branch}'")
    return True


def reference_flow(work: Path, *, parts: str = "abcd", resolve: str = "reference") -> None:
    """Plan, build ``parts`` on their own branches (cut from the same main), merge them in order."""
    for key in parts.replace("d", ""):
        build_branch(work, key)
    for key in parts.replace("d", ""):
        merge(work, PART[key][0], resolve=resolve)
    if "d" in parts:
        build_branch(work, "d")
        merge(work, PART["d"][0])


def write_plan(work: Path) -> None:
    framework.write_file(work, LAB.PLAN, (SOL / "parallel-plan.md").read_text(encoding="utf-8"))
    learner_commit(work, "docs(docs): plan the parallel work for REMIT-361")


def write_log(work: Path) -> None:
    framework.write_file(work, LAB.LOG, (SOL / "agent-log.md").read_text(encoding="utf-8"))
    learner_commit(work, "docs(docs): log what was delegated")


def run_remit(work: Path, *argv: str, env: dict[str, str] | None = None) -> runner.RunResult:
    return runner.run_python(["-m", "remit", *argv], cwd=work, pythonpath=[work / "src"], timeout=30, extra_env=env)


# --------------------------------------------------------------------------------------------
# the starter, the reference route, and the seed
# --------------------------------------------------------------------------------------------
def test_the_starter_fails_for_the_right_reasons(work):
    result = grade(work)
    assert set(result) == REQUIRED | ADVISORY
    assert_failing(result, TASK_A, TASK_B, TASK_C, TASK_D, TOGETHER, BRANCHES, ONE_TASK, MESSAGES, SCOPE, NEW_TESTS, PLAN, LOG)
    assert all(c.hint for c in result.values() if not c.ok)
    assert "transfer_delayed" not in "".join(c.detail + c.hint for c in result.values())  # never leaks the answer
    assert "Nothing is committed yet" in result[MESSAGES].hint  # no branch holds work either, so "merge" would be wrong


def test_the_reference_solution_passes_every_check_even_the_advisory_ones(work):
    framework.solve_lab(framework.load_lab("m10"), work)
    assert_failing(grade(work))


def test_the_seed_adds_exactly_two_marker_comments_and_nothing_else(template):
    diff = gitutil.out(template, "diff", "lab-start~1", "lab-start", "--numstat", "--", "src", "tests", "pyproject.toml").split()
    assert diff == ["2", "0", CLI]
    text = (template / CLI).read_text(encoding="utf-8")
    assert text.count("REMIT-361") == 2 and LAB.PARSER_MARKER in text and LAB.RUN_MARKER in text


def test_the_markers_really_do_make_two_branches_collide_and_only_there(work):
    build_branch(work, "b")
    build_branch(work, "c")
    assert merge(work, PART["b"][0]) is False
    assert merge(work, PART["c"][0]) is True  # asserts inside: the conflict is in cli.py and nowhere else
    assert LAB.conflict_marker_files(work) == []


def test_the_tickets_examples_are_what_the_program_really_prints(work):
    framework.solve_lab(framework.load_lab("m10"), work)
    task = "\n".join(line.strip() for line in (LAB.HERE / "task.md").read_text(encoding="utf-8").splitlines())  # the examples are indented blocks
    lines = run_remit(work, "corridors", "QAR-INR", env={"REMIT_DB": str(work / "x.db")}).stdout.splitlines()
    assert lines[0] in task
    script = (
        "from datetime import datetime, timezone\n"
        "from decimal import Decimal\n"
        "from remit.limits import usage_line\n"
        "from remit.models import Transfer\n"
        "from remit.money import Money\n"
        "def t(a, w): return Transfer('T','C','QAR-INR',Money(a,'QAR'),Money('5','QAR'),Money('1','INR'),Decimal(1),'R','bank_deposit',datetime.fromisoformat(w))\n"
        "now = datetime(2026,3,2,9,tzinfo=timezone.utc)\n"
        "print(usage_line('T2',[t('3000','2026-03-02T05:00:00+00:00'),t('9000','2026-03-01T10:00:00+00:00')],now))\n"
        "from remit.notify import render\n"
        "print(render('transfer_delayed','en',name='{name}',transfer_id='{transfer_id}',recipient='{recipient}'))\n"
        "print(render('transfer_delayed','ar',name='{name}',transfer_id='{transfer_id}',recipient='{recipient}'))\n"
    )
    out = runner.run_python(["-c", script], cwd=work, pythonpath=[work / "src"]).stdout.splitlines()
    assert out[0] in task
    assert f"en: {out[1]}" in task and f"ar: {out[2]}" in task
    assert "C001  Aisha Rahman\nT2: today 500.00 of 10000.00 QAR used (9500.00 left); this month 500.00 of 40000.00 QAR used (39500.00 left)" in task


# --------------------------------------------------------------------------------------------
# other sound routes: all required checks must pass
# --------------------------------------------------------------------------------------------
def test_worktrees_a_different_implementation_rebase_and_fast_forward(work, tmp_path):
    """Three worktrees beside the repo, usage_line written another way, rebase then fast-forward: no merge commits."""
    write_plan(work)  # plan first, on main, before any branch is cut
    trees = {}
    for key, name in (("a", "task/notice"), ("b", "task/corridors"), ("c", "task/limits")):
        trees[key] = tmp_path / f"wt-{key}"
        git(work, "worktree", "add", "-q", "-b", name, str(trees[key]), "main")
    for key in "abc":
        _, steps = PART[key]
        for patch, message in steps:
            gitutil.apply_patch(trees[key], SOL / patch)
            if patch == "c1_usage_line.patch":  # the same behaviour, written from the windows instead of check_limits
                framework.edit_file(trees[key], "src/remit/limits.py",
                                    '    result = check_limits(tier, history, Money("0.01", "QAR"), now)\n',
                                    "    day_start, day_end = day_window(now)\n"
                                    "    month_start, month_end = month_window(now)\n"
                                    "    items = list(history)\n"
                                    '    zero = Money.zero("QAR")\n'
                                    "    daily = sum((i.send_amount for i in items if day_start <= i.created_at < day_end), zero)\n"
                                    "    monthly = sum((i.send_amount for i in items if month_start <= i.created_at < month_end), zero)\n"
                                    "    limits = limits_for(tier)\n"
                                    "    result = LimitResult(True, None, tier, daily, limits.daily, monthly, limits.monthly)\n")
            learner_commit(trees[key], message)
    # integrate with rebase + fast-forward, in a different order from the reference: C, then B, then A
    for key in "cba":
        name = {"a": "task/notice", "b": "task/corridors", "c": "task/limits"}[key]
        rebased = git(trees[key], "rebase", "main", check=False)
        if not rebased.ok:
            assert git(trees[key], "diff", "--name-only", "--diff-filter=U").stdout.split() == [CLI]
            ordered = (SOL / "cli_resolved.txt").read_text(encoding="utf-8")
            framework.write_file(trees[key], CLI, ordered)
            git(trees[key], "add", "-A")
            git(trees[key], "-c", "core.editor=true", "rebase", "--continue")
        git(work, "merge", "-q", "--ff-only", name)
    for tree in trees.values():
        git(work, "worktree", "remove", "--force", str(tree))
    build_branch(work, "d")
    git(work, "merge", "-q", "--ff-only", PART["d"][0])
    write_log(work)
    result = grade(work)
    assert_failing(result)
    assert [c for c in gitutil.commits_since(work, "lab-start") if c.is_merge] == []  # a linear history
    assert "3" in result[BRANCHES].detail or "4" in result[BRANCHES].detail


def test_merging_in_another_order_and_deleting_the_branches_afterwards(work):
    for key in "abc":
        build_branch(work, key)
    for key in "cba":
        merge(work, PART[key][0])
    build_branch(work, "d")
    merge(work, PART["d"][0])
    for key in "abcd":
        git(work, "branch", "-D", PART[key][0])  # the merge commits still say what was merged
    assert git(work, "branch", "--format=%(refname:short)").stdout.split() == ["main"]
    result = grade(work)
    assert_required_pass(result)
    assert result[BRANCHES].detail.startswith("4 merged")


def test_tests_added_to_the_old_test_files_instead_of_new_ones_are_fine(work):
    framework.solve_lab(framework.load_lab("m10"), work)
    path = work / "tests" / "test_notify.py"
    path.write_text(path.read_text(encoding="utf-8") + "\n\ndef test_delay_notice_is_defined():\n    from remit.notify import TEMPLATES\n    assert 'transfer_delayed' in TEMPLATES\n",
                    encoding="utf-8")
    learner_commit(work, "test(notify): check the template is registered")
    assert_failing(grade(work))


def test_agent_and_editor_leftovers_do_not_count_against_the_learner(work):
    framework.solve_lab(framework.load_lab("m10"), work)
    (work / ".claude").mkdir(exist_ok=True)
    (work / ".claude" / "settings.local.json").write_text("{}")
    git(work, "worktree", "add", "-q", "-b", "scratch/agent", str(work / ".claude" / "worktrees" / "agent-1"), "main")
    (work / ".DS_Store").write_bytes(b"\0")
    (work / "src" / "remit" / "__pycache__").mkdir(exist_ok=True)
    (work / "src" / "remit" / "__pycache__" / "cli.cpython-311.pyc").write_bytes(b"\0")
    result = grade(work)
    assert_failing(result)


def test_three_branches_are_enough_and_the_runbook_can_be_skipped_only_with_a_failing_check(work):
    reference_flow(work, parts="abc")
    result = grade(work)
    assert_failing(result, TASK_D, PLAN, LOG)  # 3 merged branches pass; the missing runbook is reported
    assert result[BRANCHES].ok


# --------------------------------------------------------------------------------------------
# wrong routes
# --------------------------------------------------------------------------------------------
def test_everything_in_one_commit_on_main(work):
    reference_flow(work)
    tip = gitutil.head(work)
    git(work, "checkout", "-q", "-B", "main", "lab-start")  # start again from the beginning...
    git(work, "checkout", tip, "--", ".")  # ...and commit the whole result at once
    for key in "abcd":
        git(work, "branch", "-D", PART[key][0])
    learner_commit(work, "feat(cli): customer care pack")
    result = grade(work)
    assert_failing(result, BRANCHES, ONE_TASK, MESSAGES, PLAN, LOG)
    assert "expected at least 4" in result[MESSAGES].detail
    assert "changes files of different tasks" in result[ONE_TASK].detail
    assert "notify.py (A)" in result[ONE_TASK].detail or "corridors.py (B)" in result[ONE_TASK].detail


def test_squash_merged_branches_leave_no_trace_of_the_branches(work):
    for key in "abc":
        build_branch(work, key)
    for key in "abc":
        name = PART[key][0]
        squashed = git(work, "merge", "--squash", name, check=False)
        if not squashed.ok:
            framework.write_file(work, CLI, (SOL / "cli_resolved.txt").read_text(encoding="utf-8"))
        learner_commit(work, {"a": "feat(notify): add the delay notice", "b": "feat(corridors): add the corridors command",
                              "c": "feat(limits): add the limits command"}[key])
    build_branch(work, "d")
    git(work, "merge", "--squash", PART["d"][0])
    learner_commit(work, "docs(docs): add the runbook")
    result = grade(work)
    assert_failing(result, BRANCHES, PLAN, LOG)  # the code is right, but git cannot see which branches were merged
    assert "not --squash" in result[BRANCHES].hint


def test_a_conflict_committed_with_its_markers(work):
    reference_flow(work, parts="abc", resolve="markers")
    result = grade(work)
    assert {MARKERS, OWN_TESTS, TASK_B, TASK_C, TOGETHER, HISTORY} <= failing(result)
    assert TASK_A not in failing(result) and result[BRANCHES].ok
    assert "cli.py" in result[MARKERS].detail
    assert "======" not in result[MARKERS].hint.replace("=======", "")  # the hint explains, it does not print markers


def test_one_side_of_the_conflict_is_dropped(work):
    reference_flow(work, parts="abcd", resolve="ours")  # the limits command is thrown away
    result = grade(work)
    failed = failing(result)
    assert {TASK_C, TOGETHER, OWN_TESTS} <= failed
    assert TASK_B not in failed and TASK_A not in failed and MARKERS not in failed


def test_keep_both_sides_without_fixing_the_shared_return(work):
    """The textual conflict is resolved, the program is not: `corridors` now falls into the transfer code."""
    reference_flow(work, parts="abcd", resolve="naive")
    result = grade(work)
    failed = failing(result)
    assert TOGETHER in failed and TASK_B in failed and OWN_TESTS in failed
    assert TASK_C not in failed and MARKERS not in failed
    assert "test_a_new_command_never_falls_through_into_the_transfer_code" in result[TOGETHER].detail


def _edit_on_main(work: Path, rel: str, old: str, new: str, message: str) -> None:
    framework.edit_file(work, rel, old, new)
    learner_commit(work, message)


def test_the_day_and_month_computed_in_utc(work):
    """The classic: 'today' is the UTC date of the timestamps, so the hour between 21:00 and 24:00 UTC lands on the wrong day."""
    reference_flow(work)
    path = work / "src" / "remit" / "limits.py"
    text = path.read_text(encoding="utf-8")
    head, tail = text.index("def usage_line("), text.index("def check_limits(")
    body = (
        "def usage_line(tier: str, history: Iterable[HistoryItem], now: datetime) -> str:\n"
        "    limits = limits_for(tier)\n"
        "    items = list(history)\n"
        '    today = sum((i.send_amount for i in items if i.created_at.date() == now.date()), Money.zero("QAR"))\n'
        '    month = sum((i.send_amount for i in items if (i.created_at.year, i.created_at.month) == (now.year, now.month)), Money.zero("QAR"))\n'
        "    return (\n"
        '        f"{tier}: today {today.amount:.2f} of {limits.daily.amount:.2f} QAR used "\n'
        '        f"({max(limits.daily - today, Money.zero(\'QAR\')).amount:.2f} left); "\n'
        '        f"this month {month.amount:.2f} of {limits.monthly.amount:.2f} QAR used "\n'
        '        f"({max(limits.monthly - month, Money.zero(\'QAR\')).amount:.2f} left)"\n'
        "    )\n\n\n"
    )
    path.write_text(text[:head] + body + text[tail:], encoding="utf-8")
    learner_commit(work, "fix(limits): add up today's transfers by date")
    result = grade(work)
    failed = failing(result)
    assert TASK_C in failed and TOGETHER not in failed and TASK_B not in failed
    assert "after_midnight_in_qatar" in result[TASK_C].detail or "turns_over_at_midnight" in result[TASK_C].detail


def test_a_corridors_command_that_creates_a_database_file(work):
    reference_flow(work)
    _edit_on_main(work, CLI, '("quote", "corridors")', '("quote",)', "fix(cli): open the database for every command")
    result = grade(work)
    assert TASK_B in failing(result) and "no_database_file" in result[TASK_B].detail
    assert TASK_C not in failing(result)


def test_describe_hard_coded_for_the_four_shipped_corridors(work):
    """Special-casing the example: the answers are typed in instead of computed."""
    reference_flow(work)
    path = work / "src" / "remit" / "corridors.py"
    text = path.read_text(encoding="utf-8")
    lines = {
        "QAR-EGP": "QAR-EGP: 100.00 to 15000.00 QAR; delivery: bank_deposit (default), wallet; fees: STD-B",
        "QAR-INR": "QAR-INR: 50.00 to 25000.00 QAR; delivery: bank_deposit (default), wallet; fees: STD-A",
        "QAR-PHP": "QAR-PHP: 50.00 to 20000.00 QAR; delivery: bank_deposit (default), cash_pickup, wallet; fees: STD-A",
        "QAR-PKR": "QAR-PKR: 100.00 to 15000.00 QAR; delivery: bank_deposit (default), cash_pickup; fees: STD-B",
    }
    head, tail = text.index("def describe("), text.index("def validate_send(")
    path.write_text(text[:head] + f"def describe(corridor: Corridor) -> str:\n    return {lines!r}[corridor.code]\n\n\n" + text[tail:],
                    encoding="utf-8")
    learner_commit(work, "fix(corridors): make describe fast")
    result = grade(work)
    assert TASK_B in failing(result)
    assert "test_describe_works_for_any_corridor_not_only_the_shipped_ones" in result[TASK_B].detail


def test_an_unrelated_file_changed_on_the_way(work):
    reference_flow(work)
    _edit_on_main(work, "src/remit/fees.py", "def _D(value: str) -> Decimal:", "def _D(value: str) -> Decimal:  # parse a number", "refactor(fees): comment the helper")
    result = grade(work)
    assert_failing(result, SCOPE, PLAN, LOG)
    assert "src/remit/fees.py" in result[SCOPE].detail


def test_an_existing_test_was_weakened_to_get_a_green_run(work):
    reference_flow(work)
    _edit_on_main(work, "tests/test_fees.py", "def test_a_higher_amount_never_costs_less", "def test_a_higher_amount_never_costs_less_x", "test(fees): rename a test")
    result = grade(work)
    assert WEAKENED in failing(result)
    assert "tests/test_fees.py" in result[WEAKENED].detail


def test_an_existing_test_file_deleted(work):
    reference_flow(work)
    git(work, "rm", "-q", "tests/test_fx.py")
    learner_commit(work, "test(fx): drop a slow test file")
    assert "tests/test_fx.py was deleted" in grade(work)[WEAKENED].detail


def test_one_commit_that_mixes_two_tasks(work):
    reference_flow(work)
    framework.edit_file(work, "src/remit/notify.py", '"""Customer notifications', '"""Customer notifications (English and Arabic)')
    framework.edit_file(work, "src/remit/limits.py", '"""Sending limits by KYC tier.', '"""Sending limits by KYC tier (QAR).')
    learner_commit(work, "docs(docs): tidy two docstrings")
    result = grade(work)
    assert ONE_TASK in failing(result)
    assert "limits.py (C)" in result[ONE_TASK].detail and "notify.py (A)" in result[ONE_TASK].detail


@pytest.mark.parametrize("message", ["wip", "update stuff", "feat: add things", "Feat(cli): Add The Command.", "fix(cli): " + "x" * 70])
def test_commit_messages_that_ignore_contributing_md(work, message):
    reference_flow(work)
    framework.write_file(work, "docs/notes.md", "notes\n")
    learner_commit(work, message)
    result = grade(work)
    assert MESSAGES in failing(result)
    assert "CONTRIBUTING.md" in result[MESSAGES].hint


def test_two_branches_are_not_enough(work):
    for key in "ab":
        build_branch(work, key)
    for key in "ab":
        merge(work, PART[key][0])
    result = grade(work)
    assert BRANCHES in failing(result) and result[BRANCHES].detail.startswith("2 merged")


def test_a_branch_that_carries_no_work_does_not_count(work):
    for key in "ab":
        build_branch(work, key)
    for key in "ab":
        merge(work, PART[key][0])
    git(work, "branch", "backup")  # sits on main's own tip... and a branch on the starting commit:
    git(work, "branch", "empty", "lab-start")
    result = grade(work)
    assert BRANCHES in failing(result)  # "backup" is the same commit as b's merge only if ff; here it is a distinct tip
    assert "empty" not in result[BRANCHES].detail


def test_finishing_on_a_feature_branch(work):
    reference_flow(work)
    git(work, "switch", "-q", PART["c"][0])
    result = grade(work)
    assert ON_MAIN in failing(result) and "feat/limits-command" in result[ON_MAIN].detail
    assert "git switch main" in result[ON_MAIN].hint


def test_uncommitted_work_left_behind(work):
    reference_flow(work)
    (work / "notes.txt").write_text("todo\n")
    result = grade(work)
    assert COMMITTED in failing(result) and SCOPE in failing(result)


def test_a_secret_pasted_into_a_test(work):
    reference_flow(work)
    path = work / "tests" / "test_care_limits.py"
    path.write_text(path.read_text(encoding="utf-8") + '\nGATEWAY_KEY = "sk-live-' + "9f8e7d6c5b4a3f2e1d0c" + '"\n', encoding="utf-8")
    learner_commit(work, "test(limits): add a gateway key")
    result = grade(work)
    assert SECRETS in failing(result)
    assert "9f8e7d6c" not in result[SECRETS].detail + result[SECRETS].hint


def test_a_runbook_with_typed_examples_instead_of_real_output(work):
    reference_flow(work)
    path = work / "docs" / "CARE.md"
    path.write_text(path.read_text(encoding="utf-8").replace("fees: STD-A", "fees: STD-X"), encoding="utf-8")
    learner_commit(work, "docs(docs): retype the example")
    assert TASK_D in failing(grade(work))


def test_an_endless_loop_cannot_hang_the_grader(work):
    reference_flow(work)
    framework.edit_file(work, "src/remit/corridors.py", "def describe(corridor: Corridor) -> str:",
                        "def describe(corridor: Corridor) -> str:\n    while True:\n        pass")
    learner_commit(work, "fix(corridors): retry forever")
    assert not checks.tests_pass(work, timeout=3).ok
    assert not checks.run_hidden_pytest(work, LAB.HERE / "hidden", timeout=3, args=["--continue-on-collection-errors"]).ok


def test_a_broken_cli_fails_only_the_tasks_that_need_it(work):
    reference_flow(work)
    framework.edit_file(work, CLI, "from __future__ import annotations\n", "from __future__ import annotations\nthis is not python\n")
    learner_commit(work, "fix(cli): break the module")
    result = grade(work)
    failed = failing(result)
    assert {TASK_B, TASK_C, TOGETHER, OWN_TESTS} <= failed
    assert TASK_A not in failed and TASK_D not in failed  # the report points at the broken part


def test_a_renamed_main_is_reported_not_a_crash(work):
    reference_flow(work)
    git(work, "branch", "-m", "main", "master")
    result = grade(work)  # catch=False: a grader exception would fail this test
    assert ON_MAIN in failing(result) and BRANCHES in failing(result)
    assert "no branch called main" in result[BRANCHES].detail


def test_grading_is_repeatable_on_a_busy_history(work):
    reference_flow(work)
    first = {n: (c.ok, c.detail, c.hint) for n, c in grade(work).items()}
    second = {n: (c.ok, c.detail, c.hint) for n, c in grade(work).items()}
    assert first == second


def test_the_marker_scan_ignores_prose_about_conflicts(work):
    reference_flow(work)
    framework.write_file(work, "docs/agent-log.md", "# Log\n\nThe conflict looked like this:\n\n```\n<<<<<<< HEAD\nx\n=======\ny\n>>>>>>> branch\n```\n" + "word " * 40)
    learner_commit(work, "docs(docs): describe the conflict I met")
    assert MARKERS not in failing(grade(work))  # docs/agent-log.md is not scanned: only code and the runbook are


# --------------------------------------------------------------------------------------------
# the dry-run repairs: what a sound solution may do, and the shortcuts that must still fail
# --------------------------------------------------------------------------------------------
CARE = "docs/CARE.md"
PKR_LINE = "QAR-PKR: 100.00 to 15000.00 QAR; delivery: bank_deposit (default), cash_pickup; fees: STD-B"
INR_LINE = "QAR-INR: 50.00 to 25000.00 QAR; delivery: bank_deposit (default), wallet; fees: STD-A"


def solved(work: Path) -> Path:
    framework.solve_lab(framework.load_lab("m10"), work)
    return work


def edit_runbook(work: Path, *pairs: tuple[str, str]) -> str:
    text = (work / CARE).read_text(encoding="utf-8")
    for old, new in pairs:
        assert old in text, old
        text = text.replace(old, new)
    framework.write_file(work, CARE, text)
    learner_commit(work, "docs(docs): rework the runbook")
    return text


def test_a_runbook_that_shows_another_real_corridor_line_is_fine(work):
    """The ticket asks for 'a real example of its output': QAR-PKR is as real as QAR-INR."""
    solved(work)
    edit_runbook(work, ("python -m remit corridors            # every corridor, ordered by code\n", ""),
                 ("python -m remit corridors QAR-PKR    # one corridor", "python -m remit corridors QAR-PKR"),
                 (INR_LINE, PKR_LINE))
    assert_failing(grade(work))


def test_the_whole_corridor_list_pasted_from_the_program_is_fine(work):
    solved(work)
    everything = "\n".join([
        "QAR-EGP: 100.00 to 15000.00 QAR; delivery: bank_deposit (default), wallet; fees: STD-B", INR_LINE,
        "QAR-PHP: 50.00 to 20000.00 QAR; delivery: bank_deposit (default), cash_pickup, wallet; fees: STD-A", PKR_LINE])
    edit_runbook(work, (INR_LINE, everything))
    assert_failing(grade(work))


def test_other_ways_to_write_the_commands_and_code_blocks_are_fine(work):
    solved(work)
    text = (work / CARE).read_text(encoding="utf-8")
    text = re.sub(r"^```(\w*)$", r"~~~\1", text, flags=re.M).replace("python -m remit", "python3 -m remit")
    framework.write_file(work, CARE, text)
    learner_commit(work, "docs(docs): use tilde fences and python3")
    assert_failing(grade(work))


def test_one_typed_corridor_line_among_real_ones_is_caught(work):
    solved(work)
    edit_runbook(work, (INR_LINE, INR_LINE + "\n" + PKR_LINE.replace("bank_deposit (default), cash_pickup", "wallet (default)")))
    result = grade(work)
    assert TASK_D in failing(result) and "corridors_section" in result[TASK_D].detail


def test_hand_typed_numbers_in_the_limits_example_are_caught(work):
    solved(work)
    edit_runbook(work, ("(9500.00 left)", "(9400.00 left)"))
    result = grade(work)
    assert TASK_D in failing(result) and "real_usage_line" in result[TASK_D].detail


@pytest.mark.parametrize("old,new", [("of 10000.00 QAR", "of 12000.00 QAR"), ("this month 500.00", "this month 400.00")])
def test_a_usage_line_that_does_not_add_up_is_caught(work, old, new):
    solved(work)
    edit_runbook(work, (old, new))
    assert TASK_D in failing(grade(work))


def test_a_limits_section_with_only_prose_is_caught(work):
    solved(work)
    edit_runbook(work, ("T2: today 500.00 of 10000.00 QAR used (9500.00 left); this month 500.00 of 40000.00 QAR used (39500.00 left)",
                        "it says how much of the limit is used"))
    assert TASK_D in failing(grade(work))


def test_agent_settings_and_gitignore_are_allowed_files(work):
    """Lesson 10.1 saves a subagent under .claude/agents/; an agent may also adjust CLAUDE.md; a learner may ignore worktree folders."""
    solved(work)
    framework.write_file(work, ".claude/agents/task-worker.md", "---\nname: task-worker\ndescription: one task\n---\nDo one task.\n")
    framework.write_file(work, ".gitignore", (work / ".gitignore").read_text(encoding="utf-8") + ".claude/worktrees/\n")
    framework.write_file(work, "CLAUDE.md", (work / "CLAUDE.md").read_text(encoding="utf-8") + "\nIn the REMIT-361 lab, commit when the task is done.\n")
    learner_commit(work, "chore(ci): keep the agent setup")
    assert_failing(grade(work))


@pytest.mark.parametrize("which,addition", [
    ("tests/test_limits.py", None),  # a module-level skip, put at the top (no existing line changes)
    ("tests/test_limits.py", "skipif"),
    ("tests/conftest.py", "collect_ignore"),
])
def test_an_existing_test_switched_off_without_changing_a_line(work, which, addition):
    """Adding lines is allowed; adding a line that switches the old tests off is not."""
    solved(work)
    path = work / which
    text = path.read_text(encoding="utf-8")
    prefix = {None: "import pytest\n\npytestmark = pytest.mark.skip(reason='flaky')\n",
              "skipif": "import pytest\n\npytestmark = pytest.mark.skipif(True, reason='slow')\n",
              "collect_ignore": "collect_ignore = ['test_limits.py']\n"}[addition]
    if which.endswith("conftest.py"):
        path.write_text(text + "\n" + prefix, encoding="utf-8")
    else:
        path.write_text(prefix + text, encoding="utf-8")
    learner_commit(work, "test(limits): stop a flaky test")
    result = grade(work)
    assert WEAKENED in failing(result) and which in result[WEAKENED].detail
    assert "skip" in result[WEAKENED].detail or "ignore" in result[WEAKENED].detail


def test_a_xfail_added_to_an_old_test_file_is_caught(work):
    solved(work)
    path = work / "tests" / "test_fees.py"
    path.write_text(path.read_text(encoding="utf-8") + "\n\n@__import__('pytest').mark.xfail\ndef test_new_known_failure():\n    assert False\n", encoding="utf-8")
    learner_commit(work, "test(fees): record a known failure")
    assert WEAKENED in failing(grade(work))


def test_tests_that_merely_mention_skipped_things_are_fine(work):
    solved(work)
    path = work / "tests" / "test_notify.py"
    path.write_text(path.read_text(encoding="utf-8") + "\n\ndef test_a_skipped_step_is_not_a_skip_marker():\n    skipped = 0\n    assert skipped == 0\n", encoding="utf-8")
    learner_commit(work, "test(notify): add a plain test")
    assert_failing(grade(work))


# --- the plan and the log: shape, content, order -------------------------------------------
def test_plan_first_then_branches_passes_every_check(work):
    write_plan(work)
    reference_flow(work)
    write_log(work)
    result = grade(work)
    assert_failing(result)
    assert "committed before the code" in result[PLAN].detail


def test_the_untouched_template_is_not_a_plan(work):
    shutil.copy(work / "lab-assets" / "parallel-plan-template.md", work / "docs" / "parallel-plan.md")
    learner_commit(work, "docs(docs): start the plan")
    reference_flow(work)
    write_log(work)
    result = grade(work)
    assert_failing(result, PLAN)
    assert "still mostly the template" in result[PLAN].detail and result[PLAN].hint


def test_a_plan_written_after_the_branches_is_reported(work):
    reference_flow(work)
    write_plan(work)
    write_log(work)
    result = grade(work)
    assert_failing(result, PLAN)
    assert "before the plan was committed" in result[PLAN].detail and "first" in result[PLAN].hint
    assert not result[PLAN].required


def test_a_plan_that_was_never_committed_is_reported(work):
    reference_flow(work)
    write_log(work)
    (work / "docs" / "parallel-plan.md").write_text((SOL / "parallel-plan.md").read_text(encoding="utf-8"), encoding="utf-8")
    result = grade(work)
    assert PLAN not in {n for n, c in result.items() if c.ok}  # untracked: reported, and so is the unclean tree
    assert COMMITTED in failing(result)


def test_a_log_made_of_one_repeated_word_is_not_a_log(work):
    write_plan(work)
    reference_flow(work)
    framework.write_file(work, LAB.LOG, "filler " * 40)
    learner_commit(work, "docs(docs): add the log")
    result = grade(work)
    assert_failing(result, LOG)
    assert "different ones" in result[LOG].detail


# --- commits that mix tasks ----------------------------------------------------------------
def test_a_commit_with_the_notify_template_and_a_cli_change_mixes_tasks(work):
    reference_flow(work)
    framework.edit_file(work, "src/remit/notify.py", '"""Customer notifications', '"""Customer notifications (English and Arabic)')
    framework.edit_file(work, CLI, '"""Command line:', '"""The command line:')
    learner_commit(work, "feat(notify): tidy the docstrings")
    result = grade(work)
    assert ONE_TASK in failing(result)
    assert "notify.py (A)" in result[ONE_TASK].detail and "cli.py (B or C)" in result[ONE_TASK].detail
    assert "reset --soft" in result[ONE_TASK].hint


def test_a_commit_with_the_runbook_and_a_cli_change_mixes_tasks(work):
    reference_flow(work)
    framework.edit_file(work, CLI, '"""Command line:', '"""The command line:')
    framework.write_file(work, CARE, (work / CARE).read_text(encoding="utf-8") + "\nMore.\n")
    learner_commit(work, "docs(docs): extend the runbook and the usage note")
    assert ONE_TASK in failing(grade(work))


def test_a_limits_change_with_its_cli_change_is_one_task_and_so_is_a_test_that_spans_tasks(work):
    reference_flow(work)
    framework.edit_file(work, "src/remit/limits.py", '"""Sending limits by KYC tier.', '"""Sending limits by KYC tier (QAR).')
    framework.edit_file(work, CLI, '"""Command line:', '"""The command line:')
    learner_commit(work, "feat(limits): describe the units and the usage note")
    framework.write_file(work, "tests/test_care_together.py", (
        "import io\nfrom remit.cli import main\n\n\n"
        "def test_every_new_command_runs_after_the_merge(tmp_path):\n"
        "    env = {'REMIT_DB': str(tmp_path / 'r.db')}\n"
        "    for argv in (['corridors'], ['corridors', 'QAR-INR']):\n"
        "        out = io.StringIO()\n"
        "        assert main(argv, environ=env, out=out) == 0 and out.getvalue()\n"))
    learner_commit(work, "test(cli): run the new commands together")
    result = grade(work)
    assert ONE_TASK not in failing(result), result[ONE_TASK].detail


# --- hints and details that must fit what the learner really did ----------------------------
def test_commits_that_sit_only_on_other_branches_do_not_get_the_commit_your_change_hint(work):
    for key in "abcd":
        build_branch(work, key)  # four branches full of commits; main has none of them
    result = grade(work)
    assert MESSAGES in failing(result)
    assert "expected at least 4" in result[MESSAGES].detail
    assert "Commit your change" not in result[MESSAGES].hint
    assert "Merge each task's branch into main" in result[MESSAGES].hint

    assert "not part of main's history" in result[BRANCHES].detail  # and the branches are named
    assert "feat/limits-command" in result[BRANCHES].detail


def test_the_message_hint_for_bad_headers_fits_older_commits_too(work):
    reference_flow(work)
    framework.write_file(work, "docs/notes.md", "notes\n")
    learner_commit(work, "wip")
    hint = grade(work)[MESSAGES].hint
    assert "amend" in hint and "rebase" in hint and "merge commits are not checked" in hint


def test_squashed_branches_are_named_and_explained(work):
    for key in "abc":
        build_branch(work, key)
    for key in "abc":
        git(work, "merge", "--squash", PART[key][0], check=False)
        if key != "a":
            framework.write_file(work, CLI, (SOL / "cli_resolved.txt").read_text(encoding="utf-8"))
        learner_commit(work, "feat(cli): squash")
    result = grade(work)[BRANCHES]
    assert "unmerged, or squashed" in result.detail and "feat/delay-notice" in result.detail
    assert "Merge those branches" in result.hint and "not --squash" in result.hint  # they exist: do not say "give each task a branch"


def test_a_detached_head_is_described_as_such(work):
    reference_flow(work)
    git(work, "checkout", "-q", "--detach")
    result = grade(work)
    assert ON_MAIN in failing(result) and "detached" in result[ON_MAIN].detail


def test_the_advisory_count_reports_failures_and_errors_separately(work):
    solved(work)
    detail = grade(work)[NEW_TESTS].detail
    assert detail.endswith("on the original code, as they should")
    assert "failed" in detail and "error" in detail


def test_known_limit_branch_names_made_up_after_a_squash_look_like_fast_forwards(work):
    """The honour-system edge, said in lesson 10.2: git cannot tell `git branch fake HEAD~1` from a branch that was
    rebased and fast-forwarded, so three bookmarks on three squash commits pass 'branches merged'. The lab trusts you."""
    for key in "abc":
        build_branch(work, key)
    for key in "abc":
        git(work, "merge", "--squash", PART[key][0], check=False)
        if key != "a":
            framework.write_file(work, CLI, (SOL / "cli_resolved.txt").read_text(encoding="utf-8"))
        learner_commit(work, f"feat(cli): squash {key}")
    for key in "abc":
        git(work, "branch", "-D", PART[key][0])
    for name, back in (("fake-a", 2), ("fake-b", 1), ("fake-c", 0)):
        git(work, "branch", name, f"HEAD~{back}" if back else "HEAD")
    assert grade(work)[BRANCHES].ok


def test_the_dry_run_route_every_branch_cut_from_the_plan_commit_with_an_integration_test(work):
    """Plan first, all four branches cut from the plan commit (the runbook too), merged in order A, B, C, D,
    then one cross-task test and the log, each in a commit of its own."""
    write_plan(work)
    for key in "abcd":
        build_branch(work, key)
    for key in "abcd":
        merge(work, PART[key][0])
    framework.write_file(work, "tests/test_care_together.py", (
        "import io\nfrom remit.cli import main\n\n\n"
        "def test_corridors_and_limits_after_the_merge(tmp_path):\n"
        "    env = {'REMIT_DB': str(tmp_path / 'r.db')}\n"
        "    out = io.StringIO()\n"
        "    assert main(['corridors'], environ=env, out=out) == 0 and len(out.getvalue().splitlines()) == 4\n"))
    learner_commit(work, "test(cli): run the new commands together")
    write_log(work)
    result = grade(work)
    assert_failing(result)
    assert result[BRANCHES].detail.startswith("4 merged")


def test_the_runbook_may_word_its_headings_and_wrap_the_quote_its_own_way(work):
    """Headings that start with the ticket's words, the English wording quoted in a block that wraps in the middle of the phrase."""
    solved(work)
    text = (work / CARE).read_text(encoding="utf-8")
    text = text.replace("## Corridors\n", "## Corridors command\n").replace("## Limits\n", "## Limits (daily and monthly)\n")
    text = text.replace("is taking longer than expected. We are\n> working on it", "is taking\n> longer than expected. We are working\n> on it")
    framework.write_file(work, CARE, text)
    learner_commit(work, "docs(docs): reword the runbook headings")
    assert "is taking\n> longer" in text
    assert_failing(grade(work))


def test_a_runbook_without_the_english_wording_or_a_section_is_still_caught(work):
    solved(work)
    edit_runbook(work, ("is taking longer than expected", "is late"))
    assert TASK_D in failing(grade(work))
