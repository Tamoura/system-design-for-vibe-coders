import { and, desc, eq, gt, isNull, max, or } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { runCheck, type CheckOutcome } from '@/core/check';
import { decideIncident } from '@/core/incidents';
import { countStateChanges, FLAPPING, isFlapping } from '@/core/notifications';
import { entitlementsFor } from '@/core/plans';
import { isDue } from '@/core/schedule';
import { incidentOpenedEvent, incidentResolvedEvent, monitorFlappingEvent } from './notifications/events';
import { notifyInTx } from './notifications/pipeline';
import { publishInTx } from './realtime';

const { organizations, monitors, checkResults, incidents, incidentUpdates } = schema;

/*
 * The check runner (moved here from scripts/run-checks.ts in lesson 4.2, so
 * the tests can drive it): check every due monitor, store the result, open or
 * resolve incidents, and notify.
 *
 * Lesson 1.2/2.4: a system job that visits every organization, and inside
 * each one works in withOrg(org.id) like a request. The HTTP check happens
 * outside any transaction. TODO(5.1): a real scheduler and worker queue.
 */

type Org = { id: string; name: string; slug: string; plan: (typeof organizations.$inferSelect)['plan'] };
type MonitorRow = typeof monitors.$inferSelect;

/** Run the checks that are due (or all running monitors with `all`). Returns one line per monitor for the log. */
export async function runChecks(opts: { all?: boolean; check?: (url: string) => Promise<CheckOutcome> } = {}): Promise<{ lines: string[]; orgIds: string[] }> {
  const check = opts.check ?? ((url: string) => runCheck(url));
  const orgs = await db.select({ id: organizations.id, name: organizations.name, slug: organizations.slug, plan: organizations.plan }).from(organizations);
  const lines: string[] = [];
  const touched: string[] = [];
  for (const org of orgs) {
    const ent = entitlementsFor(org.plan);
    const due = await withOrg(org.id, async (tx) => {
      const running = await tx.select().from(monitors).where(and(eq(monitors.organizationId, org.id), eq(monitors.paused, false)));
      const last = await tx
        .select({ monitorId: checkResults.monitorId, at: max(checkResults.checkedAt) })
        .from(checkResults)
        .where(eq(checkResults.organizationId, org.id))
        .groupBy(checkResults.monitorId);
      const lastAt = new Map(last.map((r) => [r.monitorId, r.at]));
      return running.filter((m) => opts.all || isDue({ ...m, lastCheckedAt: lastAt.get(m.id) ?? null }, ent));
    });
    if (due.length) touched.push(org.id);
    for (const monitor of due) {
      const outcome = await check(monitor.url); // network: outside the transaction
      lines.push(await recordCheckResult(org, monitor, outcome));
    }
  }
  return { lines, orgIds: touched };
}

/**
 * Store one check result and act on it, in ONE transaction:
 *
 *   1. insert the result
 *   2. decide: open an incident (3 failures in a row), resolve it, or nothing
 *   3. lesson 4.2 (🟡) anti-flapping: count the monitor's state changes in the
 *      last hour. More than 4 → it is flapping: send ONE "flapping"
 *      notification and hold back the opened/resolved ones until it has been
 *      quiet for an hour.
 *   4. notify (notifyInTx): the notifications commit with the incident
 *
 * `now` is injectable so the tests can simulate an hour of flapping.
 */
export async function recordCheckResult(org: Pick<Org, 'id' | 'name' | 'slug'>, monitor: Pick<MonitorRow, 'id' | 'name' | 'url'>, outcome: CheckOutcome, now = new Date()): Promise<string> {
  return withOrg(org.id, async (tx) => {
    await tx.insert(checkResults).values({ organizationId: org.id, monitorId: monitor.id, checkedAt: now, ...outcome });
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
    let event = null;
    let line = `  ${outcome.ok ? '✓' : '✗'} ${monitor.name}: ${outcome.statusCode ?? outcome.error} in ${outcome.latencyMs} ms`;
    if (decision === 'open') {
      const cause = outcome.error ?? (outcome.statusCode ? `HTTP ${outcome.statusCode}` : 'Check failed');
      const [incident] = await tx.insert(incidents).values({ organizationId: org.id, monitorId: monitor.id, cause, openedAt: now }).returning();
      // Lesson 2.3: the first update, so the incident is searchable from the start.
      await tx.insert(incidentUpdates).values({ organizationId: org.id, incidentId: incident.id, body: `Opened automatically: ${cause}` });
      event = incidentOpenedEvent(org, monitor, incident);
      await publishInTx(tx, org.id, { type: 'incident.changed', monitorId: monitor.id, incidentId: incident.id, state: 'opened' });
      line = `  ✗ ${monitor.name}: incident opened (${cause})`;
    } else if (decision === 'resolve' && open) {
      await tx
        .update(incidents)
        .set({ resolvedAt: now })
        .where(and(eq(incidents.organizationId, org.id), eq(incidents.id, open.id)));
      await tx.insert(incidentUpdates).values({ organizationId: org.id, incidentId: open.id, body: 'Resolved automatically: checks are passing again.' });
      event = incidentResolvedEvent(org, monitor, { ...open, resolvedAt: now });
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
        await notifyInTx(tx, monitorFlappingEvent(org, monitor, now, changes));
        return `${line} · flapping (${changes} changes in an hour): one "flapping" notification, the rest held back`;
      }
      return `${line} · still flapping: notification held back`;
    }
    if (flappingSince && (event || changes === 0)) {
      // Settled: stable for a whole window, or changing at a normal rate again.
      await tx.update(monitors).set({ flappingSince: null }).where(and(eq(monitors.organizationId, org.id), eq(monitors.id, monitor.id)));
    }
    if (event) await notifyInTx(tx, event);
    return line;
  });
}
