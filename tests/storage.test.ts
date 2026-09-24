import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import S3rver from 's3rver';
import { CreateBucketCommand } from '@aws-sdk/client-s3';
import { setStorageForTests, type Storage } from '@/lib/storage';
import { createLocalStorage } from '@/lib/storage/local';
import { createS3Storage, s3Client, type S3Config } from '@/lib/storage/s3';
import { pngBytes, sendToSignedUrl } from './helpers/storage';

/*
 * Lesson 2.2: both storage drivers keep the same promises. The S3 driver runs
 * against s3rver, a small S3-compatible server in Node (no Docker needed);
 * in production the same code talks to S3, R2, Garage or SeaweedFS.
 */
const KEY = 'orgs/0190a6f2-1111-4222-8333-444455556666/logos/0190a6f2-aaaa-4bbb-8ccc-dddddddddddd';

let s3server: S3rver;
let s3config: S3Config;

beforeAll(async () => {
  s3server = new S3rver({ port: 0, address: '127.0.0.1', silent: true, directory: mkdtempSync(path.join(tmpdir(), 's3rver-')) });
  const { port } = await s3server.run();
  s3config = { bucket: 'beacon-test', region: 'us-east-1', endpoint: `http://127.0.0.1:${port}`, forcePathStyle: true, accessKeyId: 'S3RVER', secretAccessKey: 'S3RVER' };
  await s3Client(s3config).send(new CreateBucketCommand({ Bucket: s3config.bucket }));
});

afterAll(async () => {
  await s3server?.close();
});

const drivers: Record<string, () => Storage> = {
  // The /api/storage route serves whatever getStorage() returns, so point it at this instance.
  local: () => {
    const storage = createLocalStorage(mkdtempSync(path.join(tmpdir(), 'beacon-local-')));
    setStorageForTests(storage);
    return storage;
  },
  s3: () => createS3Storage(s3config),
};

for (const [name, make] of Object.entries(drivers)) {
  describe(`${name} driver`, () => {
    it('uploads through a signed PUT URL, then heads, reads, downloads and deletes', async () => {
      const storage = make();
      const png = await pngBytes(40, 20);
      const putUrl = await storage.signUpload(KEY, 'image/png', 300);
      expect((await sendToSignedUrl(putUrl, { method: 'PUT', body: png, contentType: 'image/png' })).status).toBe(200);

      expect(await storage.head(KEY)).toEqual({ size: png.byteLength, contentType: 'image/png' });
      expect(Array.from(await storage.readStart(KEY, 8))).toEqual([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

      const getUrl = await storage.signDownload(KEY, 300);
      const got = await sendToSignedUrl(getUrl, { method: 'GET' });
      expect(got.status).toBe(200);
      expect(new Uint8Array(await got.arrayBuffer())).toEqual(png);

      await storage.delete(KEY);
      expect(await storage.head(KEY)).toBeNull();
    });
  });
}

describe('local driver signatures (like presigned S3 URLs)', () => {
  it('refuses a tampered, expired, or wrong-operation URL, and a different Content-Type', async () => {
    const storage = drivers.local();
    const url = new URL(await storage.signUpload(KEY, 'image/png', 300));
    const put = (u: URL, type = 'image/png') => sendToSignedUrl(u.toString(), { method: 'PUT', body: 'x', contentType: type });

    const tampered = new URL(url);
    tampered.pathname = tampered.pathname.replace('logos', 'screenshots');
    expect((await put(tampered)).status).toBe(403);

    const typeSwap = new URL(url);
    typeSwap.searchParams.set('type', 'text/html');
    expect((await put(typeSwap, 'text/html')).status).toBe(403);

    expect((await put(url, 'text/html')).status).toBe(403); // signed for image/png

    const expired = new URL(await storage.signUpload(KEY, 'image/png', -1));
    expect((await put(expired)).status).toBe(403);

    const asGet = new URL(url);
    asGet.searchParams.set('op', 'get');
    expect((await sendToSignedUrl(asGet.toString(), { method: 'GET' })).status).toBe(403);
  });

  it('serves user content with nosniff and a sandboxing CSP', async () => {
    const storage = drivers.local();
    await storage.put(KEY, await pngBytes(10, 10), 'image/png');
    const res = await sendToSignedUrl(await storage.signDownload(KEY, 300), { method: 'GET' });
    expect(res.headers.get('x-content-type-options')).toBe('nosniff');
    expect(res.headers.get('content-security-policy')).toContain('sandbox');
  });
});
