# REMIT-318: warn customers when a transfer takes them to 80% of their daily limit

**From:** Hessa, Product Owner, Najm Remit
**To:** Payments Platform
**Priority:** Medium. Support sees this complaint every week.

Customers hit their daily sending limit without warning. The first they hear of it is "It would
take you over your sending limit", on a transfer that failed, while the family at home waits.
Let them see it coming.

## What I need

When a transfer **succeeds** and brings the customer's total for the day to **80% of their daily
limit or more**, send one more notification straight after "transfer sent". It says how much of
the limit they have used and how much they can still send today.

1. **The day** is the Qatar day, as `limits.py` defines it. **The total** is the amounts sent
   today (not fees) plus the transfer just made. **The limit** is the daily limit of their KYC tier.
2. **80% counts**: exactly 80% gets the warning, one cent less does not. Exactly 100% is allowed,
   and warned.
3. **Every** successful transfer at 80% or more gets the warning, not only the first to cross.
4. Only the **daily** limit matters; being near the monthly limit sends nothing.
5. A refused or held transfer sends no warning, only the usual "transfer failed" message.
6. The warning is in the customer's language, `en` or `ar`.
7. The percentage is a whole number, **rounded down**: at 99.95% the customer sees 99%, never 100%.
8. Best effort, like "transfer sent": if it cannot be delivered the transfer still stands, `send`
   returns normally, and the failure is audited like other notification failures.

## The interface, exactly

- A new template `limit_warning` in `notify.TEMPLATES`, in `en` and `ar`, with the placeholders
  `{name}`, `{percent}` (a whole number, passed as a `Decimal`) and `{remaining}` (a `Money` in
  QAR: the limit minus the total).
- The content team's wording, **character for character**. Copy and paste both lines into your code
  and your tests; the Arabic uses `٪` and `،`:
  - English: `Hi {name}, this transfer takes you to {percent}% of your daily sending limit. You can send {remaining} more today.`
  - Arabic: `مرحباً {name}، بهذا التحويل وصلت إلى {percent}٪ من حد الإرسال اليومي. يمكنك اليوم إرسال مبلغ إضافي أقصاه {remaining}.`
- So `render("limit_warning", "en", name="Bilal Khan", percent=Decimal(85), remaining=Money("300.00", "QAR"))`
  says `85%` and `300.00 QAR`. In Arabic every digit is an Arabic-Indic digit, as in our other messages.
- `RemitService.send` keeps its signature and `SendResult` its fields (`notified` still reports only
  the "transfer sent" message). The warning goes through the notifier like any message: for a
  warned transfer, `InMemoryNotifier.sent` ends with `transfer_sent`, then `limit_warning`. The
  existing messages do not change.
- Not in scope: changing limits, fees, rates, screening or the ledger; special wording at 100%; new
  channels or dependencies.

## Done when

- `specs/REMIT-318.md` (from `specs/TEMPLATE.md`, with your plan) is committed before any code. It
  records your decisions where this ticket is silent, for example whether to warn when "transfer sent"
  itself failed to deliver, and where a failed warning's audit entry falls. Either is accepted.
- You worked in **small steps**: three commits or more (the spec commit counts), each with `pytest -q`
  green and a message as `CONTRIBUTING.md` says (any lower-case scope, such as `docs(specs):`),
  nothing left uncommitted. The project memory lets an agent commit only when the task asks; this
  one does: ask it to, or commit yourself.
- You added tests and did not edit the old ones. They fail if the warning is removed and they pin
  the behaviour: the exact message in both languages, the percentage, totals just under and
  exactly at 80% (through `send`), and nothing sent when a transfer is refused.
- You touched only: `src/remit/notify.py`, `src/remit/service.py`, a helper in `src/remit/limits.py`
  or one new module under `src/remit/`, `tests/`, `specs/`, `docs/`, `agent-log.md` and the memory
  file (`CLAUDE.md` or `AGENTS.md`); under `src/`, at most four files and 120 changed lines. Money is
  `Decimal`; no secrets. Money logic needs a second human reviewer, and AI-assisted work carries the
  label (`CONTRIBUTING.md`).
- `agent-log.md` has an entry (one line, if you used no AI tool). You read every diff and can explain
  every line.
- Grade it from the `ailab` folder of the course repository, with your branch checked out in this
  directory: `python -m ailab grade m04 --dir <this directory>`
