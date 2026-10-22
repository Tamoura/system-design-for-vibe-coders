"""Lab m09 (lesson 9.2): "Build a project toolkit and a headless triage script".

The story
---------
Tariq and Salem's ticket REMIT-285: the team's first shared toolkit for AI-assisted work. The learner builds five things in the
Remit repository:

1. a review command (a skill, or a legacy command file) that works through the team's checklist and only reports;
2. a read-only reviewer subagent;
3. a PostToolUse hook that checks the Python file an agent has just edited (it must parse; a file under ``src/remit/`` must not
   contain a float) plus its registration in ``.claude/settings.json``;
4. a headless triage script that runs ``claude -p`` on support tickets and parses the JSON it prints;
5. three automation decision cards, one of which (an agent that approves and merges pull requests) must not say "automate".

The starting state is the base repository with the reference project memory (``CLAUDE.md``, from lab m02) and ``lab-assets/``:
skeletons for the hook and the script, four sample hook documents, sample tickets, the card template and ``bin/claude``, a copy of
the kit's STAND-IN for the ``claude`` program (``ailab/stubs/claude``). The stand-in is not Claude Code: it imitates the documented
shape of print mode (a JSON object with ``result``, ``session_id`` and ``total_cost_usd``; an exit code; ``--max-turns``) and
classifies tickets with a keyword table, so that the script can be run and graded offline, for free and identically every time.

What is graded, and what cannot be
----------------------------------
All the logic lives in ``ailab/checks_m09.py``. In short: the skill and the subagent are read as data (frontmatter, keys, tools,
body); the settings are parsed; the hook is RUN against 22 sample documents and against every file of the untouched source; the
triage script is RUN against the stand-in on ten batches of invented tickets (and three unusable input files), and the stand-in logs how it was called. Nothing
is imported in the grader's process and nothing a sample contains is ever executed.

The grader checks the RESULT. It cannot tell whether Claude Code accepts a file, whether a review prompt is any good, whether the
script works against the real program or a real model, or whether the learner's reasons on the cards are sound. The lesson says so.

Files
-----
    seed(work)    adds the reference project memory (a no-op if lab m02 is absent); everything else arrives in ``lab-assets/``.
    grade(work)   see above.
    solve(work)   applies ``solution/`` in five small commits: the reviewer, the review command, the hook, the triage script (+ tests), the cards.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from ailab import checks, checks_m09, framework, gitutil
from ailab.framework import Check, Lab

HERE = Path(__file__).resolve().parent
SOLUTION = HERE / "solution"
LEARNER = ("Najm Learner", "learner@najm.example")


def seed(work: Path) -> None:
    framework.add_reference_memory(work)


def grade(work: Path) -> list[Check]:
    return [
        checks.tests_pass(work, name=checks_m09.N_TESTS),
        # part 1: the review command
        *checks_m09.skill_checks(work),
        # part 2: the reviewer subagent
        *checks_m09.agent_checks(work),
        # part 3: the post-edit hook (registered, then RUN on sample documents)
        *checks_m09.settings_checks(work),
        *checks_m09.hook_checks(work),
        # part 4: the triage script (RUN against the claude stand-in)
        *checks_m09.triage_checks(work),
        # part 5: the cards
        *checks_m09.card_checks(work),
        # hygiene
        *checks_m09.hygiene_checks(work),
    ]


def solve(work: Path) -> None:
    """The reference solution, one commit per part."""
    work = Path(work)

    def put(src: str, dest: str) -> None:
        target = work / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOLUTION / src, target)

    def commit(message: str, minute: int) -> None:
        gitutil.commit_all(work, message, author=LEARNER, date=f"2026-03-02T10:{minute:02d}:00+00:00")

    put("remit-reviewer.md", ".claude/agents/remit-reviewer.md")
    commit("feat(claude): add a read-only reviewer subagent", 0)

    put("review-change.SKILL.md", ".claude/skills/review-change/SKILL.md")
    commit("feat(claude): add the review-change command", 10)

    put("post_edit.py", ".claude/hooks/post_edit.py")
    put("settings.json", ".claude/settings.json")
    put("test_post_edit.py", "tests/test_post_edit.py")
    commit("feat(claude): check edited Python files with a post-edit hook", 20)

    put("triage.py", "scripts/triage.py")
    put("test_triage.py", "tests/test_triage.py")
    commit("feat(scripts): triage support tickets with claude -p", 30)

    put("automation-cards.md", "docs/automation-cards.md")
    commit("docs(claude): record what we automate and what we keep manual", 40)


LAB = Lab(
    id="m09",
    title="A project toolkit and a headless triage script",
    lesson="9.2",
    needs_agent=False,  # an agent can help, and the lesson suggests it; the grader cannot tell, and the lab works by hand
    seed=seed,
    grade=grade,
    solve=solve,
)
