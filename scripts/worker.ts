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
 */
import { sql } from '../src/db';
import { stopBoss } from '../src/lib/queue';
import { startWorkers, WORKERS } from '../src/lib/queue/worker';

await startWorkers();
console.log(`Worker started: ${Object.keys(WORKERS).join(', ')}. Ctrl+C to stop.`);

let stopping = false;
for (const signal of ['SIGINT', 'SIGTERM'] as const) {
  process.on(signal, async () => {
    if (stopping) return;
    stopping = true;
    console.log(`${signal}: finishing running jobs…`);
    await stopBoss();
    await sql.end();
    process.exit(0);
  });
}
