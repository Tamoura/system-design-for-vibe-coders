"""End-to-end tests of `python -m ailab` (in-process for speed, plus a few real subprocess runs)."""
from __future__ import annotations

import json
import subprocess
import sys

from ailab import cli, gitutil
from conftest import GOOD_LAB, KIT_ROOT, make_lab, run_cli


def test_list_shows_the_labs():
    code, out, err = run_cli("list")
    assert code == 0 and err == ""
    header, *rows = out.splitlines()
    assert header.split() == ["ID", "Lesson", "Agent", "Title"]
    m00 = next(r for r in rows if r.startswith("m00"))
    assert "0.2" in m00 and " no " in m00 and "Your first fix" in m00


def test_list_json():
    code, out, _ = run_cli("list", "--json")
    rows = json.loads(out)
    assert code == 0 and any(r["id"] == "m00" and r["lesson"] == "0.2" and r["needs_agent"] is False for r in rows)


def test_doctor_passes_here(tmp_path):
    code, out, _ = run_cli("doctor", "--dir", str(tmp_path / "not-yet-created"))
    assert code == 0, out
    assert out.count("[PASS]") >= 5 and "Everything needed is in place." in out
    assert not (tmp_path / "not-yet-created").exists()


def test_doctor_fails_when_the_directory_cannot_be_written(tmp_path):
    blocker = tmp_path / "file"
    blocker.write_text("x")
    code, out, _ = run_cli("doctor", "--dir", str(blocker / "sub"))
    assert code == 1 and "[FAIL] working directory is writable" in out and "hint:" in out


def test_start_creates_the_work_directory_and_prints_the_task(work_dir):
    code, out, err = run_cli("start", "m00", "--dir", str(work_dir))
    assert code == 0 and err == ""
    assert "Lab m00: Your first fix" in out and "(lesson 0.2)" in out and "Needs an agent: no" in out
    assert "# REMIT-212: spelling mistake" in out  # the task is printed
    assert f"python -m ailab grade m00 --dir {work_dir}" in out
    assert (work_dir / "TASK.md").is_file() and (work_dir / ".git").is_dir() and gitutil.has_ref(work_dir, "lab-start")


def test_start_prints_a_grade_command_that_works_from_any_directory_and_says_where_the_work_directory_is(work_dir):
    code, out, _ = run_cli("start", "m00", "--dir", str(work_dir))
    lines = out.splitlines()
    assert code == 0 and lines[2] == f"Work directory: {work_dir}"
    tail = lines[-4:]
    assert tail == [
        f"Your work directory is {work_dir}. Edit files and run git and pytest there:",
        f"  cd {work_dir}",
        "When you are ready, grade from any directory:",
        f"  PYTHONPATH={KIT_ROOT} python -m ailab grade m00 --dir {work_dir}",
    ], tail
    assert "Next: cd" not in out and "When you are ready:" not in out  # the old printout is gone


def test_the_printed_grade_command_really_runs_from_anywhere(work_dir, tmp_path):
    """Copy the printed command, paste it in an unrelated folder (a shell would split it exactly like shlex)."""
    import shlex

    _, out, _ = run_cli("start", "m00", "--dir", str(work_dir))
    printed = out.splitlines()[-1].strip()
    env_part, *argv = shlex.split(printed)
    assert env_part == f"PYTHONPATH={KIT_ROOT}" and argv[:3] == ["python", "-m", "ailab"]
    elsewhere = tmp_path / "somewhere else"
    elsewhere.mkdir()
    env = {k: v for k, v in __import__("os").environ.items() if k != "PYTHONPATH"}
    env.update(PYTHONPATH=env_part.split("=", 1)[1], PYTHONDONTWRITEBYTECODE="1")
    result = subprocess.run([sys.executable, *argv[1:]], cwd=elsewhere, env=env, capture_output=True, text=True)
    assert result.returncode == 1 and "[FAIL]" in result.stdout and "No module named" not in result.stderr
    # without the PYTHONPATH part the same command fails there, which is what learners kept meeting
    bare = {k: v for k, v in env.items() if k != "PYTHONPATH"}
    failed = subprocess.run([sys.executable, *argv[1:]], cwd=elsewhere, env=bare, capture_output=True, text=True)
    assert failed.returncode != 0 and "No module named ailab" in failed.stderr
    # solve prints the same command for the grade that follows it
    code, solved, _ = run_cli("solve", "m00", "--dir", str(work_dir))
    assert code == 0 and solved.splitlines()[-1].strip() == printed and "from any directory" in solved


def test_grade_command_quotes_paths_with_spaces(tmp_path):
    spaced = tmp_path / "my labs" / "m00"
    command = cli.grade_command("m00", spaced)
    assert f"--dir '{spaced}'" in command and command.startswith("PYTHONPATH=") and "python -m ailab grade m00" in command


