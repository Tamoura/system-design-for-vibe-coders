# REMIT-231: a tour of Remit, and customers refused "daily limit" after midnight

**From:** Hessa, Product Owner, Najm Remit
**To:** Payments Platform (you, and your AI coding tool if you use one)
**Priority:** High for part 2. Do part 1 first: you will need it.

This ticket is your first production incident. Two parts, in this order.

### Part 1: learn the codebase, and write it down

Write `docs/onboarding.md`, a tour for the next new engineer, 250 to 1,500 words, with these six
headings (a title and extra sections are fine): **What Remit is**, **Entry points**, **Data flow**,
**Tests**, **Risks and gaps**, **Open questions**.

- **Entry points**: how Remit is run (the command line) and the class other code calls.
- **Data flow**: the stages of sending a transfer, in the order the code runs them, each named with
  the word the code uses (the audit event can go anywhere).
- **Tests**: how to run them, what makes them deterministic, where they are thin.
- **Risks and gaps**: what is risky, and the house rules a change must respect (money, the internal
  library `najmkit`).
- **Open questions**: at least one thing you could not verify. A suspicion about the incident goes
  here, as a question: the tour must stay true after your fix.

Every file, function and fact must be true of this repository today, so open the files. Do not copy
a claim from a document, or from an AI tool, unchecked. Where a document and the code disagree, the
code wins; say so, naming the document and its claim. A file named somewhere but not in the
repository: say plainly that it is not there.

### Part 2: the incident

Maha (SRE) wrote up what production did: `lab-assets/incident.md`, `lab-assets/prod.log` and
`lab-assets/kyc_tiers.csv`. You have no production access, and neither does your tool.

The test suite is green, which is not evidence that the problem is absent.

1. **Reproduce first.** Write a test that runs on today's code and fails on an assertion about what
   the customers saw (an import error is not a reproduction). Use real moments from the log.
2. **Fix the root cause** with the smallest correct change, not the symptom you saw first.
3. **Keep your test as the regression test.** It must pass after the fix. Do not edit or delete any
   existing test, and do not touch `tests/conftest.py`.
4. **Write `docs/root-cause.md`**, a note Maha can paste into the incident record, with the headings
   **Summary**, **Symptom**, **Reproduction**, **Root cause**, **Why it was missed**, **Fix**, **Impact**,
   **Prevention**, **Open questions** (a title is fine; "none" is a fine answer to the last). Name your
   test under Reproduction. Under Impact, list by id who was affected and in which direction, using
   the log: support names only some of them.

### Rules of the house

- Commit as you go: the tour, the fix with its regression test, and the note are three changes. At
  least two commits (more is fine), messages as in `CONTRIBUTING.md` (`type(scope): subject`, header
  at most 72 characters), nothing uncommitted.
- Change source code only where the defect is; tests go in `tests/`, writing in `docs/`, a helper
  script in `scripts/`. Money logic needs a second human reviewer, so keep the diff small.
- You are accountable for every line an AI tool writes. Keep a short agent log in `docs/agent-log.md`
  (prompt, what it did, what you corrected, minutes). If you used no tool, say what you did by hand.
- No real secrets or personal data in a prompt, a file or a commit. `lab-assets/` is constructed for
  teaching and holds no names.

### Done when

1. `docs/onboarding.md` is true and has its six headings.
2. A test of yours fails on the original code and passes on your fix; `pytest -q` passes.
3. The fix is a few lines (at most 20 changed) in one place; nothing else in `src` changed.
4. `docs/root-cause.md` has its nine headings, the cause, the evidence and who was affected.

When you think you are done, grade it from the `ainative/ailab` folder of the course repository, not
from this directory: `python -m ailab grade m06 --dir <this directory>`
