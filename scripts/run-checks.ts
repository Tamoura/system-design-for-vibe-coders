/**
 * Check every monitor that is due, store the results, and open or resolve
 * incidents. Run it from cron every minute, or by hand:
 *
 *   npm run checks:run            only monitors whose interval has passed
 *   npm run checks:run -- --all   every running monitor now (for trying things out)
 *
 * Lesson 3.2 (🟡): workers enforce entitlements too. Paused monitors (by hand
 * or frozen by the plan limit) never run, and a monitor is due only when its
 * interval, raised to the org's current plan minimum, has passed
 * (src/core/schedule.ts). The plan comes from the same snapshot the API uses.
 *
 * TODO(5.1): this is a loop in a script. It has no schedule per monitor, no
 * retries, no concurrency limit per tenant and no protection against two copies
 * running at once. Lesson 5.1 turns it into a proper scheduler + worker queue.
 * TODO(4.2): opening an incident should notify the team.
 *
 * Lesson 1.2: this is a system job, not a user request, so it visits every
 * organization. Everything it writes copies the monitor's organization_id
 * (the tenant_id rule), and every read about one monitor filters on that org.
 *
 * Lesson 2.4: jobs set the tenant too. The only cross-tenant query is the list
 * of organizations; everything else runs inside withOrg(org.id), so row-level
 * security applies to the job exactly as it does to a web request. Each unit
 * of work carries its orgId (the future job payload of lesson 5.1). The HTTP
 * check itself happens outside any transaction: never hold a database
 * connection open while waiting on the network.
 */
import { and, desc, eq, isNull, max } from 'drizzle-orm';
import { db, schema, sql } from '../src/db';
import { withOrg } from '../src/db/tenant';
import { runCheck } from '../src/core/check';
import { decideIncident } from '../src/core/incidents';
import { entitlementsFor } from '../src/core/plans';
import { isDue } from '../src/core/schedule';

const { organizations, monitors, checkResults, incidents, incidentUpdates } = schema;
const checkAll = process.argv.includes('--all');

const orgs = await db.select({ id: organizations.id, plan: organizations.plan }).from(organizations);
let checked = 0;

for (const { id: orgId, plan } of orgs) {
  const ent = entitlementsFor(plan);
  const active = await withOrg(orgId, async (tx) => {
    const running = await tx.select().from(monitors).where(and(eq(monitors.organizationId, orgId), eq(monitors.paused, false)));
    const last = await tx
      .select({ monitorId: checkResults.monitorId, at: max(checkResults.checkedAt) })
      .from(checkResults)
      .where(eq(checkResults.organizationId, orgId))
      .groupBy(checkResults.monitorId);
    const lastAt = new Map(last.map((r) => [r.monitorId, r.at]));
    return running.filter((m) => checkAll || isDue({ ...m, lastCheckedAt: lastAt.get(m.id) ?? null }, ent));
  });
  for (const m of active) {
    checked++;
    const outcome = await runCheck(m.url); // network: outside the transaction
    const message = await withOrg(orgId, async (tx) => {
      await tx.insert(checkResults).values({ organizationId: orgId, monitorId: m.id, ...outcome });
      const recent = await tx
        .select({ ok: checkResults.ok })
        .from(checkResults)
        .where(and(eq(checkResults.organizationId, orgId), eq(checkResults.monitorId, m.id)))
        .orderBy(desc(checkResults.checkedAt))
        .limit(5);
      const [open] = await tx
        .select()
        .from(incidents)
        .where(and(eq(incidents.organizationId, orgId), eq(incidents.monitorId, m.id), isNull(incidents.resolvedAt)))
        .limit(1);

      const decision = decideIncident(Boolean(open), recent.map((r) => r.ok));
      if (decision === 'open') {
        const cause = outcome.error ?? 'Check failed';
        const [incident] = await tx.insert(incidents).values({ organizationId: orgId, monitorId: m.id, cause }).returning();
        // Lesson 2.3: the first update, so the incident is searchable from the start.
        await tx.insert(incidentUpdates).values({ organizationId: orgId, incidentId: incident.id, body: `Opened automatically: ${cause}` });
        return `  ✗ ${m.name}: incident opened (${outcome.error})`;
      }
      if (decision === 'resolve' && open) {
        await tx
          .update(incidents)
          .set({ resolvedAt: new Date() })
          .where(and(eq(incidents.organizationId, orgId), eq(incidents.id, open.id)));
        await tx
          .insert(incidentUpdates)
          .values({ organizationId: orgId, incidentId: open.id, body: 'Resolved automatically: checks are passing again.' });
        return `  ✓ ${m.name}: incident resolved`;
      }
      return `  ${outcome.ok ? '✓' : '✗'} ${m.name}: ${outcome.statusCode ?? outcome.error} in ${outcome.latencyMs} ms`;
    });
    console.log(message);
  }
}
console.log(`Checked ${checked} monitor(s) in ${orgs.length} organization(s)${checkAll ? '' : ' (only those due; --all checks every running monitor)'}.`);
await sql.end();
