"""Several people build labs at the same time. A half-built or broken lab must hurt only itself.

These tests copy the whole kit to a temporary folder, add broken labs next to the real ones, and run the
*generic lab test* there, exactly as a lab writer would.
"""
from __future__ import annotations

import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from ailab import runner
from conftest import KIT_ROOT


@pytest.fixture(scope="module")
def kit_with_broken_labs(tmp_path_factory) -> Path:
    kit = tmp_path_factory.mktemp("kit") / "ailab-kit"
    shutil.copytree(KIT_ROOT, kit, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", ".git", ".venv"))
    labs = kit / "ailab" / "labs"
    for other in labs.iterdir():  # other writers' labs are none of this test's business (they may be unfinished)
        if other.is_dir() and other.name != "m00_first_fix" and not other.name.startswith("__"):
            shutil.rmtree(other)
    (labs / "m97_syntax").mkdir()
    (labs / "m97_syntax" / "lab.py").write_text("def broken(:\n")
    (labs / "m97_syntax" / "task.md").write_text("# nothing\n")
    (labs / "m98_unfinished").mkdir()  # only a ticket so far: no lab.py yet
    (labs / "m98_unfinished" / "task.md").write_text("# Work in progress\n")
    (labs / "m96_imports").mkdir()
    (labs / "m96_imports" / "lab.py").write_text("from ailab.framework import Lab\nimport a_module_that_is_not_written_yet\n")
    (labs / "m96_imports" / "task.md").write_text("# nothing\n")
    return kit


def run_generic(kit: Path, *extra: str) -> tuple[int, dict[str, list[str]]]:
    junit = kit / "result.xml"
    result = runner.run_python(
        ["-m", "pytest", "-q", "-p", "no:cacheprovider", f"--junitxml={junit}", "tests/test_labs_generic.py", *extra],
        cwd=kit, timeout=240)
    outcome: dict[str, list[str]] = {"passed": [], "failed": []}
    for case in ET.parse(junit).getroot().iter("testcase"):
        bad = case.find("failure") is not None or case.find("error") is not None
        outcome["failed" if bad else "passed"].append(case.get("name", ""))
    return result.returncode, outcome


# tests/test_labs_generic.py runs this many cases for every lab (well-formed, start state, starter fails, deterministic grading,
# solution passes, no false secret hits, nothing on another branch at the start, fast)
GENERIC_CASES_PER_LAB = 8


def test_broken_labs_fail_only_their_own_cases(kit_with_broken_labs):
    code, outcome = run_generic(kit_with_broken_labs)
    assert code == 1  # the suite is red because three labs are broken...
    failed = outcome["failed"]
    assert failed and all(any(lab in name for lab in ("m97", "m98", "m96")) for name in failed), failed
    # ...but nothing about m00 failed, and collection itself did not break
    assert sum(1 for name in outcome["passed"] if "m00" in name) == GENERIC_CASES_PER_LAB
    assert not any("m00" in name for name in failed)
    for lab in ("m97", "m98", "m96"):
        assert any(lab in name for name in failed), f"{lab} should have failing cases"


def test_k_selects_one_lab_so_a_writer_never_runs_the_others(kit_with_broken_labs):
    code, outcome = run_generic(kit_with_broken_labs, "-k", "m00")
    assert code == 0, outcome
    assert len(outcome["passed"]) == GENERIC_CASES_PER_LAB and not outcome["failed"]
    assert all("m00" in name for name in outcome["passed"])


def test_the_cli_lists_the_broken_labs_and_still_runs_the_good_one(kit_with_broken_labs, tmp_path):
    def cli(*args: str):
        return runner.run_python(["-m", "ailab", *args], cwd=kit_with_broken_labs)

    listing = cli("list")
    assert listing.ok
    assert "BROKEN (m97_syntax): SyntaxError" in listing.stdout
    assert "BROKEN (m98_unfinished): lab.py is missing" in listing.stdout
    assert "BROKEN (m96_imports): ModuleNotFoundError" in listing.stdout
    assert "m00" in listing.stdout and "Your first fix" in listing.stdout
    work = tmp_path / "w"
    assert cli("start", "m00", "--dir", str(work)).ok
    assert cli("grade", "m00", "--dir", str(work)).returncode == 1  # graded, not crashed
    assert cli("solve", "m00", "--dir", str(work)).ok and cli("grade", "m00", "--dir", str(work)).ok
    broken = cli("start", "m97", "--dir", str(tmp_path / "x"))
    assert broken.returncode == 2 and "BROKEN" in broken.stderr and "SyntaxError" in broken.stderr
    assert cli("grade", "m98", "--dir", str(work)).returncode == 2
