"""Tests for the framework: Check/Lab, tolerant discovery, start/grade/solve, gitutil and runner."""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from ailab import framework, gitutil, runner
from ailab.framework import Check, Lab, LabError
from conftest import GOOD_LAB, LEARNER, TASK, learner_commit, make_lab, run_cli, start

# =============================================================================
# Check and Lab
# =============================================================================


def test_check_defaults():
    check = Check("name", True)
    assert (check.detail, check.hint, check.required) == ("", "", True)


def test_passed_only_looks_at_required_checks():
    assert framework.passed([Check("a", True), Check("b", False, required=False)])
    assert not framework.passed([Check("a", True), Check("b", False)])
    assert framework.passed([])  # nothing required, nothing failed (grade_lab never returns [])


def test_lab_locates_its_files_next_to_lab_py(tmp_path):
    (tmp_path / "assets").mkdir()
    lab = Lab("m97", "t", "9.9", False, lambda w: None, lambda w: [], lambda w: None, home=tmp_path)
    assert lab.task_file == tmp_path / "task.md"
    assert lab.assets_dir == tmp_path / "assets"
    assert lab.solution_dir == tmp_path / "solution" and lab.hidden_dir == tmp_path / "hidden"
    assert Lab("m97", "t", "9.9", False, lambda w: None, lambda w: [], lambda w: None, home=tmp_path / "x").assets_dir is None
    with pytest.raises(LabError):
        Lab("m97", "t", "9.9", False, lambda w: None, lambda w: [], lambda w: None).task_file


# =============================================================================
# Discovery: tolerant, folder-name based
# =============================================================================
def test_a_broken_lab_never_hides_the_others(fake_labs):
    make_lab(fake_labs, "m91_good", GOOD_LAB.format(id="m91"))
    make_lab(fake_labs, "m92_syntax", "def broken(:\n")
    make_lab(fake_labs, "m93_import", "import module_that_does_not_exist_anywhere\nLAB = None\n")
    make_lab(fake_labs, "m94_wrong_id", GOOD_LAB.format(id="m99"))
    make_lab(fake_labs, "m95_no_lab", "x = 1\n")
    make_lab(fake_labs, "m96_no_task", GOOD_LAB.format(id="m96"), task=None)
    make_lab(fake_labs, "m97_no_file", None)
    make_lab(fake_labs, "m98_exits", "raise SystemExit(3)\n")
    (fake_labs / "not_a_lab").mkdir()
    (fake_labs / "__pycache__").mkdir()

    entries = {e.id: e for e in framework.discover()}
    assert sorted(entries) == ["m91", "m92", "m93", "m94", "m95", "m96", "m97", "m98"]
    assert not entries["m91"].broken and entries["m91"].lab.home == fake_labs / "m91_good"
    assert "SyntaxError" in entries["m92"].error
    assert "module_that_does_not_exist_anywhere" in entries["m93"].error
    assert "m99" in entries["m94"].error and "m94" in entries["m94"].error
    assert "LAB" in entries["m95"].error
    assert "task.md" in entries["m96"].error
    assert "lab.py is missing" in entries["m97"].error
    assert "SystemExit" in entries["m98"].error


def test_only_the_requested_lab_is_loaded(fake_labs):
    make_lab(fake_labs, "m91_good", GOOD_LAB.format(id="m91"))
    make_lab(fake_labs, "m92_syntax", "def broken(:\n")
    assert framework.load_lab("m91").title == "Fake lab"
    assert "ailab.labs.m92_syntax.lab" not in sys.modules  # never imported
    with pytest.raises(LabError, match="BROKEN"):
        framework.load_lab("m92")
    with pytest.raises(LabError, match="no lab"):
        framework.load_lab("m50")


