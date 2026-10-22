"""Negative and alternative-solution tests for m02 (project memory for Remit).

The grader here is a *lint* of a Markdown file, so the interesting tests are of three kinds:

* the wrong files people and agents really write (a generic ``/init``-style file, a copy of the architecture
  doc, a file with a made-up ``make test``) and the one check that must catch each;
* the right files written differently (``AGENTS.md``, ``@AGENTS.md`` in ``CLAUDE.md``, ``.claude/CLAUDE.md``, a
  scoped rule) that must all pass, because a grader has to accept any sound solution;
* safety: the lint runs commands from a file the learner wrote, so a test proves that anything it does not
  recognise is never run.

Most tests call ``memory_checks`` with the command runner stubbed out (fast); the tests that need the real
execution ask for the ``real_commands`` fixture.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

import pytest

from ailab import checks_m02 as m, framework, gitutil
from ailab.checks_m02 import (
    N_COMMANDS, N_COMMITS, N_EXISTS, N_FIGURES, N_FILLER, N_MONEY, N_NAJMKIT, N_NEVER, N_NOTES, N_POINTERS,
    N_PYTHONPATH, N_QUOTES, N_RESTATE, N_SIZE, N_STALE, N_TESTS,
)
from conftest import learner_commit, start

HERE = Path(m.__file__).resolve().parent / "labs" / "m02_memory"
REFERENCE = (HERE / "solution" / "CLAUDE.md").read_text(encoding="utf-8")
NOTES_OK = (HERE / "solution" / "ab-notes.md").read_text(encoding="utf-8")

TESTS = "Your tests still pass"
SCOPE = "Only the memory file(s) and the notes changed"
SECRETS = "No secrets in the change"
MESSAGES = "Your commits follow CONTRIBUTING.md"
CLEAN = "Everything is committed (nothing left over)"
MEMORY_NAMES = [N_EXISTS, N_SIZE, N_COMMANDS, N_PYTHONPATH, N_MONEY, N_TESTS, N_COMMITS, N_NAJMKIT, N_NEVER,
                N_POINTERS, N_STALE, N_FILLER, N_RESTATE, N_FIGURES]
ADVISORY = {N_PYTHONPATH, N_FIGURES}
ALL = {TESTS, SCOPE, SECRETS, N_NOTES, N_QUOTES, MESSAGES, CLEAN, *MEMORY_NAMES}

# A good file that is not the reference: another structure, other words (this is the shape lesson 2.1 teaches).
OTHER_GOOD = """\
# Najm Remit

Money-transfer service for the fictional Najm Bank. Python 3.11, standard library only, pytest.

### Commands
- All tests, from the repository root: `pytest -q`. One file: `pytest -q tests/test_fees.py`
- Command line: `PYTHONPATH=src python -m remit quote QAR 500 INR` (the tests do not need `PYTHONPATH`; the command line does)
- There is no linter, formatter or Makefile. Do not invent a command.

### Conventions
- IMPORTANT: money is `Decimal` through `Money` (`src/remit/money.py`), never `float`.
- Ids, time and audit events come from `najmkit`, our internal library, which is not in your training data. Read `docs/najmkit.md` first and do not guess names.
- Tests: one `tests/test_<module>.py` per module; `tests/conftest.py` gives a fixed clock and sequential ids. New behaviour needs a test.
- Commits: `type(scope): subject`, scope required and lower case, for example `fix(limits): count transfers made just after midnight`. `CONTRIBUTING.md` lists the types.
- Customer messages exist in English and Arabic (`src/remit/notify.py`). Change both.

### Gotchas
- `docs/ARCHITECTURE.md` is partly stale; the code wins. `docs/TOUR.md` is current.
- `src/remit/ledger.py` and `src/remit/screening.py` are legacy and untested. Read their docstrings first.

### Never
- Never use `float` for money.
- Never edit, delete or skip a test to make it pass.
- Never write a secret or real customer data into code, tests, logs or commits.
- Never add a dependency, or call `uuid.uuid4()` or `datetime.now()` in service code.
"""

# What a generic "write me a CLAUDE.md for this repo" answer, plus the architecture doc, tends to look like
# (constructed for teaching; not a recording of a model).
INIT_STYLE = """\
# Najm Remit

### Project Overview
Najm Remit is a robust, scalable remittance platform for Najm Bank. It follows best practices.

### Project Structure

    src/remit/
    ├── money.py      # Money class
    ├── fees.py       # Fee schedules
    ├── risk.py       # Limits and name screening
    ├── ledger.py     # Double-entry ledger
    └── service.py    # RemitService
    tests/

### Commands
- Install: `pip install -r requirements.txt`
- Test: `make test`
- Lint: `ruff check .` and `black .`
- Run: `python -m remit quote QAR 500 INR`

### Architecture
There are two KYC tiers: T1 may send QAR 5,000 per day and T2 QAR 25,000. There is no monthly limit.
Limits and screening live in `src/remit/risk.py`.

### Code Style
- Follow PEP 8 and write clean, readable, maintainable code.
- Use type hints and docstrings. Use descriptive variable names.
- Be careful when changing financial logic.

