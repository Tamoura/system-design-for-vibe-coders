"""Negative and alternative-solution tests for m13 (a personal eval and a 90-day plan).

The grader RUNS the learner's checks, so most tests here start from the solved lab, spoil one thing the way a
learner or an agent really does (a JSON array instead of JSON Lines, a check that passes before any work, a test
that asserts nothing, a goal with no number...), and say exactly which checks must fail and which must stay green.
A grader is only trusted once it has rejected wrong answers for the right reason and accepted a right answer
reached a different way, so the last group builds a differently shaped eval and plan and expects a pass.
"""
from __future__ import annotations

import hashlib
import io
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from ailab import checks_m13 as m13
from ailab import framework, gitutil
from conftest import LEARNER, learner_commit, start

R = m13.runner()


@pytest.fixture(autouse=True)
def default_timeout(monkeypatch):
    """One test shortens the grader's time limit; none may leak it into the next."""
    monkeypatch.setattr(R, "TIMEOUT", m13.GRADER_TIMEOUT)


_MEMO: dict = {}


def _eval_files_digest(work: Path) -> str:
    """What a task's result can depend on besides the task itself: the check, setup and reference files."""
    digest = hashlib.sha256()
    for top in ("eval", "lab-assets"):
        for path in sorted((work / top).rglob("*")) if (work / top).is_dir() else []:
            if path.is_file() and path.name not in ("tasks.jsonl", "README.md", "results.jsonl") and "__pycache__" not in path.parts:
                digest.update(path.relative_to(work).as_posix().encode() + b"\0" + path.read_bytes() + b"\0")
    return digest.hexdigest()


@pytest.fixture(autouse=True)
def memoise_runs(monkeypatch):
    """Running a task's checks costs a second or two. The same task over the same check files gives the same answer,
    so tests that change one task re-run only that task. (Each distinct task still runs for real once.)"""
    real = R.evaluate

    def memo(repo, base, task, **kwargs):
        key = (json.dumps({k: v for k, v in task.items() if k != "_line"}, sort_keys=True), _eval_files_digest(Path(repo)), base,
               kwargs.get("run_baseline", True), kwargs.get("run_reference", True))
        if key not in _MEMO:
            _MEMO[key] = real(repo, base, task, **kwargs)
        return _MEMO[key]

    monkeypatch.setattr(R, "evaluate", memo)


# --------------------------------------------------------------------------------------------
# fixtures and helpers
# --------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def starter(tmp_path_factory) -> Path:
    return start("m13", tmp_path_factory.mktemp("m13-starter") / "work")


@pytest.fixture(scope="module")
def solved(tmp_path_factory) -> Path:
    work = start("m13", tmp_path_factory.mktemp("m13-solved") / "work")
    framework.solve_lab(framework.load_lab("m13"), work)
    return work


@pytest.fixture
def work(solved, tmp_path) -> Path:
    """A private copy of the solved lab (history and the lab-start tag come with it)."""
    target = tmp_path / "work"
    shutil.copytree(solved, target)
    return target


@pytest.fixture
def fresh(starter, tmp_path) -> Path:
    target = tmp_path / "work"
    shutil.copytree(starter, target)
    return target


def names(checks) -> dict[str, framework.Check]:
    return {c.name: c for c in checks}


def failing(result: dict[str, framework.Check]) -> set[str]:
    return {name for name, check in result.items() if not check.ok}


def required_failures(result: dict[str, framework.Check]) -> set[str]:
    return {name for name, check in result.items() if not check.ok and check.required}


def assert_only(result, *expected: str) -> None:
    got = failing(result)
    detail = "\n".join(f"  {'ok  ' if c.ok else 'FAIL'} {n}: {c.detail}" for n, c in result.items())
    assert got == set(expected), f"expected failures {set(expected)}, got {got}\n{detail}"


def grade_eval(work: Path) -> dict[str, framework.Check]:
    return names(m13.eval_checks(work))


def grade_plan(work: Path) -> dict[str, framework.Check]:
    return names(m13.plan_checks(work))


def grade_repo(work: Path) -> dict[str, framework.Check]:
    return names(m13.repo_checks(work))


def grade_all(work: Path) -> dict[str, framework.Check]:
    return names(framework.grade_lab(framework.load_lab("m13"), work, catch=False))


def load_tasks(work: Path) -> list[dict]:
    lines = (work / "eval" / "tasks.jsonl").read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def save_tasks(work: Path, tasks: list[dict]) -> None:
    (work / "eval" / "tasks.jsonl").write_text("".join(json.dumps(t, ensure_ascii=False) + "\n" for t in tasks), encoding="utf-8")


def change(work: Path, task_id: str, **fields) -> None:
    tasks = load_tasks(work)
    for task in tasks:
        if task["id"] == task_id:
            for key, value in fields.items():
                if value is None:
                    task.pop(key, None)
                else:
                    task[key] = value
    save_tasks(work, tasks)


def write(work: Path, rel: str, text: str) -> None:
    path = work / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def plan_replace(work: Path, old: str, new: str) -> None:
    path = work / "plan.md"
    text = path.read_text(encoding="utf-8")
    assert old in text, old
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def python_check(code: str) -> dict:
    return {"run": f'python -c "{code}"'}


# --------------------------------------------------------------------------------------------
# the starter and the reference
# --------------------------------------------------------------------------------------------
def test_the_starter_fails_for_the_right_reasons(starter):
    result = grade_all(starter)
    assert required_failures(result) == {
        m13.N_JSONL, m13.N_COUNT, m13.N_FIELDS, m13.N_RUNS, m13.N_FAILS, m13.N_GUARD, m13.N_REFS, m13.N_PLACEHOLDER, m13.N_OFFLINE,
        m13.N_SECTIONS, m13.N_START, m13.N_SKILLS, m13.N_ROUTINE, m13.N_GOALS, m13.N_SCOPE, m13.N_STEPS, m13.N_COMMITS,
    }
    assert result[m13.N_CLEAN].ok and result[m13.N_SECRETS].ok
    assert all(c.hint for c in result.values() if not c.ok), "every failing check gives a hint"
    shown = "".join(c.detail + c.hint for c in result.values())
    assert "T0" not in shown, "the grader must not leak the reference tasks"


def test_the_reference_solution_passes_every_check(work):
    result = grade_all(work)
    assert_only(result)
    assert len(result) == 27  # 15 about the eval, 7 about the plan, 5 about the repository; the names are unique


def test_the_course_template_copied_unchanged_is_not_a_plan(fresh):
    shutil.copyfile(fresh / "lab-assets" / "plan-template.md", fresh / "plan.md")
    result = grade_plan(fresh)
    assert {m13.N_SECTIONS, m13.N_START, m13.N_SKILLS, m13.N_ROUTINE, m13.N_GOALS} <= failing(result)


def test_the_examples_copied_as_the_eval_are_not_eight_tasks(fresh):
    (fresh / "eval").mkdir()
    shutil.copyfile(fresh / "lab-assets" / "tasks.example.jsonl", fresh / "eval" / "tasks.jsonl")
    result = grade_eval(fresh)
    assert result[m13.N_JSONL].ok
    assert not result[m13.N_COUNT].ok and "3 of the course's examples do not count" in result[m13.N_COUNT].detail
    assert not result[m13.N_RUNS].ok  # three tasks, and fewer than six on the repository


