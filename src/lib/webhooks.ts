import { and, desc, eq, gte, inArray, sql } from 'drizzle-orm';
import { z } from 'zod';
import { db, schema } from '@/db';
import { withOrg, type TenantTx } from '@/db/tenant';
import { can } from '@/core/permissions';
import { toPublicId } from '@/core/ids';
import { assertPublicUrl, BlockedUrlError, safeFetch } from '@/core/safe-fetch';
import { generateWebhookSecret, shouldDisable, snippet, WEBHOOK_EVENT_TYPE_IDS, webhookHeaders, type WebhookEventType } from '@/core/webhooks';
import { isUuid } from '@/core/validation';
import type { Incident, Monitor } from '@/db/schema';
import { sendEmail } from './email';
import { AccessError, InvalidRequestError } from './errors';
import { enqueueInTx } from './queue';
import type { JobContext, JobData } from './queue/queues';
import { toApiIncident, toApiMonitor } from './public-api';
import { appUrl } from './urls';

const { webhookEndpoints, webhookEvents, webhookMessages, webhookAttempts, organizations, memberships, users } = schema;

/*
 * Lesson 5.3: outbound webhooks, a delivery system rather than a fetch() call.
 *
 *   the incident's transaction ─► recordWebhookEvent(): 1 event row
 *        + 1 message per subscribed, enabled endpoint + 1 `webhook.deliver` job each
 *   worker ─► deliverWebhook(): sign (Standard Webhooks) ─► safeFetch (SSRF guard,
 *        no redirects, 10 s timeout) ─► log the attempt ─► 2xx: delivered;
 *        else throw: the queue retries with backoff for ~1.5 days
 *   failing continuously for 5 days ─► endpoint disabled, admins emailed
 *   the delivery log (Settings → Webhooks) ─► resend one, or replay failed since…
 */

export const DELIVERY_TIMEOUT_MS = 10_000;
/** Webhooks only go to the standard web ports (lesson 5.3's "restrict ports"). */
export const WEBHOOK_PORTS = [80, 443] as const;

export const createEndpointInput = z.object({
  url: z.string().trim().url('Enter a full URL, like https://hooks.example.com/beacon'),
  description: z.string().trim().max(200).optional(),
  eventTypes: z.array(z.enum(WEBHOOK_EVENT_TYPE_IDS)).min(1, 'Pick at least one event type'),
});

type Scope = { orgId: string };
type Manager = Scope & { userId: string };

/** Lesson 5.3 (🟡): the URL is refused if it points inside our network, before anything is stored. */
async function assertWebhookUrl(url: string) {
  try {
    // Unlike a monitor, an endpoint must resolve now: we are about to send it events.
    await assertPublicUrl(url, { ports: WEBHOOK_PORTS });
  } catch (err) {
    if (err instanceof BlockedUrlError) throw new InvalidRequestError('blocked_url', `Beacon cannot send webhooks to this URL: ${err.message}.`);
    throw new InvalidRequestError('unresolvable_url', `Beacon cannot resolve this URL's host (${(err as Error).message}).`);
  }
}

/** Register an endpoint. Returns its signing secret ONCE (the UI shows it, then it is never sent back). */
export async function createEndpoint(ctx: Manager, input: z.infer<typeof createEndpointInput>): Promise<{ id: string; secret: string }> {
  await assertWebhookUrl(input.url);
  const secret = generateWebhookSecret();
  const [row] = await withOrg(ctx.orgId, (tx) =>
    tx
      .insert(webhookEndpoints)
      .values({ organizationId: ctx.orgId, url: input.url, description: input.description || null, eventTypes: [...new Set(input.eventTypes)], secret, createdBy: ctx.userId })
      .returning({ id: webhookEndpoints.id }),
  );
  return { id: row.id, secret };
}

export async function listEndpoints({ orgId }: Scope) {
  return withOrg(orgId, async (tx) => {
    const endpoints = await tx
      .select({
        id: webhookEndpoints.id,
        url: webhookEndpoints.url,
        description: webhookEndpoints.description,
        eventTypes: webhookEndpoints.eventTypes,
        enabled: webhookEndpoints.enabled,
        disabledReason: webhookEndpoints.disabledReason,
        failingSince: webhookEndpoints.failingSince,
        createdAt: webhookEndpoints.createdAt,
      })
      .from(webhookEndpoints)
      .where(eq(webhookEndpoints.organizationId, orgId))
      .orderBy(desc(webhookEndpoints.createdAt));
    return endpoints;
  });
}

