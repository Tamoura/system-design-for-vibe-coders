import http from 'node:http';
import type { AddressInfo } from 'node:net';
import { afterAll, afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));

import { eq } from 'drizzle-orm';
import { Webhook } from 'standardwebhooks';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { parseEnvelope } from '@/core/envelope';
import { generateWebhookSecret } from '@/core/webhooks';
import { decryptSecret, encryptSecret, secretContext } from '@/lib/secrets';
import { LocalKms, parseKeyring, setKmsForTests } from '@/lib/secrets/kms';
import { encryptLegacySecrets, rewrapAllSecrets, secretsStatus } from '@/lib/secrets/maintenance';
import { createEndpoint, deliverWebhook, recordWebhookEvent } from '@/lib/webhooks';
import { getOrgNotificationSettings, saveOrgNotificationSettings } from '@/lib/notifications';
import { readSlackWebhookUrl } from '@/lib/notifications/slack';
import { makeOrg } from './helpers/fixtures';

/*
 * Lesson 8.1 (🟡): application-level envelope encryption of the secrets Beacon
 * must read back. "A raw SELECT shows only ciphertext and a wrapped DEK";
 * "rotating the KEK re-wraps DEKs without re-encrypting data or downtime".
 */
const key = (id: string, fill: number) => `${id}:${Buffer.alloc(32, fill).toString('base64')}`;
const kmsWith = (...keys: string[]) => new LocalKms(parseKeyring(keys.join(',')));
const k1 = key('k1', 1);
const k2 = key('k2', 2);

let server: http.Server;
let base = '';
const received: { headers: http.IncomingHttpHeaders; body: string }[] = [];

beforeAll(async () => {
  setKmsForTests(kmsWith(k1));
  server = http.createServer((req, res) => {
    let body = '';
    req.on('data', (c) => (body += c));
    req.on('end', () => {
      received.push({ headers: req.headers, body });
      res.end('ok');
    });
  });
  await new Promise<void>((r) => server.listen(0, '127.0.0.1', r));
  const port = (server.address() as AddressInfo).port;
  base = `http://127.0.0.1:${port}`;
  vi.stubEnv('OUTBOUND_ALLOWLIST', `127.0.0.1:${port}`);
});
afterAll(async () => {
  setKmsForTests(undefined);
  vi.unstubAllEnvs();
  await new Promise<void>((r) => server.close(() => r()));
});
afterEach(() => setKmsForTests(kmsWith(k1)));

describe('encryptSecret / decryptSecret', () => {
  const ctx = secretContext('webhook_endpoints.secret', '00000000-0000-4000-8000-000000000001');

  it('round-trips, and the same secret never encrypts to the same string twice (fresh DEK and IV)', async () => {
    const a = await encryptSecret('whsec_abc', ctx);
    const b = await encryptSecret('whsec_abc', ctx);
    expect(a).toMatch(/^enc:v1:k1:[\w-]+:[\w-]+:[\w-]+$/);
    expect(a).not.toBe(b);
    expect(a).not.toContain('whsec_abc');
    expect(await decryptSecret(a, ctx)).toBe('whsec_abc');
  });

  it('refuses a tampered ciphertext, another context (org or column), or a key that is not in the keyring', async () => {
    const stored = await encryptSecret('whsec_abc', ctx);
    const e = parseEnvelope(stored);
    const flipped = stored.replace(/:([\w-]+)$/, (_m, ct: string) => `:${Buffer.from(Buffer.from(ct, 'base64url').map((b, i) => (i === 0 ? b ^ 1 : b))).toString('base64url')}`);
    await expect(decryptSecret(flipped, ctx)).rejects.toThrow();
    // Copied into another org's row: the context (AES-GCM additional data) does not match.
    await expect(decryptSecret(stored, secretContext('webhook_endpoints.secret', '00000000-0000-4000-8000-000000000002'))).rejects.toThrow();
    await expect(decryptSecret(stored, secretContext('organizations.slack_webhook_url', '00000000-0000-4000-8000-000000000001'))).rejects.toThrow();
    await expect(decryptSecret(stored, ctx, kmsWith(k2))).rejects.toThrow(/"k1" is not in ENCRYPTION_KEYS/);
    expect(e.kekId).toBe('k1');
  });

  it('parses the keyring strictly', () => {
    expect(() => parseKeyring('k1:short')).toThrow(/32 bytes/);
    expect(() => parseKeyring(`${k1},${k1}`)).toThrow(/duplicate/);
    expect(() => parseKeyring('BAD ID:x')).toThrow(/key id/);
    expect(kmsWith(k2, k1).currentKeyId).toBe('k2');
    expect(kmsWith(k2, 'dev').keyIds).toEqual(['k2', 'dev']); // leaving the development key behind
  });
});

describe('webhook secrets at rest', () => {
  it('a raw SELECT shows only the envelope (a wrapped DEK and ciphertext), and deliveries are still signed correctly', async () => {
    const org = await makeOrg('Enc');
    const { id, secret } = await createEndpoint({ orgId: org.id, userId: org.users.owner.id }, { url: `${base}/hook`, eventTypes: ['incident.opened'] });
    const [raw] = await db.select().from(schema.webhookEndpoints).where(eq(schema.webhookEndpoints.id, id));
    expect(raw.legacySecret).toBeNull();
    expect(raw.secretEncrypted).toMatch(/^enc:v1:k1:/);
    expect(JSON.stringify(raw)).not.toContain(secret);
    expect(JSON.stringify(raw)).not.toContain(secret.slice(6, 20));

    const delivered = await deliverOne(org.id);
    expect(new Webhook(secret).verify(delivered.body, delivered.headers as Record<string, string>)).toMatchObject({ type: 'incident.opened' });
  });
});