def test_the_cli_survives_broken_labs(fake_labs, work_dir):
    make_lab(fake_labs, "m91_good", GOOD_LAB.format(id="m91"))
    make_lab(fake_labs, "m92_syntax", "def broken(:\n")
    code, out, _ = run_cli("list")
    assert code == 0
    assert "m91" in out and "Fake lab" in out
    assert "BROKEN (m92_syntax)" in out and "SyntaxError" in out
    code, out, _ = run_cli("list", "--json")
    assert [(r["id"], r["broken"]) for r in __import__("json").loads(out)] == [("m91", False), ("m92", True)]
    assert run_cli("start", "m91", "--dir", str(work_dir))[0] == 0
    code, _, err = run_cli("start", "m92", "--dir", str(work_dir.parent / "other"))
    assert code == 2 and "BROKEN" in err


def test_ids_are_normalised_and_found_by_folder(fake_labs):
    make_lab(fake_labs, "m05_review", GOOD_LAB.format(id="m05"))
    for spelling in ("m05", "M05", "m5", "5", "05", "m05_review", " m05 "):
        assert framework.find_dirname(spelling) == "m05_review"
    with pytest.raises(LabError, match="Labs found: m05"):
        framework.find_dirname("m06")


def test_two_folders_for_one_id_are_an_error(fake_labs):
    make_lab(fake_labs, "m05_a", GOOD_LAB.format(id="m05"))
    make_lab(fake_labs, "m05_b", GOOD_LAB.format(id="m05"))
    with pytest.raises(LabError, match="more than one"):
        framework.find_dirname("m05")


def test_a_lab_can_be_fixed_and_reloaded_in_the_same_process(fake_labs):
    make_lab(fake_labs, "m91_wip", "def broken(:\n")
    assert framework.discover()[0].broken
    (fake_labs / "m91_wip" / "lab.py").write_text(GOOD_LAB.format(id="m91"), encoding="utf-8")
    assert not framework.discover()[0].broken


# =============================================================================
# Lifecycle with a fake lab
# =============================================================================
def test_start_grade_solve_with_a_fake_lab(fake_labs, work_dir):
    make_lab(fake_labs, "m91_good", GOOD_LAB.format(id="m91"))
    (fake_labs / "m91_good" / "assets").mkdir()
    (fake_labs / "m91_good" / "assets" / "notes.txt").write_text("asset\n")
    (fake_labs / "m91_good" / "solution").mkdir()
    lab = framework.load_lab("m91")
    work = framework.start_lab(lab, work_dir)

    assert (work / "seeded.txt").read_text() == "seeded\n"
    assert (work / "lab-assets" / "notes.txt").read_text() == "asset\n"
    assert (work / "TASK.md").read_text() == TASK
    assert gitutil.out(work, "log", "--format=%s", "--reverse").splitlines() == ["Initial state", "Lab starting state"]
    assert gitutil.rev_parse(work, "lab-start") == gitutil.head(work)
    assert gitutil.out(work, "show", "--stat", "--format=", "HEAD").count("seeded.txt") == 1  # seed is in commit 2
    assert gitutil.is_clean(work, ignore=())
    assert not any(p.name == "__pycache__" for p in work.rglob("*"))

    checks = framework.grade_lab(lab, work)
    assert [(c.name, c.ok) for c in checks] == [("seeded file removed", False)]
    assert not framework.passed(checks)
    framework.solve_lab(lab, work)
    assert framework.passed(framework.grade_lab(lab, work))


def test_start_refuses_a_directory_that_is_not_empty(fake_labs, tmp_path):
    make_lab(fake_labs, "m91_good", GOOD_LAB.format(id="m91"))
    target = tmp_path / "occupied"
    target.mkdir()
    (target / "mine.txt").write_text("keep me")
    with pytest.raises(LabError, match="not empty"):
        framework.start_lab(framework.load_lab("m91"), target)
    assert (target / "mine.txt").read_text() == "keep me"
    empty = tmp_path / "empty"
    empty.mkdir()
    framework.start_lab(framework.load_lab("m91"), empty)  # an empty directory is fine
    assert (empty / ".git").is_dir()


def test_a_failing_seed_leaves_nothing_behind(fake_labs, tmp_path):
    make_lab(fake_labs, "m91_bad_seed", GOOD_LAB.format(id="m91").replace('"seeded\\\\n"', '"x"').replace(
        "def seed(work):", "def seed(work):\n    raise RuntimeError('seed blew up')\n"))
    lab = framework.load_lab("m91")
    target = tmp_path / "work"
    with pytest.raises(RuntimeError, match="seed blew up"):
        framework.start_lab(lab, target)
    assert not target.exists()
    existing = tmp_path / "existing"
    existing.mkdir()
    with pytest.raises(RuntimeError):
        framework.start_lab(lab, existing)
    assert existing.is_dir() and list(existing.iterdir()) == []


