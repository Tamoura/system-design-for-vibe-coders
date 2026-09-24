import { and, eq, inArray, sql } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg, type TenantTx } from '@/db/tenant';
import { ESCALATION_STOP_SIGNALS, escalationPolicyInput, type EscalationPolicy, type EscalationTier } from '@/core/escalation';
import { InvalidRequestError } from '../errors';
import { pageInTx } from '../notifications/pipeline';
import { defineWorkflow, startWorkflowInTx, type Signal } from './engine';

const { escalationPolicies, incidents, incidentUpdates, monitors, organizations, memberships } = schema;

/**
 * Lesson 5.4 (🟡): the escalation policy, interpreted by ONE durable workflow.
 * Read it top to bottom: that is the policy.
 *
 *   load-policy          snapshot the policy (this run keeps it, whatever edits follow)
 *   for each tier:
 *     check-before-tier-N  acknowledged or resolved already? stop
 *     notify-tier-N        page the tier's people on the tier's channels
 *     wait-tier-N          wait for "acknowledged" or "resolved", at most the tier's wait
 *   record-exhausted     nobody answered: say so on the incident
 *
 * The waits cost nothing: the run suspends, and wakes on a signal (an
 * acknowledgement, the incident resolving) or at the deadline.
 */
export const incidentEscalation = defineWorkflow('incident-escalation', async (ctx, input: { orgId: string; incidentId: string }) => {
  const policy = await ctx.step('load-policy', () => loadPolicy(input.orgId));
  if (!policy || policy.tiers.length === 0) return { outcome: 'no policy' };
  for (const [i, tier] of policy.tiers.entries()) {
    const early = await ctx.waitForSignal(`check-before-tier-${i + 1}`, ESCALATION_STOP_SIGNALS, 0);
    if (early) return stopped(early, i);
    await ctx.step(`notify-tier-${i + 1}`, () => pageTier(ctx.runId, input, tier, i + 1), { tier: i + 1, userIds: tier.userIds, channels: tier.channels });
    const signal = await ctx.waitForSignal(`wait-tier-${i + 1}`, ESCALATION_STOP_SIGNALS, tier.waitMinutes * 60_000);
    if (signal) return stopped(signal, i);
  }
  await ctx.step('record-exhausted', () => note(input, `Escalation ended after ${policy.tiers.length} tier(s): nobody acknowledged the incident.`));
  return { outcome: 'exhausted' };
});

const stopped = (signal: Signal, tierIndex: number) => ({
  outcome: signal.name === 'incident.acknowledged' ? 'acknowledged' : 'resolved',
  afterTier: tierIndex + 1,
  by: signal.payload,
});

/** The snapshot. Plain JSON, so it is recorded as the step's output. */
async function loadPolicy(orgId: string): Promise<EscalationPolicy | null> {
  const [row] = await withOrg(orgId, (tx) => tx.select().from(escalationPolicies).where(eq(escalationPolicies.organizationId, orgId)));
  return row ? escalationPolicyInput.parse({ tiers: row.tiers }) : null;
}

/**
 * Page one tier. Idempotent: the event key names the run and the tier
 * ("escalation:<run>:tier-2"), so the notifications, the deliveries and the
 * SMS idempotency key do too. A step that runs twice pages once.
 */
async function pageTier(runId: string, input: { orgId: string; incidentId: string }, tier: EscalationTier, n: number) {
  const [org] = await db.select({ name: organizations.name, slug: organizations.slug }).from(organizations).where(eq(organizations.id, input.orgId));
  return withOrg(input.orgId, async (tx) => {
    const [row] = await tx
      .select({ incident: incidents, monitor: monitors })
      .from(incidents)
      .innerJoin(monitors, eq(monitors.id, incidents.monitorId))
      .where(and(eq(incidents.organizationId, input.orgId), eq(incidents.id, input.incidentId)));
    if (!row) return { skipped: 'incident deleted' };
    const { incident, monitor } = row;
    const result = await pageInTx(
      tx,
      {
        orgId: input.orgId,
        category: 'incident.escalated',
        key: `escalation:${runId}:tier-${n}`,
        title: `Tier ${n}: ${monitor.name} is down, not acknowledged`,
        body: incident.cause,
        path: `/${org.slug}/monitors/${monitor.id}#incident-${incident.id}`,
        monitorId: monitor.id,
        email: {
          template: 'incident-escalated',
          props: { orgName: org.name, monitorName: monitor.name, cause: incident.cause, openedAt: incident.openedAt.toISOString(), tier: n },
        },
      },
      tier,
    );
    if (result.paged.length) {
      await tx.insert(incidentUpdates).values({ organizationId: input.orgId, incidentId: incident.id, body: `Escalation tier ${n}: paged ${result.paged.join(', ')} (${tier.channels.join(', ')}).` });
    }
    return result;
  });
}

async function note(input: { orgId: string; incidentId: string }, body: string) {
  await withOrg(input.orgId, (tx) => tx.insert(incidentUpdates).values({ organizationId: input.orgId, incidentId: input.incidentId, body }));
  return body;
}

/**
 * Start the escalation for a newly opened incident, in the checker's
 * transaction, if the org has a policy with at least one tier. One run per
 * incident (the key), however often this is called.
 */
export async function startEscalationInTx(tx: TenantTx, orgId: string, incidentId: string) {
  const [policy] = await tx
    .select({ tiers: sql<number>`jsonb_array_length(${escalationPolicies.tiers})` })
    .from(escalationPolicies)
    .where(eq(escalationPolicies.organizationId, orgId));
  if (!policy || policy.tiers === 0) return null;
  return startWorkflowInTx(tx, orgId, 'incident-escalation', `incident-escalation:${incidentId}`, { orgId, incidentId }, incidentId);
}

/*
 * The policy itself: Settings → Escalation (roles with "notification.manage").
 */
export async function getEscalationPolicy({ orgId }: { orgId: string }): Promise<EscalationPolicy> {
  return (await loadPolicy(orgId)) ?? { tiers: [] };
}

/** Save the policy. Everyone in a tier must be a member of the org. Applies to the NEXT incident. */
export async function saveEscalationPolicy(ctx: { orgId: string; userId: string }, policy: EscalationPolicy) {
  const parsed = escalationPolicyInput.parse(policy);
  const people = [...new Set(parsed.tiers.flatMap((t) => t.userIds))];
  if (people.length) {
    const found = await db.select({ userId: memberships.userId }).from(memberships).where(and(eq(memberships.organizationId, ctx.orgId), inArray(memberships.userId, people)));
    if (found.length !== people.length) throw new InvalidRequestError('not_a_member', 'Everyone on the escalation policy must be a member of this organization.');
  }
  await withOrg(ctx.orgId, (tx) =>
    tx
      .insert(escalationPolicies)
      .values({ organizationId: ctx.orgId, tiers: parsed.tiers, updatedBy: ctx.userId })
      .onConflictDoUpdate({ target: escalationPolicies.organizationId, set: { tiers: parsed.tiers, updatedBy: ctx.userId } }),
  );
}
