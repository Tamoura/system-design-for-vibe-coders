# Review notes: REMIT-414

AI-assisted: yes. Claude Code drafted the tests and the five code changes in plan mode, step by step; I wrote the spec, the plan and these notes, and I read every changed line.

### Verdict
Approve with comments. The numbers match the ticket and the spec, the existing tests are untouched, and the three findings below are small. Because `fees.py`, `fx.py` and `service.py` are money files, this is not a merge until a second human has approved.

### What I ran
- `pytest -q`: every test passes, the 99 that existed and the new ones in `tests/test_bdt_corridor.py`.
- `git diff lab-start --stat`: five files in `src/remit`, one new test file, no existing test touched.
- `PYTHONPATH=src python -m remit quote QAR 500 BDT`: fee 14.50, rate 32.8745, receive 16437.25 BDT, as in the spec.
- `PYTHONPATH=src python -m remit quote QAR 99.99 BDT`: refused with `amount_out_of_range`.
- I put `src/` back to the starting state and ran the new tests: they fail, as they should.

### Findings

| File | Line | Severity | Problem | Fix |
|---|---|---|---|---|
| `src/remit/service.py` | 55 | minor | `SENT_TEMPLATES` names a template by string. A typo would raise `UnknownTemplate` after the ledger has posted, and `_notify` only catches `NotificationError`. | Add a test that every value of `SENT_TEMPLATES` exists in `notify.TEMPLATES` for every language. Follow-up ticket. |
| `src/remit/fees.py` | 96 | nit | The cap is reached at 7,727.27, so a customer pays the same fee at 8,000 and at 12,000. | Treasury confirms this is intended; record it in `docs/corridors.md`. |
| `src/remit/notify.py` | 54 | nit | The Arabic wording puts the Latin name and the id into Arabic text without direction marks, like the older messages. | Known (I-NOTIFY-1); not part of this ticket. |

### Second reviewer
`fees.py`, `fx.py` and `service.py` changed, and `CONTRIBUTING.md` wants a second human on each. I will ask Nada to check the `STD-C` numbers and the tie cases in `fees.py` and `fx.py` against the ticket, and Tariq to read the `service.py` change, which is where a wrong template id would fail after money has moved.
