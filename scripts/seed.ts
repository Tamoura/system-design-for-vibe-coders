/**
 * Local development data: a demo user who owns an organization called "Demo"
 * (slug "demo") with three monitors. Sign in as demo@beacon.test with the
 * password below, or see the public page at /status/demo.
 *
 * Only seeds when the demo user does not exist yet.
 */
import { eq } from 'drizzle-orm';
import { db, schema, sql } from '../src/db';
import { hashPassword } from '../src/lib/password';

const DEMO_EMAIL = 'demo@beacon.test';
const DEMO_PASSWORD = 'beacon-demo-password';

const [existing] = await db.select().from(schema.users).where(eq(schema.users.email, DEMO_EMAIL));
if (existing) {
  console.log('• demo user already exists, skipping seed');
} else {
  await db.transaction(async (tx) => {
    // The same rows Better Auth writes on sign-up: a user, and a "credential"
    // login method holding the argon2id hash (lesson 1.1).
    const [user] = await tx.insert(schema.users).values({ name: 'Demo User', email: DEMO_EMAIL, emailVerified: true }).returning();
    await tx.insert(schema.accounts).values({
      userId: user.id,
      providerId: 'credential',
      accountId: user.id,
      password: await hashPassword(DEMO_PASSWORD),
    });
    // Lesson 1.2: the org owns the monitors; the user is its owner through a membership.
    const [org] = await tx.insert(schema.organizations).values({ name: 'Demo', slug: 'demo' }).returning();
    await tx.insert(schema.memberships).values({ organizationId: org.id, userId: user.id, role: 'owner' });
    await tx.insert(schema.monitors).values(
      [
        { name: 'Example homepage', url: 'https://example.com', intervalSeconds: 300 },
        { name: 'Beacon itself', url: 'http://localhost:3000', intervalSeconds: 60 },
        { name: 'Always broken (for testing incidents)', url: 'http://localhost:59999/nothing-listens-here', intervalSeconds: 60 },
      ].map((m) => ({ ...m, organizationId: org.id, createdBy: user.id })),
    );
  });
  console.log(`✓ seeded org "demo" with 3 monitors. Sign in as ${DEMO_EMAIL} / ${DEMO_PASSWORD}`);
}
await sql.end();
