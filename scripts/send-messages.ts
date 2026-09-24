/**
 * Lesson 4.1 (🟡): the safety net for queued mail. Every sendEmail() already
 * nudges the worker after its response; this sends whatever is still due:
 * retries after a provider outage, rows left behind by a crash or a deploy.
 * Run it from cron every minute:
 *
 *   npm run messages:send
 *
 * TODO(5.1): a real job queue with a scheduler replaces this loop.
 */
import { sql } from '../src/db';
import { deliverPendingEmails } from '../src/lib/email';

let total = { sent: 0, suppressed: 0, retrying: 0, failed: 0 };
for (;;) {
  const batch = await deliverPendingEmails({ limit: 100 });
  total = { sent: total.sent + batch.sent, suppressed: total.suppressed + batch.suppressed, retrying: total.retrying + batch.retrying, failed: total.failed + batch.failed };
  if (batch.sent + batch.suppressed + batch.retrying + batch.failed < 100) break;
}
console.log(`emails: ${total.sent} sent, ${total.suppressed} suppressed, ${total.retrying} to retry later, ${total.failed} failed for good`);
await sql.end();
