import { sql } from 'drizzle-orm';
import { boolean, check, customType, index, integer, pgEnum, pgTable, primaryKey, text, timestamp, uniqueIndex, uuid, type AnyPgColumn } from 'drizzle-orm/pg-core';
import { FILE_KINDS } from '../core/files';
import { PLAN_IDS } from '../core/plans';
import { ROLES } from '../core/roles';
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

export const organizations = pgTable('organizations', {
  id: uuid('id').primaryKey().defaultRandom(),
  name: text('name').notNull(),
  // Goes in the URL: /acme/monitors and /status/acme. See src/core/slugs.ts.
  slug: text('slug').notNull().unique(),
  // The public status page at /status/[slug]. Only roles with "page.publish" may switch it (lesson 1.3).
  statusPagePublic: boolean('status_page_public').notNull().default(true),
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
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: updatedAt(),
});

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
  },
  (t) => [
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

export type Organization = typeof organizations.$inferSelect;
export type Membership = typeof memberships.$inferSelect;
export type Invitation = typeof invitations.$inferSelect;
export type Monitor = typeof monitors.$inferSelect;
export type CheckResult = typeof checkResults.$inferSelect;
export type Incident = typeof incidents.$inferSelect;
export type StoredFile = typeof files.$inferSelect;
export type IncidentUpdate = typeof incidentUpdates.$inferSelect;
export type Subscription = typeof subscriptions.$inferSelect;
