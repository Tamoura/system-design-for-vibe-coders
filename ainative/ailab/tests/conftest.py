"""Shared helpers for the kit's own tests.

Fixtures here create *started labs* in temporary folders (outside the repository), so no test
ever touches ``ailab/base`` or a real learner directory.
"""
from __future__ import annotations

import io
import os
import sys
import textwrap
from pathlib import Path

import pytest

sys.dont_write_bytecode = True  # the kit's tests leave no __pycache__ behind (least of all inside the frozen base)

KIT_ROOT = Path(__file__).resolve().parent.parent  # ainative/ailab
if str(KIT_ROOT) not in sys.path:  # pytest.ini sets pythonpath=. too; this keeps `python tests/x.py` working
    sys.path.insert(0, str(KIT_ROOT))

import ailab.labs  # noqa: E402
from ailab import cli, framework, gitutil  # noqa: E402

LEARNER = ("Test Learner", "learner@najm.example")


def run_cli(*argv: str) -> tuple[int, str, str]:
    """Run ``python -m ailab <argv>`` in-process; returns (exit code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.main(list(argv), out=out, err=err)
    return code, out.getvalue(), err.getvalue()


def start(lab_id: str, dest: Path) -> Path:
    """Start a lab in ``dest`` (through the framework, as ``ailab start`` does)."""
    return framework.start_lab(framework.load_lab(lab_id), dest)


def learner_commit(work: Path, message: str, **kwargs) -> str:
    """Commit everything as the learner (a fixed identity so tests do not depend on git config)."""
    kwargs.setdefault("author", LEARNER)
    kwargs.setdefault("date", "2026-03-02T09:30:00+00:00")
    return gitutil.commit_all(work, message, **kwargs)


def tree_digest(work: Path) -> dict[str, bytes]:
    """Every file's bytes except .git, to prove that grading did not change the work directory."""
    result = {}
    for path in sorted(work.rglob("*")):
        if path.is_file() and ".git" not in path.relative_to(work).parts:
            result[path.relative_to(work).as_posix()] = path.read_bytes()
    return result


@pytest.fixture
def work_dir(tmp_path):
    """A fresh, empty path for a new work directory."""
    return tmp_path / "work"


@pytest.fixture(autouse=True)
def quiet_env(monkeypatch):
    """Keep the learner's shell from leaking into tests (git and kit variables)."""
    for key in list(os.environ):
        if key.startswith(("GIT_", "REMIT_", "NAJMKIT_")):
            monkeypatch.delenv(key, raising=False)


# ---------------------------------------------------------------------------------------------
# Fake labs: a temporary labs/ folder wired into the framework (for testing discovery and the CLI)
# ---------------------------------------------------------------------------------------------
GOOD_LAB = '''
from ailab.framework import Check, Lab

def seed(work):
    (work / "seeded.txt").write_text("seeded\\n")

def grade(work):
    return [Check("seeded file removed", not (work / "seeded.txt").exists(), "still there", "delete it")]

def solve(work):
    (work / "seeded.txt").unlink()

LAB = Lab(id="{id}", title="Fake lab", lesson="9.9", needs_agent=False, seed=seed, grade=grade, solve=solve)
'''
TASK = "# Fake ticket\n\nThis is a fake lab used by the kit's own tests.\n"


@pytest.fixture
def fake_labs(tmp_path, monkeypatch):
    """A temporary labs folder wired into the framework and the ``ailab.labs`` package path."""
    folder = tmp_path / "labs"
    folder.mkdir()
    monkeypatch.setattr(framework, "LABS_DIR", folder)
    monkeypatch.setattr(ailab.labs, "__path__", [str(folder)] + list(ailab.labs.__path__))
    before = set(sys.modules)
    yield folder
    for name in set(sys.modules) - before:
        if name.startswith("ailab.labs."):
            del sys.modules[name]


def make_lab(folder: Path, dirname: str, lab_py: str | None, task: str | None = TASK) -> None:
    path = folder / dirname
    path.mkdir()
    if lab_py is not None:
        (path / "lab.py").write_text(textwrap.dedent(lab_py), encoding="utf-8")
    if task is not None:
        (path / "task.md").write_text(task, encoding="utf-8")


