/**
 * Check every active monitor once, store the results, and open or resolve
 * incidents. Run it by hand (`npm run checks:run`) or from cron.
 *
 * TODO(5.1): this is a loop in a script. It has no schedule per monitor, no
 * retries, no concurrency limit per tenant and no protection against two copies
 * running at once. Lesson 5.1 turns it into a proper scheduler + worker queue.
 * TODO(4.2): opening an incident should notify the team.
 */
import { and, desc, eq, isNull } from 'drizzle-orm';
import { db, schema, sql } from '../src/db';
import { runCheck } from '../src/core/check';
import { decideIncident } from '../src/core/incidents';

const { monitors, checkResults, incidents } = schema;

const active = await db.select().from(monitors).where(eq(monitors.paused, false));
console.log(`Checking ${active.length} monitor(s)…`);

for (const m of active) {
  const outcome = await runCheck(m.url);
  await db.insert(checkResults).values({ monitorId: m.id, ...outcome });

  const recent = await db
    .select({ ok: checkResults.ok })
    .from(checkResults)
    .where(eq(checkResults.monitorId, m.id))
    .orderBy(desc(checkResults.checkedAt))
    .limit(5);
  const [open] = await db
    .select()
    .from(incidents)
    .where(and(eq(incidents.monitorId, m.id), isNull(incidents.resolvedAt)))
    .limit(1);

  const decision = decideIncident(Boolean(open), recent.map((r) => r.ok));
  if (decision === 'open') {
    await db.insert(incidents).values({ monitorId: m.id, cause: outcome.error ?? 'Check failed' });
    console.log(`  ✗ ${m.name}: incident opened (${outcome.error})`);
  } else if (decision === 'resolve' && open) {
    await db.update(incidents).set({ resolvedAt: new Date() }).where(eq(incidents.id, open.id));
    console.log(`  ✓ ${m.name}: incident resolved`);
  } else {
    console.log(`  ${outcome.ok ? '✓' : '✗'} ${m.name}: ${outcome.statusCode ?? outcome.error} in ${outcome.latencyMs} ms`);
  }
}
await sql.end();
