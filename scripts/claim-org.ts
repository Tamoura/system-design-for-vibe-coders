/**
 * Make an existing user the owner of an organization:
 *
 *   npm run org:claim -- default you@example.com
 *
 * Migration 0003 moved the monitors that existed before Module 1 into an
 * organization called "default" that has no members. Sign up, then run this
 * once to become its owner.
 *
 * Lesson 7.1, "data fixes as code": a reviewed script in the repo, not a
 * `psql` UPDATE typed at night. Module 7 kept it (the admin panel has no
 * "make anyone an owner" button, on purpose) and made it leave evidence: the
 * change and its audit event commit together, named after the OS user.
 */
import './load-env'; // lesson 7.4: .env.local, like Next.js (must be the first import)
import { and, eq } from 'drizzle-orm';
import { db, schema, sql } from '../src/db';
import { cliAuditSource, recordAudit } from '../src/lib/audit';

const [slug, email] = process.argv.slice(2);
if (!slug || !email) {
  console.error('usage: npm run org:claim -- <org-slug> <user-email>');
  process.exit(1);
}
const [org] = await db.select().from(schema.organizations).where(eq(schema.organizations.slug, slug));
const [user] = await db.select().from(schema.users).where(eq(schema.users.email, email.toLowerCase()));
if (!org || !user) {
  console.error(!org ? `No organization with slug "${slug}"` : `No user with email ${email}. Sign up first.`);
  await sql.end();
  process.exit(1);
}
await db.transaction(async (tx) => {
  const [before] = await tx
    .select({ role: schema.memberships.role })
    .from(schema.memberships)
    .where(and(eq(schema.memberships.organizationId, org.id), eq(schema.memberships.userId, user.id)));
  await tx
    .insert(schema.memberships)
    .values({ organizationId: org.id, userId: user.id, role: 'owner' })
    .onConflictDoUpdate({ target: [schema.memberships.organizationId, schema.memberships.userId], set: { role: 'owner' } });
  await recordAudit(tx, {
    orgId: org.id,
    action: before ? 'member.role_changed' : 'member.joined',
    source: cliAuditSource('npm run org:claim'),
    target: { type: 'member', id: user.id, name: user.email },
    changes: { role: { before: before?.role ?? null, after: 'owner' } },
  });
});
console.log(`✓ ${email} is now an owner of "${org.name}" (/${org.slug}/monitors)`);
await sql.end();
