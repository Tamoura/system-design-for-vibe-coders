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
        m13.N_JSONL, m13.N_COUNT, m13.N_FIELDS, m13.N_REMIT, m13.N_RUNS, m13.N_FAILS, m13.N_GUARD, m13.N_REFS, m13.N_PLACEHOLDER, m13.N_OFFLINE,
        m13.N_SECTIONS, m13.N_START, m13.N_SKILLS, m13.N_ROUTINE, m13.N_GOALS, m13.N_SCOPE, m13.N_STEPS, m13.N_COMMITS,
    }
    assert result[m13.N_CLEAN].ok and result[m13.N_SECRETS].ok
    assert all(c.hint for c in result.values() if not c.ok), "every failing check gives a hint"
    shown = "".join(c.detail + c.hint for c in result.values())
    assert "T0" not in shown, "the grader must not leak the reference tasks"


def test_the_reference_solution_passes_every_check(work):
    result = grade_all(work)
    assert_only(result)
    assert len(result) == 28  # 16 about the eval, 7 about the plan, 5 about the repository; the names are unique


def test_the_course_template_copied_unchanged_is_not_a_plan(fresh):
    shutil.copyfile(fresh / "lab-assets" / "plan-template.md", fresh / "plan.md")
    result = grade_plan(fresh)
    assert {m13.N_SECTIONS, m13.N_START, m13.N_SKILLS, m13.N_ROUTINE, m13.N_GOALS} <= failing(result)


def test_the_examples_copied_as_the_eval_are_not_eight_tasks(fresh):
    (fresh / "eval").mkdir()
    shutil.copyfile(fresh / "lab-assets" / "tasks.example.jsonl", fresh / "eval" / "tasks.jsonl")
    result = grade_eval(fresh)
    assert result[m13.N_JSONL].ok
    assert not result[m13.N_COUNT].ok and "4 of the course's examples do not count" in result[m13.N_COUNT].detail
    assert not result[m13.N_REMIT].ok and not result[m13.N_RUNS].ok  # nothing of the learner's own to run


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
    assert not result[m13.N_COUNT].ok and "5 different tasks" in result[m13.N_COUNT].detail
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
    change(work, "T03", check={"run": run})
    result = grade_eval(work)
    assert not result[m13.N_FAILS].ok and "T03" in result[m13.N_FAILS].detail
    assert "before any work" in result[m13.N_FAILS].detail
    assert required_failures(result) <= {m13.N_FAILS, m13.N_PLACEHOLDER}  # a check that always passes also accepts a lazy edit


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
    tried = [what for what, _ in R.evaluate(work, "lab-start", task).placeholders]
    assert tried and not any("NOTES.txt" in what or "test_cli_corridors" in what for what in tried)  # only the stray edit to cli.py


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
    change(work, "T02", check={"run": run})
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


def test_a_task_without_a_reference_is_not_trusted(work):
    """A check nobody has seen pass cannot be trusted, so every task on the Remit repository needs a reference."""
    change(work, "T01", reference=None)
    result = grade_eval(work)
    assert_only(result, m13.N_REFS)
    assert "no reference for T01 (line 1)" in result[m13.N_REFS].detail
    assert "prepare" in result[m13.N_REFS].hint and "verify" in result[m13.N_REFS].hint


def test_no_references_at_all(work):
    for task in load_tasks(work):
        change(work, task["id"], reference=None)
    result = grade_eval(work)
    assert_only(result, m13.N_REFS)
    assert "no reference for" in result[m13.N_REFS].detail


def test_a_task_from_the_learners_own_project_needs_no_reference(work):
    assert "reference" not in next(t for t in load_tasks(work) if t["id"] == "T09")
    assert_only(grade_eval(work))


def test_too_few_tasks_the_kit_can_run(work):
    """Four of the eight Remit tasks moved to the learner's own project: nine tasks, but only four the kit can run."""
    for task_id in ("T04", "T05", "T06", "T07"):
        change(work, task_id, repo="own")
    result = grade_eval(work)
    assert_only(result, m13.N_REMIT)
    assert "at least 6" in result[m13.N_REMIT].detail and "4 tasks" in result[m13.N_REMIT].detail
    assert result[m13.N_COUNT].ok and result[m13.N_RUNS].ok  # not reported under the wrong name