def test_start_accepts_id_spellings_and_defaults_the_directory_to_the_lab_id(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert run_cli("start", "M0")[0] == 0
    assert (tmp_path / "m00" / "TASK.md").is_file()


def test_start_refuses_to_overwrite(work_dir):
    assert run_cli("start", "m00", "--dir", str(work_dir))[0] == 0
    code, _, err = run_cli("start", "m00", "--dir", str(work_dir))
    assert code == 2 and "not empty" in err


def test_unknown_lab_and_bad_usage():
    code, _, err = run_cli("start", "m77", "--dir", "/nonexistent/never-created")
    assert code == 2 and "no lab" in err and "m00" in err
    assert run_cli()[0] == 2
    assert run_cli("frobnicate")[0] == 2
    assert run_cli("--help")[0] == 0


def test_grade_fails_on_the_starter_and_passes_after_solve(work_dir):
    run_cli("start", "m00", "--dir", str(work_dir))
    code, out, _ = run_cli("grade", "m00", "--dir", str(work_dir))
    assert code == 1
    lines = out.splitlines()
    assert any(line.startswith("[FAIL] Your tests pass") for line in lines)
    assert any(line.startswith("       hint: ") for line in lines)
    assert any(line.startswith("[PASS] ") for line in lines)
    assert lines[-1].endswith("NOT YET") and "required checks passed" in lines[-1]

    assert run_cli("solve", "m00", "--dir", str(work_dir))[0] == 0
    code, out, _ = run_cli("grade", "m00", "--dir", str(work_dir))
    assert code == 0 and "FAIL" not in out and out.splitlines()[-1].endswith("PASSED")


def test_grade_json_output(work_dir):
    run_cli("start", "m00", "--dir", str(work_dir))
    code, out, _ = run_cli("grade", "m00", "--dir", str(work_dir), "--json")
    payload = json.loads(out)
    assert code == 1 and payload["lab"] == "m00" and payload["passed"] is False
    assert payload["required_total"] == len(payload["checks"]) and payload["required_passed"] < payload["required_total"]
    assert set(payload["checks"][0]) == {"name", "ok", "detail", "hint", "required"}
    run_cli("solve", "--dir", str(work_dir))
    code, out, _ = run_cli("grade", "--dir", str(work_dir), "--json")
    assert code == 0 and json.loads(out)["passed"] is True


def test_grade_works_without_the_lab_id_because_the_directory_remembers_it(work_dir):
    run_cli("start", "m00", "--dir", str(work_dir))
    code, out, _ = run_cli("grade", "--dir", str(work_dir))
    assert code == 1 and "Lab m00" in out


def test_grade_rejects_the_wrong_lab_or_a_plain_directory(fake_labs, tmp_path):
    make_lab(fake_labs, "m91_one", GOOD_LAB.format(id="m91"))
    make_lab(fake_labs, "m92_two", GOOD_LAB.format(id="m92"))
    work = tmp_path / "work"
    assert run_cli("start", "m91", "--dir", str(work))[0] == 0
    plain = tmp_path / "plain"
    plain.mkdir()
    code, _, err = run_cli("grade", "m91", "--dir", str(plain))
    assert code == 2 and "was not created by" in err
    code, _, err = run_cli("grade", "m91", "--dir", str(tmp_path / "missing"))
    assert code == 2 and "not a directory" in err
    code, _, err = run_cli("grade", "m92", "--dir", str(work))
    assert code == 2 and "started for m91, not m92" in err
    code, _, err = run_cli("solve", "m92", "--dir", str(work))
    assert code == 2 and "started for m91" in err
    assert run_cli("grade", "m91", "--dir", str(work))[0] == 1  # the right lab grades (and fails: nothing solved)


def test_a_lab_is_only_graded_in_a_directory_started_for_it(work_dir):
    run_cli("start", "m00", "--dir", str(work_dir))
    code, _, err = run_cli("grade", "--dir", str(work_dir.parent))
    assert code == 2 and "was not created by" in err


def test_solve_does_not_clobber_the_learners_work_without_force(work_dir):
    run_cli("start", "m00", "--dir", str(work_dir))
    (work_dir / "mine.txt").write_text("work in progress\n")
    code, _, err = run_cli("solve", "m00", "--dir", str(work_dir))
    assert code == 2 and "--force" in err
    assert not gitutil.commits_since(work_dir)  # nothing was applied
    assert run_cli("solve", "m00", "--dir", str(work_dir), "--force")[0] == 0
    assert len(gitutil.commits_since(work_dir)) == 1


def test_python_dash_m_ailab_really_works_as_a_subprocess(tmp_path):
    """The documented entry point, run the way a learner runs it: from the kit folder."""
    env = {**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"}
    work = tmp_path / "w"
    result = subprocess.run([sys.executable, "-m", "ailab", "list"], cwd=KIT_ROOT, env=env, capture_output=True, text=True)
    assert result.returncode == 0 and "m00" in result.stdout
    result = subprocess.run([sys.executable, "-m", "ailab", "start", "m00", "--dir", str(work)], cwd=KIT_ROOT, env=env,
                            capture_output=True, text=True)
    assert result.returncode == 0 and (work / "TASK.md").exists()
    result = subprocess.run([sys.executable, "-m", "ailab", "grade", "m00", "--dir", str(work)], cwd=KIT_ROOT, env=env,
                            capture_output=True, text=True)
    assert result.returncode == 1 and "[FAIL]" in result.stdout
    result = subprocess.run([sys.executable, "-m", "ailab", "nonsense"], cwd=KIT_ROOT, env=env, capture_output=True, text=True)
    assert result.returncode == 2
