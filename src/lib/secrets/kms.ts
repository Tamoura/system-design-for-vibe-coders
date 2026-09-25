import { createHash } from 'node:crypto';
import { aesGcmDecrypt, aesGcmEncrypt, DEK_BYTES } from '@/core/envelope';
import { logger } from '../observability/logger';

/*
 * Lesson 8.1 (🟡): the KMS, behind an interface. A KMS (key management
 * service) holds the key-encryption keys (KEKs) and does exactly two things
 * with them: wrap a data key, unwrap a data key. The KEK never leaves it.
 *
 *   local     (this file) KEKs from ENCRYPTION_KEYS, in the app's memory. Fine for
 *             self-hosting and development; the keys are as safe as the environment.
 *   aws-kms   (not built) KMS Encrypt/Decrypt with a KeyId: the same two methods,
 *   openbao   (not built) OpenBao/Vault transit: POST transit/encrypt|decrypt/<key>.
 *
 * Methods are async on purpose: a real KMS is a network call. In production,
 * cache unwrapped DEKs for a few minutes if it becomes a hot path.
 */
export interface Kms {
  /** The KEK new values are wrapped with. */
  readonly currentKeyId: string;
  /** Every KEK this KMS can unwrap with (current first). */
  readonly keyIds: string[];
  wrapKey(dek: Buffer): Promise<{ kekId: string; wrapped: Buffer }>;
  unwrapKey(kekId: string, wrapped: Buffer): Promise<Buffer>;
}

/** A development-only KEK: public (it is in this file), so production refuses to run without ENCRYPTION_KEYS. */
const DEV_KEY = { id: 'dev', key: createHash('sha256').update('beacon-development-key-NOT-SECRET').digest() };

/**
 * ENCRYPTION_KEYS="k2:<base64 of 32 bytes>,k1:<base64 of 32 bytes>". The FIRST
 * key encrypts; every listed key decrypts. That is the whole rotation story:
 * add a new key in front, re-wrap (npm run secrets -- rotate), drop the old one.
 */
export function parseKeyring(value: string): { id: string; key: Buffer }[] {
  const keys = value
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)
    .map((entry) => {
      const i = entry.indexOf(':');
      const id = entry.slice(0, i);
      const key = Buffer.from(entry.slice(i + 1), 'base64');
      if (i < 1 || !/^[a-z0-9_-]{1,32}$/.test(id)) throw new Error(`ENCRYPTION_KEYS: "${id}" is not a key id (a-z, 0-9, _ and -)`);
      if (key.length !== 32) throw new Error(`ENCRYPTION_KEYS: key "${id}" must be 32 bytes, base64 (openssl rand -base64 32)`);
      return { id, key };
    });
  if (!keys.length) throw new Error('ENCRYPTION_KEYS is empty');
  if (new Set(keys.map((k) => k.id)).size !== keys.length) throw new Error('ENCRYPTION_KEYS: duplicate key id');
  return keys;
}

export class LocalKms implements Kms {
  private readonly keys: Map<string, Buffer>;
  readonly currentKeyId: string;
  readonly keyIds: string[];

  constructor(keyring: { id: string; key: Buffer }[]) {
    this.keys = new Map(keyring.map((k) => [k.id, k.key]));
    this.keyIds = keyring.map((k) => k.id);
    this.currentKeyId = this.keyIds[0];
  }

  async wrapKey(dek: Buffer) {
    const kek = this.keys.get(this.currentKeyId)!;
    // The KEK wraps the DEK with AES-256-GCM too; the key id is the context, so a DEK
    // wrapped by k1 cannot be passed off as wrapped by k2.
    const { iv, ciphertext } = aesGcmEncrypt(kek, dek, `kek:${this.currentKeyId}`);
    return { kekId: this.currentKeyId, wrapped: Buffer.concat([iv, ciphertext]) };
  }

  async unwrapKey(kekId: string, wrapped: Buffer) {
    const kek = this.keys.get(kekId);
    if (!kek) throw new Error(`Encryption key "${kekId}" is not in ENCRYPTION_KEYS (was it removed before \`npm run secrets -- rotate\`?)`);
    const dek = aesGcmDecrypt(kek, wrapped.subarray(0, 12), wrapped.subarray(12), `kek:${kekId}`);
    if (dek.length !== DEK_BYTES) throw new Error('Unwrapped data key has the wrong length');
    return dek;
  }
}

let instance: Kms | undefined;

/** The configured KMS (KMS_DRIVER, default `local`). */
export function getKms(): Kms {
  if (instance) return instance;
  const driver = process.env.KMS_DRIVER ?? 'local';
  if (driver !== 'local') throw new Error(`KMS_DRIVER=${driver} is not implemented; see src/lib/secrets/kms.ts`);
  if (process.env.ENCRYPTION_KEYS) {
    instance = new LocalKms(parseKeyring(process.env.ENCRYPTION_KEYS));
  } else {
    // src/lib/env.ts makes ENCRYPTION_KEYS required in production, so this is development or tests.
    if (process.env.NODE_ENV !== 'test') logger.warn('secrets.dev_key: ENCRYPTION_KEYS is not set; using the public development key');
    instance = new LocalKms([DEV_KEY]);
  }
  return instance;
}

/** Tests (and the rotation drill) swap the KMS. */
export function setKmsForTests(kms: Kms | undefined) {
  instance = kms;
}