/** One endpoint (without its secret) and its delivery log: every message with its attempts. */
export async function getEndpointLog({ orgId }: Scope, endpointId: string, opts: { limit?: number } = {}) {
  if (!isUuid(endpointId)) return null;
  return withOrg(orgId, async (tx) => {
    const [endpoint] = await tx
      .select()
      .from(webhookEndpoints)
      .where(and(eq(webhookEndpoints.organizationId, orgId), eq(webhookEndpoints.id, endpointId)));
    if (!endpoint) return null;
    const messages = await tx
      .select({ message: webhookMessages, eventType: webhookEvents.type })
      .from(webhookMessages)
      .innerJoin(webhookEvents, eq(webhookEvents.id, webhookMessages.eventId))
      .where(and(eq(webhookMessages.organizationId, orgId), eq(webhookMessages.endpointId, endpointId)))
      .orderBy(desc(webhookMessages.createdAt))
      .limit(opts.limit ?? 50);
    const attempts = messages.length
      ? await tx
          .select()
          .from(webhookAttempts)
          .where(and(eq(webhookAttempts.organizationId, orgId), inArray(webhookAttempts.messageId, messages.map((m) => m.message.id))))
          .orderBy(webhookAttempts.createdAt)
      : [];
    const { secret: _secret, ...safe } = endpoint; // the secret never leaves the server again
    return {
      endpoint: safe,
      messages: messages.map(({ message, eventType }) => ({
        ...message,
        webhookId: toPublicId('webhookMessage', message.id),
        eventType,
        attempts: attempts.filter((a) => a.messageId === message.id),
      })),
    };
  });
}

export async function setEndpointEnabled(ctx: Scope, endpointId: string, enabled: boolean) {
  if (!isUuid(endpointId)) throw new AccessError('not_found');
  const updated = await withOrg(ctx.orgId, (tx) =>
    tx
      .update(webhookEndpoints)
      // Re-enabling starts with a clean slate: the 5-day clock restarts.
      .set(enabled ? { enabled: true, disabledReason: null, failingSince: null } : { enabled: false, disabledReason: 'Disabled by a person.' })
      .where(and(eq(webhookEndpoints.organizationId, ctx.orgId), eq(webhookEndpoints.id, endpointId)))
      .returning({ id: webhookEndpoints.id }),
  );
  if (!updated.length) throw new AccessError('not_found');
}

export async function deleteEndpoint(ctx: Scope, endpointId: string) {
  if (!isUuid(endpointId)) throw new AccessError('not_found');
  const deleted = await withOrg(ctx.orgId, (tx) =>
    tx.delete(webhookEndpoints).where(and(eq(webhookEndpoints.organizationId, ctx.orgId), eq(webhookEndpoints.id, endpointId))).returning({ id: webhookEndpoints.id }),
  );
  if (!deleted.length) throw new AccessError('not_found');
}

/*
 * Events.
 */

/** The payload: the incident and its monitor, in the public API's shapes (lesson 5.2), so there is one contract. */
export function incidentPayload(type: WebhookEventType, incident: Incident, monitor: Monitor, at = new Date()) {
  return { type, timestamp: at.toISOString(), data: { incident: toApiIncident(incident), monitor: toApiMonitor(monitor) } };
}

/**
 * Record an event and fan it out, INSIDE the caller's transaction (the one
 * that opened or resolved the incident): the event, a message per enabled
 * endpoint subscribed to this type, and a `webhook.deliver` job per message.
 * All of it commits with the incident, or none of it (lesson 5.1).
 */
export async function recordWebhookEvent(tx: TenantTx, orgId: string, type: WebhookEventType, payload: object): Promise<number> {
  const endpoints = await tx
    .select({ id: webhookEndpoints.id })
    .from(webhookEndpoints)
    .where(and(eq(webhookEndpoints.organizationId, orgId), eq(webhookEndpoints.enabled, true), sql`${type} = any(${webhookEndpoints.eventTypes})`));
  if (endpoints.length === 0) return 0; // nobody listens: store nothing
  const [event] = await tx.insert(webhookEvents).values({ organizationId: orgId, type, payload }).returning({ id: webhookEvents.id });
  const messages = await tx
    .insert(webhookMessages)
    .values(endpoints.map((e) => ({ organizationId: orgId, endpointId: e.id, eventId: event.id })))
    .onConflictDoNothing()
    .returning({ id: webhookMessages.id, endpointId: webhookMessages.endpointId });
  for (const m of messages) {
    // Grouped by ENDPOINT: the worker lets one endpoint use at most 2 slots at a time.
    await enqueueInTx(tx, 'webhook.deliver', { orgId, messageId: m.id }, { key: m.id, group: m.endpointId });
  }
  return messages.length;
}

