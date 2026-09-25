# Enterprise readiness review

Lesson 9.1 (🔴). A customer's security team asks Beacon to *prove* it is ready for them. This review traces two
customer actions through every component they should touch, names each seam, says what the code does today (with the
file that does it) and records every gap. It ends with the five questions the lesson says an enterprise review asks.

"Enterprise readiness is mostly seam work": every component below was built and tested on its own in Modules 1–8.
The gaps are almost all *between* components.

- **Branch:** `module-9-solution`. **Picture:** [`docs/architecture.md`](architecture.md). **Decisions:** [`docs/adr/`](adr/README.md).
- **Fixed during the review:** one seam (A3), with a test. Everything else is recorded, not built: the rule for this
  module was "no new features".

## Findings at a glance

| # | Seam | Severity | Status |
|---|---|---|---|
| A1 | A customer admin cannot remove a member at all (no remove or leave action) | High | Open: lesson 1.2 🔴 |
| A2 | No SSO or SCIM: deprovisioning in the customer's IdP never reaches Beacon | High | Open: lesson 1.4 |
| A3 | API keys created by a person kept working after their account was deleted | High | **Fixed** (below) |
| A4 | A key keeps its scopes when its creator is demoted | Medium | Open |
| A5 | Webhook endpoints a leaver created keep receiving incident data | Medium | Open |
| A6 | Escalation tiers keep departed people silently; a tier of only them pages nobody | Medium | Open |
| A7 | Invitations a leaver sent stay valid until they expire (7 days) | Low | Open |
| A8 | "Sign out everywhere" (support) ends sessions but not the membership; no admin-side equivalent | Low | Open |
| A9 | Billing seats | — | Not applicable: per-monitor pricing |
| A10 | A leaver's personal status-page subscription stays on the org's list | Low | By design |
| A11 | Resolving an incident by hand is not in the audit log, and the incident does not record who | Low | Open |
| B1 | The organization export has every row but not the files (logos, screenshots) | Medium | Open |
| B2 | Objects of deleted monitors and incidents stay in the bucket and survive the org purge | High | Open |
| B3 | Restoring a backup brings deleted orgs and accounts back; nothing replays deletions | Medium | Open |
| B4 | Events already forwarded to PostHog are not deleted with the org or the person | Medium | Open (documented) |
| B5 | The Stripe customer and its meter usage are not deleted | Low | Open (documented) |
| B6 | `email_outbox` rows for the org's people stay up to 30 days after the purge | Low | Open |
| B7 | `rate_limit_buckets` rows keyed by IP address have no retention | Low | Open |
| B8 | During the 7-day grace period the public API still accepts writes | Low | Open |
| C1 | Staff sign in like customers: no MFA, no separate hostname, no approval for impersonation | Medium | Open: lesson 7.1 🔴 |

---

## Trace A: a customer's admin removes an employee

**Scenario.** Acme is on Business. Sam, an admin, leaves Acme. Sam created an API key for Terraform and a webhook
endpoint, sent two invitations last week, is on tier 1 of the escalation policy and gets SMS alerts.

**What can actually happen today.** The lesson's version starts in the customer's identity provider. Beacon has no
IdP connection (A2), so there are only three levers, and none of them is "remove Sam":

| Lever | Who pulls it | Code | What it removes |
|---|---|---|---|
| Change Sam's role (e.g. to viewer) | Acme's owner or an admin with `member.manage` | `changeMemberRole()` in `src/lib/members.ts` | Write permissions. Sam can still sign in and read everything. |
| "Sign this user out everywhere" | Beacon support, on request, with a reason | `revokeUserSessions()` in `src/lib/admin/support.ts` | Sessions. Sam can sign in again the same minute. |
| Delete the account | **Sam**, from Account settings | `deleteAccount()` in `src/lib/privacy/user-data.ts` | The user row and everything that cascades from it. |

There is no `removeMember()` anywhere in `src/` (A1). The trace below therefore follows the one path that removes
access, **account deletion**, and notes for each seam what an admin-driven removal would need.

