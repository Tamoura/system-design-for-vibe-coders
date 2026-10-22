"""A second, different set of sound specs for lab m03: the opposite decisions, other formats, other words.

A grader must accept every sound solution, not only the reference one. These three specs resolve the same hidden
ambiguities as the reference specs but decide them the other way (the express surcharge is discounted, the fee is
floored at the minimum, the discount is rounded rather than the fee, the family may receive a little less, the cut-off
is read in the partners' time zones and falls one second later) and use other layouts (Given / When / Then lines,
sub-sections for decisions, checkboxes in the plan, tables for the context). They are test data, not a recommendation.
"""

T1 = """\
# T1: REMIT-341 Egypt fee offer

## Goal
Customers sending QAR to Egypt get 15% off the whole fee they would otherwise pay, see the saving on the quote and are told about it in the confirmation message in both languages.

## Context
Fees are priced in `src/remit/fees.py`. `explain_fee` returns the tier, the raw fee, the minimum and cap flags, the base and the express surcharge. The schedule used for Egypt, `STD-B`, is shared with Pakistan. The quote is built in `src/remit/service.py`; the confirmation text lives in `src/remit/notify.py`. Money rules are in `CONTRIBUTING.md`.

## Behaviour
Corridor `QAR-EGP`. "Full fee" means base plus express surcharge. Discount = full fee x 0.15, rounded half up to 0.01; charged fee = full fee minus discount; the charged fee is never below the schedule minimum of 6.00.

Given a standard transfer of 100.00 QAR
When the fee is priced
Then the full fee is 6.00, the discounted fee would be 5.10, the floor of 6.00 applies and the customer pays 6.00 with a saving of 0.00.

Given a standard transfer of 260.00 QAR
When the fee is priced
Then the full fee is 9.50, the discount is 1.43 (1.425 rounds up), the customer pays 8.07 and saves 1.43.

Given an express transfer of 260.00 QAR
When the fee is priced
Then the full fee is 29.50, the discount is 4.43 (4.425 rounds up), the customer pays 25.07 and saves 4.43.

Given a standard transfer of 15,000.00 QAR
When the fee is priced
Then the full fee is 120.00 (cap), the discount is 18.00 and the customer pays 102.00.

## Acceptance criteria
1. `quote_fee` for 260.00 QAR on `QAR-EGP` returns 8.07 QAR, and with `express=True` it returns 25.07 QAR.
2. `quote_fee` for 100.00 QAR on `QAR-EGP` returns 6.00 QAR: the discount never takes the fee below the minimum.
3. For 15,000.00 QAR on `QAR-EGP` the fee is 102.00 QAR, and `QAR-PKR` still returns 120.00 QAR for 15,000.00 QAR.
4. The saving shown on the quote for 260.00 QAR is "1.43 QAR" and equals full fee minus charged fee.
5. The English confirmation for a discounted transfer contains "You saved" and the Arabic one contains the saving in Arabic-Indic digits, `١٫٤٣ ريال قطري`.

## Constraints
1. Money is `Decimal` through `Money`; rounding is half up.
2. Only `src/remit/fees.py`, `src/remit/service.py` and `src/remit/notify.py` change, with their tests.
3. The offer is keyed on the corridor code, never on the schedule.
4. A second human reviewer approves the pull request because `fees.py` and `service.py` are money logic.

## Non-goals
- No end date for the offer.
- No other corridor and no loyalty tier logic.

## Decisions and open questions
### Express
The discount covers the whole fee including the express surcharge, because the ticket says "our fee" and the customer sees one number. Assumption; Hessa confirms.
### Minimum fee
The minimum of 6.00 stays a floor: a discounted fee is never lower than the schedule minimum, so tiny transfers get no discount. Finance has not seen it, so Hessa confirms with Finance.
### Rounding
The discount amount is calculated as the full fee times 0.15 and rounded half up to 0.01; the charged fee is the full fee minus that rounded discount, so the saving shown is the discount itself.
### Scope
Only the corridor `QAR-EGP` is discounted. `QAR-PKR`, which shares `STD-B`, and every other corridor stay as they are.
### Wording
The Arabic confirmation uses Arabic-Indic digits through `format_money`; a native reader approves the wording.

## Risks
Undercharging Pakistan if the offer were keyed on `STD-B`; revenue impact on every Egypt transfer; a quote and a charge that disagree.

## Test plan
Criteria 1 to 3 are tests in `tests/test_fees.py`, criterion 4 in `tests/test_service.py` and criterion 5 in `tests/test_notify.py`. Run `pytest -q`.

## Plan
Files: `src/remit/fees.py`, `src/remit/service.py`, `src/remit/notify.py` and the matching tests.
- [ ] 1. Create a branch `remit-341-egypt` and run `pytest -q`.
- [ ] 2. Add failing tests for the four Behaviour cases in `tests/test_fees.py`.
- [ ] 3. Implement the discount for `QAR-EGP` in `src/remit/fees.py`; run `pytest -q tests/test_fees.py`.
- [ ] 4. Add a failing test in `tests/test_service.py` for the saving on the quote, then add the saving to `src/remit/service.py`.
- [ ] 5. Add failing English and Arabic tests in `tests/test_notify.py`, then add the sentence in `src/remit/notify.py`.
- [ ] 6. Run `pytest -q` and read `git diff --stat`.
Rollback: `git revert` the branch's commits.
"""