# --------------------------------------------------------------------------------------------
# eval/tasks.jsonl: the file itself
# --------------------------------------------------------------------------------------------
def test_a_json_array_instead_of_json_lines(work):
    """What a chat assistant produces when you ask for 'a JSON file of tasks'."""
    write(work, "eval/tasks.jsonl", json.dumps(load_tasks(work), indent=2))
    result = grade_eval(work)
    assert not result[m13.N_JSONL].ok
    assert "one" in result[m13.N_JSONL].hint.lower()
    assert not result[m13.N_COUNT].ok  # nothing was read, so nothing counts


def test_pretty_printed_objects_are_not_json_lines(work):
    write(work, "eval/tasks.jsonl", "\n".join(json.dumps(t, indent=2) for t in load_tasks(work)))
    assert not grade_eval(work)[m13.N_JSONL].ok


def test_a_markdown_fence_around_the_lines(work):
    body = (work / "eval" / "tasks.jsonl").read_text(encoding="utf-8")
    write(work, "eval/tasks.jsonl", "```json\n" + body + "```\n")
    result = grade_eval(work)
    assert not result[m13.N_JSONL].ok and "line 1" in result[m13.N_JSONL].detail


def test_one_bad_line_among_good_ones_is_named(work):
    lines = (work / "eval" / "tasks.jsonl").read_text(encoding="utf-8").splitlines()
    lines[3] = lines[3].rstrip("}")  # truncated object
    write(work, "eval/tasks.jsonl", "\n".join(lines) + "\n")
    result = grade_eval(work)
    assert not result[m13.N_JSONL].ok and "line 4" in result[m13.N_JSONL].detail
    assert_only(result, m13.N_JSONL)  # the eight good lines are still eight tasks, and still run


def test_five_tasks_are_not_eight(work):
    save_tasks(work, load_tasks(work)[:5])
    result = grade_eval(work)
    assert not result[m13.N_COUNT].ok and "5 tasks of your own" in result[m13.N_COUNT].detail
    assert result[m13.N_JSONL].ok and result[m13.N_FIELDS].ok


def test_duplicate_ids_are_named(work):
    tasks = load_tasks(work)
    tasks[4]["id"] = "T03"
    save_tasks(work, tasks)
    result = grade_eval(work)
    assert not result[m13.N_COUNT].ok and "id T03 on lines 3 and 5" in result[m13.N_COUNT].detail


@pytest.mark.parametrize(
    "fields, expected",
    [
        ({"prompt": "Fix it."}, "prompt"),
        ({"kind": "chore"}, "kind"),
        ({"title": "x"}, "title"),
        ({"check": {}}, "check.run"),
        ({"check": {"run": ""}}, "check.run"),
        ({"reference": "../outside.patch"}, "reference"),
        ({"setup": "eval/setup/missing.patch"}, "does not exist"),
    ],
    ids=["short-prompt", "unknown-kind", "tiny-title", "empty-check", "blank-run", "path-escape", "missing-patch"],
)
def test_malformed_tasks_are_named(work, fields, expected):
    change(work, "T05", **fields)
    result = grade_eval(work)
    assert not result[m13.N_FIELDS].ok
    assert "T05" in result[m13.N_FIELDS].detail and expected in result[m13.N_FIELDS].detail


def test_a_bad_id_is_named_by_its_line(work):
    change(work, "T05", id="3 bad id")
    result = grade_eval(work)
    assert not result[m13.N_FIELDS].ok and "line 5" in result[m13.N_FIELDS].detail and "id:" in result[m13.N_FIELDS].detail


def test_a_task_without_any_check_at_all(work):
    change(work, "T06", check=None)
    result = grade_eval(work)
    assert not result[m13.N_FIELDS].ok and "check.run" in result[m13.N_FIELDS].detail


# --------------------------------------------------------------------------------------------
# the checks themselves: do they run, do they bite?
# --------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "run",
    ['python -c "assert True"', "pytest -q", 'grep -q "" README.md', 'python -c "print(1)"'],
    ids=["assert-true", "whole-suite", "grep-anything", "just-prints"],
)
def test_a_check_that_already_passes_proves_nothing(work, run):
    change(work, "T03", check={"run": run}, reference=None)
    result = grade_eval(work)
    assert not result[m13.N_FAILS].ok and "T03" in result[m13.N_FAILS].detail
    assert "before any work" in result[m13.N_FAILS].detail
    assert required_failures(result) == {m13.N_FAILS}


def test_a_check_that_only_asks_for_a_file_accepts_a_placeholder(work):
    """T04's answer check replaced by 'ANSWER.md exists and has a line': the empty note 'TODO' satisfies it."""
    change(work, "T04", check={"run": 'grep -q "" ANSWER.md'})
    result = grade_eval(work)
    assert_only(result, m13.N_PLACEHOLDER)
    assert "T04" in result[m13.N_PLACEHOLDER].detail and "ANSWER.md" in result[m13.N_PLACEHOLDER].detail


def test_a_test_writing_task_whose_check_only_runs_the_tests_accepts_a_test_that_asserts_nothing(work):
    """T05 checked by 'run the new tests' alone, with no mutation: `assert True` passes, so the check is too weak."""
    change(work, "T05", check={"run": "pytest -q tests/test_ledger_partner_share.py", "guard": "pytest -q"})
    result = grade_eval(work)
    assert_only(result, m13.N_PLACEHOLDER)
    assert "tests/test_ledger_partner_share.py" in result[m13.N_PLACEHOLDER].detail


def test_a_reference_with_helper_files_the_check_does_not_use_is_not_called_weak(work):
    """An agent's reference often adds a test and a note the prompt asked for. If the check does not depend on a file,
    replacing it with a placeholder proves nothing, so it must not be reported."""
    extra = ("diff --git a/NOTES.txt b/NOTES.txt\nnew file mode 100644\n--- /dev/null\n+++ b/NOTES.txt\n@@ -0,0 +1 @@\n+what I changed\n"
             "diff --git a/tests/test_cli_corridors.py b/tests/test_cli_corridors.py\nnew file mode 100644\n--- /dev/null\n"
             "+++ b/tests/test_cli_corridors.py\n@@ -0,0 +1,3 @@\n+def test_it():\n+    assert 1 + 1 == 2\n+\n")
    path = work / "eval" / "reference" / "T01.patch"
    path.write_text(path.read_text(encoding="utf-8") + extra, encoding="utf-8")
    result = grade_eval(work)
    assert_only(result)
    task = next(t for t in load_tasks(work) if t["id"] == "T01")
    assert R.new_files_in_patch(path.read_text(encoding="utf-8")) == ["NOTES.txt", "tests/test_cli_corridors.py"]
    assert R.evaluate(work, "lab-start", task).placeholders == []


