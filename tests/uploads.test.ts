import { beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));

import { eq } from 'drizzle-orm';
import sharp from 'sharp';
import { db, schema } from '@/db';
import { processUploadedFile } from '@/lib/files';
import { createMonitor } from '@/lib/monitors';
import * as logoRoute from '@/app/api/orgs/[orgSlug]/logo/route';
import * as screenshotsRoute from '@/app/api/orgs/[orgSlug]/incidents/[incidentId]/screenshots/route';
import * as completeRoute from '@/app/api/orgs/[orgSlug]/files/[fileId]/complete/route';
import * as fileRoute from '@/app/api/orgs/[orgSlug]/files/[fileId]/route';
import * as statusLogoRoute from '@/app/status/[slug]/logo/route';
import { makeOrg, signInAs } from './helpers/fixtures';
import { pngBytes, sendToSignedUrl, useTempLocalStorage } from './helpers/storage';
import { jobsIn, runQueuedJobs } from './helpers/queue';

/*
 * Lesson 2.2: logo uploads (🟢) and incident screenshots (🟡), end to end
 * through the API routes, with the local storage driver in a temp directory.
 */
const storage = useTempLocalStorage();
let acme: Awaited<ReturnType<typeof makeOrg>>;
let globex: Awaited<ReturnType<typeof makeOrg>>;
let incidentId: string;

beforeAll(async () => {
  acme = await makeOrg('Acme');
  globex = await makeOrg('Globex');
  const m = await createMonitor({ orgId: acme.id, userId: acme.users.owner.id }, { name: 'api', url: 'https://acme.test', intervalSeconds: 60 });
  [{ id: incidentId }] = await db.insert(schema.incidents).values({ organizationId: acme.id, monitorId: m.id, cause: 'down' }).returning();
});

const json = (body: unknown) => new Request('http://test/x', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) });
const p = <T extends object>(params: T) => ({ params: Promise.resolve(params) });

async function askForLogoUrl(orgSlug: string, file: { name: string; type: string; size: number }) {
  return logoRoute.POST(json(file), p({ orgSlug }));
}

/** The browser's three steps. Returns the "complete" response body. */
async function upload(orgSlug: string, ask: (f: { name: string; type: string; size: number }) => Promise<Response>, name: string, type: string, bytes: Uint8Array) {
  const ticket = await ask({ name, type, size: bytes.byteLength });
  expect(ticket.status).toBe(201);
  const { data } = await ticket.json();
  expect((await sendToSignedUrl(data.upload.url, { method: 'PUT', body: bytes, contentType: type })).status).toBe(200);
  const done = await completeRoute.POST(new Request('http://test/x', { method: 'POST' }), p({ orgSlug, fileId: data.fileId }));
  expect(done.status).toBe(200);
  return (await done.json()).data as { fileId: string; status: string; reason: string | null };
}

async function fileRow(id: string) {
  const [row] = await db.select().from(schema.files).where(eq(schema.files.id, id));
  return row;
}

