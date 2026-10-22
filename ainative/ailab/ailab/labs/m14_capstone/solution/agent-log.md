# Agent log: REMIT-414

*Constructed for teaching: these rows describe a plausible working day, they are not recorded from a real model session.*

| # | Task | Prompt (short) | What it did | What I corrected | Artefact | Minutes |
|---|---|---|---|---|---|---|
| 1 | Interview for the spec | "Interview me about TASK.md, five questions at a time, read the code first, write nothing" (plan mode) | Asked 11 questions about rounding, tiers and the wallet | It assumed STD-B could be reused; I answered with Hessa's notes. I worked every number out myself and checked it with `python -m remit quote` | `specs/REMIT-414.md` | 30 |
| 2 | Plan | "Turn the spec into 9 steps, one commit each, tests first" | Proposed the steps in the wrong order: the corridor before STD-C | I moved the corridor after the providers because an existing test checks the schedule | `specs/REMIT-414-plan.md` | 15 |
| 3 | Memory and guard | "Update CLAUDE.md for corridor work; keep it under 60 lines" | Wrote 90 lines with a copy of the architecture page | Cut it to the commands, the rules, the checklist and a never list | `CLAUDE.md` | 15 |
| 4 | Tests first | "Write failing tests for AC1 to AC9, exact values, no mocks" | Wrote 21 tests in one go | Two used values it had invented (a fee of 39.50 for 2,000.00); I recalculated and fixed them | `tests/test_bdt_corridor.py` | 35 |
| 5 | The five code steps | "Do step 2, stop, show the diff" and so on, one step per prompt | Made each change correctly in `fees.py`, `fx.py`, `corridors.py`, `notify.py` | In `service.py` it first rewrote `_notify`; I asked for the smaller `SENT_TEMPLATES` lookup | `src/remit/service.py` | 40 |
| 6 | Review | "Review the diff against the spec in a fresh session, correctness and the stated requirements only" | Reported 6 points | 3 were real; 3 were style or wrong about the cap | `docs/review-REMIT-414.md` | 25 |
| 7 | Documents | "Generate docs/corridors.md from the code, then I check it" | Typed rates from memory in its first draft | I replaced them with output from the running code | `docs/corridors.md` | 20 |

Total minutes: 180