def test_a_crashing_grader_becomes_a_failing_check(fake_labs, work_dir):
    make_lab(fake_labs, "m91_good", GOOD_LAB.format(id="m91").replace("return [Check(", "raise ValueError('oops')\n    return [Check("))
    lab = framework.load_lab("m91")
    work = framework.start_lab(lab, work_dir)
    (check,) = framework.grade_lab(lab, work)
    assert not check.ok and "ValueError: oops" in check.detail and "bug in the lab" in check.hint
    with pytest.raises(ValueError):
        framework.grade_lab(lab, work, catch=False)


def test_grading_a_directory_that_is_not_a_lab_is_an_error(tmp_path):
    with pytest.raises(LabError, match="not a directory"):
        framework.check_work_dir(tmp_path / "missing")
    with pytest.raises(LabError, match="was not created"):
        framework.check_work_dir(tmp_path)


def test_solve_refuses_after_changes_unless_forced(work_dir):
    lab = framework.load_lab("m00")
    work = start("m00", work_dir)
    (work / "notes.txt").write_text("my own work\n")
    with pytest.raises(LabError, match="--force"):
        framework.solve_lab(lab, work)
    framework.solve_lab(lab, work, force=True)
    assert framework.passed(framework.grade_lab(lab, work)) is False  # the extra file makes m00 fail its scope checks


# =============================================================================
# Seed helpers and reference memory
# =============================================================================
def test_edit_file_insists_on_an_exact_match(tmp_path):
    framework.write_file(tmp_path, "pkg/a.txt", "one two two\n")
    framework.edit_file(tmp_path, "pkg/a.txt", "one", "1")
    assert framework.read_file(tmp_path, "pkg/a.txt") == "1 two two\n"
    with pytest.raises(LabError, match="found 2"):
        framework.edit_file(tmp_path, "pkg/a.txt", "two", "2")
    framework.edit_file(tmp_path, "pkg/a.txt", "two", "2", count=2)
    with pytest.raises(LabError, match="found 0"):
        framework.edit_file(tmp_path, "pkg/a.txt", "absent", "x")
    framework.remove_file(tmp_path, "pkg/a.txt")
    assert not (tmp_path / "pkg" / "a.txt").exists()


def test_reference_memory_is_a_no_op_without_an_m02_solution(fake_labs, tmp_path):
    assert framework.add_reference_memory(tmp_path) is False
    assert not (tmp_path / "CLAUDE.md").exists()
    make_lab(fake_labs, "m02_memory", GOOD_LAB.format(id="m02"))
    assert framework.add_reference_memory(tmp_path) is False  # lab exists, solution/CLAUDE.md does not
    (fake_labs / "m02_memory" / "solution").mkdir()
    (fake_labs / "m02_memory" / "solution" / "CLAUDE.md").write_text("# Memory\n")
    assert framework.add_reference_memory(tmp_path) is True
    assert (tmp_path / "CLAUDE.md").read_text() == "# Memory\n"


def test_doctor_checks_report_the_environment(tmp_path):
    checks = {c.name: c for c in framework.doctor_checks(tmp_path)}
    assert checks["Python 3.11 or newer"].ok and checks["git is installed"].ok and checks["pytest can be imported"].ok
    assert checks["working directory is writable"].ok and checks["lab kit is complete"].ok
    assert not checks["git knows who you are (needed to commit)"].required  # advisory
    blocker = tmp_path / "file"
    blocker.write_text("x")
    bad = {c.name: c for c in framework.doctor_checks(blocker / "sub")}
    assert not bad["working directory is writable"].ok
    assert not (blocker / "sub").exists()  # doctor never creates the directory


