import { createCipheriv, createDecipheriv, randomBytes } from 'node:crypto';

/*
 * Lesson 8.1 (🟡): envelope encryption, the pure parts. Never invent crypto:
 * this is AES-256-GCM from Node's crypto module (OpenSSL), used the standard
 * way (a fresh random 12-byte IV per encryption, the 16-byte tag checked on
 * decrypt). What Beacon adds is only the envelope around it:
 *
 *   plaintext ──AES-256-GCM, a fresh random DEK──► ciphertext
 *   DEK ──wrapped by the KMS's key-encryption key (KEK)──► wrapped DEK
 *   stored:  enc:v1:<kek id>:<wrapped DEK>:<iv>:<ciphertext+tag>   (base64url)
 *
 * The KEK never touches the database; the DEK is stored only wrapped. Rotating
 * the KEK re-wraps the small DEKs and leaves the ciphertext alone.
 *
 * `aad` (additional authenticated data) is not secret and not stored: it is
 * the context the value belongs to ("webhook_endpoints.secret:org:<id>").
 * Decrypting with a different context fails, so a ciphertext copied into
 * another org's row, or another column, is useless.
 */

export const ENVELOPE_PREFIX = 'enc:v1:';
export const DEK_BYTES = 32; // AES-256

export type Envelope = { kekId: string; wrappedDek: Buffer; iv: Buffer; ciphertext: Buffer };

const b64 = (b: Buffer) => b.toString('base64url');
const unb64 = (s: string) => Buffer.from(s, 'base64url');

export function isEnvelope(value: string | null | undefined): value is string {
  return typeof value === 'string' && value.startsWith(ENVELOPE_PREFIX);
}

export function newDek(): Buffer {
  return randomBytes(DEK_BYTES);
}

/** AES-256-GCM. Returns the ciphertext with its 16-byte tag appended. */
export function aesGcmEncrypt(key: Buffer, plaintext: Buffer, aad: string): { iv: Buffer; ciphertext: Buffer } {
  const iv = randomBytes(12); // never reuse an IV with the same key: random 96 bits per call
  const cipher = createCipheriv('aes-256-gcm', key, iv);
  cipher.setAAD(Buffer.from(aad, 'utf8'));
  const ciphertext = Buffer.concat([cipher.update(plaintext), cipher.final(), cipher.getAuthTag()]);
  return { iv, ciphertext };
}

/** The reverse. Throws if the key, the context or a single bit of the ciphertext is wrong. */
export function aesGcmDecrypt(key: Buffer, iv: Buffer, ciphertextWithTag: Buffer, aad: string): Buffer {
  const tag = ciphertextWithTag.subarray(ciphertextWithTag.length - 16);
  const decipher = createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAAD(Buffer.from(aad, 'utf8'));
  decipher.setAuthTag(tag);
  return Buffer.concat([decipher.update(ciphertextWithTag.subarray(0, ciphertextWithTag.length - 16)), decipher.final()]);
}

export function formatEnvelope(e: Envelope): string {
  return `${ENVELOPE_PREFIX}${e.kekId}:${b64(e.wrappedDek)}:${b64(e.iv)}:${b64(e.ciphertext)}`;
}

export function parseEnvelope(value: string): Envelope {
  if (!isEnvelope(value)) throw new Error('Not an encrypted value (expected enc:v1:…)');
  const parts = value.slice(ENVELOPE_PREFIX.length).split(':');
  if (parts.length !== 4 || parts.some((p) => !p)) throw new Error('Malformed encrypted value');
  const [kekId, wrappedDek, iv, ciphertext] = parts;
  return { kekId, wrappedDek: unb64(wrappedDek), iv: unb64(iv), ciphertext: unb64(ciphertext) };
}
