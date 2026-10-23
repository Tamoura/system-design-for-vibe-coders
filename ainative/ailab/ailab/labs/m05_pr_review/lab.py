"""Lab m05 (lesson 5.2): "Review a pull request an agent wrote".

The story
---------
Lujain asked Claude Code to build Hessa's ticket REMIT-229 (a loyalty discount on transfer fees). The result
is the branch ``agent/loyalty-discount``: four tidy commits, seven new tests, a description that says "105
passed". The suite really is green. The branch is still not mergeable: it carries eight seeded problems
(an invented dependency, a swallowed exception, float money, a test that asserts nothing, an over-mocked
test, a hard-coded key, scope creep and the test deleted to hide it).

The learner is the second human reviewer. They write ``review.md`` (verdict, what they ran, findings with
file, line and severity) and then fix the branch with commits of their own.

What the grader can and cannot tell
-----------------------------------
It reads the review for *mentions* of the seeded problems (right file, plus a line near the problem or a
keyword saying what is wrong; ``checks_m05.match_findings``), it checks the verdict and the severities (too low
fails, a test problem called a blocker fails, a review of nothing but blockers fails), and then it grades the fixed
branch with hidden acceptance tests and static checks (a key that was only moved, a test restored under a new name
and a float that has nothing to do with money are all handled in ``checks_m05``). It cannot tell whether the
reviewer understood a finding, only that the review says it. The course says so.

How the branch is made (and why materials/ is not called assets/)
-----------------------------------------------------------------
The pull request diff must be exactly the agent's work, so ``git diff main...agent/loyalty-discount`` may not
contain the kit's own TASK.md and lab-assets/. The framework adds those after the seed, on the branch that is
checked out. So the seed commits them to ``main`` *first* (from ``materials/``), then branches, applies the
agent's four patches (``agent/NN.patch``) as four commits, and stays on the branch. The framework's own
"Lab starting state" commit is then empty. ``lab-start`` points at the agent's tip, so every helper that
compares with ``lab-start`` sees exactly what the learner changed.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

from ailab import checks, checks_m05, framework, gitutil
from ailab.framework import Check, Lab
from ailab.gitutil import TOOL_NOISE

HERE = Path(__file__).resolve().parent
BRANCH = "agent/loyalty-discount"
LUJAIN = ("Lujain", "lujain@najm.example")
LEARNER = ("Najm Learner", "learner@najm.example")

# The agent's four commits: (patch file, message, date). The messages are the agent's own style.
AGENT_COMMITS = [
    ("01.patch",
     "feat(fees): add a loyalty discount to quote_fee\n\n"
     "Silver customers get 10% off the fee and gold customers 20%, as REMIT-229 asks.\n"
     "Rates come from najm-loyalty when it is installed, else from a local table.",
     "2026-03-02T10:12:00+00:00"),
    ("02.patch",
     "feat(service): charge the customer's loyalty tier on quote and send",
     "2026-03-02T10:25:00+00:00"),
    ("03.patch",
     "test(loyalty): cover the loyalty discount",
     "2026-03-02T10:40:00+00:00"),
    ("04.patch",
     "refactor(fees): tidy helper names and docs\n\nAlso keeps the customer-facing total under the cap.",
     "2026-03-02T11:05:00+00:00"),
]
SOLUTION_DATES = ["2026-03-03T09:10:00+00:00", "2026-03-03T09:25:00+00:00", "2026-03-03T09:40:00+00:00",
                  "2026-03-03T09:50:00+00:00", "2026-03-03T10:05:00+00:00"]
REVIEW_COMMIT = ("docs(review): record my review of the loyalty discount pull request", "2026-03-03T10:20:00+00:00")

# Review checks (names are stable: the starter and the solved state must list the same names)
R_FILE = "review.md has a verdict, what you ran and findings"
R_FORM = "Each finding names a file, a line and a severity"
R_VERDICT = "Your verdict blocks the merge"
R_FOUND = "Your review covers the problems in the pull request"
R_SEVERITY = "Your severities fit the risk"
R_ALL = "Your review covers every problem the grader knows"
R_KEY = "Your review names the follow-up beyond the diff"
# Fix checks. The names say nothing about what is wrong: they are listed before the learner has reviewed anything.
F_VISIBLE = "The branch's own tests pass"
F_HIDDEN = "The discount behaves as REMIT-229 says"
F_RULES = "The team's code rules hold (CONTRIBUTING.md)"
F_CHECKLIST = "The branch passes the review checklist (lesson 5.1)"
F_CATCH = "Your tests would have caught the agent's bugs"
F_SCOPE = "Only the files the change needs changed"
F_COMMITS = "Your commit messages follow CONTRIBUTING.md"
F_CLEAN = "Your fix is committed"
F_SMALL = "The fix is small"
F_BRANCH = "You fixed the agent's branch on top of its commits"
FIX_NAMES = [(F_VISIBLE, True), (F_HIDDEN, True), (F_RULES, True), (F_CHECKLIST, True), (F_CATCH, True), (F_SCOPE, True),
             (F_COMMITS, True), (F_CLEAN, True), (F_SMALL, False), (F_BRANCH, False)]

# Files a sound fix may touch. Anything else is scope creep of the learner's own.
ALLOWED = ["pyproject.toml", "src/remit/fees.py", "src/remit/loyalty.py", "src/remit/service.py", "tests/**", "docs/**"]
LEARNER_NOISE = (*TOOL_NOISE, "review.md")
RAN_MIN_WORDS = 3  # "What I ran" only has to say something; TASK.md and the lesson state the number


# ---------------------------------------------------------------------------------------------
# seed: main gets the lab's own files, then the agent's branch is built on top
# ---------------------------------------------------------------------------------------------
def seed(work: Path) -> None:
    framework.write_file(work, "TASK.md", (HERE / "task.md").read_text(encoding="utf-8"))
    assets = work / "lab-assets"
    assets.mkdir()
    for source in sorted((HERE / "materials").iterdir()):
        shutil.copyfile(source, assets / source.name)
    gitutil.commit_all(work, "Add the lab materials", force=["lab-assets", "TASK.md"])
    gitutil.create_branch(work, BRANCH)
    for patch, message, date in AGENT_COMMITS:
        gitutil.apply_patch(work, HERE / "agent" / patch)
        gitutil.commit_all(work, message, author=LUJAIN, date=date)
    # the learner starts on the branch; the framework's "Lab starting state" commit is empty and lab-start marks the tip


# ---------------------------------------------------------------------------------------------
# grade
# ---------------------------------------------------------------------------------------------
def _known_files(work: Path) -> list[str]:
    return gitutil.out(work, "ls-tree", "-r", "--name-only", gitutil.TAG_START).splitlines()


def grade_review(work: Path) -> list[Check]:
    path = work / "review.md"
    structure_hint = "Start from lab-assets/review-template.md and keep its three headings: Verdict, What I ran, Findings."
    if not path.is_file():
        waiting = "no review.md yet"
        return [Check(R_FILE, False, "review.md does not exist", structure_hint)] + [
            Check(name, False, waiting, "Write review.md first." if name == R_FORM else "", required)
            for name, required in ((R_FORM, True), (R_VERDICT, True), (R_FOUND, True), (R_SEVERITY, True),
                                   (R_ALL, False), (R_KEY, False))]
    review = checks_m05.parse_review(path.read_text(encoding="utf-8"), _known_files(work))
    sections = review.sections
    missing = [title for title, key in (("Verdict", "verdict"), ("What I ran", "what i ran"), ("Findings", "finding"))
               if not any(key in name for name in sections)]
    ran = next((body for name, body in sections.items() if "what i ran" in name), "")
    thin = ["What I ran"] if "What I ran" not in missing and len(ran.split()) < RAN_MIN_WORDS else []
    problems = ([f"missing: {', '.join(missing)}"] if missing else []) + (
        [f"too short: {', '.join(thin)} (list the commands you ran and what they showed: at least {RAN_MIN_WORDS} words)"] if thin else [])
    structure = Check(R_FILE, not problems, "; ".join(problems), structure_hint if problems else "")
    matches = checks_m05.match_findings(review.findings, checks_m05.flaw_lines(work))

    incomplete = []
    for finding in review.findings:
        gaps = [label for label, ok in (("file", bool(finding.files)), ("line", finding.line_given),
                                        ("severity", finding.severity is not None)) if not ok]
        if gaps:
            incomplete.append(f"#{finding.index} (no {' or '.join(gaps)})")
    enough = len(review.findings) >= 6
    form_detail = f"{checks.plural(len(review.findings), 'finding')} found in review.md"
    if incomplete:
        form_detail += "; incomplete: " + ", ".join(incomplete[:4])
    elif not enough:
        form_detail += "; a pull request this size has more than that to say"
    form = Check(R_FORM, enough and not incomplete, form_detail,
                 "One block per problem: File, Line (a number, or - for something deleted), Severity (blocker, major, minor or nit), "
                 "Problem and Fix. See lab-assets/review-template.md.")

    blocks = checks_m05.verdict_blocks_merge(review.verdict)
    verdict = Check(R_VERDICT, blocks, "" if blocks else "the verdict does not ask for changes",
                    "Money logic with problems in it is not approved 'with comments'. Say what you decided: request changes.")

    classes = sorted({f.risk for f in checks_m05.FLAWS} - {f.risk for f in checks_m05.FLAWS if f.id in matches.found})
    found_ok = matches.count >= 6
    found_detail = f"your findings cover {matches.count} of {len(checks_m05.FLAWS)} problems the grader knows about"
    if matches.extra:
        found_detail += f" (and {checks.plural(len(matches.extra), 'more finding')} the grader cannot judge, which may still be fair)"
    hint = ("Read the diff by risk class and name the file and what is wrong, in concrete words."
            + (f" Nothing found yet in: {', '.join(classes)}." if classes else ""))
    found = Check(R_FOUND, found_ok, found_detail, "" if found_ok else hint)

    low = checks_m05.under_rated(matches)
    high = checks_m05.over_rated(matches)
    flat = checks_m05.all_blockers(review.findings)
    severity_ok = bool(matches.found) and not low and not high and not flat
    severity_notes = ([f"{checks.plural(len(low), 'finding')} rated lower than the damage it could do"] if low else []) + (
        [f"{checks.plural(len(high), 'finding')} rated higher than the damage it could do"] if high else []) + (
        ["every finding is a blocker, so nothing is ranked"] if flat else [])
    severity = Check(R_SEVERITY, severity_ok,
                     "nothing to rate yet" if not matches.found else ("; ".join(severity_notes) if severity_notes else "ratings fit"),
                     "Rate by the damage if it ships. A finding that could lose money, leak a secret or hide a defect is a blocker or a major, "
                     "not a nit; a test too weak to fail is a major at most; if everything is a blocker, nothing is.")

    everything = Check(R_ALL, matches.count == len(checks_m05.FLAWS),
                       f"{matches.count} of {len(checks_m05.FLAWS)}", "Go through the diff once more by risk class: the tests are code too.",
                       required=False)
    key = matches.found.get("hard-coded-key")
    leaked = bool(key and re.search(r"(?i)rotat|revok|leak|history|compromis", key.text))
    key_check = Check(R_KEY, leaked, "" if leaked else "the review does not say what must happen outside the code",
                      "Some problems cannot be fixed by a commit alone. Say who must do what next, and why a commit is not enough.",
                      required=False)
    return [structure, form, verdict, found, severity, everything, key_check]


def _scope_check(work: Path) -> Check:
    """checks.files_changed_within, but the detail lists every file (the helper stops at four)."""
    result = checks.files_changed_within(work, ALLOWED, ignore=LEARNER_NOISE, name=F_SCOPE,
                                         hint="Touch only the files the pull request already changes, plus tests and docs. "
                                              "Revert anything else (git restore <file>, or git rm <file> for a new file).")
    changed = gitutil.changed_files(work, gitutil.TAG_START, ignore=LEARNER_NOISE)
    outside = [path for path in changed if not gitutil.glob_match(path, ALLOWED)]
    if outside:
        result.detail = "unrelated files changed: " + ", ".join(outside)
    elif result.ok and changed:
        result.detail = "changed: " + ", ".join(changed)
    return result


def _branch_check(work: Path) -> Check:
    """The fix belongs on top of the agent's commits, on the branch that is checked out (the grader grades what is checked out)."""
    if not gitutil.is_ancestor(work, gitutil.TAG_START, "HEAD"):
        branch = gitutil.current_branch(work)
        if branch == BRANCH:
            return Check(F_BRANCH, False, "the history of agent/loyalty-discount no longer contains the agent's commits",
                         "Add commits on top of the agent's instead of rewriting or replacing its history (a squash is a rewrite).",
                         required=False)
        return Check(F_BRANCH, False, f"you are on '{branch}', which does not contain the agent's commits",
                     "The grader grades what is checked out. Switch to agent/loyalty-discount (git switch agent/loyalty-discount) "
                     "and make your commits there.", required=False)
    if not gitutil.commits_since(work):
        return Check(F_BRANCH, False, "no commits of yours on the branch yet",
                     "Add commits on top of agent/loyalty-discount instead of rewriting or replacing its history.", required=False)
    return Check(F_BRANCH, True, "", "", required=False)


