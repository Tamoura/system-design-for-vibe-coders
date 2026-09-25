import { and, desc, eq, getTableColumns, getTableName, is, isNull, sql, type SQL } from 'drizzle-orm';
import { PgTable, type PgColumn } from 'drizzle-orm/pg-core';
import { db, schema } from '@/db';
import { withOrg, type TenantTx } from '@/db/tenant';
import { statusGrantsAccess } from '@/core/plans';
import { DAY_MS, ORG_DELETION_GRACE_DAYS, ORG_EXPORT_TTL_DAYS } from '@/core/retention';
import { isUuid } from '@/core/validation';
import type { AuditSource } from '@/core/audit';
import { auditSourceOf, recordAudit, SYSTEM_SOURCE } from '../audit';
import { AccessError, InvalidRequestError } from '../errors';
import { enqueueInTx } from '../queue';
import type { JobContext } from '../queue/queues';
import { getStorage } from '../storage';
import { logger } from '../observability/logger';

const { organizations, memberships, users, orgExports, subscriptions, files } = schema;

/*
 * Lesson 8.1 (GDPR for a SaaS processor): the ORGANIZATION's data rights.
 * The customer (the org) is the controller of its data; Beacon is the
 * processor and must be able to hand it all back, and to delete it all.
 *
 *   export   owner asks ─► org_exports row + `org.export` job (same transaction)
 *            worker ─► every tenant table's rows for this org ─► one JSON file in
 *            object storage ─► owner downloads it by a 5-minute signed URL; the file
 *            expires after 7 days (the retention job deletes it)
 *   delete   owner asks (typing the slug) ─► deletion_scheduled_for = now + 7 days,
 *            checks stop, status page gone, a delayed `org.delete` job; cancel any time
 *            before ─► the job deletes the org's files from storage, then the org row,
 *            and Postgres cascades to every tenant table ─► a platform audit event
 *
 * Not built (lesson 8.1's 🔴 exercise): per-tenant data keys to crypto-shred, a
 * deletion that reaches an analytics warehouse or a search index (Beacon keeps
 * both in Postgres, so the cascade covers them), and a Stripe customer deletion.
 */

type OwnerCtx = { orgId: string; userId: string; audit?: AuditSource };

/* ---------------------------------------------------------------------------
 * Export
 * ------------------------------------------------------------------------- */

/**
 * Tables that carry organization_id but are NOT in the export, and why. Every
 * other tenant table is exported automatically: a table added next month is in
 * the export without anyone remembering to add it (tests/privacy.test.ts checks
 * this list against the database).
 */
export const NOT_EXPORTED: Record<string, string> = {
  memberships: 'exported as "members", with each person’s name and email',
  presence: 'who had a page open in the last 30 seconds: ephemeral',
  feature_flag_overrides: 'Beacon’s own configuration, not customer data',
  impersonation_sessions: 'staff records; each impersonation is in the exported audit log',
  org_exports: 'the exports themselves',
};

/** Columns never exported: secrets (even encrypted) and derived data. JS property names. */
const OMIT: Record<string, string[]> = {
  webhook_endpoints: ['secretEncrypted', 'legacySecret'],
  api_keys: ['keyHash'],
  invitations: ['tokenHash'],
  incident_updates: ['search'],
};

type TenantTable = { name: string; table: PgTable; orgColumn: PgColumn };

/** Every table in the schema with an organizationId column, found by looking, not by a list. */
export function tenantTables(): TenantTable[] {
  return (Object.values(schema) as unknown[])
    .filter((t): t is PgTable => is(t, PgTable))
    .map((table) => ({ table, name: getTableName(table), orgColumn: (getTableColumns(table) as Record<string, PgColumn>).organizationId }))
    .filter((t) => t.orgColumn !== undefined)
    .sort((a, b) => a.name.localeCompare(b.name));
}

