import { getStorage } from '@/lib/storage';
import { LOCAL_MAX_BYTES, verifyLocalUrl } from '@/lib/storage/local';

/*
 * Lesson 2.2: the local storage driver's "bucket". It answers only signed,
 * unexpired URLs minted by src/lib/storage/local.ts, like presigned S3 URLs,
 * and knows nothing about sessions or organizations: the access check
 * happened when Beacon signed the URL.
 *
 * With STORAGE_DRIVER=s3 this route is switched off (404); the browser talks
 * to the bucket instead.
 */

type Params = { params: Promise<{ key: string[] }> };

const enabled = () => process.env.STORAGE_DRIVER !== 's3';
const denied = () => new Response('Forbidden: missing, invalid or expired signature', { status: 403 });

/** PUT /api/storage/orgs/{orgId}/{folder}/{fileId}?op=put&expires=…&type=…&sig=… */
export async function PUT(req: Request, { params }: Params) {
  if (!enabled()) return new Response(null, { status: 404 });
  const key = (await params).key.join('/');
  const signed = verifyLocalUrl('put', key, new URL(req.url).searchParams);
  if (!signed) return denied();
  // Like S3: the Content-Type was part of the signature and must match.
  if ((req.headers.get('content-type') ?? '') !== signed.contentType) return denied();

  // Read the body, but stop at LOCAL_MAX_BYTES instead of buffering anything
  // a client decides to send.
  const chunks: Uint8Array[] = [];
  let size = 0;
  const reader = req.body?.getReader();
  while (reader) {
    const { done, value } = await reader.read();
    if (done) break;
    size += value.byteLength;
    if (size > LOCAL_MAX_BYTES) {
      await reader.cancel();
      return new Response('Entity too large', { status: 413 });
    }
    chunks.push(value);
  }
  await getStorage().put(key, Buffer.concat(chunks), signed.contentType);
  return new Response(null, { status: 200 });
}

/** GET /api/storage/orgs/…?op=get&expires=…&sig=… */
export async function GET(req: Request, { params }: Params) {
  if (!enabled()) return new Response(null, { status: 404 });
  const key = (await params).key.join('/');
  if (!verifyLocalUrl('get', key, new URL(req.url).searchParams)) return denied();
  const storage = getStorage();
  const info = await storage.head(key);
  if (!info) return new Response('Not found', { status: 404 });
  return new Response(Buffer.from(await storage.get(key)), {
    headers: {
      'Content-Type': info.contentType ?? 'application/octet-stream',
      'Content-Length': String(info.size),
      // User content on Beacon's own domain: never let the browser guess a
      // type, never run anything in it (lesson 2.2).
      'X-Content-Type-Options': 'nosniff',
      'Content-Security-Policy': "default-src 'none'; sandbox",
      'Cache-Control': 'private, max-age=300',
    },
  });
}
