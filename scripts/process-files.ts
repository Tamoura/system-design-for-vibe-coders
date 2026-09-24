/**
 * Lesson 2.2 (🟡): finish uploads whose background job never ran (the server
 * restarted between "processing" and "ready"). Run it by hand or from cron:
 *
 *   npm run files:process
 *
 * TODO(5.1): a durable job queue with retries makes this unnecessary.
 * Lesson 2.4: like the check runner, it visits one organization at a time and
 * every query runs inside withOrg().
 */
import { db, schema, sql } from '../src/db';
import { listProcessingFileIds, processUploadedFile } from '../src/lib/files';

const orgs = await db.select({ id: schema.organizations.id }).from(schema.organizations);
let processed = 0;
for (const { id: orgId } of orgs) {
  for (const fileId of await listProcessingFileIds({ orgId })) {
    await processUploadedFile({ orgId }, fileId);
    processed++;
  }
}
console.log(`✓ processed ${processed} file(s)`);
await sql.end();