def grade_fix(work: Path) -> list[Check]:
    short = checks._short  # noqa: SLF001 (kit-internal helper: "a, b (+2 more)")

    # CONTRIBUTING.md: standard library only, no secrets, money is Decimal
    rule_problems: list[str] = []
    rule_hints: list[str] = []
    deps = checks_m05.import_problems(work)
    if deps:
        rule_problems.append("standard library only: " + short(deps))
        rule_hints.append("Standard library only: no new dependency, not even for tests.")
    secrets = checks.no_secrets(work, scan="all", ignore=(*LEARNER_NOISE, "TASK.md", "lab-assets/**"))
    leaks = checks_m05.leaked_key_problems(work)
    shown = [hit for hit in leaks if not (not secrets.ok and hit.rsplit(" in ", 1)[-1] in secrets.detail)]
    if not secrets.ok or shown:
        rule_problems.append("secrets: " + short(([secrets.detail] if not secrets.ok else []) + shown))
        rule_hints.append("No secrets anywhere: not in code, tests, fixtures, a default value or review.md. Remove it, read secrets from "
                          "the environment with no fallback, and say in your review that a key that was committed must be rotated. "
                          "To test that it is gone, look for its prefix, not the key.")
    floats = checks_m05.float_problems(work)
    if floats:
        rule_problems.append("money is Decimal: " + short(floats))
        rule_hints.append("Money is Decimal: no float() and no float rates in the money code. Round half up.")

    # the lesson 5.1 checklist, as far as a machine can read it
    list_problems: list[str] = []
    list_hints: list[str] = []
    excepts = checks_m05.broad_except_problems(work)
    if excepts:
        list_problems.append("errors hidden by a broad handler at " + short(excepts))
        list_hints.append("Catch the specific error you can handle; let the rest fail loudly.")
    unasserted = checks_m05.unasserted_tests(work)
    if unasserted:
        list_problems.append("no assertion in " + short(unasserted))
        list_hints.append("Assert what the ticket promises: a test that cannot fail proves nothing.")
    faked = checks_m05.faked_fee_code(work)
    if faked:
        list_problems.append("fee code patched in " + short(faked))
        list_hints.append("Call the real fee code in a test; patch only the edges (clock, notifier).")
    missing = checks_m05.missing_tests(work)
    if missing:
        list_problems.append("existing test missing: " + short(missing))
        list_hints.append("A test that exists on main is gone: put it back as it was (same name, same body). "
                          "Never delete or rewrite a test to get green.")

    failing, _ = checks_m05.failing_on_original(work)
    return [
        checks.tests_pass(work, name=F_VISIBLE),
        checks.hidden_tests_pass(work, HERE / "hidden", name=F_HIDDEN,
                                 hint="Re-read REMIT-229 in lab-assets/ and check each rule and each example against the code, "
                                      "including the cents."),
        Check(F_RULES, not rule_problems, "; ".join(rule_problems), " ".join(rule_hints)),
        Check(F_CHECKLIST, not list_problems, "; ".join(list_problems), " ".join(list_hints)),
        Check(F_CATCH, failing >= 2, f"{checks.plural(failing, 'new or changed test')} fail on the agent's version of the code",
              "Leave tests behind that fail on the agent's version (a parametrized test counts once per case): "
              "restore what was deleted and cover what your review found."),
        _scope_check(work),
        checks.conventional_commits(work, name=F_COMMITS),
        checks.all_committed(work, ignore=LEARNER_NOISE, name=F_CLEAN),
        checks.diff_size(work, max_lines=300, min_lines=1, ignore=LEARNER_NOISE, name=F_SMALL, required=False,
                         hint="A review fix is small. A rewrite of the pull request is a different pull request."),
        _branch_check(work),
    ]


