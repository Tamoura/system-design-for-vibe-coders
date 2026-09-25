import { randomUUID } from 'node:crypto';
import { hostname, userInfo } from 'node:os';
import { and, desc, eq, gte, inArray, isNull, lt, lte, sql, type SQL } from 'drizzle-orm';
import { schema } from '@/db';
import { withOrg, type TenantTx } from '@/db/tenant';
import {
  actionsIn,
  AUDIT_CATEGORIES,
  actorLabel,
  AUDIT_ACTIONS,
  categoryOf,
  csvRow,
  eventHash,
  findSecrets,
  GENESIS_HASH,
  isAuditAction,
  type AuditAction,
  type AuditCategory,
  type AuditChanges,
  type AuditSource,
  type AuditTarget,
} from '@/core/audit';
import type { AuditEvent } from '@/db/schema';

const { auditEvents, users } = schema;

/*
 * Lesson 7.3: the audit log, from the app's side.
 *
 *   recordAudit(tx, event)   write one event INSIDE the caller's transaction:
 *                            if the change commits, the event exists; if it
 *                            rolls back, the event never happened. Never
 *                            "after", never fire-and-forget.
 *   listAuditEvents(…)       the customer's page and CSV export: one org, its
 *                            plan's retention window, filters, keyset pagination.
 *
 * Staff-only reads (every org, platform events), the chain verifier and the
 * retention job connect as the database owner: src/lib/admin/audit.ts.
 */

export type AuditEventInput = {
  /** The tenant. null for platform events (staff roles, global flags). */
  orgId: string | null;
  action: AuditAction;
  source: AuditSource;
  target?: AuditTarget;
  /** Before/after of the changed fields only (diffFields in src/core/audit.ts). */
  changes?: AuditChanges;
  /** Small facts that are not changes: a key's prefix and scopes, an event count… Never a secret. */
  metadata?: Record<string, unknown>;
  /** Staff actions (lesson 7.1): the required reason or ticket link. */
  reason?: string;
  at?: Date;
};

/** When nobody asked: a webhook sync, a scheduled job. */
export const SYSTEM_SOURCE: AuditSource = { actor: { type: 'system', id: 'beacon', name: 'Beacon' }, via: 'worker' };

/** A command run by hand on a server (`npm run flags`, `npm run staff`): the OS user is the actor. */
export function cliAuditSource(command: string): AuditSource {
  let who = 'unknown';
  try {
    who = `${userInfo().username}@${hostname()}`;
  } catch {
    // no passwd entry (some containers): keep "unknown"
  }
  return { actor: { type: 'system', id: 'cli', name: `${command} (${who})` }, via: 'cli' };
}

/**
 * Who is acting, for lib functions called from several places: the context's
 * `audit` (set by requireMembership / publicApi / the admin routes), else the
 * user id alone (a script or a test), else the system.
 */
export function auditSourceOf(ctx: { audit?: AuditSource; userId?: string | null }): AuditSource {
  if (ctx.audit) return ctx.audit;
  if (ctx.userId) return { actor: { type: 'user', id: ctx.userId } };
  return SYSTEM_SOURCE;
}

/**
 * Write one audit event in the caller's transaction. For an org event the
 * transaction is a withOrg() one (row-level security checks the org); for a
 * platform event, an ordinary transaction as the database owner.
 *
 * The hash chain (tamper evidence): events of one org are serialised by a
 * transaction-scoped advisory lock, so each one reads the hash of the one
 * committed before it. The lock is per org: orgs never wait for each other.
 */
