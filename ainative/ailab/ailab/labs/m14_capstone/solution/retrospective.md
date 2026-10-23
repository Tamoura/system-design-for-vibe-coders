# Retrospective: REMIT-414, the Bangladesh corridor

Total minutes: {TOTAL} (the total at the bottom of `docs/agent-log.md`)
The commit I would redo: {HASH} `feat(fx): add the BDT mid rate and margin`, because I wrote it before I had worked out the rounding tie by hand.

### What went well
Writing the spec before any prompt paid off: the worked examples in `specs/REMIT-414.md` became the tests in `tests/test_bdt_corridor.py` almost line by line, and when the agent invented a fee of 39.50 the test failed at once. Putting the corridor last in `specs/REMIT-414-plan.md` kept the old tests green after every code commit. The guard hook in `.claude/hooks/guard.py` never fired, which is the point of a guard.

### What went wrong
I trusted the agent's first draft of `docs/corridors.md` for ten minutes before noticing it had typed the rates from memory. The review notes in `docs/review-REMIT-414.md` found the template-id risk only because I asked a fresh session; my own read had missed it.

### What the agent got wrong
It proposed STD-B for Bangladesh (the context was in Hessa's notes, not in the memory file), it ordered the plan so that the corridor came before its schedule, it invented two expected values in the first tests, and it rewrote `_notify` when a lookup table was enough. A test that pins the numbers caught the invented values; nothing caught the rewrite except reading the diff.

### What my context or spec missed
`CLAUDE.md` did not say that a corridor points at a schedule that must exist first, so the agent had to guess the order. It does now, in the checklist. The spec did not say whether the wallet has a lower maximum; I decided it does not and logged the question for Hessa.

### The five habits
Context first: slipped once, the order of the corridor steps. Specify before you delegate: held. Small verified steps: held, one commit per step. Trust evidence, not fluency: the log shows two fluent wrong answers. Automate the loop, keep the skill: I worked the rounding ties out by hand before the agent did, and I would do it again.

### Follow-ups
Ask Hessa whether wallets need a lower maximum (owner: Hessa). Add a test that every value in `SENT_TEMPLATES` exists in both languages (owner: me). The `risk.py` section of `docs/ARCHITECTURE.md` describes a module that no longer exists (owner: Tariq's clinic).
