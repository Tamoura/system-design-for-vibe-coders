import { sendQueuedEmail } from '../email';
import { processUploadedFile } from '../files';
import { deliverNotification } from '../notifications/deliver';
import { notifyIncident } from '../notifications/incidents';
import { runScheduledCheck, scheduleChecks } from '../scheduler';
import { reportPendingUsage } from '../usage';
import type { JobContext, JobData, QueueName } from './queues';

/*
 * Lesson 5.1: which function runs each queue's jobs. The worker
 * (./worker.ts) and the tests (./run.ts) both look handlers up here.
 *
 * Every handler follows the lesson's rules:
 *  - it takes ids and re-reads the rows (a retry an hour later sees today's data);
 *  - it is idempotent: running it twice has the effect of running it once;
 *  - it THROWS to ask for a retry. Returning means done; the return value is
 *    stored on the job (`output`), which `npm run jobs` shows.
 */
type Handler<Q extends QueueName> = (data: JobData[Q], job: JobContext) => Promise<unknown>;

export const HANDLERS: { [Q in QueueName]?: Handler<Q> } = {
  'checks.schedule': () => scheduleChecks(),
  'check.run': (data) => runScheduledCheck(data),
  'incident.notify': (data) => notifyIncident(data),
  'notification.deliver': (data, job) => deliverNotification(data.orgId, data.deliveryId, job),
  'email.send': (data, job) => sendQueuedEmail(data.emailId, job),
  'file.process': (data) => processUploadedFile({ orgId: data.orgId }, data.fileId),
  'usage.report': () => reportPendingUsage(),
};

export function handlerFor<Q extends QueueName>(queue: Q): Handler<Q> | undefined {
  return HANDLERS[queue] as Handler<Q> | undefined;
}
