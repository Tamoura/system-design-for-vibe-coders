/**
 * Local development data (lesson 2.1): one organization "Demo" (slug "demo")
 * with an owner and a member, five monitors, and a day of check results.
 *
 *   demo@beacon.test    owner    password: beacon-demo-password
 *   member@beacon.test  member   password: beacon-demo-password
 *
 * Idempotent: every row is looked up by a natural key (email, slug, monitor
 * name) before it is inserted, so running it twice changes nothing, and running
 * it after someone adds a monitor here fills in only what is missing.
 * `npm run db:reset` drops everything, migrates and runs this.
 *
 * Never run it against production: it creates users with a known password.
 */
import { and, count, eq } from 'drizzle-orm';
import { db, schema, sql } from '../src/db';
import { hashPassword } from '../src/lib/password';
import type { Role } from '../src/core/roles';

if (process.env.NODE_ENV === 'production') {
  console.error('Refusing to seed with NODE_ENV=production.');
  process.exit(1);
}

const PASSWORD = 'beacon-demo-password';
const USERS: { email: string; name: string; role: Role }[] = [
  { email: 'demo@beacon.test', name: 'Demo User', role: 'owner' },
  { email: 'member@beacon.test', name: 'Mia Member', role: 'member' },
];

// `failEvery`: 1 = always fails, 0 = never, n = every nth check fails.
const MONITORS = [
  { name: 'Example homepage', url: 'https://example.com', intervalSeconds: 300, failEvery: 0 },
  { name: 'checkout-api', url: 'https://checkout.example.com/health', intervalSeconds: 60, failEvery: 40 },
  { name: 'billing-api', url: 'https://billing.example.com/health', intervalSeconds: 60, failEvery: 0 },
  { name: 'Beacon itself', url: 'http://localhost:3000', intervalSeconds: 60, failEvery: 0 },
  { name: 'Always broken (for testing incidents)', url: 'http://localhost:59999/nothing-listens-here', intervalSeconds: 60, failEvery: 1 },
];

const CHECKS_PER_MONITOR = 288; // one every 5 minutes for 24 hours

// 1. Users, each with a "credential" login method holding an argon2id hash
//    (the same rows Better Auth writes on sign-up, lesson 1.1).
const users: Record<string, string> = {};
for (const u of USERS) {
  await db.insert(schema.users).values({ name: u.name, email: u.email, emailVerified: true }).onConflictDoNothing();
  const [user] = await db.select().from(schema.users).where(eq(schema.users.email, u.email));
  const [login] = await db
    .select()
    .from(schema.accounts)
    .where(and(eq(schema.accounts.userId, user.id), eq(schema.accounts.providerId, 'credential')));
  if (!login) {
    await db.insert(schema.accounts).values({ userId: user.id, providerId: 'credential', accountId: user.id, password: await hashPassword(PASSWORD) });
  }
  users[u.email] = user.id;
}

// 2. The organization and its memberships (lesson 1.2).
await db.insert(schema.organizations).values({ name: 'Demo', slug: 'demo' }).onConflictDoNothing();
const [org] = await db.select().from(schema.organizations).where(eq(schema.organizations.slug, 'demo'));
for (const u of USERS) {
  await db.insert(schema.memberships).values({ organizationId: org.id, userId: users[u.email], role: u.role }).onConflictDoNothing();
}

// 3. Monitors, then a day of check results for any monitor that has none yet.
//    A seed script is an admin tool that connects as the database owner, so it
//    writes tenant tables directly and sets organization_id itself.
const ownerId = users['demo@beacon.test'];
let createdMonitors = 0;
let createdChecks = 0;
for (const spec of MONITORS) {
  const { failEvery, ...fields } = spec;
  let [monitor] = await db
    .select()
    .from(schema.monitors)
    .where(and(eq(schema.monitors.organizationId, org.id), eq(schema.monitors.name, spec.name)));
  if (!monitor) {
    [monitor] = await db.insert(schema.monitors).values({ ...fields, organizationId: org.id, createdBy: ownerId }).returning();
    createdMonitors++;
  }

  const [{ n }] = await db.select({ n: count() }).from(schema.checkResults).where(eq(schema.checkResults.monitorId, monitor.id));
  if (n > 0) continue;
  const now = Date.now();
  const rows = Array.from({ length: CHECKS_PER_MONITOR }, (_, i) => {
    const ok = failEvery === 0 ? true : failEvery === 1 ? false : i % failEvery !== 0;
    return {
      organizationId: org.id,
      monitorId: monitor.id,
      checkedAt: new Date(now - (i + 1) * 5 * 60_000),
      ok,
      statusCode: ok ? 200 : failEvery === 1 ? null : 503,
      latencyMs: ok ? 80 + ((i * 37) % 120) : null,
      error: ok ? null : failEvery === 1 ? 'connect ECONNREFUSED 127.0.0.1:59999' : 'HTTP 503',
    };
  });
  await db.insert(schema.checkResults).values(rows);
  createdChecks += rows.length;

  if (failEvery === 1) {
    await db.insert(schema.incidents).values({
      organizationId: org.id,
      monitorId: monitor.id,
      openedAt: new Date(now - CHECKS_PER_MONITOR * 5 * 60_000),
      cause: 'connect ECONNREFUSED 127.0.0.1:59999',
    });
  }
}

console.log(
  createdMonitors || createdChecks
    ? `✓ seeded org "demo": ${createdMonitors} monitor(s), ${createdChecks} check result(s)`
    : '• seed data already present, nothing to do',
);
console.log(`  Sign in as ${USERS.map((u) => `${u.email} (${u.role})`).join(' or ')}, password ${PASSWORD}`);
await sql.end();