T2 = """\
# T2 - REMIT-342: reverse quote

## Goal
Let a customer enter how much their family should get, in the family's own currency, and show the normal quote for the QAR amount that gets them closest to it.

## Context
| Piece | Where | What it does today |
|---|---|---|
| Forward quote | `RemitService.quote` in `src/remit/service.py` | takes QAR, returns fee, total, rate, receive amount |
| Exchange | `fx_quote` in `src/remit/fx.py` | customer rate to 4 decimals, receive rounded half up to 0.01, valid 60 seconds |
| Fee tiers | `src/remit/fees.py` | tier by the whole amount, upper bound inclusive |
| Corridor range | `validate_send` in `src/remit/corridors.py` | `min_send` and `max_send`, inclusive |
Hessa's notes are in `lab-assets/hessa-notes.md`.

## Behaviour
Corridor `QAR-INR`, customer rate 22.5720. The send amount is the typed amount divided by the rate, rounded to the nearest 0.01 QAR (half up).

| Typed (INR) | Send (QAR) | Family gets (INR) | Fee (QAR) |
|---|---|---|---|
| 10,000.00 | 443.03 | 10,000.07 | 10.86 |
| 10,001.00 | 443.07 | 10,000.98 | 10.86 |
| 22,572.00 | 1,000.00 | 22,572.00 | 20.00 |
| 1,128.60 | 50.00 | 1,128.60 | 5.00 |
| 1,000.00 | 44.31 | refused | refused |

## Acceptance criteria
- Typing 10,001.00 INR on `QAR-INR` produces a quote with send amount 443.07 QAR, family gets 10,000.98 INR and the shortfall of 0.02 INR is printed on the quote.
- Typing 22,572.00 INR produces 1,000.00 QAR and a fee of 20.00 QAR, which is the first fee tier's upper edge.
- Typing 1,000.00 INR raises `AmountOutOfRange` because the derived 44.31 QAR is below `min_send` of 50.00 QAR.
- Typing 1,128.60 INR is accepted at exactly 50.00 QAR.
- The reverse quote and the forward quote of the derived amount return equal `Quote` objects.

## Constraints
1. `Decimal` and `Money` only; rounding is half up like the rest of Remit.
2. Call `fx_quote`, `quote_fee` and `validate_send`; do not copy their arithmetic.
3. No change to existing forward behaviour or tests.
4. A second human reviewer, since `fx.py` and `service.py` are money logic.

## Non-goals
- No new currencies, no user interface, no change to rates or margins.
- No guarantee that the family gets exactly the typed amount.

## Decisions and open questions
1. The typed number is in the receive currency of the corridor; the customer pays in QAR.
2. The send amount is rounded to the nearest 0.01 QAR, half up, so the family can receive slightly less or slightly more than typed; the quote prints the real receive amount and the difference. Hessa preferred "a little too much", so this is an assumption for Hessa to confirm.
3. The fee tier comes from the derived QAR amount (whole amount, upper bound inclusive): exactly 1,000.00 QAR is still in the first tier of `STD-B` terms, and the quote shows the fee that tier gives.
4. The derived QAR amount must be inside `min_send` and `max_send`, both inclusive, otherwise `AmountOutOfRange`.

## Risks
The family can receive less than promised; support needs a script for the difference.

## Test plan
Each criterion is a test in `tests/test_service.py`; the equality criterion is a loop over 100 targets in `tests/test_fx.py`. Run `pytest -q`.

## Plan
Files: `src/remit/fx.py`, `src/remit/service.py`, `tests/test_fx.py`, `tests/test_service.py`.
1. Create the branch `remit-342-alt` and run `pytest -q`.
2. Add failing tests for the five table rows in `tests/test_service.py`.
3. Add `send_amount_for_receive` to `src/remit/fx.py`, rounding the quotient half up; run `pytest -q tests/test_fx.py`.
4. Add `quote_for_receive` to `src/remit/service.py` calling `quote`; run `pytest -q tests/test_service.py`.
5. Run `pytest -q`, read `git diff --stat`.
Rollback: `git revert` the commits.
"""