describe('🟢 logo upload', () => {
  it('only owners and admins of the org can get a signed URL', async () => {
    const file = { name: 'logo.png', type: 'image/png', size: 1000 };
    for (const [role, status] of [['owner', 201], ['admin', 201], ['member', 403], ['viewer', 403]] as const) {
      signInAs(acme.users[role]);
      expect((await askForLogoUrl(acme.slug, file)).status, role).toBe(status);
    }
    signInAs(globex.users.owner);
    expect((await askForLogoUrl(acme.slug, file)).status).toBe(404);
    signInAs(null);
    expect((await askForLogoUrl(acme.slug, file)).status).toBe(401);
  });

  it('refuses a 10 MB file or an .exe before any URL is issued', async () => {
    signInAs(acme.users.admin);
    const before = (await db.select().from(schema.files)).length;
    const big = await askForLogoUrl(acme.slug, { name: 'big.png', type: 'image/png', size: 10 * 1024 * 1024 });
    expect(big.status).toBe(400);
    expect((await big.json()).error).toBe('too_large');
    const exe = await askForLogoUrl(acme.slug, { name: 'setup.exe', type: 'application/x-msdownload', size: 5000 });
    expect(exe.status).toBe(400);
    expect((await exe.json()).error).toBe('type_not_allowed');
    expect((await db.select().from(schema.files)).length).toBe(before); // no row, no URL
  });

  it('signs a 5-minute PUT URL for orgs/{orgId}/logos/{fileId}, and "complete" marks it ready', async () => {
    signInAs(acme.users.admin);
    const res = await askForLogoUrl(acme.slug, { name: 'logo.png', type: 'image/png', size: 1234 });
    const { data } = await res.json();
    const url = new URL(data.upload.url);
    expect(url.pathname).toBe(`/api/storage/orgs/${acme.id}/logos/${data.fileId}`);
    expect(Number(url.searchParams.get('expires')) - Date.now() / 1000).toBeLessThanOrEqual(300);
    expect((await fileRow(data.fileId)).status).toBe('pending');

    const png = await pngBytes(300, 100);
    const result = await upload(acme.slug, (f) => askForLogoUrl(acme.slug, f), 'acme.png', 'image/png', png);
    expect(result.status).toBe('ready');
    const [org] = await db.select().from(schema.organizations).where(eq(schema.organizations.id, acme.id));
    expect(org.logoFileId).toBe(result.fileId);
    expect(await fileRow(result.fileId)).toMatchObject({ contentType: 'image/png', sizeBytes: png.byteLength, uploadedBy: acme.users.admin.id });
  });

  it('replacing the logo deletes the old one', async () => {
    signInAs(acme.users.owner);
    const first = await upload(acme.slug, (f) => askForLogoUrl(acme.slug, f), 'one.png', 'image/png', await pngBytes(50, 50));
    const oldKey = (await fileRow(first.fileId)).key;
    const second = await upload(acme.slug, (f) => askForLogoUrl(acme.slug, f), 'two.png', 'image/png', await pngBytes(60, 60));
    expect(await fileRow(first.fileId)).toBeUndefined();
    expect(await storage.head(oldKey)).toBeNull();
    expect((await fileRow(second.fileId)).status).toBe('ready');
  });

  it('shows the logo on the public status page only while it is published', async () => {
    const res = await statusLogoRoute.GET(new Request('http://test/x'), p({ slug: acme.slug }));
    expect(res.status).toBe(302);
    const image = await sendToSignedUrl(res.headers.get('location')!, { method: 'GET' });
    expect(image.headers.get('content-type')).toBe('image/png');

    await db.update(schema.organizations).set({ statusPagePublic: false }).where(eq(schema.organizations.id, acme.id));
    expect((await statusLogoRoute.GET(new Request('http://test/x'), p({ slug: acme.slug }))).status).toBe(404);
    await db.update(schema.organizations).set({ statusPagePublic: true }).where(eq(schema.organizations.id, acme.id));
    expect((await statusLogoRoute.GET(new Request('http://test/x'), p({ slug: globex.slug }))).status).toBe(404); // no logo
  });
});

describe('🟡 checking the bytes after upload', () => {
  it('rejects a text file renamed to .png and deletes its object', async () => {
    signInAs(acme.users.admin);
    const text = new TextEncoder().encode('this is not a PNG, just text pretending to be one');
    const result = await upload(acme.slug, (f) => askForLogoUrl(acme.slug, f), 'sneaky.png', 'image/png', text);
    expect(result.status).toBe('rejected');
    const row = await fileRow(result.fileId);
    expect(row.status).toBe('rejected');
    expect(await storage.head(row.key)).toBeNull();
  });

  it('rejects a file bigger than announced (a presigned PUT does not limit size)', async () => {
    signInAs(acme.users.admin);
    const png = await pngBytes(200, 200);
    const ticket = await (await askForLogoUrl(acme.slug, { name: 'small.png', type: 'image/png', size: 100 })).json();
    await sendToSignedUrl(ticket.data.upload.url, { method: 'PUT', body: png, contentType: 'image/png' });
    const done = await completeRoute.POST(new Request('http://test/x', { method: 'POST' }), p({ orgSlug: acme.slug, fileId: ticket.data.fileId }));
    expect((await done.json()).data.status).toBe('rejected');
  });

  it('"complete" before anything was uploaded is a 400, and the row stays pending', async () => {
    signInAs(acme.users.admin);
    const ticket = await (await askForLogoUrl(acme.slug, { name: 'later.png', type: 'image/png', size: 100 })).json();
    const done = await completeRoute.POST(new Request('http://test/x', { method: 'POST' }), p({ orgSlug: acme.slug, fileId: ticket.data.fileId }));
    expect(done.status).toBe(400);
    expect((await fileRow(ticket.data.fileId)).status).toBe('pending');
  });
});

