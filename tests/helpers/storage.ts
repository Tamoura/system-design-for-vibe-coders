import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import sharp from 'sharp';
import { setStorageForTests } from '@/lib/storage';
import { createLocalStorage } from '@/lib/storage/local';
import * as localBucket from '@/app/api/storage/[...key]/route';

/** Use the local storage driver in a fresh temp directory for this test file. */
export function useTempLocalStorage() {
  const dir = mkdtempSync(path.join(tmpdir(), 'beacon-storage-'));
  const storage = createLocalStorage(dir);
  setStorageForTests(storage);
  return storage;
}

/**
 * Do what the browser does with a signed URL. Local-driver URLs point at
 * /api/storage/…, so the request goes to that route handler; anything else
 * (the S3 test server) is fetched for real.
 */
export async function sendToSignedUrl(url: string, init: { method: 'PUT' | 'GET'; body?: Uint8Array | string; contentType?: string }) {
  const request = new Request(url, {
    method: init.method,
    body: init.body as BodyInit | undefined,
    headers: init.contentType ? { 'content-type': init.contentType } : undefined,
  });
  const { pathname } = new URL(url);
  if (pathname.startsWith('/api/storage/')) {
    const key = pathname.slice('/api/storage/'.length).split('/');
    const handler = init.method === 'PUT' ? localBucket.PUT : localBucket.GET;
    return handler(request, { params: Promise.resolve({ key }) });
  }
  return fetch(request);
}

export async function pngBytes(width = 800, height = 600): Promise<Uint8Array> {
  return new Uint8Array(await sharp({ create: { width, height, channels: 3, background: '#3366cc' } }).png().toBuffer());
}
