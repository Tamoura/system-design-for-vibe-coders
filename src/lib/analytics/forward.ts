import { and, asc, eq, inArray, isNull } from 'drizzle-orm';
import { schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { getAnalyticsDriver, type AnalyticsDriver } from './drivers';

const { analyticsEvents } = schema;

export const FORWARD_BATCH_SIZE = 500;
const MAX_BATCHES_PER_JOB = 10;

/**
 * Lesson 6.2 (🟡): the `analytics.forward` job. Sends one org's events that
 * have not been forwarded yet, in batches, then stamps them `forwarded_at`.
 *
 * Batched and asynchronous ("the request that records a click never waits on
 * the analytics database"): trackInTx() only inserts a row and at most one job
 * per org per minute. The network call happens here, outside any transaction
 * (lesson 2.4). If PostHog is down the driver throws and the queue retries
 * with backoff; nothing is lost, the rows are still unforwarded.
 */
export async function forwardAnalytics(orgId: string, driver: AnalyticsDriver | null = getAnalyticsDriver()): Promise<string> {
  if (!driver) return 'skipped: no analytics driver configured (events stay in Postgres)';
  let sent = 0;
  for (let i = 0; i < MAX_BATCHES_PER_JOB; i++) {
    const rows = await withOrg(orgId, (tx) =>
      tx
        .select()
        .from(analyticsEvents)
        .where(and(eq(analyticsEvents.organizationId, orgId), isNull(analyticsEvents.forwardedAt)))
        .orderBy(asc(analyticsEvents.occurredAt))
        .limit(FORWARD_BATCH_SIZE),
    );
    if (rows.length === 0) break;
    const plan = rows[rows.length - 1].orgPlan; // the most recent plan: the group's current trait
    await driver.send({
      orgId,
      plan,
      events: rows.map((r) => ({
        id: r.id,
        event: r.event,
        userId: r.userId,
        properties: r.properties as Record<string, unknown>,
        orgPlan: r.orgPlan,
        occurredAt: r.occurredAt,
      })),
    });
    const ids = rows.map((r) => r.id);
    await withOrg(orgId, (tx) =>
      tx
        .update(analyticsEvents)
        .set({ forwardedAt: new Date() })
        .where(and(eq(analyticsEvents.organizationId, orgId), inArray(analyticsEvents.id, ids))),
    );
    sent += rows.length;
    if (rows.length < FORWARD_BATCH_SIZE) break;
  }
  return `forwarded ${sent} event${sent === 1 ? '' : 's'} to ${driver.name}`;
}