| Seam | Should | Does today | Gap |
|---|---|---|---|
| **Identity provider / SCIM** | Deactivating Sam in Okta removes Sam from Beacon within minutes | Not built. The `sso` entitlement exists in `src/core/plans.ts` with no feature behind it ([ADR 0002](adr/0002-authentication-better-auth.md)) | A2 |
| **Sessions** | Every session ends | `sessions.user_id` cascades on user delete (`src/db/auth-schema.ts`); there is no cookie cache, so the next request is unauthenticated (`src/lib/auth.ts`, `src/lib/session.ts`) | — |
| **Live connections** | Open dashboards stop receiving events | The SSE stream re-checks membership and session every 30 s and sends `event: revoked` (`src/lib/realtime-stream.ts`; tested in `tests/realtime.test.ts`) | ≤ 30 s window, accepted |
| **Membership** | Sam is no longer in Acme | `memberships.user_id` cascades (`src/db/schema.ts`); the account page warns first and refuses if Sam is Acme's only owner (`accountDeletionPlan()`) | A1: no admin-driven path |
| **API keys Sam created** | Revoked, or moved to a named owner | **Before this review:** kept working, `created_by` set to null. **Now:** revoked in the deletion's transaction, one `api_key.revoked` audit event each (`src/lib/privacy/user-data.ts`) | A3 fixed; A4 for demotions |
| **Webhook endpoints Sam created** | Reviewed by an admin | Keep delivering; `created_by` set to null (`src/lib/webhooks.ts`). The URL may be a receiver Sam controls | A5 |
| **Invitations Sam sent** | Reviewed, or revoked | Stay valid until `expires_at` (7 days, `src/core/invitations.ts`); `invited_by` set to null | A7 |
| **Notification preferences, inbox, phone number** | Gone | `notification_preferences`, `notifications`, `notification_deliveries` cascade on `user_id`; the phone number is on the user row (`src/db/auth-schema.ts`) | — |
| **Queued messages to Sam** | Not sent | `deleteAccount()` deletes Sam's `email_outbox` rows; pending deliveries cascade and their `notification.deliver` jobs find no row and skip (`src/lib/notifications/deliver.ts`) | — |
| **New alerts** | Never reach Sam | Recipients are resolved from current memberships when each event is delivered (`notifyInTx()` in `src/lib/notifications/pipeline.ts`) | — |
| **Escalation policy / on-call** | Sam is replaced; nobody is left un-paged | The stored tiers keep Sam's user id (`escalation_policies.tiers`). `pageInTx()` pages only current members, so Sam is skipped silently; a tier that was only Sam pages nobody and still waits its full delay. The settings page lists only current members, so the gap is invisible until someone saves (`src/lib/workflows/escalation.ts`, `src/app/[orgSlug]/settings/escalation/page.tsx`) | A6 |
| **Monitors, notes, files Sam created** | Stay with Acme | Kept, author set to null (`USER_DATA_COVERAGE` in `src/lib/privacy/user-data.ts`, checked against every foreign key by `tests/privacy.test.ts`). The "members edit only their own monitors" rule then leaves them to owners and admins (`src/core/permissions.ts`) | — |
| **Audit log** | Records who removed whom, and what followed | `member.account_deleted` in each org Sam left, `account.deleted` in the platform log, and now `api_key.revoked` per key, all in the same transaction (`src/lib/audit.ts`). Sam's past events keep Sam's name and email as evidence (`docs/security/privacy.md`) | — |
| **Staff impersonation of Sam** | Ends | `impersonation_sessions.target_user_id` cascades (`src/db/schema.ts`) | — |
| **Product analytics** | Sam forgotten, history kept | `analytics_events.user_id` set to null; already-forwarded PostHog events keep Sam's pseudonymous id | B4 |
| **Status-page subscription** | Sam's own choice | Kept: the list is Acme's, and every email has one-click unsubscribe (`src/lib/notifications/subscribers.ts`) | A10 |
| **Billing seats** | Seat count drops, prorated | Not applicable: Beacon prices per monitor, not per seat ([ADR 0005](adr/0005-billing-stripe-and-entitlements.md)); removing a member changes no invoice | A9 |

**"How many minutes until Sam's access is gone everywhere?"** If Sam deletes the account: the next request for the
session and, since the fix, for every API key Sam created; at most 30 seconds for an open live stream. If Sam does not:
**never**, unless Acme asks Beacon support, and even then only until Sam signs in again (A1, A2, A8). That answer
alone would fail an enterprise review, and it is the first thing to build next (see "Next steps").

### The seam that was fixed: A3

The lesson's check-yourself question 5, found for real. `deleteAccount()` removed the user, sessions and memberships,
but `api_keys.created_by` was `ON DELETE SET NULL` and nothing revoked the key. `verifyApiKey()` does not look at the
creator, so a key minted by Sam kept its scopes after Sam no longer existed, and API calls with it were audited as
the key, with no person behind it. A key is bounded by its creator's role only when it is created (lesson 5.2), so a
key without a creator is bounded by nothing.