def test_own_project_tasks_count_towards_the_eight(work):
    """Seven Remit tasks and one of your own are eight; seven Remit tasks alone are seven."""
    save_tasks(work, [t for t in load_tasks(work) if t["id"] != "T08"])
    assert_only(grade_eval(work))
    save_tasks(work, [t for t in load_tasks(work) if t["id"] != "T09"])
    result = grade_eval(work)
    assert_only(result, m13.N_COUNT, m13.N_OWN)  # N_OWN is only advisory
    assert "7 different tasks" in result[m13.N_COUNT].detail and "own project" in result[m13.N_COUNT].hint


def test_eight_copies_of_one_task_are_one_task(work):
    first = next(t for t in load_tasks(work) if t["id"] == "T01")
    save_tasks(work, [dict(first, id=f"C0{n}", title=f"Corridors command, copy {n}") for n in range(1, 9)])
    result = grade_eval(work)
    assert not result[m13.N_COUNT].ok and "1 different tasks" in result[m13.N_COUNT].detail
    assert "repeats the prompt of C01" in result[m13.N_COUNT].detail


def test_copies_with_a_reworded_prompt_but_the_same_check_and_patches_are_still_copies(work):
    first = next(t for t in load_tasks(work) if t["id"] == "T01")
    save_tasks(work, [dict(first, id=f"C0{n}", prompt=first["prompt"] + " " + "Please be careful. " * n) for n in range(1, 9)])
    result = grade_eval(work)
    assert not result[m13.N_COUNT].ok and "same check and patches as C01" in result[m13.N_COUNT].detail


def test_a_second_boundary_task_with_its_own_check_is_not_a_copy(work):
    tasks = load_tasks(work)
    t02 = next(t for t in tasks if t["id"] == "T02")
    other = dict(t02, id="T10", prompt=t02["prompt"].replace("60 seconds", "sixty seconds"), check={"run": "pytest -q eval/checks/test_t02_quote_expiry.py -k last_instant"})
    other.pop("reference")
    save_tasks(work, tasks + [other])
    assert m13.N_COUNT not in failing(grade_eval(work))


def _insert_line_patch(work: Path, text: str) -> str:
    """A patch that inserts one line near the top of docs/ARCHITECTURE.md (three lines of context on each side, so git applies it)."""
    lines = (work / "docs" / "ARCHITECTURE.md").read_text(encoding="utf-8").splitlines()
    return ("diff --git a/docs/ARCHITECTURE.md b/docs/ARCHITECTURE.md\n--- a/docs/ARCHITECTURE.md\n+++ b/docs/ARCHITECTURE.md\n"
            "@@ -1,6 +1,7 @@\n" + "".join(f" {line}\n" for line in lines[:3]) + f"+{text}\n" + "".join(f" {line}\n" for line in lines[3:6]))


@pytest.mark.parametrize("with_reference", [False, True], ids=["no-reference", "reference-does-not-help"])
def test_checks_that_can_never_pass_do_not_hide_behind_missing_references(work, with_reference):
    """Six of the checks replaced by `exit 1`: they fail on the untouched repo, which is all `baseline` asks."""
    for task_id in ("T01", "T02", "T03", "T04", "T05", "T06"):
        fields = {"check": {"run": 'python -c "import sys; sys.exit(1)"'}}
        if not with_reference:
            fields["reference"] = None
        change(work, task_id, **fields)
    result = grade_eval(work)
    assert not result[m13.N_REFS].ok
    assert ("no reference for T01" if not with_reference else "still fails after the reference") in result[m13.N_REFS].detail


