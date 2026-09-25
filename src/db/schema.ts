import { sql } from 'drizzle-orm';
import { bigint, boolean, check, customType, doublePrecision, index, integer, jsonb, pgEnum, pgTable, primaryKey, text, timestamp, uniqueIndex, uuid, type AnyPgColumn } from 'drizzle-orm/pg-core';
import { FILE_KINDS } from '../core/files';
import { MILESTONES } from '../core/onboarding';
import { CATEGORY_IDS, CHANNELS } from '../core/notifications';
import { PLAN_IDS } from '../core/plans';
import { ROLES } from '../core/roles';
import { STAFF_ROLES } from '../core/staff';
import { users } from './auth-schema';

// Lesson 1.1: users, sessions and login methods. Better Auth defines their shape.
export * from './auth-schema';

/*
 * Lesson 1.2: the multi-tenant skeleton. The customer is an organization, not
 * a person. Users join organizations through memberships that carry a role,
 * and everything Beacon creates (monitors, check results, incidents) belongs
 * to an organization, never to a user.
 */

export const orgRole = pgEnum('org_role', ROLES);
// Lesson 3.2: the plan names live in src/core/plans.ts; the database only stores which one.
export const orgPlan = pgEnum('plan_id', PLAN_IDS);

/**
 * Lesson 2.1: every table Beacon owns gets `created_at` and `updated_at`
 * (timestamptz, UTC). Drizzle fills `updated_at` on every `.update()` through
 * `$onUpdate`. A hand-written SQL UPDATE bypasses it; a trigger would not,
 * at the cost of logic you cannot see in this file.
 */
const updatedAt = () =>
  timestamp('updated_at', { withTimezone: true })
    .notNull()
    .defaultNow()
    .$onUpdate(() => new Date());

export const organizations = pgTable(
  'organizations',
  {
  id: uuid('id').primaryKey().defaultRandom(),
  name: text('name').notNull(),
  // Goes in the URL: /acme/monitors and /status/acme. See src/core/slugs.ts.
  slug: text('slug').notNull().unique(),
  // The public status page at /status/[slug]. Only roles with "page.publish" may switch it (lesson 1.3).
  // Lesson 6.1: new orgs start UNpublished (an empty status page helps nobody);
  // publishing it is the last onboarding step. Migration 0021 kept existing orgs as they were.
  statusPagePublic: boolean('status_page_public').notNull().default(false),
  // Lesson 2.2: the status page logo, a row in `files` (the bytes are in object storage).
  logoFileId: uuid('logo_file_id').references((): AnyPgColumn => files.id, { onDelete: 'set null' }),
  // Lesson 3.1: the Stripe Customer belongs to the ORGANIZATION, not to the
  // person who clicked "Upgrade". When that person leaves, billing stays.
  stripeCustomerId: text('stripe_customer_id').unique(),
  // Lesson 3.2 (🟡): a snapshot of the plan the org's subscriptions entitle
  // it to. Only syncCustomerFromStripe() writes it (src/lib/billing/sync.ts);
  // getEntitlements() reads it, so a monitor create costs no Stripe call and
  // the API, the UI and the check runner all enforce the same limits.
  plan: orgPlan('plan').notNull().default('free'),
  // Lesson 7.1 (🟡): a plan given free of charge by Beacon staff ("Comp plan",
  // billing role, with a reason in the audit log). The plan snapshot above is
  // the better of this and the Stripe subscriptions (src/lib/billing/plan.ts),
  // until comp_plan_until; null = no end date.
  compPlan: orgPlan('comp_plan'),
  compPlanUntil: timestamp('comp_plan_until', { withTimezone: true }),
  // Lesson 4.2 (🟡): the org's Slack channel, as a Slack "incoming webhook" URL
  // (https://hooks.slack.com/services/…). It is a secret: anyone with it can
  // post to the channel. Lesson 8.1: stored envelope-encrypted ("enc:v1:…",
  // src/lib/secrets), so a database dump does not leak it.
  slackWebhookUrlEncrypted: text('slack_webhook_url_encrypted'),
  // Lesson 8.1: the Module 4–7 plaintext column (expand/contract, docs/deployment.md).
  // `npm run db:migrate` encrypts what is here into the column above and empties it;
  // nothing reads it any more, and a later migration drops it.
  legacySlackWebhookUrl: text('slack_webhook_url'),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: updatedAt(),
  },
  // Lesson 7.1 (🟢): the admin panel's customer search by (part of) the org name.
  (t) => [index('organizations_name_trgm_idx').using('gin', t.name.op('gin_trgm_ops'))],
);