@pytest.mark.parametrize(
    "run, expected",
    [
        ("pytest -q eval/checks/test_does_not_exist.py", "does not exist"),
        ("python eval/checks/nope.py", "does not exist"),
        ("pytest -q eval/checks/test_t02_quote_expiry.py -k nothing_matches_this", "collected no tests"),
    ],
    ids=["missing-pytest-file", "missing-script", "empty-selection"],
)
def test_a_check_that_cannot_run_is_broken_not_failing(work, run, expected):
    change(work, "T02", check={"run": run}, reference=None)
    result = grade_eval(work)
    assert not result[m13.N_RUNS].ok and "T02" in result[m13.N_RUNS].detail and expected in result[m13.N_RUNS].detail
    assert result[m13.N_FAILS].ok  # a broken check is reported once, where it belongs


def test_a_syntax_error_in_the_check_is_broken(work):
    write(work, "eval/checks/check_t06_function_length.py", "def broken(:\n    pass\n")
    result = grade_eval(work)
    assert not result[m13.N_RUNS].ok and "syntax error" in result[m13.N_RUNS].detail


def test_a_check_that_imports_a_package_nobody_has_is_broken(work):
    write(work, "eval/checks/check_t06_function_length.py", "import left_pad_9000\n")
    result = grade_eval(work)
    assert not result[m13.N_RUNS].ok and "left_pad_9000" in result[m13.N_RUNS].detail


def test_a_check_for_code_that_does_not_exist_yet_fails_as_it_should(work):
    """Importing the function the tool must write fails on the starter: that is a failing check, not a broken one."""
    write(work, "eval/checks/test_t01_corridors_command.py",
          "def test_new_helper():\n    from remit.cli import list_corridors\n    assert list_corridors()\n")
    change(work, "T01", reference=None)
    result = grade_eval(work)
    assert result[m13.N_RUNS].ok and result[m13.N_FAILS].ok


def test_a_hanging_check_cannot_hang_the_grader(work, monkeypatch):
    monkeypatch.setattr(m13, "GRADER_TIMEOUT", 2.0)
    change(work, "T06", check={"run": 'python -c "import time; time.sleep(60)"'}, reference=None)
    result = grade_eval(work)
    assert not result[m13.N_RUNS].ok and "did not finish within 2 s" in result[m13.N_RUNS].detail


@pytest.mark.parametrize(
    "run, expected",
    [
        ("bash -c 'touch /tmp/ailab-m13-pwned'", "not allowed"),
        ("curl http://localhost:9/x", "not allowed"),
        ("rm -rf eval", "not allowed"),
        ("pytest -q && echo done", "shell operator"),
        ("pytest -q > out.txt", "shell operator"),
        ("git push origin main", "read-only"),
        ("pytest -q /etc", "relative"),
        ("pytest -q ../elsewhere", "relative"),
        ("sh eval/checks/run.sh", "not allowed"),
    ],
    ids=["bash", "curl", "rm", "and", "redirect", "git-push", "absolute", "parent", "sh"],
)
def test_commands_outside_the_allow_list_are_refused_and_never_run(work, run, expected):
    marker = Path("/tmp/ailab-m13-pwned")
    marker.unlink(missing_ok=True)
    change(work, "T08", check={"run": run}, reference=None)
    result = grade_eval(work)
    assert not result[m13.N_RUNS].ok and "T08" in result[m13.N_RUNS].detail and expected in result[m13.N_RUNS].detail
    assert not marker.exists()
    assert (work / "eval").is_dir()


def test_a_guard_that_fails_on_the_untouched_repo(work):
    """The planted bug of T02 already breaks tests/test_fx.py: a guard that includes it is red before any work."""
    change(work, "T02", check={"run": "pytest -q eval/checks/test_t02_quote_expiry.py", "guard": "pytest -q tests/test_fx.py"})
    result = grade_eval(work)
    assert_only(result, m13.N_GUARD)
    assert "T02" in result[m13.N_GUARD].detail


def test_a_guard_that_fails_after_the_reference(work):
    """A guard must protect what a correct solution leaves alone. This one insists on the smell T03 is meant to remove."""
    change(work, "T03", check={"run": "pytest -q eval/checks/test_t03_search_is_safe.py", "guard": 'grep -q "KNOWN SMELL" src/remit/store.py'})
    result = grade_eval(work)
    assert_only(result, m13.N_REFS)
    assert "T03" in result[m13.N_REFS].detail and "guard fails after the reference" in result[m13.N_REFS].detail


def test_a_reference_that_does_not_make_the_check_pass(work):
    """The T07 docs patch offered as T01's 'solution': the check still fails, so the check or the reference is wrong."""
    change(work, "T01", reference="eval/reference/T07.patch")
    result = grade_eval(work)
    assert_only(result, m13.N_REFS)
    assert "T01" in result[m13.N_REFS].detail and "still fails after the reference" in result[m13.N_REFS].detail


def test_a_reference_that_does_not_apply(work):
    write(work, "eval/reference/T03.patch", "this is not a patch\n")
    result = grade_eval(work)
    assert not result[m13.N_RUNS].ok and "T03" in result[m13.N_RUNS].detail and "does not apply" in result[m13.N_RUNS].detail


def test_a_setup_patch_that_does_not_apply(work):
    write(work, "eval/setup/T02.patch", "diff --git a/nope.py b/nope.py\n--- a/nope.py\n+++ b/nope.py\n@@ -1 +1 @@\n-a\n+b\n")
    result = grade_eval(work)
    assert not result[m13.N_RUNS].ok and "T02" in result[m13.N_RUNS].detail


def test_only_two_references_are_not_three(work):
    for task_id in ("T01", "T02", "T03", "T04", "T05", "T06"):
        change(work, task_id, reference=None)
    # T02 needs its setup to fail on the starter; without a reference it still does. T08 and T07 keep theirs.
    result = grade_eval(work)
    assert_only(result, m13.N_REFS)
    assert "2 references pass their checks" in result[m13.N_REFS].detail


def test_no_references_at_all(work):
    for task in load_tasks(work):
        change(work, task["id"], reference=None)
    result = grade_eval(work)
    assert_only(result, m13.N_REFS)
    assert "0 references pass their checks" in result[m13.N_REFS].detail


def test_too_few_tasks_the_kit_can_run(work):
    for task_id in ("T04", "T05", "T06", "T07"):
        change(work, task_id, repo="own")
    result = grade_eval(work)
    assert_only(result, m13.N_RUNS)
    assert "at least 6" in result[m13.N_RUNS].detail


def test_a_check_that_needs_the_network(work):
    write(work, "eval/checks/check_t06_function_length.py",
          "import urllib.request\nurllib.request.urlopen('http://localhost:9/')\n")
    result = grade_eval(work)
    assert not result[m13.N_OFFLINE].ok and "check_t06_function_length.py" in result[m13.N_OFFLINE].detail


def test_a_url_in_a_check_command_counts_as_network(work):
    change(work, "T08", check={"run": 'python -c "import sys; sys.exit(\'see https://example.invalid\')"'}, reference=None)
    assert not grade_eval(work)[m13.N_OFFLINE].ok


def test_a_check_that_reads_the_clock_is_only_advisory(work):
    path = work / "eval" / "checks" / "check_t06_function_length.py"
    path.write_text(path.read_text(encoding="utf-8") + "\nimport datetime\nprint(datetime.datetime.now())\n", encoding="utf-8")
    result = grade_eval(work)
    assert_only(result, m13.N_CLOCK)
    assert not result[m13.N_CLOCK].required


