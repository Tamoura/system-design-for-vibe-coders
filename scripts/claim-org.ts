/**
 * Make an existing user the owner of an organization:
 *
 *   npm run org:claim -- default you@example.com
 *
 * Migration 0003 moved the monitors that existed before Module 1 into an
 * organization called "default" that has no members. Sign up, then run this
 * once to become its owner. It is a back-office tool with direct database
 * access; TODO(7.1): the admin panel replaces it.
 */
import { eq } from 'drizzle-orm';
import { db, schema, sql } from '../src/db';

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
await db
  .insert(schema.memberships)
  .values({ organizationId: org.id, userId: user.id, role: 'owner' })
  .onConflictDoUpdate({ target: [schema.memberships.organizationId, schema.memberships.userId], set: { role: 'owner' } });
console.log(`✓ ${email} is now an owner of "${org.name}" (/${org.slug}/monitors)`);
await sql.end();