@pytest.mark.parametrize("kind", ["docs", "other", "fix"])
def test_a_one_word_reference_does_not_make_a_docs_check_trustworthy(work, kind):
    """A docs task checked by `grep -q reviewed docs/ARCHITECTURE.md`, 'solved' by appending the word."""
    write(work, "eval/reference/T10.patch", _insert_line_patch(work, "reviewed"))
    task = {"id": "T10", "title": "Review the architecture page", "kind": kind,
            "prompt": "Read docs/ARCHITECTURE.md and the code in src/remit and bring the page up to date, so that every statement it makes is true today. Change nothing else.",
            "check": {"run": "grep -q reviewed docs/ARCHITECTURE.md"}, "reference": "eval/reference/T10.patch"}
    save_tasks(work, load_tasks(work) + [task])
    result = grade_eval(work)
    assert not result[m13.N_REFS].ok
    assert "T10" in result[m13.N_REFS].detail and "changes only 1 word:" in result[m13.N_REFS].detail


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
    save_tasks(work, [t for t in load_tasks(work) if t["id"] != "T09"])  # eight tasks on this repository, none from the learner's project
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


@pytest.mark.parametrize("line, expected", [("", "no line"), ("Start date: next Monday", "not a date I can read"), ("Start date: 2026-13-45", "not a real date")])
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
        ("| 2026-12-15 |", "| end of the quarter |", "not a full date"),
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


def test_a_missing_start_date_is_reported_once_not_on_every_goal(work):
    plan_replace(work, "Start date: 2026-11-02", "")
    result = grade_plan(work)
    assert_only(result, m13.N_START)  # the goals are fine; their dates are checked once the start date is fixed


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
     "check": {"run": 'grep -q "T3" docs/ARCHITECTURE.md'}, "reference": "eval/reference/T07.patch"},
    {"id": "A5", "title": "Smaller send", "kind": "refactor",
     "prompt": "Split RemitService.send into smaller private methods so that no function in service.py is longer than seventy lines. Behaviour, messages and the order of the steps must not change, and no test may be edited.",
     "check": {"run": 'python -c "import ast, pathlib; tree = ast.parse(pathlib.Path(\'src/remit/service.py\').read_text()); assert all(n.end_lineno - n.lineno + 1 <= 70 for n in ast.walk(tree) if isinstance(n, ast.FunctionDef))"',
               "guard": "pytest -q tests/test_config_cli.py"}, "reference": "eval/reference/T06.patch"},
    {"id": "A6", "title": "Explain the monthly limit", "kind": "explain",
     "prompt": "Which module decides whether a transfer is over the monthly limit, and which function does it? Write the answer in ANSWER.md in two sentences naming both. Change nothing else.",
     "check": {"run": 'grep -q "check_limits" ANSWER.md'}, "reference": "eval/reference/A6.patch"},
    {"id": "A7", "title": "Tests for the partner share", "kind": "test",
     "prompt": "Write tests in tests/test_ledger_partner_share.py that prove the ledger rounds the partner's share of the fee half-even. They must pass on today's code and fail if the share were rounded half up instead.",
     "check": {"run": "python eval/checks/check_t05_tests_bite.py"}, "reference": "eval/reference/T05.patch"},
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
    """Fewer guards, grep and python -c checks, shared references, columns in another order, en-dash headings, other titles."""
    solved_dir = fresh.parent / "reference"
    shutil.copytree(fresh, solved_dir)
    framework.solve_lab(framework.load_lab("m13"), solved_dir)
    # take the pieces we reuse from the reference solution, then rebuild the eval from scratch around them
    eval_dir = fresh / "eval"
    for sub in ("checks", "reference", "setup"):
        shutil.copytree(solved_dir / "eval" / sub, eval_dir / sub)
    save_tasks(fresh, ALT_TASKS)
    write(fresh, "eval/reference/A6.patch",
          "diff --git a/ANSWER.md b/ANSWER.md\nnew file mode 100644\n--- /dev/null\n+++ b/ANSWER.md\n@@ -0,0 +1,2 @@\n"
          "+The limits module decides whether a transfer is over the monthly limit.\n"
          "+The function that does it is check_limits, which compares the month's total with the tier's monthly limit.\n")
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
        ("pytest -q eval\\checks\\test_x.py", False), ("python eval\\checks\\check.py", False), ('python -c "print(1)"', True),
        ("python -c \"print('a\\\\nb')\"", True),
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
        (["pytest", "-q", "x.py"], 1, "", "/usr/bin/python: No module named pytest", "broken"),
        (["python", "-m", "pytest", "x.py"], 1, "", "/usr/bin/python3: No module named pytest", "broken"),
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
    assert R.patch_files(patch) == (["ANSWER.md", "tests/test_new.py"], ["src/a.py"])
    gone = "diff --git a/old.md b/old.md\ndeleted file mode 100644\n--- a/old.md\n+++ /dev/null\n@@ -1 +0,0 @@\n-bye\n"
    assert R.patch_files(gone) == ([], []) and R.changed_words(gone) == 1
    assert R.changed_words(patch) == 3  # the added x, the removed a and the added b are one word each; headers do not count



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
    assert "FAILED eval/checks/test_t03_search_is_safe.py::test_" in text  # baseline says why a check fails, not only that it does
    assert "FileNotFoundError" in text  # T04 reads ANSWER.md, which does not exist yet
    code, text = run_cli(work, "verify")
    assert code == 0 and "lazy answer" in text and text.count("ok:") == 8
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