- **Fix** (`src/lib/privacy/user-data.ts`, commit "Account deletion revokes the API keys the person created"): in the
  deletion's single transaction, revoke every live key the user created, in every org, and record `api_key.revoked`
  with `cause: creator_account_deleted` in each org's audit log. The rows stay in the org's key list. The account page
  now says "API keys you created are revoked" before the person confirms.
- **Proof:** `tests/privacy.test.ts`, "lesson 9.1 (the readiness review's seam): API keys the person created stop
  working with their account; the org's other keys do not": two keys in two orgs return `null` from `verifyApiKey()`
  (a 401) right after deletion, the owner's key still works, both audit logs name the revocation. The test fails on
  the previous commit.
- **Trade-off, accepted:** an integration built on a leaver's key breaks when they delete their account. That is the
  point; the audit log says which key and why, and an admin mints a new one. Keys that should outlive people need an
  explicit service-account owner ([ADR 0007](adr/0007-public-api-and-api-keys.md)).

---

## Trace B: a customer requests a full data export, then deletion

Two different subjects, handled by two different flows (`docs/security/privacy.md`): the **organization**
(Beacon is the processor; the owner asks) and a **person** (the data subject; they ask for themselves).

### Step 1: the export

| Seam | Does today | Gap |
|---|---|---|
| **Who may ask** | Owners only (the `org.export` and `org.delete` permissions in `src/core/permissions.ts`; routes in `src/app/[orgSlug]/settings/data/actions.ts`); audited as `org.export_requested` | — |
| **Every tenant table** | `buildOrgExport()` discovers tables by the `organization_id` column, not by a list; `NOT_EXPORTED` names five exceptions with reasons; secrets and hashes are omitted column by column (`src/lib/privacy/org-data.ts`). `tests/privacy.test.ts` fails if a new table is neither exported nor listed | — |
| **Runs as** | The `org.export` job, inside `withOrg()`: RLS applies to the export too; one file under `orgs/{orgId}/exports/` | — |
| **Uploaded files** | Only the `files` rows (name, type, size, storage key), not the bytes. The status-page logo and every incident screenshot are missing from the archive | B1 |
| **Billing history** | Invoices live in Stripe; the owner downloads them from the Customer Portal | — (say so in the export) |
| **Delivery** | A 5-minute signed URL, owners only, audited as `org.export_downloaded`; the file expires after 7 days (`retention.purge`, `src/lib/privacy/retention.ts`) | — |
| **A person's own data** | `GET /api/account/export` (`src/app/api/account/export/route.ts`): profile, logins (no tokens or hashes), sessions, and per org what they created and did, including their audit trail; audited as `account.data_exported` | Status-page subscriptions not included (documented) |

### Step 2: the deletion

The owner types the slug; `requestOrgDeletion()` refuses while a paid subscription is active, then sets
`deletion_scheduled_for = now + 7 days` and enqueues a delayed `org.delete` job, in one transaction
(`src/lib/privacy/org-data.ts`). Checks stop at once (`scheduleChecks()` skips the org, `src/lib/scheduler.ts`) and the
status page returns 404 (`findPublicStatusPage()` in `src/lib/organizations.ts`). After the grace period,
`purgeOrganization()` deletes objects, then the org row, and proves the result.

