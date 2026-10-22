# REMIT-231: a tour of Remit, and customers refused "daily limit" after midnight

**From:** Hessa, Product Owner, Najm Remit
**To:** Payments Platform (you, and your AI coding tool if you use one)
**Priority:** High for part 2. Do part 1 first: you will need it.

This ticket is your first production incident. Two parts, in this order.

### Part 1: learn the codebase, and write it down

Write `docs/onboarding.md`: a tour of this repository for the next new engineer, 250 to 1,500 words,
with exactly these headings: **What Remit is**, **Entry points**, **Data flow**, **Tests**,
**Risks and gaps**, **Open questions**.

- **Data flow**: the steps a transfer goes through when it is sent, in the order the code runs them.
- **Tests**: how to run them, what makes them deterministic, and where they are thin.
- **Open questions**: at least one thing you could not verify.

Every file, function and fact must be true of this repository today. Open the files. Do not copy a
claim from a document, or from an AI tool, without checking it. Where a document and the code
disagree, the code wins; say so.

### Part 2: the incident

Maha (SRE) wrote up what production did: `lab-assets/incident.md`, `lab-assets/prod.log` and
`lab-assets/kyc_tiers.csv`. You have no production access, and neither does your tool.

The test suite is green, which is not evidence that the problem is absent.

1. **Reproduce first.** Write a test of your own that fails on today's code and shows what the
   customers saw. Use real moments from the log.
2. **Fix the root cause** with the smallest change that is correct, not the symptom you saw first.
3. **Keep your test as the regression test.** It must pass after the fix. Do not edit or delete any
   existing test, and do not touch `tests/conftest.py`.
4. **Write `docs/root-cause.md`**, a note Maha can paste into the incident record, with the headings
   **Summary**, **Symptom**, **Reproduction**, **Root cause**, **Why it was missed**, **Fix**, **Impact**,
   **Prevention**, **Open questions**. Name your test under Reproduction. Under Impact, say who was
   affected and in which direction, using the log.

### Rules of the house

- Commit as you go: the tour, the fix with its regression test, and the note are three changes. At
  least two commits, messages as in `CONTRIBUTING.md`, nothing left uncommitted.
- Money logic needs a second human reviewer, so keep the diff small.
- You are accountable for every line an AI tool writes. Keep a short agent log in `docs/agent-log.md`
  (prompt, what it did, what you corrected, minutes). If you used no tool, say what you did by hand.
- No real secrets or personal data in a prompt, a file or a commit. `lab-assets/` is constructed for
  teaching and holds no names.

### Done when

1. `docs/onboarding.md` is true and has its six sections.
2. A test of yours fails on the original code and passes on your fix; `pytest -q` passes.
3. The fix is a few lines in one place; nothing else in `src` changed.
4. `docs/root-cause.md` explains the cause, the evidence and who was affected.

When you think you are done, grade it from the `ailab` folder of the course repository:
`python -m ailab grade m06 --dir <this directory>`