# =============================================================================
# gitutil
# =============================================================================
@pytest.fixture
def repo(tmp_path):
    path = tmp_path / "repo"
    path.mkdir()
    gitutil.init_repo(path)
    (path / "a.txt").write_text("one\ntwo\nthree\n")
    (path / "keep.txt").write_text("keep\n")
    gitutil.commit_all(path, "Initial state")
    gitutil.tag(path, "lab-start")
    return path


def test_init_uses_main_and_kit_commits_are_reproducible(tmp_path):
    shas = []
    for name in ("one", "two"):
        path = tmp_path / name
        path.mkdir()
        gitutil.init_repo(path)
        (path / "f.txt").write_text("same\n")
        shas.append(gitutil.commit_all(path, "Initial state"))
        assert gitutil.current_branch(path) == "main"
    assert shas[0] == shas[1]  # fixed author, date and content give the same commit


def test_changed_files_sees_committed_staged_unstaged_untracked_and_deleted(repo):
    assert gitutil.changed_files(repo) == []
    (repo / "a.txt").write_text("one\nTWO\nthree\n")  # modified, unstaged
    (repo / "new.txt").write_text("hello\n")  # untracked
    (repo / "keep.txt").unlink()  # deleted
    (repo / "staged.txt").write_text("s\n")
    gitutil.git(repo, "add", "staged.txt")
    assert gitutil.changed_status(repo) == {"a.txt": "M", "keep.txt": "D", "new.txt": "A", "staged.txt": "A"}
    learner_commit(repo, "fix(x): all")
    assert gitutil.changed_files(repo) == ["a.txt", "keep.txt", "new.txt", "staged.txt"]  # still "since the start"


def test_a_file_added_and_removed_again_is_not_a_change(repo):
    (repo / "tmp.txt").write_text("x\n")
    learner_commit(repo, "chore(x): add")
    gitutil.git(repo, "rm", "-q", "tmp.txt")
    learner_commit(repo, "chore(x): remove")
    assert gitutil.changed_files(repo) == []


def test_tool_noise_is_ignored_by_default(repo):
    for rel in (".claude/settings.local.json", ".DS_Store", "pkg/__pycache__/x.pyc", ".aider.chat.history.md", ".idea/x.xml"):
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text("noise\n")
    (repo / ".claude" / "commands").mkdir(parents=True)
    (repo / ".claude" / "commands" / "review.md").write_text("real work\n")
    assert gitutil.changed_files(repo) == [".claude/commands/review.md"]
    assert len(gitutil.changed_files(repo, ignore=())) == 6


OTHER_TOOLS_NOISE = (
    ".cursor/rules/remit.mdc", ".cursorrules", ".windsurf/rules/remit.md", ".codex/config.toml", ".gemini/settings.json",
    "GEMINI.md", ".github/copilot-instructions.md", ".aider.conf.yml", ".aider.chat.history.md",
)


def test_files_other_agent_tools_write_are_noise_too(repo):
    for rel in OTHER_TOOLS_NOISE:
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text("noise\n")
    assert gitutil.changed_files(repo) == []
    assert gitutil.diff_numstat(repo).total == 0 and gitutil.status_porcelain(repo) == []
    assert len(gitutil.changed_files(repo, ignore=())) == len(OTHER_TOOLS_NOISE)
    learner_commit(repo, "chore(x): a tool's files got committed")
    assert gitutil.changed_files(repo) == []  # ignored once committed too


def test_files_that_labs_ask_for_are_never_noise(repo):
    """CLAUDE.md and AGENTS.md are the project memory (lab m02 onwards); .claude/ and workflows are real work."""
    real = ("CLAUDE.md", "AGENTS.md", ".claude/settings.json", ".claude/agents/reviewer.md", ".claude/commands/review.md",
            ".github/workflows/review.yml", ".github/pull_request_template.md", "cursor-notes.md", "docs/GEMINI.md")
    for rel in real:
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text("work\n")
        assert not gitutil.glob_match(rel, gitutil.TOOL_NOISE), rel
    assert gitutil.changed_files(repo) == sorted(real)