| Store | What happens | Evidence | Gap |
|---|---|---|---|
| **Postgres, every tenant table** (monitors, checks, incidents, notifications, deliveries, webhooks, workflows, usage, AI summaries, `llm_usage`, `llm_cache`, the org's own audit log…) | `ON DELETE CASCADE` from `organizations`, one statement | `countOrgRows()` asks Postgres' catalog for **every** table with `organization_id` and the job throws if any row is left | — |
| **Members' user accounts** | Kept: they are people, who may belong to other orgs; each can delete their own account (Trace A) | — | — |
| **Uploaded files** | The keys still referenced by `files` rows and `org_exports` rows are deleted from the bucket before the rows go | `files_deleted` in the platform audit event | **B2:** deleting a monitor or incident earlier cascaded its `files` rows but never deleted the objects (`deleteMonitor()` in `src/lib/monitors.ts`), so those screenshots and thumbnails stay under `orgs/{orgId}/` forever; the purge cannot find them, and `countOrgRows()` only proves Postgres |
| **Export files** | Deleted with the org, or after 7 days | retention job | — |
| **Queue jobs** (`pgboss` schema) | Pending jobs find no org and skip (`loadNotifyEvent()`, `runOrgExport()`); finished jobs keep their payload of ids until pg-boss's own cleanup (`deleteAfterSeconds` in `src/lib/queue/queues.ts`, 90 days for `org.delete`) | ids only, no content | Accepted |
| **Transactional email** | `email_outbox` is not a tenant table (`src/db/schema.ts`): alerts already queued or sent to the org's people keep recipient and template props until the 30-day retention | `RETENTION_RULES.emailOutbox` in `src/core/retention.ts` | B6 |
| **Suppression list** | Kept: global by address, a legitimate interest (never mail a dead or complaining address) | — | — |
| **Rate-limit buckets** | `org:<id>` and `ip:<address>` rows stay; no retention rule covers `rate_limit_buckets` | — | B7 |
| **Product analytics** | Postgres rows cascade; events already forwarded to PostHog stay there | documented in `docs/security/privacy.md` | B4 |
| **Stripe** | The subscription must be cancelled first (blocker); the customer object, invoices and reported meter usage stay at Stripe | documented | B5 |
| **Email, SMS, Slack, AI providers** | Their own retention (listed on `/trust`, `src/core/trust.ts`) | subprocessor list | contractual, not code |
| **Audit** | The org's own log goes with the org; the platform log keeps `org.deleted` with name, slug and counts for 2 years (evidence of what Beacon did) | `src/lib/audit.ts`, `src/core/retention.ts` | By design |
| **Logs, traces, errors** | Carry ids, never content; 30 days at the log platform | `src/lib/observability/logger.ts` redaction | — |
| **Backups** | Kept 30 days, then aged out (`docs/backup-and-restore.md`) | `OTHER_RETENTION` in `src/core/retention.ts` | **B3:** restoring a backup restores orgs and accounts deleted since it was taken; there is no list of deletions to replay after a restore |
| **During the grace period** | Members can sign in (to cancel); the public API keeps answering and accepts writes that will never be checked (`src/lib/public-api.ts` does not look at `deletion_scheduled_for`) | — | B8 |

---

## The five questions, answered for Beacon

### 1. Isolation: can one tenant's traffic, data or failure affect another?

- **Data:** two layers, both tested. Every query filters by org in code, and `withOrg()` makes Postgres enforce the
  same filter with row-level security as a role that owns nothing (`src/db/tenant.ts`,
  `drizzle/0007_row_level_security.sql`). Every tenant table has a policy or a written reason
  (`tests/tenant-scoping.test.ts`); every route is called as another org (`tests/cross-tenant-routes.test.ts`,
  `tests/public-api.test.ts`); AI context, cache and summaries are per org (`tests/ai.test.ts`); encrypted secrets are
  bound to their org and column, so a copied ciphertext fails to decrypt (`tests/secrets.test.ts`).
- **Traffic:** per-org token buckets for the public API sized by plan, per-IP buckets before authentication
  (`src/lib/public-api.ts`), per-org AI call limits (`src/lib/ai/gateway.ts`), invitations and SMS rate-limited.
  **Not limited:** the dashboard's own JSON routes and server actions.
- **Work:** queue fairness by group: 5 checks, 5 deliveries, 2 AI summaries per org at once; 2 webhook deliveries per
  endpoint, so a slow receiver delays only itself (`src/lib/queue/worker.ts`).
- **Failure:** all tenants share one Postgres and one worker pool. A single huge org slows everyone's checks before any
  limit notices it; the per-org share cap and cells are lesson 5.1 and 2.4 🔴 ([ADR 0003](adr/0003-tenancy-shared-schema-and-rls.md)).

### 2. Identity lifecycle: when an employee leaves, how long until their access is gone?

Answered in Trace A. Honest summary for the customer: *immediately and everywhere if the person deletes their own
account, including their API keys since this review; otherwise not until they do*. Beacon has no remove-member action
(A1) and no SCIM (A2). Both are the top of the roadmap.

### 3. Evidence: can you prove what happened?

- **Audit log:** every sensitive change writes `audit_events` in its own transaction, with actor, IP, user agent,
  request id, reason and before/after (`src/lib/audit.ts`); staff actions appear to the customer as "Beacon support";
  append-only for the app role, a hash chain per org verified nightly and by `npm run audit -- verify`
  (`src/lib/admin/audit.ts`). Customers filter and export it as CSV (Pro 30 days, Business 365). Gap A11: resolving
  an incident by hand is on the incident timeline, not in the audit log.
- **Change management:** every change goes through CI (tests, typecheck, OpenAPI and config drift, gitleaks,
  `npm audit`, trivy, the AI eval) and ships as one image promoted by digest from staging to production
  (`.github/workflows/ci.yml`, `.github/workflows/deploy.yml`).
- **Backups tested by restore:** a scripted restore drill with timings, which found and fixed a missing grant
  (`docs/backup-and-restore.md`, `scripts/restore.sh`).
- **Access reviews:** staff roles are listed at `/internal/staff`, each grant audited with a reason; customer members
  and API keys (with last use) are listed in Settings. No periodic review is scheduled.
- **Incident history:** the SLO, alerts and runbooks are in `docs/operations.md`; there is no public history of
  Beacon's own incidents yet.

### 4. Residency and exit: where does the data live, and how does a customer get it back or deleted?

- **Where:** one Postgres and one bucket, in whatever region the operator deploys; subprocessors and their locations on
  `/trust` (`src/core/trust.ts`). No per-org region: a residency requirement means a second deployment (a cell).
- **Get it back:** the org export (every table, discovered from the schema) and a person's export; B1 (files).
- **Delete it:** a 7-day grace, then a purge with a row-count proof; a person's deletion at once. Gaps: B2 (orphaned
  objects), B3 (backups), B4 (PostHog), B5 (Stripe), B6–B8.

