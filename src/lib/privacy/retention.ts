import { and, inArray, isNull, lt, ne } from 'drizzle-orm';
import { db, schema } from '@/db';
import { RETENTION_RULES, retentionCutoff } from '@/core/retention';
import { SYSTEM_SOURCE } from '../audit';
import { recordPlatformAudit } from '../admin/audit';
import { getStorage } from '../storage';

const { checkResults, webhookEvents, notifications, notificationDeliveries, emailOutbox, orgExports } = schema;

/*
 * Lesson 8.1: "decide how long you keep it, write it down, and enforce it
 * with jobs". The nightly `retention.purge` job deletes what src/core/retention.ts
 * says is past its time. Like the audit retention job (lesson 7.3) it is
 * platform housekeeping that runs as the database owner across every org,
 * never from a request (tests/tenant-scoping.test.ts lists it as exempt).
 *
 * Big tables are deleted in batches of 5,000 rows so one run never holds a
 * long lock or a huge transaction; what is left is picked up the next night.
 */
const BATCH = 5_000;
const MAX_BATCHES = 200; // at most a million rows per table per night

export async function purgeExpiredData(now = new Date()): Promise<Record<string, number>> {
  const deleted: Record<string, number> = {};

  const checkCutoff = retentionCutoff(RETENTION_RULES.checkResults.days, now);
  deleted.check_results = await inBatches(() =>
    db.delete(checkResults).where(inArray(checkResults.id, db.select({ id: checkResults.id }).from(checkResults).where(lt(checkResults.checkedAt, checkCutoff)).limit(BATCH))).returning({ id: checkResults.id }),
  );

  // Deleting an event cascades to its messages and their attempts (the delivery log).
  const hookCutoff = retentionCutoff(RETENTION_RULES.webhookDeliveries.days, now);
  deleted.webhook_events = await inBatches(() =>
    db.delete(webhookEvents).where(inArray(webhookEvents.id, db.select({ id: webhookEvents.id }).from(webhookEvents).where(lt(webhookEvents.createdAt, hookCutoff)).limit(BATCH))).returning({ id: webhookEvents.id }),
  );

  // Notifications cascade to their deliveries; Slack and subscriber deliveries have no notification row.
  const noteCutoff = retentionCutoff(RETENTION_RULES.notifications.days, now);
  deleted.notifications = await inBatches(() =>
    db.delete(notifications).where(inArray(notifications.id, db.select({ id: notifications.id }).from(notifications).where(lt(notifications.createdAt, noteCutoff)).limit(BATCH))).returning({ id: notifications.id }),
  );
  deleted.notification_deliveries = await inBatches(() =>
    db
      .delete(notificationDeliveries)
      .where(inArray(notificationDeliveries.id, db.select({ id: notificationDeliveries.id }).from(notificationDeliveries).where(and(isNull(notificationDeliveries.notificationId), lt(notificationDeliveries.createdAt, noteCutoff))).limit(BATCH)))
      .returning({ id: notificationDeliveries.id }),
  );

  // Never a pending email: that one is still in the queue.
  const mailCutoff = retentionCutoff(RETENTION_RULES.emailOutbox.days, now);
  deleted.email_outbox = await inBatches(() =>
    db.delete(emailOutbox).where(inArray(emailOutbox.id, db.select({ id: emailOutbox.id }).from(emailOutbox).where(and(ne(emailOutbox.status, 'pending'), lt(emailOutbox.createdAt, mailCutoff))).limit(BATCH))).returning({ id: emailOutbox.id }),
  );

  // Export files: the object first, then the row (a row without its file is harmless; the reverse is a leak).
  const expired = await db.select({ id: orgExports.id, key: orgExports.storageKey }).from(orgExports).where(lt(orgExports.expiresAt, now));
  for (const e of expired) if (e.key) await getStorage().delete(e.key);
  deleted.org_exports = expired.length ? (await db.delete(orgExports).where(inArray(orgExports.id, expired.map((e) => e.id))).returning({ id: orgExports.id })).length : 0;

  const total = Object.values(deleted).reduce((a, b) => a + b, 0);
  if (total > 0) await recordPlatformAudit({ action: 'retention.purged', source: SYSTEM_SOURCE, metadata: deleted });
  return deleted;
}

async function inBatches(deleteBatch: () => Promise<unknown[]>): Promise<number> {
  let total = 0;
  for (let i = 0; i < MAX_BATCHES; i++) {
    const n = (await deleteBatch()).length;
    total += n;
    if (n < BATCH) break;
  }
  return total;
}