def test_a_hostile_check_cannot_touch_the_work_directory(work):
    """Checks run in throw-away copies: a check that writes files writes them there."""
    write(work, "eval/checks/check_t06_function_length.py",
          "import pathlib\npathlib.Path('hacked.txt').write_text('x')\npathlib.Path('eval/checks/new.py').write_text('x')\nraise SystemExit(1)\n")
    before = sorted(p.relative_to(work).as_posix() for p in work.rglob("*") if ".git" not in p.parts)
    grade_eval(work)
    after = sorted(p.relative_to(work).as_posix() for p in work.rglob("*") if ".git" not in p.parts)
    assert before == after and not (work / "hacked.txt").exists()


def test_checks_placed_outside_eval_are_not_part_of_a_clean_copy(work):
    """A check committed under tests/ does not exist in the clean copy the kit builds, so its reference cannot pass it."""
    shutil.copyfile(work / "eval" / "checks" / "test_t03_search_is_safe.py", work / "tests" / "test_t03_search_is_safe.py")
    change(work, "T03", check={"run": "pytest -q tests/test_t03_search_is_safe.py", "guard": "pytest -q"})
    learner_commit(work, "test(eval): move a check next to the tests")
    eval_result = grade_eval(work)
    assert not eval_result[m13.N_REFS].ok and "T03" in eval_result[m13.N_REFS].detail
    assert not grade_repo(work)[m13.N_SCOPE].ok


def test_no_guards_no_own_project_and_no_readme_only_lose_advisory_checks(work):
    for task in load_tasks(work):
        change(work, task["id"], check={"run": task["check"]["run"]})  # drop every guard
    change(work, "T09", repo=None, check={"run": "pytest -q eval/checks/test_t03_search_is_safe.py"})
    (work / "eval" / "README.md").unlink()
    result = grade_eval(work)
    assert required_failures(result) == set()
    assert {m13.N_GUARDED, m13.N_OWN, m13.N_README} <= failing(result)


def test_a_results_log_with_a_bad_line(work):
    write(work, "eval/results.jsonl", '{"task": "T01", "tool": "me", "passed": true}\nnot json\n')
    result = grade_eval(work)
    assert not result[m13.N_RESULTS].ok and not result[m13.N_RESULTS].required


# --------------------------------------------------------------------------------------------
# plan.md
# --------------------------------------------------------------------------------------------
def test_a_missing_section_is_named(work):
    text = (work / "plan.md").read_text(encoding="utf-8")
    write(work, "plan.md", text.replace("## Eval cadence", "## Something else"))
    result = grade_plan(work)
    assert_only(result, m13.N_SECTIONS)
    assert "Eval cadence" in result[m13.N_SECTIONS].detail


def test_a_section_with_one_line_is_too_thin(work):
    text = (work / "plan.md").read_text(encoding="utf-8")
    start = text.index("## Days 31-60")
    end = text.index("## Days 61-90")
    write(work, "plan.md", text[:start] + "## Days 31-60\n\nKeep going.\n\n" + text[end:])
    result = grade_plan(work)
    assert_only(result, m13.N_SECTIONS)
    assert "too short: Days 31-60" in result[m13.N_SECTIONS].detail


def test_guidance_comments_do_not_count_as_words(work):
    text = (work / "plan.md").read_text(encoding="utf-8")
    start = text.index("## What I will ignore")
    write(work, "plan.md", text[:start] + "## What I will ignore\n\n<!-- the noise you will not chase for ninety days, and what would make you look again -->\n")
    assert "too short: What I will ignore" in grade_plan(work)[m13.N_SECTIONS].detail


@pytest.mark.parametrize("heading", ["## Days 1–30", "## Days 1 to 30", "## First 30 days", "## Month 1"])
def test_other_ways_to_title_the_first_month_are_accepted(work, heading):
    plan_replace(work, "## Days 1-30", heading)
    assert grade_plan(work)[m13.N_SECTIONS].ok


@pytest.mark.parametrize("line, expected", [("", "no line"), ("Start date: next Monday", "no line"), ("Start date: 2026-13-45", "not a real date")])
def test_the_start_date_must_be_a_real_date(work, line, expected):
    plan_replace(work, "Start date: 2026-11-02", line)
    result = grade_plan(work)
    assert not result[m13.N_START].ok and expected in result[m13.N_START].detail


def test_a_bold_start_date_is_fine(work):
    plan_replace(work, "Start date: 2026-11-02", "**Start date:** 2026-11-02")
    assert grade_plan(work)[m13.N_START].ok


def test_a_skills_map_with_five_skills(work):
    plan_replace(work, "| Security basics | September, the quote-mark search bug | 2 | I can spot string-built SQL but not explain a full threat model |\n", "")
    result = grade_plan(work)
    assert_only(result, m13.N_SKILLS)
    assert "5 skills" in result[m13.N_SKILLS].detail


@pytest.mark.parametrize(
    "old, new, expected",
    [("| 3 | I could trace", "| high | I could trace", "Reading unfamiliar code"), ("| 4 | I write boundary tests first and can say what a mutation test shows |", "| 4 | good |", "Testing")],
    ids=["confidence-not-a-number", "evidence-too-thin"],
)
def test_a_skills_map_without_a_number_or_evidence(work, old, new, expected):
    plan_replace(work, old, new)
    result = grade_plan(work)
    assert_only(result, m13.N_SKILLS)
    assert expected in result[m13.N_SKILLS].detail


@pytest.mark.parametrize(
    "old, new, expected",
    [
        ("| 6 | 2026-12-15 |", "| improve | 2026-12-15 |", "no number"),
        ("| 2026-12-15 |", "| end of the quarter |", "not a YYYY-MM-DD date"),
        ("| 2026-12-15 |", "| 2027-03-01 |", "outside the 90 days"),
        ("| 2026-12-15 |", "| 2026-10-01 |", "outside the 90 days"),
        ("| 0 in the last month |", "| |", "baseline"),
        ("| A tally in my agent log, checked against the git history |", "| a tally |", "how you will measure"),
        ("| Debug more of my own bugs unaided |", "| Be better |", "at least 4 words"),
    ],
    ids=["vague-target", "vague-date", "after-the-window", "before-the-start", "no-baseline", "no-way-to-measure", "vague-goal"],
)
def test_goals_that_cannot_be_measured(work, old, new, expected):
    plan_replace(work, old, new)
    result = grade_plan(work)
    assert_only(result, m13.N_GOALS)
    assert expected in result[m13.N_GOALS].detail


def test_two_goals_and_eight_goals_are_both_wrong(work):
    text = (work / "plan.md").read_text(encoding="utf-8")
    section = text[text.index("## Goals"):text.index("## Days 1-30")]
    goal_rows = [line for line in section.splitlines() if line.startswith("| ") and not line.startswith(("| Goal", "|---"))]
    assert len(goal_rows) == 4
    write(work, "plan.md", text.replace(goal_rows[2] + "\n", "").replace(goal_rows[3] + "\n", ""))
    assert "2 goals" in grade_plan(work)[m13.N_GOALS].detail
    many = text.replace(goal_rows[3] + "\n", "".join(goal_rows[3] + "\n" for _ in range(5)))
    write(work, "plan.md", many)
    assert "8 goals" in grade_plan(work)[m13.N_GOALS].detail