def test_verify_asks_for_a_reference_on_every_task(work):
    change(work, "T05", reference=None)
    code, text = run_cli(work, "verify")
    assert code == 1 and "T05" in text and "MISSING" in text and "needs a `reference`" in text


def test_verify_says_when_no_lazy_answer_could_be_tried(work):
    """A reference that only creates a file of a kind the kit cannot fake: the learner is told that no probe applied."""
    write(work, "eval/reference/T10.patch",
          "diff --git a/data/rates.bin b/data/rates.bin\nnew file mode 100644\n--- /dev/null\n+++ b/data/rates.bin\n@@ -0,0 +1 @@\n+rates\n")
    task = {"id": "T10", "title": "Add the rates file", "kind": "other",
            "prompt": "Create the file data/rates.bin with the agreed exchange rates in it, one per line, and change nothing else in the repository at all.",
            "check": {"run": 'python -c "import pathlib; assert pathlib.Path(\'data/rates.bin\').is_file()"'}, "reference": "eval/reference/T10.patch"}
    save_tasks(work, load_tasks(work) + [task])
    code, text = run_cli(work, "verify")
    assert code == 0 and "ok: the reference passes; no lazy-answer probe applied" in text


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
    assert done.returncode == 0 and done.stdout.count("ok:") == 4, done.stdout + done.stderr


def test_the_course_examples_are_themselves_sound_tasks(work):
    """The four worked examples in lab-assets must pass the same discipline they teach."""
    examples = str(work / "lab-assets" / "tasks.example.jsonl")
    code, text = run_cli(work, "--tasks", examples, "baseline")
    assert code == 0 and text.count("ok:") == 4
    code, text = run_cli(work, "--tasks", examples, "verify")
    assert code == 0 and text.count("ok:") == 4


# --------------------------------------------------------------------------------------------
# git inside a workspace; the worked "write tests" example; a setup patch that is not there yet
# --------------------------------------------------------------------------------------------
def test_a_git_guard_sees_what_a_solution_changed(work):
    """Every workspace is a repository with one commit, so `git diff` is a usable guard: 'do not edit the tests'."""
    change(work, "T02", check={"run": "pytest -q eval/checks/test_t02_quote_expiry.py", "guard": "git diff --quiet -- tests"})
    assert_only(grade_eval(work))


