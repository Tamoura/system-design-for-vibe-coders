import { and, desc, eq, gt, isNull, or } from 'drizzle-orm';
import { schema } from '@/db';
import { withOrg } from '@/db/tenant';
import type { CheckOutcome } from '@/core/check';
import { decideIncident } from '@/core/incidents';
import { countStateChanges, FLAPPING, isFlapping } from '@/core/notifications';
import { enqueueNotify } from './notifications/incidents';
import type { JobData } from './queue';
import { publishInTx } from './realtime';

const { monitors, checkResults, incidents, incidentUpdates } = schema;

/*
 * Lesson 4.2 → 5.1: what happens with a check result. The checking itself is
 * scheduled and run by the queue (src/lib/scheduler.ts); this file decides
 * what a result means: store it, open or resolve an incident, flapping.
 */

type Org = { id: string; name: string; slug: string };
type MonitorRow = typeof monitors.$inferSelect;

/**
 * Store one check result and act on it, in ONE transaction:
 *
 *   1. insert the result
 *   2. decide: open an incident (3 failures in a row), resolve it, or nothing
 *   3. lesson 4.2 (🟡) anti-flapping: count the monitor's state changes in the
 *      last hour. More than 4 → it is flapping: send ONE "flapping"
 *      notification and hold back the opened/resolved ones until it has been
 *      quiet for an hour.
 *   4. lesson 5.1 (🟢/🟡): ENQUEUE an `incident.notify` job, in this same
 *      transaction. The checker sends nothing itself: no email, Slack or SMS
 *      call, no recipient lookup. The job exists if and only if the incident
 *      committed, and the worker does the fan-out (src/lib/notifications/incidents.ts).
 *
 * `now` is injectable so the tests can simulate an hour of flapping.
 */
export async function recordCheckResult(
  org: Org,
  monitor: Pick<MonitorRow, 'id' | 'name' | 'url'>,
  outcome: CheckOutcome,
  now = new Date(),
  opts: { scheduledAt?: Date } = {},
): Promise<string> {
  return withOrg(org.id, async (tx) => {
    // Lesson 5.1: a scheduled check is stored with its slot, unique per monitor.
    // If this slot is already recorded, the job ran twice: do nothing more.
    const stored = await tx
      .insert(checkResults)
      .values({ organizationId: org.id, monitorId: monitor.id, checkedAt: now, scheduledAt: opts.scheduledAt ?? null, ...outcome })
      .onConflictDoNothing()
      .returning({ id: checkResults.id });
    if (stored.length === 0) return `  = ${monitor.name}: this slot was already checked (the job ran twice), nothing to do`;
    // Lesson 4.3: open dashboards turn the tile red or green. Sent when this transaction commits.
    await publishInTx(tx, org.id, { type: 'monitor.status', monitorId: monitor.id, state: outcome.ok ? 'up' : 'down', checkedAt: now.toISOString(), latencyMs: outcome.latencyMs });
    const recent = await tx
      .select({ ok: checkResults.ok })
      .from(checkResults)
      .where(and(eq(checkResults.organizationId, org.id), eq(checkResults.monitorId, monitor.id)))
      .orderBy(desc(checkResults.checkedAt))
      .limit(5);
    const [open] = await tx
      .select()
      .from(incidents)
      .where(and(eq(incidents.organizationId, org.id), eq(incidents.monitorId, monitor.id), isNull(incidents.resolvedAt)))
      .limit(1);

    const decision = decideIncident(Boolean(open), recent.map((r) => r.ok));
    // Lesson 5.1: the job carries ids, not the incident: the worker re-reads it.
    let event: JobData['incident.notify'] | null = null;
    let line = `  ${outcome.ok ? '✓' : '✗'} ${monitor.name}: ${outcome.statusCode ?? outcome.error} in ${outcome.latencyMs} ms`;
    if (decision === 'open') {
      const cause = outcome.error ?? (outcome.statusCode ? `HTTP ${outcome.statusCode}` : 'Check failed');
      const [incident] = await tx.insert(incidents).values({ organizationId: org.id, monitorId: monitor.id, cause, openedAt: now }).returning();
      // Lesson 2.3: the first update, so the incident is searchable from the start.
      await tx.insert(incidentUpdates).values({ organizationId: org.id, incidentId: incident.id, body: `Opened automatically: ${cause}` });
      event = { orgId: org.id, event: 'incident.opened', incidentId: incident.id };
      await publishInTx(tx, org.id, { type: 'incident.changed', monitorId: monitor.id, incidentId: incident.id, state: 'opened' });
      line = `  ✗ ${monitor.name}: incident opened (${cause})`;
    } else if (decision === 'resolve' && open) {
      await tx
        .update(incidents)
        .set({ resolvedAt: now })
        .where(and(eq(incidents.organizationId, org.id), eq(incidents.id, open.id)));
      await tx.insert(incidentUpdates).values({ organizationId: org.id, incidentId: open.id, body: 'Resolved automatically: checks are passing again.' });
      event = { orgId: org.id, event: 'incident.resolved', incidentId: open.id };
      await publishInTx(tx, org.id, { type: 'incident.changed', monitorId: monitor.id, incidentId: open.id, state: 'resolved' });
      line = `  ✓ ${monitor.name}: incident resolved`;
    }

    // Lesson 4.2 (🟡): flapping. Count state changes in the window, this one included.
    const since = new Date(now.getTime() - FLAPPING.windowMs);
    const window = await tx
      .select({ openedAt: incidents.openedAt, resolvedAt: incidents.resolvedAt })
      .from(incidents)
      .where(and(eq(incidents.organizationId, org.id), eq(incidents.monitorId, monitor.id), or(gt(incidents.openedAt, since), gt(incidents.resolvedAt, since))));
    const changes = countStateChanges(window, since);
    const [{ flappingSince }] = await tx.select({ flappingSince: monitors.flappingSince }).from(monitors).where(and(eq(monitors.organizationId, org.id), eq(monitors.id, monitor.id)));

    if (event && isFlapping(changes)) {
      if (!flappingSince) {
        // It just started flapping: say so once, instead of this opened/resolved alert.
        await tx.update(monitors).set({ flappingSince: now }).where(and(eq(monitors.organizationId, org.id), eq(monitors.id, monitor.id)));
        await enqueueNotify(tx, { orgId: org.id, event: 'monitor.flapping', monitorId: monitor.id, since: now.toISOString(), changes });
        return `${line} · flapping (${changes} changes in an hour): one "flapping" notification, the rest held back`;
      }
      return `${line} · still flapping: notification held back`;
    }
    if (flappingSince && (event || changes === 0)) {
      // Settled: stable for a whole window, or changing at a normal rate again.
      await tx.update(monitors).set({ flappingSince: null }).where(and(eq(monitors.organizationId, org.id), eq(monitors.id, monitor.id)));
    }
    if (event) await enqueueNotify(tx, event);
    return line;
  });
}
