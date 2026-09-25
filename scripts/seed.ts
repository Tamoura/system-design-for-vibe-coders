/**
 * Local development data (lesson 2.1): one organization "Demo" (slug "demo")
 * with an owner and a member, five monitors, and a day of check results.
 *
 *   demo@beacon.test    owner    password: beacon-demo-password
 *   member@beacon.test  member   password: beacon-demo-password
 *
 * Lesson 7.1: and three Beacon STAFF accounts (same password, no customer
 * org of their own), one per staff role worth trying in the admin panel:
 *
 *   staff@beacon.test    superadmin   /internal: everything, including staff roles
 *   support@beacon.test  support      extend trials, resend emails, read-only impersonation
 *   billing@beacon.test  billing      comp plans, extend trials; no impersonation
 *
 * Idempotent: every row is looked up by a natural key (email, slug, monitor
 * name) before it is inserted, so running it twice changes nothing, and running
 * it after someone adds a monitor here fills in only what is missing.
 * `npm run db:reset` drops everything, migrates and runs this.
 *
 * Never run it against production: it creates users with a known password.
 */
import './load-env'; // lesson 7.4: .env.local, like Next.js (must be the first import)
import { and, count, eq } from 'drizzle-orm';
import { db, schema, sql } from '../src/db';
import { hashPassword } from '../src/lib/password';
import type { Role } from '../src/core/roles';
import type { StaffRole } from '../src/core/staff';

if (process.env.NODE_ENV === 'production') {
  console.error('Refusing to seed with NODE_ENV=production.');
  process.exit(1);
}

const PASSWORD = 'beacon-demo-password';
const USERS: { email: string; name: string; role: Role }[] = [
  { email: 'demo@beacon.test', name: 'Demo User', role: 'owner' },
  { email: 'member@beacon.test', name: 'Mia Member', role: 'member' },
];
const STAFF: { email: string; name: string; role: StaffRole }[] = [
  { email: 'staff@beacon.test', name: 'Sam Superadmin', role: 'superadmin' },
  { email: 'support@beacon.test', name: 'Sue Support', role: 'support' },
  { email: 'billing@beacon.test', name: 'Bill Billing', role: 'billing' },
];

// `failEvery`: 1 = always fails, 0 = never, n = every nth check fails.
// Lesson 3.2: "demo" is on Free, so five monitors at 5-minute intervals is
// exactly its limit: the monitors page shows "Upgrade to add more monitors".
const MONITORS = [
  { name: 'Example homepage', url: 'https://example.com', intervalSeconds: 300, failEvery: 0 },
  { name: 'checkout-api', url: 'https://checkout.example.com/health', intervalSeconds: 300, failEvery: 40 },
  { name: 'billing-api', url: 'https://billing.example.com/health', intervalSeconds: 300, failEvery: 0 },
  // Lesson 7.2: Beacon monitors itself, through its liveness endpoint (dogfooding). It needs a
  // second, OUTSIDE probe too: if Beacon is down, it cannot tell you (docs/operations.md).
  { name: 'Beacon itself', url: 'http://localhost:3000/api/health', intervalSeconds: 300, failEvery: 0 },
  { name: 'Always broken (for testing incidents)', url: 'http://localhost:59999/nothing-listens-here', intervalSeconds: 300, failEvery: 1 },
];

const CHECKS_PER_MONITOR = 288; // one every 5 minutes for 24 hours

// Past incidents with updates, so full-text search (lesson 2.3) has prose to
// find. Try '"certificate expired" -staging' in the Ctrl+K palette.
const PAST_INCIDENTS: Record<string, { hoursAgo: number; cause: string; updates: string[] }[]> = {
  'checkout-api': [
    {
      hoursAgo: 20,
      cause: 'HTTP 503',
      updates: [
        'Opened automatically: HTTP 503',
        'The TLS certificate expired on the checkout load balancer. Renewing it now.',
        'Certificate renewed and deployed; checkout is answering again.',
      ],
    },
  ],
  'billing-api': [
    {
      hoursAgo: 30,
      cause: 'HTTP 502',
      updates: ['Opened automatically: HTTP 502', 'Only staging is affected: the certificate expired on the staging proxy.', 'Staging certificate replaced.'],
    },
  ],
};

// 1. Users, each with a "credential" login method holding an argon2id hash
//    (the same rows Better Auth writes on sign-up, lesson 1.1).
const users: Record<string, string> = {};
for (const u of [...USERS, ...STAFF]) {
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

// 1b. Lesson 7.1: the staff rows. Staff are a separate table, not a customer role.
for (const s of STAFF) {
  await db.insert(schema.staffUsers).values({ userId: users[s.email], role: s.role }).onConflictDoNothing();
}

// 2. The organization and its memberships (lesson 1.2).
// Lesson 6.1: the demo's status page is published (new orgs start unpublished).
await db.insert(schema.organizations).values({ name: 'Demo', slug: 'demo', statusPagePublic: true }).onConflictDoNothing();
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

  const incidents = [...(PAST_INCIDENTS[spec.name] ?? [])];
  if (failEvery === 1) {
    const cause = 'connect ECONNREFUSED 127.0.0.1:59999';
    incidents.push({ hoursAgo: CHECKS_PER_MONITOR / 12, cause, updates: [`Opened automatically: ${cause}`] });
  }
  for (const past of incidents) {
    const openedAt = new Date(now - past.hoursAgo * 3600_000);
    const [incident] = await db
      .insert(schema.incidents)
      .values({
        organizationId: org.id,
        monitorId: monitor.id,
        openedAt,
        // Past incidents are resolved; the "always broken" one stays open.
        resolvedAt: failEvery === 1 ? null : new Date(openedAt.getTime() + 45 * 60_000),
        cause: past.cause,
      })
      .returning();
    await db.insert(schema.incidentUpdates).values(
      past.updates.map((body, i) => ({
        organizationId: org.id,
        incidentId: incident.id,
        authorId: i === 0 ? null : ownerId,
        body,
        createdAt: new Date(openedAt.getTime() + i * 15 * 60_000),
      })),
    );
  }
}

// 4. Lesson 6.1: the demo org has done most of its onboarding (monitors, checks,
//    a teammate, a published status page). "Connect an alert channel" is left,
//    so the Getting started checklist shows on the Monitors page.
const at = new Date(Date.now() - CHECKS_PER_MONITOR * 5 * 60_000);
for (const milestone of ['monitor_created', 'first_check', 'teammate_invited', 'status_page_published'] as const) {
  await db.insert(schema.orgMilestones).values({ organizationId: org.id, milestone, reachedAt: at, userId: ownerId }).onConflictDoNothing();
}

console.log(
  createdMonitors || createdChecks
    ? `✓ seeded org "demo": ${createdMonitors} monitor(s), ${createdChecks} check result(s)`
    : '• seed data already present, nothing to do',
);
console.log(`  Sign in as ${USERS.map((u) => `${u.email} (${u.role})`).join(' or ')}, password ${PASSWORD}`);
console.log(`  Beacon staff (/internal): ${STAFF.map((s) => `${s.email} (${s.role})`).join(', ')}`);
await sql.end();
