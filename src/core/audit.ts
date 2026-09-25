import { createHash } from 'node:crypto';

/*
 * Lesson 7.3: the audit log's rules, as pure code (no database).
 *
 * An audit event is EVIDENCE, not debugging output: "who did what to which
 * thing, when and from where". Four things live here:
 *
 *   1. AUDIT_ACTIONS  the typed registry of every action Beacon records. One
 *                     dotted verb per action (`member.role_changed`), a
 *                     category for the filter, and a sentence for the UI and
 *                     the docs. recordAudit() refuses a name that is not here,
 *                     so three developers cannot invent "Updated monitor",
 *                     "monitor update" and "MONITOR_UPDATED".
 *   2. diffFields()   before/after of the fields that changed: never the
 *                     whole row, never a secret.
 *   3. findSecrets()  a last line of defence: an event whose changes or
 *                     metadata look like they carry a key, a token or a
 *                     password is refused.
 *   4. the hash chain (lesson 7.3 🔴, tamper evidence): each event stores
 *                     hash = sha256(prev_hash + canonical JSON of the event).
 *                     Editing or deleting any past row breaks every hash
 *                     after it, and verifyChain() says where.
 */

export const AUDIT_CATEGORIES = ['members', 'monitors', 'integrations', 'billing', 'settings', 'support', 'platform'] as const;
export type AuditCategory = (typeof AUDIT_CATEGORIES)[number];

type ActionSpec = { category: AuditCategory; description: string };