def waiting_fix_checks() -> list[Check]:
    hint = "Finish review.md (verdict, findings, severities). The fix is graded once the review is complete."
    return [Check(name, False, "not checked yet: the review comes first", hint if index == 0 else "", required)
            for index, (name, required) in enumerate(FIX_NAMES)]


def grade(work: Path) -> list[Check]:
    review = grade_review(work)
    review_done = all(c.ok for c in review if c.required)
    return review + (grade_fix(work) if review_done else waiting_fix_checks())


# ---------------------------------------------------------------------------------------------
# solve: the reference review and fix, as the commits a careful reviewer would make
# ---------------------------------------------------------------------------------------------
def solve(work: Path) -> None:
    steps = sorted((HERE / "solution").glob("*.patch"))
    for patch, date in zip(steps, SOLUTION_DATES):
        gitutil.apply_patch(work, patch)
        message = patch.with_suffix(".msg").read_text(encoding="utf-8").strip()
        gitutil.commit_all(work, message, author=LEARNER, date=date)
    framework.write_file(work, "review.md", (HERE / "solution" / "review.md").read_text(encoding="utf-8"))
    gitutil.commit_all(work, REVIEW_COMMIT[0], author=LEARNER, date=REVIEW_COMMIT[1])


LAB = Lab(
    id="m05",
    title="Review a pull request an agent wrote",
    lesson="5.2",
    needs_agent=False,  # a second-model reviewer is a good exercise, but the review and the fix can be done by hand
    seed=seed,
    grade=grade,
    solve=solve,
)
