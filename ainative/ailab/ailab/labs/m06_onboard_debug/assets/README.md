# lab-assets for lab m06

**Everything in this folder is constructed for teaching.** It is not real production data, it was
not recorded from a real system, and it was not produced by a real model. The bank, the customers,
the incident and every number are fictional.

| File | What it is |
|---|---|
| `incident.md` | The incident note from Maha, the SRE lead. Read it first. |
| `prod.log` | An audit trail extract, in JSON Lines (one event per line, keys sorted), in the format `najmkit.audit` writes. All timestamps are UTC. |
| `kyc_tiers.csv` | The KYC tier of every customer id that appears in `prod.log`. |

Useful to know:

- `docs/najmkit.md` explains the audit file format. The events you will meet are
  `transfer.sent`, `transfer.rejected` and `notification.failed`.
- This `prod.log` holds ids, amounts and times, and no names: the kind of extract you can reasonably
  show to an approved AI tool. A real extract needs that check, by a person, before it goes anywhere.
