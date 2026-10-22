"""Lab m10 (lesson 10.2): "Split a change across agents and integrate it".

The story
---------
Hessa's ticket REMIT-361 asks for four small changes in four different places: a notification
template (``notify``), a ``corridors`` command (``corridors`` + ``cli``), a ``limits`` command
(``limits`` + ``cli``) and a runbook page (``docs``). They can be built at the same time. The
learner writes a plan, builds the pieces on separate branches (or in separate worktrees, by hand or
with agents), merges them into ``main`` and resolves the conflict the seed planted: the two commands
both add themselves at a marked place in ``src/remit/cli.py``.

What the seed plants
--------------------
Only two marker comments in ``cli.py``, one in the argument parser and one in the command
dispatch. Anything inserted directly below such a marker lands on the same lines as another
branch's insertion, so git cannot merge the two without a human. The base behaviour does not change.

What the grader checks, and what it cannot
------------------------------------------
It checks the *result*: the merged ``main`` passes the hidden acceptance tests (one check per task,
plus one for the pieces working together), at least three branches were merged, no conflict marker is
left, each commit belongs to one task, commit messages follow CONTRIBUTING.md, only the expected
files changed and no existing test was weakened. It cannot tell whether you planned well, whether an
agent or you wrote a line, or whether you really read the ``limits`` diff (the ticket asks you to).
The plan and the agent log are advisory checks that look only for their shape.
"""
from __future__ import annotations

import re
from pathlib import Path

from ailab import checks, checks_m10, framework, gitutil
from ailab.framework import Check, Lab

HERE = Path(__file__).resolve().parent
CLI = "src/remit/cli.py"

PARSER_MARKER = "    # --- Customer Care desk commands (REMIT-361): add your parser below this line ---\n"
RUN_MARKER = "    # --- Customer Care desk commands (REMIT-361): handle your command below this line, ending with `return 0` ---\n"

# Which module each task owns. A commit that changes two of them is "about two tasks".
AREAS = {
    "src/remit/notify.py": "notify",
    "src/remit/corridors.py": "corridors",
    "src/remit/limits.py": "limits",
}
ALLOWED = [*AREAS, CLI, "tests/**", "docs/**", "lab-assets/**", "TASK.md"]
PLAN = "docs/parallel-plan.md"
LOG = "docs/agent-log.md"
REQUIRED_BRANCHES = 3
MIN_COMMITS = 4  # four tasks, each at least one commit

# The hidden test file behind each task check: (module, check name, hint).
PARTS = [
    ("test_m10_notice", "Task A: the delay notice works",
     "Compare your template with the wording in the ticket, in both languages, word for word."),
    ("test_m10_corridors", "Task B: the corridors command works",
     "Run `python -m remit corridors` yourself and compare each line with the form in the ticket."),
    ("test_m10_limits", "Task C: the limits command works",
     "Run `python -m remit limits --customer C001` on a customer with a transfer, then re-read what 'today' means in limits.py."),
    ("test_m10_runbook", "Task D: the runbook is there",
     "Check the headings, the commands and the example output against the ticket's wording."),
    ("test_m10_together", "The pieces work together after the merge",
     "Run every command by hand on the merged main: the old ones too. Look for a lost import, a dropped branch in `_run`, a usage list that names only one new command."),
]

LEARNER = ("Najm Learner", "learner@najm.example")


# ---------------------------------------------------------------------------------------------
# seed: two marker comments in cli.py, nothing else
# ---------------------------------------------------------------------------------------------
def seed(work: Path) -> None:
    """Add the two markers. The code between them and what follows is the base's own, so the
    behaviour of every existing command is unchanged and the base tests stay green.

    The learner's agents should know the team's rules, so the reference project memory from lab m02 is
    copied in once that lab exists (a no-op until then)."""
    framework.add_reference_memory(work)
    framework.edit_file(
        work, CLI,
        '    history.add_argument("--customer", required=True)\n    return parser\n',
        '    history.add_argument("--customer", required=True)\n' + PARSER_MARKER + "    return parser\n",
    )
    framework.edit_file(
        work, CLI,
        "        return 0\n\n    amount = Money(args.amount, args.send_currency)\n",
        "        return 0\n\n" + RUN_MARKER + "    amount = Money(args.amount, args.send_currency)\n",
    )


