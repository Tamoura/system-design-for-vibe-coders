import { eq } from 'drizzle-orm';
import { schema } from '@/db';
import { withOrg, type TenantTx } from '@/db/tenant';
import { findPii, TRACKING_PLAN, type EventName, type EventProperties } from '@/core/tracking-plan';
import { enqueueInTx } from '../queue';
import { getAnalyticsDriver } from './drivers';
import { logger } from '../observability/logger';

const { organizations, analyticsEvents } = schema;

/*
 * Lesson 6.2 (🟡): server-side product analytics.
 *
 *   business write ─► trackInTx(tx, { orgId, userId }, 'monitor_created', { … })   same transaction
 *                        │ checks the event against the tracking plan (name, exact properties, no PII)
 *                        ├─► INSERT analytics_events (org, user id, event, properties, plan)
 *                        └─► if PostHog is configured: one `analytics.forward` job per org per minute
 *   worker ─► forwardAnalytics(orgId) ─► PostHog /batch (events + the org as a group) ─► forwarded_at
 *
 * Why server-side: the event is recorded because the monitor really was
 * created, in the same commit. An ad blocker cannot drop it and a user cannot
 * forge it (blocking PostHog in the browser changes nothing: the browser never
 * talks to PostHog). Why Postgres first: the events are ours, queryable next
 * to the app data for the activation funnel (./funnel.ts), and a PostHog
 * outage just delays forwarding (the job retries).
 *
 * `track` only accepts names from the tracking plan with exactly their
 * properties: `track(scope, 'monitor_creatd', …)` does not compile.
 */

export type TrackScope = { orgId: string; userId?: string | null };

export class TrackingPlanError extends Error {}

/** Check an event against the plan. Throws TrackingPlanError; returns the parsed properties. */
export function validateEvent<E extends EventName>(event: E, properties: EventProperties<E>): Record<string, unknown> {
  const spec = TRACKING_PLAN[event];
  if (!spec) throw new TrackingPlanError(`"${event}" is not in the tracking plan (src/core/tracking-plan.ts)`);
  const parsed = spec.properties.safeParse(properties);
  if (!parsed.success) throw new TrackingPlanError(`${event}: ${parsed.error.issues.map((i) => `${i.path.join('.') || '(root)'} ${i.message}`).join('; ')}`);
  const pii = findPii(parsed.data as Record<string, unknown>);
  if (pii.length) throw new TrackingPlanError(`${event}: ${pii.join('; ')}`);
  return parsed.data as Record<string, unknown>;
}

/**
 * Record a product event inside the caller's withOrg() transaction, so it
 * commits with the change it describes. A tracking-plan violation is a bug:
 * it throws in development and tests (so it never ships), and in production
 * it is logged and the event dropped: analytics must never break a monitor create.
 */
export async function trackInTx<E extends EventName>(tx: TenantTx, scope: TrackScope, event: E, properties: EventProperties<E>, at = new Date()): Promise<void> {
  let props: Record<string, unknown>;
  try {
    props = validateEvent(event, properties);
  } catch (err) {
    if (process.env.NODE_ENV === 'production') {
      logger.error({ event, error: (err as Error).message }, 'analytics.event_dropped');
      return;
    }
    throw err;
  }
  const [org] = await tx.select({ plan: organizations.plan }).from(organizations).where(eq(organizations.id, scope.orgId));
  await tx.insert(analyticsEvents).values({
    organizationId: scope.orgId,
    userId: scope.userId ?? null,
    event,
    properties: props,
    orgPlan: org.plan,
    occurredAt: at,
  });
  if (getAnalyticsDriver()) {
    // One forwarding job per org per minute (deterministic id): events are
    // sent in batches, not one HTTP call each.
    const minute = Math.floor(at.getTime() / 60_000);
    await enqueueInTx(tx, 'analytics.forward', { orgId: scope.orgId }, {
      key: `${scope.orgId}@${minute}`,
      startAfter: new Date((minute + 1) * 60_000),
      group: scope.orgId,
    });
  }
}

/** The same, in its own transaction: for code that has none open (after a commit, a route handler). */
export async function track<E extends EventName>(scope: TrackScope, event: E, properties: EventProperties<E>): Promise<void> {
  await withOrg(scope.orgId, (tx) => trackInTx(tx, scope, event, properties));
}

export { getAnalyticsDriver, setAnalyticsDriverForTests, createMemoryAnalyticsDriver } from './drivers';
