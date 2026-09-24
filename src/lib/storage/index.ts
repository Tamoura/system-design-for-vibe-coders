import { createLocalStorage } from './local';
import { createS3Storage } from './s3';

/**
 * Lesson 2.2: object storage behind a small interface. The rest of Beacon
 * never imports the AWS SDK; it asks for signed URLs and, in background jobs,
 * reads and writes whole objects.
 *
 * Two drivers, picked by STORAGE_DRIVER:
 *   local (default)  files under .storage/, served by /api/storage/… with
 *                    HMAC-signed, expiring URLs that mimic presigned S3 URLs.
 *                    For development and tests: no Docker, no bucket.
 *   s3               any S3-compatible store: AWS S3, Cloudflare R2, Garage,
 *                    SeaweedFS, MinIO. Configure the S3_* variables in
 *                    .env.example and run `npm run storage:setup` once.
 *
 * Both are private: nothing is readable without a URL that Beacon signed
 * after an access check, and those URLs expire in minutes.
 */
export type ObjectInfo = { size: number; contentType: string | null };

export interface Storage {
  /** A URL the browser can PUT the bytes to, directly, until it expires. */
  signUpload(key: string, contentType: string, expiresInSeconds: number): Promise<string>;
  /** A URL the browser can GET the object from until it expires. */
  signDownload(key: string, expiresInSeconds: number): Promise<string>;
  /** Size and type of an object, or null if there is none. */
  head(key: string): Promise<ObjectInfo | null>;
  /** The first `length` bytes (for sniffing the real type). */
  readStart(key: string, length: number): Promise<Uint8Array>;
  /** The whole object. Only for background jobs, never in a request. */
  get(key: string): Promise<Uint8Array>;
  /** Write a whole object. Only for background jobs (e.g. thumbnails). */
  put(key: string, bytes: Uint8Array, contentType: string): Promise<void>;
  delete(key: string): Promise<void>;
}

let instance: Storage | undefined;

export function getStorage(): Storage {
  if (!instance) instance = process.env.STORAGE_DRIVER === 's3' ? createS3Storage() : createLocalStorage();
  return instance;
}

/** Tests swap the driver (e.g. to a fresh temp directory). */
export function setStorageForTests(storage: Storage | undefined) {
  instance = storage;
}