export async function recordAudit(tx: TenantTx, input: AuditEventInput): Promise<{ id: string; hash: string }> {
  if (!isAuditAction(input.action)) throw new Error(`Unknown audit action "${String(input.action)}": add it to AUDIT_ACTIONS in src/core/audit.ts`);
  const secrets = findSecrets({ changes: input.changes, metadata: input.metadata, target: input.target });
  if (secrets.length) throw new Error(`Refusing to write a secret into the audit log (${input.action}: ${secrets.join(', ')})`);

  const actor = { ...input.source.actor };
  let onBehalfOf = input.source.onBehalfOf ?? null;
  // Snapshot names and emails now: the user may be deleted later (lesson 7.3).
  if (actor.type === 'user' && actor.id && actor.name === undefined) {
    const [u] = await tx.select({ name: users.name, email: users.email }).from(users).where(eq(users.id, actor.id));
    actor.name = u?.name ?? null;
    actor.email = u?.email ?? null;
  }
  if (onBehalfOf && onBehalfOf.name === undefined) {
    const [u] = await tx.select({ name: users.name }).from(users).where(eq(users.id, onBehalfOf.id));
    onBehalfOf = { ...onBehalfOf, name: u?.name ?? null };
  }

  const chain = `audit:${input.orgId ?? 'platform'}`;
  await tx.execute(sql`select pg_advisory_xact_lock(hashtext(${chain}))`);
  const [previous] = await tx
    .select({ hash: auditEvents.hash })
    .from(auditEvents)
    .where(input.orgId ? eq(auditEvents.organizationId, input.orgId) : isNull(auditEvents.organizationId))
    .orderBy(desc(auditEvents.seq))
    .limit(1);
  const prevHash = previous?.hash ?? GENESIS_HASH;

  const event = {
    id: randomUUID(),
    organizationId: input.orgId,
    occurredAt: input.at ?? new Date(),
    action: input.action,
    actorType: actor.type,
    actorId: actor.id ?? null,
    actorName: actor.name ?? null,
    actorEmail: actor.email ?? null,
    onBehalfOfId: onBehalfOf?.id ?? null,
    onBehalfOfName: onBehalfOf?.name ?? null,
    targetType: input.target?.type ?? null,
    targetId: input.target?.id ?? null,
    targetName: input.target?.name ?? null,
    ipAddress: input.source.ip ?? null,
    userAgent: input.source.userAgent?.slice(0, 300) ?? null,
    requestId: input.source.requestId ?? null,
    via: input.source.via ?? null,
    reason: input.reason ?? null,
    changes: input.changes && Object.keys(input.changes).length ? input.changes : null,
    metadata: input.metadata && Object.keys(input.metadata).length ? input.metadata : null,
  };
  const hash = eventHash(prevHash, event);
  await tx.insert(auditEvents).values({
    ...event,
    category: categoryOf(input.action),
    prevHash,
    hash,
  });
  return { id: event.id, hash };
}

/* ---------------------------------------------------------------------------
 * The customer's view (lesson 7.3 🟡): Settings → Audit log.
 * ------------------------------------------------------------------------- */

export type AuditFilters = {
  /** A member's user id, or 'staff' (Beacon support), or 'api_key' (any API key). */
  actor?: string;
  category?: AuditCategory;
  targetType?: string;
  targetId?: string;
  from?: Date;
  to?: Date;
};

/** The target types Beacon records, for the filter. */
export const AUDIT_TARGET_TYPES = ['monitor', 'member', 'invitation', 'api_key', 'webhook_endpoint', 'organization', 'status_page', 'alert_policy', 'escalation_policy', 'subscription', 'user'] as const;

/**
 * The page's and the API's query string → filters. Unknown values are
 * dropped rather than trusted (a category must be one of the registry's,
 * dates must be YYYY-MM-DD, whole UTC days).
 */
export function parseAuditQuery(params: URLSearchParams): { filters: AuditFilters; before?: number } {
  const get = (k: string) => params.get(k)?.trim() || undefined;
  const day = (v: string | undefined, end: boolean) => (v && /^\d{4}-\d{2}-\d{2}$/.test(v) ? new Date(`${v}T${end ? '23:59:59.999' : '00:00:00.000'}Z`) : undefined);
  const category = get('category');
  const actor = get('actor');
  const targetType = get('target_type');
  const before = Number(get('before'));
  return {
    filters: {
      actor: actor === 'staff' || actor === 'api_key' || (actor && /^[0-9a-f-]{36}$/i.test(actor)) ? actor : undefined,
      category: category && (AUDIT_CATEGORIES as readonly string[]).includes(category) ? (category as AuditCategory) : undefined,
      targetType: targetType && (AUDIT_TARGET_TYPES as readonly string[]).includes(targetType) ? targetType : undefined,
      targetId: get('target_id')?.slice(0, 100),
      from: day(get('from'), false),
      to: day(get('to'), true),
    },
    before: Number.isSafeInteger(before) && before > 0 ? before : undefined,
  };
}

