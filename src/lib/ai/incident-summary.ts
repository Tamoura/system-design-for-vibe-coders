import { and, asc, desc, eq, gte, inArray, isNotNull, like, lte, sql } from 'drizzle-orm';
import { z } from 'zod';
import { schema } from '@/db';
import { withOrg, type TenantTx } from '@/db/tenant';
import { cheapestPlanWhere, entitlementsFor, PLANS } from '@/core/plans';
import { buildIncidentPrompt, IncidentSummarySchema, PROMPT_VERSION, summaryProblems, SYSTEM_PROMPT, type IncidentContext } from '@/core/incident-summary';
import { isUuid } from '@/core/validation';
import type { AuditSource } from '@/core/audit';
import { auditSourceOf, recordAudit, SYSTEM_SOURCE } from '../audit';
import { AccessError, InvalidRequestError, LimitExceededError } from '../errors';
import { enqueueInTx } from '../queue';
import { AiRateLimitedError, AiUnavailableError, generateStructured, providerChain } from './gateway';

const { incidents, monitors, checkResults, incidentUpdates, notificationDeliveries, organizations, incidentSummaries, llmUsage } = schema;

/*
 * Lesson 8.2 (🟢): the AI incident summary, from Beacon's side.
 *
 *   incident resolved (checker or a person), or "Summarize with AI" clicked
 *     └─ in the same transaction: org opted in AND plan entitled? → summary row
 *        "generating" + an `ai.summarize` job (lesson 5.1: slow work is a job)
 *   worker ─► loadIncidentContext() inside withOrg (only this org's rows, RLS)
 *          ─► the gateway (./gateway.ts): rate limit, cache, Claude or the fake,
 *             zod + summaryProblems() checks, metering
 *          ─► a DRAFT, or "failed" with a Retry button (never a crash)
 *   a person edits the draft and clicks Publish (page.publish) ─► on the status page
 *
 * The model never publishes anything, and never sees an email address, a
 * phone number, a recipient or a full URL (loadIncidentContext minimises).
 */
export const FEATURE = 'incident_summary';
const CHECK_WINDOW_BEFORE_MS = 15 * 60_000;

type Scope = { orgId: string };
type Actor = Scope & { userId: string; audit?: AuditSource };

/* ---------------------------------------------------------------------------
 * The data the model sees.
 * ------------------------------------------------------------------------- */