# ---------------------------------------------------------------------------------------------
# helpers for the checks
# ---------------------------------------------------------------------------------------------
def _names(items: list[str], limit: int = 4) -> str:
    shown = ", ".join(items[:limit])
    return shown + (f" (+{len(items) - limit} more)" if len(items) > limit else "")


def _part_check(result: checks.PytestResult, module: str, name: str, hint: str) -> Check:
    """One check per hidden test file, from a single pytest run (failures name the test, never its code)."""
    if result.timed_out:
        return Check(name, False, "the acceptance tests did not finish in time (an endless loop?)", hint)
    if result.total == 0:
        return Check(name, False, "the acceptance tests could not run (does your code still import? run `pytest -q`)", hint)
    failed = [ident.split("::")[-1] for ident in result.failures if module in ident]
    if failed:
        return Check(name, False, f"{len(failed)} hidden checks failed: {_names(failed, 2)}", hint)
    return Check(name, True)


def _on_main(work: Path) -> Check:
    name = "You finished on main"
    branch = gitutil.current_branch(work)
    if branch == "main":
        return Check(name, True, "")
    return Check(name, False, f"the checked-out branch is {branch!r}, not main",
                 "Merge your branches into main and finish there: git switch main")


def merged_lines_of_work(work: Path) -> dict[str, str]:
    """Distinct branch tips that are part of ``main``, beyond the start: {sha: label}.

    Two sources, so deleting a branch after a merge commit does not erase the evidence:
    (1) local branches other than main whose tip is an ancestor of main (fast-forwards and merges);
    (2) the second parents of the merge commits on main's own first-parent line.
    A branch still sitting on the starting commit does not count: it carries no work.
    """
    start = gitutil.rev_parse(work, "lab-start") or "lab-start"
    found: dict[str, str] = {}
    on_main = gitutil.commits_since(work, "lab-start", "main", first_parent=True)
    merges_on_main = {c.sha for c in on_main if c.is_merge}  # a ref pointing at one of these is a bookmark, not a branch
    listing = gitutil.out(work, "for-each-ref", "--format=%(objectname) %(refname:short)", "refs/heads")
    for row in listing.splitlines():
        sha, _, branch = row.partition(" ")
        if branch == "main" or sha in merges_on_main:
            continue
        if gitutil.is_ancestor(work, sha, "main") and not gitutil.is_ancestor(work, sha, start):
            found[sha] = branch
    for commit in on_main:
        if commit.is_merge:
            for parent in commit.parents[1:]:
                if not gitutil.is_ancestor(work, parent, start):
                    found.setdefault(parent, f"a merged branch ({parent[:7]})")
    return found


def _branches_merged(work: Path) -> Check:
    name = f"At least {REQUIRED_BRANCHES} branches were merged into main"
    found = merged_lines_of_work(work)
    detail = (f"{len(found)} merged: {_names(sorted(found.values()))}" if found
              else "no branch has been merged into main yet")
    if len(found) >= REQUIRED_BRANCHES:
        return Check(name, True, detail)
    return Check(name, False, detail,
                 "Build each task on its own branch, then `git merge` it into main (no --squash), and keep the branches until you have graded.")


def _commit_files(work: Path, sha: str) -> list[str]:
    return gitutil.out(work, "diff-tree", "--no-commit-id", "--name-only", "-r", sha).splitlines()


def _one_task_per_commit(work: Path) -> Check:
    name = "Each commit is about one task"
    commits = [c for c in gitutil.commits_since(work, "lab-start") if not c.is_merge]
    if not commits:
        return Check(name, False, "no commits since the start yet", "Commit each task's work on its own branch.")
    mixed = []
    for commit in commits:
        areas = sorted({AREAS[f] for f in _commit_files(work, commit.sha) if f in AREAS})
        if len(areas) > 1:
            mixed.append(f'"{commit.subject}" changes {" and ".join(areas)}')
    if mixed:
        return Check(name, False, _names(mixed, 2),
                     "Split it: one task per commit (git reset --soft, then commit the files of each task separately).")
    return Check(name, True, f"{checks.plural(len(commits), 'commit')} checked")


def _tracked_text_files(work: Path, globs: list[str]) -> list[str]:
    listing = gitutil.git(work, "ls-files", "--cached", "--others", "--exclude-standard", "-z").stdout
    return sorted(p for p in listing.split("\0") if p and gitutil.glob_match(p, globs))


_OPEN = re.compile(r"^<{7}(?: |$)", re.M)
_CLOSE = re.compile(r"^>{7}(?: |$)", re.M)


