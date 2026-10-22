"""Every lab must pass the same lifecycle test: start -> grade FAILS -> solve -> grade PASSES.

One test case per lab and per property, so a broken or half-built lab fails only its own cases and
the rest of the suite still runs. Labs are listed by *folder name* at collection time (nothing is
imported then); each lab is imported lazily inside its test. To test only your lab:

    pytest -q tests/test_labs_generic.py -k m05
"""
from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from ailab import framework, gitutil
from conftest import tree_digest

BUDGET_SECONDS = 30  # the plan says ~20 s; the test allows slack for slow machines

# Folder names only: no lab.py is imported while the suite is being collected.
LAB_DIRS = framework.lab_dirnames()
PARAMS = [pytest.param(name.split("_", 1)[0], id=name.split("_", 1)[0]) for name in LAB_DIRS]


@dataclass
class Lifecycle:
    """What happened when a lab was started, graded twice, solved and graded again."""

    lab: framework.Lab
    work: Path
    start_seconds: float = 0.0
    starter_grades: list = field(default_factory=list)
    starter_grades_again: list = field(default_factory=list)
    digest_before: dict = field(default_factory=dict)
    digest_after_grading: dict = field(default_factory=dict)
    status_before: list = field(default_factory=list)
    log_at_start: list = field(default_factory=list)  # commit subjects up to lab-start, oldest first
    head_at_start: str = ""
    tag_at_start: str = ""
    status_after_grading: list = field(default_factory=list)
    solved_grades: list = field(default_factory=list)
    total_seconds: float = 0.0


@pytest.fixture(scope="module")
def lifecycle_for(tmp_path_factory):
    """Returns a function lab_id -> Lifecycle, running each lab's lifecycle at most once per module."""
    cache: dict[str, Lifecycle | BaseException] = {}

    def get(lab_id: str) -> Lifecycle:
        if lab_id not in cache:
            try:
                cache[lab_id] = _run_lifecycle(lab_id, tmp_path_factory.mktemp(f"lab-{lab_id}") / "work")
            except BaseException as exc:  # reported by every test of this lab, and only by them
                cache[lab_id] = exc
        value = cache[lab_id]
        if isinstance(value, BaseException):
            raise value
        return value

    return get


def _run_lifecycle(lab_id: str, work: Path) -> Lifecycle:
    began = time.monotonic()
    lab = framework.load_lab(lab_id)
    framework.start_lab(lab, work)
    life = Lifecycle(lab=lab, work=work, start_seconds=time.monotonic() - began)
    life.digest_before = tree_digest(work)
    life.log_at_start = gitutil.out(work, "log", "--reverse", "--format=%s", "lab-start").splitlines()
    life.head_at_start = gitutil.head(work)
    life.tag_at_start = gitutil.rev_parse(work, "lab-start") or ""
    life.status_before = gitutil.status_porcelain(work, ignore=())
    life.starter_grades = framework.grade_lab(lab, work, catch=False)
    life.digest_after_grading = tree_digest(work)
    life.status_after_grading = gitutil.status_porcelain(work, ignore=())
    life.starter_grades_again = framework.grade_lab(lab, work, catch=False)
    framework.solve_lab(lab, work)
    life.solved_grades = framework.grade_lab(lab, work, catch=False)
    life.total_seconds = time.monotonic() - began
    return life


def describe(checks) -> str:
    return "\n".join(f"  {'PASS' if c.ok else 'FAIL'} {c.name}: {c.detail}" for c in checks)


@pytest.mark.parametrize("lab_id", PARAMS)
def test_lab_is_well_formed(lab_id):
    entry = framework.load_entry(framework.find_dirname(lab_id))
    assert not entry.broken, f"lab {lab_id} is BROKEN: {entry.error}"
    lab = entry.lab
    assert re.fullmatch(r"m\d\d", lab.id)
    assert re.fullmatch(r"\d+\.\d+", lab.lesson), f"lesson should look like '4.2', got {lab.lesson!r}"
    assert lab.title.strip() and isinstance(lab.needs_agent, bool)
    task = lab.task_file.read_text(encoding="utf-8")
    assert task.startswith("# "), "task.md should start with a heading (the ticket title)"
    assert len(task.split()) >= 30, "task.md looks too short to be a ticket"
    assert "/home/" not in task and "hidden/" not in task, "task.md must not mention hidden material or absolute paths"


@pytest.mark.parametrize("lab_id", PARAMS)
def test_start_creates_the_documented_state(lifecycle_for, lab_id):
    life = lifecycle_for(lab_id)
    work, lab = life.work, life.lab
    assert life.log_at_start[0] == "Initial state" and life.log_at_start[-1] == "Lab starting state"
    assert life.tag_at_start == life.head_at_start, "the lab-start tag must point at the starting state"
    assert (work / "TASK.md").read_text(encoding="utf-8") == lab.task_file.read_text(encoding="utf-8")
    assert (work / "src" / "remit" / "service.py").is_file() and (work / "CONTRIBUTING.md").is_file()
    if lab.assets_dir is not None:
        for source in lab.assets_dir.rglob("*"):
            if source.is_file() and "__pycache__" not in source.parts:
                assert (work / "lab-assets" / source.relative_to(lab.assets_dir)).is_file()
    assert life.status_before == [], f"a freshly started lab must be clean, got {life.status_before}"
    assert gitutil.get_config(work, "ailab.lab") == lab.id
    assert gitutil.current_branch(work) in gitutil.branches(work)


@pytest.mark.parametrize("lab_id", PARAMS)
def test_the_starter_is_not_already_solved(lifecycle_for, lab_id):
    life = lifecycle_for(lab_id)
    assert not framework.passed(life.starter_grades), "the untouched starter passes the grader:\n" + describe(life.starter_grades)
    failing = [c for c in life.starter_grades if c.required and not c.ok]
    assert failing and all(c.detail or c.hint for c in failing), "every failing check needs a detail or a hint"


@pytest.mark.parametrize("lab_id", PARAMS)
def test_grading_is_deterministic_and_leaves_the_work_alone(lifecycle_for, lab_id):
    life = lifecycle_for(lab_id)

    def key(checks):
        return [(c.name, c.ok, c.detail, c.hint, c.required) for c in checks]

    assert key(life.starter_grades) == key(life.starter_grades_again)
    assert life.digest_before == life.digest_after_grading, "grading changed files in the work directory"
    assert life.status_before == life.status_after_grading, "grading changed git status"
    names = [c.name for c in life.starter_grades]
    assert len(names) == len(set(names)), "check names must be unique within a lab"


@pytest.mark.parametrize("lab_id", PARAMS)
def test_the_reference_solution_passes(lifecycle_for, lab_id):
    life = lifecycle_for(lab_id)
    assert framework.passed(life.solved_grades), "the reference solution fails the grader:\n" + describe(life.solved_grades)
    assert [c.name for c in life.solved_grades] == [c.name for c in life.starter_grades]


@pytest.mark.parametrize("lab_id", PARAMS)
def test_the_whole_lab_is_fast(lifecycle_for, lab_id):
    life = lifecycle_for(lab_id)
    assert life.total_seconds < BUDGET_SECONDS, f"start+grade+solve+grade took {life.total_seconds:.1f}s"


def test_at_least_one_lab_is_present():
    assert LAB_DIRS, "no lab folders found"
