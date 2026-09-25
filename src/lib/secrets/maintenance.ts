import { and, eq, isNotNull } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import type { AuditSource } from '@/core/audit';
import { recordAudit, SYSTEM_SOURCE } from '../audit';
import { encryptSecret, keyIdOf, rewrapSecret, secretContext } from './index';
import { getKms, type Kms } from './kms';

const { organizations, webhookEndpoints } = schema;

/*
 * Lesson 8.1 (🟡): the two maintenance jobs of application-level encryption.
 *
 *   encryptLegacySecrets()  Module 7 → 8: encrypt the plaintext webhook secrets and
 *                           Slack URLs and empty the old columns. Run by
 *                           `npm run db:migrate` after the SQL migrations. Idempotent.
 *   rewrapAllSecrets()      KEK rotation: re-wrap every data key with the current KEK
 *                           (`npm run secrets -- rotate`). The ciphertext is untouched.
 *
 * Both run as a platform maintenance task, org by org, each org's rows inside
 * withOrg() (row-level security still applies). Every write is compare-and-set
 * (WHERE the column still holds what we read), so running them twice, or
 * while the app is serving traffic, never loses a concurrent change.
 */

type Counts = { webhookSecrets: number; slackUrls: number };

async function allOrgIds(): Promise<string[]> {
  return (await db.select({ id: organizations.id }).from(organizations)).map((o) => o.id);
}

export async function encryptLegacySecrets(opts: { kms?: Kms; source?: AuditSource } = {}): Promise<Counts> {
  const kms = opts.kms ?? getKms();
  const counts: Counts = { webhookSecrets: 0, slackUrls: 0 };

  // Slack URLs live on the organization row itself (the tenant, not a tenant table).
  const orgs = await db.select({ id: organizations.id, url: organizations.legacySlackWebhookUrl }).from(organizations).where(isNotNull(organizations.legacySlackWebhookUrl));
  for (const org of orgs) {
    const encrypted = await encryptSecret(org.url!, secretContext('organizations.slack_webhook_url', org.id), kms);
    const done = await db
      .update(organizations)
      .set({ slackWebhookUrlEncrypted: encrypted, legacySlackWebhookUrl: null })
      .where(and(eq(organizations.id, org.id), eq(organizations.legacySlackWebhookUrl, org.url!)))
      .returning({ id: organizations.id });
    counts.slackUrls += done.length;
  }

  for (const orgId of await allOrgIds()) {
    const rows = await withOrg(orgId, (tx) =>
      tx
        .select({ id: webhookEndpoints.id, secret: webhookEndpoints.legacySecret })
        .from(webhookEndpoints)
        .where(and(eq(webhookEndpoints.organizationId, orgId), isNotNull(webhookEndpoints.legacySecret))),
    );
    if (!rows.length) continue;
    const encrypted = await Promise.all(rows.map(async (r) => ({ ...r, value: await encryptSecret(r.secret!, secretContext('webhook_endpoints.secret', orgId), kms) })));
    counts.webhookSecrets += await withOrg(orgId, async (tx) => {
      let n = 0;
      for (const r of encrypted) {
        const done = await tx
          .update(webhookEndpoints)
          .set({ secretEncrypted: r.value, legacySecret: null })
          .where(and(eq(webhookEndpoints.organizationId, orgId), eq(webhookEndpoints.id, r.id), eq(webhookEndpoints.legacySecret, r.secret!)))
          .returning({ id: webhookEndpoints.id });
        n += done.length;
      }
      return n;
    });
  }

  if (counts.webhookSecrets + counts.slackUrls > 0) {
    await db.transaction((tx) =>
      recordAudit(tx, { orgId: null, action: 'secrets.encrypted', source: opts.source ?? SYSTEM_SOURCE, metadata: { webhook_secrets: counts.webhookSecrets, slack_urls: counts.slackUrls, kek: kms.currentKeyId } }),
    );
  }
  return counts;
}

export async function rewrapAllSecrets(opts: { kms?: Kms; source?: AuditSource } = {}): Promise<Counts & { toKey: string }> {
  const kms = opts.kms ?? getKms();
  const counts: Counts = { webhookSecrets: 0, slackUrls: 0 };

  const orgs = await db.select({ id: organizations.id, value: organizations.slackWebhookUrlEncrypted }).from(organizations).where(isNotNull(organizations.slackWebhookUrlEncrypted));
  for (const org of orgs) {
    const rewrapped = await rewrapSecret(org.value!, kms);
    if (!rewrapped) continue;
    const done = await db
      .update(organizations)
      .set({ slackWebhookUrlEncrypted: rewrapped })
      .where(and(eq(organizations.id, org.id), eq(organizations.slackWebhookUrlEncrypted, org.value!)))
      .returning({ id: organizations.id });
    counts.slackUrls += done.length;
  }

  for (const orgId of await allOrgIds()) {
    const rows = await withOrg(orgId, (tx) =>
      tx
        .select({ id: webhookEndpoints.id, value: webhookEndpoints.secretEncrypted })
        .from(webhookEndpoints)
        .where(and(eq(webhookEndpoints.organizationId, orgId), isNotNull(webhookEndpoints.secretEncrypted))),
    );
    const changed = (await Promise.all(rows.map(async (r) => ({ ...r, next: await rewrapSecret(r.value!, kms) })))).filter((r) => r.next);
    if (!changed.length) continue;
    counts.webhookSecrets += await withOrg(orgId, async (tx) => {
      let n = 0;
      for (const r of changed) {
        const done = await tx
          .update(webhookEndpoints)
          .set({ secretEncrypted: r.next })
          .where(and(eq(webhookEndpoints.organizationId, orgId), eq(webhookEndpoints.id, r.id), eq(webhookEndpoints.secretEncrypted, r.value!)))
          .returning({ id: webhookEndpoints.id });
        n += done.length;
      }
      return n;
    });
  }

  await db.transaction((tx) =>
    recordAudit(tx, { orgId: null, action: 'secrets.rewrapped', source: opts.source ?? SYSTEM_SOURCE, metadata: { webhook_secrets: counts.webhookSecrets, slack_urls: counts.slackUrls, kek: kms.currentKeyId } }),
  );
  return { ...counts, toKey: kms.currentKeyId };
}

/** How many stored secrets are wrapped with each KEK, and how many are still plaintext. */
export async function secretsStatus(): Promise<{ byKey: Record<string, number>; plaintext: number }> {
  const byKey: Record<string, number> = {};
  let plaintext = 0;
  const count = (value: string | null) => {
    if (!value) return;
    const id = keyIdOf(value) ?? '(not an envelope)';
    byKey[id] = (byKey[id] ?? 0) + 1;
  };
  for (const o of await db.select({ enc: organizations.slackWebhookUrlEncrypted, legacy: organizations.legacySlackWebhookUrl }).from(organizations)) {
    count(o.enc);
    if (o.legacy) plaintext++;
  }
  for (const orgId of await allOrgIds()) {
    const rows = await withOrg(orgId, (tx) =>
      tx.select({ enc: webhookEndpoints.secretEncrypted, legacy: webhookEndpoints.legacySecret }).from(webhookEndpoints).where(eq(webhookEndpoints.organizationId, orgId)),
    );
    for (const r of rows) {
      count(r.enc);
      if (r.legacy) plaintext++;
    }
  }
  return { byKey, plaintext };
}
