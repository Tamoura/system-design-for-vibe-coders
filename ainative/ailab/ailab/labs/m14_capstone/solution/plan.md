# Plan for REMIT-414: the Bangladesh corridor

### Steps

| # | Step | Files | Proves | Check | Commit |
|---|---|---|---|---|---|
| 1 | Write the tests first and watch them fail for the right reason | `tests/test_bdt_corridor.py` | AC1 to AC9 | `pytest -q tests/test_bdt_corridor.py` fails on missing BDT, not on a typo | `test(corridors): pin the Bangladesh corridor, fees, rate and wording` |
| 2 | Add the STD-C schedule | `src/remit/fees.py` | AC3, AC4, AC5 | the fee tests pass; the corridor tests still fail | `feat(fees): add the STD-C fee schedule for Bangladesh` |
| 3 | Add the BDT mid rate and margin | `src/remit/fx.py` | AC5, AC6 | the rate tests pass | `feat(fx): add the BDT mid rate and margin` |
| 4 | Open the corridor, last, because it points at STD-C | `src/remit/corridors.py` | AC1, AC2, AC9 | `pytest -q`; `python -m remit quote QAR 500 BDT` | `feat(corridors): open the QAR-BDT corridor` |
| 5 | Add the approved wording in both languages | `src/remit/notify.py` | AC7 | the template tests pass | `feat(notify): add the transfer_sent_bdt wording` |
| 6 | Choose the template by corridor and pass the rate | `src/remit/service.py` | AC7, AC8 | all tests pass; money file, second reviewer | `feat(service): send the Bangladesh wording on QAR-BDT transfers` |
| 7 | Record the decision about the schedule | `docs/adr/0001-own-fee-schedule-for-bangladesh.md` | AC3 | Nygard sections complete | `docs(adr): record why Bangladesh gets its own fee schedule` |
| 8 | Write the corridors page and fix the architecture notes | `docs/corridors.md`, `docs/ARCHITECTURE.md` | AC1, AC3 | every number copied from the running code | `docs(docs): add the corridors page and fix the architecture notes` |
| 9 | Review my own diff as a stranger | `docs/review-REMIT-414.md` | AC7, AC8 | findings with file and severity | `docs(review): review the REMIT-414 diff` |

### Order and why
Tests first, so that the agent has something to be held to. Then the providers before the consumer: the corridor entry refers to `STD-C` and to the rate, and an existing test checks that every corridor points at a real schedule, so adding it first would turn the suite red. The wording comes after the numbers because it needs the rate. Documents come last, copied from the running program.

### Stop rules
Stop the agent and take the wheel when a diff touches a file outside the list above, when an existing test is edited, when a float or a new dependency appears, when it proposes to change `limits.py` or `ledger.py`, or when a fee does not match the Behaviour table in the spec.

### Rollback
Every step is one commit on its own branch, so `git revert` of the step undoes it. To remove the whole corridor, revert steps 6, 5, 4, 3 and 2 in that order; no data is migrated, because the corridor only adds entries to tables in code.
