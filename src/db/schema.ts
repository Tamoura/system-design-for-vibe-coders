import { boolean, index, integer, pgTable, text, timestamp, uuid } from 'drizzle-orm/pg-core';

// Lesson 1.1: users, sessions and login methods. Better Auth defines their shape.
export * from './auth-schema';

/*
 * Beacon's core domain: monitors, the results of checking them, and the
 * incidents opened when they fail. This is the ~15% of Beacon that is
 * *Beacon*. Everything the course adds around it — users, organizations,
 * billing, jobs, webhooks, audit logs — is the generic 85%.
 *
 * TODO(1.2): Beacon is single-tenant on `main`. Every table below needs an
 *            `organization_id` before a second customer can sign up.
 */

export const monitors = pgTable('monitors', {
  id: uuid('id').primaryKey().defaultRandom(),
  name: text('name').notNull(),
  url: text('url').notNull(),
  // How often to check, in seconds. Plans will limit this (TODO(3.2)).
  intervalSeconds: integer('interval_seconds').notNull().default(300),
  paused: boolean('paused').notNull().default(false),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
});

export const checkResults = pgTable(
  'check_results',
  {
    id: uuid('id').primaryKey().defaultRandom(),
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
    monitorId: uuid('monitor_id').notNull().references(() => monitors.id, { onDelete: 'cascade' }),
    openedAt: timestamp('opened_at', { withTimezone: true }).notNull().defaultNow(),
    resolvedAt: timestamp('resolved_at', { withTimezone: true }),
    cause: text('cause').notNull(),
  },
  (t) => [index('incidents_monitor_idx').on(t.monitorId, t.openedAt.desc())],
);

export type Monitor = typeof monitors.$inferSelect;
export type CheckResult = typeof checkResults.$inferSelect;
export type Incident = typeof incidents.$inferSelect;