def test_a_tool_that_edits_the_tests_fails_a_git_guard_even_if_it_commits(work, tmp_path):
    change(work, "T02", check={"run": "pytest -q eval/checks/test_t02_quote_expiry.py", "guard": "git diff --quiet -- tests"})
    ws = tmp_path / "run-T02"
    assert run_cli(work, "prepare", "T02", "--dir", str(ws))[0] == 0
    subprocess.run(["git", "apply", str(work / "eval" / "reference" / "T02.patch")], cwd=ws, check=True)
    code, text = run_cli(work, "score", "T02", "--dir", str(ws), "--tool", "me", "--no-record")
    assert code == 0 and text.startswith("T02: PASS"), text  # the honest fix

    with (ws / "tests" / "test_fx.py").open("a", encoding="utf-8") as handle:
        handle.write("\n# loosened by the tool\n")
    gitutil.git(ws, "-c", "user.name=tool", "-c", "user.email=tool@example.invalid", "commit", "-qam", "tool: fix and tidy the tests")
    code, text = run_cli(work, "score", "T02", "--dir", str(ws), "--tool", "cheater", "--no-record")
    assert code == 1 and "guard" in text, text  # committing does not hide the edit


def test_baseline_and_verify_run_in_a_repository_with_one_commit(work):
    change(work, "T02", check={"run": "git log --oneline", "guard": "git diff --quiet"}, reference=None)
    task = next(t for t in load_tasks(work) if t["id"] == "T02")
    report = R.evaluate(work, "lab-start", task, run_reference=False)
    assert report.baseline.passed and report.guard_baseline.passed  # `git log` works: a commit exists; nothing is changed yet


def test_a_missing_setup_patch_says_how_to_make_one(work, tmp_path):
    task = next(t for t in load_tasks(work) if t["id"] == "T02")
    (work / "eval" / "setup" / "T02.patch").unlink()
    with pytest.raises(R.RunnerError) as caught:
        R.make_workspace(work, "lab-start", task, tmp_path / "ws")
    assert "does not exist yet" in str(caught.value) and "Leave `setup` out" in str(caught.value)
    assert run_cli(work, "prepare", "T02", "--dir", str(tmp_path / "ws2"))[0] == 2


def _ex4(work: Path, tmp_path: Path, tests_text: str | None):
    """The worked 'write tests' check, run in a clean copy where the tool wrote ``tests_text``."""
    examples, _ = R.load_tasks(work / "lab-assets" / "tasks.example.jsonl")
    task = next(t for t in examples if t["id"] == "EX4")
    ws = tmp_path / "ws"
    R.make_workspace(work, "lab-start", task, ws)
    if tests_text is not None:
        (ws / "tests" / "test_fees_express_cap.py").write_text(tests_text, encoding="utf-8")
    return R.run_check(task["check"]["run"], ws)


EX4_REAL = (
    "from remit.corridors import get_corridor\nfrom remit.fees import quote_fee\nfrom remit.money import Money\n\n"
    "def test_express_is_added_after_the_cap():\n"
    "    assert quote_fee(Money('15000.00', 'QAR'), get_corridor('QAR', 'INR'), express=True) == Money('165.00', 'QAR')\n"
)


def test_the_worked_write_tests_check_accepts_tests_that_pin_the_rule(work, tmp_path):
    assert _ex4(work, tmp_path, EX4_REAL).passed


@pytest.mark.parametrize("text, expected", [
    (None, "does not exist yet"),
    ("def test_nothing():\n    assert True\n", "do not pin it down"),
    ("from remit.corridors import get_corridor\nfrom remit.fees import quote_fee\nfrom remit.money import Money\n\n"
     "def test_cap():\n    assert quote_fee(Money('15000.00', 'QAR'), get_corridor('QAR', 'INR')) == Money('150.00', 'QAR')\n", "do not pin it down"),
    (EX4_REAL.replace("165.00", "166.00"), "must pass on the real code"),
], ids=["no-file", "asserts-nothing", "tests-another-rule", "wrong-expectation"])
def test_the_worked_write_tests_check_rejects_tests_that_cannot_notice(work, tmp_path, text, expected):
    outcome = _ex4(work, tmp_path, text)
    assert outcome.verdict == "fail" and expected in outcome.detail, outcome


