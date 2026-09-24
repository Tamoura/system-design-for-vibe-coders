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

export async function runJob(job: Job): Promise<void> {
  switch (job.type) {
    case 'file.thumbnail':
      await processUploadedFile({ orgId: job.orgId }, job.fileId);
      return;
  }
}