def conflict_marker_files(work: Path) -> list[str]:
    """Code and runbook files that still contain a ``<<<<<<<`` ... ``>>>>>>>`` block."""
    bad = []
    for rel in _tracked_text_files(work, ["src/**/*.py", "tests/**/*.py", "docs/CARE.md"]):
        try:
            text = (work / rel).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if _OPEN.search(text) and _CLOSE.search(text):
            bad.append(rel)
    return bad


def _no_markers(work: Path) -> Check:
    name = "No conflict markers are left in the code"
    bad = conflict_marker_files(work)
    if bad:
        return Check(name, False, f"unresolved conflict in {_names(bad)}",
                     "Open each file, keep what BOTH sides added, delete the <<<<<<<, ======= and >>>>>>> lines, then run pytest and commit.")
    return Check(name, True, "")


def _markers_in_history(work: Path) -> Check:
    """Did any commit (merge commits included) ever contain a conflict block in code or in the runbook?"""
    name = "No commit in the history contains conflict markers"
    paths = ["src", "tests", "docs/CARE.md"]
    bad = []
    for commit in gitutil.commits_since(work, "lab-start"):
        opened = gitutil.git(work, "grep", "-l", "-E", r"^<{7}( |$)", commit.sha, "--", *paths, check=False).stdout.split()
        closed = gitutil.git(work, "grep", "-l", "-E", r"^>{7}( |$)", commit.sha, "--", *paths, check=False).stdout.split()
        if set(opened) & set(closed):
            bad.append(commit.sha[:7])
    if bad:
        return Check(name, False, f"found in {checks.plural(len(bad), 'commit')}: {_names(bad)}",
                     "A conflict was committed unresolved (and fixed later). Next time resolve it before you commit the merge.",
                     required=False)
    return Check(name, True, "", "", required=False)


def _tests_not_weakened(work: Path) -> Check:
    """Tests that existed at the start may gain lines but not lose or change any."""
    name = "Existing tests were not weakened"
    existing = gitutil.out(work, "ls-tree", "-r", "--name-only", "lab-start", "tests").splitlines()
    problems = []
    for rel in existing:
        if not rel.endswith(".py"):
            continue
        if not (work / rel).exists():
            problems.append(f"{rel} was deleted")
            continue
        stat = gitutil.out(work, "diff", "--numstat", "lab-start", "--", rel)
        if stat:
            _, deleted, _ = stat.split("\t", 2)
            if deleted not in ("0", "-"):
                problems.append(f"{rel}: {deleted} existing lines changed or removed")
    if problems:
        return Check(name, False, _names(problems),
                     "Put your tests in new files, or only add to the old ones. Undo the change: git restore --source=lab-start <file>")
    return Check(name, True, "")


def _plan(work: Path) -> Check:
    return checks.sections_check(
        work, PLAN, ["Task graph", "Boundaries", "Merge order", "Verification"], min_words=4,
        name="A parallel plan exists (docs/parallel-plan.md)",
        hint="Copy lab-assets/parallel-plan-template.md to docs/parallel-plan.md and fill in each section before you start.",
        required=False,
    )


def _agent_log(work: Path) -> Check:
    name = "A short log exists (docs/agent-log.md)"
    path = work / LOG
    words = len(path.read_text(encoding="utf-8").split()) if path.is_file() else 0
    if words >= 30:
        return Check(name, True, f"{words} words", required=False)
    return Check(name, False, "docs/agent-log.md is missing" if not path.is_file() else f"only {words} words",
                 "Write down what you delegated, what you had to correct and how long it took (about 30 words or more).",
                 required=False)


# ---------------------------------------------------------------------------------------------
# grade
# ---------------------------------------------------------------------------------------------
def grade(work: Path) -> list[Check]:
    hidden = checks.run_hidden_pytest(work, HERE / "hidden", args=["--continue-on-collection-errors"])
    return [
        _on_main(work),
        checks.all_committed(work, name="Everything is committed"),
        checks.tests_pass(work, name="Your own tests pass"),
        *[_part_check(hidden, module, name, hint) for module, name, hint in PARTS],
        _no_markers(work),
        _branches_merged(work),
        _one_task_per_commit(work),
        checks.conventional_commits(work, min_commits=MIN_COMMITS),
        checks.files_changed_within(
            work, ALLOWED, name="Only the expected files changed",
            hint="This ticket touches notify.py, corridors.py, limits.py, cli.py, tests and docs. Undo the rest: git restore --source=lab-start <file>",
        ),
        _tests_not_weakened(work),
        checks.no_secrets(work),
        # advisory: the habits the lesson teaches, which a grader can only look at from outside
        checks_m10.new_tests_fail_on_starter(work, hint="Tests that pass without your change prove nothing. Add tests that need the new behaviour."),
        _plan(work),
        _agent_log(work),
        _markers_in_history(work),
    ]