# --------------------------------------------------------------------------------------------
# lazy answers: every way of saying nothing, in every kind of file
# --------------------------------------------------------------------------------------------
def _answer_task(work: Path, filename: str, run: str, *, task_id: str = "T10", prompt: str | None = None) -> dict:
    """T04's explain task, but asking for ``filename`` (its reference patch rewritten to create that file), checked by ``run``."""
    patch = (work / "eval" / "reference" / "T04.patch").read_text(encoding="utf-8").replace("ANSWER.md", filename)
    write(work, f"eval/reference/{task_id}.patch", patch)
    task = {"id": task_id, "title": "Explain the failed save", "kind": "explain",
            "prompt": prompt or f"Read RemitService.send. If store.save_transfer raises, what happens to the ledger postings that were already made? Answer in {filename} in the repository root and change no other file.",
            "check": {"run": run}, "reference": f"eval/reference/{task_id}.patch"}
    save_tasks(work, [t for t in load_tasks(work) if t["id"] != "T04"] + [task])
    return task


@pytest.mark.parametrize("filename", ["ANSWER.markdown", "ANSWER.json", "notes/answer.yaml", "answer.csv", "ANSWER"])
def test_an_existence_check_is_weak_whatever_the_file_is_called(work, filename):
    """The probe used to look only at .md, .txt, .rst and no suffix; a .markdown or .json answer slipped through."""
    _answer_task(work, filename, f"python -c \"import pathlib; assert pathlib.Path('{filename}').exists()\"")
    result = grade_eval(work)
    assert_only(result, m13.N_PLACEHOLDER)
    assert filename in result[m13.N_PLACEHOLDER].detail


def test_a_new_module_that_only_has_to_import_is_weak(work):
    patch = ("diff --git a/src/remit/corridor_table.py b/src/remit/corridor_table.py\nnew file mode 100644\n--- /dev/null\n"
             "+++ b/src/remit/corridor_table.py\n@@ -0,0 +1,2 @@\n+def rows():\n+    return []\n")
    write(work, "eval/reference/T10.patch", patch)
    task = {"id": "T10", "title": "A corridor table module", "kind": "feature",
            "prompt": "Create a module remit.corridor_table with a function rows that returns the supported corridors as a list of tuples sorted by code. Do not change any other module.",
            "check": {"run": 'python -c "import remit.corridor_table"'}, "reference": "eval/reference/T10.patch"}
    save_tasks(work, load_tasks(work) + [task])
    result = grade_eval(work)
    assert_only(result, m13.N_PLACEHOLDER)
    assert "an empty module in src/remit/corridor_table.py" in result[m13.N_PLACEHOLDER].detail


def test_a_word_count_check_accepts_filler(work):
    """`len(answer.split()) >= 3` rejects the kit's 'TODO' and accepts any three words, which is not a check."""
    _answer_task(work, "ANSWER.md", 'python -c "import pathlib; assert len(pathlib.Path(\'ANSWER.md\').read_text().split()) >= 3"')
    result = grade_eval(work)
    assert_only(result, m13.N_PLACEHOLDER)
    assert "filler text in ANSWER.md" in result[m13.N_PLACEHOLDER].detail
    assert "a placeholder in ANSWER.md" not in result[m13.N_PLACEHOLDER].detail  # 'TODO' alone is rejected by this check


def test_a_check_that_the_prompt_copied_back_satisfies_is_weak(work):
    """The words of the check are in the prompt, so a tool that hands the question back passes."""
    _answer_task(work, "ANSWER.md", 'grep -q "already" ANSWER.md')
    result = grade_eval(work)
    assert_only(result, m13.N_PLACEHOLDER)
    assert "the prompt copied back in ANSWER.md" in result[m13.N_PLACEHOLDER].detail


def test_a_stray_edit_that_satisfies_the_check_is_weak(work):
    """A docs task checked by 'the file mentions the T3 tier' where the file already does, plus a stray TODO line."""
    assert "TODO" not in (work / "docs" / "ARCHITECTURE.md").read_text(encoding="utf-8")
    write(work, "eval/reference/T10.patch", _insert_line_patch(work, "TODO bring this page up to date later on"))
    task = {"id": "T10", "title": "Bring the page up to date", "kind": "docs",
            "prompt": "Compare docs/ARCHITECTURE.md with the code in src/remit and correct every statement that is no longer true. Change documentation only, nothing else at all.",
            "check": {"run": 'grep -q "TODO" docs/ARCHITECTURE.md'}, "reference": "eval/reference/T10.patch"}
    save_tasks(work, load_tasks(work) + [task])
    result = grade_eval(work)
    assert not result[m13.N_PLACEHOLDER].ok and "a stray line in docs/ARCHITECTURE.md" in result[m13.N_PLACEHOLDER].detail