def test_diff_numstat_counts_lines_since_the_tag_including_untracked(repo):
    (repo / "a.txt").write_text("one\nTWO\nthree\nfour\n")  # +2 -1
    (repo / "new.txt").write_text("1\n2\n3\n")  # +3
    (repo / "blob.bin").write_bytes(b"\0\1\2")
    stat = gitutil.diff_numstat(repo)
    assert (stat.added, stat.deleted, stat.total, stat.n_files) == (5, 1, 6, 3)
    assert stat.files == ["a.txt", "blob.bin", "new.txt"]
    learner_commit(repo, "feat(x): y")
    assert gitutil.diff_numstat(repo).total == 6  # committing does not change the total


def test_commits_since_returns_oldest_first_with_bodies(repo):
    (repo / "a.txt").write_text("1\n")
    learner_commit(repo, "fix(a): first\n\nBecause reasons.\n\nSecond paragraph.")
    (repo / "b.txt").write_text("2\n")
    learner_commit(repo, "feat(b): second")
    first, second = gitutil.commits_since(repo)
    assert (first.subject, second.subject) == ("fix(a): first", "feat(b): second")
    assert first.body == "Because reasons.\n\nSecond paragraph." and second.body == ""
    assert (first.author_name, first.author_email) == LEARNER and not first.is_merge
    assert first.message.startswith("fix(a): first\n\nBecause")
    assert gitutil.commits_since(repo, ref="lab-start") == []


def test_merge_commits_are_marked_and_can_be_filtered(repo):
    gitutil.create_branch(repo, "feature")
    (repo / "f.txt").write_text("f\n")
    learner_commit(repo, "feat(f): add f")
    gitutil.checkout(repo, "main")
    (repo / "m.txt").write_text("m\n")
    learner_commit(repo, "feat(m): add m")
    gitutil.merge(repo, "feature", message="Merge feature", no_ff=True)
    commits = gitutil.commits_since(repo)
    assert [c.is_merge for c in commits] == [False, False, True]
    assert [c.subject for c in gitutil.commits_since(repo, no_merges=True)] == ["feat(f): add f", "feat(m): add m"]
    assert set(gitutil.branches(repo)) == {"main", "feature"}


def test_glob_matching():
    match = gitutil.glob_match
    assert match("src/remit/notify.py", ["src/remit/notify.py"])
    assert match("src/remit/notify.py", ["src/**"]) and match("src/a.py", ["src/**/*.py"]) and match("src/x/y/z.py", ["src/**/*.py"])
    assert match("tests/test_a.py", ["tests/**"]) and match("tests/sub/test_a.py", ["tests/*/test_*.py"])
    assert not match("tests/sub/test_a.py", ["tests/*.py"])  # a single * stays inside one folder
    assert not match("src/remit/notify.pyc", ["src/remit/notify.py"])
    assert match("README.md", ["*.md"]) and not match("docs/a.md", ["*.md"]) and match("docs/a.md", ["**/*.md"])
    assert match("a/__pycache__/b.pyc", gitutil.TOOL_NOISE)


def test_commit_all_force_adds_ignored_files_and_empty_commits_need_a_flag(repo):
    (repo / ".gitignore").write_text("*.log\n")
    (repo / "prod.log").write_text("line\n")
    learner_commit(repo, "chore(x): ignore logs")
    assert "prod.log" not in gitutil.out(repo, "ls-files")
    learner_commit(repo, "chore(x): add the log anyway", force=["prod.log"])
    assert "prod.log" in gitutil.out(repo, "ls-files")
    with pytest.raises(gitutil.GitError):
        gitutil.commit_all(repo, "nothing to commit")
    gitutil.commit_all(repo, "empty", allow_empty=True)


def test_apply_patch_and_file_at(repo):
    patch = "--- a/a.txt\n+++ b/a.txt\n@@ -1,3 +1,3 @@\n one\n-two\n+2\n three\n"
    gitutil.apply_patch(repo, patch)
    assert (repo / "a.txt").read_text() == "one\n2\nthree\n"
    assert gitutil.file_at(repo, "lab-start", "a.txt") == "one\ntwo\nthree\n"
    assert gitutil.file_at(repo, "lab-start", "nope.txt") is None
    with pytest.raises(gitutil.GitError):
        gitutil.apply_patch(repo, patch)  # already applied