/** For the incident code: load the incident and its monitor in the same transaction, then record the event. */
export async function recordIncidentWebhook(tx: TenantTx, orgId: string, type: WebhookEventType, incidentId: string, at = new Date()): Promise<number> {
  const [row] = await tx
    .select({ incident: schema.incidents, monitor: schema.monitors })
    .from(schema.incidents)
    .innerJoin(schema.monitors, eq(schema.monitors.id, schema.incidents.monitorId))
    .where(and(eq(schema.incidents.organizationId, orgId), eq(schema.incidents.id, incidentId)));
  if (!row) return 0;
  return recordWebhookEvent(tx, orgId, type, incidentPayload(type, row.incident, row.monitor, at));
}

/*
 * Delivery.
 */

type DeliveryOutcome = { status: 'delivered' | 'skipped' | 'disabled'; statusCode?: number };

/**
 * The `webhook.deliver` job. Idempotent: a message that is no longer pending
 * was delivered (or given up on) by an earlier run. Throws on failure so the
 * queue retries; the receiver can drop a duplicate by its webhook-id.
 */
export async function deliverWebhook(job: JobData['webhook.deliver'], ctx: Pick<JobContext, 'attempt' | 'lastAttempt'> = { attempt: 1, lastAttempt: false }, now = new Date()): Promise<DeliveryOutcome> {
  const { orgId, messageId } = job;
  const row = await withOrg(orgId, async (tx) => {
    const [r] = await tx
      .select({ message: webhookMessages, endpoint: webhookEndpoints, event: webhookEvents })
      .from(webhookMessages)
      .innerJoin(webhookEndpoints, eq(webhookEndpoints.id, webhookMessages.endpointId))
      .innerJoin(webhookEvents, eq(webhookEvents.id, webhookMessages.eventId))
      .where(and(eq(webhookMessages.organizationId, orgId), eq(webhookMessages.id, messageId)));
    return r;
  });
  if (!row || row.message.status !== 'pending') return { status: 'skipped' };
  if (!row.endpoint.enabled) {
    await updateMessage(orgId, messageId, { status: 'failed' });
    return { status: 'disabled' };
  }

  // The body is the stored event, byte for byte the same on every retry.
  const body = JSON.stringify(row.event.payload);
  const webhookId = toPublicId('webhookMessage', messageId);
  const started = performance.now();
  let statusCode: number | null = null;
  let responseBody: string | null = null;
  let error: string | null = null;
  try {
    const res = await safeFetch(
      row.endpoint.url,
      { method: 'POST', body, headers: webhookHeaders(row.endpoint.secret, webhookId, body, now), signal: AbortSignal.timeout(DELIVERY_TIMEOUT_MS) },
      { maxRedirects: 0, ports: WEBHOOK_PORTS }, // a redirect is a failure: never follow one for a webhook
    );
    statusCode = res.status;
    responseBody = snippet(await res.text().catch(() => ''));
    if (res.status < 200 || res.status >= 300) error = `HTTP ${res.status}`;
  } catch (err) {
    const e = err as Error & { cause?: Error & { code?: string } };
    const blocked = err instanceof BlockedUrlError ? err : e.cause instanceof BlockedUrlError ? e.cause : null;
    error = blocked
      ? `Blocked: ${blocked.message}`
      : e.name === 'TimeoutError' || e.name === 'AbortError'
        ? `Timed out after ${DELIVERY_TIMEOUT_MS / 1000} s`
        : (e.cause?.code ?? e.cause?.message ?? e.message);
  }
  const durationMs = Math.round(performance.now() - started);

  // Record the attempt, and decide. The transaction must COMMIT (so the log
  // keeps the failure) before we throw to ask the queue for a retry.
  const result = await withOrg(orgId, async (tx) => {
    await tx.insert(webhookAttempts).values({ organizationId: orgId, messageId, trigger: job.manual ? 'manual' : 'automatic', statusCode, durationMs, responseBody, error });
    const counters = { attempts: sql`${webhookMessages.attempts} + 1`, lastAttemptAt: now };
    const thisMessage = and(eq(webhookMessages.organizationId, orgId), eq(webhookMessages.id, messageId));
    const thisEndpoint = and(eq(webhookEndpoints.organizationId, orgId), eq(webhookEndpoints.id, row.endpoint.id));
    if (!error) {
      await tx.update(webhookMessages).set({ ...counters, status: 'delivered', deliveredAt: now }).where(thisMessage);
      await tx.update(webhookEndpoints).set({ failingSince: null }).where(thisEndpoint); // healthy again: the 5-day clock stops
      return { kind: 'delivered' as const };
    }
    // A failure. Has this endpoint failed for long enough to give up on it?
    const failingSince = row.endpoint.failingSince ?? now;
    const disable = shouldDisable(failingSince, now);
    await tx
      .update(webhookEndpoints)
      .set(disable ? { failingSince, enabled: false, disabledReason: `Every delivery failed since ${failingSince.toISOString()}. Last error: ${error}` } : { failingSince })
      .where(thisEndpoint);
    await tx.update(webhookMessages).set({ ...counters, status: disable || ctx.lastAttempt ? 'failed' : 'pending' }).where(thisMessage);
    return disable ? { kind: 'disabled' as const, failingSince } : { kind: 'failed' as const };
  });

  if (result.kind === 'delivered') return { status: 'delivered', statusCode: statusCode ?? undefined };
  if (result.kind === 'disabled') {
    await emailAdminsEndpointDisabled(orgId, row.endpoint.id, row.endpoint.url, result.failingSince, error ?? 'unknown');
    return { status: 'disabled' };
  }
  throw new Error(`Webhook to ${row.endpoint.url} failed: ${error}`); // the queue retries with backoff
}

