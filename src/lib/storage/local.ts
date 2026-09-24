import { createHmac, timingSafeEqual } from 'node:crypto';
import { mkdir, open, readFile, rm, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { isValidKey } from '@/core/files';
import type { Storage } from './index';

/*
 * Lesson 2.2: a stand-in for S3 on your laptop and in tests.
 *
 * Objects are files under STORAGE_LOCAL_DIR (default .storage/), with the
 * content type in a small .meta.json next to each one. The signed URLs work
 * like presigned S3 URLs: they name one operation on one key, expire, and
 * carry an HMAC signature, so the route at /api/storage/[...key] can check
 * them without a session.
 *
 * One honest difference: here the bytes do pass through the Next.js process,
 * because it plays the part of the bucket. With STORAGE_DRIVER=s3 the browser
 * talks to the bucket and Beacon never sees the bytes.
 */

export const LOCAL_MAX_BYTES = 20 * 1024 * 1024; // the "bucket" refuses anything bigger, whatever was signed

type Operation = 'put' | 'get';

function secret(): string {
  const value = process.env.STORAGE_LOCAL_SECRET ?? process.env.BETTER_AUTH_SECRET;
  if (value) return value;
  if (process.env.NODE_ENV === 'production') throw new Error('Set STORAGE_LOCAL_SECRET (or BETTER_AUTH_SECRET) to use the local storage driver');
  return 'dev-only-local-storage-secret';
}

function signature(op: Operation, key: string, expires: number, contentType: string): string {
  return createHmac('sha256', secret()).update(`${op}\n${key}\n${expires}\n${contentType}`).digest('base64url');
}

function signedUrl(op: Operation, key: string, expiresInSeconds: number, contentType = ''): string {
  const expires = Math.floor(Date.now() / 1000) + expiresInSeconds;
  const base = process.env.APP_URL ?? 'http://localhost:3000';
  const url = new URL(`/api/storage/${key}`, base);
  url.searchParams.set('op', op);
  url.searchParams.set('expires', String(expires));
  if (contentType) url.searchParams.set('type', contentType);
  url.searchParams.set('sig', signature(op, key, expires, contentType));
  return url.toString();
}

/** Check a signed URL for `op` on `key`. Returns the signed content type (for PUT), or null if invalid. */
export function verifyLocalUrl(op: Operation, key: string, params: URLSearchParams): { contentType: string } | null {
  if (!isValidKey(key) || params.get('op') !== op) return null;
  const expires = Number(params.get('expires'));
  if (!Number.isInteger(expires) || expires < Date.now() / 1000) return null;
  const contentType = params.get('type') ?? '';
  const expected = Buffer.from(signature(op, key, expires, contentType));
  const given = Buffer.from(params.get('sig') ?? '');
  if (given.length !== expected.length || !timingSafeEqual(given, expected)) return null;
  return { contentType };
}

export function createLocalStorage(root = process.env.STORAGE_LOCAL_DIR ?? '.storage'): Storage {
  const dir = path.resolve(root);
  const fileFor = (key: string) => {
    if (!isValidKey(key)) throw new Error(`Invalid storage key: ${key}`);
    return path.join(dir, ...key.split('/'));
  };
  const metaFor = (key: string) => `${fileFor(key)}.meta.json`;

  return {
    async signUpload(key, contentType, expiresIn) {
      fileFor(key); // validates the key
      return signedUrl('put', key, expiresIn, contentType);
    },
    async signDownload(key, expiresIn) {
      fileFor(key);
      return signedUrl('get', key, expiresIn);
    },
    async head(key) {
      try {
        const [info, meta] = await Promise.all([stat(fileFor(key)), readFile(metaFor(key), 'utf8')]);
        return { size: info.size, contentType: (JSON.parse(meta) as { contentType: string | null }).contentType };
      } catch (err) {
        if ((err as NodeJS.ErrnoException).code === 'ENOENT') return null;
        throw err;
      }
    },
    async readStart(key, length) {
      const handle = await open(fileFor(key), 'r');
      try {
        const buffer = Buffer.alloc(length);
        const { bytesRead } = await handle.read(buffer, 0, length, 0);
        return new Uint8Array(buffer.subarray(0, bytesRead));
      } finally {
        await handle.close();
      }
    },
    async get(key) {
      return new Uint8Array(await readFile(fileFor(key)));
    },
    async put(key, bytes, contentType) {
      const file = fileFor(key);
      await mkdir(path.dirname(file), { recursive: true });
      await writeFile(file, bytes);
      await writeFile(metaFor(key), JSON.stringify({ contentType }));
    },
    async delete(key) {
      await rm(fileFor(key), { force: true });
      await rm(metaFor(key), { force: true });
    },
  };
}
