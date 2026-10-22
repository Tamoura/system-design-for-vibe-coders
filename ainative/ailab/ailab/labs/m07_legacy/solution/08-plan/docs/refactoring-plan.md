# Refactoring plan: REMIT-372, an injectable Ledger and najmkit 2

**Owner:** Najm Learner · **Second reviewer:** Tariq · **Agent and mode:** Claude Code, plan mode for this plan and acceptEdits for the steps · **Pull request labelled AI-assisted:** yes

### 1. Why, and what must not change
- Why: the reporting job needs two services in one process, and a module-level ledger cannot give it two sets of books. najmkit 1 loses support in 3.0.
- Must not change (each pinned by a test): the order and amounts of the four postings, the half-even partner share (Q-LED-1), reading an unknown account creates it (Q-LED-2), entry ids and times from najmkit (Q-LED-3), QAR only and zero legs not posted (Q-LED-4), the audit lines byte for byte, and the store-failure limitation D-SVC-1.
- May change: nothing by agreement. The one deliberate difference is that two Ledger objects no longer share their books, which is the ticket.

### 2. What I do not understand yet
- Whether anything else reads the module-level ledger: searched `src` and `tests` for `ledger.`; only `service.py` and `conftest.py` do.
- Whether `posted_at` must be identical for the four legs: pinned by a test, the clock is read four times and a fixed clock hides it.

### 3. The safety net
- `tests/test_ledger_characterization.py`, written first and run against the original code, through the seam in `tests/ledger_port.py`.
- Mutation check: I broke the original ledger sixteen ways by hand and every break fails at least one test.
- Not covered: concurrent postings (the module never claimed to be thread safe).

### 4. The seams and the steps
| # | Step | Kind | Check after the step | Commit message |
|---|---|---|---|---|
| 1 | Characterization tests and the test seam | tests only | suite green on the original code | test(ledger): pin the ledger's current behaviour |
| 2 | `Ledger` class, module functions wrap one instance | refactor | suite green | refactor(ledger): add a Ledger class |
| 3 | `RemitService(..., ledger=None)` | refactor | suite green | refactor(service): give RemitService its own Ledger |
| 4 | Delete the module functions and `reset()` | refactor | suite green, conftest edited | refactor(ledger): remove the module-level state |
| 5 | Call sites to the najmkit v2 names | migration | `-W error::DeprecationWarning` green | refactor(najmkit): move Remit to the v2 names |
| 6 | Delete the deprecated v1 names | migration | suite green | refactor(najmkit): remove the deprecated v1 names |
| 7 | docs/najmkit.md | docs | read against the code | docs(najmkit): describe the v2 API |

### 5. Delegation
- For the agent: steps 2, 3 and 5 (mechanical, a rule I can state), each with "do not change behaviour and do not edit the characterization tests".
- I keep: step 1 (I read every expectation), the `audit.emit` conversions in step 5 (the fraud team's parser), and every merge decision.
- Instruction: scope is `src/remit/ledger.py` for step 2; stop and ask if a characterization test fails; no formatting changes.

### 6. Review at scale
- Read in full: the characterization tests, `ledger.py`, the `audit.emit` call sites.
- Sampled by hand: `tests/test_najmkit.py` hunks and every file the migration touched, first and last hunk.
- Automated: full suite on every commit, `-W error::DeprecationWarning`, a search for the six v1 names, `git diff --stat` against the plan.

### 7. Rollback and done
- Each step is one commit and is undone with `git revert`. I stop and ask if a step needs a change to a characterization test.
- Done: tests green, characterization tests unchanged since step 1, v1 names gone, `docs/najmkit.md` and CLAUDE.md updated.
