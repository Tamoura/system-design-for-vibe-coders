"""Tests for the post-edit hook: feed it hook documents on standard input, never run anything it reads."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".claude" / "hooks" / "post_edit.py"


def run_hook(document, project=ROOT):
    text = document if isinstance(document, str) else json.dumps(document)
    return subprocess.run([sys.executable, str(HOOK)], input=text, capture_output=True, text=True, timeout=20,
                          env={"CLAUDE_PROJECT_DIR": str(project), "PATH": "/usr/bin:/bin"})


def edit(path, project=ROOT):
    return {"hook_event_name": "PostToolUse", "tool_name": "Edit", "cwd": str(project), "tool_input": {"file_path": str(path)}}


def money_file(tmp_path, source):
    path = tmp_path / "src" / "remit" / "sample.py"
    path.parent.mkdir(parents=True)
    path.write_text(source, encoding="utf-8")
    return path


def test_a_clean_money_file_is_quiet(tmp_path):
    path = money_file(tmp_path, "from decimal import Decimal\nFEE = Decimal('0.15')\n")
    result = run_hook(edit(path, tmp_path), tmp_path)
    assert result.returncode == 0 and result.stderr == ""


def test_a_float_literal_in_money_code_is_reported(tmp_path):
    path = money_file(tmp_path, "FEE = 0.15\n")
    result = run_hook(edit(path, tmp_path), tmp_path)
    assert result.returncode == 2
    assert "sample.py" in result.stderr and "float" in result.stderr


def test_float_call_is_reported_but_isinstance_and_strings_are_not(tmp_path):
    bad = money_file(tmp_path, "def f(x):\n    return float(x)\n")
    assert run_hook(edit(bad, tmp_path), tmp_path).returncode == 2
    fine = tmp_path / "src" / "remit" / "fine.py"
    fine.write_text('"""No float here: 0.15."""\n# float(x)\nOK = isinstance(1, (bool, float))\nNAME = "float"\n', encoding="utf-8")
    assert run_hook(edit(fine, tmp_path), tmp_path).returncode == 0


def test_floats_are_allowed_outside_money_code(tmp_path):
    path = tmp_path / "tests" / "test_x.py"
    path.parent.mkdir()
    path.write_text("VALUE = 1.5\n", encoding="utf-8")
    assert run_hook(edit(path, tmp_path), tmp_path).returncode == 0


def test_a_syntax_error_is_reported_anywhere(tmp_path):
    path = tmp_path / "broken.py"
    path.write_text("def broken(:\n    pass\n", encoding="utf-8")
    result = run_hook(edit(path, tmp_path), tmp_path)
    assert result.returncode == 2 and "broken.py" in result.stderr


def test_other_files_missing_files_and_missing_paths_are_ignored(tmp_path):
    notes = tmp_path / "notes.md"
    notes.write_text("float(x) = 0.15\n", encoding="utf-8")
    assert run_hook(edit(notes, tmp_path), tmp_path).returncode == 0
    assert run_hook(edit(tmp_path / "gone.py", tmp_path), tmp_path).returncode == 0
    assert run_hook({"tool_name": "Edit", "tool_input": {}}, tmp_path).returncode == 0


def test_a_relative_path_is_resolved_against_the_document_cwd(tmp_path):
    money_file(tmp_path, "RATE = 0.5\n")
    document = {"tool_name": "Edit", "cwd": str(tmp_path), "tool_input": {"file_path": "src/remit/sample.py"}}
    assert run_hook(document, tmp_path).returncode == 2


def test_unreadable_input_is_the_hooks_problem_not_the_agents(tmp_path):
    for text in ("this is not json", "[1, 2, 3]", ""):
        result = run_hook(text, tmp_path)
        assert result.returncode in (0, 1) and "Traceback" not in result.stderr