def test_the_lazy_answers_a_real_check_rejects(tmp_path):
    answers = R.lazy_answers("ANSWER.md", "Explain the cap.")
    assert [what for what, _ in answers] == ["a placeholder", "filler text", "the prompt copied back"]
    assert len(answers[1][1].split()) > 50 and answers[2][1] == "Explain the cap.\n"
    assert [what for what, _ in R.lazy_answers("tests/test_new.py")] == ["a test that asserts nothing"]
    assert [what for what, _ in R.lazy_answers("src/remit/x.py")] == ["an empty module"]
    assert [what for what, _ in R.lazy_answers("data/a.json")] == ["an empty JSON object"]
    assert R.lazy_answers("logo.png") == []


# --------------------------------------------------------------------------------------------
# the plan: forms that are sound must be accepted
# --------------------------------------------------------------------------------------------
@pytest.mark.parametrize("written", ["2026-11-02", "2026/11/02", "2 November 2026", "2nd Nov 2026", "November 2, 2026", "**2 November 2026**",
                                      "2026-11-02 (a Monday)", "Monday 2 November 2026"])
def test_a_start_date_may_be_written_in_any_unambiguous_form(work, written):
    plan_replace(work, "Start date: 2026-11-02", f"Start date: {written}")
    assert_only(grade_plan(work))


def test_goal_dates_may_be_written_out_too(work):
    plan_replace(work, "| 2026-12-15 |", "| 15 December 2026 |")
    plan_replace(work, "| 2026-12-31 |", "| Dec 31, 2026 (end of year) |")
    plan_replace(work, "| 2027-01-15 |", "| 2027-01-15 (a Friday) |")
    assert_only(grade_plan(work))


@pytest.mark.parametrize("written", ["02/11/2026", "next Monday", "end of the quarter", "2026-13-45"])
def test_a_date_that_is_not_one_is_still_rejected(work, written):
    plan_replace(work, "Start date: 2026-11-02", f"Start date: {written}")
    assert not grade_plan(work)[m13.N_START].ok


@pytest.mark.parametrize("target", ["four flows", "all four traces", "Twice a week", "10 of 10", "90%"])
def test_a_target_may_be_a_number_in_words(work, target):
    plan_replace(work, "| 6 | 2026-12-15 |", f"| {target} | 2026-12-15 |")
    assert_only(grade_plan(work))


@pytest.mark.parametrize("target", ["more", "all of them", "better"])
def test_a_target_with_no_number_in_it_is_still_rejected(work, target):
    plan_replace(work, "| 6 | 2026-12-15 |", f"| {target} | 2026-12-15 |")
    assert "no number" in grade_plan(work)[m13.N_GOALS].detail


@pytest.mark.parametrize("minutes", ["1 hour", "1.5 h", "half an hour", "~45 min", "30-45", "an hour"])
def test_a_duration_may_be_written_as_people_write_it(work, minutes):
    plan_replace(work, "| Monday | One kata without the agent, then the agent as a tutor for hints only | 45 |",
                 f"| Monday | One kata without the agent, then the agent as a tutor for hints only | {minutes} |")
    assert_only(grade_plan(work))


def test_a_thin_section_says_how_long_it_should_be(work):
    text = (work / "plan.md").read_text(encoding="utf-8")
    start, end = text.index("## Days 31-60"), text.index("## Days 61-90")
    write(work, "plan.md", text[:start] + "## Days 31-60\n\nKeep going.\n\n" + text[end:])
    assert "Days 31-60 (12+ words)" in grade_plan(work)[m13.N_SECTIONS].detail