### Git
- Use conventional commits, for example `feat: add quote endpoint`.
"""


# --------------------------------------------------------------------------------------------------------------
# fixtures and helpers
# --------------------------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def template(tmp_path_factory) -> Path:
    return start("m02", tmp_path_factory.mktemp("m02-template") / "work")


@pytest.fixture
def work(template, tmp_path) -> Path:
    """A private copy of the started lab (the .git folder and the lab-start tag come with it)."""
    target = tmp_path / "work"
    shutil.copytree(template, target)
    return target


@pytest.fixture(autouse=True)
def stub_commands(request, monkeypatch):
    """Most tests are about text, so the (slow) real execution of documented commands is replaced by 'it worked'."""
    if "real_commands" in request.fixturenames:
        return

    def fake(root, command, database, timeout=60.0):
        problem = m._pytest_args_problem(command.args) if command.kind == "pytest" else ""
        if problem:
            return m.Outcome(command, False, False, f"was not run: the grader does not accept {problem}")
        return m.Outcome(command, True, True)

    monkeypatch.setattr(m, "run_command", fake)


@pytest.fixture
def real_commands():
    return True


def put(work: Path, text: str, name: str = "CLAUDE.md") -> Path:
    path = work / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def lint(work: Path) -> dict[str, framework.Check]:
    return {c.name: c for c in m.memory_checks(work)}


def grade(work: Path) -> dict[str, framework.Check]:
    return {c.name: c for c in framework.grade_lab(framework.load_lab("m02"), work, catch=False)}


def failing(result, *, required_only: bool = False) -> set[str]:
    return {n for n, c in result.items() if not c.ok and (c.required or not required_only)}


def assert_only(result, *expected: str, among: list[str] | None = None) -> None:
    got = failing(result)
    if among is not None:
        got &= set(among)
    detail = "\n".join(f"  {'ok  ' if c.ok else 'FAIL'} {n}: {c.detail}" for n, c in result.items())
    assert got == set(expected), f"expected failures {set(expected)}, got {got}\n{detail}"


def replace(text: str, old: str, new: str) -> str:
    assert old in text, f"test bug: {old!r} is not in the text"
    return text.replace(old, new)


# --------------------------------------------------------------------------------------------------------------
# the starter and the right answers
# --------------------------------------------------------------------------------------------------------------
def test_the_starter_fails_for_the_right_reasons(work):
    result = grade(work)
    assert set(result) == ALL
    ok_at_start = {TESTS, SECRETS, CLEAN}
    assert failing(result, required_only=True) == ALL - ok_at_start - ADVISORY
    assert all(c.hint or c.detail for c in result.values() if not c.ok)
    assert result[N_EXISTS].hint  # the first thing to do is spelled out
    assert "20 TODO" in result[N_NOTES].detail or "TODO" in result[N_NOTES].detail


def test_the_reference_solution_passes_every_check_even_the_advisory_ones(work):
    framework.solve_lab(framework.load_lab("m02"), work)
    result = grade(work)
    assert_only(result)
    assert gitutil.current_branch(work) == "main" and len(gitutil.commits_since(work)) == 2


def test_the_reference_memory_is_lean_and_what_later_labs_receive(work, tmp_path):
    lines = [ln for ln in REFERENCE.splitlines() if ln.strip()]
    assert 20 <= len(lines) <= 80, "the reference memory should model a lean file"
    target = tmp_path / "later-lab"
    target.mkdir()
    assert framework.add_reference_memory(target) is True
    assert (target / "CLAUDE.md").read_text(encoding="utf-8") == REFERENCE


def test_a_different_good_file_in_claude_md_is_accepted(work):
    put(work, OTHER_GOOD)
    assert_only(lint(work))


def test_agents_md_alone_is_accepted(work):
    put(work, OTHER_GOOD, "AGENTS.md")
    result = lint(work)
    assert_only(result)
    assert result[N_EXISTS].detail == "AGENTS.md"


def test_the_shared_file_pattern_claude_md_importing_agents_md_is_accepted(work):
    put(work, OTHER_GOOD, "AGENTS.md")
    put(work, "# Najm Remit\n\n@AGENTS.md\n")
    result = lint(work)
    assert_only(result)
    assert "AGENTS.md" in result[N_SIZE].detail or result[N_SIZE].ok  # the import is counted, not hidden


def test_agents_md_is_ignored_when_claude_md_does_not_import_it_and_the_learner_is_told(work):
    put(work, REFERENCE)
    put(work, "# Notes for other tools\n" + "\n".join(f"- line {i} of a second file" for i in range(20)), "AGENTS.md")
    result = lint(work)
    assert_only(result)
    assert "AGENTS.md exists but is ignored" in result[N_EXISTS].detail


def test_a_dot_claude_folder_memory_with_a_scoped_rule_is_accepted(work):
    """The commit rule lives only in a path-scoped rule: it still counts, but not toward the always-loaded size."""
    main = REFERENCE
    commit_line = next(ln for ln in main.splitlines() if ln.startswith("- Commits are"))
    main = main.replace(commit_line + "\n", "")
    put(work, main, ".claude/CLAUDE.md")
    put(work, "---\npaths:\n  - \"**\"\n---\n" + commit_line + "\n", ".claude/rules/commits.md")
    result = lint(work)
    assert_only(result)


def test_a_scoped_rule_does_not_count_toward_the_launch_size(work):
    put(work, REFERENCE)
    padding = "\n".join(f"- Rule number {i}: keep step {i} separate from step {i + 1}." for i in range(200))
    put(work, "---\npaths:\n  - \"docs/**\"\n---\n" + padding + "\n", ".claude/rules/many.md")
    assert lint(work)[N_SIZE].ok
    put(work, padding + "\n", ".claude/rules/many.md")  # without paths: it is loaded at launch
    assert not lint(work)[N_SIZE].ok


# --------------------------------------------------------------------------------------------------------------
# the typical wrong file: generic, copied from the architecture doc, commands that do not exist
# --------------------------------------------------------------------------------------------------------------
def test_an_init_style_file_fails_for_the_expected_reasons(work):
    put(work, INIT_STYLE)
    result = lint(work)
    assert_only(result, N_COMMANDS, N_PYTHONPATH, N_MONEY, N_TESTS, N_COMMITS, N_NAJMKIT, N_NEVER, N_POINTERS, N_STALE,
                N_FILLER, N_RESTATE, N_FIGURES)
    assert "make" in result[N_COMMANDS].detail and "ruff" in result[N_COMMANDS].detail
    assert "risk.py" in result[N_POINTERS].detail and "requirements.txt" in result[N_POINTERS].detail
    assert "best practices" in result[N_FILLER].detail
    assert all(result[n].hint for n in failing(result))
    assert result[N_SIZE].ok  # it is not too long: size alone is a poor judge of a memory file


def test_the_failure_messages_never_hand_over_the_answer(work):
    put(work, INIT_STYLE)
    text = " ".join(c.detail + " " + c.hint for c in lint(work).values())
    for giveaway in ("Decimal(", "src/remit/limits.py", "docs/najmkit.md", "pytest -q"):
        assert giveaway not in text, giveaway


def test_copying_the_architecture_doc_in_with_an_import_brings_its_stale_facts(work):
    put(work, REFERENCE.rstrip() + "\n\n@docs/ARCHITECTURE.md\n")
    result = lint(work)
    assert {N_STALE, N_POINTERS} <= failing(result)
    assert N_COMMANDS not in failing(result)


def test_pasting_the_readme_and_contributing_into_the_file_is_restating(work):
    pasted = (work / "CONTRIBUTING.md").read_text(encoding="utf-8")
    put(work, REFERENCE.rstrip() + "\n\n" + pasted)
    result = lint(work)
    assert N_RESTATE in failing(result)
    assert "copied word for word" in result[N_RESTATE].detail


def test_a_directory_tree_without_a_code_fence_is_restating_too(work):
    put(work, REFERENCE.rstrip() + "\n\n## Layout\n\n    src/remit/\n    ├── money.py\n    └── fees.py\n")
    assert_only(lint(work), N_RESTATE)


def test_a_directory_tree_is_restating(work):
    put(work, REFERENCE.rstrip() + "\n\n```text\nsrc/remit/\n├── money.py\n└── fees.py\n```\n")
    assert_only(lint(work), N_RESTATE)


def test_a_bullet_per_file_is_restating(work):
    lines = "\n".join(f"- `src/remit/{n}.py`: the {n} module" for n in
                      ("money", "corridors", "fees", "fx", "limits", "ledger", "store", "notify", "service", "cli", "config", "models"))
    put(work, REFERENCE.rstrip() + "\n\n## Modules\n" + lines + "\n")
    assert_only(lint(work), N_RESTATE)


# --------------------------------------------------------------------------------------------------------------
# one change, one failing check
# --------------------------------------------------------------------------------------------------------------
def test_removing_the_pythonpath_hint_only_costs_the_advisory_check(work):
    text = replace(REFERENCE, "`PYTHONPATH=src python -m remit quote", "`python -m remit quote")
    text = replace(text, "The tests do not need `PYTHONPATH`; `python -m remit` does.", "That is how the CLI runs.")
    put(work, text)
    result = lint(work)
    assert_only(result, N_PYTHONPATH)
    assert not result[N_PYTHONPATH].required


def test_a_made_up_make_target_fails_the_commands(work):
    put(work, replace(REFERENCE, "- There is no linter", "- Lint: `make lint`\n- There is no linter"))
    result = lint(work)
    assert_only(result, N_COMMANDS)
    assert "make lint" in result[N_COMMANDS].detail


def test_a_tool_the_repo_does_not_use_but_a_repo_that_does_may_document(work):
    put(work, replace(REFERENCE, "- There is no linter", "- Format: `black .`\n- There is no linter"))
    assert_only(lint(work), N_COMMANDS)
    (work / "pyproject.toml").write_text((work / "pyproject.toml").read_text() + "\n[tool.black]\nline-length = 100\n")
    assert N_COMMANDS not in failing(lint(work))  # now the repo does use black: the grader no longer calls it invented


def test_an_option_the_grader_does_not_know_is_a_failure_not_a_free_pass(work):
    put(work, replace(REFERENCE, "- There is no linter", "- Coverage: `pytest -q --cov=src`\n- There is no linter"))
    result = lint(work)
    assert_only(result, N_COMMANDS)
    assert "--cov" in result[N_COMMANDS].detail


def test_known_safe_pytest_options_are_accepted(work):
    extra = "- Faster: `pytest -q -x --tb=short -k fee` or `pytest -q -p no:randomly --maxfail=2`\n- There is no linter"
    put(work, replace(REFERENCE, "- There is no linter", extra))
    assert_only(lint(work))


def test_a_file_with_no_test_command_fails_the_commands(work):
    text = "\n".join(ln for ln in REFERENCE.splitlines() if "pytest" not in ln)
    put(work, text + "\n")
    result = lint(work)
    assert N_COMMANDS in failing(result)
    assert "does not say how to run the tests" in result[N_COMMANDS].detail


def test_test_commands_that_are_only_templates_do_not_count(work):
    text = "\n".join(ln for ln in REFERENCE.splitlines() if "pytest" not in ln)
    put(work, text + "\n\n## Tests\n- Run them with `pytest -q tests/test_<module>.py`\n")
    result = lint(work)
    assert "templates with placeholders" in result[N_COMMANDS].detail


def test_money_may_not_be_float(work):
    old = next(ln for ln in REFERENCE.splitlines() if ln.startswith("- IMPORTANT: money"))
    put(work, replace(REFERENCE, old, "- Money is `Decimal`. Use float when you need a percentage."))
    result = lint(work)
    assert N_MONEY in failing(result)
    assert "allows float" in result[N_MONEY].detail


def test_money_must_say_decimal_and_forbid_float(work):
    old = next(ln for ln in REFERENCE.splitlines() if ln.startswith("- IMPORTANT: money"))
    put(work, replace(REFERENCE, old, "- Money goes through `Money`."))
    assert N_MONEY in failing(lint(work))


@pytest.mark.parametrize(
    "line,needle",
    [
        ("- Commits follow Conventional Commits, for example `feat: add the quote endpoint`.", "without a scope"),
        ("- Commits are `type(scope): subject`; the scope is optional.", "optional"),
        ("- Commits are `type(scope): subject`. Types: feat, fix, style, wip, docs, test.", "does not allow"),
        ("- Write good commit messages.", "format with a scope"),
    ],
    ids=["no-scope-example", "optional-scope", "foreign-type", "no-format"],
)
def test_commit_rules_that_contradict_contributing_md(work, line, needle):
    old = next(ln for ln in REFERENCE.splitlines() if ln.startswith("- Commits are"))
    put(work, replace(REFERENCE, old, line))
    result = lint(work)
    assert_only(result, N_COMMITS)
    assert needle in result[N_COMMITS].detail


def test_a_test_framework_the_repo_does_not_use(work):
    put(work, replace(REFERENCE, "- Tests: pytest, one file per module", "- Tests: unittest classes, one file per module"))
    assert N_TESTS in failing(lint(work))


def test_najmkit_must_be_mentioned_and_pointed_to(work):
    text = replace(REFERENCE, "Read `docs/najmkit.md` for the exact names; do not guess them. ", "")
    text = text.replace("- `docs/najmkit.md` before you touch ids, time or audit events.\n", "")
    put(work, text)
    result = lint(work)
    assert_only(result, N_NAJMKIT)
    assert "does not point" in result[N_NAJMKIT].detail
    put(work, "\n".join(ln for ln in REFERENCE.splitlines() if "najmkit" not in ln.lower()) + "\n")
    assert "not mentioned" in lint(work)[N_NAJMKIT].detail


@pytest.mark.parametrize("invented", ["audit.write", "ids.generate", "clock.utcnow", "clock.freeze", "ids.new_uuid"])
def test_a_najmkit_function_an_agent_would_invent_is_caught(work, invented):
    put(work, REFERENCE.rstrip() + f"\n\n## Audit\n- Record events with `{invented}`.\n")
    result = lint(work)
    assert N_NAJMKIT in failing(result)
    assert invented in result[N_NAJMKIT].detail


def test_real_najmkit_names_and_file_names_that_look_like_them_are_fine(work):
    extra = "\n- Use `ids.new_id`, `clock.now` and `audit.log_event`; the audit file is `audit.jsonl` and `clock.py` is tiny.\n"
    put(work, REFERENCE.rstrip() + extra)
    assert_only(lint(work))


def test_no_never_list_fails(work):
    kept = [ln for ln in REFERENCE.splitlines() if not re.match(r"\s*(?:- )?(Never|Do not|IMPORTANT)", ln) and ln != "## Never"]
    put(work, "\n".join(kept) + "\n")
    assert N_NEVER in failing(lint(work))


def test_a_generic_never_list_fails(work):
    generic = "## Never\n- Never write bad code.\n- Never be sloppy.\n- Never break the build.\n"
    text = REFERENCE[: REFERENCE.index("## Never")] + generic
    put(work, text)
    result = lint(work)
    assert N_NEVER in failing(result)
    assert "specific" in result[N_NEVER].detail


def test_a_never_list_that_is_a_wall_of_rules_fails(work):
    wall = "\n".join(f"- Never use `float` for money in module number {i}." for i in range(14))
    text = REFERENCE[: REFERENCE.index("## Never")] + "## Never\n" + wall + "\n"
    put(work, text)
    result = lint(work)
    assert N_NEVER in failing(result)
    assert "stops being read" in result[N_NEVER].hint or "too long" in result[N_NEVER].detail or "long" in result[N_NEVER].detail


def test_words_with_a_slash_that_are_not_files_are_not_pointers(work):
    extra = "\n- Branch from `origin/main`; fill in `yes/no` and `and/or` cells; write `n/a` when unknown.\n"
    put(work, REFERENCE.rstrip() + extra)
    assert_only(lint(work))


def test_a_folder_that_does_not_exist_is_a_missing_pointer_even_without_a_file_name(work):
    put(work, REFERENCE.rstrip() + "\n- Unit tests live in `test/` and examples in `docs/examples`.\n")
    result = lint(work)
    assert_only(result, N_POINTERS)
    assert "test/" in result[N_POINTERS].detail and "docs/examples" in result[N_POINTERS].detail


def test_several_rules_on_one_line_count_one_by_one(work):
    line = "Never use `float` for money. Never edit a test to make it pass; never commit a secret."
    assert len(m._rules_in(line)) == 3
    assert len(m._rules_in("- Money is `Decimal`, never `float` (see `money.py`).")) == 0  # a rule inside a sentence is not a list item
    put(work, REFERENCE[: REFERENCE.index("## Never")] + "## Never\n" + line + "\n")
    assert N_NEVER not in failing(lint(work))


def test_the_tests_folder_can_be_named_in_words(work):
    put(work, replace(REFERENCE, "one file per module in `tests/` (", "one file per module in the `tests` folder ("))
    assert N_TESTS not in failing(lint(work))


def test_saying_that_a_tool_or_file_does_not_exist_is_not_documenting_it(work):
    """The template tells the learner to list the tools that do not exist; the lint must not punish that."""
    extra = ("\n- There is no `Makefile`, no `ruff` and no `requirements.txt`; do not use `make`.\n"
             "- `docs/ARCHITECTURE.md` lists a `risk.py` that does not exist.\n"
             "- Never create `docs/adr/` or `src/utils.py` without a ticket.\n")
    put(work, REFERENCE.rstrip() + extra)
    result = lint(work)
    assert_only(result)


def test_a_command_under_a_never_heading_is_a_warning_not_a_command(work):
    extra = "\n## Never run\n- `make test`\n```bash\nruff check .\n```\n"
    put(work, REFERENCE.rstrip() + extra)
    assert N_COMMANDS not in failing(lint(work))


def test_a_command_with_a_negation_after_it_is_still_a_command(work):
    """'(no network needed)' after a command must not hide it: a broken command there still fails."""
    put(work, replace(REFERENCE, "- There is no linter", "- Format: `black .` (no network needed)\n- There is no linter"))
    assert N_COMMANDS in failing(lint(work))


@pytest.mark.parametrize("line", [
    "- `make`, `ruff` and `black` are not used here. Do not invent a command.",
    "- Lint and format: none configured (`ruff` and `make` are absent).",
])
def test_a_bare_tool_name_followed_by_an_absence_is_a_statement_not_a_command(work, line):
    """'`ruff` is not used' names the tool to say it is not there; with arguments it would still be a command."""
    put(work, replace(REFERENCE, "- There is no linter", line + "\n- There is no linter"))
    assert_only(lint(work))


def test_a_bare_tool_name_without_any_absence_word_is_still_a_command(work):
    put(work, replace(REFERENCE, "- There is no linter", "- Lint: `ruff`\n- There is no linter"))
    result = lint(work)
    assert_only(result, N_COMMANDS)
    assert "ruff" in result[N_COMMANDS].detail


@pytest.mark.parametrize("line", [
    "- Commits are `type(scope): subject`. The scope is required, not optional, and lower case.",
    "- Commits are `type(scope): subject`; the scope is never optional.",
    "- Commits are `type(scope): subject`. Types: feat, fix, docs, test, refactor, perf, chore, ci, build, revert (there is no `style` type).",
], ids=["required-not-optional", "never-optional", "negated-foreign-type"])
def test_a_negated_mention_of_an_optional_scope_or_a_foreign_type_is_not_a_contradiction(work, line):
    old = next(ln for ln in REFERENCE.splitlines() if ln.startswith("- Commits are"))
    put(work, replace(REFERENCE, old, line))
    assert_only(lint(work))


def test_a_scope_that_is_not_required_is_still_wrong(work):
    old = next(ln for ln in REFERENCE.splitlines() if ln.startswith("- Commits are"))
    put(work, replace(REFERENCE, old, "- Commits are `type(scope): subject`, but the scope is not required."))
    result = lint(work)
    assert_only(result, N_COMMITS)
    assert "optional" in result[N_COMMITS].detail


@pytest.mark.parametrize("rules", [
    "- IMPORTANT: never use `float` for money.\n- IMPORTANT: never edit a test to make it pass.\n",
    "- Money must not be a `float`.\n- A test must not be edited or skipped to make it pass.\n",
    "- Money is never a `float`.\n- Secrets are never committed to this repository.\n",
], ids=["marker", "must-not", "is-never"])
def test_prohibitions_with_a_marker_or_a_modal_verb_count_as_never_rules(work, rules):
    kept = [ln for ln in REFERENCE.splitlines() if not re.match(r"\s*(?:- )?(Never|Do not|IMPORTANT)", ln) and ln != "## Never"]
    put(work, "\n".join(kept) + "\n\n## Boundaries and rules\n" + rules)
    assert N_NEVER not in failing(lint(work))


def test_modal_wording_inside_ordinary_prose_is_not_a_prohibition(work):
    assert m._rules_in("- The tests do not need `PYTHONPATH`; the command line does.") == []
    assert m._rules_in("- Remit never loads a `.env` file.") == []
    assert len(m._rules_in("- Money must not be a `float`.")) == 1


def test_pointing_to_a_file_that_does_not_exist_fails(work):
    put(work, REFERENCE.rstrip() + "\n- Design notes: `docs/DESIGN.md`.\n")
    result = lint(work)
    assert_only(result, N_POINTERS)
    assert "docs/DESIGN.md" in result[N_POINTERS].detail


def test_a_typo_in_a_test_file_name_fails_the_pointer_and_the_command(work):
    put(work, replace(REFERENCE, "tests/test_fees.py`", "tests/test_fee.py`"))
    assert {N_POINTERS} <= failing(lint(work))


def test_pointers_to_ignored_and_template_paths_are_fine(work):
    extra = "\n- Local files that are never committed: `.env`, `remit.db` and `audit.jsonl`. Tests: `tests/test_<module>.py`, `src/remit/*.py`, `tests/`.\n"
    put(work, REFERENCE.rstrip() + extra)
    assert_only(lint(work))


def test_a_pytest_node_id_and_a_file_line_reference_resolve(work):
    extra = "\n- Look at `src/remit/service.py:120` and `tests/test_fees.py::test_a_higher_amount_never_costs_less`.\n"
    put(work, REFERENCE.rstrip() + extra)
    assert_only(lint(work))


def test_too_few_pointers_fails(work):
    text = "\n".join(re.sub(r"`[^`]*/[^`]*`|`[\w.]+\.(?:md|toml|py)`", "the file", ln) for ln in REFERENCE.splitlines())
    put(work, text + "\n")
    result = lint(work)
    assert N_POINTERS in failing(result)
    assert "at least" in result[N_POINTERS].detail


def test_stale_facts_from_the_architecture_doc_are_caught(work):
    put(work, REFERENCE.rstrip() + "\n- Limits: T1 customers may send QAR 5,000 per day and there is no monthly limit.\n")
    result = lint(work)
    assert N_STALE in failing(result)
    assert N_FIGURES in failing(result)  # the advisory one agrees: business figures do not belong in memory


def test_a_line_that_says_the_doc_is_out_of_date_is_not_a_stale_claim(work):
    put(work, REFERENCE.rstrip() + "\n- The architecture doc says there is no monthly limit; that is out of date, the code wins.\n")
    assert N_STALE not in failing(lint(work))


@pytest.mark.parametrize(
    "phrase",
    ["Follow best practices.", "Write clean, maintainable code.", "You are an expert Python engineer.", "Follow PEP 8.",
     "Use type hints everywhere.", "Apply SOLID and DRY.", "Think step by step.", "Add docstrings to every function."],
)
def test_filler_is_caught(work, phrase):
    put(work, REFERENCE.rstrip() + f"\n- {phrase}\n")
    result = lint(work)
    assert_only(result, N_FILLER)


def test_the_word_docstrings_in_a_real_gotcha_is_not_filler(work):
    put(work, REFERENCE)
    assert N_FILLER not in failing(lint(work))  # the reference says "module docstrings list known quirks"


def test_too_short_fails_the_size(work):
    put(work, "# Najm Remit\n\nRun `pytest -q`. Money is Decimal.\n")
    result = lint(work)
    assert N_SIZE in failing(result) and "too few" in result[N_SIZE].detail


def test_too_long_fails_the_size_and_only_the_size(work):
    padding = "\n".join(f"- Remember number {i}: the quote shown in step {i} is the quote used in step {i + 1}." for i in range(130))
    put(work, REFERENCE.rstrip() + "\n\n## Reminders\n" + padding + "\n")
    result = lint(work)
    assert_only(result, N_SIZE)
    assert "200" in result[N_SIZE].hint


def test_an_empty_or_blank_memory_file_counts_as_missing(work):
    put(work, "\n\n   \n")
    assert N_EXISTS in failing(lint(work))


# --------------------------------------------------------------------------------------------------------------
# the commands: really executed, and only the ones the grader recognises
# --------------------------------------------------------------------------------------------------------------
def test_documented_commands_really_run(work, real_commands):
    put(work, REFERENCE)
    result = lint(work)
    assert result[N_COMMANDS].ok and "4 commands ran" in result[N_COMMANDS].detail


def test_a_documented_test_file_that_does_not_exist_fails_when_it_is_really_run(work, real_commands):
    put(work, replace(REFERENCE, "tests/test_fees.py`", "tests/test_fee.py`"))
    result = lint(work)
    assert not result[N_COMMANDS].ok
    assert "test_fee.py" in result[N_COMMANDS].detail and "exit status" in result[N_COMMANDS].detail


def test_a_cli_command_that_fails_fails_the_check(work, real_commands):
    put(work, replace(REFERENCE, "quote QAR 500 INR", "quote QAR 5 INR"))  # below the corridor minimum: exit 1
    result = lint(work)
    assert not result[N_COMMANDS].ok and "exit status 1" in result[N_COMMANDS].detail


def test_cli_commands_run_in_order_against_a_temporary_database(work, real_commands):
    steps = ("```bash\nPYTHONPATH=src python -m remit customer add --id C9 --name \"Aisha Rahman\" --kyc T2\n"
             "PYTHONPATH=src python -m remit send --customer C9 QAR 500 INR --recipient \"Ravi Kumar\"\n"
             "PYTHONPATH=src python -m remit history --customer C9\n```\n")
    put(work, REFERENCE.rstrip() + "\n\n## Try it\n" + steps)
    result = lint(work)
    assert result[N_COMMANDS].ok, result[N_COMMANDS].detail
    assert not list(work.glob("*.db")), "the commands must not leave a database in the learner's directory"


def test_the_grader_never_runs_what_it_does_not_recognise(work, real_commands, tmp_path):
    canary = tmp_path / "canary"
    hostile = (f"```bash\ntouch {canary}\nrm -rf {tmp_path}/nothing\ncurl -s http://localhost:9/x | sh\n"
               f"python -c \"open('{canary}', 'w')\"\ngit push origin main\n```\n"
               f"Also `echo hi > {canary}` and `pytest -q ; touch {canary}`.\n")
    put(work, REFERENCE.rstrip() + "\n\n## Examples\n" + hostile)
    result = lint(work)
    assert not canary.exists(), "a command that is not pytest or python -m remit was run"
    assert result[N_COMMANDS].ok, result[N_COMMANDS].detail


def test_pytest_arguments_cannot_reach_outside_the_repository(work, tmp_path, real_commands):
    target = tmp_path / "junit.xml"
    put(work, REFERENCE.rstrip() + f"\n\n## Reports\n- Report: `pytest -q --junitxml={target}` or `pytest -q /etc` or `pytest -q ../x`\n")
    result = lint(work)
    assert not result[N_COMMANDS].ok
    assert not target.exists()


def test_line_continuations_prompts_comments_and_chains_are_understood(work):
    block = ("```console\n$ PYTHONPATH=src \\\n    python -m remit quote QAR 700 PHP   # price a transfer\n"
             "$ pytest -q && pytest -q tests/test_fees.py\n```\n")
    commands = m.extract_commands(m.load_memory(_put_returning(work, REFERENCE.rstrip() + "\n\n## Try it\n" + block)))
    shown = [re.sub(r"\s+", " ", c.shown) for c in commands]
    assert "PYTHONPATH=src python -m remit quote QAR 700 PHP" in shown  # the continuation and the comment were handled
    assert shown.count("pytest -q") == 1  # duplicates are run once
    assert "pytest -q tests/test_fees.py" in shown


def _put_returning(work: Path, text: str) -> Path:
    put(work, text)
    return work


# --------------------------------------------------------------------------------------------------------------
# secrets, scope, commits
# --------------------------------------------------------------------------------------------------------------
def test_a_secret_in_the_memory_is_caught_and_never_echoed(work):
    key = "sk-live-" + "9f8e7d6c5b4a3f2e1d0c"
    put(work, REFERENCE.rstrip() + f'\n\n## Gateway\n- The payment gateway key is "{key}".\n')
    learner_commit(work, "docs(memory): add project memory")
    result = grade(work)
    assert SECRETS in failing(result)
    assert "9f8e7d6c" not in result[SECRETS].detail + result[SECRETS].hint


def test_changing_source_or_tests_fails_the_scope(work):
    put(work, REFERENCE)
    framework.edit_file(work, "src/remit/notify.py", "recieved", "received") if "recieved" in (work / "src/remit/notify.py").read_text() else \
        (work / "src/remit/notify.py").write_text((work / "src/remit/notify.py").read_text() + "\n# a tidy-up the ticket did not ask for\n")
    learner_commit(work, "docs(memory): add project memory")
    result = grade(work)
    assert SCOPE in failing(result)
    assert "src/remit/notify.py" in result[SCOPE].detail


def test_fixing_the_architecture_doc_in_this_pull_request_fails_the_scope_with_a_kind_hint(work):
    put(work, REFERENCE)
    framework.edit_file(work, "docs/ARCHITECTURE.md", "| `risk.py` |", "| `limits.py` |")
    learner_commit(work, "docs(memory): add project memory")
    result = grade(work)
    assert SCOPE in failing(result) and "another ticket" in result[SCOPE].hint


def test_extra_claude_settings_are_out_of_scope_here(work):
    put(work, REFERENCE)
    put(work, '{"permissions": {"deny": ["Read(./.env)"]}}', ".claude/settings.json")
    learner_commit(work, "docs(memory): add project memory")
    assert SCOPE in failing(grade(work))


def test_tool_noise_does_not_count_against_the_learner(work):
    put(work, REFERENCE)
    learner_commit(work, "docs(memory): add project memory")
    put(work, "{}", ".claude/settings.local.json")
    (work / ".DS_Store").write_bytes(b"\0")
    assert SCOPE not in failing(grade(work))


def test_an_uncommitted_memory_fails_the_hygiene_checks_only(work):
    put(work, REFERENCE)
    shutil.copyfile(HERE / "solution" / "ab-notes.md", work / "ab-notes.md")
    result = grade(work)
    assert_only(result, MESSAGES, CLEAN)


@pytest.mark.parametrize("message", ["added a CLAUDE.md", "docs: add project memory", "Docs(memory): Add it", "docs(memory): add it."],
                         ids=["no-convention", "no-scope", "wrong-case", "full-stop"])
def test_commit_messages_that_ignore_contributing_md(work, message):
    put(work, REFERENCE)
    shutil.copyfile(HERE / "solution" / "ab-notes.md", work / "ab-notes.md")
    learner_commit(work, message)
    result = grade(work)
    assert_only(result, MESSAGES)
    assert "CONTRIBUTING.md" in result[MESSAGES].hint


def test_one_commit_for_everything_is_fine(work):
    put(work, REFERENCE)
    shutil.copyfile(HERE / "solution" / "ab-notes.md", work / "ab-notes.md")
    learner_commit(work, "docs(memory): add project memory and the A/B notes")
    assert_only(grade(work))


# --------------------------------------------------------------------------------------------------------------
# the A/B notes
# --------------------------------------------------------------------------------------------------------------
def notes_result(work: Path, text: str) -> dict[str, framework.Check]:
    put(work, REFERENCE)
    put(work, text, "ab-notes.md")
    learner_commit(work, "docs(memory): add project memory")
    return grade(work)


def test_filled_notes_pass(work):
    result = notes_result(work, NOTES_OK)
    assert_only(result)


def test_the_template_as_it_is_fails(work):
    put(work, REFERENCE)
    learner_commit(work, "docs(memory): add project memory")
    result = grade(work)
    assert_only(result, N_NOTES, N_QUOTES)
    assert "TODO" in result[N_NOTES].detail


def test_notes_may_report_no_difference(work):
    same = re.sub(r"(\| [^|]+ \| )(\w+)( \| )(\w+)( \|)", lambda mm: mm.group(1) + mm.group(2) + mm.group(3) + mm.group(2) + mm.group(5), NOTES_OK)
    same = same.replace("In A the agent", "In both runs the agent")  # prose only has to be present
    assert_only(notes_result(work, same))


def test_a_missing_row_or_a_word_where_a_number_belongs_fails(work):
    result = notes_result(work, replace(NOTES_OK, "| 22 | 14 |", "| long | quick |"))
    assert N_NOTES in failing(result) and "whole number" in result[N_NOTES].detail


def test_a_missing_table_row_fails(work):
    text = "\n".join(ln for ln in NOTES_OK.splitlines() if "Wrong turns" not in ln)
    result = notes_result(work, text)
    assert N_NOTES in failing(result) and "Wrong turns" in result[N_NOTES].detail


def test_yes_or_no_cells_are_checked(work):
    result = notes_result(work, replace(NOTES_OK, "| yes | yes |", "| green | red |"))
    assert N_NOTES in failing(result) and "yes or no" in result[N_NOTES].detail


def test_a_missing_section_fails(work):
    text = NOTES_OK[: NOTES_OK.index("## Limits of this comparison")]
    result = notes_result(work, text)
    assert N_NOTES in failing(result) and "limits" in result[N_NOTES].detail.lower()


def test_one_word_sections_fail(work):
    text = re.sub(r"(## What was different\n\n)(.*?)(\n\n## )", r"\1Better.\3", NOTES_OK, flags=re.S)
    result = notes_result(work, text)
    assert N_NOTES in failing(result) and "too short" in result[N_NOTES].detail


def test_a_paraphrased_quote_cannot_be_checked(work):
    text = re.sub(r"(## The memory line that mattered\n\n)> .*\n", r"\1> The one about money being decimal.\n", NOTES_OK)
    result = notes_result(work, text)
    assert N_QUOTES in failing(result) and "not in your memory" in result[N_QUOTES].detail


def test_a_quote_from_somewhere_else_fails(work):
    text = re.sub(r"(## A memory line that changed nothing\n\n)> .*\n", r"\1> Tests deliberately fail on Fridays at noon.\n", NOTES_OK)
    result = notes_result(work, text)
    assert N_QUOTES in failing(result)


def test_a_quote_without_a_quote_mark_fails(work):
    text = re.sub(r"(## The memory line that mattered\n\n)> .*\n", r"\1The money line mattered a lot to the agent here.\n", NOTES_OK)
    result = notes_result(work, text)
    assert N_QUOTES in failing(result) and "no quoted line" in result[N_QUOTES].detail


def test_quoting_a_line_you_deleted_after_the_experiment_is_the_point_and_passes(work):
    """Pruning is the lesson: the line that changed nothing is deleted in a later commit, and the quote still checks out."""
    put(work, REFERENCE)
    put(work, NOTES_OK, "ab-notes.md")
    learner_commit(work, "docs(memory): add project memory")
    pruned = "\n".join(ln for ln in REFERENCE.splitlines() if "English and Arabic" not in ln) + "\n"
    put(work, pruned)
    learner_commit(work, "docs(memory): prune a line that changed nothing")
    result = grade(work)
    assert_only(result)


def test_notes_without_a_memory_file_wait_for_one(work):
    put(work, NOTES_OK, "ab-notes.md")
    learner_commit(work, "docs(notes): record the comparison")
    result = grade(work)
    assert result[N_QUOTES].detail == m.WAITING


def test_the_notes_file_deleted_fails_cleanly(work):
    put(work, REFERENCE)
    (work / "ab-notes.md").unlink()
    learner_commit(work, "docs(memory): add project memory")
    result = grade(work)
    assert N_NOTES in failing(result) and "missing" in result[N_NOTES].detail


# --------------------------------------------------------------------------------------------------------------
# the helpers on their own
# --------------------------------------------------------------------------------------------------------------
def test_imports_are_expanded_four_hops_deep_and_cycles_stop(work):
    put(work, "# a\n@b.md\n", "a.md")
    put(work, "# b\n@c.md\n", "b.md")
    put(work, "# c\n@a.md\n", "c.md")  # a cycle
    put(work, "# Memory\n@a.md\n" + "\n".join(f"- filler line {i}" for i in range(20)))
    mem = m.load_memory(work)
    assert [ln.text for ln in mem.lines if ln.kind == "import"] == ["# a", "@b.md", "# b", "@c.md", "# c", "@a.md"]
    assert not mem.missing_imports


def test_a_missing_import_is_a_pointer_problem(work):
    put(work, REFERENCE.rstrip() + "\n\n@docs/missing-guide.md\n")
    result = lint(work)
    assert N_POINTERS in failing(result) and "missing-guide.md" in result[N_POINTERS].detail


def test_an_import_is_not_recognised_inside_code_or_an_email(work):
    put(work, REFERENCE.rstrip() + "\n\nWrite to payments@najm.example or use `@not/an/import.md`.\n```text\n@also/not/an/import.md\n```\n")
    mem = m.load_memory(work)
    assert not mem.missing_imports


def test_the_lint_is_deterministic(work):
    put(work, INIT_STYLE)
    first = [(c.name, c.ok, c.detail, c.hint) for c in m.memory_checks(work)]
    second = [(c.name, c.ok, c.detail, c.hint) for c in m.memory_checks(work)]
    assert first == second


@pytest.mark.parametrize(
    "token,expected",
    [("src/remit/fees.py", True), ("README.md", True), (".env.example", True), ("docs/", True), ("tests/test_<module>.py", False),
     ("pytest -q", False), ("ids.new_id", False), ("Decimal", False), ("https://example.com/x.md", False), ("--flag", False),
     ("a=b.py", False), ("type(scope)", False)],
)
def test_what_counts_as_a_path(token, expected):
    assert m._looks_like_path(m._clean_token(token)) is expected
