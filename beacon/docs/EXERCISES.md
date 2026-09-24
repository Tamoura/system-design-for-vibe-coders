# Beacon exercises, lesson by lesson

Every exercise from the **SaaS Building Blocks** course's "🛠️ Build it into Beacon" sections,
copied here so you can work without switching tabs. Read the lesson first — the exercises assume it.

- **Course:** https://tamoura.github.io/system-design-for-vibe-coders/saas/ (English) · https://tamoura.github.io/system-design-for-vibe-coders/saas/index.ar.html (العربية)
- **Reference solutions:** the `module-N-solution` branches implement the 🟢 Beginner and 🟡 Intermediate
  exercises of every lesson in module N, on top of the previous module's solution. 🔴 Advanced exercises are
  left as stretch goals — no solution is provided, on purpose.

Try the exercise before you look. When you do look, compare with `git diff module-(N-1)-solution module-N-solution`.

## Module 1 — Identity & Access

Solution branch: `module-1-solution`

### 1.1 — Authentication: proving who someone is

#### 🟢 Beginner exercise

Add email-and-password sign-up and login to Beacon using Better Auth (or Devise, django-allauth, or Laravel's starter kits in your stack). Protect the `/monitors` pages so logged-out users are redirected to `/login`. Add a logout button that deletes the server-side session.

**Done when:**
- Passwords are stored as argon2id or bcrypt hashes. Grep your database dump for a test password and find nothing.
- The session cookie is `HttpOnly`, `Secure` in production, and `SameSite=Lax`.
- After logout, replaying the old cookie with `curl` returns a redirect or 401.

#### 🟡 Intermediate exercise

Add "Sign in with GitHub" and a password-reset flow. Link a GitHub identity to an existing user only when GitHub reports the email as verified *and* the user confirms by signing in with their existing method. Make the reset request endpoint return the same response for known and unknown emails.

**Done when:**
- The OAuth flow uses the authorization code grant with PKCE and validates `state`.
- Reset tokens are hashed in the database, expire within an hour, and fail on second use.
- A completed reset signs out every other session for that user.
- Response bodies for "reset my password" are byte-identical for existing and non-existing emails.

#### 🔴 Advanced exercise

Add passkeys and TOTP as second factors, a "Signed-in devices" page, and step-up re-authentication for "create API key" and "delete organization". Rate-limit login by IP and by account using Redis.

**Done when:**
- A user can register a passkey and sign in with it without a password.
- TOTP enrolment issues ten hashed, single-use recovery codes.
- Revoking a device on the devices page makes that browser's next request unauthenticated.
- Twenty failed logins in a minute for one account trigger a slowdown or CAPTCHA, not a permanent lockout.

### 1.2 — Users, organizations & invitations: the multi-tenant skeleton

#### 🟢 Beginner exercise

Add `organizations` and `memberships` tables and move `monitors` from `user_id` ownership to `org_id` ownership, keeping `created_by`. On sign-up, create a personal org with the user as `owner`. Put the org slug in the URL: `/[orgSlug]/monitors`.

**Done when:**
- Every monitor row has a non-null `org_id` and every monitor query filters on it.
- Visiting `/some-other-org/monitors` as a non-member returns 404.
- A migration moves existing user-owned monitors into each user's personal org.

#### 🟡 Intermediate exercise

Build invitations: an admin enters an email and role, the invitee gets an email link, and accepting creates a membership. Support revoke and resend. Add an org switcher listing every org the user belongs to.

**Done when:**
- Invitation tokens are hashed, expire in 7 days, and cannot be reused.
- An invite for `sam@acme.com` cannot be accepted by a user logged in as `sam@gmail.com`.
- A user with no account can sign up from the invite link and lands inside the org.
- Invites are rate-limited per org.

#### 🔴 Advanced exercise

Implement leave, remove member, ownership transfer and org deletion with a 30-day grace period. Add a Postgres row-level security policy on `monitors` as a backstop, so a query without an org filter returns nothing.

**Done when:**
- The last owner cannot leave or be demoted, and the UI explains why.
- Ownership transfer requires re-authentication and emails both parties.
- A deleted org is inaccessible immediately, restorable for 30 days, and purged by a scheduled job after that.
- With RLS on, `SELECT * FROM monitors` from the app's database role returns only the current org's rows.

### 1.3 — Authorization: roles, permissions, and "can this user do this?"

#### 🟢 Beginner exercise

Add the owner/admin/member/viewer roles from the matrix above. Implement `requirePermission()` and call it from every monitor, incident and status-page endpoint. Hide buttons in the UI based on the same permissions map.

**Done when:**
- Every mutating endpoint calls `requirePermission()` before doing work.
- A viewer calling `DELETE /api/monitors/:id` with `curl` gets 403.
- Every monitor query includes `orgId`, and fetching another org's monitor id returns 404.

#### 🟡 Intermediate exercise

Add request-body validation with Zod (or your stack's equivalent) on every write endpoint, and response DTOs on every read endpoint. Implement role-change rules: users can only assign roles at or below their own, and never change their own role. Add one ABAC rule: members may edit only monitors they created.

**Done when:**
- Sending `{"orgId": "<other org>"}` or `{"role": "owner"}` in a body has no effect.
- No API response contains columns not listed in its DTO.
- An admin cannot promote anyone to owner, and nobody can change their own role.
- An automated test calls each endpoint as each role and checks the expected status codes.

#### 🔴 Advanced exercise

Introduce per-status-page sharing with OpenFGA (or SpiceDB): a team or individual can be made editor of one status page without admin rights. Keep tuples in sync with memberships using an outbox table processed by a background job. Build a "my status pages" list using `ListObjects`.

**Done when:**
- Removing a membership removes the user's access to every status page in that org within seconds.
- The list endpoint returns exactly the pages a single-object check would allow.
- An admin page answers "why can this user edit this page?" by showing the relationship path.

### 1.4 — Enterprise identity: SSO, SAML, OIDC and SCIM

#### 🟢 Beginner exercise

Run authentik or Keycloak locally with Docker as a test IdP. Self-host SAML Jackson (Ory Polis) and connect one Beacon org to your local IdP. Let a user log in via SSO and land in the right org.

**Done when:**
- A user created in the local IdP can sign into Beacon without a Beacon password.
- The user lands in the org that owns the connection, with the default role.
- A tampered or expired SAML response is rejected with a clear error in logs.

#### 🟡 Intermediate exercise

Add domain verification by DNS TXT record, home realm discovery on the login page, JIT provisioning with IdP group-to-role mapping, and an "enforce SSO" org setting with a break-glass owner exception.

**Done when:**
- An org cannot configure SSO for a domain until the TXT record is verified.
- Typing an email on a verified domain routes to that org's IdP automatically.
- With enforcement on, a password login to that org is refused for everyone except the designated break-glass owners, and each break-glass login is audited and emailed.
- Changing a user's IdP group changes their Beacon role on next login.

#### 🔴 Advanced exercise

Implement a SCIM 2.0 server for Users and Groups (or use Ory Polis's directory sync and consume its events). Connect it to your local IdP and to one real IdP developer tenant (Okta and Microsoft Entra ID both offer free developer tenants). Support two connections on one org, routed by domain.

**Done when:**
- Assigning a user to Beacon in the IdP creates their membership without them logging in.
- Deactivating a user in the IdP ends their Beacon sessions for that org and revokes their API keys within a minute.
- `GET /scim/v2/Users?filter=userName eq "..."` returns results in the RFC 7644 list-response format.
- Both connections work at once, and an email from either domain reaches the correct IdP.

## Module 2 — Data

Solution branch: `module-2-solution`

### 2.1 — The data layer: Postgres, ORMs, migrations and seeds

#### 🟢 Beginner exercise

Create Beacon's schema for `organization`, `user`, `membership`, `monitor` and `check_result` with the ORM or query builder of your choice, generate the first migration, and write an idempotent seed script that creates one org, two users (owner and member) and five monitors with a day of fake check results.

**Done when:**

- A fresh clone plus one command (`npm run db:reset` or equivalent) produces a working, seeded database.
- Every tenant-owned table has `organization_id`, `created_at` and `updated_at`, with foreign keys.
- Running the seed twice does not create duplicates.

#### 🟡 Intermediate exercise

Build the dashboard query "all monitors in my org with their latest check" and make it fast. Seed 500 monitors with 1,000 checks each, log the queries, fix any N+1, and add the index that makes `EXPLAIN ANALYZE` show an index scan.

```sql
SELECT DISTINCT ON (m.id) m.id, m.url, c.status_code, c.checked_at
FROM monitor m
LEFT JOIN check_result c ON c.monitor_id = m.id
WHERE m.organization_id = $1
ORDER BY m.id, c.checked_at DESC;
```

**Done when:**

- The page issues a constant number of queries regardless of monitor count.
- `EXPLAIN ANALYZE` shows no sequential scan on `check_result`.
- The page loads in under 200 ms locally with the large seed.

#### 🔴 Advanced exercise

Rename `monitor.url` to `monitor.target` with zero downtime using expand/contract across at least three separate migrations and deploys. Then set up PITR on your managed provider (or pgBackRest locally), delete all monitors on purpose, and restore to the minute before.

**Done when:**

- A load script hitting the API during every step sees zero errors.
- The backfill runs in batches with a `lock_timeout` set.
- You have a written restore runbook with the measured recovery time.

### 2.2 — File uploads and object storage

#### 🟢 Beginner exercise

Let org admins upload a status page logo. Create a `file` table, an endpoint that returns a presigned PUT URL for `orgs/{orgId}/logos/{fileId}`, and a "complete" endpoint that marks the row ready. Run SeaweedFS, Garage or a free-tier R2 bucket as your storage.

**Done when:**

- The file bytes never pass through your app server.
- Only admins of the org can request a signed URL for that org.
- Uploading a 10 MB file or a `.exe` is rejected before a URL is issued.

#### 🟡 Intermediate exercise

Add incident screenshots, private to org members. Downloads go through an endpoint that checks membership and redirects to a 5-minute presigned GET. After upload, sniff the real content type from the bytes and reject mismatches, and generate a 400 px thumbnail in a background job with `sharp`.

**Done when:**

- A logged-in user from another org gets 404 for the download endpoint, even with a valid file id.
- A text file renamed to `.png` is rejected after upload and its object deleted.
- Thumbnails are generated asynchronously and the UI shows a processing state.

#### 🔴 Advanced exercise

Implement organization offboarding for files and add hygiene rules. Write a job that deletes every object under an org's prefix in batches, plus lifecycle rules for `exports/` (7 days) and incomplete multipart uploads (1 day). Add a nightly reconciliation job that finds orphaned `pending` rows and objects with no row.

**Done when:**

- Deleting a test org removes all its objects, verified by listing the prefix.
- Lifecycle rules are defined in code (Terraform, OpenTofu or a script), not clicked in a console.
- The reconciliation job reports and cleans orphans in both directions.

### 2.3 — Search: from `LIKE '%x%'` to a search engine

#### 🟢 Beginner exercise

Add monitor search to Beacon's dashboard using `pg_trgm`. Index `name` and `url`, rank by similarity, and always filter by the current organization.

**Done when:**

- "chekout" finds a monitor named "checkout-api".
- `EXPLAIN ANALYZE` shows the trigram index in use on a seed of 50,000 monitors.
- A test proves a user never receives another org's monitors, even for identical names.

#### 🟡 Intermediate exercise

Add full-text search over incident updates with a generated `tsvector` column, `websearch_to_tsquery`, ranking and highlighted snippets, then build a cmd-K palette that queries monitors, incidents and settings pages in one call.

**Done when:**

- `"certificate expired" -staging` behaves like a web search query.
- Results show a highlighted snippet and the object type.
- The palette is keyboard-only usable and responds in under 150 ms locally.

#### 🔴 Advanced exercise

Move search to Meilisearch or Typesense with an outbox-driven indexer and a nightly reindex into a fresh index swapped in atomically. The browser queries the engine directly using a tenant token or scoped key minted by your API with a mandatory `organization_id` filter.

**Done when:**

- Killing the search engine for five minutes loses no updates; the worker catches up.
- Tampering with the filter in the browser still returns only the user's org.
- Deleting an incident removes it from search within a minute.

### 2.4 — Multi-tenancy deep dive: isolation, noisy neighbours, residency

#### 🟢 Beginner exercise

Audit every Beacon endpoint for tenant scoping. Introduce a scoped data-access helper so handlers can only load tenant data through `forOrg(orgId)`, and write a cross-tenant test that runs against every route.

**Done when:**

- No handler queries a tenant table without going through the scoped helper (enforced by a lint rule or code review checklist).
- An automated test logs in as org B and gets 404 for every org A resource.
- Cache keys and job payloads include `org_id`.

#### 🟡 Intermediate exercise

Enable Postgres RLS on `monitor`, `incident` and `incident_update` as defence in depth. The app connects as a non-owner role and sets `app.current_org` per transaction; jobs set it too.

```ts
export async function withOrg<T>(orgId: string, fn: (tx: Tx) => Promise<T>) {
  return db.transaction(async (tx) => {
    await tx.execute(sql`select set_config('app.current_org', ${orgId}, true)`);
    return fn(tx);
  });
}
```

**Done when:**

- Deleting the `WHERE organization_id` from a query in a test still returns only the current org's rows.
- Inserting a monitor with another org's id fails with an RLS violation.
- It works through PgBouncer or your provider's pooler in transaction mode.

#### 🔴 Advanced exercise

Add EU data residency and fair scheduling. Create a tenant directory table (org → region), run two local "cells" with separate databases and buckets, and route requests by the org's region. Then cap each org's concurrent check jobs so a 3,000-monitor org cannot delay others.

**Done when:**

- An EU org's rows, files and search documents exist only in the EU cell.
- The global directory stores no personal data beyond ids and region.
- A load test with one huge org keeps other orgs' checks within their scheduled interval.

## Module 3 — Money

Solution branch: `module-3-solution`

### 3.1 — Subscriptions and payments: checkout, webhooks, the customer portal

#### 🟢 Beginner exercise

Add Stripe Checkout and the Customer Portal to Beacon's billing settings page. Create the Pro Product with a monthly Price in test mode. "Upgrade" creates a Checkout Session with the organization ID in `client_reference_id` or `metadata`. "Manage billing" opens a Portal session for the org's Customer.

**Done when:**
- An org owner can upgrade with the test card `4242 4242 4242 4242` and land back on Beacon.
- The success page says "confirming…" and doesn't change the plan itself.
- "Manage billing" opens the Portal, where the owner can update the card and cancel.
- Non-owners don't see the billing buttons (reuse your 1.3 permission check).

#### 🟡 Intermediate exercise

Write the webhook handler: raw-body signature verification, a `stripe_events` table with a unique `id` for dedupe, and a `syncCustomerFromStripe(customerId)` function that fetches the customer's subscriptions and upserts a `subscriptions` row (status, price ID, current period end, cancel-at-period-end). Use `stripe listen --forward-to localhost:3000/api/stripe/webhook` locally.

**Done when:**
- Sending the same event twice (`stripe events resend`) changes nothing the second time.
- A request with a tampered body gets `400`, and a valid one gets `200`.
- Cancelling in the Portal sets `cancel_at_period_end = true` in your table within seconds.
- Deleting your `subscriptions` row and replaying any event restores it correctly.

#### 🔴 Advanced exercise

Implement the full lifecycle with a Stripe **test clock**: a 14-day trial with a card, conversion, a failed renewal (use a test card that declines), a 7-day grace period with a banner, then automatic downgrade to Free. Add a nightly reconciliation job that lists all Stripe subscriptions and reports any mismatch with your table.

**Done when:**
- Advancing the test clock drives Beacon through `trialing → active → past_due → canceled` with no manual steps.
- The dashboard banner appears during `past_due` and disappears after a successful card update.
- Manually corrupting a row (setting a canceled org to `active`) is reported by the reconciliation job the next time it runs.
- An integration test covers the whole path.

### 3.2 — Plans, limits and entitlements: turning pricing into code

#### 🟢 Beginner exercise

Create `lib/plans.ts` with Free, Pro and Business entitlements and a `getEntitlements(org)` function. Replace every `plan === "..."` check in Beacon with an entitlement check. Enforce `maxMonitors` and `minIntervalSec` on monitor create *and* update.

**Done when:**
- `grep -rn "plan ===" src/` returns nothing outside `lib/plans.ts`.
- A Free org gets a structured `limit_exceeded` error when creating its sixth monitor via the API, not only via the UI.
- The monitor form disables intervals below the org's minimum and shows an upgrade prompt.

#### 🟡 Intermediate exercise

Implement downgrade handling with the **freeze** policy. When an org's entitlements shrink (webhook sync or admin change), pause the newest monitors beyond the limit with `pausedReason = "plan_limit"`, clamp intervals up to the new minimum, and email the owner. Add a UI where the owner picks which monitors stay active.

**Done when:**
- Downgrading Pro to Free with 12 monitors leaves 5 active, 7 paused, and no data deleted.
- Upgrading again un-pauses the plan-paused monitors (but not manually paused ones).
- The scheduler never runs a paused monitor and never runs checks faster than the org's current minimum.
- The owner receives exactly one email per downgrade.

#### 🔴 Advanced exercise

Add per-org **overrides** and **add-ons**. Overrides (`maxMonitors`, `minIntervalSec`, `smsCreditsPerMonth`) are editable in the admin panel with a reason and an optional expiry, and they're audit-logged. Add a "+25 monitors" add-on as a second Stripe subscription item with quantity. Make enforcement race-safe for monitor creation.

**Done when:**
- Entitlements are computed as plan + add-ons × quantity + unexpired overrides, with unit tests for each combination.
- Expired overrides stop applying without a deploy.
- Firing 20 concurrent create requests at an org with one free slot creates exactly one monitor.
- Every override change appears in the audit log with actor and reason.

### 3.3 — Usage-based billing and metering

#### 🟢 Beginner exercise

Create a `usage_events` table (`idempotency_key` unique, `org_id`, `meter`, `quantity`, `occurred_at`) and record one event per SMS in the SMS worker, keyed by the Twilio message SID. Show "SMS used this period" on the billing page, computed from the org's current billing period in the subscriptions table.

**Done when:**
- Running the SMS job twice for the same message creates one usage row.
- The billing page shows the correct count for the current period, not the calendar month.
- Events store `occurred_at` from the send time, not the time of insertion.

#### 🟡 Intermediate exercise

Bill overage through Stripe Billing meters. Create a meter `sms_segments` (sum) and a metered Price for $0.05 per unit above an included 100. The simplest approach: report only units beyond the included amount, or use a graduated price with a free first tier. Report each usage event to Stripe with your idempotency key as the identifier, from a background job with retries. Add 80% and 100% alert emails.

**Done when:**
- A test-clock subscription that sends 130 SMS gets an invoice with a $1.50 overage line.
- Replaying the reporting job doesn't change the invoice.
- Each alert email is sent at most once per org per period.
- Beacon's count and Stripe's meter summary match for the test org.

#### 🔴 Advanced exercise

Replace the counter with a **credit ledger**: monthly grants (reset each period, expiring), purchasable packs (one-time Checkout, expiring after 12 months), and debits that consume monthly credits first. Add a customer-configurable overage cap enforced atomically in the SMS sender, with fallback to email and in-app when the cap is hit. Add a daily reconciliation job comparing Beacon usage, Stripe meter totals and Twilio's usage for each org.

**Done when:**
- The balance is always derivable from immutable grant and debit rows, with no mutable balance column as source of truth.
- Concurrent SMS sends never overdraw the balance or exceed the cap (tested with parallel jobs).
- When the cap is reached, SMS stops, the alert still arrives by email and in-app, and the owner is notified once.
- The reconciliation job flags an intentionally deleted usage row.

## Module 4 — Communication

Solution branch: `module-4-solution`

### 4.1 — Transactional email that actually arrives

#### 🟢 Beginner exercise

Set up Mailpit in Beacon's `docker-compose.yml` and a provider (Resend, Postmark or SES) for production. Create React Email (or MJML) templates for *verify email*, *invitation* and *incident opened*, and send them through a single `sendEmail()` function that picks SMTP-to-Mailpit in development and the provider in production.

**Done when:**
- Signing up locally shows the verify email in Mailpit's UI at `localhost:8025`.
- Every template has a plain-text part and renders in a preview.
- No code outside `sendEmail()` imports the provider SDK.

#### 🟡 Intermediate exercise

Authenticate `mail.beacon.app` (SPF, DKIM, DMARC with `p=none` and a report address), move all sending into a queued job with idempotency keys, and handle the provider's bounce and complaint webhooks with signature verification. Maintain a `email_suppressions` table checked before every send, and show a warning in the team-members UI for suppressed addresses.

**Done when:**
- An external checker (or the provider's dashboard) shows SPF, DKIM and DMARC passing and aligned.
- A simulated hard bounce (providers offer test addresses) adds a suppression row, and no further emails are attempted to that address.
- A provider outage (simulate with a bad API key) delays emails but doesn't fail user requests, and they send after recovery.

#### 🔴 Advanced exercise

Let Business orgs send status-page subscriber emails from their own domain. Build domain onboarding (create the identity via the provider's API, display DNS records, poll verification), send subscriber updates from a separate stream with RFC 8058 one-click unsubscribe headers, and fan out incident updates in throttled batches.

**Done when:**
- An org can add `status.acme.com`, see its DNS records, and gets a "verified" state once they propagate.
- Until verification, emails go out from Beacon's domain with the org's display name.
- Subscriber emails include `List-Unsubscribe` and `List-Unsubscribe-Post`, and one-click unsubscribing removes the subscriber without a login.
- A 10,000-subscriber fan-out completes within your provider's rate limits without delaying password-reset emails.

### 4.2 — Notifications: in-app, push, Slack, SMS — and preferences

#### 🟢 Beginner exercise

Build the in-app inbox: a `notifications` table, a `notify()` function called when an incident opens or resolves, a bell icon with an unread count, and "mark as read" / "mark all as read". Every org member with access to the monitor gets one notification per incident state change.

**Done when:**
- Opening an incident creates exactly one notification per eligible member, even if `notify()` is called twice (unique dedupe key).
- The unread count updates after marking as read.
- Members without access to the monitor (1.3) receive nothing.

#### 🟡 Intermediate exercise

Add email, Slack and SMS channels behind a channel-router with per-channel jobs, plus a preferences page (category × channel matrix, with required categories locked on). Implement anti-flapping: incidents open after 3 consecutive failures, and a monitor that changes state more than 4 times in an hour sends one "flapping" notification and suppresses the rest. Add a per-user SMS throttle of 5 per hour, with email fallback.

**Done when:**
- A simulated flapping monitor (alternating up/down every 30s for an hour) produces at most a handful of notifications per channel.
- A user who disabled email for "incident resolved" gets no resolved emails but still gets in-app ones.
- The sixth SMS within an hour is replaced by an email saying how many alerts were held back.
- Every delivery attempt is recorded with channel, status and provider message ID.

#### 🔴 Advanced exercise

Implement escalation policies per org: step 1 (push + Slack to primary on-call), step 2 after 5 minutes (SMS), step 3 after 10 more minutes (secondary on-call, SMS + voice). Acknowledgement (from the app, a Slack button, or an SMS reply) cancels pending steps. Add a daily digest for non-critical categories and an incident timeline showing every delivery.

**Done when:**
- An unacknowledged incident escalates on schedule. Acknowledging at any step cancels all later steps, with no duplicate pages.
- Acknowledging from Slack's button updates the incident within seconds.
- Non-critical notifications for a user within the digest window arrive as a single email.
- The incident timeline shows who was notified, how, when, and whether it was delivered.

### 4.3 — Real-time and collaboration: WebSockets to CRDTs

#### 🟢 Beginner exercise

Replace dashboard polling with SSE. The check worker publishes `{type: "monitor.status", monitorId, status}` to Redis channel `org:{orgId}`, an authorized SSE endpoint forwards it, and the dashboard updates the monitor tile in place and refetches the full list on reconnect.

**Done when:**
- A monitor going down turns red on an open dashboard within about a second, without polling.
- A user who isn't a member of the org gets `403` from the SSE endpoint.
- Restarting the server makes dashboards reconnect automatically and resync.

#### 🟡 Intermediate exercise

Run two app instances behind a load balancer and prove fan-out works across them. Add presence to the incident page ("Alice and Bob are viewing") with Redis TTL heartbeats, and client reconnection with exponential backoff and jitter. Disconnect a user's streams within a minute when they're removed from the org.

**Done when:**
- An event published on instance A reaches clients connected to instance B.
- Presence updates within a few seconds of a tab opening or closing, and stale entries expire.
- Killing an instance spreads its clients' reconnects over several seconds instead of one spike.
- A removed member's open dashboard stops receiving events.

#### 🔴 Advanced exercise

Make the postmortem editor collaborative with Yjs and Hocuspocus: authenticate connections with a short-lived token, authorize per incident in `onAuthenticate`, persist merged documents to Postgres (debounced), and show live cursors via awareness. Separately, add optimistic locking (`version` column, `409` on conflict) to monitor settings.

**Done when:**
- Two browsers editing the same postmortem, including while one is briefly offline, converge to the same text with no lost edits.
- Only members of the incident's org can connect to its document.
- Restarting the Hocuspocus server loses no edits made more than a few seconds earlier.
- Saving monitor settings from two stale tabs gives the second a clear conflict message instead of silently overwriting.

## Module 5 — Background Work & Integrations

Solution branch: `module-5-solution`

### 5.1 — Background jobs, queues and scheduled tasks

#### 🟢 Beginner exercise

Move incident notifications out of the request. When a monitor fails, the checker writes the incident and enqueues a `notify-incident` job; a separate worker process sends the emails. Configure 8 attempts with exponential backoff and a dead-letter destination.

**Done when:**
- The request/checker path returns without making any email, Slack or SMS call.
- Killing the email provider (point it at a bad host) causes retries visible in the queue dashboard, and the job succeeds once you restore it.
- A job that fails every attempt ends up in the DLQ with its error, not lost.

#### 🟡 Intermediate exercise

Make notifications exactly-once *in effect*. Add a `notification_deliveries` table with a unique key per `(incident, recipient, channel)`, and move enqueuing into the same transaction as the incident (Postgres queue) or through an outbox table (Redis queue).

**Done when:**
- Running the same job twice by hand sends each subscriber exactly one email.
- Crashing the process between "incident committed" and "job enqueued" still results in notifications (the relay or transactional enqueue catches it).
- A test proves the handler is a no-op for an incident that no longer exists.

#### 🔴 Advanced exercise

Build the sharded check scheduler. Store `next_run_at` and a stable phase offset per monitor, run two scheduler processes that each own half the shards, and claim due monitors with `SKIP LOCKED` in batches. Add a per-org concurrency cap so one org cannot use more than 5% of check workers.

```sql
-- claim a batch of due monitors in my shards
UPDATE monitors m SET next_run_at = m.next_run_at + m.interval_seconds * interval '1 second'
WHERE m.id IN (
  SELECT id FROM monitors
  WHERE shard = ANY($1) AND next_run_at <= now() AND paused = false
  ORDER BY next_run_at
  FOR UPDATE SKIP LOCKED
  LIMIT 5000
)
RETURNING m.id, m.org_id, m.region;
```

**Done when:**
- With 100,000 seeded monitors, the per-second check rate is flat (no spike at `:00`).
- Killing one scheduler causes the other to take over its shards within a minute, with no monitor checked twice in the same interval.
- An org with 20,000 monitors cannot delay another org's checks by more than one interval.

### 5.2 — The public API: API keys, versioning and rate limits

#### 🟢 Beginner exercise

Ship `GET /v1/monitors` and `POST /v1/monitors` authenticated with org-owned API keys. Keys are prefixed `bk_live_`, stored as SHA-256 hashes, shown once in a settings page, and revocable.

**Done when:**
- The `api_keys` table contains no plaintext keys.
- A revoked key gets a 401 within one request.
- Keys from org A can never read org B's monitors (you have a test for it).
- The list endpoint is cursor-paginated with a maximum `limit`.

#### 🟡 Intermediate exercise

Go OpenAPI-first. Define the monitor schemas once, generate the OpenAPI document from them, serve Scalar docs at `/docs/api`, return RFC 9457 problem details for every error, and support `Idempotency-Key` on `POST`.

**Done when:**
- A CI step fails if the generated spec changes without being committed.
- Every 4xx/5xx has `application/problem+json` with `type`, `title` and `status`.
- Sending the same `POST` twice with the same key creates one monitor and returns the same body twice.

#### 🔴 Advanced exercise

Add plan-aware rate limiting and date-based versioning. Rate limit with a token bucket per org sized by plan, with separate limits for `POST /v1/monitors/{id}/check`. Add a `Beacon-Version` header; pin each org to the version current at its first call; write one version-change transformer (e.g. renaming `url` to `target`) that downgrades responses for older pins.

**Done when:**
- Exceeding the limit returns 429 with `Retry-After` and remaining-quota headers on every response.
- A Business org gets a higher limit than a Pro org without code changes, only plan config.
- An org pinned to the old version still sees `url`; a new org sees `target`; the handler only knows `target`.

### 5.3 — Outbound webhooks and third-party integrations

#### 🟢 Beginner exercise

Add webhook endpoints to Beacon's settings. Orgs register a URL, choose event types, and receive a `whsec_` secret once. On `incident.opened` and `incident.resolved`, enqueue one delivery job per matching endpoint, signed per Standard Webhooks, with a 10-second timeout and retries.

**Done when:**
- A receiver using the official Standard Webhooks library for its language verifies your signatures.
- An endpoint returning 500 is retried with growing delays, and the attempts are stored.
- A slow endpoint does not delay any other endpoint's deliveries.

#### 🟡 Intermediate exercise

Build the customer-facing webhook log and SSRF protection. Show every message and attempt per endpoint, with resend and "replay failed since…" buttons. Route all webhook *and* monitor traffic through a guard that resolves DNS, rejects private/loopback/link-local/CGNAT addresses (v4 and v6), pins the resolved IP, and refuses redirects for webhooks.

**Done when:**
- Registering `http://127.0.0.1`, `http://169.254.169.254`, `http://[::1]` or a hostname resolving to `10.x` fails, for both webhooks and monitors.
- A customer can replay yesterday's failed messages from the UI without support.
- Endpoints failing continuously for 5 days are disabled and the org's admins are emailed.

#### 🔴 Advanced exercise

Ship the Slack integration. "Add to Slack" runs the OAuth v2 flow with a signed `state`, stores the bot token encrypted per org, posts incidents to a chosen channel, and handles the "Acknowledge" button by verifying Slack's request signature and updating the incident. Handle uninstall and revoked tokens gracefully.

**Done when:**
- Tokens are encrypted at rest and never logged.
- Clicking "Acknowledge" in Slack updates the incident and the message within seconds; a request with a bad signature is rejected.
- Revoking the app in Slack marks the integration "needs reconnect" and stops delivery attempts, with an email to admins.

### 5.4 — Workflow engines and durable execution

#### 🟢 Beginner exercise

Pick one engine (Inngest or Trigger.dev locally is quickest) and move the "incident opened" notification fan-out from lesson 5.1 into a workflow with three named steps: load incident, notify channels, record deliveries. Kill the worker between steps and watch it resume.

**Done when:**
- The engine's dashboard shows each run with per-step inputs, outputs and timings.
- Killing the worker after step 2 does not re-send notifications when it restarts.
- A failing step retries on its own without re-running earlier steps.

#### 🟡 Intermediate exercise

Implement escalation policies as data plus one durable workflow. Store policies (ordered tiers of recipients, channels and wait durations) per org; the workflow snapshots the policy, notifies each tier and waits for `incident/acknowledged` *or* `incident/resolved`, whichever comes first.

**Done when:**
- Acknowledging in the dashboard or Slack stops the escalation within seconds.
- Resolving the incident before any ack cancels the remaining tiers.
- Editing the policy mid-incident does not affect the escalation already running, but applies to the next incident.
- SMS sends use an idempotency key derived from run ID and tier, so a retried step never double-pages.

#### 🔴 Advanced exercise

Write the custom-domain connection as a saga with compensations, and handle workflow versioning. Steps: create domain record, register hostname with the edge provider, wait up to 72 hours for DNS verification, issue the certificate, activate. On permanent failure or timeout, compensate in reverse and email the customer. Then change the workflow (add a "notify Slack on success" step) while old runs are waiting, using your engine's versioning mechanism.

**Done when:**
- A domain that never verifies ends with no leftover hostname or record, and an email to the customer.
- A failure at "issue certificate" removes the hostname and domain record.
- Runs started before the deploy complete on the old path; runs started after include the new step; no run fails with a replay/determinism error.

## Module 6 — Product & Growth

Solution branch: `module-6-solution`

### 6.1 — The app shell: marketing site, onboarding, dashboard and settings

#### 🟢 Beginner exercise

Build Beacon's authenticated layout with shadcn/ui: a sidebar (Monitors, Incidents, Status pages, Settings), an org switcher that changes the `/[org]/...` URL segment, and an empty state on the Monitors page with a single "Add your first monitor" button that opens a form validated with a shared zod schema.

**Done when:**
- Switching org changes the URL and reloading the page keeps you in the same org.
- Submitting an invalid URL shows an inline error without a network request, *and* posting the same bad payload with `curl` is rejected by the server with the same message.
- The whole flow works with keyboard only (Tab, Enter, Escape closes the dialog).

#### 🟡 Intermediate exercise

Split settings into Account (`/settings/account`), Organization (`/[org]/settings/general`, `/members`), Billing and Developer (API keys). Add an onboarding checklist driven by milestones stored on the org: first monitor, first alert channel, status page published. The checklist hides itself once all three are done.

**Done when:**
- A Member role gets a 403 from the server when calling the org-rename endpoint directly, not just a hidden button.
- A second admin who joins after onboarding is done never sees the checklist.
- Milestone timestamps are stored, so you can later compute "time to activation" (6.2).

#### 🔴 Advanced exercise

Ship custom domains for status pages. Add a `custom_domains` table (`org_id`, `hostname`, `verified_at`, `last_checked_at`), a settings page that shows the CNAME to create, a verification job (5.1) that re-checks DNS daily, and a Caddy config with `on_demand_tls` whose `ask` endpoint only returns 200 for verified hostnames.

**Done when:**
- `status.yourtestdomain.com` serves the right org's status page over valid HTTPS with no manual cert step.
- Pointing an unregistered domain at the server does **not** trigger a certificate request (check Caddy's logs).
- Deleting the DNS record makes the domain unverified within a day, and it stops being served.

### 6.2 — Analytics: product, web and the event pipeline

#### 🟢 Beginner exercise

Write Beacon's tracking plan: 8–12 events in object_action form, each with properties and a one-line "why". Then add cookieless web analytics (Plausible or Umami) to the marketing site only.

**Done when:**
- Every event in the plan maps to a question you'd actually ask (activation, retention, upgrade).
- No event property contains an email, name, or monitored URL.
- Visits to the marketing site appear in the dashboard with no cookie set (check DevTools → Application).

#### 🟡 Intermediate exercise

Integrate PostHog (cloud or self-hosted). Call `identify` on login and `group("organization", orgId, { plan })` on every page load in the app. Send `monitor_created` and `subscription_upgraded` **server-side** after the database write or Stripe webhook succeeds. Build an activation funnel: `org_created` → `monitor_created` → first `monitor_check_completed` within 24h.

**Done when:**
- The funnel can be broken down by organization plan, not just by user.
- Blocking the PostHog domain in the browser doesn't stop `monitor_created` from being recorded.
- A typed `track` helper rejects event names not in your plan at compile time.

#### 🔴 Advanced exercise

Build customer-facing uptime analytics. Write every check result to a ClickHouse table (`org_id`, `monitor_id`, `ts`, `status`, `latency_ms`) using batched inserts from the check worker (5.1). Expose a server endpoint returning 90-day daily uptime % and p95 latency for one monitor, and render it with Tremor on the status page.

**Done when:**
- The endpoint takes `org_id` from the session or status-page lookup, never from a query parameter, and a test proves org A can't read org B's data.
- Inserts are batched (e.g. every second or every 1,000 rows), not one row per check.
- A retention policy (ClickHouse TTL) drops data past the plan's history limit.

### 6.3 — Feature flags and experiments

#### 🟢 Beginner exercise

Implement a minimal in-house flag: a `feature_flags` table (`key`, `enabled`, `rollout_percent`) and a `feature_flag_overrides` table (`key`, `org_id`, `enabled`). Write `isEnabled(key, orgId)` that checks overrides first, then hashes `key:orgId` into 0–99 against `rollout_percent`.

**Done when:**
- The same org always gets the same answer for the same flag (write a test over 1,000 calls).
- Raising the rollout from 10% to 30% keeps every org that was already on.
- An override for your internal org turns the flag on regardless of percentage.

#### 🟡 Intermediate exercise

Replace the in-house function with OpenFeature and a self-hosted Unleash (or Flagsmith) provider. Put the new scheduler behind `new-scheduler`, keyed by org ID, with local evaluation in the worker. Add `disable-sms-sending` as an ops kill switch that on-call can flip from the dashboard.

**Done when:**
- Stopping the flag service doesn't crash workers; they keep using the last known rules or the safe default.
- Flipping the kill switch stops SMS sends within your refresh interval, with no deploy.
- Every flag has an owner and an expiry noted, and there's a ticket to remove `new-scheduler`.

#### 🔴 Advanced exercise

Run a real experiment on onboarding with GrowthBook or PostHog: `onboarding-checklist-v2`, randomised by org, primary metric "activated within 24h" (from 6.2). Log an exposure event only when the org sees the checklist. Before launching, write down the minimum detectable effect and the required sample size.

**Done when:**
- The experiment doc states the metric, sample size and stopping rule *before* launch.
- A sample-ratio-mismatch check runs and passes.
- The result (win, loss or inconclusive) is recorded, the losing branch and the flag are deleted, and the audit log shows who changed the experiment and when.

## Module 7 — Operating the SaaS

Solution branch: `module-7-solution`

### 7.1 — The admin panel: support tools and impersonation

#### 🟢 Beginner exercise

Create a `staff_users` table separate from `users`, and an `/admin` area (or separate app) that only staff sessions can open. Build a customer search that finds an org by member email, org name, or Stripe customer id, and a read-only org page showing plan, trial end, monitor count vs. limit, members, and the last 10 incidents.

**Done when:**
- A customer account with any role gets 404 on every `/admin` route.
- Search finds an org from a partial email in under a second on seeded data.
- The org page shows usage vs. plan limit pulled from the same entitlements code the product uses.

#### 🟡 Intermediate exercise

Add two write actions: "Extend trial by N days" (support role, max 14) and "Comp plan" (billing role). Both must call your existing billing service functions, require a reason, and write an audit event.

**Done when:**
- Extending a trial updates Postgres *and* the Stripe subscription's trial end, and the monitor scheduler sees the new limit without a restart.
- A support-role staff member cannot see the "Comp plan" button, and a direct POST returns 403.
- Every action produces an audit event with staff id, org id, reason, before and after values.

#### 🔴 Advanced exercise

Implement read-only impersonation: a one-time signed token from the admin app, a 30-minute session flagged `impersonatorId` and `readOnly`, middleware that rejects mutating requests, a banner, and an org-level "Allow Beacon staff to view our account" setting that defaults to off for Business orgs.

```ts
// middleware in the customer app
export function guardImpersonation(req: Req, session: Session) {
  if (!session.impersonatorId) return;
  if (Date.now() > session.impersonationExpiresAt) throw new Unauthorized();
  const mutating = !["GET", "HEAD", "OPTIONS"].includes(req.method);
  if (mutating && session.readOnly) {
    throw new Forbidden("Read-only impersonation");
  }
  req.auditContext = {
    actor: `staff:${session.impersonatorId}`,
    onBehalfOf: `user:${session.userId}`,
  };
}
```

**Done when:**
- Any POST/PUT/PATCH/DELETE during read-only impersonation returns 403, including API routes.
- Sessions expire at 30 minutes even if active.
- Impersonating a Business org with consent off is refused and the refusal itself is audited.
- The customer's own audit log shows "Beacon support viewed your account" entries.

### 7.2 — Observability: logs, errors, metrics and traces

#### 🟢 Beginner exercise

Replace every `console.log` in Beacon's API and workers with pino. Add middleware that assigns a request id (reusing an incoming `x-request-id` if present), returns it in the response headers, and puts `requestId` and `orgId` on every log line. Install Sentry (or GlitchTip) on server and client with the release set to the git SHA.

**Done when:**
- Every log line is JSON and includes `requestId`; authenticated requests also include `orgId`.
- The `authorization` header and any `password` or `apiKey` field never appear in logs.
- A deliberately thrown error in the browser shows readable source file names in Sentry, tagged with the release.

#### 🟡 Intermediate exercise

Add OpenTelemetry to the API and the check workers, exporting to a local collector and a backend of your choice (SigNoz or Grafana + Tempo in Docker Compose). Propagate trace context through the BullMQ job payload. Emit two product metrics: `checks_executed_total` and `check_lag_seconds` (a histogram).

**Done when:**
- A single trace shows the API request that created a monitor, the enqueue, and the first check execution in the worker.
- A dashboard shows check lag p50/p95/p99 per region.
- Stopping one worker makes check lag visibly climb on the dashboard within a minute.

#### 🔴 Advanced exercise

Define an SLO: "99.9% of scheduled checks run within 15 seconds of schedule, over 30 days." Implement multi-window burn-rate alerting (page on fast burn, ticket on slow burn), write a runbook for the page, and add an independent external probe on a different provider. Add a "debug logging for one org for one hour" switch (a feature flag keyed by `orgId`).

**Done when:**
- A synthetic outage (pausing the scheduler for 10 minutes) pages; a 30-second blip doesn't.
- The page links to a runbook that a teammate who has never seen the system can follow.
- Enabling debug logging for one org increases log volume only for that org and turns itself off.

### 7.3 — Audit logs and activity feeds

#### 🟢 Beginner exercise

Create the `audit_events` table from the diagram (skip the hash columns) and a `recordAudit(tx, event)` helper. Call it inside the same transaction for: member invited, member role changed, monitor created, monitor paused, monitor deleted, API key created, API key revoked.

**Done when:**
- Each listed action creates exactly one event with actor, action, target, org, IP, user agent, and timestamp.
- A failure after the change but before commit leaves neither the change nor the event.
- Creating an API key logs only the key's prefix, never the full key.

#### 🟡 Intermediate exercise

Build the customer-facing audit log page under org settings, visible only to owners and admins, with filters for actor, action category, target and date range, a row detail view showing the before/after diff, and CSV export. Make retention a plan entitlement: Business 365 days, Pro 30 days, Free none.

**Done when:**
- A member (non-admin) gets 403 on the page and the API behind it.
- Filters combine and paginate correctly over 100,000 seeded events in under 500 ms (add the indexes you need).
- Staff impersonation actions show "Beacon support (on behalf of Ana)" rather than just "Ana".

#### 🔴 Advanced exercise

Make the log tamper-evident: revoke UPDATE and DELETE from the app role, add a per-org hash chain, a nightly verifier job, and an hourly anchor of the latest hash per org to object storage with an object-lock retention. Add a trigger-based safety net on `monitors` and `memberships` that records changes made outside the app (for example via `psql`).

```sql
REVOKE UPDATE, DELETE ON audit_events FROM beacon_app;

CREATE FUNCTION audit_fallback() RETURNS trigger AS $$
BEGIN
  IF current_setting('beacon.audited', true) IS DISTINCT FROM 'on' THEN
    INSERT INTO audit_fallback_events(table_name, op, row_id, old_row, new_row)
    VALUES (TG_TABLE_NAME, TG_OP, COALESCE(NEW.id, OLD.id), to_jsonb(OLD), to_jsonb(NEW));
  END IF;
  RETURN NULL;
END $$ LANGUAGE plpgsql;
-- the app runs SET LOCAL beacon.audited = 'on' inside audited transactions
```

**Done when:**
- Manually editing an audit row as a superuser is detected by the verifier on its next run.
- A `psql` update to a monitor produces a fallback event; an app update does not produce a duplicate.
- The verifier and anchor jobs are observable (7.2): a failed run alerts.

### 7.4 — Deployment, environments and self-hostable SaaS

#### 🟢 Beginner exercise

Write a multi-stage Dockerfile for Beacon's web app and a `docker-compose.yml` for local development (app, worker, Postgres, Redis). Move all configuration into environment variables validated at startup with a schema, and write a `.env.example` listing every variable.

**Done when:**
- `docker compose up` on a fresh clone gives a working Beacon with seed data.
- Removing `DATABASE_URL` makes the app exit at startup with a clear message naming the variable.
- The production image contains no dev dependencies and no `.env` files.

#### 🟡 Intermediate exercise

Build a CI/CD pipeline (GitHub Actions or similar): lint, typecheck, test, build one image tagged with the git SHA, deploy a preview environment per PR, then on merge run migrations, deploy to staging, run smoke tests, and promote the same image to production. Then perform the `url` → `target` rename using expand/migrate/contract across three deploys.

**Done when:**
- The image digest deployed to production is identical to the one tested in staging.
- A load test hitting the API and running checks during all three rename deploys sees zero 5xx errors and zero crashed workers.
- Every PR shows a working preview URL in its checks.

#### 🔴 Advanced exercise

Make Beacon self-hostable and recoverable. Ship a production `docker-compose.yml`, generated config docs, and an offline-verified license key that unlocks Business features (SSO, audit log). Then run a disaster-recovery drill: restore production's latest backup into a scratch environment with IaC, point the app at it, and measure RPO and RTO.

```ts
import { jwtVerify, importSPKI } from "jose";

const PUBLIC_KEY = await importSPKI(process.env.BEACON_LICENSE_PUBKEY!, "EdDSA");

export async function loadLicense(token?: string) {
  if (!token) return { plan: "free" as const };
  const { payload } = await jwtVerify(token, PUBLIC_KEY, { issuer: "beacon" });
  return {
    plan: payload.plan as "pro" | "business",
    customer: payload.sub!,
    maxMonitors: payload.maxMonitors as number,
    expiresAt: new Date(payload.exp! * 1000),
  };
}
```

**Done when:**
- A self-hoster can install from the docs alone, with no Stripe, email or analytics credentials, and the app works on the Free plan.
- A tampered or expired license falls back to Free with a clear admin warning, without crashing.
- The DR drill writes down measured RPO and RTO and at least one thing that went wrong, with a fix.

## Module 8 — Trust & the Frontier

Solution branch: `module-8-solution`

### 8.1 — Security and compliance: secrets, encryption, SOC 2, GDPR

#### 🟢 Beginner exercise

Remove every secret from Beacon's repo and config. Add gitleaks as a pre-commit hook and a CI step, move secrets to Infisical (or your platform's secret store), set security headers including a CSP on status pages, and publish `/.well-known/security.txt`.

**Done when:**
- `gitleaks detect` over the full history finds nothing, or every finding has been rotated.
- A test commit containing a fake AWS key is blocked locally and in CI.
- The status page response has CSP, HSTS and `nosniff` headers, and security.txt has `Contact` and `Expires`.

#### 🟡 Intermediate exercise

Build an SSRF-safe fetch for the check worker: resolve DNS, reject private/loopback/link-local/metadata ranges (IPv4 and IPv6), connect to the validated IP, cap redirects and re-validate each hop, and enforce timeouts and a response-size limit. Add trivy to CI for the worker image.

**Done when:**
- Monitors pointing at `http://169.254.169.254/`, `http://localhost:5432`, a hostname that resolves to `10.0.0.5`, and a public URL that redirects to `127.0.0.1` are all refused with a clear error.
- Tests cover IPv6 (`[::1]`) and decimal-encoded IPs (`http://2130706433/`).
- CI fails on critical CVEs in the worker image.

#### 🔴 Advanced exercise

Add per-tenant envelope encryption for Slack tokens and webhook secrets using a KMS (cloud KMS or OpenBao transit), plus a GDPR toolkit: an org-level data export (JSON of monitors, incidents, subscribers, audit log) and an org deletion job that removes data from Postgres, ClickHouse (6.2), object storage and search, then crypto-shreds the org's DEK.

**Done when:**
- A raw `SELECT` on the integrations table shows only ciphertext and a wrapped DEK.
- Rotating the KEK re-wraps DEKs without re-encrypting data or downtime.
- After deletion, a script proves no rows with that `org_id` remain in any store, and the deletion is recorded in the audit log.

### 8.2 — AI features as a SaaS component

#### 🟢 Beginner exercise

Build the AI incident summary. Add one server function that loads a single incident's tenant-scoped context, calls a model through the Vercel AI SDK with a zod schema for the output, and saves the result as a **draft** that a user can edit before publishing to the status page. Stream the text into the UI.

**Done when:**
- The output is validated against the schema. Invalid output shows a retry, not a crash.
- Nothing reaches the public status page without a human clicking Publish.
- The provider API key exists only on the server (check the client bundle).

#### 🟡 Intermediate exercise

Put a gateway in front of it: LiteLLM (or a thin in-house module) with a primary and fallback model, a timeout, per-org rate limits, and a `llm_usage` table recording `org_id`, feature, model, input/output tokens and cost for every call. Add Langfuse tracing and a promptfoo eval of 15 anonymised incidents that runs in CI, including one incident whose error body contains a prompt-injection attempt.

**Done when:**
- Pointing the primary model at a bad endpoint still produces summaries through the fallback.
- A monthly per-org usage query matches the provider's dashboard within a small margin.
- The eval fails if the summary claims "resolved" for an open incident, or if it follows the injected instruction.

#### 🔴 Advanced exercise

Ship "Ask Beacon": RAG over an org's incidents and postmortems using pgvector with `org_id` filtering (plus RLS), tool calls (`getIncident`, `listMonitors`) that run with the user's permissions, per-org monthly token budgets enforced before each call and reported to usage billing (3.3), and a read-only MCP server exposing the same tools with API-key auth.

**Done when:**
- A test with two orgs holding near-duplicate postmortems proves no cross-tenant retrieval, through chat *and* through MCP.
- An org over its budget gets a clear "limit reached" response without a model call, and usage appears on its invoice preview.
- Every AI answer and MCP tool call is recorded in the audit log (7.3) with user, org and tools used.

## Module 9 — Capstone

Solution branch: `module-9-solution` (architecture docs and ADRs)

### 9.1 — Assemble Beacon: reference architecture, build-vs-buy and a 90-day plan

#### 🟢 Beginner exercise

Draw Beacon's full architecture as a diagram in your repo — Mermaid in a Markdown
file is fine. Every box must name the lesson it came from and the concrete choice
you made (library, service or "built"). Then trace one request, "a Pro customer
adds a monitor", through the diagram, naming every component it touches.

**Done when:**

- The diagram shows all three rings and the tenant boundary.
- Every component names a concrete technology choice.
- The traced request mentions authentication, authorization, entitlement check,
  database write, audit log and job scheduling, in the right order.

#### 🟡 Intermediate exercise

Write five architecture decision records for Beacon's most consequential choices:
authentication, job queue, billing, webhooks and observability. Each ADR states
the context, the decision, two alternatives you rejected, the consequences, and
the signal that would make you revisit it ("revisit when we exceed 10,000
monitors per worker" is a signal; "revisit if needed" is not).

**Done when:**

- Five ADRs exist in `docs/adr/`, each one page or less.
- Each names a concrete revisit trigger.
- A teammate can read them and predict what you would choose for a sixth component.

#### 🔴 Advanced exercise

Run an enterprise readiness review of your Beacon. Pick the action "a customer's
admin removes an employee through their identity provider" and trace it across
SCIM, sessions, API keys, audit log, notifications, on-call schedules and billing
seats. Then do the same for "a customer requests a full data export and then
account deletion". Fix at least one seam you find, and present the review in 15
minutes to a peer acting as the customer's security team.

**Done when:**

- Both traces are written down with every component they touch and every gap found.
- At least one gap is fixed with a test that proves it.
- The presentation answers the five 🔴 questions above: isolation, identity
  lifecycle, evidence, residency and exit, and blast radius.