export const memberships = pgTable(
  'memberships',
  {
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    userId: uuid('user_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
    role: orgRole('role').notNull(),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  // One role per person per org: the pair is the primary key.
  (t) => [primaryKey({ columns: [t.organizationId, t.userId] }), index('memberships_user_idx').on(t.userId)],
);

/**
 * Lesson 1.2 (🟡): a pending membership for someone who has not accepted yet.
 * The emailed link carries a random token; the table stores only its SHA-256
 * hash, like a password-reset token (lesson 1.1). Single use, 7-day expiry,
 * and bound to the invited email. Rules live in src/core/invitations.ts.
 */
export const invitations = pgTable(
  'invitations',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    email: text('email').notNull(), // stored lower-case
    role: orgRole('role').notNull(),
    tokenHash: text('token_hash').notNull().unique(),
    invitedBy: uuid('invited_by').references(() => users.id, { onDelete: 'set null' }),
    expiresAt: timestamp('expires_at', { withTimezone: true }).notNull(),
    // Last time the email went out (create or resend); the per-org rate limit counts these.
    sentAt: timestamp('sent_at', { withTimezone: true }).notNull().defaultNow(),
    acceptedAt: timestamp('accepted_at', { withTimezone: true }),
    acceptedBy: uuid('accepted_by').references(() => users.id, { onDelete: 'set null' }),
    revokedAt: timestamp('revoked_at', { withTimezone: true }),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [
    index('invitations_org_sent_idx').on(t.organizationId, t.sentAt),
    // At most one open invitation per email per org. Accepted and revoked ones don't count.
    uniqueIndex('invitations_one_open_per_email')
      .on(t.organizationId, t.email)
      .where(sql`${t.acceptedAt} is null and ${t.revokedAt} is null`),
  ],
);

/*
 * Beacon's core domain: monitors, the results of checking them, and the
 * incidents opened when they fail. This is the ~15% of Beacon that is
 * *Beacon*. Everything the course adds around it — users, organizations,
 * billing, jobs, webhooks, audit logs — is the generic 85%.
 *
 * Lesson 1.2, the tenant_id rule: every tenant-owned row carries
 * organization_id directly, even check_results and incidents, which could
 * reach it through their monitor. Every query can then filter by org without
 * a join, and a query that forgets to stands out in review.
 */

export const monitorPausedReason = pgEnum('paused_reason', ['manual', 'plan_limit']);

export const monitors = pgTable(
  'monitors',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    // Kept for history and for the "members edit their own monitors" rule
    // (lesson 1.3). Ownership is organizationId: when the author leaves, the monitor stays.
    createdBy: uuid('created_by').references(() => users.id, { onDelete: 'set null' }),
    name: text('name').notNull(),
    url: text('url').notNull(),
    // How often to check, in seconds. Lesson 3.2: never below the plan's
    // minimum (entitlement minIntervalSec), enforced in src/lib/monitors.ts.
    intervalSeconds: integer('interval_seconds').notNull().default(300),
    paused: boolean('paused').notNull().default(false),
    // Lesson 3.2 (🟡): WHY it is paused. 'manual': someone switched it off.
    // 'plan_limit': frozen by a downgrade; an upgrade switches it back on.
    pausedReason: monitorPausedReason('paused_reason'),
    // Lesson 4.2 (🟡): set when the monitor started flapping (too many state
    // changes in an hour); cleared once it has been stable for an hour. While
    // set, "opened"/"resolved" notifications for it are held back.
    flappingSince: timestamp('flapping_since', { withTimezone: true }),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [
    // Paused ⇔ there is a reason. The database keeps the two columns honest.
    check('monitors_paused_reason_check', sql`${t.paused} = (${t.pausedReason} is not null)`),
    index('monitors_org_idx').on(t.organizationId, t.createdAt),
    // Lesson 2.3 (🟢): trigram indexes (pg_trgm) for fuzzy search on name and
    // URL. They serve ILIKE '%…%' and the similarity operators, so "chekout"
    // finds "checkout-api" without reading every row. See src/lib/search.ts.
    index('monitors_name_trgm_idx').using('gin', t.name.op('gin_trgm_ops')),
    index('monitors_url_trgm_idx').using('gin', t.url.op('gin_trgm_ops')),
  ],
);

/**
 * Lesson 2.1: the one table without `updated_at`, on purpose. A check result
 * is a fact that never changes (append-only), `checked_at` is its creation
 * time, and at millions of rows a day every unused column costs disk.
 */
export const checkResults = pgTable(
  'check_results',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    monitorId: uuid('monitor_id').notNull().references(() => monitors.id, { onDelete: 'cascade' }),
    checkedAt: timestamp('checked_at', { withTimezone: true }).notNull().defaultNow(),
    ok: boolean('ok').notNull(),
    statusCode: integer('status_code'),
    latencyMs: integer('latency_ms'),
    error: text('error'),
    // Lesson 5.1: the scheduler's slot this result belongs to (null for results
    // from before Module 5). Unique per monitor: a check job that runs twice
    // (queues deliver at least once) stores one result, not two.
    scheduledAt: timestamp('scheduled_at', { withTimezone: true }),
  },
  (t) => [
    uniqueIndex('check_results_monitor_slot_idx').on(t.monitorId, t.scheduledAt).where(sql`${t.scheduledAt} is not null`),
    /*
     * Lesson 2.1 (🟡): the index behind the dashboard (listMonitors). Every
     * query here filters by org AND monitor (the tenant_id rule), then walks
     * by time: "latest check" reads the first entry, "last 24 hours" a range.
     * Column order matters: equality columns first, the range/sort column next.
     *
     * `ok` and `latency_ms` ride along at the end so Postgres can answer from
     * the index alone ("Index Only Scan", no table reads). With 500 monitors ×
     * 1,000 checks that took the dashboard query from ~1 s to ~0.1 s.
     * (Postgres can also carry them as `INCLUDE (ok, latency_ms)`; Drizzle
     * cannot express INCLUDE yet, and extra key columns work the same here.)
     *
     * It replaces the starter's (monitor_id, checked_at DESC), which could not
     * cover the organization_id filter. A trap it also had: Drizzle writes
     * `.desc()` as DESC NULLS LAST, which does not match `ORDER BY checked_at
     * DESC` (NULLS FIRST), so Postgres sorted instead of reading the index in
     * order. A plain ascending column avoids that: Postgres reads a B-tree
     * backwards just as well.
     *
     * It doubles as the index on the organization_id foreign key, which
     * Postgres does not create by itself.
     */
    index('check_results_org_monitor_time_idx').on(t.organizationId, t.monitorId, t.checkedAt, t.ok, t.latencyMs),
  ],
);

export const incidents = pgTable(
  'incidents',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    monitorId: uuid('monitor_id').notNull().references(() => monitors.id, { onDelete: 'cascade' }),
    openedAt: timestamp('opened_at', { withTimezone: true }).notNull().defaultNow(),
    resolvedAt: timestamp('resolved_at', { withTimezone: true }),
    // Lesson 5.4: someone took ownership ("I'm on it"). Stops the escalation.
    acknowledgedAt: timestamp('acknowledged_at', { withTimezone: true }),
    acknowledgedBy: uuid('acknowledged_by').references(() => users.id, { onDelete: 'set null' }),
    cause: text('cause').notNull(),
    // opened_at is when the outage began; created_at is when the row was written.
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [
    index('incidents_monitor_idx').on(t.monitorId, t.openedAt.desc()),
    // Lesson 2.1 (🟡): "is there an open incident for this monitor?" runs for
    // every monitor on the dashboard. A partial index holds only open incidents,
    // so it stays tiny however many resolved ones pile up.
    index('incidents_open_idx').on(t.monitorId).where(sql`${t.resolvedAt} is null`),
    // Lesson 5.2: GET /api/v1/incidents pages through one org's incidents, newest first (keyset on created_at, id).
    index('incidents_org_created_idx').on(t.organizationId, t.createdAt, t.id),
  ],
);

/** Postgres' full-text search document type (lesson 2.3). Drizzle has no built-in for it. */
const tsvector = customType<{ data: string }>({ dataType: () => 'tsvector' });

/**
 * Lesson 2.3 (🟡): what happened during an incident, in the team's words
 * ("Certificate expired on the load balancer, renewing"). The check runner
 * writes the first and last ones; people add the rest.
 *
 * `search` is a generated column: Postgres keeps the stemmed, searchable form
 * of `body` up to date on every insert and update, and the GIN index makes
 * `search @@ websearch_to_tsquery(…)` fast.
 */
export const incidentUpdates = pgTable(
  'incident_updates',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    incidentId: uuid('incident_id').notNull().references(() => incidents.id, { onDelete: 'cascade' }),
    authorId: uuid('author_id').references(() => users.id, { onDelete: 'set null' }), // null: written by Beacon
    body: text('body').notNull(),
    search: tsvector('search').generatedAlwaysAs(sql`to_tsvector('english', body)`),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [
    index('incident_updates_incident_idx').on(t.incidentId, t.createdAt),
    index('incident_updates_search_idx').using('gin', t.search),
  ],
);

/**
 * Lesson 2.2: metadata for every uploaded file. The bytes live in object
 * storage under `key`; this row is what access checks and the UI use.
 *
 *   pending     a URL was signed, the browser may be uploading
 *   processing  the bytes checked out; a background job is making a thumbnail
 *   ready       usable
 *   rejected    the bytes were not what was announced; the object was deleted
 */
export const fileKind = pgEnum('file_kind', FILE_KINDS);
export const fileStatus = pgEnum('file_status', ['pending', 'processing', 'ready', 'rejected']);

export const files = pgTable(
  'files',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    kind: fileKind('kind').notNull(),
    // Set for incident screenshots: the incident they belong to.
    incidentId: uuid('incident_id').references(() => incidents.id, { onDelete: 'cascade' }),
    // orgs/{orgId}/{folder}/{fileId}: generated by Beacon, never the user's file name.
    key: text('key').notNull().unique(),
    originalName: text('original_name').notNull(), // shown in the UI, never used as a path
    declaredType: text('declared_type').notNull(), // what the browser said before upload
    declaredSize: integer('declared_size').notNull(),
    contentType: text('content_type'), // what the bytes say (sniffed after upload)
    sizeBytes: integer('size_bytes'), // the real size, from the storage HEAD
    status: fileStatus('status').notNull().default('pending'),
    rejectionReason: text('rejection_reason'),
    thumbnailKey: text('thumbnail_key'),
    uploadedBy: uuid('uploaded_by').references(() => users.id, { onDelete: 'set null' }),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [index('files_org_created_idx').on(t.organizationId, t.createdAt), index('files_incident_idx').on(t.incidentId)],
);

/*
 * Module 3: money.
 */

/**
 * Lesson 3.1 (🟡): our COPY of each Stripe subscription. Stripe owns the truth
 * about money; webhooks keep this table in sync (src/lib/billing/sync.ts) and
 * nothing else writes it. The id is Stripe's (`sub_…`), so a re-sync upserts
 * the same row instead of adding one.
 */
export const subscriptions = pgTable(
  'subscriptions',
  {
    id: text('id').primaryKey(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    stripeCustomerId: text('stripe_customer_id').notNull(),
    // Stripe's status, stored as-is (trialing, active, past_due, canceled, …).
    // What each one grants is decided in one place: statusGrantsAccess() in src/core/plans.ts.
    status: text('status').notNull(),
    priceId: text('price_id'),
    currentPeriodStart: timestamp('current_period_start', { withTimezone: true }),
    currentPeriodEnd: timestamp('current_period_end', { withTimezone: true }),
    cancelAtPeriodEnd: boolean('cancel_at_period_end').notNull().default(false),
    // Lesson 7.1 (🟡): Stripe's trial_end, for a subscription in "trialing". Support's
    // "Extend trial" moves it in Stripe first; the sync copies it here.
    trialEnd: timestamp('trial_end', { withTimezone: true }),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [index('subscriptions_org_idx').on(t.organizationId)],
);

/**
 * Lesson 3.1 (🟡): every webhook event we have seen, by Stripe's event id.
 * Stripe delivers at least once, so the same event can arrive twice; the
 * primary key makes the second insert a no-op and the handler skips it.
 * `processed_at` stays null if handling failed, so Stripe's retry is handled
 * again instead of being skipped as a duplicate.
 * Not a tenant table: the org is only known after reading the event.
 */
export const stripeEvents = pgTable('stripe_events', {
  id: text('id').primaryKey(),
  type: text('type').notNull(),
  processedAt: timestamp('processed_at', { withTimezone: true }),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: updatedAt(),
});

/**
 * Lesson 3.3 (🟢): one row per billable fact (one SMS sent). Immutable apart
 * from `reported_at`, set once the event reached the billing provider.
 *
 *  - idempotency_key is UNIQUE and derived from the fact (`sms:{messageSid}`),
 *    so recording the same SMS twice creates one row;
 *  - occurred_at is when it happened (the send time), not when the row was
 *    written, and usage is summed by it, so a late event still lands in the
 *    right billing period.
 */
export const usageEvents = pgTable(
  'usage_events',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    idempotencyKey: text('idempotency_key').notNull().unique(),
    meter: text('meter').notNull(),
    quantity: integer('quantity').notNull(),
    occurredAt: timestamp('occurred_at', { withTimezone: true }).notNull(),
    reportedAt: timestamp('reported_at', { withTimezone: true }),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [
    // "SMS used this period": sum(quantity) for one org, one meter, a time range.
    index('usage_events_org_meter_time_idx').on(t.organizationId, t.meter, t.occurredAt),
    // The reporting job's queue: only the rows not yet sent to the provider.
    index('usage_events_unreported_idx').on(t.organizationId).where(sql`${t.reportedAt} is null`),
    check('usage_events_quantity_positive', sql`${t.quantity} > 0`),
  ],
);

/**
 * Lesson 3.3 (🟡): usage alerts already sent. The primary key is "this org,
 * this meter, this billing period, this threshold", so each alert email goes
 * out at most once per period however many SMS cross the line at once.
 */
export const usageAlerts = pgTable(
  'usage_alerts',
  {
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    meter: text('meter').notNull(),
    periodStart: timestamp('period_start', { withTimezone: true }).notNull(),
    threshold: integer('threshold').notNull(), // percent of the included amount: 80 or 100
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [primaryKey({ columns: [t.organizationId, t.meter, t.periodStart, t.threshold] })],
);

/*
 * Module 4: communication.
 */

/**
 * Lesson 4.1 (🟡): the email outbox. sendEmail() only inserts a row here (and
 * its job) and returns; the worker sends it (src/lib/email/index.ts).
 * A slow or broken provider therefore delays emails but never fails the
 * request that asked for one, and a failed send is retried with backoff.
 *
 *  - idempotency_key is UNIQUE: asking twice for the same email (a retried
 *    request, a double click) queues it once. The key also goes to the
 *    provider, which drops a duplicate send (Resend's Idempotency-Key).
 *  - the template name and its props are stored, not the HTML: the worker
 *    renders at send time.
 *  - lesson 5.1: each row has an `email.send` job in the queue (enqueued in
 *    the same transaction), and the QUEUE owns retries and backoff. The row
 *    records the outcome: status, attempts, last error, provider message id.
 *
 * Not a tenant table: verification and password-reset emails belong to no
 * organization. Notification emails have their own queue with the org on
 * every row (notification_deliveries, lesson 4.2).
 */
export const emailStatus = pgEnum('email_status', ['pending', 'sent', 'failed', 'suppressed']);

export const emailOutbox = pgTable(
  'email_outbox',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    idempotencyKey: text('idempotency_key').notNull().unique(),
    to: text('to').notNull(),
    template: text('template').notNull(),
    props: jsonb('props').notNull(),
    // Lesson 4.1: the one-click unsubscribe URL (RFC 8058) for subscribed or optional mail, if any.
    listUnsubscribe: text('list_unsubscribe'),
    status: emailStatus('status').notNull().default('pending'),
    attempts: integer('attempts').notNull().default(0),
    lastError: text('last_error'),
    providerMessageId: text('provider_message_id'),
    sentAt: timestamp('sent_at', { withTimezone: true }),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  // The worker's start-up check: "which emails are still pending?" (lesson 5.1). Only pending rows are in the index.
  (t) => [index('email_outbox_pending_idx').on(t.createdAt).where(sql`${t.status} = 'pending'`)],
);

/**
 * Lesson 4.1 (🟡): addresses we must not email. Filled by the provider's
 * bounce and complaint webhooks (src/lib/email/webhook.ts) and checked before
 * every send. Keyed by the lower-cased address, for every organization at
 * once: an address that does not exist does not exist for anyone.
 *
 *   hard_bounce  the mailbox does not exist: never send again
 *   complaint    they pressed "Report spam": only essential mail (password
 *                reset, verification) still goes out
 */
export const suppressionReason = pgEnum('suppression_reason', ['hard_bounce', 'complaint', 'manual']);

export const emailSuppressions = pgTable('email_suppressions', {
  email: text('email').primaryKey(),
  reason: suppressionReason('reason').notNull(),
  detail: text('detail'),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: updatedAt(),
});

/*
 * Lesson 4.2: notifications. One event (an incident opened) becomes one row
 * per recipient in `notifications` (the in-app inbox), and one row per
 * channel in `notification_deliveries` (the channel jobs AND the delivery
 * log). Rules: src/core/notifications.ts. Pipeline: src/lib/notifications.
 */
export const notificationCategory = pgEnum('notification_category', CATEGORY_IDS);
export const notificationChannel = pgEnum('notification_channel', CHANNELS);

export const notifications = pgTable(
  'notifications',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    userId: uuid('user_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
    category: notificationCategory('category').notNull(),
    // Lesson 4.2 (🟢): "<what happened>:<user>", UNIQUE. Calling notify() twice
    // for the same event inserts nothing the second time.
    dedupeKey: text('dedupe_key').notNull().unique(),
    title: text('title').notNull(),
    body: text('body').notNull(),
    url: text('url').notNull(), // a path inside Beacon, e.g. /acme/monitors/…
    monitorId: uuid('monitor_id').references(() => monitors.id, { onDelete: 'cascade' }),
    readAt: timestamp('read_at', { withTimezone: true }),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [
    index('notifications_inbox_idx').on(t.organizationId, t.userId, t.createdAt),
    // The bell's unread count, on every page: only unread rows are in this index.
    index('notifications_unread_idx').on(t.organizationId, t.userId).where(sql`${t.readAt} is null`),
  ],
);

/**
 * Lesson 4.2 (🟡): a person's choice for one category × channel, per org
 * (you may want SMS from your employer's org but not from a side project).
 * No row = the category's default.
 */
export const notificationPreferences = pgTable(
  'notification_preferences',
  {
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    userId: uuid('user_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
    category: notificationCategory('category').notNull(),
    channel: notificationChannel('channel').notNull(),
    enabled: boolean('enabled').notNull(),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [primaryKey({ columns: [t.organizationId, t.userId, t.category, t.channel] })],
);

/** Lesson 4.2 (🟡): the org's policy, set by owners and admins. `enabled = false` switches a channel off for everyone. */
export const orgNotificationPolicies = pgTable(
  'org_notification_policies',
  {
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    category: notificationCategory('category').notNull(),
    channel: notificationChannel('channel').notNull(),
    enabled: boolean('enabled').notNull(),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [primaryKey({ columns: [t.organizationId, t.category, t.channel] })],
);

/**
 * Lesson 4.2 (🟡): people who asked for status-page emails. Not users: they
 * subscribe on the public page, confirm from an email (double opt-in: a
 * stranger cannot sign you up), and unsubscribe with one click.
 */
export const statusPageSubscribers = pgTable(
  'status_page_subscribers',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    email: text('email').notNull(), // lower-case
    confirmedAt: timestamp('confirmed_at', { withTimezone: true }),
    confirmationSentAt: timestamp('confirmation_sent_at', { withTimezone: true }),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [uniqueIndex('status_page_subscribers_org_email').on(t.organizationId, t.email)],
);

export const deliveryStatus = pgEnum('delivery_status', ['pending', 'sent', 'failed', 'skipped', 'throttled', 'suppressed']);

/**
 * Lesson 4.2 (🟡): one row per message on one channel: the delivery log ("was
 * our on-call paged at 03:12, and did they get it?"): channel, status,
 * provider message id, error, time. Lesson 5.1: the sending is a
 * `notification.deliver` job in the queue, enqueued with the row; the unique
 * dedupe_key (event, recipient, channel) makes it exactly-once in effect.
 *
 * Recipients: a member (user_id, via a notification), a status-page
 * subscriber (subscriber_id), or the org's Slack channel (neither).
 */
export const notificationDeliveries = pgTable(
  'notification_deliveries',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    notificationId: uuid('notification_id').references(() => notifications.id, { onDelete: 'cascade' }),
    userId: uuid('user_id').references(() => users.id, { onDelete: 'cascade' }),
    subscriberId: uuid('subscriber_id').references(() => statusPageSubscribers.id, { onDelete: 'cascade' }),
    channel: notificationChannel('channel').notNull(),
    // UNIQUE: one delivery per event, recipient and channel, however often it is enqueued.
    dedupeKey: text('dedupe_key').notNull().unique(),
    recipient: text('recipient').notNull(), // email address, phone number, "slack" or the user id (in-app)
    // What to send: { title, body, url, email?: { template, props }, listUnsubscribe? }
    payload: jsonb('payload').notNull(),
    status: deliveryStatus('status').notNull().default('pending'),
    attempts: integer('attempts').notNull().default(0),
    providerMessageId: text('provider_message_id'),
    error: text('error'),
    sentAt: timestamp('sent_at', { withTimezone: true }),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [
    // Lesson 5.1: pending deliveries (each has a `notification.deliver` job; the worker's start-up check reads this).
    index('notification_deliveries_pending_idx').on(t.organizationId, t.createdAt).where(sql`${t.status} = 'pending'`),
    // The SMS throttle: "how many SMS did this person get in the last hour?"
    index('notification_deliveries_user_channel_idx').on(t.organizationId, t.userId, t.channel, t.sentAt),
    index('notification_deliveries_notification_idx').on(t.notificationId),
  ],
);

/**
 * Lesson 4.3 (🟡): who is looking at what, right now ("Alice and Bob are
 * viewing"). Each open tab heartbeats every 10 s; a row whose last_seen_at is
 * older than the TTL no longer counts, so a crashed tab disappears by itself.
 * The lesson keeps this in Redis with TTL keys; Beacon has no Redis yet, and
 * a small table with a timestamp does the same job (src/lib/presence.ts).
 */
export const presence = pgTable(
  'presence',
  {
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    topic: text('topic').notNull(), // "monitor:<id>"
    userId: uuid('user_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
    lastSeenAt: timestamp('last_seen_at', { withTimezone: true }).notNull().defaultNow(),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [primaryKey({ columns: [t.organizationId, t.topic, t.userId] })],
);

/*
 * Module 5: background work and integrations.
 */

/**
 * Lesson 5.2 (🟢): API keys. The key itself is never stored: only its SHA-256
 * hash (the lookup), and its first 12 and last 4 characters (for "bk_live_Ab3x…9f2Q"
 * in the settings list). Rules: src/core/api-keys.ts.
 *
 * Not under row-level security, like memberships: a request's key is how
 * Beacon LEARNS which org the request is for, so the lookup by hash happens
 * before any org is known. Managing keys (list, create, revoke) still names
 * the org in every query.
 */
export const apiKeys = pgTable(
  'api_keys',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    name: text('name').notNull(),
    keyHash: text('key_hash').notNull().unique(),
    keyStart: text('key_start').notNull(), // "bk_live_Ab3x"
    keyLast4: text('key_last4').notNull(),
    scopes: text('scopes').array().notNull(),
    // Kept for history; the key belongs to the org and outlives its creator.
    createdBy: uuid('created_by').references(() => users.id, { onDelete: 'set null' }),
    lastUsedAt: timestamp('last_used_at', { withTimezone: true }),
    revokedAt: timestamp('revoked_at', { withTimezone: true }),
    revokedBy: uuid('revoked_by').references(() => users.id, { onDelete: 'set null' }),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [index('api_keys_org_idx').on(t.organizationId, t.createdAt)],
);

/**
 * Lesson 5.2 (🟡): Idempotency-Key on POST. The first request with a key
 * stores its response here; a retry with the same key and the same body gets
 * that response back instead of creating a second monitor. `status_code` is
 * null while the first request is still running (a concurrent retry gets 409).
 * Kept 24 hours.
 */
export const apiIdempotencyKeys = pgTable(
  'api_idempotency_keys',
  {
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    key: text('key').notNull(),
    // What the key was used for: "POST /api/v1/monitors" and a hash of the body.
    requestMethod: text('request_method').notNull(),
    requestPath: text('request_path').notNull(),
    requestHash: text('request_hash').notNull(),
    statusCode: integer('status_code'),
    // The response text exactly as sent (not jsonb, which would reorder its keys): a retry gets the same bytes.
    responseBody: text('response_body'),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [primaryKey({ columns: [t.organizationId, t.key] })],
);

/**
 * Lesson 5.2: token buckets for rate limiting (src/core/rate-limit.ts), one row
 * per bucket ("org:<id>", "ip:<address>"). In Postgres rather than in memory so
 * every app instance counts against the same bucket. At high traffic this
 * moves to Redis, the lesson's default; the functions stay the same.
 */
export const rateLimitBuckets = pgTable('rate_limit_buckets', {
  key: text('key').primaryKey(),
  tokens: doublePrecision('tokens').notNull(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).notNull(),
});

/*
 * Lesson 5.3: outbound webhooks. The data model is Svix's, the reference the
 * lesson recommends reading: an EVENT happened once; it becomes one MESSAGE
 * per subscribed endpoint; each message has ATTEMPTS. src/lib/webhooks.ts.
 */

/**
 * An org's receiving URL, the event types it wants, and its signing secret.
 * The secret must be readable to sign, so it cannot be hashed like an API key:
 * it is shown once in the UI and never sent back. Lesson 8.1: stored
 * envelope-encrypted (src/lib/secrets): a raw SELECT shows ciphertext and a
 * wrapped data key, never the secret.
 */
export const webhookEndpoints = pgTable(
  'webhook_endpoints',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    url: text('url').notNull(),
    description: text('description'),
    eventTypes: text('event_types').array().notNull(),
    secretEncrypted: text('secret_encrypted'),
    // Lesson 8.1: the Module 5–7 plaintext column, emptied by `npm run db:migrate` (see
    // legacySlackWebhookUrl above). Nullable now; dropped by a later migration.
    legacySecret: text('secret'),
    enabled: boolean('enabled').notNull().default(true),
    disabledReason: text('disabled_reason'),
    // Lesson 5.3 (🟡): set on the first failed delivery, cleared by the next
    // success. Failing for 5 days in a row disables the endpoint.
    failingSince: timestamp('failing_since', { withTimezone: true }),
    createdBy: uuid('created_by').references(() => users.id, { onDelete: 'set null' }),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [index('webhook_endpoints_org_idx').on(t.organizationId, t.createdAt)],
);

/** Something happened ("incident.opened"), once, with its payload. Immutable. */
export const webhookEvents = pgTable(
  'webhook_events',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    type: text('type').notNull(),
    payload: jsonb('payload').notNull(),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => [index('webhook_events_org_created_idx').on(t.organizationId, t.createdAt)],
);

export const webhookMessageStatus = pgEnum('webhook_message_status', ['pending', 'delivered', 'failed']);

/**
 * One event for one endpoint: what `webhook-id` names (the same on every
 * retry, so receivers can drop duplicates). Unique per (endpoint, event).
 */
export const webhookMessages = pgTable(
  'webhook_messages',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    endpointId: uuid('endpoint_id').notNull().references(() => webhookEndpoints.id, { onDelete: 'cascade' }),
    eventId: uuid('event_id').notNull().references(() => webhookEvents.id, { onDelete: 'cascade' }),
    status: webhookMessageStatus('status').notNull().default('pending'),
    attempts: integer('attempts').notNull().default(0),
    lastAttemptAt: timestamp('last_attempt_at', { withTimezone: true }),
    deliveredAt: timestamp('delivered_at', { withTimezone: true }),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [
    uniqueIndex('webhook_messages_endpoint_event_idx').on(t.endpointId, t.eventId),
    // The delivery log: an endpoint's messages, newest first; "replay failed since…".
    index('webhook_messages_endpoint_created_idx').on(t.organizationId, t.endpointId, t.createdAt),
  ],
);

/** Every HTTP attempt of a message, for the customer-facing delivery log. */
export const webhookAttempts = pgTable(
  'webhook_attempts',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    messageId: uuid('message_id').notNull().references(() => webhookMessages.id, { onDelete: 'cascade' }),
    // 'automatic' (the queue, retries included) or 'manual' (Resend / Replay in the UI).
    trigger: text('trigger').notNull(),
    statusCode: integer('status_code'),
    durationMs: integer('duration_ms').notNull(),
    responseBody: text('response_body'), // the first 500 characters
    error: text('error'),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => [index('webhook_attempts_message_idx').on(t.messageId, t.createdAt)],
);

/*
 * Lesson 5.4: durable workflows, a small engine on top of the job queue
 * (src/lib/workflows/engine.ts). A RUN is one execution of a workflow; its
 * STEPS are the event history ("step notify-tier-0 returned …"), which is what
 * lets a run resume after a crash without doing a finished step again; SIGNALS
 * are the events a waiting run is woken by (an incident acknowledged).
 */
export const workflowRunStatus = pgEnum('workflow_run_status', ['running', 'waiting', 'completed', 'failed']);

export const workflowRuns = pgTable(
  'workflow_runs',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    workflow: text('workflow').notNull(), // "incident-escalation"
    // One run per business key: "incident-escalation:<incident id>". Starting it twice starts it once.
    key: text('key').notNull().unique(),
    // What the run is about, for "show this incident's workflows" (an incident id).
    subjectId: uuid('subject_id'),
    input: jsonb('input').notNull(),
    status: workflowRunStatus('status').notNull().default('running'),
    output: jsonb('output'),
    error: text('error'),
    wakeAt: timestamp('wake_at', { withTimezone: true }),
    completedAt: timestamp('completed_at', { withTimezone: true }),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [index('workflow_runs_subject_idx').on(t.organizationId, t.subjectId)],
);

export const workflowStepStatus = pgEnum('workflow_step_status', ['running', 'waiting', 'completed', 'failed']);

export const workflowSteps = pgTable(
  'workflow_steps',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    runId: uuid('run_id').notNull().references(() => workflowRuns.id, { onDelete: 'cascade' }),
    // Step names are the history's keys: rename one and runs in flight lose their place.
    name: text('name').notNull(),
    status: workflowStepStatus('status').notNull(),
    input: jsonb('input'),
    output: jsonb('output'),
    error: text('error'),
    attempts: integer('attempts').notNull().default(0),
    // A wait's deadline, fixed the first time the run reaches it (replays reuse it).
    wakeAt: timestamp('wake_at', { withTimezone: true }),
    startedAt: timestamp('started_at', { withTimezone: true }).notNull().defaultNow(),
    finishedAt: timestamp('finished_at', { withTimezone: true }),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [uniqueIndex('workflow_steps_run_name_idx').on(t.runId, t.name)],
);

export const workflowSignals = pgTable(
  'workflow_signals',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    runId: uuid('run_id').notNull().references(() => workflowRuns.id, { onDelete: 'cascade' }),
    name: text('name').notNull(), // "incident.acknowledged"
    payload: jsonb('payload'),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => [index('workflow_signals_run_idx').on(t.runId, t.createdAt)],
);

/**
 * Lesson 5.4 (🟡): the org's escalation policy, as data (src/core/escalation.ts):
 * ordered tiers of people, channels and a wait. One per org.
 */
export const escalationPolicies = pgTable('escalation_policies', {
  organizationId: uuid('organization_id').primaryKey().references(() => organizations.id, { onDelete: 'cascade' }),
  tiers: jsonb('tiers').notNull(),
  updatedBy: uuid('updated_by').references(() => users.id, { onDelete: 'set null' }),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: updatedAt(),
});

/*
 * Module 6 — Product & Growth.
 */

/**
 * Lesson 6.1 (🟡): onboarding milestones, stored on the org. One row per
 * milestone the org has reached, written once (the primary key plus
 * ON CONFLICT DO NOTHING): the first monitor, the first check result, the
 * first alert channel, the first invitation, the status page published.
 * `reached_at` is what "time to activation" is computed from (lesson 6.2).
 */
export const orgMilestones = pgTable(
  'org_milestones',
  {
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    milestone: text('milestone', { enum: MILESTONES }).notNull(),
    reachedAt: timestamp('reached_at', { withTimezone: true }).notNull().defaultNow(),
    // Who got there (null: Beacon itself, e.g. the first check). Deleted users leave the milestone.
    userId: uuid('user_id').references(() => users.id, { onDelete: 'set null' }),
  },
  (t) => [primaryKey({ columns: [t.organizationId, t.milestone] })],
);

/**
 * Lesson 6.2 (🟡): product analytics events, written by the SERVER after the
 * thing happened (usually in the same transaction), as the tracking plan in
 * src/core/tracking-plan.ts says. Postgres is the source of truth here; when a
 * PostHog key is configured the worker forwards them in batches and stamps
 * `forwarded_at` (src/lib/analytics).
 *
 *  - organization_id on every event: B2B analytics is per ORG (the `group` call).
 *  - user_id is Beacon's internal id, never the email. Deleting the user keeps
 *    the event and forgets the person (GDPR erasure, lesson 8.1).
 *  - org_plan: the plan when it happened, so funnels break down by plan.
 *  - properties: enums, numbers and booleans only (no PII), checked on write.
 *
 * At scale these move to ClickHouse or the analytics vendor (lesson 6.2 🔴);
 * never run heavy analytics queries on the production primary.
 */
export const analyticsEvents = pgTable(
  'analytics_events',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    userId: uuid('user_id').references(() => users.id, { onDelete: 'set null' }),
    event: text('event').notNull(),
    properties: jsonb('properties').notNull().default({}),
    orgPlan: orgPlan('org_plan').notNull(),
    occurredAt: timestamp('occurred_at', { withTimezone: true }).notNull().defaultNow(),
    forwardedAt: timestamp('forwarded_at', { withTimezone: true }),
  },
  (t) => [
    index('analytics_events_org_time_idx').on(t.organizationId, t.occurredAt),
    // The funnel reads one event type across all orgs over a time range.
    index('analytics_events_event_time_idx').on(t.event, t.occurredAt),
    // What the forwarder still has to send (tiny: forwarded rows leave it).
    index('analytics_events_unforwarded_idx').on(t.organizationId, t.occurredAt).where(sql`${t.forwardedAt} is null`),
  ],
);

/**
 * Lesson 6.3 (🟢): the flag rules. What a flag IS (type, owner, expiry, safe
 * default) is code, in src/core/flags.ts; how it is set right now is data,
 * here, changed without a deploy. A key with no row uses its safe default.
 */
export const featureFlags = pgTable(
  'feature_flags',
  {
    key: text('key').primaryKey(),
    // The master switch: false turns the flag off for every org, overrides included (the kill switch).
    enabled: boolean('enabled').notNull().default(false),
    // 0–100: which share of orgs, by a stable hash of key + org id (src/core/flags.ts rolloutBucket).
    rolloutPercent: integer('rollout_percent').notNull().default(0),
    updatedBy: uuid('updated_by').references(() => users.id, { onDelete: 'set null' }),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [check('feature_flags_rollout_percent_check', sql`${t.rolloutPercent} between 0 and 100`)],
);

/**
 * Lesson 6.3 (🟢): per-org targeting. "On for our own org", "on for these
 * three beta customers", "off for Acme". Platform configuration written by
 * Beacon staff, not tenant data: every process loads the whole rule set to
 * evaluate flags in memory, so this table is deliberately not under RLS
 * (tests/tenant-scoping.test.ts lists it).
 */
export const featureFlagOverrides = pgTable(
  'feature_flag_overrides',
  {
    key: text('key').notNull().references(() => featureFlags.key, { onDelete: 'cascade' }),
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    enabled: boolean('enabled').notNull(),
    updatedBy: uuid('updated_by').references(() => users.id, { onDelete: 'set null' }),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: updatedAt(),
  },
  (t) => [primaryKey({ columns: [t.key, t.organizationId] }), index('feature_flag_overrides_org_idx').on(t.organizationId)],
);

/*
 * Lesson 7.1: Beacon's staff, a separate population with separate roles.
 * Not a column on `users` and not a role in `memberships`: a bug in the
 * customer permission code must never grant back-office access. A staff
 * member signs in with a normal Beacon account (in production: your company's
 * identity provider, with MFA, on a separate hostname; see docs/SOLUTIONS.md),
 * and this row is what makes that account staff. `npm run staff` manages it.
 */
export const staffRole = pgEnum('staff_role', STAFF_ROLES);

export const staffUsers = pgTable('staff_users', {
  id: uuid('id').primaryKey().defaultRandom(),
  userId: uuid('user_id')
    .notNull()
    .unique()
    .references(() => users.id, { onDelete: 'cascade' }),
  role: staffRole('role').notNull(),
  createdBy: uuid('created_by').references((): AnyPgColumn => staffUsers.id, { onDelete: 'set null' }),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: updatedAt(),
});

/**
 * Lesson 7.1: one row per impersonation ("view as a customer"). The cookie
 * holds a random token; only its SHA-256 hash is stored (like a reset token).
 * Read-only, bound to ONE organization, and dead after 30 minutes whatever
 * happens (expires_at), or when the staff member exits (ended_at).
 * Not under row-level security: it is looked up before any org is known, on
 * every request of the staff member (tests/tenant-scoping.test.ts lists it).
 */
export const impersonationSessions = pgTable(
  'impersonation_sessions',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    tokenHash: text('token_hash').notNull().unique(),
    staffUserId: uuid('staff_user_id')
      .notNull()
      .references(() => staffUsers.id, { onDelete: 'cascade' }),
    targetUserId: uuid('target_user_id')
      .notNull()
      .references(() => users.id, { onDelete: 'cascade' }),
    organizationId: uuid('organization_id')
      .notNull()
      .references(() => organizations.id, { onDelete: 'cascade' }),
    reason: text('reason').notNull(),
    readOnly: boolean('read_only').notNull().default(true),
    expiresAt: timestamp('expires_at', { withTimezone: true }).notNull(),
    endedAt: timestamp('ended_at', { withTimezone: true }),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => [index('impersonation_sessions_org_idx').on(t.organizationId, t.createdAt)],
);

/**
 * Lesson 7.3: the audit log. Append-only evidence of who did what to which
 * thing, when and from where, written by recordAudit() (src/lib/audit.ts) IN
 * THE SAME TRANSACTION as the change it describes.
 *
 *  - actor_*: a SNAPSHOT (type, id, name, email) taken at event time, because
 *    the user may be deleted later; on_behalf_of_* is set during staff
 *    impersonation ("Beacon support, on behalf of Ana").
 *  - changes: before/after of the changed fields only, never whole rows or secrets.
 *  - organization_id: the tenant (row-level security, like every tenant
 *    table); NULL for platform events (a staff role granted, a flag changed),
 *    which only staff can read.
 *  - seq, prev_hash, hash: a hash chain per organization (tamper evidence):
 *    seq orders the chain, hash = sha256(prev_hash + the event).
 *
 * Append-only is enforced by the database, not by good intentions: the app
 * role (beacon_app) may INSERT and SELECT, never UPDATE or DELETE (migration
 * 0024). Retention deletes run as the owner, in the worker.
 */
export const auditEvents = pgTable(
  'audit_events',
  {
    id: uuid('id').primaryKey(),
    seq: bigint('seq', { mode: 'number' }).generatedAlwaysAsIdentity(),
    organizationId: uuid('organization_id').references(() => organizations.id, { onDelete: 'cascade' }),
    occurredAt: timestamp('occurred_at', { withTimezone: true }).notNull(),
    action: text('action').notNull(),
    category: text('category').notNull(),
    actorType: text('actor_type').notNull(),
    actorId: text('actor_id'),
    actorName: text('actor_name'),
    actorEmail: text('actor_email'),
    onBehalfOfId: text('on_behalf_of_id'),
    onBehalfOfName: text('on_behalf_of_name'),
    targetType: text('target_type'),
    targetId: text('target_id'),
    targetName: text('target_name'),
    ipAddress: text('ip_address'),
    userAgent: text('user_agent'),
    requestId: text('request_id'),
    via: text('via'),
    // Staff actions only (lesson 7.1): the required reason or ticket link.
    reason: text('reason'),
    changes: jsonb('changes'),
    metadata: jsonb('metadata'),
    prevHash: text('prev_hash').notNull(),
    hash: text('hash').notNull(),
  },
  (t) => [
    // The customer page walks one org's events newest first (seq follows time),
    // with optional filters on category, actor or target, then keyset pagination on seq.
    index('audit_events_org_seq_idx').on(t.organizationId, t.seq),
    index('audit_events_org_category_seq_idx').on(t.organizationId, t.category, t.seq),
    index('audit_events_org_actor_seq_idx').on(t.organizationId, t.actorId, t.seq),
    index('audit_events_org_target_seq_idx').on(t.organizationId, t.targetType, t.targetId, t.seq),
    // Retention deletes the oldest events of each org (and staff pages read by time).
    index('audit_events_occurred_idx').on(t.occurredAt),
  ],
);

export type Organization = typeof organizations.$inferSelect;
export type Membership = typeof memberships.$inferSelect;
export type Invitation = typeof invitations.$inferSelect;
export type Monitor = typeof monitors.$inferSelect;
export type CheckResult = typeof checkResults.$inferSelect;
export type Incident = typeof incidents.$inferSelect;
export type StoredFile = typeof files.$inferSelect;
export type IncidentUpdate = typeof incidentUpdates.$inferSelect;
export type Subscription = typeof subscriptions.$inferSelect;
export type UsageEvent = typeof usageEvents.$inferSelect;
export type EmailOutboxRow = typeof emailOutbox.$inferSelect;
export type Notification = typeof notifications.$inferSelect;
export type NotificationDelivery = typeof notificationDeliveries.$inferSelect;
export type StatusPageSubscriber = typeof statusPageSubscribers.$inferSelect;
export type ApiKey = typeof apiKeys.$inferSelect;
export type WebhookEndpoint = typeof webhookEndpoints.$inferSelect;
export type WebhookMessage = typeof webhookMessages.$inferSelect;
export type WorkflowRun = typeof workflowRuns.$inferSelect;
export type AnalyticsEvent = typeof analyticsEvents.$inferSelect;
export type FeatureFlag = typeof featureFlags.$inferSelect;
export type StaffUser = typeof staffUsers.$inferSelect;
export type ImpersonationSession = typeof impersonationSessions.$inferSelect;
export type AuditEvent = typeof auditEvents.$inferSelect;