/** The whole export document for one org. Runs in the worker, inside withOrg (RLS applies). */
export async function buildOrgExport(orgId: string, now = new Date()) {
  return withOrg(orgId, async (tx) => {
    const [org] = await tx.select().from(organizations).where(eq(organizations.id, orgId));
    if (!org) return null;
    const { slackWebhookUrlEncrypted, legacySlackWebhookUrl, ...orgFields } = org;
    const members = await tx
      .select({ userId: users.id, name: users.name, email: users.email, role: memberships.role, joinedAt: memberships.createdAt })
      .from(memberships)
      .innerJoin(users, eq(users.id, memberships.userId))
      .where(eq(memberships.organizationId, orgId));
    const tables: Record<string, unknown[]> = {};
    for (const t of tenantTables()) {
      if (NOT_EXPORTED[t.name]) continue;
      const rows = (await tx.select().from(t.table).where(eq(t.orgColumn, orgId))) as Record<string, unknown>[];
      const omit = OMIT[t.name] ?? [];
      tables[t.name] = rows.map((r) => Object.fromEntries(Object.entries(r).filter(([k]) => !omit.includes(k))));
    }
    return {
      format: 'beacon-organization-export',
      version: 1,
      exportedAt: now.toISOString(),
      organization: { ...orgFields, slackConnected: Boolean(slackWebhookUrlEncrypted ?? legacySlackWebhookUrl) },
      members,
      tables,
    };
  });
}

/** An owner asks for an export. The job is enqueued in the same transaction as the row. */
export async function requestOrgExport(ctx: OwnerCtx, now = new Date()): Promise<{ id: string }> {
  return withOrg(ctx.orgId, async (tx) => {
    // One at a time: a second click while one is being built returns the same export.
    const [pending] = await tx
      .select({ id: orgExports.id })
      .from(orgExports)
      .where(and(eq(orgExports.organizationId, ctx.orgId), eq(orgExports.status, 'pending')));
    if (pending) return pending;
    const [row] = await tx
      .insert(orgExports)
      .values({ organizationId: ctx.orgId, requestedBy: ctx.userId, expiresAt: new Date(now.getTime() + ORG_EXPORT_TTL_DAYS * DAY_MS) })
      .returning({ id: orgExports.id });
    await recordAudit(tx, { orgId: ctx.orgId, action: 'org.export_requested', source: auditSourceOf(ctx), target: { type: 'export', id: row.id } });
    await enqueueInTx(tx, 'org.export', { orgId: ctx.orgId, exportId: row.id }, { key: row.id, group: ctx.orgId });
    return row;
  });
}

/** The `org.export` job: build, store, mark ready. Idempotent (a ready export is not rebuilt). */
export async function runOrgExport(data: { orgId: string; exportId: string }, job: Pick<JobContext, 'lastAttempt'> = { lastAttempt: true }) {
  const { orgId, exportId } = data;
  const [row] = await withOrg(orgId, (tx) => tx.select().from(orgExports).where(and(eq(orgExports.organizationId, orgId), eq(orgExports.id, exportId))));
  if (!row || row.status !== 'pending') return { skipped: row ? row.status : 'export deleted' };
  try {
    const doc = await buildOrgExport(orgId);
    if (!doc) return { skipped: 'organization deleted' };
    const bytes = new TextEncoder().encode(JSON.stringify(doc, null, 2));
    const key = `orgs/${orgId}/exports/${exportId}.json`; // under the org's prefix, like every file (lesson 2.2)
    await getStorage().put(key, bytes, 'application/json');
    await withOrg(orgId, (tx) =>
      tx.update(orgExports).set({ status: 'ready', storageKey: key, sizeBytes: bytes.length, completedAt: new Date(), error: null }).where(and(eq(orgExports.organizationId, orgId), eq(orgExports.id, exportId))),
    );
    return { exportId, bytes: bytes.length, tables: Object.keys(doc.tables).length };
  } catch (err) {
    const message = (err as Error).message.slice(0, 300);
    await withOrg(orgId, (tx) =>
      tx.update(orgExports).set({ error: message, ...(job.lastAttempt && { status: 'failed' as const }) }).where(and(eq(orgExports.organizationId, orgId), eq(orgExports.id, exportId))),
    );
    throw err; // the queue retries
  }
}

export async function listOrgExports({ orgId }: { orgId: string }) {
  return withOrg(orgId, (tx) => tx.select().from(orgExports).where(eq(orgExports.organizationId, orgId)).orderBy(desc(orgExports.createdAt)).limit(10));
}

