import { and, asc, desc, eq, inArray, isNull, lt, sql, type SQL } from 'drizzle-orm';
import { db, schema } from '@/db';
import { entitlementsFor } from '@/core/plans';
import { verifyChain } from '@/core/audit';
import type { AuditEvent } from '@/db/schema';
import { recordAudit, SYSTEM_SOURCE, type AuditEventInput } from '../audit';
import { logger } from '../observability/logger';

const { auditEvents, organizations } = schema;

/*
 * Lesson 7.3: the audit log from Beacon's side, as the database OWNER.
 *
 * Staff pages read every org's events and the platform's own (organization_id
 * NULL); the verifier recomputes the hash chains; the retention job deletes
 * what the plan no longer covers. None of this is reachable by a customer
 * request, so it is exempt from the "tenant tables only through withOrg()"
 * lint (tests/tenant-scoping.test.ts), like the activation funnel.
 */

/** A platform event (no org): a staff role granted, a global flag flipped. */
export async function recordPlatformAudit(input: Omit<AuditEventInput, 'orgId'>) {
  return db.transaction((tx) => recordAudit(tx, { ...input, orgId: null }));
}

/**
 * Walk one chain (an org's, or the platform's with `null`) and recompute
 * every hash. The worker runs it for every org once a day (`audit.verify`);
 * `npm run audit -- verify` runs it by hand.
 */
export async function verifyAuditChain(orgId: string | null) {
  const rows = await db
    .select()
    .from(auditEvents)
    .where(orgId ? eq(auditEvents.organizationId, orgId) : isNull(auditEvents.organizationId))
    .orderBy(asc(auditEvents.seq));
  return verifyChain(rows);
}

/** Every chain. A broken one is logged at `error` level: an alert rule watches for `audit.chain_broken` (7.2). */
export async function verifyAllAuditChains() {
  const orgs = await db.select({ id: organizations.id, slug: organizations.slug }).from(organizations);
  const broken: { org: string; problems: number }[] = [];
  let checked = 0;
  for (const org of [...orgs, { id: null, slug: '(platform)' }]) {
    const result = await verifyAuditChain(org.id);
    checked += result.checked;
    if (!result.ok) {
      broken.push({ org: org.slug, problems: result.problems.length });
      logger.error({ org: org.slug, problems: result.problems.slice(0, 10) }, 'audit.chain_broken');
    }
  }
  return { chains: orgs.length + 1, events: checked, broken };
}

/**
 * Lesson 7.3 (🟡): retention by plan. The CUSTOMER sees their plan's window
 * (Business 365 days, Pro 30, Free none: listAuditEvents filters by it). Rows
 * are deleted once they are older than the plan's window AND older than
 * AUDIT_MIN_KEEP_DAYS, so an org that upgrades from Free sees its last month,
 * and Beacon keeps a month for its own security investigations. Platform
 * events are kept two years.
 *
 * Deleting whole old rows keeps each chain verifiable: the first remaining
 * event's prev_hash is simply trusted (src/core/audit.ts verifyChain).
 */
export const AUDIT_MIN_KEEP_DAYS = 30;
export const PLATFORM_AUDIT_KEEP_DAYS = 730;

export async function purgeExpiredAuditEvents(now = new Date()) {
  const orgs = await db.select({ id: organizations.id, plan: organizations.plan }).from(organizations);
  let deleted = 0;
  for (const org of orgs) {
    const keepDays = Math.max(entitlementsFor(org.plan).auditLogRetentionDays, AUDIT_MIN_KEEP_DAYS);
    const cutoff = new Date(now.getTime() - keepDays * 86_400_000);
    const rows = await db
      .delete(auditEvents)
      .where(and(eq(auditEvents.organizationId, org.id), lt(auditEvents.occurredAt, cutoff)))
      .returning({ id: auditEvents.id });
    deleted += rows.length;
  }
  const platformCutoff = new Date(now.getTime() - PLATFORM_AUDIT_KEEP_DAYS * 86_400_000);
  const platform = await db
    .delete(auditEvents)
    .where(and(isNull(auditEvents.organizationId), lt(auditEvents.occurredAt, platformCutoff)))
    .returning({ id: auditEvents.id });
  deleted += platform.length;
  if (deleted > 0) await recordPlatformAudit({ action: 'audit.retention_purged', source: SYSTEM_SOURCE, metadata: { deleted } });
  return { deleted };
}

/** Staff: the latest events across Beacon, optionally one org's, or staff actions only. */
export async function listAuditForStaff(filters: { orgId?: string | null; staffOnly?: boolean; before?: number; limit?: number } = {}) {
  const where: SQL[] = [];
  if (filters.orgId === null) where.push(isNull(auditEvents.organizationId));
  else if (filters.orgId) where.push(eq(auditEvents.organizationId, filters.orgId));
  if (filters.staffOnly) where.push(inArray(auditEvents.actorType, ['staff']));
  if (filters.before !== undefined) where.push(lt(auditEvents.seq, filters.before));
  const rows: (AuditEvent & { orgSlug: string | null })[] = await db
    .select({ ...auditEventColumns(), orgSlug: organizations.slug })
    .from(auditEvents)
    .leftJoin(organizations, eq(organizations.id, auditEvents.organizationId))
    .where(where.length ? and(...where) : undefined)
    .orderBy(desc(auditEvents.seq))
    .limit(filters.limit ?? 100);
  return rows;
}

function auditEventColumns() {
  const { id, seq, organizationId, occurredAt, action, category, actorType, actorId, actorName, actorEmail, onBehalfOfId, onBehalfOfName, targetType, targetId, targetName, ipAddress, userAgent, requestId, via, reason, changes, metadata, prevHash, hash } =
    auditEvents;
  return { id, seq, organizationId, occurredAt, action, category, actorType, actorId, actorName, actorEmail, onBehalfOfId, onBehalfOfName, targetType, targetId, targetName, ipAddress, userAgent, requestId, via, reason, changes, metadata, prevHash, hash };
}

/** For tests and the verifier's own test: how many events an org has (as the owner). */
export async function countAuditEvents(orgId: string | null) {
  const [row] = await db
    .select({ n: sql<number>`count(*)::int` })
    .from(auditEvents)
    .where(orgId ? eq(auditEvents.organizationId, orgId) : isNull(auditEvents.organizationId));
  return row.n;
}