describe('🟡 incident screenshots, private to the org', () => {
  const ask = (orgSlug: string, id: string) => (f: object) => screenshotsRoute.POST(json(f), p({ orgSlug, incidentId: id }));
  let screenshotId: string;

  it('a member uploads one; it is "processing" until the background job has made a thumbnail', async () => {
    signInAs(acme.users.member);
    const result = await upload(acme.slug, ask(acme.slug, incidentId), 'error-page.png', 'image/png', await pngBytes(1600, 900));
    expect(result.status).toBe('processing');
    screenshotId = result.fileId;
    // Lesson 2.4: the job payload carries the org. Lesson 5.1: it is a job in the queue, enqueued with the status change.
    // Lesson 7.2: and the request's id (`_meta`), so the worker's log lines tie back to this upload.
    expect((await jobsIn('file.process')).map((j) => j.data)).toContainEqual({ orgId: acme.id, fileId: screenshotId, _meta: { requestId: expect.any(String) } });

    await runQueuedJobs({ queues: ['file.process'] }); // the worker
    const row = await fileRow(screenshotId);
    expect(row.status).toBe('ready');
    const thumb = await sharp(await storage.get(row.thumbnailKey!)).metadata();
    expect({ width: thumb.width, format: thumb.format }).toEqual({ width: 400, format: 'webp' });
  });

  it('viewers cannot upload; screenshots for another org’s incident are 404', async () => {
    signInAs(acme.users.viewer);
    expect((await ask(acme.slug, incidentId)({ name: 'a.png', type: 'image/png', size: 100 })).status).toBe(403);
    signInAs(globex.users.owner);
    expect((await ask(globex.slug, incidentId)({ name: 'a.png', type: 'image/png', size: 100 })).status).toBe(404);
  });

  it('members download through a redirect to a 5-minute signed URL', async () => {
    signInAs(acme.users.viewer);
    const res = await fileRoute.GET(new Request('http://test/x'), p({ orgSlug: acme.slug, fileId: screenshotId }));
    expect(res.status).toBe(302);
    const signed = new URL(res.headers.get('location')!);
    expect(Number(signed.searchParams.get('expires')) - Date.now() / 1000).toBeLessThanOrEqual(300);
    const thumb = await fileRoute.GET(new Request('http://test/x?variant=thumbnail'), p({ orgSlug: acme.slug, fileId: screenshotId }));
    expect(new URL(thumb.headers.get('location')!).pathname).toMatch(/\.thumb\.webp$/);
  });

  it('a logged-in user from another org gets 404, even with a valid file id', async () => {
    signInAs(globex.users.owner);
    expect((await fileRoute.GET(new Request('http://test/x'), p({ orgSlug: globex.slug, fileId: screenshotId }))).status).toBe(404);
    expect((await fileRoute.GET(new Request('http://test/x'), p({ orgSlug: acme.slug, fileId: screenshotId }))).status).toBe(404);
    const complete = await completeRoute.POST(new Request('http://test/x', { method: 'POST' }), p({ orgSlug: globex.slug, fileId: screenshotId }));
    expect(complete.status).toBe(404);
  });

  it('a screenshot that sharp cannot decode is rejected by the job and deleted', async () => {
    signInAs(acme.users.member);
    // Starts like a PNG (passes the sniff), but the rest is garbage.
    const fake = new Uint8Array([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, ...new TextEncoder().encode('garbage garbage garbage')]);
    const result = await upload(acme.slug, ask(acme.slug, incidentId), 'broken.png', 'image/png', fake);
    expect(result.status).toBe('processing');
    const spy = vi.spyOn(console, 'error').mockImplementation(() => {});
    await processUploadedFile({ orgId: acme.id }, result.fileId);
    spy.mockRestore();
    const row = await fileRow(result.fileId);
    expect(row.status).toBe('rejected');
    expect(await storage.head(row.key)).toBeNull();
  });
});
