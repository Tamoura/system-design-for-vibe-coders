# INC-2031: Customers did not receive their transfer-sent message for 52 minutes

Severity SEV3. Service: Najm Remit, version 0.4.0. Date: 11 March 2026. Incident commander: Maha. All times are UTC.

## Summary

On 11 March 2026, from 09:58 to 10:50 UTC (52 minutes), Najm Remit kept completing transfers but could not send the "transfer sent" message to customers. The audit log shows 171 `notification.failed` events with template `transfer_sent` against 188 `transfer.sent` events in the window (E1, E9). A reconciliation afterwards found no mismatch between the ledger and the store (E13). The alert fired 13 minutes after the first failure (E1, E2). The cause is not established.

## Impact

- Customers: 171 `notification.failed` events with template `transfer_sent`, against 188 `transfer.sent` events. The record counts events, not customers.
- Money: the reconciliation checked 188 transfers; the ledger and the store agree for all of them, with 0 mismatches (E13).
- Support: 64 tickets tagged "no confirmation" were opened between 09:58 and 11:10 UTC.
- Rejections: 23 `limit_exceeded` rejections in the window, against 9 in the same window one week earlier (4 March).

## Timeline

| Time (UTC) | What happened | Record id |
|---|---|---|
| 09:58 | First `notification.failed` event of the day: template `transfer_sent`, reason `notification_error`. | E1 |
| 10:11 | Alert fired: notification failure rate above 20% for 10 minutes. The on-call SRE was paged. | E2 |
| 10:14 | The on-call SRE acknowledged the page. | E3 |
| 10:19 | INC-2031 was opened in the payments incidents channel at SEV3. Maha took the incident commander role. | E4 |
| 10:26 | A payments engineer read the audit log: transfers were still completing, and every `notification.failed` event had reason `notification_error`. | E5 |
| 10:30 | The notification gateway vendor's status page posted: "Investigating delayed message delivery". | E6 |
| 10:36 | The customer support lead said callers were asking where their confirmation was, and asked for a line to give them. | E7 |
| 10:41 | A notice was added to the Najm app: the transfer goes through even if the confirmation message is late. | E8 |
| 10:50 | Last `notification.failed` event of the window. | E9 |
| 10:52 | The alert resolved on its own. | E10 |
| 11:02 | The vendor's status page posted that message delivery was back to normal. | E11 |
| 11:10 | Maha closed INC-2031. | E12 |
| 11:40 | Reconciliation of the window finished: 188 transfers checked, ledger and store agree, 0 mismatches. | E13 |

## What we know

- At 10:26 a payments engineer read the audit log and found every `notification.failed` event with reason `notification_error` (E5). The record's counts for the whole window are 171 events with template `transfer_sent` and 4 with template `transfer_failed`.
- Transfers kept completing, and no transfer is missing from the ledger or the store (E5, E13).
- No deploy or configuration change was made during the window. The last deploy was version 0.4.0 on 9 March.
- The alert rule is a failure rate above 20% for 10 minutes; it fired at 10:11, 13 minutes after the first failure and 41 minutes before it resolved (E1, E2, E10).
- The vendor's public status page reported delayed message delivery at 10:30 and "Resolved" at 11:02 (E6, E11).

## What we infer

1. The failures came from the gateway side. Confidence: medium. It rests on E6 and E11, which bracket most of the failure window, and on E5 (one error reason in what the engineer read at 10:26). The vendor's incident report, or the gateway response codes in our own logs, would confirm or refute it.
2. Most of the 188 transfers had no confirmation. Confidence: medium. It rests on 171 failures against 188 sends, but events are not customers and a retry could have delivered some. Joining the failed events to transfer ids would check it.
3. The extra `limit_exceeded` rejections (23 against 9) may come from customers sending again after seeing no confirmation. Confidence: low. It rests on E7 and on the counts alone. Checking whether rejected customers had a similar transfer minutes earlier would confirm or refute it.
4. Detection was slow mostly because of the alert rule. Confidence: medium. The rule needs 10 minutes of failures (E2). Replaying the failure rate through the rule would confirm it.

## What we do not know

- Why message delivery degraded at the vendor, and whether that is the cause of our failures.
- Why 17 of the 188 transfers did not have a failed confirmation event while the rest did.
- Whether any customer sent a transfer again because no confirmation arrived.
- How many of the 64 tickets came from customers who had a transfer in the window.
- How many distinct customers the failures represent: the record counts events, not customers.

## Action items

1. Alert on the notification failure rate over a shorter window than 10 minutes. Owner: SRE on-call team. Done when a replay of INC-2031 fires the alert within 5 minutes.
2. Show the in-app notice automatically when the failure-rate alert fires. Owner: payments engineering. Done when a test alert turns the notice on and off.
3. Decide how failed confirmations are retried, and write the ADR. Owner: payments engineering. Done when the ADR is merged.
4. Match the tagged support tickets to transfers in the window, to answer the open questions. Owner: customer support lead with a payments engineer. Done when the numbers are added to this review.