export const AUDIT_ACTIONS = {
  // Members and invitations (lessons 1.2, 1.3)
  'member.invited': { category: 'members', description: 'Invited someone to the organization' },
  'member.invitation_resent': { category: 'members', description: 'Resent an invitation (a new link; the old one stopped working)' },
  'member.invitation_revoked': { category: 'members', description: 'Revoked an open invitation' },
  'member.joined': { category: 'members', description: 'Accepted an invitation and joined' },
  'member.role_changed': { category: 'members', description: "Changed a member's role" },
  'member.account_deleted': { category: 'members', description: 'A member deleted their Beacon account and left (lesson 8.1)' },
  // Monitors (the product). Pausing is audited because it silences alerts.
  'monitor.created': { category: 'monitors', description: 'Created a monitor' },
  'monitor.updated': { category: 'monitors', description: 'Changed a monitor (name, URL or interval)' },
  'monitor.paused': { category: 'monitors', description: 'Paused a monitor: no checks, no alerts' },
  'monitor.resumed': { category: 'monitors', description: 'Resumed a paused monitor' },
  'monitor.deleted': { category: 'monitors', description: 'Deleted a monitor and its history' },
  // Lesson 8.2: what the AI did, and what a person published.
  'incident.summary_generated': { category: 'monitors', description: 'The AI wrote a draft summary of an incident (model and provider in the details)' },
  'incident.summary_published': { category: 'monitors', description: 'Published an incident summary to the public status page' },
  // Integrations (lessons 5.2, 5.3)
  'api_key.created': { category: 'integrations', description: 'Created an API key (only its prefix is recorded)' },
  'api_key.revoked': { category: 'integrations', description: 'Revoked an API key' },
  'webhook.created': { category: 'integrations', description: 'Added a webhook endpoint' },
  'webhook.enabled': { category: 'integrations', description: 'Re-enabled a webhook endpoint' },
  'webhook.disabled': { category: 'integrations', description: 'Disabled a webhook endpoint' },
  'webhook.deleted': { category: 'integrations', description: 'Deleted a webhook endpoint' },
  // Settings that decide who gets alerted, and what the world sees
  'org.renamed': { category: 'settings', description: 'Renamed the organization' },
  'status_page.published': { category: 'settings', description: 'Published the public status page' },
  'status_page.unpublished': { category: 'settings', description: 'Hid the public status page' },
  'alerts.settings_changed': { category: 'settings', description: 'Changed the organization alert policy or Slack channel' },
  'escalation.policy_changed': { category: 'settings', description: 'Changed the escalation policy' },
  // Lesson 8.1: GDPR, portability and erasure
  'org.export_requested': { category: 'settings', description: "Asked for an export of all the organization's data" },
  'org.export_downloaded': { category: 'settings', description: 'Downloaded an export of the organization' },
  'org.deletion_requested': { category: 'settings', description: 'Asked to delete the organization (after a grace period)' },
  'org.deletion_cancelled': { category: 'settings', description: 'Cancelled the deletion of the organization' },
  'ai.summaries_enabled': { category: 'settings', description: 'Turned on AI incident summaries (incident data is sent to the AI provider)' },
  'ai.summaries_disabled': { category: 'settings', description: 'Turned off AI incident summaries' },
  // Billing (lessons 3.1, 3.2)
  'billing.plan_changed': { category: 'billing', description: 'The plan changed (a Stripe subscription update, or Beacon support)' },
  'billing.trial_extended': { category: 'billing', description: 'Beacon support extended the trial' },
  'billing.plan_comped': { category: 'billing', description: 'Beacon support gave the organization a plan free of charge' },
  'billing.comp_removed': { category: 'billing', description: 'Beacon support removed a complimentary plan' },
  // Beacon support (lesson 7.1). These appear in the CUSTOMER's log too.
  'support.impersonation_started': { category: 'support', description: 'Beacon support started viewing the account (read-only)' },
  'support.impersonation_ended': { category: 'support', description: 'Beacon support stopped viewing the account' },
  'support.invitation_resent': { category: 'support', description: 'Beacon support resent an invitation' },
  'support.verification_resent': { category: 'support', description: 'Beacon support resent an email verification link' },
  'support.sessions_revoked': { category: 'support', description: 'Beacon support signed a user out everywhere' },
  // Platform events: Beacon's own staff and configuration, with no organization.
  'staff.granted': { category: 'platform', description: 'Granted a staff role' },
  'staff.revoked': { category: 'platform', description: 'Removed a staff member' },
  'flag.changed': { category: 'platform', description: 'Changed a feature flag rule (lesson 6.3)' },
  'flag.override_changed': { category: 'platform', description: 'Changed a per-organization flag override (lesson 6.3)' },
  'audit.retention_purged': { category: 'platform', description: 'Deleted audit events past their retention' },
  // Lesson 8.1: encryption at rest. Counts and key ids only, never a key or a secret.
  'account.data_exported': { category: 'platform', description: 'A user downloaded their personal data (lesson 8.1, GDPR Art. 15/20)' },
  'account.deleted': { category: 'platform', description: 'A user deleted their account (lesson 8.1, GDPR Art. 17)' },
  'org.deleted': { category: 'platform', description: "An organization's data was purged after its grace period (lesson 8.1)" },
  'retention.purged': { category: 'platform', description: 'Deleted data past its retention period (lesson 8.1)' },
  'secrets.encrypted': { category: 'platform', description: 'Encrypted stored secrets that were still in plain text (the Module 8 migration)' },
  'secrets.rewrapped': { category: 'platform', description: 'Re-wrapped the data keys of stored secrets with the current encryption key (key rotation)' },
} as const satisfies Record<string, ActionSpec>;

export type AuditAction = keyof typeof AUDIT_ACTIONS;

export function isAuditAction(value: unknown): value is AuditAction {
  return typeof value === 'string' && Object.hasOwn(AUDIT_ACTIONS, value);
}

export function categoryOf(action: AuditAction): AuditCategory {
  return AUDIT_ACTIONS[action].category;
}

/** The actions of one category, for the filter (and for a `category IN (…)` query). */
export function actionsIn(category: AuditCategory): AuditAction[] {
  return (Object.keys(AUDIT_ACTIONS) as AuditAction[]).filter((a) => AUDIT_ACTIONS[a].category === category);
}

/*
 * Who did it. The lesson's actor types: a person, an API key, Beacon staff,
 * or the system itself (a webhook sync, a scheduled job). Name and email are
 * SNAPSHOTS taken at event time: "actor 42" means nothing once the user is
 * deleted. (GDPR erasure can overwrite the snapshot with "Deleted user" and
 * keep the id: lesson 7.3, PII in audit logs.)
 */
export type AuditActorType = 'user' | 'api_key' | 'staff' | 'system';
export type AuditActor = { type: AuditActorType; id: string | null; name?: string | null; email?: string | null };

