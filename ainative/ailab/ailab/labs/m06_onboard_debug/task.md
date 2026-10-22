# REMIT-231: a tour of Remit, and customers refused "daily limit" after midnight

**From:** Hessa, Product Owner, Najm Remit
**To:** Payments Platform (you, and your AI coding tool if you use one)
**Priority:** High for part 2. Do part 1 first, because you will need it.

You are new on the team and the first real ticket is a production incident. Two parts, in this
order.

## Part 1: learn the codebase, and write it down

Before you touch money logic, write `docs/onboarding.md`: a tour of the Remit repository for the next
new engineer. One or two pages (250 to 1,500 words). Use exactly these headings:

**What Remit is**, **Entry points**, **Data flow**, **Tests**, **Risks and gaps**, **Open questions**.

- **Data flow** is the steps a transfer goes through when it is sent, in the order the code runs them.
- **Tests** says how to run them, where they live, what makes them deterministic, and where they are thin.
- **Risks and gaps** says where it is dangerous to change things.
- **Open questions** lists at least one thing you could not verify.

Every file, function and fact in the tour must be true of this repository today. Open the files. Do not
copy a claim from a document, or from an AI tool, without checking it. Where this repository's
documents disagree with its code, the code wins; say so in the tour.

## Part 2: the incident

Maha (SRE) has written up what production did: `lab-assets/incident.md`, with `lab-assets/prod.log` and
`lab-assets/kyc_tiers.csv`. Everything you need is in those files and in this repository. You have no
production access, and neither does your tool.

The test suite is green today. A green suite is not evidence that the problem is absent. Please:

1. **Reproduce first.** Write a test of your own that fails on the code as it is today and shows what the
   customers saw. Use real moments from the log.
2. **Find the root cause and fix it** with the smallest change that is correct. Fix the cause, not the
   symptom you happened to see first.
3. **Keep your test as the regression test.** It must pass after the fix. Do not edit or delete any existing
   test, and do not touch `tests/conftest.py`.
4. **Write `docs/root-cause.md`**, a note Maha can paste into the incident record. Use these headings:
   **Summary**, **Symptom**, **Reproduction**, **Root cause**, **Why it was missed**, **Fix**,
   **Impact**, **Prevention**, **Open questions**. The root cause is a mechanism (what the code does,
   where, and what it should do), not a symptom. Under **Reproduction** name your test. Under **Impact**
   say who was affected, and in which direction, using the log.

## Rules of the house

- Commit as you go: the tour is one change, the fix with its regression test another, the note a third.
  At least two commits; every message follows `CONTRIBUTING.md`; nothing left uncommitted.
- Money logic needs a second human reviewer. Make your diff small enough to review in five minutes.
- If an AI tool wrote or shaped any part of your work, you are still accountable for every line. Keep a
  short agent log in `docs/agent-log.md`: for each session, the prompt, what it did, what you corrected,
  how long it took. If you used no tool, say so and say what you did by hand.
- Never put real secrets or personal data in a prompt, a file or a commit. The extract in `lab-assets/` is
  constructed for teaching and holds no names.

## Done when

1. `docs/onboarding.md` exists, is true, and has the six sections.
2. A test of yours fails on the original code and passes on your fix; `pytest -q` passes.
3. The fix is a few lines in one place, and nothing else in `src` changed.
4. `docs/root-cause.md` explains the cause, the evidence and who was affected.
5. Everything is committed, with messages that follow the rules.

When you think you are done, grade it from the `ailab` folder of the course repository:
`python -m ailab grade m06 --dir <this directory>`