def test_goals_with_dates_need_a_start_date_to_be_checked(work):
    plan_replace(work, "Start date: 2026-11-02", "")
    result = grade_plan(work)
    assert not result[m13.N_START].ok and not result[m13.N_GOALS].ok
    assert "Start date" in result[m13.N_GOALS].detail


def test_a_goal_table_without_a_target_column(work):
    plan_replace(work, "| Goal | Metric | Baseline | Target | By | How I will measure it |", "| Goal | Metric | Baseline | Result | By | How I will measure it |")
    result = grade_plan(work)
    assert not result[m13.N_GOALS].ok and "target" in result[m13.N_GOALS].detail


@pytest.mark.parametrize(
    "old, new, expected",
    [
        ("| Monday | One kata without the agent, then the agent as a tutor for hints only | 45 |", "| Monday | One kata | 2 |", "outside 5 to 240"),
        ("| Monday | One kata without the agent, then the agent as a tutor for hints only | 45 |", "| Monday | One kata without the agent for a long time | a lot |", "not a number"),
        ("| Monday | One kata without the agent, then the agent as a tutor for hints only | 45 |", "| Monday | One kata without the agent for a long time | 240 |\n| Tuesday | Another long deep practice session | 240 |\n| Wednesday | More long deep practice here | 240 |", "minutes a week"),
    ],
    ids=["five-minutes-is-two", "minutes-not-a-number", "far-too-much"],
)
def test_an_unrealistic_weekly_routine(work, old, new, expected):
    plan_replace(work, old, new)
    result = grade_plan(work)
    assert not result[m13.N_ROUTINE].ok and expected in result[m13.N_ROUTINE].detail


def test_a_routine_with_two_practices(work):
    text = (work / "plan.md").read_text(encoding="utf-8")
    start, end = text.index("| Wednesday"), text.index("## Goals")
    write(work, "plan.md", text[:start] + "\n" + text[end:])
    result = grade_plan(work)
    assert not result[m13.N_ROUTINE].ok and "at least 3" in result[m13.N_ROUTINE].detail


def test_a_routine_that_always_uses_the_agent_loses_only_an_advisory_check(work):
    plan_replace(work, "One kata without the agent, then the agent as a tutor for hints only", "One kata with the agent as a tutor for hints")
    plan_replace(work, "Explain-back: tell a colleague what the agent changed and why, without notes", "Explain-back: tell a colleague what the agent changed and why")
    result = grade_plan(work)
    assert_only(result, m13.N_NO_AI)
    assert not result[m13.N_NO_AI].required


def test_no_goal_about_the_eval_loses_only_an_advisory_check(work):
    text = (work / "plan.md").read_text(encoding="utf-8")
    write(work, "plan.md", text.replace("Pass rate of my eval per tool, three runs each", "Tasks scored per tool, three runs each")
          .replace("no eval yet", "nothing yet").replace("eval/results.jsonl and the report command", "the report command"))
    assert_only(grade_plan(work), m13.N_EVAL_GOAL)


# --------------------------------------------------------------------------------------------
# the repository
# --------------------------------------------------------------------------------------------
def test_editing_the_code_or_the_course_files_is_out_of_scope(work):
    framework.edit_file(work, "src/remit/fees.py", '"""Fees: what Najm charges', '"""Fees (my notes): what Najm charges')
    (work / "lab-assets" / "eval_runner.py").write_text("# my edit\n", encoding="utf-8")
    learner_commit(work, "chore(fees): notes")
    result = grade_repo(work)
    assert_only(result, m13.N_SCOPE)
    assert "src/remit/fees.py" in result[m13.N_SCOPE].detail and "lab-assets/eval_runner.py" in result[m13.N_SCOPE].detail


def test_one_big_commit(work):
    gitutil.git(work, "reset", "--soft", "lab-start")
    learner_commit(work, "docs(plan): everything at once")
    assert_only(grade_repo(work), m13.N_STEPS)


@pytest.mark.parametrize("message", ["add my eval", "feat: eval", "Docs(plan): Plan", "docs(plan): add my plan."], ids=["plain", "no-scope", "wrong-case", "full-stop"])
def test_commit_messages_that_ignore_contributing_md(work, message):
    gitutil.git(work, "commit", "--amend", "-m", message, "--author", "Najm Learner <learner@najm.example>")
    assert_only(grade_repo(work), m13.N_COMMITS)


def test_uncommitted_work(work):
    write(work, "eval/notes.md", "scratch\n")
    assert_only(grade_repo(work), m13.N_CLEAN)


def test_a_credential_in_the_readme(work):
    path = work / "eval" / "README.md"
    path.write_text(path.read_text(encoding="utf-8") + '\nGATEWAY_KEY = "sk-live-' + "9f8e7d6c5b4a3f2e1d0c" + '"\n', encoding="utf-8")
    learner_commit(work, "docs(eval): note the key")
    result = grade_repo(work)
    assert_only(result, m13.N_SECRETS)
    assert "9f8e7d6c" not in result[m13.N_SECRETS].detail + result[m13.N_SECRETS].hint


def test_tool_noise_does_not_count_against_the_learner(work):
    (work / ".claude").mkdir()
    (work / ".claude" / "settings.local.json").write_text("{}")
    (work / ".DS_Store").write_bytes(b"\0")
    (work / "eval" / "checks" / "__pycache__").mkdir()
    (work / "eval" / "checks" / "__pycache__" / "x.cpython-311.pyc").write_bytes(b"\0")
    assert_only(grade_repo(work))


