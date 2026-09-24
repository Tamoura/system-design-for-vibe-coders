import { and, eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg, type TenantTx } from '@/db/tenant';
import { enqueueInTx } from '../queue';
import type { JobData } from '../queue/queues';
import { incidentOpenedEvent, incidentResolvedEvent, monitorFlappingEvent } from './events';
import { notifyInTx, type NotifyEvent } from './pipeline';

const { organizations, monitors, incidents } = schema;

/**
 * Lesson 5.1 (🟢): the `incident.notify` job. The checker (or "Mark
 * resolved") committed the incident and this job with it; here, in the
 * worker, the event becomes notifications and one delivery job per channel.
 *
 * It re-reads everything from the ids in the payload (lesson 5.1: IDs, not
 * objects), and is a no-op when the incident or monitor is gone by now: a
 * deleted monitor's incident has nobody left to tell (tested). Running it
 * twice adds nothing: notifyInTx() dedupes per person and per channel.
 */
export async function notifyIncident(job: JobData['incident.notify']): Promise<{ skipped: string } | { notified: number; deliveries: number }> {
  const [org] = await db.select({ id: organizations.id, name: organizations.name, slug: organizations.slug }).from(organizations).where(eq(organizations.id, job.orgId));
  if (!org) return { skipped: 'organization deleted' };
  return withOrg(org.id, async (tx) => {
    let event: NotifyEvent;
    if (job.event === 'monitor.flapping') {
      const [monitor] = await tx.select().from(monitors).where(and(eq(monitors.organizationId, org.id), eq(monitors.id, job.monitorId)));
      if (!monitor) return { skipped: 'monitor deleted' };
      event = monitorFlappingEvent(org, monitor, new Date(job.since), job.changes);
    } else {
      const [row] = await tx
        .select({ incident: incidents, monitor: monitors })
        .from(incidents)
        .innerJoin(monitors, eq(monitors.id, incidents.monitorId))
        .where(and(eq(incidents.organizationId, org.id), eq(incidents.id, job.incidentId)));
      if (!row) return { skipped: 'incident deleted' };
      const { incident, monitor } = row;
      if (job.event === 'incident.opened') {
        event = incidentOpenedEvent(org, monitor, incident);
      } else {
        if (!incident.resolvedAt) return { skipped: 'incident is open again' };
        event = incidentResolvedEvent(org, monitor, { ...incident, resolvedAt: incident.resolvedAt });
      }
    }
    return notifyInTx(tx, event);
  });
}

/**
 * Enqueue `incident.notify` inside the transaction that changed the incident.
 * The job's key names the event ("incident.opened:<id>"), so the same event
 * enqueued twice is one job; notifyInTx() dedupes per person on top of that.
 */
export async function enqueueNotify(tx: TenantTx, job: JobData['incident.notify']) {
  const key = job.event === 'monitor.flapping' ? `${job.event}:${job.monitorId}:${job.since}` : `${job.event}:${job.incidentId}`;
  await enqueueInTx(tx, 'incident.notify', job, { key, group: job.orgId });
}