export async function loadIncidentContext(tx: TenantTx, orgId: string, incidentId: string, now = new Date()): Promise<IncidentContext | null> {
  const [row] = await tx
    .select({ incident: incidents, monitor: { name: monitors.name, url: monitors.url, id: monitors.id } })
    .from(incidents)
    .innerJoin(monitors, eq(monitors.id, incidents.monitorId))
    .where(and(eq(incidents.organizationId, orgId), eq(incidents.id, incidentId)));
  if (!row) return null;
  const { incident, monitor } = row;
  const end = incident.resolvedAt ?? now;
  const checks = await tx
    .select({ ok: checkResults.ok, statusCode: checkResults.statusCode, error: checkResults.error, checkedAt: checkResults.checkedAt })
    .from(checkResults)
    .where(
      and(
        eq(checkResults.organizationId, orgId),
        eq(checkResults.monitorId, monitor.id),
        gte(checkResults.checkedAt, new Date(incident.openedAt.getTime() - CHECK_WINDOW_BEFORE_MS)),
        lte(checkResults.checkedAt, end),
      ),
    )
    .orderBy(asc(checkResults.checkedAt))
    .limit(5_000);
  const failed = checks.filter((c) => !c.ok);
  const statusCodes: Record<string, number> = {};
  const errors = new Map<string, number>();
  for (const c of failed) {
    if (c.statusCode) statusCodes[String(c.statusCode)] = (statusCodes[String(c.statusCode)] ?? 0) + 1;
    const text = (c.error ?? (c.statusCode ? `HTTP ${c.statusCode}` : 'unknown')).slice(0, 200);
    errors.set(text, (errors.get(text) ?? 0) + 1);
  }
  const notes = await tx
    .select({ at: incidentUpdates.createdAt, authorId: incidentUpdates.authorId, body: incidentUpdates.body })
    .from(incidentUpdates)
    .where(and(eq(incidentUpdates.organizationId, orgId), eq(incidentUpdates.incidentId, incidentId)))
    .orderBy(asc(incidentUpdates.createdAt))
    .limit(20);
  const deliveries = await tx
    .select({
      channel: notificationDeliveries.channel,
      sent: sql<number>`(count(*) filter (where ${notificationDeliveries.status} = 'sent'))::int`,
      failed: sql<number>`(count(*) filter (where ${notificationDeliveries.status} = 'failed'))::int`,
    })
    .from(notificationDeliveries)
    .where(and(eq(notificationDeliveries.organizationId, orgId), like(notificationDeliveries.dedupeKey, `incident.%:${incidentId}:%`)))
    .groupBy(notificationDeliveries.channel);
  let host = 'unknown';
  try {
    host = new URL(monitor.url).host; // the host only: a path or query string can carry tokens
  } catch {
    // an unparsable URL stays "unknown"
  }
  return {
    monitor: { name: monitor.name, host },
    incident: {
      status: incident.resolvedAt ? 'resolved' : 'ongoing',
      openedAt: incident.openedAt.toISOString(),
      resolvedAt: incident.resolvedAt?.toISOString() ?? null,
      acknowledgedAt: incident.acknowledgedAt?.toISOString() ?? null,
      durationMinutes: Math.round((end.getTime() - incident.openedAt.getTime()) / 60_000),
      cause: incident.cause.slice(0, 200),
    },
    checks: {
      total: checks.length,
      failed: failed.length,
      statusCodes,
      errors: [...errors.entries()].sort((a, b) => b[1] - a[1]).slice(0, 5).map(([text, count]) => ({ text, count })),
      firstFailureAt: failed[0]?.checkedAt.toISOString() ?? null,
      lastSuccessAt: [...checks].reverse().find((c) => c.ok)?.checkedAt.toISOString() ?? null,
    },
    notes: notes.map((n) => ({ at: n.at.toISOString(), by: n.authorId ? 'team' : 'beacon', text: n.body.slice(0, 500) })),
    notifications: deliveries.map((d) => ({ channel: d.channel, sent: d.sent, failed: d.failed })),
  };
}

/* ---------------------------------------------------------------------------
 * Opt-in and entitlement.
 * ------------------------------------------------------------------------- */

async function availabilityInTx(tx: TenantTx, orgId: string) {
  const [org] = await tx.select({ plan: organizations.plan, enabled: organizations.aiSummariesEnabled }).from(organizations).where(eq(organizations.id, orgId));
  const entitled = Boolean(org && entitlementsFor(org.plan).aiSummaries);
  return { entitled, enabled: Boolean(org?.enabled), plan: org?.plan ?? 'free' };
}

function notEntitledError(plan: keyof typeof PLANS) {
  const upgradeTo = cheapestPlanWhere((e) => e.aiSummaries);
  return new LimitExceededError('aiSummaries', 0, `AI incident summaries are not on the ${PLANS[plan].name} plan.${upgradeTo ? ` Upgrade to ${PLANS[upgradeTo].name} to use them.` : ''}`, upgradeTo);
}

/** Lesson 8.2: the org's opt-in (org.manage). Turning it on needs the entitlement; turning it off never does. */
export async function setAiSummariesEnabled(ctx: Actor, enabled: boolean) {
  await withOrg(ctx.orgId, async (tx) => {
    const a = await availabilityInTx(tx, ctx.orgId);
    if (enabled && !a.entitled) throw notEntitledError(a.plan);
    if (a.enabled === enabled) return;
    await tx.update(organizations).set({ aiSummariesEnabled: enabled }).where(eq(organizations.id, ctx.orgId));
    await recordAudit(tx, {
      orgId: ctx.orgId,
      action: enabled ? 'ai.summaries_enabled' : 'ai.summaries_disabled',
      source: auditSourceOf(ctx),
      target: { type: 'organization', id: ctx.orgId },
      changes: { ai_summaries_enabled: { before: a.enabled, after: enabled } },
      metadata: enabled ? { providers: providerChain().map((p) => `${p.name}/${p.model}`) } : undefined,
    });
  });
}