/** Where the request came from. Set once at the edge of the app (requireMembership, publicApi, the admin routes). */
export type AuditSource = {
  actor: AuditActor;
  /** Lesson 7.1: set while Beacon staff act inside a customer's account ("on behalf of Ana"). */
  onBehalfOf?: { id: string; name?: string | null; email?: string | null } | null;
  ip?: string | null;
  userAgent?: string | null;
  requestId?: string | null;
  via?: 'app' | 'api' | 'admin' | 'worker' | 'cli';
};

export type AuditTarget = { type: string; id: string | null; name?: string | null };

/** before/after of one changed field. */
export type FieldChange = { before: unknown; after: unknown };
export type AuditChanges = Record<string, FieldChange>;

/**
 * The fields that differ between `before` and `after`, limited to `fields`
 * (an allow-list: "diff specific fields, never whole rows"). Dates compare by
 * value and are stored as ISO strings.
 */
export function diffFields<T extends Record<string, unknown>>(before: Partial<T> | null, after: Partial<T> | null, fields: readonly (keyof T & string)[]): AuditChanges {
  const changes: AuditChanges = {};
  for (const field of fields) {
    const b = normalize(before?.[field]);
    const a = normalize(after?.[field]);
    if (JSON.stringify(b) !== JSON.stringify(a)) changes[field] = { before: b ?? null, after: a ?? null };
  }
  return changes;
}

function normalize(value: unknown): unknown {
  return value instanceof Date ? value.toISOString() : value;
}

/*
 * Secrets never go in the audit log. Beacon's secrets have recognisable
 * shapes (API keys `bk_live_…`, webhook secrets `whsec_…`, Stripe keys, Slack
 * webhook URLs), and some field names are always sensitive. recordAudit()
 * refuses an event that contains one: a loud bug in development beats a
 * breach in an export a customer mailed to their SIEM.
 */
