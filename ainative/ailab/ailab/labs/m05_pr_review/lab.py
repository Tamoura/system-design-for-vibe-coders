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
keyword saying what is wrong; ``checks_m05.match_findings``), it checks the verdict and the severities, and
then it grades the fixed branch with hidden acceptance tests and static checks. It cannot tell whether the
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
    thin = ["What I ran"] if "What I ran" not in missing and len(ran.split()) < 6 else []
    problems = ([f"missing: {', '.join(missing)}"] if missing else []) + ([f"too short: {', '.join(thin)}"] if thin else [])
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
    severity_ok = bool(matches.found) and not low
    severity = Check(R_SEVERITY, severity_ok,
                     "nothing to rate yet" if not matches.found else
                     (f"{checks.plural(len(low), 'finding')} rated lower than the damage it could do" if low else "ratings fit"),
                     "A finding that could lose money, leak a secret or hide a defect is a blocker or a major, not a nit.")

    everything = Check(R_ALL, matches.count == len(checks_m05.FLAWS),
                       f"{matches.count} of {len(checks_m05.FLAWS)}", "Go through the diff once more by risk class: the tests are code too.",
                       required=False)
    key = matches.found.get("hard-coded-key")
    leaked = bool(key and re.search(r"(?i)rotat|revok|leak|history|compromis", key.text))
    key_check = Check(R_KEY, leaked, "" if leaked else "the review does not say what must happen outside the code",
                      "Some problems cannot be fixed by a commit alone. Say who must do what next, and why a commit is not enough.",
                      required=False)
    return [structure, form, verdict, found, severity, everything, key_check]


def grade_fix(work: Path) -> list[Check]:
    short = checks._short  # noqa: SLF001 (kit-internal helper: "a, b (+2 more)")

    # CONTRIBUTING.md: standard library only, no secrets, money is Decimal
    rule_problems = []
    deps = checks_m05.import_problems(work)
    if deps:
        rule_problems.append("standard library only: " + short(deps))
    secrets = checks.no_secrets(work, scan="all", ignore=(*LEARNER_NOISE, "TASK.md", "lab-assets/**"))
    if not secrets.ok:
        rule_problems.append("secrets: " + secrets.detail)
    floats = checks_m05.float_problems(work)
    if floats:
        rule_problems.append("money is Decimal: " + short(floats))

    # the lesson 5.1 checklist, as far as a machine can read it
    list_problems = []
    excepts = checks_m05.broad_except_problems(work)
    if excepts:
        list_problems.append("errors hidden by a broad handler at " + short(excepts))
    unasserted = checks_m05.unasserted_tests(work)
    if unasserted:
        list_problems.append("no assertion in " + short(unasserted))
    faked = checks_m05.faked_fee_code(work)
    if faked:
        list_problems.append("fee code patched in " + short(faked))
    base_names = checks_m05.list_test_names(work, "main") if gitutil.has_ref(work, "main") else set()
    missing = sorted(base_names - checks_m05.list_test_names(work))
    if missing:
        list_problems.append("existing test missing: " + short(missing))

    failing, _ = checks_m05.failing_on_original(work)
    return [
        checks.tests_pass(work, name=F_VISIBLE),
        checks.hidden_tests_pass(work, HERE / "hidden", name=F_HIDDEN,
                                 hint="Re-read REMIT-229 in lab-assets/ and check each rule and each example against the code, "
                                      "including the cents."),
        Check(F_RULES, not rule_problems, "; ".join(rule_problems),
              "CONTRIBUTING.md, Code rules: money is Decimal, no secrets, standard library only (not even for tests)."),
        Check(F_CHECKLIST, not list_problems, "; ".join(list_problems),
              "Lesson 5.1: catch the specific error you can handle, assert what the ticket promises, call the real code in a test, "
              "and never delete a test to get green."),
        Check(F_CATCH, failing >= 2, f"{checks.plural(failing, 'new or changed test')} fail on the agent's version of the code",
              "Leave tests behind that fail on the agent's version: restore what was deleted and cover what your review found."),
        checks.files_changed_within(work, ALLOWED, ignore=LEARNER_NOISE, name=F_SCOPE,
                                    hint="Fix the pull request; do not widen it. Revert changes outside the discount code and its tests."),
        checks.conventional_commits(work, name=F_COMMITS),
        checks.all_committed(work, ignore=LEARNER_NOISE, name=F_CLEAN),
        checks.diff_size(work, max_lines=300, min_lines=1, ignore=LEARNER_NOISE, name=F_SMALL, required=False,
                         hint="A review fix is small. A rewrite of the pull request is a different pull request."),
        Check(F_BRANCH, gitutil.is_ancestor(work, gitutil.TAG_START, "HEAD") and bool(gitutil.commits_since(work)),
              "", "Add commits on top of agent/loyalty-discount instead of rewriting or replacing its history.", required=False),
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