/* ---------------------------------------------------------------------------
 * Asking for a summary.
 * ------------------------------------------------------------------------- */

/**
 * In the caller's transaction (the one that resolved the incident): when the
 * org has opted in and its plan includes it, mark the summary "generating" and
 * enqueue the job. A published summary, or a draft a person has edited, is
 * never overwritten by a new automatic one.
 */
export async function enqueueIncidentSummaryInTx(tx: TenantTx, orgId: string, incidentId: string, trigger: 'resolved' | 'manual', now = new Date()): Promise<boolean> {
  const a = await availabilityInTx(tx, orgId);
  if (!a.entitled || !a.enabled) return false;
  const [existing] = await tx.select().from(incidentSummaries).where(and(eq(incidentSummaries.organizationId, orgId), eq(incidentSummaries.incidentId, incidentId)));
  if (existing?.status === 'published') return false;
  if (trigger === 'resolved' && existing?.editedAt) return false;
  await tx
    .insert(incidentSummaries)
    .values({ organizationId: orgId, incidentId, status: 'generating' })
    .onConflictDoUpdate({ target: incidentSummaries.incidentId, set: { status: 'generating', error: null } });
  await enqueueInTx(tx, 'ai.summarize', { orgId, incidentId }, { key: `${incidentId}@${now.toISOString()}`, group: orgId });
  return true;
}

/** "Summarize with AI" / "Retry" (incident.write). 402 without the plan, 400 when the org has not opted in. */
export async function requestIncidentSummary(ctx: Actor, incidentId: string) {
  if (!isUuid(incidentId)) throw new AccessError('not_found');
  await withOrg(ctx.orgId, async (tx) => {
    const [incident] = await tx.select({ id: incidents.id }).from(incidents).where(and(eq(incidents.organizationId, ctx.orgId), eq(incidents.id, incidentId)));
    if (!incident) throw new AccessError('not_found');
    const a = await availabilityInTx(tx, ctx.orgId);
    if (!a.entitled) throw notEntitledError(a.plan);
    if (!a.enabled) throw new InvalidRequestError('ai_disabled', 'AI summaries are turned off for this organization (Settings → AI summaries).');
    const queued = await enqueueIncidentSummaryInTx(tx, ctx.orgId, incidentId, 'manual');
    if (!queued) throw new InvalidRequestError('already_published', 'This incident’s summary is already published.');
  });
}

/* ---------------------------------------------------------------------------
 * The job.
 * ------------------------------------------------------------------------- */

