/**
 * Lesson 5.1: the background worker. Runs the job queues (checks, incident
 * notifications, emails, SMS, Slack, thumbnails, usage reporting) and the
 * recurring schedule (the check scheduler every minute, usage every 5).
 *
 *   npm run worker
 *
 * Run it next to the web app, in its own process (in production: its own
 * container). Several can run at once; they share the work. Ctrl+C (SIGINT)
 * or SIGTERM from the platform stops it gracefully: running jobs get up to
 * 20 seconds to finish, and whatever does not finish is retried by the next
 * worker (queues deliver at least once, which is why every handler is
 * idempotent).
 *
 * Module 7: the configuration is checked first (lesson 7.4), then traces,
 * metrics and error tracking start (lesson 7.2). Every log line is JSON.
 */
import './load-env'; // lesson 7.4: .env.local, like Next.js (must be the first import)
import { validateEnvOrExit } from '../src/lib/env';

process.env.OTEL_SERVICE_NAME ??= 'beacon-worker';
validateEnvOrExit('beacon-worker');

const { initTelemetry, shutdownTelemetry } = await import('../src/lib/observability/telemetry');
const { initErrorTracking, flushErrors } = await import('../src/lib/observability/errors');
const { logger } = await import('../src/lib/observability/logger');
initTelemetry('beacon-worker');
await initErrorTracking('beacon-worker');

const { sql } = await import('../src/db');
const { stopBoss } = await import('../src/lib/queue');
const { startWorkers, WORKERS } = await import('../src/lib/queue/worker');

await startWorkers();
logger.info({ queues: Object.keys(WORKERS), release: process.env.APP_RELEASE ?? 'dev' }, 'worker.started');

let stopping = false;
for (const signal of ['SIGINT', 'SIGTERM'] as const) {
  process.on(signal, async () => {
    if (stopping) return;
    stopping = true;
    logger.info({ signal }, 'worker.stopping'); // finishing running jobs…
    await stopBoss();
    await Promise.allSettled([shutdownTelemetry(), flushErrors()]);
    await sql.end();
    process.exit(0);
  });
}
