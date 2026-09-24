/**
 * Lessons 4.1 and 4.2 (🟡): the safety net for queued messages. Every
 * sendEmail() and notify() already nudges its worker after the response;
 * this sends whatever is still due: retries after a provider outage, rows
 * left behind by a crash or a deploy. Notifications first (they can queue
 * more work, e.g. an SMS usage alert), then the email outbox.
 * Run it from cron every minute:
 *
 *   npm run messages:send
 *
 * TODO(5.1): a real job queue with a scheduler replaces this loop.
 */
import { sql } from '../src/db';
import { deliverPendingEmails } from '../src/lib/email';
import { deliverPendingNotifications } from '../src/lib/notifications';

const notified = await deliverPendingNotifications();
console.log(
  `notifications: ${notified.sent} sent, ${notified.throttled} SMS throttled, ${notified.suppressed} suppressed, ${notified.skipped} skipped, ${notified.retrying} to retry later, ${notified.failed} failed for good`,
);

let total = { sent: 0, suppressed: 0, retrying: 0, failed: 0 };
for (;;) {
  const batch = await deliverPendingEmails({ limit: 100 });
  total = { sent: total.sent + batch.sent, suppressed: total.suppressed + batch.suppressed, retrying: total.retrying + batch.retrying, failed: total.failed + batch.failed };
  if (batch.sent + batch.suppressed + batch.retrying + batch.failed < 100) break;
}
console.log(`emails: ${total.sent} sent, ${total.suppressed} suppressed, ${total.retrying} to retry later, ${total.failed} failed for good`);
await sql.end();