/** The `ai.summarize` job. Never throws for a model problem: the summary shows "failed" and a Retry. */
export async function runIncidentSummary(data: { orgId: string; incidentId: string }, now = new Date()) {
  const { orgId, incidentId } = data;
  const prepared = await withOrg(orgId, async (tx) => {
    const a = await availabilityInTx(tx, orgId);
    const [summary] = await tx.select().from(incidentSummaries).where(and(eq(incidentSummaries.organizationId, orgId), eq(incidentSummaries.incidentId, incidentId)));
    if (!summary || summary.status !== 'generating') return { skip: summary ? summary.status : 'no summary requested' };
    if (!a.entitled || !a.enabled) {
      await tx.update(incidentSummaries).set({ status: 'failed', error: 'AI summaries were turned off before this one was written.' }).where(eq(incidentSummaries.id, summary.id));
      return { skip: 'turned off' };
    }
    const ctx = await loadIncidentContext(tx, orgId, incidentId, now);
    return ctx ? { ctx } : { skip: 'incident deleted' };
  });
  if ('skip' in prepared) return { skipped: prepared.skip };
  const { ctx } = prepared;

  try {
    const result = await generateStructured({
      orgId,
      feature: FEATURE,
      subjectId: incidentId,
      system: SYSTEM_PROMPT,
      prompt: buildIncidentPrompt(ctx),
      promptVersion: PROMPT_VERSION,
      schema: IncidentSummarySchema,
      check: (summary) => summaryProblems(summary, ctx),
      maxOutputTokens: 4_000,
    });
    const s = result.output;
    await withOrg(orgId, async (tx) => {
      const [saved] = await tx
        .update(incidentSummaries)
        .set({
          status: 'draft',
          headline: s.headline,
          body: s.customerFacingUpdate,
          details: { status: s.status, impact: s.impact, suspectedCause: s.suspectedCause, timeline: s.timeline },
          provider: result.provider,
          model: result.model,
          inputHash: result.inputHash,
          error: null,
          generatedAt: now,
          editedBy: null,
          editedAt: null,
        })
        .where(and(eq(incidentSummaries.organizationId, orgId), eq(incidentSummaries.incidentId, incidentId), eq(incidentSummaries.status, 'generating')))
        .returning({ id: incidentSummaries.id });
      // Lesson 8.2, enterprise questionnaires: "can we see what the AI did?"
      if (saved) {
        await recordAudit(tx, {
          orgId,
          action: 'incident.summary_generated',
          source: SYSTEM_SOURCE,
          target: { type: 'incident', id: incidentId },
          metadata: { provider: result.provider, model: result.model, cached: result.cached },
        });
      }
    });
    return { incidentId, provider: result.provider, model: result.model, cached: result.cached };
  } catch (err) {
    if (!(err instanceof AiUnavailableError || err instanceof AiRateLimitedError)) throw err; // a real bug: the queue retries
    const message = err instanceof AiRateLimitedError ? err.message : 'The AI could not write a valid summary this time. Try again, or write the update yourself.';
    await withOrg(orgId, (tx) =>
      tx.update(incidentSummaries).set({ status: 'failed', error: message }).where(and(eq(incidentSummaries.organizationId, orgId), eq(incidentSummaries.incidentId, incidentId), eq(incidentSummaries.status, 'generating'))),
    );
    return { failed: err.message.slice(0, 300) };
  }
}

/* ---------------------------------------------------------------------------
 * The human in the loop.
 * ------------------------------------------------------------------------- */

export const summaryEditInput = z.object({
  headline: z.string().trim().min(5, 'At least 5 characters').max(120),
  body: z.string().trim().min(10, 'At least 10 characters').max(600),
});

/** A person edits the draft (incident.write). What they save is what gets published. */
export async function updateSummaryDraft(ctx: Actor, incidentId: string, input: z.infer<typeof summaryEditInput>) {
  if (!isUuid(incidentId)) throw new AccessError('not_found');
  const rows = await withOrg(ctx.orgId, (tx) =>
    tx
      .update(incidentSummaries)
      .set({ headline: input.headline, body: input.body, editedBy: ctx.userId, editedAt: new Date() })
      .where(and(eq(incidentSummaries.organizationId, ctx.orgId), eq(incidentSummaries.incidentId, incidentId), eq(incidentSummaries.status, 'draft')))
      .returning({ id: incidentSummaries.id }),
  );
  if (!rows.length) throw new AccessError('not_found');
}

/** Publish to the public status page (page.publish). The only way AI text reaches the public. */
export async function publishSummary(ctx: Actor, incidentId: string) {
  if (!isUuid(incidentId)) throw new AccessError('not_found');
  await withOrg(ctx.orgId, async (tx) => {
    const [row] = await tx
      .update(incidentSummaries)
      .set({ status: 'published', publishedBy: ctx.userId, publishedAt: new Date() })
      .where(and(eq(incidentSummaries.organizationId, ctx.orgId), eq(incidentSummaries.incidentId, incidentId), eq(incidentSummaries.status, 'draft')))
      .returning();
    if (!row) throw new AccessError('not_found');
    await recordAudit(tx, {
      orgId: ctx.orgId,
      action: 'incident.summary_published',
      source: auditSourceOf(ctx),
      target: { type: 'incident', id: incidentId, name: row.headline },
      metadata: { edited_by_a_person: Boolean(row.editedAt), model: row.model },
    });
  });
}