def test_identity_is_only_set_when_git_has_none(tmp_path, monkeypatch):
    empty_home = tmp_path / "home"
    empty_home.mkdir()
    for key in ("HOME", "XDG_CONFIG_HOME"):
        monkeypatch.setenv(key, str(empty_home))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    path = tmp_path / "r"
    path.mkdir()
    gitutil.init_repo(path)
    assert gitutil.ensure_identity(path) is True
    assert gitutil.out(path, "config", "user.name") == "Najm Learner"
    assert gitutil.ensure_identity(path) is False  # now it has one


def test_local_excludes_hide_files_from_status_without_touching_gitignore(repo):
    gitutil.add_local_excludes(repo, [".aider*", "scratch/"])
    gitutil.add_local_excludes(repo, [".aider*"])  # idempotent
    (repo / "scratch").mkdir()
    (repo / "scratch" / "x").write_text("x")
    assert gitutil.status_porcelain(repo, ignore=()) == []
    assert (repo / ".git" / "info" / "exclude").read_text().count(".aider*") == 1


def test_git_environment_from_the_callers_shell_does_not_leak(repo, monkeypatch, tmp_path):
    other = tmp_path / "other"
    other.mkdir()
    subprocess.run(["git", "init", "-q", str(other)], check=True)
    monkeypatch.setenv("GIT_DIR", str(other / ".git"))
    assert gitutil.current_branch(repo) == "main"  # still talks to `repo`, not to GIT_DIR


# =============================================================================
# runner
# =============================================================================
def test_run_captures_output_and_exit_status(tmp_path):
    result = runner.run([sys.executable, "-c", "import sys; print('out'); print('err', file=sys.stderr); sys.exit(3)"],
                        cwd=tmp_path)
    assert (result.returncode, result.stdout.strip(), result.stderr.strip()) == (3, "out", "err")
    assert not result.ok and not result.timed_out and result.output == "out\nerr\n"


def test_run_kills_the_whole_process_group_on_timeout(tmp_path):
    marker = tmp_path / "grandchild-survived"
    script = (
        "import subprocess, sys, time\n"
        f"subprocess.Popen([sys.executable, '-c', \"import time, pathlib; time.sleep(3); pathlib.Path(r'{marker}').write_text('x')\"])\n"
        "time.sleep(30)\n"
    )
    started = time.monotonic()
    result = runner.run([sys.executable, "-c", script], timeout=1.0)
    assert result.timed_out and not result.ok and time.monotonic() - started < 10
    time.sleep(3.5)  # long enough for a surviving grandchild to write its marker
    assert not marker.exists()


def test_run_reports_a_missing_command_instead_of_raising(tmp_path):
    result = runner.run(["definitely-not-a-command-xyz"])
    assert result.returncode == 127 and "not found" in result.stderr
    assert runner.run(["ls"], cwd=tmp_path / "missing-dir").returncode != 0


def test_clean_env_scrubs_the_learners_shell(monkeypatch):
    for key in ("REMIT_DB", "NAJMKIT_AUDIT_LOG", "PYTEST_ADDOPTS", "GIT_DIR", "PYTHONPATH"):
        monkeypatch.setenv(key, "x")
    env = runner.clean_env(pythonpath=["/a", "/b"], extra={"KEEP": "1"})
    assert not any(k.startswith(("REMIT_", "NAJMKIT_", "GIT_")) for k in env)
    assert env["PYTHONPATH"] == os.pathsep.join(["/a", "/b"]) and env["KEEP"] == "1"
    assert env["PYTHONDONTWRITEBYTECODE"] == "1" and env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] == "1"
    assert "PYTEST_ADDOPTS" not in env
    assert runner.clean_env(keep_git=True).get("GIT_DIR") == "x"
    assert "PYTHONPATH" not in runner.clean_env()


def test_run_python_uses_the_given_pythonpath(tmp_path):
    (tmp_path / "mymod.py").write_text("VALUE = 42\n")
    result = runner.run_python(["-c", "import mymod; print(mymod.VALUE)"], pythonpath=[tmp_path])
    assert result.ok and result.stdout.strip() == "42"
