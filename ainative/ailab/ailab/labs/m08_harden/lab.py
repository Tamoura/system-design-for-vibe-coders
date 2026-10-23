"""Lab m08 (lesson 8.2): "Harden your setup with permissions, a guard hook and a dependency check".

The story
---------
Noura's ticket REMIT-258: the repository should carry its own guard rails. The learner writes four things:

1. ``.claude/settings.json``: permission rules (deny what must never happen, allow only the narrow commands used all day)
   and the registration of a PreToolUse hook for the Bash tool;
2. ``.claude/hooks/guard.py``: a guard hook that reads the hook-input JSON on stdin and blocks dangerous shell commands
   with exit code 2 and a ``Blocked:`` reason, while letting harmless ones through (and failing closed on input it cannot read);
3. ``scripts/depcheck.py`` + ``deps-allowlist.txt``: a check that flags packages which are in neither the allow-list nor the
   lockfile, the guard against hallucinated or squatted package names;
4. ``injection-notes.md``: notes on a README (``lab-assets/vendor-readme/README.md``, constructed for teaching) in which five
   tricks aimed at an AI assistant are planted: an HTML comment, a visible "note for assistants", invisible Unicode tag
   characters, advice to switch permission checks off, and an install line with an unvetted package.

The starting state is the base repository plus ``lab-assets/`` (the guard skeleton, six sample hook inputs, the README, a sample
project with problems, a notes template) and a FAKE ``.env`` (git-ignored, one made-up line) for trying the deny rule on.

What is graded, and what cannot be
----------------------------------
All the logic lives in ``ailab/checks_m08.py``. In short: the settings are parsed and read as data; the guard is RUN against
``len(HOOK_CASES)`` sample hook inputs (the required ones and 4 advisory ones) in a subprocess with a time limit; the dependency
check is RUN against ``len(DEP_CASES)`` small projects built in temporary folders and on the learner's own repository; the notes
are checked for structure and for mentioning each planted trick. Nothing is imported in the grader's process and nothing from a
sample is ever executed. Every situation the grader tries is a rule that TASK.md states (plus the shapes the lesson explains); a
rule the grader enforces and TASK.md does not state is a bug. Situations TASK.md leaves open are not tried.

The grader checks the RESULT. It cannot tell whether Claude Code accepts the settings file, whether the sandbox is on, whether
the learner understood the README, or whether a rule that passes the samples is a good rule for a situation the samples do not
contain. The lesson says so, and the notes and the group session are where that judgement is practised.

Files
-----
    seed(work)    writes a fake, git-ignored ``.env`` (so the learner can watch a deny rule work); everything else arrives
                  in ``lab-assets/`` from ``assets/``.
    grade(work)   see above.
    solve(work)   applies ``solution/`` in five small commits (tests and code together, as CONTRIBUTING.md asks): the guard,
                  the dependency check, the settings, the CI step, the notes.
"""
from __future__ import annotations

import shutil
from dataclasses import replace
from pathlib import Path

from ailab import checks, checks_m08, framework, gitutil
from ailab.framework import Check, Lab

HERE = Path(__file__).resolve().parent
SOLUTION = HERE / "solution"
LEARNER = ("Najm Learner", "learner@najm.example")

FAKE_ENV = "# Fake, for lab m08 only: it is git-ignored, and it exists so you can watch your deny rule work.\nFAKE_KEY=not-a-real-secret\n"


def seed(work: Path) -> None:
    (Path(work) / ".env").write_text(FAKE_ENV, encoding="utf-8")


def scope_hint(check: Check) -> Check:
    """CONTRIBUTING.md lists example scopes; this lab's areas are not among them, and the rule accepts any lower-case scope."""
    if check.ok:
        return check
    note = (" The scope can be any lower-case word for the area you touched (security, hooks, deps, claude, docs...): "
            "CONTRIBUTING.md's list gives examples. The header is type(scope): subject, at most 72 characters, no full stop.")
    return replace(check, hint=check.hint + note)


def grade(work: Path) -> list[Check]:
    settings = checks_m08.load_settings(work)
    return [
        checks.tests_pass(work, name="Your tests pass"),
        # part 1: permission rules
        checks_m08.settings_json_check(settings),
        checks_m08.settings_rules_check(settings),
        checks_m08.credential_check(settings),
        checks_m08.dangerous_deny_check(settings),
        checks_m08.allow_door_check(settings),
        checks_m08.hook_registration_check(settings),
        checks_m08.network_advisory(settings),
        checks_m08.money_advisory(settings),
        # part 2: the guard hook (it is run against the sample inputs)
        *checks_m08.guard_checks(work),
        # part 3: the dependency check (it is run against small projects and against this repository)
        *checks_m08.depcheck_checks(work),
        # part 4: the notes
        *checks_m08.notes_checks(work),
        # hygiene
        checks_m08.existing_tests_untouched(work),
        checks_m08.own_tests_advisory(work),
        checks.files_changed_within(
            work,
            checks_m08.ALLOWED_FILES,
            name=checks_m08.N_SCOPE,
            hint="Allowed: .claude/ (settings and hook), scripts/, new files under tests/, deps-allowlist.txt, requirements.lock, "
                 "injection-notes.md, a CI step in .github/workflows/, docs/, top-level Markdown files and .gitignore. "
                 "Revert anything else (src/, pyproject.toml, an existing test) with git restore.",
        ),
        checks.no_secrets(work),
        scope_hint(checks.conventional_commits(work)),
        checks.commit_count(work, at_least=3, required=False, name="Small commits",
                            hint="One commit per part makes the review, and any revert, easy."),
        checks.all_committed(work),
    ]


def solve(work: Path) -> None:
    """The reference solution: the guard, the dependency check, the settings, a CI step, the notes: one commit each."""
    work = Path(work)

    def put(src: str, dest: str) -> None:
        target = work / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOLUTION / src, target)

    def commit(message: str, minute: int) -> None:
        gitutil.commit_all(work, message, author=LEARNER, date=f"2026-03-02T10:{minute:02d}:00+00:00")

    put("guard.py", ".claude/hooks/guard.py")
    put("test_guard.py", "tests/test_guard.py")
    commit("feat(security): add a guard hook that blocks dangerous shell commands", 0)

    put("depcheck.py", "scripts/depcheck.py")
    put("deps-allowlist.txt", "deps-allowlist.txt")
    put("test_depcheck.py", "tests/test_depcheck.py")
    commit("feat(security): add a dependency check and an allow-list", 10)

    put("settings.json", ".claude/settings.json")
    commit("chore(claude): add permission rules and register the guard hook", 20)

    framework.edit_file(
        work, ".github/workflows/ci.yml",
        "      - name: Run the tests\n        run: pytest -q\n",
        "      - name: Run the tests\n        run: pytest -q\n"
        "      - name: Check dependencies against the allow-list\n        run: python scripts/depcheck.py\n",
    )
    commit("ci(security): run the dependency check on every push", 30)

    put("injection-notes.md", "injection-notes.md")
    commit("docs(security): record what the csvtidy README tried to make an agent do", 40)


LAB = Lab(
    id="m08",
    title="Harden your setup: permissions, a guard hook, a dependency check",
    lesson="8.2",
    needs_agent=False,  # an agent can help, and the lesson suggests it; the grader cannot tell, and the lab works by hand
    seed=seed,
    grade=grade,
    solve=solve,
)