### 5. Blast radius: what can a compromised account, key, endpoint or prompt do?

| Compromised | Can | Cannot | Contained by |
|---|---|---|---|
| **A customer's session** | What that member's role allows, in their orgs | Other orgs (404); billing unless owner | server-side sessions, deleted on sign-out, reset or deletion |
| **An API key** | Its scopes, in one org: read monitors and incidents, create/edit/delete monitors with `monitors:write` | Members, keys, billing, webhooks, settings; other orgs | revocation is immediate (no cache), per-org and per-IP buckets, audited as the key; A4 (demotion) |
| **A webhook endpoint or its secret** | Receive this org's incident payloads; forge Beacon's signature to that one receiver | Call back into Beacon; reach Beacon's network (SSRF guard, no redirects) | per-endpoint secrets, disable after 5 days of failures; A5 (leaver's endpoints) |
| **A Beacon staff account** | Support: read-only impersonation of any org's member for 30 minutes, extend trials, resend emails, sign people out. Superadmin: grant staff roles | Write while impersonating (the proxy refuses every mutating request); comp a plan without the billing role | a reason on every action, audited in the customer's own log; C1: no MFA or separate hostname for staff yet |
| **An AI prompt (injection in an incident note)** | Produce a misleading draft summary | Publish it, call tools, reach the network, see another org's data | untrusted-data framing, output checked against the facts, a person publishes, per-org cache and limits (`src/lib/ai/incident-summary.ts`); the eval's injection cases in CI |
| **The database owner credentials** | Everything, including rewriting the audit chain | — | the real risk; hash anchoring to write-once storage and a non-owner app login role are not built ([ADR 0009](adr/0009-observability-and-audit.md), [ADR 0003](adr/0003-tenancy-shared-schema-and-rls.md)) |

---

## Next steps, in order

1. **Offboarding as one service function** (A1, A4–A7): `removeMember(ctx, userId)` that deletes the membership,
   revokes the keys that person created in that org, lists their webhook endpoints and open invitations for the admin
   to confirm, removes them from escalation tiers (refusing to leave a tier empty), and records it all in one
   transaction. The account deletion and a future SCIM handler both call it.
2. **SCIM and SSO** (A2) on top of that function ([ADR 0002](adr/0002-authentication-better-auth.md)).
3. **Storage by prefix** (B1, B2): `Storage.list(prefix)` / `deletePrefix()` in both drivers; the purge deletes
   `orgs/{orgId}/` and proves the prefix is empty, like `countOrgRows()` proves Postgres; the export adds the objects.
4. **A deletion ledger** (B3): the platform audit log already holds `org.deleted` and `account.deleted`; a restore
   runbook step that replays them after any restore.
5. The small ones: retention rules for `rate_limit_buckets` (B7), refuse API writes during the grace period (B8),
   `resolved_by` and an audit event for manual resolves (A11), staff MFA (C1).

## Presenting this in 15 minutes

To a peer playing the customer's security team: 2 minutes on the architecture diagram and the tenant boundary
(`docs/architecture.md`), 5 minutes on Trace A ending with the "how many minutes" answer and the A3 fix with its test
running, 4 minutes on Trace B's store-by-store table, 4 minutes on the five questions, the blast-radius table first.
Lead with the gaps; a security team trusts the vendor who names them.
