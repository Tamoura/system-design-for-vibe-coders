/**
 * Lesson 5.1: a small queue dashboard in the terminal.
 *
 *   npm run jobs                       depth, age of the oldest waiting job, failures,
 *                                      jobs waiting to be retried, the dead-letter queue
 *   npm run jobs -- redrive [queue]    move dead-lettered jobs back to their queue
 *   npm run jobs -- run                run every due job once, in this process (no worker needed)
 *
 * pg-boss also has a web dashboard (@pg-boss/dashboard). Like any queue
 * dashboard it shows every org's job payloads, so it belongs behind admin
 * authentication (lesson 7.1), never on the public internet.
 */
import { sql } from '../src/db';
import { stopBoss } from '../src/lib/queue';
import { runQueuedJobs } from '../src/lib/queue/run';
import { queueStatus, redriveDeadLetters } from '../src/lib/queue/status';

const [command, arg] = process.argv.slice(2);

if (command === 'redrive') {
  console.log(`Moved ${await redriveDeadLetters(arg)} dead-lettered job(s) back to ${arg ?? 'their queues'}.`);
} else if (command === 'run') {
  console.log(await runQueuedJobs());
} else {
  const { queues, retrying, dead } = await queueStatus();
  console.log('queue                  waiting  deferred  active  failed  oldest waiting');
  for (const q of queues) {
    const age = q.oldestWaitingSec === null ? '-' : `${q.oldestWaitingSec}s`;
    console.log(`${q.queue.padEnd(22)} ${String(q.waiting).padStart(7)} ${String(q.deferred).padStart(9)} ${String(q.active).padStart(7)} ${String(q.failed).padStart(7)}  ${age}`);
  }
  console.log(`\nWaiting to be retried (${retrying.length}):`);
  for (const j of retrying) {
    console.log(`  ${j.queue} ${j.id}: attempt ${j.attempt} of ${j.of} failed, next at ${j.nextAttemptAt.toISOString()} (${j.error ?? 'no error message'}) ${JSON.stringify(j.data)}`);
  }
  console.log(`\nDead letters (${dead.length}):`);
  for (const j of dead) {
    console.log(`  from ${j.sourceQueue} at ${j.deadAt.toISOString()}: ${j.error ?? 'no error message'} ${JSON.stringify(j.data)}`);
  }
}
await stopBoss();
await sql.end();
