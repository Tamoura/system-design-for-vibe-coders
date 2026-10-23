# 1. A failed notification does not undo a transfer

Date: 2026-03-12

## Status

Accepted. This ADR records, after the fact, a decision the code has embodied since the first release.

## Context

`src/remit/service.py` runs `RemitService.send` as eight steps in a fixed order: validate, limits, screening, fee, fx, ledger, store, notify. The first seven decide whether money moves. The eighth only tells the customer. By the time notify runs, the ledger has posted (`ledger.post_transfer`) and the transfer row is saved (`store.Store.save_transfer`), and neither can be taken back: the steps from the ledger onwards are not one atomic unit (the known limitation D-SVC-1 in the module docstring of `src/remit/service.py`).

Customer messages leave through a notifier that talks to a provider we do not run. When delivery fails, a notifier raises `errors.NotificationError`. The team had to choose what a failed message should do to the transfer: fail the whole send, retry until the message goes, or carry on.

## Decision

`RemitService._notify` catches `errors.NotificationError`, writes a `notification.failed` event with `najmkit.audit.log_event`, and returns False. The transfer stands. The caller sees the outcome in `service.SendResult.notified`.

## Consequences

- A provider outage cannot block or undo a customer's money. The customer's debit and the ledger postings stay consistent with the stored transfer, which is the part that matters for the bank.
- The cost is silence. A customer can pay, get no confirmation, and not know that the transfer went through. Nothing retries the message, so a lost message stays lost.
- The only trace is one audit event per failure. Unless someone watches the rate of `notification.failed` events, a long outage can go unseen for a while.
- Support has to be able to answer "did my transfer go through?" from the stored transfer, not from the message.

## Critic's objections

1. **Objection:** A customer who is not told is a customer who sends again, so best effort turns one failure into several transfers. **Response:** Accepted as a real risk, but the alternative is worse: failing after the ledger has posted would leave a posting with no transfer. We keep the decision and add an action: alert on the notification failure rate, and show a notice in the app when it is high.
2. **Objection:** Nothing retries, so the message is simply lost. A retry queue is the standard answer. **Response:** Accepted as the better design, and deferred. It needs somewhere to keep unsent messages and a rule for how long a late "sent" message is still useful. Follow-up ticket.
3. **Objection:** The steelman alternative is a transactional outbox: write the message to the same database as the transfer, and let a worker deliver it. **Response:** Rejected for now because the ledger is not in that database (`ledger.post_transfer` keeps module-level state), so the outbox would not make the steps atomic either. Revisit when the ledger is refactored.
4. **Objection:** The return value `SendResult.notified` is easy to ignore. **Response:** Rejected as a design problem: the audit event is the durable record, and the flag is only a convenience for the caller.
