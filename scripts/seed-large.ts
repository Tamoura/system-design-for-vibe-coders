/**
 * Lesson 2.1 (🟡) and 2.3 (🟢): a big organization to measure queries against.
 *
 *   npm run db:seed:large                                  # 500 monitors × 1,000 checks
 *   npm run db:seed:large -- --monitors=50000 --checks=0   # for the search exercise
 *
 * It (re)creates an organization "Big" (slug "big") owned by demo@beacon.test
 * when that user exists (run `npm run db:seed` first), deleting the previous
 * "big" org and everything in it. Rows are generated inside Postgres with
 * generate_series, which is far faster than sending them from Node.
 */
import './load-env'; // lesson 7.4: .env.local, like Next.js (must be the first import)
import postgres from 'postgres';

const arg = (name: string, fallback: number) => {
  const hit = process.argv.find((a) => a.startsWith(`--${name}=`));
  return hit ? Number(hit.split('=')[1]) : fallback;
};
const MONITORS = arg('monitors', 500);
const CHECKS = arg('checks', 1000);

const SERVICES = [
  'checkout', 'billing', 'search', 'auth', 'images', 'reports', 'webhooks', 'status', 'payments', 'invoices',
  'accounts', 'signup', 'login', 'profile', 'settings', 'exports', 'imports', 'mailer', 'notifier', 'scheduler',
  'gateway', 'catalog', 'inventory', 'orders', 'shipping', 'tracking', 'reviews', 'ratings', 'analytics', 'metrics',
  'logging', 'tracing', 'uploads', 'thumbnails', 'videos', 'chat', 'presence', 'feeds', 'comments', 'admin',
];

const url = process.env.DATABASE_URL ?? 'postgres://beacon:beacon@localhost:5432/beacon';
const sql = postgres(url, { max: 1, onnotice: () => {} });
const started = Date.now();

await sql.begin(async (tx) => {
  await tx`DELETE FROM organizations WHERE slug = 'big'`; // cascades to its monitors and checks
  // Lesson 3.2: on Business (500 monitors, 30-second checks), set directly
  // like an admin comping a plan. It has no Stripe customer, so no webhook
  // will ever recompute it. (With --monitors above 500 it is over the limit:
  // it can add nothing, but this org is for measuring queries.)
  const [org] = await tx`INSERT INTO organizations (name, slug, plan) VALUES ('Big', 'big', 'business') RETURNING id`;
  await tx`
    INSERT INTO memberships (organization_id, user_id, role)
    SELECT ${org.id}, id, 'owner' FROM users WHERE email = 'demo@beacon.test'`;

  // Names like "checkout-api-eu-west-prod-123": realistic material for the
  // trigram search of lesson 2.3. 40 services, so one service is 2.5% of
  // the rows, a selective search the trigram index is built for.
  await tx`
    INSERT INTO monitors (organization_id, name, url, interval_seconds, created_at)
    SELECT ${org.id},
           (${SERVICES}::text[])[1 + i % ${SERVICES.length}]
             || '-' || (ARRAY['api','web','worker'])[1 + i % 3]
             || '-' || (ARRAY['eu-west','us-east','ap-south'])[1 + i % 3]
             || '-' || (ARRAY['prod','staging'])[1 + i % 2] || '-' || i,
           'https://' || (${SERVICES}::text[])[1 + i % ${SERVICES.length}]
             || '-' || i || '.example.com/health',
           60,
           now() - make_interval(secs => i)
    FROM generate_series(1, ${MONITORS}) AS i`;

  // One check per minute going back from now, about 2% of them failing.
  if (CHECKS > 0) {
    await tx`
      INSERT INTO check_results (organization_id, monitor_id, checked_at, ok, status_code, latency_ms)
      SELECT m.organization_id, m.id, now() - make_interval(mins => n),
             (n + abs(hashtext(m.id::text))) % 50 <> 0,
             CASE WHEN (n + abs(hashtext(m.id::text))) % 50 <> 0 THEN 200 ELSE 503 END,
             50 + (n * 7) % 200
      FROM monitors m, generate_series(1, ${CHECKS}) AS n
      WHERE m.organization_id = ${org.id}`;
  }
});
// Fresh statistics, so the planner knows how big the tables are now, and a
// VACUUM so the visibility map is set and index-only scans skip the table
// (autovacuum does both on its own a little later).
await sql`VACUUM ANALYZE monitors`;
await sql`VACUUM ANALYZE check_results`;
await sql.end();
console.log(`✓ org "big": ${MONITORS} monitors × ${CHECKS} checks in ${((Date.now() - started) / 1000).toFixed(1)}s. Open /big/monitors as demo@beacon.test.`);
