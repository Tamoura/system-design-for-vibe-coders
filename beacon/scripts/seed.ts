import { db, schema, sql } from '../src/db';

// Idempotent-ish seed for local development: only seeds an empty table.
const existing = await db.select().from(schema.monitors).limit(1);
if (existing.length === 0) {
  await db.insert(schema.monitors).values([
    { name: 'Example homepage', url: 'https://example.com', intervalSeconds: 300 },
    { name: 'Beacon itself', url: 'http://localhost:3000', intervalSeconds: 60 },
    { name: 'Always broken (for testing incidents)', url: 'http://localhost:59999/nothing-listens-here', intervalSeconds: 60 },
  ]);
  console.log('✓ seeded 3 monitors');
} else {
  console.log('• monitors already exist, skipping seed');
}
await sql.end();
