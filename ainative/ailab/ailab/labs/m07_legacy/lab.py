"""Lab m07 (lesson 7.2): "Tame an untested module, refactor it, then migrate a dependency".

The story
---------
``remit/ledger.py`` is Remit's oldest module: a double-entry "shadow ledger" with no tests and its books in
module-level variables (quirks Q-LED-1..4 in KIT_NOTES.md). Finance wants two RemitService objects in one process,
each with its own books, and Platform Engineering is retiring najmkit 1. The learner does three things, in three
kinds of commit:

  Part 1  write characterization tests for the ledger BEFORE touching it, through a small seam they copy from
          lab-assets (tests/ledger_port.py: ``make_ledger()`` and ``ledger_of(service)``), so that the same tests
          run on the legacy module and on the refactored class;
  Part 2  refactor: ``class Ledger`` with instance state only, ``RemitService(..., ledger=None)`` (AUTHORING.md,
          decision 3: the interface is fixed and task.md states it), module-level functions and ``reset()`` gone;
  Part 3  migrate najmkit v1 to v2. The seed ADDS v2 (the "expand" step: new names beside the old ones, which still
          work but warn) and the migration notes; the learner moves every call site, then deletes the deprecated names
          (the "contract" step). One behaviour changes in v2 on purpose: ``audit.emit`` accepts JSON values only, so
          a ``Money`` must be converted, and a "tidy" conversion changes the audit lines that other teams parse.

What is seeded
--------------
src/najmkit/{__init__,ids,clock,audit}.py        replaced by the v2 versions in ``najmkit_v2/`` (v1 names kept as wrappers)
docs/najmkit-v2-migration.md                     the migration notes (``seed_docs/``)
CLAUDE.md                                        the reference project memory from m02, when it exists
lab-assets/{ledger_port.py, try_mutation.py, refactoring-plan-template.md}   (``assets/``)
The starter suite stays green (99 tests): the v1 wrappers keep every existing call working, with DeprecationWarnings.

What the grader checks (and cannot tell)
----------------------------------------
Part 1: the learner's ``tests/test_ledger_*.py`` pass on the ORIGINAL ledger (rebuilt from the lab-start tag), also on a copy of
it that only differs in comments and private names (so they cannot fingerprint the file), never read the ledger's source text,
and kill at least 13 of 16 mutants of it (``checks_m07.MUTANTS``). Every pytest run is ``pytest -q`` as CI runs it (no working
directory on ``sys.path``: ``from tests.x import`` fails, as it does in CI). Part 2: a hidden characterization suite on the refactor (quirks
preserved, the interface, independent instances, a service that owns its ledger), no module-level state, the old
functions gone. Part 3: no v1 name left in src/remit or tests (import-aware AST scan), the v1 names gone from najmkit
(subprocess import), the audit lines and ids unchanged (hidden), docs updated (advisory). Process: only the allowed files
changed, conventional commits, at least three that change a file with the ledger tests committed before anything under src/
moves, each leaving the suite green (advisory), nothing left uncommitted, no document still calling the ledger untested or
module-level (advisory).
It cannot tell whether the tests are *understood*, whether the refactor was done in small steps rather than one leap
(it can see commits, not thinking), or whether a different quirk exists that nobody pinned: no suite can.

Files
-----
    lab.py            this file                      task.md           the ticket (REMIT-372)
    najmkit_v2/       the v2 library (seed)          seed_docs/        the migration notes (seed)
    assets/           -> lab-assets/                 hidden/           hidden acceptance tests (3 files + conftest)
    solution/         the reference solution, step by step (steps.json)
    ../../checks_m07.py   the helpers for this lab
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from ailab import checks, checks_m07 as m07, framework, gitutil
from ailab.framework import Check, Lab

HERE = Path(__file__).resolve().parent
V2_FILES = ("__init__.py", "ids.py", "clock.py", "audit.py")
LEARNER = ("Najm Learner", "learner@najm.example")

# Files a sound solution may touch.
# (README.md describes the ledger as old code with no tests; pyproject.toml and the CI workflow are where a team makes
# "deprecation warnings are errors" permanent. The ticket lists all of them.)
ALLOWED = [
    "src/remit/ledger.py", "src/remit/service.py", "src/remit/store.py", "src/remit/cli.py", "src/najmkit/**",
    "tests/**", "docs/**", "scripts/**", "CLAUDE.md", "AGENTS.md", ".claude/**", "README.md", "pyproject.toml", ".github/workflows/**",
]
PLAN = "docs/refactoring-plan.md"
PLAN_SECTIONS = ["what must not change", "what i do not understand", "safety net", "seams and the steps", "delegation",
                 "review at scale", "rollback"]

# Check names (stable: the starter and the solved state list the same names in the same order).
C_WROTE = "You wrote characterization tests for the ledger"
C_BASELINE = "Your ledger tests describe the original ledger"
C_MUTANTS = "Your ledger tests catch defects in the original ledger"
C_MUTANTS_ALL = "Your ledger tests catch every defect the grader tried"
C_SUITE = "The whole suite passes"
C_KEPT = "No existing test was deleted"
C_QUIRKS = "The Ledger class keeps every quirk"
C_SERVICE = "RemitService owns its ledger and send() posts as before"
C_STATE = "The ledger keeps no state at module level"
C_LEGACY = "The old module-level ledger functions are gone"
C_V1CALLS = "No use of the najmkit v1 names is left"
C_V1GONE = "The deprecated v1 names are removed from najmkit"
C_AUDIT = "The audit lines and ids come out as before"
C_DOCS = "docs/najmkit.md describes najmkit 2"
C_SCOPE = "Only the files this ticket needs changed"
C_MESSAGES = "Commit messages follow CONTRIBUTING.md"
C_COUNT = "Small steps: at least three commits"
C_GREEN = "Every commit leaves the suite green"
C_CLEAN = "Everything is committed"
C_SECRETS = "No secrets in the change"
C_PLAN = "docs/refactoring-plan.md has its sections"
C_STALE = "No document still calls the ledger untested or module-level"

NEW_MEMORY_LINE = (
    "- `src/remit/screening.py` is legacy and has no tests; its docstring lists its quirks. `src/remit/ledger.py` is a `Ledger` class "
    "(state per instance; `RemitService` owns one) with characterization tests in `tests/test_ledger_characterization.py` that pin "
    "its quirks on purpose: do not \"fix\" them.\n"
)
# What the project memory said about the ledger before this ticket (the line the reference solution replaces).
_STALE_MEMORY = re.compile(r"(?i)ledger[^\n]{0,80}\b(no tests|untested|without tests)|ledger[^\n]*module-level")


# ---------------------------------------------------------------------------------------------
# seed: najmkit 2 beside najmkit 1, the migration notes, the project memory
# ---------------------------------------------------------------------------------------------
def seed(work: Path) -> None:
    for name in V2_FILES:
        framework.write_file(work, f"src/najmkit/{name}", (HERE / "najmkit_v2" / name).read_text(encoding="utf-8"))
    framework.write_file(work, "docs/najmkit-v2-migration.md", (HERE / "seed_docs" / "najmkit-v2-migration.md").read_text(encoding="utf-8"))
    framework.add_reference_memory(work)


# ---------------------------------------------------------------------------------------------
# grade
# ---------------------------------------------------------------------------------------------
def _hidden(work: Path, filename: str, name: str, hint: str) -> Check:
    sources = [HERE / "hidden" / "conftest.py", HERE / "hidden" / filename]
    return checks.hidden_tests_pass(work, sources, name=name, hint=hint, timeout=60)


def grade(work: Path) -> list[Check]:
    results: list[Check] = []

    # ---- Part 1: characterization tests, judged on the ORIGINAL code ----
    report = m07.characterization_report(work)
    enough = report.n_tests >= 10
    results.append(Check(
        C_WROTE, enough,
        f"{report.n_tests} tests in {', '.join(report.tests)}" if report.tests else "no tests/test_ledger_*.py file was added yet",
        "" if enough else
        "Add more tests, one behaviour each: at least ten in all (every case of a parametrized test counts)." if report.tests else
        "Copy lab-assets/ledger_port.py to tests/ledger_port.py and write at least ten tests in new files named "
        "tests/test_ledger_*.py.",
    ))
    if not report.tests:
        waiting = "not checked yet: write your ledger tests first"
        results.append(Check(C_BASELINE, False, waiting, "Characterization tests come first, before you change any code."))
        results.append(Check(C_MUTANTS, False, waiting, "Once your tests pass on the original code, the grader breaks it sixteen ways and counts how many of your tests notice."))
        results.append(Check(C_MUTANTS_ALL, False, waiting, "Same check, all of them.", required=False))
    else:
        results.append(Check(
            C_BASELINE, report.ready,
            f"they pass on the code as it was at the start ({report.n_tests} tests)" if report.ready else report.problem,
            report.hint,
        ))
        if not report.ready:
            results.append(Check(C_MUTANTS, False, "not checked yet: fix the line above first", "Fix the line above first."))
            results.append(Check(C_MUTANTS_ALL, False, "not checked yet", required=False))
        else:
            total = len(report.killed) + len(report.survived)
            ok = len(report.killed) >= m07.MIN_KILLED
            missed = [m.description for m in report.survived]
            detail = f"your tests catch {len(report.killed)} of {total} deliberate defects"
            if missed:
                detail += f"; they miss: {checks._short(missed, 3)}"
            results.append(Check(C_MUTANTS, ok, detail,
                                 "" if ok else "For each behaviour the module docstring and your experiments reveal, ask: "
                                 "which test fails if it changes? Add exact expectations (values, order, errors)."))
            results.append(Check(C_MUTANTS_ALL, not report.survived, detail, "Add a test for each behaviour listed above.", required=False))

    # ---- the whole suite, and nothing deleted ----
    results.append(m07.suite_check(work, name=C_SUITE))
    deleted = m07.tests_not_deleted(work)
    results.append(Check(C_KEPT, not deleted, "; ".join(deleted) if deleted else "every starting test is still there",
                         "Tests may be edited to follow a rename, never removed to make the suite green."))

    # ---- Part 2: the refactor ----
    results.append(_hidden(work, "test_m07_ledger.py", C_QUIRKS,
                           "Compare what the old module did with what your Ledger does: run your characterization tests, "
                           "then read the docstring of the original ledger (git show lab-start:src/remit/ledger.py)."))
    results.append(_hidden(work, "test_m07_service.py", C_SERVICE,
                           "RemitService takes ledger=None (a fresh Ledger() each time), keeps it as self.ledger, and send() "
                           "still posts in the same order with the same ids."))
    source = (work / m07.LEDGER).read_text(encoding="utf-8") if (work / m07.LEDGER).is_file() else ""
    state = m07.module_state_problems(source) + [f"new module-level state in {entry}" for entry in m07.new_module_state(work)]
    results.append(Check(C_STATE, not state, "; ".join(state[:3]) if state else "no module-level state",
                         "Balances and the journal belong to a Ledger instance (self._balances), not to the module or the class."))
    legacy = m07.legacy_functions_left(source)
    results.append(Check(C_LEGACY, not legacy, f"still defined at module level: {', '.join(legacy)}" if legacy else "none left",
                         "RemitService gets its ledger passed in; delete the wrappers and reset() once nothing calls them."))

    # ---- Part 3: the migration ----
    left = m07.v1_calls_left(work)
    results.append(Check(C_V1CALLS, not left, f"{len(left)} left: {checks._short(left, 3)}" if left else "none left",
                         "Run pytest -W error::DeprecationWarning: it raises at the first old call a test reaches, and every test runs "
                         "tests/conftest.py first, so migrate that file before the rest. docs/najmkit-v2-migration.md has the new names. "
                         "A clock object's .now() method is not one of the renamed functions."))
    defined = m07.v1_names_still_defined(work)
    if defined is None:
        results.append(Check(C_V1GONE, False, "najmkit could not be imported", "Run python -c 'import najmkit.ids, najmkit.clock, najmkit.audit' with PYTHONPATH=src."))
    else:
        results.append(Check(C_V1GONE, not defined, f"still defined: {', '.join(defined)}" if defined else "all removed",
                             "Delete the section marked 'deprecated v1 names' in ids.py, clock.py and audit.py once nothing calls it."))
    results.append(_hidden(work, "test_m07_migration.py", C_AUDIT,
                           "Other teams parse these lines: they must be identical, character for character, to what Remit "
                           "wrote before the migration. Compare a line before and after."))
    results.append(_docs_check(work))

    # ---- process ----
    results.append(checks.files_changed_within(
        work, ALLOWED, name=C_SCOPE,
        hint="Undo what the ticket does not need, whether or not you committed it: git restore --source=lab-start -- <file> "
             "(git rm for a file you added), then commit."))
    results.append(checks.conventional_commits(work, name=C_MESSAGES))
    results.append(m07.small_steps(work, name=C_COUNT))
    if gitutil.commits_since(work):
        red, examined = m07.green_commits(work)
        results.append(Check(C_GREEN, not red, f"{examined} commits run, all green" if not red else f"red at: {checks._short(red, 3)}",
                             "Make each step small enough that pytest -q is green after it.", required=False))
    else:
        results.append(Check(C_GREEN, False, "no commits yet", "Commit each step when its tests are green.", required=False))
    results.append(checks.all_committed(work, name=C_CLEAN))
    results.append(checks.no_secrets(work, name=C_SECRETS))
    results.append(checks.sections_check(
        work, PLAN, PLAN_SECTIONS, min_words=6, name=C_PLAN, required=False,
        hint="Copy lab-assets/refactoring-plan-template.md to docs/refactoring-plan.md and fill in every section."))
    results.append(_stale_check(work))
    return results


def _docs_check(work: Path) -> Check:
    path = work / "docs" / "najmkit.md"
    if not path.is_file():
        return Check(C_DOCS, False, "docs/najmkit.md does not exist", "Keep the reference page and update it.", required=False)
    text = path.read_text(encoding="utf-8")
    old = sorted(set(re.findall(r"\b(new_id|use_generator|log_event|set_clock|get_clock|reset_clock)\b", text)))
    new = [name for name in ("make_id", "utc_now", "emit") if name not in text]
    problems = ([f"still describes: {', '.join(old)}"] if old else []) + ([f"does not mention: {', '.join(new)}"] if new else [])
    return Check(C_DOCS, not problems, "; ".join(problems) if problems else "describes the v2 names",
                 "A stale reference page is how the next agent (or colleague) learns the wrong names.", required=False)


def _stale_check(work: Path) -> Check:
    stale = m07.stale_document_lines(work)
    return Check(C_STALE, not stale, f"{stale[0][:110]}" + (f" (+{len(stale) - 1} more)" if len(stale) > 1 else "") if stale else "up to date",
                 "Documents go stale like code, and the next agent believes them. Fix the lines: README.md, docs/ARCHITECTURE.md, "
                 "docs/TOUR.md and CLAUDE.md all talk about the ledger.", required=False)


# ---------------------------------------------------------------------------------------------
# solve: the reference solution, one commit per step
# ---------------------------------------------------------------------------------------------
def _update_memory(work: Path) -> None:
    path = work / "CLAUDE.md"
    if not path.is_file():
        return
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    replaced = False
    for index, line in enumerate(lines):
        if _STALE_MEMORY.search(line):
            lines[index] = "" if replaced else NEW_MEMORY_LINE  # the new line says it all once
            replaced = True
    path.write_text("".join(lines), encoding="utf-8", newline="\n")


def solution_steps() -> list[dict]:
    """The reference solution, step by step: {"dir", "message", "files"} (files are relative to the repository)."""
    return json.loads((HERE / "solution" / "steps.json").read_text(encoding="utf-8"))


def step_file(step: dict, rel: str) -> Path:
    """Where a step's file is stored. The seam ``tests/ledger_port.py`` is the lab asset itself, not a second copy of it."""
    if rel == "tests/ledger_port.py":
        return HERE / "assets" / "ledger_port.py"
    return HERE / "solution" / step["dir"] / rel


def solve(work: Path) -> None:
    for number, step in enumerate(solution_steps()):
        for rel in step["files"]:
            target = work / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(step_file(step, rel), target)
        if step["dir"] == "04-remove-module-state":
            _update_memory(work)
        gitutil.commit_all(work, step["message"], author=LEARNER, date=f"2026-03-03T09:{10 + 5 * number:02d}:00+00:00")


LAB = Lab(
    id="m07",
    title="Tame an untested module, refactor it, then migrate a dependency",
    lesson="7.2",
    needs_agent=True,  # recommended: Part 3 is a textbook agent task; the no-agent path is the whole lab by hand
    seed=seed,
    grade=grade,
    solve=solve,
)
