# Privacy and GDPR

Lesson 8.1. Beacon's customers (organizations) are the **controllers** of their data: their team, their monitors,
their status-page subscribers. Beacon is their **processor**. This page is what that means in the code.

## Obligations and where they live

| Obligation | In Beacon |
|---|---|
| DPA (Art. 28) | A contract, not code. The subprocessor list it refers to is `SUBPROCESSORS` in `src/core/trust.ts`, published on `/trust`. |
| Subprocessor list, notice before adding one | `src/core/trust.ts`; a new vendor is added in the pull request that integrates it (SECURITY.md). |
| Access and portability, for a person (Art. 15, 20) | **Account settings → Download my data** → `GET /api/account/export` (`src/lib/privacy/user-data.ts` `exportUserData`). Audited as `account.data_exported`. |
| Portability, for the organization | **Settings → Data & privacy → Export data** (owners): an `org.export` job writes one JSON file with every tenant table to object storage; a 5-minute signed download link; the file expires after 7 days. `src/lib/privacy/org-data.ts`. Audited: `org.export_requested`, `org.export_downloaded`. |
| Erasure, for a person (Art. 17) | **Account settings → Delete your account**. The rules for orgs they own are below. Audited: `account.deleted` (platform) and `member.account_deleted` in each org they left. |
| Erasure, for the organization | **Settings → Data & privacy → Delete organization** (owners, typing the slug): checks stop and the status page goes offline at once; after 7 days the `org.delete` job deletes the org's files, then the org row, and Postgres cascades to every tenant table. `countOrgRows()` proves nothing is left (it asks Postgres' catalog for every table with `organization_id`), and the job fails loudly if anything is. Audited: `org.deletion_requested`, `org.deletion_cancelled`, and `org.deleted` in the platform log. |
| Retention | `src/core/retention.ts`, enforced nightly by the `retention.purge` job; the table below. |
| Breach notification (72 hours for the controller) | The incident process (docs/operations.md) starts a clock; the audit log (7.3) and request ids (7.2) answer "whose data, since when". |
| International transfers | A deployment decision: the region of the database, and the subprocessors' locations on `/trust`. |

## Deleting an account: the org-ownership edge cases

`accountDeletionPlan()` decides before anything is deleted, and the account page shows its answer:

- **Only owner of an org that has other members:** refused. Make another member owner first. An org is never left without an owner (lesson 1.2).
- **Only member of an org:** the org is scheduled for deletion together with the account (the same 7-day grace; Beacon support can stop it).
- **Such an org still has an active paid subscription:** refused until it is cancelled, so nobody is billed for an org without people.
- **Beacon staff:** refused; staff are removed with `npm run staff -- remove`.

What the person created in an org they leave (monitors, incident notes, files) stays with the org, which is the
controller; the author columns become `null`. Their sessions, sign-in methods, memberships, notifications,
preferences and queued emails are deleted.

**Kept on purpose:** audit events keep the actor's name and email as they were when the person acted. The audit
log is evidence (lesson 7.3), its hash chain covers those fields, GDPR Art. 17(3)(e) allows keeping records needed
for legal claims, and the audit retention deletes them on schedule. Rewriting them would break the chain; a
future version could store a pseudonym plus a separately erasable mapping.

## Retention

Keep this table in sync with `src/core/retention.ts` (the trust page and **Settings → Data & privacy** render
from that file directly).

| Data | Kept | Enforced by |
|---|---|---|
| Check results | 90 days | `retention.purge` (nightly) |
| Webhook events, messages, attempts | 30 days | `retention.purge` |
| Notifications and their deliveries | 180 days | `retention.purge` |
| Sent or failed emails (outbox) | 30 days; pending ones are never deleted | `retention.purge` |
| Organization export files | 7 days | `retention.purge` (the file first, then the row) |
| Audit log | By plan: Business 365 days, Pro 30; platform events 2 years | `audit.retention` (lesson 7.3) |
| A deleted organization | 7 days to cancel, then purged | `org.delete` |
| Backups | 30 days | your backup schedule (docs/backup-and-restore.md) |
| Application logs | 30 days | your log platform; no passwords, keys, cookies or AI prompt text in them |

## Not built (lesson 8.1's 🔴 exercise)

Per-tenant data keys and crypto-shredding, deletion from an external analytics warehouse or search index (Beacon
keeps both in Postgres, so the cascade covers them; PostHog, when configured, needs its own deletion API call), a
Stripe customer deletion, and status-page subscriptions in a person's export (they belong to each org's list and
every email has a one-click unsubscribe).