describe('key rotation (npm run secrets -- rotate)', () => {
  it('re-wraps every DEK with the new key and leaves the ciphertext alone; the old key can then go', async () => {
    const org = await makeOrg('Rotate');
    const { id, secret } = await createEndpoint({ orgId: org.id, userId: org.users.owner.id }, { url: `${base}/hook`, eventTypes: ['incident.opened'] });
    await saveOrgNotificationSettings({ orgId: org.id }, { allowed: new Set(), slackWebhookUrl: 'https://hooks.slack.com/services/T0/B0/rotate-me' });
    const before = parseEnvelope((await endpointRow(id)).secretEncrypted!);

    setKmsForTests(kmsWith(k2, k1)); // step 1: k2 in front, k1 kept
    const result = await rewrapAllSecrets();
    expect(result.toKey).toBe('k2');
    expect(result.webhookSecrets).toBeGreaterThanOrEqual(1);
    expect(result.slackUrls).toBeGreaterThanOrEqual(1);

    const after = parseEnvelope((await endpointRow(id)).secretEncrypted!);
    expect(after.kekId).toBe('k2');
    expect(after.wrappedDek.equals(before.wrappedDek)).toBe(false);
    expect(after.iv.equals(before.iv)).toBe(true); // the data was NOT re-encrypted
    expect(after.ciphertext.equals(before.ciphertext)).toBe(true);

    // Running it again changes nothing (idempotent).
    expect(await rewrapAllSecrets()).toMatchObject({ webhookSecrets: 0, slackUrls: 0 });
    expect((await secretsStatus()).byKey).not.toHaveProperty('k1');

    setKmsForTests(kmsWith(k2)); // step 3: k1 removed
    const delivered = await deliverOne(org.id);
    expect(new Webhook(secret).verify(delivered.body, delivered.headers as Record<string, string>)).toBeTruthy();
    expect(await readSlackWebhookUrl(org.id)).toBe('https://hooks.slack.com/services/T0/B0/rotate-me');

    const [audit] = await db.select().from(schema.auditEvents).where(eq(schema.auditEvents.action, 'secrets.rewrapped'));
    expect(audit).toMatchObject({ organizationId: null, category: 'platform' });
    expect(JSON.stringify(audit)).not.toMatch(/whsec_|hooks\.slack\.com|AQEB/); // counts and key ids only
  });
});

describe('upgrading from Module 7: plaintext secrets are encrypted by db:migrate', () => {
  it('encrypts legacy webhook secrets and Slack URLs, empties the plaintext columns, and is idempotent', async () => {
    const org = await makeOrg('Legacy');
    const legacy = generateWebhookSecret();
    // What a Module 7 database holds: plaintext, written before this module existed.
    const [ep] = await db
      .insert(schema.webhookEndpoints)
      .values({ organizationId: org.id, url: `${base}/legacy`, eventTypes: ['incident.opened'], legacySecret: legacy })
      .returning();
    await db.update(schema.organizations).set({ legacySlackWebhookUrl: 'https://hooks.slack.com/services/T0/B0/legacy' }).where(eq(schema.organizations.id, org.id));
    expect((await secretsStatus()).plaintext).toBeGreaterThanOrEqual(2);

    const first = await encryptLegacySecrets();
    expect(first.webhookSecrets).toBeGreaterThanOrEqual(1);
    expect(first.slackUrls).toBeGreaterThanOrEqual(1);
    expect(await encryptLegacySecrets()).toEqual({ webhookSecrets: 0, slackUrls: 0 });
    expect((await secretsStatus()).plaintext).toBe(0);

    const row = await endpointRow(ep.id);
    expect(row.legacySecret).toBeNull();
    expect(await decryptSecret(row.secretEncrypted!, secretContext('webhook_endpoints.secret', org.id))).toBe(legacy);
    const [orgRow] = await db.select().from(schema.organizations).where(eq(schema.organizations.id, org.id));
    expect(orgRow.legacySlackWebhookUrl).toBeNull();
    expect(orgRow.slackWebhookUrlEncrypted).toMatch(/^enc:v1:/);
    expect((await getOrgNotificationSettings({ orgId: org.id })).slack).toEqual({ connected: true, hint: '…legacy' });

    // The customer's receiver keeps verifying with the secret they saved in Module 5.
    const delivered = await deliverOne(org.id);
    expect(new Webhook(legacy).verify(delivered.body, delivered.headers as Record<string, string>)).toBeTruthy();
    expect(await db.select().from(schema.auditEvents).where(eq(schema.auditEvents.action, 'secrets.encrypted'))).toHaveLength(1);
  });
});

async function endpointRow(id: string) {
  const [row] = await db.select().from(schema.webhookEndpoints).where(eq(schema.webhookEndpoints.id, id));
  return row;
}

/** Record an event for the org's endpoints and deliver the newest message now; returns what the receiver got. */
async function deliverOne(orgId: string) {
  received.length = 0;
  await withOrg(orgId, (tx) => recordWebhookEvent(tx, orgId, 'incident.opened', { type: 'incident.opened', data: { test: true } }));
  const messages = await withOrg(orgId, (tx) => tx.select().from(schema.webhookMessages).where(eq(schema.webhookMessages.status, 'pending')));
  for (const m of messages) await deliverWebhook({ orgId, messageId: m.id });
  expect(received.length).toBeGreaterThan(0);
  return received[received.length - 1];
}
