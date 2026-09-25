import { randomUUID } from 'node:crypto';
import { and, eq, inArray } from 'drizzle-orm';
import sharp from 'sharp';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import {
  checkUploadRequest,
  DOWNLOAD_URL_TTL_SECONDS,
  keyBelongsToOrg,
  objectKey,
  REFUSAL_MESSAGES,
  sniffImageType,
  SNIFF_BYTES,
  thumbnailKey,
  UPLOAD_RULES,
  UPLOAD_URL_TTL_SECONDS,
  type FileKind,
} from '@/core/files';
import type { StoredFile } from '@/db/schema';
import { AccessError, InvalidRequestError } from './errors';
import { isUuid } from '@/core/validation';
import type { OrgScope } from './monitors';
import { findPublicStatusPage } from './organizations';
import { enqueueInTx } from './queue';
import { getStorage } from './storage';
import { logger } from './observability/logger';

const { files, incidents, organizations } = schema;

/*
 * Lesson 2.2: uploads in three steps, and the bytes never pass through Beacon.
 *
 *   1. requestUpload()   Beacon checks the role (in the route), the declared
 *                        size and type, writes a `pending` row, and signs a
 *                        5-minute PUT URL for orgs/{orgId}/{folder}/{fileId}.
 *   2. the browser PUTs the file straight to storage.
 *   3. completeUpload()  Beacon checks what actually arrived: the real size
 *                        (HEAD) and the real type (the first bytes). A
 *                        mismatch deletes the object and rejects the row.
 *
 * Storage calls happen outside withOrg(): never hold a database transaction
 * open while waiting on the network.
 */

export type UploadTicket = { fileId: string; upload: { method: 'PUT'; url: string; headers: Record<string, string> } };
export type UploadRequest = { name: string; type: string; size: number };

/** Sign a URL, but only for a key under this org's prefix: a cheap guard against id-swapping bugs. */
function assertOwnKey(orgId: string, key: string) {
  if (!keyBelongsToOrg(key, orgId)) throw new Error(`Refusing to sign ${key} for org ${orgId}`);
}

/** Step 1. `incidentId` is required for screenshots and must be an incident of this org (else 404). */
export async function requestUpload(
  ctx: OrgScope & { userId: string },
  kind: FileKind,
  file: UploadRequest,
  incidentId?: string,
): Promise<UploadTicket> {
  const refusal = checkUploadRequest(kind, file);
  if (refusal) throw new InvalidRequestError(refusal, REFUSAL_MESSAGES[refusal]);

  const fileId = randomUUID();
  const key = objectKey(ctx.orgId, kind, fileId);
  await withOrg(ctx.orgId, async (tx) => {
    if (kind === 'incident_screenshot') {
      const found =
        incidentId && isUuid(incidentId)
          ? await tx
              .select({ id: incidents.id })
              .from(incidents)
              .where(and(eq(incidents.organizationId, ctx.orgId), eq(incidents.id, incidentId)))
          : [];
      if (found.length === 0) throw new AccessError('not_found');
    }
    await tx.insert(files).values({
      id: fileId,
      organizationId: ctx.orgId,
      kind,
      incidentId: kind === 'incident_screenshot' ? incidentId : null,
      key,
      originalName: file.name.slice(0, 200),
      declaredType: file.type,
      declaredSize: file.size,
      uploadedBy: ctx.userId,
    });
  });

  assertOwnKey(ctx.orgId, key);
  const url = await getStorage().signUpload(key, file.type, UPLOAD_URL_TTL_SECONDS);
  return { fileId, upload: { method: 'PUT', url, headers: { 'Content-Type': file.type } } };
}

/** One file of this org, or null. The object-level check for every file endpoint. */
export async function getFile({ orgId }: OrgScope, fileId: string): Promise<StoredFile | null> {
  if (!isUuid(fileId)) return null;
  const [row] = await withOrg(orgId, (tx) =>
    tx
      .select()
      .from(files)
      .where(and(eq(files.organizationId, orgId), eq(files.id, fileId)))
      .limit(1),
  );
  return row ?? null;
}

export type CompleteResult = { status: StoredFile['status']; reason?: string; needsProcessing: boolean };

/**
 * Step 3. The caller has loaded the file with getFile() and checked the role
 * may upload this kind. Safe to call twice: only a `pending` file is checked.
 */
export async function completeUpload(ctx: OrgScope, file: StoredFile): Promise<CompleteResult> {
  if (file.status !== 'pending') return { status: file.status, reason: file.rejectionReason ?? undefined, needsProcessing: false };
  const storage = getStorage();

  // The browser said it uploaded. Check what really arrived.
  const info = await storage.head(file.key);
  if (!info) throw new InvalidRequestError('not_uploaded', REFUSAL_MESSAGES.not_uploaded);

  let reason: keyof typeof REFUSAL_MESSAGES | null = null;
  if (info.size > UPLOAD_RULES[file.kind].maxBytes) reason = 'too_large'; // a presigned PUT does not limit size
  else if (info.size !== file.declaredSize) reason = 'size_mismatch';
  else if (sniffImageType(await storage.readStart(file.key, SNIFF_BYTES)) !== file.declaredType) reason = 'content_mismatch';

  if (reason) {
    await storage.delete(file.key);
    await setFile(ctx, file.id, { status: 'rejected', rejectionReason: REFUSAL_MESSAGES[reason], sizeBytes: info.size });
    return { status: 'rejected', reason: REFUSAL_MESSAGES[reason], needsProcessing: false };
  }

  if (file.kind === 'incident_screenshot') {
    // 🟡: the thumbnail is made by a background job; until then the UI shows
    // "processing". Lesson 5.1: the job is enqueued in the same transaction as
    // the status change, so a "processing" file always has its job. The payload
    // carries the org (lesson 2.4) and the file id, never the file.
    await withOrg(ctx.orgId, async (tx) => {
      await tx
        .update(files)
        .set({ status: 'processing', contentType: file.declaredType, sizeBytes: info.size })
        .where(and(eq(files.organizationId, ctx.orgId), eq(files.id, file.id)));
      await enqueueInTx(tx, 'file.process', { orgId: ctx.orgId, fileId: file.id }, { key: file.id });
    });
    return { status: 'processing', needsProcessing: true };
  }

  await setFile(ctx, file.id, { status: 'ready', contentType: file.declaredType, sizeBytes: info.size });
  await replaceLogo(ctx, file.id);
  return { status: 'ready', needsProcessing: false };
}

