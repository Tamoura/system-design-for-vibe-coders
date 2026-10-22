# REMIT-318: warn customers when a transfer takes them to 80% of their daily limit

## Goal
After a successful transfer that leaves a customer's total for the Qatar day at 80% of their KYC tier's daily limit or more, send one extra notification, `limit_warning`, in the customer's language. It says what share of the limit is used and how much can still be sent today. Nothing else about sending, limits or fees changes.

## Context
- `RemitService.send` in `src/remit/service.py` already computes the limit position before the transfer: `SendResult.limits.daily_used` and `daily_limit` come from `check_limits` and do NOT include the transfer being made, so the total after is `daily_used + send_amount`.
- `src/remit/notify.py` holds `TEMPLATES` (English and Arabic) and `render`, which formats `Money` and `Decimal` values for the language: Arabic-Indic digits, `٬` and `٫`, the Arabic currency name. An `int` is left as it is, so a percentage passed as an `int` would print Western digits in Arabic.
- `service._notify` already delivers best effort: it catches `NotificationError` and audits `notification.failed`.
- The daily limits are T1 2,000.00, T2 10,000.00 and T3 30,000.00 QAR. The day is a Qatar calendar day (UTC+3). The limits count amounts sent, never fees.
- `CONTRIBUTING.md`: Decimal money, no floats, tests with new behaviour, Conventional Commits, a second human reviewer for `service.py`.

## Behaviour
Customer Bilal, T1, English, nothing sent earlier today (daily limit 2,000.00):

| Sends | Total after | Warning? | Text shows |
|---|---|---|---|
| 1,599.99 | 79.99995% | no | |
| 1,600.00 | 80% | yes | 80%, 400.00 QAR left |
| 1,615.00 | 80.75% | yes | 80% (rounded down), 385.00 QAR left |
| 1,999.99 | 99.9995% | yes | 99%, 0.01 QAR left |
| 2,000.00 | 100% | yes | 100%, 0.00 QAR left |
| 1,000.00 then 600.00 | 50%, then 80% | only the second | 80%, 400.00 QAR left |
| 1,600.00 then 100.00 | 80%, then 85% | both | 80%, then 85% |
| 1,500.00 on each of five days | 75% each day | never | the monthly total reaches 93.75% and is ignored |
| 1,000.00 at 23:59 and 700.00 at 00:00 Qatar time | 50%, then 35% | never | a new Qatar day starts at 21:00 UTC |
| 1,500.00 then 600.00 | 75%, then refused | no warning on the refusal | the usual transfer_failed message |

Arabic, Mariam, T3 (daily limit 30,000.00), sends 24,000.00: the Arabic wording, with Arabic-Indic digits, `٨٠٪` and `٦٬٠٠٠٫٠٠ ريال قطري`.

## Acceptance criteria
- `TEMPLATES["limit_warning"]` has exactly `en` and `ar`, with the approved wording and the placeholders `{name}`, `{percent}`, `{remaining}`.
- A total of exactly 80% of the daily limit gets one `limit_warning` straight after `transfer_sent`; one cent less gets none.
- The percentage is the share used, rounded down to a whole number; the remaining amount is the limit minus the total.
- Every later successful transfer in the same day at 80% or more gets its own warning.
- The text is in the customer's language and the Arabic text contains no Western digits.
- A refused or held transfer sends no warning; the monthly limit and earlier days play no part.
- A `NotificationError` on the warning leaves the transfer stored, `SendResult.notified` True and an audit event `notification.failed` for `limit_warning`.
- `send` keeps its signature, `SendResult` its fields; the three existing templates and the 99 existing tests are unchanged and pass.

## Constraints
Money stays `Decimal`; no `float`, no float literal. No new dependency. Only `notify.py`, `service.py`, tests, the spec and docs change. No existing test is edited. `service.py` is money logic: a second human reviewer, and the pull request is labelled AI-assisted.

## Non-goals
No change to limits, fees, rates, screening or the ledger. No special wording at 100%. No per-customer settings. No new notification channel. No "already warned today" state.

## Decisions and open questions
- The total counts amounts sent, not fees, because `check_limits` adds up `send_amount`; the ticket says the same.
- The threshold is compared as `total >= limit * 0.80` in Decimal, so 80% exactly warns; a float 0.8 would not compare equal to Decimal 0.80.
- The percentage is rounded down so a customer never reads 100% before the limit is reached; the ticket asks for this.
- The warning is sent through `_notify`, so a failed delivery is audited and never undoes the transfer; this is the behaviour of `transfer_sent` today.
- The Arabic wording is the content team's and is copied character for character; a native reader approves any change. Assumption: Hessa confirms the English wording.
- The percentage is passed to `render` as a `Decimal`, so that Arabic digits come from `format_number` and not from the caller.

## Risks
A missing warning is invisible: the customer simply hits the limit as before, so the tests must pin the line from both sides. A warning on a refused transfer would contradict the failed message. Reviewers can miss an Arabic digit problem, so the Arabic text is tested for Western digits.

## Test plan
- `tests/test_limit_warning.py` proves each criterion: wording in both languages, the line at 1,599.99 and 1,600.00, rounding down, the cumulative day, an Arabic customer, a refused transfer, a failed delivery.
- Run `pytest -q`; every commit must be green. Run a real send by hand for 1,700.00 as T1 and read both messages.

## Plan
Files expected: `src/remit/notify.py`, `src/remit/service.py`, `tests/test_limit_warning.py`, `docs/ARCHITECTURE.md`.
1. Commit this spec and plan. Check: none. Rollback: revert the commit.
2. Add the template and its wording tests in one commit. Check: the wording tests fail first, then `pytest -q` is green.
3. Add the decision in `RemitService.send` with the line tests: 1,599.99 and 1,600.00, rounding, the running total. Check: tests red before, green after.
4. Add the edge tests: Arabic customer, refused transfer, failed delivery. Check: `pytest -q`; run the new tests against the starting code and see them fail.
5. Document the warning in `docs/ARCHITECTURE.md`; write the agent log. Check: read the diff.
Rollback for the whole change: delete the branch.
