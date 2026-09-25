/**
 * Check monitors now, instead of waiting for their next slot (lesson 5.1).
 *
 *   npm run checks:run            monitors that are due (never checked, or their interval has passed)
 *   npm run checks:run -- --all   every running monitor
 *
 * Since Module 5 this only ENQUEUES `check.run` jobs: the worker
 * (`npm run worker`) runs them, and it also checks every monitor on schedule
 * by itself, so you rarely need this. Before Module 5 this script was the
 * whole scheduler, run from cron.
 */
import './load-env'; // lesson 7.4: .env.local, like Next.js (must be the first import)
import { sql } from '../src/db';
import { stopBoss } from '../src/lib/queue';
import { enqueueChecksNow } from '../src/lib/scheduler';

const all = process.argv.includes('--all');
const { enqueued } = await enqueueChecksNow({ all });
console.log(`Enqueued ${enqueued} check(s)${all ? '' : ' (only monitors that are due; --all checks every running monitor)'}. The worker runs them: npm run worker`);
await stopBoss();
await sql.end();
