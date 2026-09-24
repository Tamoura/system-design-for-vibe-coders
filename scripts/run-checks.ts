/**
 * Check every monitor that is due, store the results, open or resolve
 * incidents, and notify. Run it from cron every minute, or by hand:
 *
 *   npm run checks:run            only monitors whose interval has passed
 *   npm run checks:run -- --all   every running monitor now (for trying things out)
 *
 * The work itself is in src/lib/checks.ts (lesson 4.2 moved it there so the
 * tests can drive it, flapping included). Lesson 3.2: paused monitors never
 * run, and a monitor is due only when its interval, raised to the plan's
 * minimum, has passed. Lesson 2.4: every org is worked on inside withOrg().
 *
 * Lesson 4.2: opening or resolving an incident writes notifications in the
 * same transaction. This script is not a web request, so nothing sends them
 * "after the response": it runs the channel workers itself before exiting
 * (email, SMS through the provider and recordSmsSent() from lesson 3.3,
 * Slack). Whatever fails is retried by `npm run messages:send`.
 *
 * TODO(5.1): this is a loop in a script. It has no schedule per monitor, no
 * retries, no concurrency limit per tenant and no protection against two copies
 * running at once. Lesson 5.1 turns it into a proper scheduler + worker queue.
 */
import { sql } from '../src/db';
import { runChecks } from '../src/lib/checks';
import { deliverPendingEmails } from '../src/lib/email';
import { deliverPendingNotifications } from '../src/lib/notifications';

const checkAll = process.argv.includes('--all');
const { lines, orgIds } = await runChecks({ all: checkAll });
for (const line of lines) console.log(line);
console.log(`Checked ${lines.length} monitor(s)${checkAll ? '' : ' (only those due; --all checks every running monitor)'}.`);

const sent = { sent: 0, throttled: 0, suppressed: 0, retrying: 0 };
for (const orgId of orgIds) {
  const r = await deliverPendingNotifications({ orgId });
  sent.sent += r.sent;
  sent.throttled += r.throttled;
  sent.suppressed += r.suppressed;
  sent.retrying += r.retrying;
}
await deliverPendingEmails();
if (sent.sent + sent.throttled + sent.suppressed + sent.retrying > 0) {
  console.log(`Notifications: ${sent.sent} sent, ${sent.throttled} SMS throttled, ${sent.suppressed} suppressed, ${sent.retrying} to retry.`);
}
await sql.end();