T3 = """\
# T3 - REMIT-343: cash pickup note

## Goal
When a cash pickup transfer is made after the partner counter's closing time, the confirmation (English or Arabic) says the cash will be collected tomorrow.

## Context
- `transfer_sent` is rendered in `src/remit/notify.py` and chosen in `src/remit/service.py`.
- The counters are in Manila (QAR-PHP) and Karachi (QAR-PKR); `cash_pickup` appears in `src/remit/corridors.py` for these two corridors only.
- Time arrives from the injected clock as aware UTC; `tests/test_service.py` uses `FixedClock`.

## Behaviour
The cut-off is 18:00 on the wall clock of the counter: Manila is UTC+8, so 10:00 UTC; Karachi is UTC+5, so 13:00 UTC.

| Corridor | Sent at (UTC) | Local time at the counter | Note? |
|---|---|---|---|
| `QAR-PHP` | 2026-03-02T09:59:59Z | 17:59:59 | no |
| `QAR-PHP` | 2026-03-02T10:00:00Z | 18:00:00 | no |
| `QAR-PHP` | 2026-03-02T10:00:01Z | 18:00:01 | yes |
| `QAR-PKR` | 2026-03-02T13:00:01Z | 18:00:01 | yes |
| `QAR-PKR` | 2026-03-02T12:59:59Z | 17:59:59 | no |

English: "The pickup counter has closed for today, so your recipient can collect the cash tomorrow."
Arabic: "أُغلق مركز الاستلام لهذا اليوم، لذا يمكن للمستلم استلام المبلغ نقداً غداً."

## Acceptance criteria
- A `cash_pickup` transfer on `QAR-PHP` at 2026-03-02T10:00:01Z carries the English note above, and the same transfer at 2026-03-02T10:00:00Z does not.
- A `cash_pickup` transfer on `QAR-PKR` at 2026-03-02T13:00:01Z carries the note, and at 2026-03-02T12:59:59Z it does not.
- A `bank_deposit` transfer on `QAR-PHP` at 2026-03-02T10:00:01Z gets exactly the old text.
- The Arabic confirmation for the same transfers contains the Arabic sentence above and no ASCII digits in the sentence.
- Existing tests for `transfer_sent` pass unchanged.

## Constraints
- Use the injected clock and convert with a fixed offset per corridor, kept in one dictionary.
- Arabic digits come from `localize_digits`; names and ids stay Latin.
- No new dependency and no change to `src/remit/limits.py`.
- Because `service.py` is touched, a second human reviewer is required.

## Non-goals
- No weekend logic, no holidays, no new language.
- No change to bank deposit or wallet transfers.

## Decisions and open questions
- The cut-off is in the counter's local time, Manila for `QAR-PHP` and Karachi for `QAR-PKR`, not in Qatar time. This is an assumption; Ops confirms the real closing hours of each partner.
- At exactly 18:00:00 the counter is still open: the note starts one second later, at 18:00:01.
- "Tomorrow" means the next calendar day at the counter, not a working day; Friday, Saturday and holidays are an open question for Ops.
- Only `cash_pickup` transfers on the two corridors are affected; `bank_deposit` and `wallet` keep the existing message.
- The Arabic sentence above is a draft and a native reader approves it; times in Arabic text use Arabic-Indic digits through `localize_digits`, and names stay as written.

## Risks
A counter that closes earlier than 18:00 makes the note wrong; the two zones are hard-coded.

## Test plan
The table is the test table in `tests/test_service.py`; the sentences are tested in `tests/test_notify.py`. Run `pytest -q`.

## Plan
Files: `src/remit/notify.py`, `src/remit/service.py`, `tests/test_notify.py`, `tests/test_service.py`.
1. Create the branch `remit-343-alt` and run `pytest -q`.
2. Add failing tests for the five table rows in `tests/test_service.py`.
3. Add the offsets dictionary and `is_after_cutoff` to `src/remit/service.py`; run `pytest -q tests/test_service.py`.
4. Add failing English and Arabic tests in `tests/test_notify.py`; then add the template in `src/remit/notify.py`.
5. Run `pytest -q`, read `git diff --stat`.
Rollback: delete the branch before merge, `git revert` after.
"""