const SECRET_KEYS = /^(password|secret|token|api_?key|key_hash|token_hash|authorization|cookie|slack_?webhook_?url)$/i;
const SECRET_VALUES = [/\bbk_(live|test)_[A-Za-z0-9_-]{16,}/, /\bwhsec_[A-Za-z0-9+/=_-]{10,}/, /\bsk_(live|test)_[A-Za-z0-9]{10,}/, /hooks\.slack\.com\/services\//];

/** Paths inside `value` that look like secrets (empty = fine). */
export function findSecrets(value: unknown, path = ''): string[] {
  if (value === null || value === undefined) return [];
  if (typeof value === 'string') return SECRET_VALUES.some((re) => re.test(value)) ? [path || '(value)'] : [];
  if (Array.isArray(value)) return value.flatMap((v, i) => findSecrets(v, `${path}[${i}]`));
  if (typeof value === 'object') {
    return Object.entries(value as Record<string, unknown>).flatMap(([k, v]) => {
      const p = path ? `${path}.${k}` : k;
      if (SECRET_KEYS.test(k) && v !== null && v !== undefined && typeof v !== 'boolean') return [p];
      return findSecrets(v, p);
    });
  }
  return [];
}

/* ---------------------------------------------------------------------------
 * Tamper evidence (lesson 7.3 🔴, the essentials of it): a hash chain per org.
 * ------------------------------------------------------------------------- */

/** JSON with sorted keys at every level, so the same event always hashes the same. */
export function canonicalJson(value: unknown): string {
  if (value === null || typeof value !== 'object') return JSON.stringify(value ?? null);
  if (value instanceof Date) return JSON.stringify(value.toISOString());
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`;
  const entries = Object.entries(value as Record<string, unknown>)
    .filter(([, v]) => v !== undefined)
    .sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0));
  return `{${entries.map(([k, v]) => `${JSON.stringify(k)}:${canonicalJson(v)}`).join(',')}}`;
}

/** The fields that are hashed: everything that makes the event evidence. */
export type HashableEvent = {
  id: string;
  organizationId: string | null;
  occurredAt: Date;
  action: string;
  actorType: string;
  actorId: string | null;
  actorName: string | null;
  actorEmail: string | null;
  onBehalfOfId: string | null;
  onBehalfOfName: string | null;
  targetType: string | null;
  targetId: string | null;
  targetName: string | null;
  ipAddress: string | null;
  userAgent: string | null;
  requestId: string | null;
  via: string | null;
  reason: string | null;
  changes: unknown;
  metadata: unknown;
};

/** The first event of a chain points at this. */
export const GENESIS_HASH = '0'.repeat(64);

/** Exactly the hashed fields, whatever else the row carries (seq, category, the hashes themselves). */
export function hashable(e: HashableEvent): HashableEvent {
  return {
    id: e.id,
    organizationId: e.organizationId,
    occurredAt: e.occurredAt,
    action: e.action,
    actorType: e.actorType,
    actorId: e.actorId,
    actorName: e.actorName,
    actorEmail: e.actorEmail,
    onBehalfOfId: e.onBehalfOfId,
    onBehalfOfName: e.onBehalfOfName,
    targetType: e.targetType,
    targetId: e.targetId,
    targetName: e.targetName,
    ipAddress: e.ipAddress,
    userAgent: e.userAgent,
    requestId: e.requestId,
    via: e.via,
    reason: e.reason,
    changes: e.changes,
    metadata: e.metadata,
  };
}

export function eventHash(prevHash: string, event: HashableEvent): string {
  const body = canonicalJson({ ...hashable(event), occurredAt: event.occurredAt.toISOString() });
  return createHash('sha256').update(prevHash).update('\n').update(body).digest('hex');
}

export type ChainProblem = { id: string; problem: 'hash_mismatch' | 'broken_link' };

/**
 * Walk one org's events in insertion order and recompute every hash. The
 * first row's prev_hash is trusted (older rows may have been deleted by the
 * retention policy); after that, each row must point at the previous one and
 * hash to what it says.
 */
export function verifyChain(rows: (HashableEvent & { prevHash: string; hash: string })[]): { ok: boolean; checked: number; problems: ChainProblem[] } {
  const problems: ChainProblem[] = [];
  let previous: string | null = null;
  for (const row of rows) {
    if (previous !== null && row.prevHash !== previous) problems.push({ id: row.id, problem: 'broken_link' });
    if (eventHash(row.prevHash, row) !== row.hash) problems.push({ id: row.id, problem: 'hash_mismatch' });
    previous = row.hash;
  }
  return { ok: problems.length === 0, checked: rows.length, problems };
}

/* ---------------------------------------------------------------------------
 * Presentation: the customer sees "Beacon support", never a staff email.
 * ------------------------------------------------------------------------- */

/**
 * Lesson 7.3 (🟡): how an actor is shown to the CUSTOMER.
 *   a user                      "Ana (ana@acme.test)"
 *   staff impersonating Ana     "Beacon support (on behalf of Ana)"
 *   staff                       "Beacon support"
 *   an API key                  "API key bk_live_Ab3x…"
 *   the system                  "Beacon" (e.g. a Stripe sync)
 */
export function actorLabel(e: { actorType: string; actorName: string | null; actorEmail: string | null; onBehalfOfName?: string | null }): string {
  if (e.actorType === 'staff') return e.onBehalfOfName ? `Beacon support (on behalf of ${e.onBehalfOfName})` : 'Beacon support';
  if (e.actorType === 'api_key') return `API key ${e.actorName ?? ''}`.trim();
  if (e.actorType === 'system') return e.actorName ?? 'Beacon';
  if (e.actorName && e.actorEmail) return `${e.actorName} (${e.actorEmail})`;
  return e.actorName ?? e.actorEmail ?? 'Deleted user';
}

/** One CSV field: quoted, and neutralised against spreadsheet formula injection (=, +, -, @). */
export function csvField(value: unknown): string {
  let s = value === null || value === undefined ? '' : typeof value === 'string' ? value : value instanceof Date ? value.toISOString() : JSON.stringify(value);
  if (/^[=+\-@\t\r]/.test(s)) s = `'${s}`;
  return `"${s.replace(/"/g, '""')}"`;
}

export function csvRow(values: unknown[]): string {
  return values.map(csvField).join(',');
}
