import { and, eq, like, sql } from 'drizzle-orm';
import { schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { CHANNEL_LABELS, type Channel } from '@/core/notifications';
import { loadNotifyEvent, type NotifyJob } from '../notifications/incidents';
import { notifyInTx } from '../notifications/pipeline';
import { defineWorkflow } from './engine';

const { notificationDeliveries, incidentUpdates } = schema;

/**
 * Lesson 5.4 (🟢): the incident fan-out as a workflow with three named steps.
 *
 *   load-incident      re-read the incident (or monitor) and build the event
 *   notify-channels    notifications + deliveries + one delivery job each
 *   record-deliveries  write "who was told, and how" on the incident's timeline
 *
 * Each step's result is recorded. Kill the worker after step 2 and the run
 * resumes at step 3: step 2 is replayed from its recorded result, so nobody is
 * notified twice. A failing step 3 retries on its own (tested).
 */
export const incidentNotify = defineWorkflow('incident-notify', async (ctx, job: NotifyJob) => {
  const event = await ctx.step('load-incident', () => loadNotifyEvent(job), job);
  if ('skipped' in event) return event;
  const sent = await ctx.step('notify-channels', () => withOrg(job.orgId, (tx) => notifyInTx(tx, event)), { key: event.key, category: event.category });
  if (job.event === 'monitor.flapping') return sent; // no incident to write on
  const summary = await ctx.step('record-deliveries', () => recordDeliveries(job.orgId, job.incidentId, event.key));
  return { ...sent, summary };
});

/** The incident timeline gets one line: "Alert sent: 4 in-app, 3 email, 1 SMS, Slack." */
async function recordDeliveries(orgId: string, incidentId: string, eventKey: string): Promise<string> {
  return withOrg(orgId, async (tx) => {
    const rows = await tx
      .select({ channel: notificationDeliveries.channel, n: sql<number>`count(*)::int` })
      .from(notificationDeliveries)
      .where(and(eq(notificationDeliveries.organizationId, orgId), like(notificationDeliveries.dedupeKey, `${eventKey}:%`)))
      .groupBy(notificationDeliveries.channel);
    const parts = rows.map((r) => (r.channel === 'slack' ? 'Slack' : `${r.n} ${CHANNEL_LABELS[r.channel as Channel].toLowerCase()}`));
    const what = eventKey.startsWith('incident.resolved') ? 'Resolution notice sent' : 'Alert sent';
    const body = parts.length ? `${what}: ${parts.join(', ')}.` : `${what} to nobody (no eligible recipients).`;
    // Idempotent too: one line per event, however often this step runs.
    const [existing] = await tx
      .select({ id: incidentUpdates.id })
      .from(incidentUpdates)
      .where(and(eq(incidentUpdates.organizationId, orgId), eq(incidentUpdates.incidentId, incidentId), like(incidentUpdates.body, `${what}:%`)));
    if (!existing) await tx.insert(incidentUpdates).values({ organizationId: orgId, incidentId, body });
    return body;
  });
}