export async function listIncidentSummaries({ orgId }: Scope, incidentIds: string[]) {
  if (!incidentIds.length) return [];
  return withOrg(orgId, (tx) => tx.select().from(incidentSummaries).where(and(eq(incidentSummaries.organizationId, orgId), inArray(incidentSummaries.incidentId, incidentIds))));
}

/** For the public status page: PUBLISHED summaries only, the last 30 days, newest first. */
export async function listPublishedSummaries(orgId: string, now = new Date()) {
  return withOrg(orgId, (tx) =>
    tx
      .select({ headline: incidentSummaries.headline, body: incidentSummaries.body, publishedAt: incidentSummaries.publishedAt, openedAt: incidents.openedAt, resolvedAt: incidents.resolvedAt })
      .from(incidentSummaries)
      .innerJoin(incidents, eq(incidents.id, incidentSummaries.incidentId))
      .where(and(eq(incidentSummaries.organizationId, orgId), eq(incidentSummaries.status, 'published'), isNotNull(incidentSummaries.publishedAt), gte(incidentSummaries.publishedAt, new Date(now.getTime() - 30 * 86_400_000))))
      .orderBy(desc(incidentSummaries.publishedAt))
      .limit(10),
  );
}

/* ---------------------------------------------------------------------------
 * Settings page: availability and what AI cost this month.
 * ------------------------------------------------------------------------- */

export async function getAiSettings({ orgId }: Scope) {
  return withOrg(orgId, async (tx) => ({ ...(await availabilityInTx(tx, orgId)), providers: providerChain().map((p) => ({ name: p.name, model: p.model })) }));
}

/**
 * Lesson 8.2 (🟡): "a monthly per-org usage query" to hold against the
 * provider's dashboard: calls, tokens and cost for one calendar month (UTC).
 */
export async function aiUsageForMonth({ orgId }: Scope, month = new Date()) {
  const start = new Date(Date.UTC(month.getUTCFullYear(), month.getUTCMonth(), 1));
  const end = new Date(Date.UTC(month.getUTCFullYear(), month.getUTCMonth() + 1, 1));
  return withOrg(orgId, async (tx) => {
    const rows = await tx
      .select({
        model: llmUsage.model,
        outcome: llmUsage.outcome,
        calls: sql<number>`count(*)::int`,
        inputTokens: sql<number>`coalesce(sum(${llmUsage.inputTokens}), 0)::int`,
        outputTokens: sql<number>`coalesce(sum(${llmUsage.outputTokens}), 0)::int`,
        costMicros: sql<number>`coalesce(sum(${llmUsage.costMicros}), 0)::bigint`,
      })
      .from(llmUsage)
      .where(and(eq(llmUsage.organizationId, orgId), gte(llmUsage.createdAt, start), lte(llmUsage.createdAt, end)))
      .groupBy(llmUsage.model, llmUsage.outcome)
      .orderBy(llmUsage.model, llmUsage.outcome);
    const n = (v: unknown) => Number(v);
    const total = rows.reduce(
      (t, r) => ({ calls: t.calls + n(r.calls), inputTokens: t.inputTokens + n(r.inputTokens), outputTokens: t.outputTokens + n(r.outputTokens), costMicros: t.costMicros + n(r.costMicros) }),
      { calls: 0, inputTokens: 0, outputTokens: 0, costMicros: 0 },
    );
    return { start, end, rows: rows.map((r) => ({ ...r, calls: n(r.calls), inputTokens: n(r.inputTokens), outputTokens: n(r.outputTokens), costMicros: n(r.costMicros) })), total };
  });
}
