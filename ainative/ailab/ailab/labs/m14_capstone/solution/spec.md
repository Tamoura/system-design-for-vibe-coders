# REMIT-414: open the Bangladesh (BDT) corridor

### Goal
Customers can quote and send money from Qatar to Bangladesh on a new corridor, `QAR-BDT`, with its own fee schedule `STD-C`, a rate and margin agreed with Treasury, and a confirmation message that Customer Care approved in English and Arabic. Every other corridor behaves exactly as it does today.

### Context
Remit has four corridors in `src/remit/corridors.py`, two fee schedules in `src/remit/fees.py` and a mid rate and margin per corridor in `src/remit/fx.py`. `BDT` is already a `Money` currency with an Arabic name in `src/remit/notify.py`, but no corridor, schedule, rate or margin exists for it. `RemitService.send` in `src/remit/service.py` always sends the `transfer_sent` template. A corridor is data in those three modules; the CLI picks it up by itself. The rules in `CONTRIBUTING.md` apply: Decimal money rounded half up, tests for new behaviour, commits as `type(scope): subject`, and a second human on every money file.

### Behaviour
All amounts are QAR unless a currency is written. Worked from the ticket:

| Case | Result |
|---|---|
| Fee for 100.00 (the minimum amount) | raw 5.70, so the minimum fee 7.00 applies |
| Fee for 167.50 | 167.50 x 2.20% + 3.50 = 7.185 exactly, so 7.19 (half up) |
| Fee for 500.00 | 14.50, express 32.50 |
| Fee for 1,000.00 and 1,000.01 | 25.50 in tier 0, 28.00 in tier 1: the whole amount decides, the bound belongs to the lower tier |
| Fee for 5,000.00 and 5,000.01 | 92.00 and 100.00 |
| Fee for 10,000.00 | raw 155.00, so the cap 130.00; express adds 18.00 after the cap: 148.00 |
| Customer rate | 33.46 x (1 - 0.0175) = 32.874450, so 32.8745 (half up) |
| 500.00 QAR buys | 16,437.25 BDT |
| 250.00 QAR buys | 8,218.625 exactly, so 8,218.63 BDT |
| 99.99 or 12,000.01 | refused: the range is 100.00 to 12,000.00 inclusive |
| `cash_pickup` | refused; `bank_deposit` is the default, `wallet` is allowed |

English message for Aisha (T2) sending 500.00 to Rahim Uddin: "Hi Aisha Rahman, your transfer TRF-000001 to Bangladesh was sent. Rahim Uddin received 16,437.25 BDT at a rate of 1 QAR = 32.8745 BDT. You paid 500.00 QAR plus a fee of 14.50 QAR. Please keep this message as your receipt." The Arabic message writes every amount and the rate in Arabic-Indic digits.

### Acceptance criteria
- AC1: the `QAR-BDT` corridor accepts 100.00 to 12,000.00 QAR inclusive and refuses one cent outside either end.
- AC2: delivery is `bank_deposit` by default, `wallet` is allowed and `cash_pickup` is refused.
- AC3: `STD-C` picks its tier from the whole amount with the upper bound included (1,000.00 is tier 0 at 25.50; 1,000.01 is tier 1 at 28.00; 5,000.00 and 5,000.01 likewise).
- AC4: the minimum fee 7.00 and the cap 130.00 apply, and the express surcharge 18.00 is added after the cap.
- AC5: fees and receive amounts round half up (a fee of exactly 7.185 is 7.19; 250.00 QAR buys 8,218.63 BDT).
- AC6: the customer rate is 32.8745, 500.00 QAR buys 16,437.25 BDT, and a quote lasts 60 seconds.
- AC7: a `QAR-BDT` transfer sends `transfer_sent_bdt` with the approved wording in the customer's language, Arabic digits included; other corridors keep `transfer_sent`.
- AC8: the KYC daily and monthly limits and the ledger postings are unchanged: a T1 customer is refused 2,000.01 in a day, and the ledger is posted in QAR.
- AC9: the four existing corridors quote exactly as before.

### Constraints
Decimal only, rounded half up, no float anywhere. Standard library only, no new dependency. `najmkit` for ids and time. No existing test is edited. Only `corridors.py`, `fees.py`, `fx.py`, `notify.py` and `service.py` change in `src/`; `limits.py`, `ledger.py` and `screening.py` stay as they are. A second human reviews the three money files that change.

### Non-goals
A daily limit for Bangladesh only, a cash pickup option and a first-transfer promotion (all from the planning meeting). Fixing the stale `risk.py` section of `docs/ARCHITECTURE.md`, which is another ticket. Real exchange-rate feeds.

### Decisions and open questions
- The maximum of 12,000.00 is a per-transfer limit on the corridor, not a daily limit: a T1 customer is still held to 2,000.00 a day and a T2 customer to 10,000.00.
- The new corridor gets its own schedule `STD-C` instead of pointing at `STD-B`, because Treasury wants a different price curve, lower for everyday amounts with a higher minimum (from Hessa's notes; Hessa confirms).
- The wallet is allowed for the whole range, as the ticket says; whether wallets should have a lower maximum is open and goes to Hessa as a follow-up.
- The wording lives in a new template `transfer_sent_bdt`, chosen by corridor code in the service, so no existing message changes.
- The rate in the message is the customer rate (32.8745), shown with the digits of the customer's language.

### Risks
A mistyped template id in the service would fail after the ledger has posted (the known limitation D-SVC-1), so a test must prove that the id exists in both languages. A rounding slip of one cent in a fee would be visible to customers at once; the tie cases in Behaviour are tests. A wrong rate would not fail any test unless the numbers are pinned, so they are. We would notice in the audit log: `transfer.sent` events carry the corridor, the amount and the fee.

### Test plan
New file `tests/test_bdt_corridor.py`, one or more tests per criterion, each naming its AC id. Run `pytest -q`; also `PYTHONPATH=src python -m remit quote QAR 500 BDT` and compare it with the table above. The existing tests must pass unchanged.