/** A 5-minute download link for a ready, unexpired export of THIS org (404 otherwise). Audited. */
export async function exportDownloadUrl(ctx: OwnerCtx, exportId: string, now = new Date()): Promise<string> {
  if (!isUuid(exportId)) throw new AccessError('not_found');
  const key = await withOrg(ctx.orgId, async (tx) => {
    const [row] = await tx.select().from(orgExports).where(and(eq(orgExports.organizationId, ctx.orgId), eq(orgExports.id, exportId)));
    if (!row || row.status !== 'ready' || !row.storageKey || row.expiresAt <= now) return null;
    await recordAudit(tx, { orgId: ctx.orgId, action: 'org.export_downloaded', source: auditSourceOf(ctx), target: { type: 'export', id: row.id } });
    return row.storageKey;
  });
  if (!key) throw new AccessError('not_found');
  return getStorage().signDownload(key, 300);
}

/* ---------------------------------------------------------------------------
 * Deletion (offboarding)
 * ------------------------------------------------------------------------- */

/** Why the org cannot be deleted right now (empty = it can). */
export async function orgDeletionBlockers(tx: TenantTx, orgId: string): Promise<string[]> {
  const subs = await tx.select().from(subscriptions).where(eq(subscriptions.organizationId, orgId));
  // Deleting an org that still pays would leave a subscription billing nobody.
  const paying = subs.some((s) => statusGrantsAccess(s.status) && !s.cancelAtPeriodEnd);
  return paying ? ['It has an active paid subscription. Cancel it in Billing first (it runs until the end of the period).'] : [];
}

/**
 * Schedule the deletion, in the caller's transaction (also used when the last
 * member deletes their account). Checks stop at once; the status page is gone.
 */
export async function scheduleOrgDeletionInTx(tx: TenantTx, orgId: string, opts: { requestedBy: string | null; source: AuditSource; now?: Date }) {
  const now = opts.now ?? new Date();
  const at = new Date(now.getTime() + ORG_DELETION_GRACE_DAYS * DAY_MS);
  const [org] = await tx
    .update(organizations)
    .set({ deletionScheduledFor: at, deletionRequestedBy: opts.requestedBy })
    .where(and(eq(organizations.id, orgId), isNull(organizations.deletionScheduledFor)))
    .returning({ id: organizations.id, name: organizations.name });
  if (!org) return null; // already scheduled
  await recordAudit(tx, {
    orgId,
    action: 'org.deletion_requested',
    source: opts.source,
    target: { type: 'organization', id: orgId, name: org.name },
    metadata: { scheduled_for: at.toISOString(), grace_days: ORG_DELETION_GRACE_DAYS },
  });
  // A delayed job. Its key includes the date, so cancel-then-request-again schedules a new one;
  // the job itself re-reads the row and does nothing if the deletion was cancelled or moved.
  await enqueueInTx(tx, 'org.delete', { orgId }, { key: `${orgId}@${at.toISOString()}`, startAfter: at });
  return at;
}

export async function requestOrgDeletion(ctx: OwnerCtx & { orgSlug: string }, confirmSlug: string, now = new Date()): Promise<Date> {
  if (confirmSlug.trim() !== ctx.orgSlug) throw new InvalidRequestError('confirmation_mismatch', `Type the organization's URL name, ${ctx.orgSlug}, to confirm.`);
  return withOrg(ctx.orgId, async (tx) => {
    const blockers = await orgDeletionBlockers(tx, ctx.orgId);
    if (blockers.length) throw new InvalidRequestError('deletion_blocked', blockers.join(' '));
    const at = await scheduleOrgDeletionInTx(tx, ctx.orgId, { requestedBy: ctx.userId, source: auditSourceOf(ctx), now });
    if (!at) throw new InvalidRequestError('already_scheduled', 'This organization is already scheduled for deletion.');
    return at;
  });
}

