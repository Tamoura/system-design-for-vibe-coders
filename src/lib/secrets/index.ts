import { aesGcmDecrypt, aesGcmEncrypt, formatEnvelope, isEnvelope, newDek, parseEnvelope } from '@/core/envelope';
import { getKms, type Kms } from './kms';

/*
 * Lesson 8.1 (🟡): application-level encryption of the secrets Beacon must be
 * able to READ BACK (a webhook signing secret signs every delivery; a Slack
 * URL is where we post). API keys only need verifying, so they stay hashed (5.2).
 *
 *   await encryptSecret(secret, secretContext('webhook_endpoints.secret', orgId))  → "enc:v1:…"
 *   await decryptSecret(stored, secretContext('webhook_endpoints.secret', orgId))  → the secret
 *
 * One fresh data key (DEK) per value, wrapped by the KMS (./kms.ts). The format
 * and the AES-GCM parts are in src/core/envelope.ts; how to rotate the KMS key
 * is in docs/security/secrets.md.
 */

/** The columns that hold encrypted secrets. The name is part of the ciphertext's context. */
export type SecretColumn = 'webhook_endpoints.secret' | 'organizations.slack_webhook_url';

/** Binds a ciphertext to its column and its organization (AES-GCM additional data). */
export function secretContext(column: SecretColumn, orgId: string): string {
  return `${column}:org:${orgId}`;
}

export async function encryptSecret(plaintext: string, context: string, kms: Kms = getKms()): Promise<string> {
  const dek = newDek();
  const { iv, ciphertext } = aesGcmEncrypt(dek, Buffer.from(plaintext, 'utf8'), context);
  const { kekId, wrapped } = await kms.wrapKey(dek);
  dek.fill(0); // do not leave the data key lying around in memory longer than needed
  return formatEnvelope({ kekId, wrappedDek: wrapped, iv, ciphertext });
}

export async function decryptSecret(stored: string, context: string, kms: Kms = getKms()): Promise<string> {
  const e = parseEnvelope(stored);
  const dek = await kms.unwrapKey(e.kekId, e.wrappedDek);
  try {
    return aesGcmDecrypt(dek, e.iv, e.ciphertext, context).toString('utf8');
  } finally {
    dek.fill(0);
  }
}

/**
 * Key rotation: unwrap the DEK with its old KEK and wrap it with the current
 * one. The IV and ciphertext are copied unchanged: the data is not re-encrypted.
 * Returns null when the value is already on the current key.
 */
export async function rewrapSecret(stored: string, kms: Kms = getKms()): Promise<string | null> {
  const e = parseEnvelope(stored);
  if (e.kekId === kms.currentKeyId) return null;
  const dek = await kms.unwrapKey(e.kekId, e.wrappedDek);
  const { kekId, wrapped } = await kms.wrapKey(dek);
  dek.fill(0);
  return formatEnvelope({ ...e, kekId, wrappedDek: wrapped });
}

/** Which KEK a stored value is wrapped with (for `npm run secrets -- status`). */
export function keyIdOf(stored: string): string | null {
  return isEnvelope(stored) ? parseEnvelope(stored).kekId : null;
}

export { isEnvelope };