async function updateMessage(orgId: string, messageId: string, patch: Partial<typeof webhookMessages.$inferInsert>) {
  await withOrg(orgId, (tx) => tx.update(webhookMessages).set(patch).where(and(eq(webhookMessages.organizationId, orgId), eq(webhookMessages.id, messageId))));
}

/** Lesson 5.3 (🟡): tell the people who can fix it (roles with "integration.manage"). */
async function emailAdminsEndpointDisabled(orgId: string, endpointId: string, url: string, failingSince: Date, lastError: string) {
  const [org] = await db.select({ name: organizations.name, slug: organizations.slug }).from(organizations).where(eq(organizations.id, orgId));
  const people = await db.select({ email: users.email, role: memberships.role }).from(memberships).innerJoin(users, eq(users.id, memberships.userId)).where(eq(memberships.organizationId, orgId));
  for (const p of people.filter((m) => can(m.role, 'integration.manage'))) {
    await sendEmail({
      to: p.email,
      template: 'webhook-disabled',
      props: { orgName: org.name, endpointUrl: url, failingSince: failingSince.toISOString(), lastError, url: appUrl(`/${org.slug}/settings/webhooks/${endpointId}`) },
      idempotencyKey: `webhook-disabled:${endpointId}:${failingSince.toISOString()}:${p.email}`,
    });
  }
}

/*
 * Lesson 5.3 (🟡): the customer-facing controls on the delivery log.
 */

/** Send one message again, now (whatever happened before). */
export async function resendMessage(ctx: Scope, endpointId: string, messageId: string): Promise<void> {
  if (!isUuid(endpointId) || !isUuid(messageId)) throw new AccessError('not_found');
  const found = await requeue(ctx.orgId, [eq(webhookMessages.endpointId, endpointId), eq(webhookMessages.id, messageId)], false);
  if (found === 0) throw new AccessError('not_found');
}

/** Replay every FAILED message of an endpoint created since a moment ("everything since yesterday"). */
export async function replayFailedSince(ctx: Scope, endpointId: string, since: Date): Promise<number> {
  if (!isUuid(endpointId)) throw new AccessError('not_found');
  return requeue(ctx.orgId, [eq(webhookMessages.endpointId, endpointId), gte(webhookMessages.createdAt, since)], true);
}

async function requeue(orgId: string, where: ReturnType<typeof eq>[], onlyFailed: boolean): Promise<number> {
  return withOrg(orgId, async (tx) => {
    const filters = [eq(webhookMessages.organizationId, orgId), ...where];
    if (onlyFailed) filters.push(eq(webhookMessages.status, 'failed'));
    const rows = await tx.update(webhookMessages).set({ status: 'pending' }).where(and(...filters)).returning({ id: webhookMessages.id, endpointId: webhookMessages.endpointId });
    const at = Date.now();
    for (const r of rows) {
      // A new job (a new key): the original job may be long finished or dead-lettered.
      await enqueueInTx(tx, 'webhook.deliver', { orgId, messageId: r.id, manual: true }, { key: `${r.id}:manual:${at}`, group: r.endpointId });
    }
    return rows.length;
  });
}
