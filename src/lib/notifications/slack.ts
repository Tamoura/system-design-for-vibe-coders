import { eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { decryptSecret, secretContext } from '../secrets';

/**
 * Lesson 8.1: the org's Slack incoming-webhook URL, decrypted. Server-side only
 * (the settings page shows its last 6 characters; the worker posts to it).
 */
export async function readSlackWebhookUrl(orgId: string): Promise<string | null> {
  const [org] = await db.select({ encrypted: schema.organizations.slackWebhookUrlEncrypted }).from(schema.organizations).where(eq(schema.organizations.id, orgId));
  return org?.encrypted ? decryptSecret(org.encrypted, secretContext('organizations.slack_webhook_url', orgId)) : null;
}