export async function cancelOrgDeletion(ctx: OwnerCtx): Promise<boolean> {
  return withOrg(ctx.orgId, async (tx) => {
    const [before] = await tx.select({ at: organizations.deletionScheduledFor, name: organizations.name }).from(organizations).where(eq(organizations.id, ctx.orgId));
    if (!before?.at) return false;
    await tx.update(organizations).set({ deletionScheduledFor: null, deletionRequestedBy: null }).where(eq(organizations.id, ctx.orgId));
    await recordAudit(tx, { orgId: ctx.orgId, action: 'org.deletion_cancelled', source: auditSourceOf(ctx), target: { type: 'organization', id: ctx.orgId, name: before.name } });
    return true;
  });
}

/**
 * The `org.delete` job, after the grace period. Files first (object storage
 * has no cascade), then the org row: every tenant table references it with
 * ON DELETE CASCADE, so Postgres removes the rest in the same statement.
 */
export async function purgeOrganization(orgId: string, now = new Date(), source: AuditSource = SYSTEM_SOURCE) {
  const [org] = await db.select().from(organizations).where(eq(organizations.id, orgId));
  if (!org) return { skipped: 'already deleted' };
  if (!org.deletionScheduledFor) return { skipped: 'deletion cancelled' };
  if (org.deletionScheduledFor > now) return { skipped: `scheduled for ${org.deletionScheduledFor.toISOString()}` };

  const keys = await withOrg(orgId, async (tx) => {
    const fileKeys = await tx.select({ key: files.key, thumb: files.thumbnailKey }).from(files).where(eq(files.organizationId, orgId));
    const exportKeys = await tx.select({ key: orgExports.storageKey }).from(orgExports).where(eq(orgExports.organizationId, orgId));
    return [...fileKeys.flatMap((f) => [f.key, f.thumb]), ...exportKeys.map((e) => e.key)].filter((k): k is string => Boolean(k));
  });
  const storage = getStorage();
  for (const key of keys) await storage.delete(key); // idempotent: a missing object is fine

  const before = await countOrgRows(orgId);
  await db.transaction(async (tx) => {
    await tx.delete(organizations).where(eq(organizations.id, orgId));
    // The org's own audit log went with it (it was the customer's data); the fact of the deletion
    // stays in the PLATFORM log, where Beacon keeps evidence of what it did and when.
    await recordAudit(tx, {
      orgId: null,
      action: 'org.deleted',
      source,
      target: { type: 'organization', id: orgId, name: org.name },
      metadata: { slug: org.slug, rows_deleted: Object.values(before).reduce((a, b) => a + b, 0), files_deleted: keys.length, requested_at_grace_days: ORG_DELETION_GRACE_DAYS },
    });
  });
  const left = Object.entries(await countOrgRows(orgId)).filter(([, n]) => n > 0);
  if (left.length) {
    logger.error({ orgId, left }, 'privacy.org_purge_incomplete');
    throw new Error(`Rows left after deleting org ${orgId}: ${left.map(([t, n]) => `${t}=${n}`).join(', ')}`);
  }
  return { deleted: orgId, files: keys.length };
}

/**
 * How many rows each table holds for an org, over EVERY table with an
 * organization_id column (asked of Postgres' catalog, so no table is
 * forgotten). The proof, after a deletion, that nothing is left. Owner only.
 */
export async function countOrgRows(orgId: string): Promise<Record<string, number>> {
  const tables = await ownerRows<{ table_name: string }>(
    sql`select c.table_name from information_schema.columns c join pg_class cl on cl.relname = c.table_name and cl.relkind = 'r'
        where c.table_schema = 'public' and c.column_name = 'organization_id' order by 1`,
  );
  const counts: Record<string, number> = {};
  for (const { table_name } of tables) {
    const [row] = await ownerRows<{ n: number }>(sql`select count(*)::int as n from ${sql.identifier(table_name)} where organization_id = ${orgId}`);
    counts[table_name] = row.n;
  }
  const [org] = await db.select({ id: organizations.id }).from(organizations).where(eq(organizations.id, orgId));
  counts.organizations = org ? 1 : 0;
  return counts;
}

/** A hand-written query as the database owner (postgres.js returns an array, PGlite `{ rows }`). */
async function ownerRows<T>(query: SQL): Promise<T[]> {
  const result = (await db.execute(query)) as unknown as T[] | { rows: T[] };
  return Array.isArray(result) ? result : result.rows;
}