# --------------------------------------------------------------------------------------------
# the repository: the score log is not work to commit
# --------------------------------------------------------------------------------------------
def test_the_results_log_written_by_score_may_stay_uncommitted(work):
    """`score` appends to eval/results.jsonl; following the lesson and grading must not give 'NOT YET' for it."""
    write(work, "eval/results.jsonl", '{"task": "T03", "tool": "me", "passed": true}\n')
    result = grade_all(work)
    assert required_failures(result) == set(), {n: c.detail for n, c in result.items() if not c.ok and c.required}


def test_other_uncommitted_files_in_eval_still_count(work):
    write(work, "eval/results.jsonl", '{"task": "T03", "tool": "me", "passed": true}\n')
    write(work, "eval/notes.md", "scratch\n")
    result = grade_repo(work)
    assert_only(result, m13.N_CLEAN)
    assert "notes.md" in result[m13.N_CLEAN].detail and "results.jsonl" not in result[m13.N_CLEAN].detail


# --------------------------------------------------------------------------------------------
# a timeout is not a typo; the hint must say which
# --------------------------------------------------------------------------------------------
def test_a_timeout_gets_a_timeout_hint_not_the_allow_list(work, monkeypatch):
    monkeypatch.setattr(m13, "GRADER_TIMEOUT", 2.0)
    change(work, "T06", check={"run": 'python -c "import time; time.sleep(60)"'}, reference=None)
    hint = grade_eval(work)[m13.N_RUNS].hint
    assert "time limit" in hint and "Allowed commands" not in hint


def test_a_disallowed_command_gets_the_allow_list_hint(work):
    change(work, "T08", check={"run": "npm test"}, reference=None)
    hint = grade_eval(work)[m13.N_RUNS].hint
    assert "Allowed commands" in hint and "time limit" not in hint


def test_the_grader_and_the_runner_share_one_generous_time_limit():
    assert m13.GRADER_TIMEOUT == 60.0 and R.TIMEOUT == 60.0


# --------------------------------------------------------------------------------------------
# the lesson and the kit say the same thing
# --------------------------------------------------------------------------------------------
LESSON = Path(__file__).resolve().parents[2] / "modules" / "13-sharp.md"


def _lesson_blocks() -> list[tuple[str, str]]:
    import re
    text = LESSON.read_text(encoding="utf-8")
    return [(m.group(1), m.group(2)) for m in re.finditer(r"```(\w*)[^\n]*\n(.*?)```", text, flags=re.S)]


@pytest.mark.skipif(not LESSON.is_file(), reason="the lesson is not next to the kit")
def test_the_ticket_in_the_lesson_is_the_task_file():
    ticket = (m13.HERE / "task.md").read_text(encoding="utf-8").rstrip("\n")
    assert any(body.rstrip("\n") == ticket for _, body in _lesson_blocks()), "the lesson's ticket block differs from task.md"


@pytest.mark.skipif(not LESSON.is_file(), reason="the lesson is not next to the kit")
def test_the_worked_check_in_the_lesson_is_the_learners_file():
    """The block starts with the path the learner sees, `lab-assets/example/check_ex2.py`, not a path in the course repository."""
    shown = [body for lang, body in _lesson_blocks() if lang == "python" and body.startswith("# lab-assets/example/check_ex2.py")]
    assert len(shown) == 1
    assert shown[0].rstrip("\n") == (m13.HERE / "assets" / "example" / "check_ex2.py").read_text(encoding="utf-8").rstrip("\n")


@pytest.mark.skipif(not LESSON.is_file(), reason="the lesson is not next to the kit")
def test_every_check_named_in_the_lessons_sample_output_exists():
    """If a check is renamed, the sample output in the lesson goes stale: every `[FAIL] name:` line must name a real check."""
    import re
    known = {getattr(m13, n) for n in dir(m13) if n.startswith("N_")}
    lines = [line for _, body in _lesson_blocks() for line in body.splitlines() if line.startswith("[FAIL] ")]
    assert lines, "the lesson shows no sample failures"
    for line in lines:
        name = re.match(r"\[FAIL\] (.+?)(?: \(advisory\))?: ", line).group(1)
        assert name in known, f"the lesson shows a check that no longer exists: {name}"


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
