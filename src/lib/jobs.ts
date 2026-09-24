import { after } from 'next/server';
import { processUploadedFile } from './files';

/**
 * Background work, until lesson 5.1 brings a real queue.
 *
 * `after()` runs the job once the response has been sent, in the same
 * process: the user does not wait for it, but a crash or a deploy loses it.
 * `npm run files:process` picks up anything left in "processing".
 * TODO(5.1): a durable queue with retries replaces both.
 *
 * Lesson 2.4: every job payload names its organization, and the job runs its
 * queries inside withOrg(orgId), exactly like a request.
 */
export type Job = { type: 'file.thumbnail'; orgId: string; fileId: string };

export function enqueue(job: Job): void {
  after(() => runJob(job));
}

/**
 * Lesson 4.1 (🟡): run a queue's worker once the response has been sent.
 * The queue itself is a table (email_outbox, notification_deliveries), so
 * this is only a nudge: if the process dies, the rows are still there and
 * `npm run messages:send` (cron) sends them.
 *
 * Outside a request (the check runner, a test) `after()` is not available;
 * those callers run the worker themselves when they are done.
 */
export function runAfterResponse(work: () => Promise<unknown>): void {
  try {
    after(async () => {
      try {
        await work();
      } catch (err) {
        console.error('background work failed (the queue keeps it for the next run):', err);
      }
    });
  } catch {
    // Not in a request scope: nothing to schedule on.
  }
}

export async function runJob(job: Job): Promise<void> {
  switch (job.type) {
    case 'file.thumbnail':
      await processUploadedFile({ orgId: job.orgId }, job.fileId);
      return;
  }
}
