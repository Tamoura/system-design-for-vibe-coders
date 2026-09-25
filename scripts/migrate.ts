/**
 * Lesson 7.4: migrations are a RELEASE step. They run once per deploy, before
 * the new code starts (a `migrate` one-shot container in
 * docker-compose.prod.yml, the release phase of a PaaS), never on every web
 * instance's boot. Every migration must keep the code that is still running
 * working (expand → migrate → contract, docs/deployment.md).
 */
import './load-env'; // lesson 7.4: .env.local, like Next.js (must be the first import)
import { drizzle } from 'drizzle-orm/postgres-js';
import { migrate } from 'drizzle-orm/postgres-js/migrator';
import postgres from 'postgres';
import { installQueues } from '../src/lib/queue/install';
import { validateEnvOrExit } from '../src/lib/env';
import { cliAuditSource } from '../src/lib/audit';
import { sql as appSql } from '../src/db';
import { encryptLegacySecrets } from '../src/lib/secrets/maintenance';

validateEnvOrExit('migrate');

/*
 * Lesson 2.1: a migration that waits for a lock (say, ALTER TABLE behind a
 * long-running query) makes every query after it wait too. lock_timeout makes
 * it fail fast instead; run it again when the database is quieter.
 */
const sql = postgres(process.env.DATABASE_URL ?? 'postgres://beacon:beacon@localhost:5432/beacon', {
  max: 1,
  onnotice: () => {},
  connection: { lock_timeout: 10_000 }, // milliseconds
});
await migrate(drizzle(sql), { migrationsFolder: './drizzle' });
await sql.end();
console.log('✓ migrations applied');

// Lesson 5.1: the job queue's own tables (schema `pgboss`, versioned by
// pg-boss itself), Beacon's queues and their retry settings, and what the
// app role may do with them. Safe to run again.
await installQueues({ connectionString: process.env.DATABASE_URL ?? 'postgres://beacon:beacon@localhost:5432/beacon', max: 2 });
console.log('✓ job queues ready');

// Lesson 8.1: the data half of migration 0025. Plaintext webhook secrets and Slack URLs from
// before Module 8 are encrypted with the current key and the plaintext columns emptied. SQL
// cannot do it (the key is not in the database), so it runs here, once per deploy, idempotent.
const encrypted = await encryptLegacySecrets({ source: cliAuditSource('db:migrate') });
if (encrypted.webhookSecrets + encrypted.slackUrls > 0) {
  console.log(`✓ encrypted ${encrypted.webhookSecrets} webhook secret(s) and ${encrypted.slackUrls} Slack URL(s) that were stored in plain text`);
}
await appSql.end();
