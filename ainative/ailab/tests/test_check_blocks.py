"""check_blocks.py: lesson blocks that name a kit file must equal it (and kit files must live where they say)."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import KIT_ROOT

SKELETON = "# ailab/labs/m99_demo/assets/guard_skeleton.py\nimport sys\n\n\ndef main():\n    return 0\n"


@pytest.fixture
def sandbox(tmp_path):
    """A miniature ainative/ with the real script, one kit file and a modules folder."""
    kit = tmp_path / "ainative" / "ailab"
    (kit / "ailab" / "labs" / "m99_demo" / "assets").mkdir(parents=True)
    shutil.copyfile(KIT_ROOT / "check_blocks.py", kit / "check_blocks.py")
    (kit / "ailab" / "labs" / "m99_demo" / "assets" / "guard_skeleton.py").write_text(SKELETON)
    modules = tmp_path / "ainative" / "modules"
    modules.mkdir()
    return kit, modules


def run(kit: Path, *args: str):
    result = subprocess.run([sys.executable, str(kit / "check_blocks.py"), *args], capture_output=True, text=True,
                            env={"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1"})
    return result.returncode, result.stdout


def lesson(body: str, lang: str = "python") -> str:
    return f"# Module 8\n\nText.\n\n```{lang}\n{body}```\n\nMore text.\n"


def test_a_matching_block_passes(sandbox):
    kit, modules = sandbox
    (modules / "08-security.md").write_text(lesson(SKELETON))
    code, out = run(kit, str(modules))
    assert code == 0 and out.startswith("1 lesson blocks match their kit files, 0 problems")


def test_a_block_that_differs_from_the_file_fails(sandbox):
    kit, modules = sandbox
    (modules / "08-security.md").write_text(lesson(SKELETON.replace("return 0", "return 1")))
    code, out = run(kit, str(modules))
    assert code == 1 and "08-security.md: the block for ailab/labs/m99_demo/assets/guard_skeleton.py differs from the file" in out


def test_a_block_naming_a_missing_file_fails(sandbox):
    kit, modules = sandbox
    (modules / "08-security.md").write_text(lesson("# ailab/labs/m99_demo/assets/nope.py\nx = 1\n"))
    code, out = run(kit, str(modules))
    assert code == 1 and "nope.py does not exist" in out


def test_blocks_without_a_path_comment_are_ignored(sandbox):
    kit, modules = sandbox
    (modules / "08-security.md").write_text(lesson("# just a comment\nx = 1\n") + lesson('{"a": 1}\n', "json"))
    code, out = run(kit, str(modules))
    assert code == 0 and out.startswith("0 lesson blocks match")


def test_shell_yaml_and_toml_blocks_are_checked_too(sandbox):
    kit, modules = sandbox
    sh = "# ailab/labs/m99_demo/assets/run.sh\necho hello\n"
    (kit / "ailab" / "labs" / "m99_demo" / "assets" / "run.sh").write_text(sh)
    (modules / "09-automate.md").write_text(lesson(sh, "bash"))
    code, out = run(kit, str(modules))
    assert code == 0 and out.startswith("1 lesson blocks match")


def test_arabic_lessons_are_checked_unless_english_only(sandbox):
    kit, modules = sandbox
    (modules / "08-security.md").write_text(lesson(SKELETON))
    (modules / "08-security.ar.md").write_text(lesson(SKELETON.replace("main", "رئيسي")))
    assert run(kit, str(modules))[0] == 1
    code, out = run(kit, str(modules), "--english-only")
    assert code == 0 and out.startswith("1 lesson blocks match")


def test_a_kit_file_that_names_the_wrong_path_fails(sandbox):
    kit, modules = sandbox
    (kit / "ailab" / "labs" / "m99_demo" / "assets" / "moved.py").write_text("# ailab/labs/m99_demo/assets/old_name.py\nx = 1\n")
    code, out = run(kit, str(modules))
    assert code == 1 and "its first line says ailab/labs/m99_demo/assets/old_name.py" in out


def test_kit_files_that_name_a_path_but_are_not_shown_are_reported(sandbox):
    kit, modules = sandbox
    code, out = run(kit, str(modules))
    assert code == 0 and "1 kit files that name their path are not shown in any lesson" in out
    assert "guard_skeleton.py" in out


def test_the_real_kit_is_consistent(tmp_path):
    """No kit file names a path other than its own. (An empty modules folder is used on purpose: lessons are
    written in parallel and may be unfinished, so this test must not depend on them.)"""
    code, out = run(KIT_ROOT, str(tmp_path))
    assert code == 0, out
