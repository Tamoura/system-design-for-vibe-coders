import { sql } from 'drizzle-orm';
import { boolean, index, integer, pgEnum, pgTable, primaryKey, text, timestamp, uniqueIndex, uuid } from 'drizzle-orm/pg-core';
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

export const organizations = pgTable('organizations', {
  id: uuid('id').primaryKey().defaultRandom(),
  name: text('name').notNull(),
  // Goes in the URL: /acme/monitors and /status/acme. See src/core/slugs.ts.
  slug: text('slug').notNull().unique(),
  // The public status page at /status/[slug]. Only roles with "page.publish" may switch it (lesson 1.3).
  statusPagePublic: boolean('status_page_public').notNull().default(true),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
});

export const memberships = pgTable(
  'memberships',
  {
    organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
    userId: uuid('user_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
    role: orgRole('role').notNull(),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
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
    // How often to check, in seconds. Plans will limit this (TODO(3.2)).
    intervalSeconds: integer('interval_seconds').notNull().default(300),
    paused: boolean('paused').notNull().default(false),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => [index('monitors_org_idx').on(t.organizationId, t.createdAt)],
);

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
  (t) => [index('check_results_monitor_time_idx').on(t.monitorId, t.checkedAt.desc())],
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
  },
  (t) => [index('incidents_monitor_idx').on(t.monitorId, t.openedAt.desc())],
);

export type Organization = typeof organizations.$inferSelect;
export type Membership = typeof memberships.$inferSelect;
export type Invitation = typeof invitations.$inferSelect;
export type Monitor = typeof monitors.$inferSelect;
export type CheckResult = typeof checkResults.$inferSelect;
export type Incident = typeof incidents.$inferSelect;