# ---------------------------------------------------------------------------------------------
# solve: the reference solution, done the way the lab asks (a plan, four branches, four merges)
# ---------------------------------------------------------------------------------------------
# (branch, [(patch file, commit message)]). The first wave is cut from the same main and built "in parallel";
# the runbook is cut after the first wave is merged, because it quotes the integrated program's real output.
FIRST_WAVE: list[tuple[str, list[tuple[str, str]]]] = [
    ("feat/delay-notice", [
        ("a1_template.patch", "feat(notify): add the transfer_delayed notification"),
        ("a2_tests.patch", "test(notify): cover the delay notice in both languages"),
    ]),
    ("feat/corridors-command", [
        ("b1_describe.patch", "feat(corridors): describe a corridor in one line"),
        ("b2_command.patch", "feat(cli): add the corridors command"),
        ("b3_tests.patch", "test(corridors): cover describe and the command"),
    ]),
    ("feat/limits-command", [
        ("c1_usage_line.patch", "feat(limits): summarise a customer's daily and monthly use"),
        ("c2_command.patch", "feat(cli): add the limits command"),
        ("c3_tests.patch", "test(limits): cover the Qatar day and month boundaries"),
    ]),
]
SECOND_WAVE: list[tuple[str, list[tuple[str, str]]]] = [
    ("docs/care-runbook", [
        ("d1_runbook.patch", "docs(docs): add the Customer Care runbook"),
    ]),
]


def _stamp(step: int) -> str:
    return f"2026-03-02T{10 + step // 60:02d}:{step % 60:02d}:00+00:00"


def solve(work: Path) -> None:
    """Plan on main, build the first three tasks on their own branches, merge them in order (the second
    command's merge meets the planted conflict), then write the runbook from the integrated program.

    The patches in ``solution/`` were produced by doing exactly this by hand; ``cli_resolved.txt`` is the
    ``cli.py`` that results from keeping both commands (and both ``return 0`` lines) when the conflict is met.
    """
    solution = HERE / "solution"
    step = 0

    def commit(message: str) -> None:
        nonlocal step
        step += 3
        gitutil.commit_all(work, message, author=LEARNER, date=_stamp(step))

    def build(wave: list[tuple[str, list[tuple[str, str]]]]) -> None:
        for branch, steps in wave:
            gitutil.checkout(work, "main")
            gitutil.create_branch(work, branch)
            for patch, message in steps:
                gitutil.apply_patch(work, solution / patch)
                commit(message)
        gitutil.checkout(work, "main")

    def integrate(wave: list[tuple[str, list[tuple[str, str]]]]) -> None:
        nonlocal step
        for branch, _ in wave:
            step += 3
            merged = gitutil.merge(work, branch, no_ff=True, message=f"Merge branch '{branch}'",
                                   author=LEARNER, date=_stamp(step), check=False)
            if not merged.ok:  # the planted conflict in cli.py: keep both commands
                framework.write_file(work, CLI, (solution / "cli_resolved.txt").read_text(encoding="utf-8"))
                commit(f"Merge branch '{branch}'")

    # 1. the plan is written on main before any branch is cut
    framework.write_file(work, PLAN, (solution / "parallel-plan.md").read_text(encoding="utf-8"))
    commit("docs(docs): plan the parallel work for REMIT-361")
    # 2. tasks A, B and C, each on its own branch cut from the same main; then integrate them in order
    build(FIRST_WAVE)
    integrate(FIRST_WAVE)
    # 3. task D, cut from the integrated main
    build(SECOND_WAVE)
    integrate(SECOND_WAVE)
    # 4. the log, last
    framework.write_file(work, LOG, (solution / "agent-log.md").read_text(encoding="utf-8"))
    commit("docs(docs): log what was delegated and what needed correcting")


LAB = Lab(
    id="m10",
    title="Split a change across branches and integrate it",
    lesson="10.2",
    needs_agent=False,  # an agent is recommended (that is what the lab is about); the grader only sees the result
    seed=seed,
    grade=grade,
    solve=solve,
)
