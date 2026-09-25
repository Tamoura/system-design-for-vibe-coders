/**
 * Lesson 7.3: the audit log from the command line (as the database owner).
 *
 *   npm run audit -- verify            recompute every hash chain; exit 1 if one is broken
 *   npm run audit -- verify <org-slug> one org's chain, with the first problems
 *   npm run audit -- purge             delete events past their plan's retention now
 *
 * The worker runs both every night (audit.verify, audit.retention).
 */
import './load-env'; // lesson 7.4: .env.local, like Next.js (must be the first import)
import { eq } from 'drizzle-orm';
import { db, schema, sql } from '../src/db';
import { purgeExpiredAuditEvents, verifyAllAuditChains, verifyAuditChain } from '../src/lib/admin/audit';

const [command, slug] = process.argv.slice(2);

try {
  if (command === 'verify' && slug) {
    const [org] = await db.select({ id: schema.organizations.id }).from(schema.organizations).where(eq(schema.organizations.slug, slug));
    if (!org) throw new Error(`No organization "${slug}"`);
    const result = await verifyAuditChain(org.id);
    console.log(result.ok ? `✓ ${slug}: ${result.checked} events, chain intact` : `✗ ${slug}: ${result.problems.length} problem(s)`, result.ok ? '' : result.problems.slice(0, 20));
    if (!result.ok) process.exitCode = 1;
  } else if (command === 'verify') {
    const result = await verifyAllAuditChains();
    console.log(result.broken.length ? `✗ broken chains: ${result.broken.map((b) => `${b.org} (${b.problems})`).join(', ')}` : `✓ ${result.chains} chains, ${result.events} events, all intact`);
    if (result.broken.length) process.exitCode = 1;
  } else if (command === 'purge') {
    const { deleted } = await purgeExpiredAuditEvents();
    console.log(`✓ deleted ${deleted} event(s) past retention`);
  } else {
    console.error('usage: npm run audit -- verify [org-slug] | purge');
    process.exitCode = 1;
  }
} finally {
  await sql.end();
}