# --------------------------------------------------------------------------------------------
# an alternative, differently shaped, correct solution
# --------------------------------------------------------------------------------------------
ALT_TASKS = [
    {"id": "A1", "title": "Corridors listing", "kind": "feature",
     "prompt": "Add a corridors command to the CLI that prints every supported corridor on its own line with the smallest and largest amount you can send, sorted by corridor code, without opening the database.",
     "check": {"run": "pytest -q eval/checks/test_t01_corridors_command.py"}, "reference": "eval/reference/T01.patch"},
    {"id": "A2", "title": "Quotes die at sixty seconds", "kind": "fix",
     "prompt": "A customer used a quote that was exactly one minute old and it was accepted. Quotes are valid for sixty seconds and are expired from the moment they reach that age. Find the cause and fix it.",
     "setup": "eval/setup/T02.patch", "check": {"run": "pytest -q eval/checks/test_t02_quote_expiry.py"},
     "reference": "eval/reference/T02.patch"},
    {"id": "A3", "title": "Search without injection", "kind": "fix",
     "prompt": "The customer name search builds SQL by formatting strings, so quotes break it. Use a bound parameter so any fragment is plain data, and keep the results for ordinary fragments the same.",
     "check": {"run": "pytest -q eval/checks/test_t03_search_is_safe.py", "guard": "pytest -q tests/test_store.py"},
     "reference": "eval/reference/T03.patch"},
    {"id": "A4", "title": "Is T3 documented", "kind": "docs",
     "prompt": "The architecture page lists two customer tiers but the code has three. Update the page so that it describes all of the tiers that exist, and say nothing that is not true.",
     "check": {"run": 'grep -q "T3" docs/ARCHITECTURE.md'}},
    {"id": "A5", "title": "A helper for the corridor table", "kind": "refactor",
     "prompt": "Move the corridor code formatting out of the command handler into a small helper function named format_corridor in remit.cli, so that other commands could reuse it. Behaviour must not change.",
     "check": {"run": 'python -c "import remit.cli as c; assert hasattr(c, \'format_corridor\')"', "guard": "pytest -q tests/test_config_cli.py"}},
    {"id": "A6", "title": "Explain the monthly limit", "kind": "explain",
     "prompt": "Which module decides whether a transfer is over the monthly limit, and which function does it? Write the answer in ANSWER.md in two sentences naming both. Change nothing else.",
     "check": {"run": 'grep -q "check_limits" ANSWER.md'}},
    {"id": "A7", "title": "A test for the cap", "kind": "test",
     "prompt": "Write a test in tests/test_fee_cap.py that proves the express surcharge is added after the cap for a very large transfer to India. It must fail if the surcharge were added before the cap.",
     "check": {"run": "pytest -q tests/test_fee_cap.py"}},
    {"id": "A8", "title": "Review for the second reviewer", "kind": "review",
     "prompt": "Review review/PR-482.diff as the second reviewer and write what you find in REVIEW.md, the most serious first, with the reason each one matters. Do not change any other file.",
     "setup": "eval/setup/T08.patch", "check": {"run": "python eval/checks/check_t08_review.py"}, "reference": "eval/reference/T08.patch"},
]

ALT_PLAN = """# Ninety days

**Start date:** 2026-12-01

## Where I am (skills map)

| Skill | Evidence | Last did it without AI | Confidence (1-5) |
|---|---|---|---|
| Reading code | I traced send() end to end last week | August | 3 |
| Debugging | I fixed the quote expiry bug from a log | September | 4 |
| Systems thinking | I could not predict the ledger failure mode | July | 2 |
| Data structures | I use dicts and lists well | May | 3 |
| Testing | I write boundary tests before the code | October | 4 |
| Security basics | I can spot string-built SQL queries | June | 2 |

## Practice each week

| Practice | Minutes | When |
|---|---|---|
| Kata from memory, no agent | 40 | Tuesday |
| Read a merged pull request and write two questions | 30 | Thursday |
| Re-run two eval tasks and log what I corrected | 30 | Friday |

## Goals

| Target | By | Goal | Metric | How I will measure it | Baseline |
|---|---|---|---|---|---|
| 5 | 2027-01-10 | Fix real bugs before asking the agent | Bugs fixed unaided | A tally in my notes and the git log | 0 |
| 8 of 8 | 2027-02-15 | Run every eval task on my main tool | Tasks scored with three runs | The report command output | none yet |
| 90% | 2027-02-28 | Explain every line I commit | Pull requests I can explain | My reviewer's comments in each pull request | not tracked |

## Days 1–30

Keep the weekly routine for four weeks. Run validate, baseline and verify until the eval is clean. Start the tally.

## Days 31–60

Score each task three times with my main tool and read every diff. Pick systems thinking as the skill to lift.

## Days 61–90

Score a second tool, compare pass rates and minutes, and write a page for my lead. Re-rate the skills map honestly.

## When I run the eval again

Every month and whenever my main tool or model changes. The pass rate decides which tasks I delegate and which I keep.

## Not doing

Chasing every release or leaderboard. I look at a new tool only when a task in my eval fails on everything I have.
"""


def test_a_differently_shaped_but_sound_solution_is_accepted(fresh):
    """Fewer references and guards, grep and python -c checks, columns in another order, en-dash headings, other titles."""
    solved_dir = fresh.parent / "reference"
    shutil.copytree(fresh, solved_dir)
    framework.solve_lab(framework.load_lab("m13"), solved_dir)
    # take the pieces we reuse from the reference solution, then rebuild the eval from scratch around them
    eval_dir = fresh / "eval"
    for sub in ("checks", "reference", "setup"):
        shutil.copytree(solved_dir / "eval" / sub, eval_dir / sub)
    save_tasks(fresh, ALT_TASKS)
    (eval_dir / "README.md").write_text(
        "# Eval\n\nRun validate, baseline and verify first. A pass is a passing check plus a passing guard. I run every task "
        "three times per tool, from a clean workspace, and again when the tool changes or monthly.\n", encoding="utf-8")
    learner_commit(fresh, "test(eval): eight tasks with checks")
    (fresh / "plan.md").write_text(ALT_PLAN, encoding="utf-8")
    learner_commit(fresh, "docs(plan): ninety days")
    result = grade_all(fresh)
    assert required_failures(result) == set(), {n: c.detail for n, c in result.items() if not c.ok and c.required}
    assert not result[m13.N_OWN].ok  # the advisory notes that remain: no task from the learner's own project


# --------------------------------------------------------------------------------------------
# the runner the learner is given
# --------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "command, ok",
    [
        ("pytest -q", True), ("pytest -q eval/checks/test_x.py -k a_b", True), ("python -m pytest -q tests", True),
        ("python eval/checks/check.py", True), ('python -c "import sys; sys.exit(0)"', True), ('grep -q "after the cap" ANSWER.md', True),
        ("git diff --quiet", True), ("git log -1", True),
        ("", False), ("   ", False), ("npm test", False), ("make", False), ("bash run.sh", False), ("pytest -q | head", False),
        ("pytest -q ; ls", False), ("pytest -q 2>&1", False), ("git commit -m x", False), ("git", False), ("pytest /tmp", False),
        ("pytest ~/x", False), ("pytest ../x", False), ("pytest 'unclosed", False),
    ],
)
def test_the_command_allow_list(command, ok):
    argv, problem = R.parse_command(command)
    assert (argv is not None) is ok, problem
    assert ok == (problem == "")


@pytest.mark.parametrize(
    "argv, code, out, err, verdict",
    [
        (["pytest", "-q", "x.py"], 0, "1 passed", "", "pass"),
        (["pytest", "-q", "x.py"], 1, "1 failed", "", "fail"),
        (["pytest", "-q", "x.py"], 5, "no tests ran", "", "broken"),
        (["pytest", "-q", "eval/x.py"], 4, "", "ERROR: file or directory not found: eval/x.py", "broken"),
        (["pytest", "-q", "tests/new.py"], 4, "", "ERROR: file or directory not found: tests/new.py", "fail"),
        (["pytest", "-q", "x.py"], 2, "", "E   ModuleNotFoundError: No module named 'remit.reporting'", "fail"),
        (["pytest", "-q", "x.py"], 2, "", "E   ModuleNotFoundError: No module named 'pandas'", "broken"),
        (["pytest", "-q", "x.py"], 2, "E     SyntaxError: invalid syntax", "", "broken"),
        (["pytest", "-q", "x.py"], 3, "INTERNALERROR", "", "broken"),
        (["python", "-m", "pytest", "x.py"], 1, "1 failed", "", "fail"),
        (["python", "check.py"], 1, "", "AssertionError: no", "fail"),
        (["python", "eval/checks/gone.py"], 2, "", "python: can't open file 'eval/checks/gone.py': [Errno 2]", "broken"),
        (["python", "scripts/new.py"], 2, "", "python: can't open file 'scripts/new.py': [Errno 2]", "fail"),
        (["python", "check.py"], 1, "", "  File \"check.py\", line 1\nSyntaxError: invalid syntax", "broken"),
        (["python", "check.py"], 1, "", "ModuleNotFoundError: No module named 'numpy'", "broken"),
        (["python", "check.py"], 1, "", "ImportError: cannot import name 'x' from 'remit.cli'", "fail"),
        (["python", "-m", "remit.nothing"], 1, "", "python: No module named remit.nothing", "fail"),
        (["grep", "-q", "x", "f"], 1, "", "", "fail"),
        (["grep", "-q", "x", "f"], 2, "", "grep: f: No such file or directory", "fail"),
        (["grep", "-q", "(", "f"], 2, "", "grep: Unmatched ( or \\(", "broken"),
        (["git", "diff", "--quiet"], 1, "", "", "fail"),
        (["git", "diff"], 128, "", "fatal: not a git repository", "broken"),
    ],
)
def test_classifying_a_finished_check(argv, code, out, err, verdict):
    assert R.classify(argv, code, out, err)[0] == verdict


