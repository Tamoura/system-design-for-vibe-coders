import { and, eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg, type TenantTx } from '@/db/tenant';
import { startWorkflowInTx } from '../workflows/engine';
import { incidentOpenedEvent, incidentResolvedEvent, monitorFlappingEvent } from './events';
import type { NotifyEvent } from './pipeline';

const { organizations, monitors, incidents } = schema;

/** What the checker hands over: ids, not objects (lesson 5.1). */
export type NotifyJob =
  | { orgId: string; event: 'incident.opened' | 'incident.resolved'; incidentId: string }
  | { orgId: string; event: 'monitor.flapping'; monitorId: string; since: string; changes: number };

/**
 * Lesson 5.1 (🟢) → 5.4 (🟢): hand the fan-out to the worker, inside the
 * transaction that changed the incident. In 5.1 this was one
 * `incident.notify` job; since 5.4 it starts the three-step `incident-notify`
 * workflow (src/lib/workflows/incident-notify.ts), which runs on the same
 * queue. The key names the event ("incident.opened:<id>"): the same event
 * handed over twice is one run, and notifyInTx() dedupes per person on top.
 */
export async function enqueueNotify(tx: TenantTx, job: NotifyJob) {
  const key = job.event === 'monitor.flapping' ? `${job.event}:${job.monitorId}:${job.since}` : `${job.event}:${job.incidentId}`;
  const subject = job.event === 'monitor.flapping' ? job.monitorId : job.incidentId;
  await startWorkflowInTx(tx, job.orgId, 'incident-notify', `incident-notify:${key}`, job, subject);
}

/**
 * Step 1 of the fan-out: re-read the incident (or monitor) from the ids and
 * build the event, or say why there is nothing to do: a deleted monitor's
 * incident has nobody left to tell (tested).
 */
export async function loadNotifyEvent(job: NotifyJob): Promise<NotifyEvent | { skipped: string }> {
  const [org] = await db.select({ id: organizations.id, name: organizations.name, slug: organizations.slug }).from(organizations).where(eq(organizations.id, job.orgId));
  if (!org) return { skipped: 'organization deleted' };
  return withOrg(org.id, async (tx) => {
    if (job.event === 'monitor.flapping') {
      const [monitor] = await tx.select().from(monitors).where(and(eq(monitors.organizationId, org.id), eq(monitors.id, job.monitorId)));
      if (!monitor) return { skipped: 'monitor deleted' };
      return monitorFlappingEvent(org, monitor, new Date(job.since), job.changes);
    }
    const [row] = await tx
      .select({ incident: incidents, monitor: monitors })
      .from(incidents)
      .innerJoin(monitors, eq(monitors.id, incidents.monitorId))
      .where(and(eq(incidents.organizationId, org.id), eq(incidents.id, job.incidentId)));
    if (!row) return { skipped: 'incident deleted' };
    const { incident, monitor } = row;
    if (job.event === 'incident.opened') return incidentOpenedEvent(org, monitor, incident);
    if (!incident.resolvedAt) return { skipped: 'incident is open again' };
    return incidentResolvedEvent(org, monitor, { ...incident, resolvedAt: incident.resolvedAt });
  });
}