async function setFile({ orgId }: OrgScope, fileId: string, values: Partial<StoredFile>) {
  await withOrg(orgId, (tx) =>
    tx
      .update(files)
      .set(values)
      .where(and(eq(files.organizationId, orgId), eq(files.id, fileId))),
  );
}

/** Point the org at its new logo, then delete the old one (row and object). */
async function replaceLogo(ctx: OrgScope, newFileId: string) {
  const [org] = await db.select({ logoFileId: organizations.logoFileId }).from(organizations).where(eq(organizations.id, ctx.orgId));
  await db.update(organizations).set({ logoFileId: newFileId }).where(eq(organizations.id, ctx.orgId));
  const old = org?.logoFileId ? await getFile(ctx, org.logoFileId) : null;
  if (old) {
    await getStorage().delete(old.key);
    await withOrg(ctx.orgId, (tx) => tx.delete(files).where(and(eq(files.organizationId, ctx.orgId), eq(files.id, old.id))));
  }
}

/**
 * The background job (🟡): a 400 px wide WebP thumbnail made with sharp. If
 * sharp cannot decode the image, it was not really an image: reject it too.
 * Lesson 5.1: the `file.process` job in the worker. Idempotent: only a file
 * still "processing" is touched.
 */
export async function processUploadedFile(ctx: OrgScope, fileId: string): Promise<void> {
  const file = await getFile(ctx, fileId);
  if (!file || file.status !== 'processing') return;
  const storage = getStorage();
  try {
    const original = await storage.get(file.key);
    const thumb = await sharp(original).rotate().resize({ width: 400, withoutEnlargement: true }).webp({ quality: 80 }).toBuffer();
    const key = thumbnailKey(file.key);
    assertOwnKey(ctx.orgId, key);
    await storage.put(key, thumb, 'image/webp');
    await setFile(ctx, file.id, { status: 'ready', thumbnailKey: key });
  } catch (err) {
    logger.warn({ err, fileId: file.id }, 'file.rejected'); // lesson 7.2: a structured line, with the request/job context
    await storage.delete(file.key);
    await setFile(ctx, file.id, { status: 'rejected', rejectionReason: REFUSAL_MESSAGES.content_mismatch });
  }
}

/**
 * A 5-minute download URL for a ready file of this org, or null (→ 404).
 * 🟡: members reach private files only through this, never by a public URL.
 */
export async function signedDownloadUrl(ctx: OrgScope, fileId: string, variant: 'original' | 'thumbnail' = 'original'): Promise<string | null> {
  const file = await getFile(ctx, fileId);
  if (!file || file.status !== 'ready') return null;
  const key = variant === 'thumbnail' ? file.thumbnailKey : file.key;
  if (!key) return null;
  assertOwnKey(ctx.orgId, key);
  return getStorage().signDownload(key, DOWNLOAD_URL_TTL_SECONDS);
}

/** The screenshots of some incidents of this org, for the monitor page. */
export async function listIncidentScreenshots({ orgId }: OrgScope, incidentIds: string[]) {
  if (incidentIds.length === 0) return [];
  return withOrg(orgId, (tx) =>
    tx
      .select({
        id: files.id,
        incidentId: files.incidentId,
        status: files.status,
        originalName: files.originalName,
        rejectionReason: files.rejectionReason,
      })
      .from(files)
      .where(and(eq(files.organizationId, orgId), eq(files.kind, 'incident_screenshot'), inArray(files.incidentId, incidentIds)))
      .orderBy(files.createdAt),
  );
}

/** Files in "processing" (for the worker's start-up check, src/lib/queue/worker.ts). */
export async function listProcessingFileIds({ orgId }: OrgScope): Promise<string[]> {
  const rows = await withOrg(orgId, (tx) =>
    tx
      .select({ id: files.id })
      .from(files)
      .where(and(eq(files.organizationId, orgId), eq(files.status, 'processing'))),
  );
  return rows.map((r) => r.id);
}

/**
 * The public status page's logo: public only while the org publishes its
 * status page. The bucket stays private; this hands out a short-lived URL.
 */
export async function publicLogoUrl(statusPageSlug: string): Promise<string | null> {
  const org = await findPublicStatusPage(statusPageSlug);
  if (!org?.logoFileId) return null;
  return signedDownloadUrl({ orgId: org.id }, org.logoFileId);
}