def test_reading_tasks_reports_every_bad_line(tmp_path):
    path = tmp_path / "t.jsonl"
    path.write_text('{"id": "a"}\n\n[1, 2]\nnot json\n{"id": "b"}\n', encoding="utf-8")
    tasks, problems = R.load_tasks(path)
    assert [t["id"] for t in tasks] == ["a", "b"] and [t["_line"] for t in tasks] == [1, 5]
    assert len(problems) == 2 and "line 3" in problems[0] and "array" in problems[0] and "line 4" in problems[1]
    assert R.load_tasks(tmp_path / "none.jsonl")[1] == ["none.jsonl does not exist"]
    empty = tmp_path / "e.jsonl"
    empty.write_text("\n\n", encoding="utf-8")
    assert R.load_tasks(empty)[1] == ["e.jsonl has no tasks"]


def test_patch_helpers():
    patch = ("diff --git a/ANSWER.md b/ANSWER.md\nnew file mode 100644\n--- /dev/null\n+++ b/ANSWER.md\n@@ -0,0 +1 @@\n+x\n"
             "diff --git a/src/a.py b/src/a.py\nindex 1..2 100644\n--- a/src/a.py\n+++ b/src/a.py\n@@ -1 +1 @@\n-a\n+b\n"
             "diff --git a/tests/test_new.py b/tests/test_new.py\nnew file mode 100644\n")
    assert R.new_files_in_patch(patch) == ["ANSWER.md", "tests/test_new.py"]
    assert R.placeholder_for("ANSWER.md") == "TODO\n"
    assert "assert True" in R.placeholder_for("tests/test_new.py")
    assert R.placeholder_for("src/remit/cli.py") is None and R.placeholder_for("tests/helpers.py") is None


def test_the_static_lint_reads_checks_and_commands(tmp_path):
    (tmp_path / "eval" / "checks").mkdir(parents=True)
    (tmp_path / "eval" / "checks" / "a.py").write_text("# requests are fine in a comment\nimport time\ntime.sleep(1)\nimport socket\n", encoding="utf-8")
    tasks = [{"id": "T1", "check": {"run": "curl http://x", "guard": "pytest -q"}}]
    found = R.lint(tmp_path, tasks)
    assert any("a.py:4" in spot for spot in found["network"]) and any("T1 check.run" in spot for spot in found["network"])
    assert found["clock"] == ["eval/checks/a.py:3"]


def run_cli(work: Path, *argv: str) -> tuple[int, str]:
    out = io.StringIO()
    code = R.main(list(argv) + ["--repo", str(work)], out=out)
    return code, out.getvalue()


def test_validate_list_baseline_and_verify_agree_with_the_grader(work):
    code, text = run_cli(work, "validate")
    assert code == 0 and "9 tasks read from tasks.jsonl; 0 problems" in text
    code, text = run_cli(work, "baseline")
    assert code == 0 and "T09" in text and "not run" in text and text.count("ok:") == 8
    code, text = run_cli(work, "verify")
    assert code == 0 and "placeholder answer does not" in text
    code, text = run_cli(work, "list")
    assert code == 0 and "[own project]" in text


def test_the_runner_says_what_is_wrong_before_it_runs_anything(work):
    change(work, "T03", check={"run": "curl http://localhost:9"})
    code, text = run_cli(work, "validate")
    assert code == 1 and "problem: T03" in text and "not allowed" in text
    code, text = run_cli(work, "baseline")
    assert code == 1 and "Fix `validate` first" in text


def test_baseline_names_a_vacuous_check(work):
    change(work, "T03", check={"run": 'python -c "assert True"'}, reference=None)
    code, text = run_cli(work, "baseline")
    assert code == 1 and "PASSES but nothing is done yet" in text


def test_verify_names_a_weak_placeholder_check(work):
    change(work, "T04", check={"run": 'grep -q "" ANSWER.md'})
    code, text = run_cli(work, "verify")
    assert code == 1 and "a placeholder in ANSWER.md passes the check" in text


def test_prepare_hides_the_checks_and_score_reads_the_workspace(work, tmp_path):
    ws = tmp_path / "run-T03"
    code, text = run_cli(work, "prepare", "T03", "--dir", str(ws))
    assert code == 0 and "Store.search_by_name builds its SQL" in text
    for hidden in ("eval", "lab-assets", "TASK.md"):
        assert not (ws / hidden).exists(), f"the tool must not see {hidden}"
    assert (ws / "src" / "remit" / "store.py").is_file() and (ws / ".git").is_dir()
    assert gitutil.out(ws, "log", "--format=%s").strip() == "Eval start: T03"

    code, text = run_cli(work, "score", "T03", "--dir", str(ws), "--tool", "nobody", "--no-record")
    assert code == 1 and text.startswith("T03: FAIL")  # nothing done yet

    subprocess.run(["git", "apply", str(work / "eval" / "reference" / "T03.patch")], cwd=ws, check=True)
    code, text = run_cli(work, "score", "T03", "--dir", str(ws), "--tool", "me", "--model", "by hand", "--minutes", "4",
                         "--note", "wrote it myself", "--date", "2026-11-09")
    assert code == 0 and text.startswith("T03: PASS") and "recorded in results.jsonl" in text
    record = json.loads((work / "eval" / "results.jsonl").read_text(encoding="utf-8").splitlines()[-1])
    assert record == {"task": "T03", "tool": "me", "model": "by hand", "passed": True, "check": "pass", "guard": "pass",
                      "minutes": 4.0, "note": "wrote it myself", "base": "lab-start", "date": "2026-11-09"}
    code, text = run_cli(work, "report")
    assert code == 0 and "me by hand" in text and "1/1" in text
    rows, problems = R.load_tasks(work / "eval" / "results.jsonl")
    assert len(rows) == 1 and not problems  # `score` writes valid JSON Lines