export const AUDIT_PAGE_SIZE = 50;
/** The CSV export's ceiling: a year of a busy org fits; beyond it, narrow the dates. */
export const AUDIT_EXPORT_MAX_ROWS = 20_000;

/**
 * One page of an org's events, newest first, within its plan's retention
 * window. Keyset pagination on `seq` ("the events before this one"), which
 * stays fast on page 2,000 where OFFSET would read 100,000 rows.
 */
export async function listAuditEvents(
  orgId: string,
  filters: AuditFilters,
  opts: { retentionDays: number; limit?: number; before?: number; now?: Date },
): Promise<{ rows: AuditEvent[]; nextBefore: number | null }> {
  const limit = opts.limit ?? AUDIT_PAGE_SIZE;
  const oldest = new Date((opts.now ?? new Date()).getTime() - opts.retentionDays * 86_400_000);
  const where: SQL[] = [eq(auditEvents.organizationId, orgId), gte(auditEvents.occurredAt, oldest)];
  if (filters.actor === 'staff' || filters.actor === 'api_key') where.push(eq(auditEvents.actorType, filters.actor));
  else if (filters.actor) where.push(eq(auditEvents.actorId, filters.actor));
  // The category is also stored on the row (indexed); the action list keeps the filter honest if categories move.
  if (filters.category) where.push(eq(auditEvents.category, filters.category), inArray(auditEvents.action, actionsIn(filters.category)));
  if (filters.targetType) where.push(eq(auditEvents.targetType, filters.targetType));
  if (filters.targetId) where.push(eq(auditEvents.targetId, filters.targetId));
  if (filters.from) where.push(gte(auditEvents.occurredAt, filters.from));
  if (filters.to) where.push(lte(auditEvents.occurredAt, filters.to));
  if (opts.before !== undefined) where.push(lt(auditEvents.seq, opts.before));

  const rows = await withOrg(orgId, (tx) =>
    tx
      .select()
      .from(auditEvents)
      .where(and(...where))
      .orderBy(desc(auditEvents.seq))
      .limit(limit + 1),
  );
  const hasMore = rows.length > limit;
  const page = hasMore ? rows.slice(0, limit) : rows;
  return { rows: page, nextBefore: hasMore ? page[page.length - 1].seq : null };
}

/**
 * What the CUSTOMER sees of an event. Beacon staff appear as "Beacon support"
 * (with "on behalf of Ana" during impersonation): not their name, email, IP
 * or the internal reason. Everything else is the customer's own data.
 */
export function toCustomerView(e: AuditEvent) {
  const staff = e.actorType === 'staff';
  return {
    id: e.id,
    occurredAt: e.occurredAt,
    action: e.action,
    category: e.category,
    description: isAuditAction(e.action) ? AUDIT_ACTIONS[e.action].description : e.action,
    actor: actorLabel(e),
    actorType: e.actorType,
    actorId: staff ? null : e.actorId,
    targetType: e.targetType,
    targetId: e.targetId,
    targetName: e.targetName,
    ipAddress: staff ? null : e.ipAddress,
    userAgent: staff ? null : e.userAgent,
    requestId: e.requestId,
    via: e.via,
    changes: e.changes as AuditChanges | null,
    metadata: e.metadata as Record<string, unknown> | null,
  };
}

export type CustomerAuditEvent = ReturnType<typeof toCustomerView>;

export const CSV_HEADER = ['occurred_at', 'action', 'category', 'actor', 'actor_type', 'target_type', 'target_id', 'target_name', 'ip_address', 'user_agent', 'request_id', 'changes', 'metadata'];

export function toCsvLine(e: CustomerAuditEvent): string {
  return csvRow([e.occurredAt, e.action, e.category, e.actor, e.actorType, e.targetType, e.targetId, e.targetName, e.ipAddress, e.userAgent, e.requestId, e.changes, e.metadata]);
}