def test_a_tool_cannot_pass_by_planting_its_own_check_or_editing_the_tests(work, tmp_path):
    """T02's planted bug, 'fixed' by weakening the visible test and by adding an eval/ folder of its own."""
    ws = tmp_path / "run-T02"
    run_cli(work, "prepare", "T02", "--dir", str(ws))
    test_file = ws / "tests" / "test_fx.py"
    text = test_file.read_text(encoding="utf-8")
    test_file.write_text(text.replace("is_expired", "is_expired_or_not"), encoding="utf-8")
    (ws / "eval" / "checks").mkdir(parents=True)
    (ws / "eval" / "checks" / "test_t02_quote_expiry.py").write_text("def test_it():\n    assert True\n", encoding="utf-8")
    code, text = run_cli(work, "score", "T02", "--dir", str(ws), "--tool", "cheater", "--no-record")
    assert code == 1 and "FAIL" in text


def test_scoring_a_check_that_cannot_run_is_an_error_not_a_failure(work, tmp_path):
    ws = tmp_path / "run-T03"
    run_cli(work, "prepare", "T03", "--dir", str(ws))
    shutil.rmtree(work / "eval" / "checks")
    code, text = run_cli(work, "score", "T03", "--dir", str(ws), "--tool", "x", "--no-record")
    assert code == 2 and text == ""  # the error goes to stderr


def test_prepare_refuses_a_folder_that_is_not_empty(work, tmp_path):
    (tmp_path / "busy").mkdir()
    (tmp_path / "busy" / "file").write_text("x")
    assert run_cli(work, "prepare", "T03", "--dir", str(tmp_path / "busy"))[0] == 2


def test_the_runner_is_standalone(work):
    """The learner runs it as a script, from inside the repository, without the kit on the path."""
    env = {"PATH": "/usr/bin:/bin:/usr/local/bin", "PYTHONDONTWRITEBYTECODE": "1"}
    done = subprocess.run([sys.executable, "lab-assets/eval_runner.py", "validate"], cwd=work, env=env, capture_output=True, text=True)
    assert done.returncode == 0 and "0 problems" in done.stdout, done.stderr
    done = subprocess.run([sys.executable, "lab-assets/eval_runner.py", "--tasks", "lab-assets/tasks.example.jsonl", "baseline"],
                          cwd=work, env=env, capture_output=True, text=True)
    assert done.returncode == 0 and done.stdout.count("ok:") == 3, done.stdout + done.stderr


def test_the_course_examples_are_themselves_sound_tasks(work):
    """The three worked examples in lab-assets must pass the same discipline they teach."""
    examples = str(work / "lab-assets" / "tasks.example.jsonl")
    code, text = run_cli(work, "--tasks", examples, "baseline")
    assert code == 0 and text.count("ok:") == 3
    code, text = run_cli(work, "--tasks", examples, "verify")
    assert code == 0 and text.count("ok:") == 3


# --------------------------------------------------------------------------------------------
# results go to eval/, checks get no secrets, the worked EX2 check is fair but not weak
# --------------------------------------------------------------------------------------------
def test_score_records_in_eval_even_when_the_tasks_file_lives_elsewhere(work, tmp_path):
    """Scoring a course example must not leave lab-assets/results.jsonl behind: it would break the 'only eval/ and plan.md' check."""
    examples = work / "lab-assets" / "tasks.example.jsonl"
    ws = tmp_path / "run-EX1"
    assert run_cli(work, "--tasks", str(examples), "prepare", "EX1", "--dir", str(ws))[0] == 0
    subprocess.run(["git", "apply", str(work / "lab-assets" / "example" / "ex1-reference.patch")], cwd=ws, check=True)
    code, text = run_cli(work, "--tasks", str(examples), "score", "EX1", "--dir", str(ws), "--tool", "me", "--date", "2026-11-09")
    assert code == 0 and text.startswith("EX1: PASS") and "recorded in results.jsonl" in text
    assert not (work / "lab-assets" / "results.jsonl").exists()
    assert (work / "eval" / "results.jsonl").is_file()
    code, text = run_cli(work, "--tasks", str(examples), "report")
    assert code == 0 and "EX1" in text and "1/1" in text
    code, text = run_cli(work, "report")  # the learner's own tasks: the example's row is not counted against them
    assert code == 0 and "1/1" not in text
    assert grade_repo(work)[m13.N_SCOPE].ok  # results.jsonl is inside eval/


def test_a_check_does_not_inherit_secret_looking_environment_variables(work, monkeypatch, tmp_path):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "not-a-real-key")
    monkeypatch.setenv("MY_SERVICE_TOKEN", "not-a-real-token")
    monkeypatch.setenv("DB_PASSWORD", "not-a-real-password")
    monkeypatch.setenv("HARMLESS_SETTING", "kept")
    env = R._env(tmp_path)
    assert not {"ANTHROPIC_API_KEY", "MY_SERVICE_TOKEN", "DB_PASSWORD"} & set(env)
    assert env.get("HARMLESS_SETTING") == "kept" and "PATH" in env
    probe = tmp_path / "probe"
    probe.mkdir()
    (probe / "show.py").write_text("import os, sys\nsys.exit(0 if 'ANTHROPIC_API_KEY' not in os.environ else 1)\n", encoding="utf-8")
    assert R.run_check("python show.py", probe).passed


def _ex2_run(tmp_path: Path, answer: str | None) -> subprocess.CompletedProcess:
    """Run the worked EX2 check (the very file shown in the lesson) in a folder whose ANSWER.md has this text."""
    ws = tmp_path / "ex2"
    ws.mkdir(exist_ok=True)
    note = ws / "ANSWER.md"
    if note.exists():
        note.unlink()
    if answer is not None:
        note.write_text(answer + "\n", encoding="utf-8")
    check = m13.HERE / "assets" / "example" / "check_ex2.py"
    return subprocess.run([sys.executable, str(check)], cwd=ws, capture_output=True, text=True, timeout=20)


@pytest.mark.parametrize("answer", [
    "The express surcharge is added after the cap, so an express fee can exceed the cap.",
    "The express surcharge is added after the fee has been capped, so the express fee on large transfers is higher than the cap.",
    "Express adds a flat surcharge after capping, so large express transfers go over the cap: 165 on STD-A, not 150.",
    "The express surcharge is applied on top of the cap, so the fee can pass 150 and exceed the cap.",
])
def test_the_worked_ex2_check_accepts_correct_answers_in_different_words(tmp_path, answer):
    done = _ex2_run(tmp_path, answer)
    assert done.returncode == 0, done.stderr


@pytest.mark.parametrize("answer", [
    "TODO",                                                                                     # the kit's placeholder
    "",                                                                                         # an empty note
    "The express surcharge comes first and the cap is applied after it, so the fee never goes above the cap.",  # the reversed rule
    "Express is a flat extra charge. It does not matter for big transfers.",                    # fluent, says nothing
])
def test_the_worked_ex2_check_still_rejects_empty_and_wrong_answers(tmp_path, answer):
    done = _ex2_run(tmp_path, answer)
    assert done.returncode != 0 and "the answer does not say" in done.stderr, done.stderr


def test_the_worked_ex2_check_fails_when_there_is_no_answer_yet(tmp_path):
    done = _ex2_run(tmp_path, None)
    assert done.returncode != 0 and "FileNotFoundError" in done.stderr
