import { and, eq } from 'drizzle-orm';
import { schema } from '@/db';
import { withOrg, type TenantTx } from '@/db/tenant';
import { onboardingState, type Milestone, type OnboardingState } from '@/core/onboarding';

const { organizations, orgMilestones } = schema;

/*
 * Lesson 6.1 (🟡): record and read the org's onboarding milestones
 * (src/core/onboarding.ts says which, and in which order).
 */

/**
 * Record that the org reached a milestone, in the caller's transaction (the
 * one that created the monitor, stored the check, …), so the milestone exists
 * if and only if the thing happened. Only the FIRST time counts: the primary
 * key (org, milestone) plus ON CONFLICT DO NOTHING keep the original time.
 * Returns true when this call was the first time.
 */
export async function recordMilestoneInTx(tx: TenantTx, orgId: string, milestone: Milestone, userId: string | null, at = new Date()): Promise<boolean> {
  const inserted = await tx
    .insert(orgMilestones)
    .values({ organizationId: orgId, milestone, userId, reachedAt: at })
    .onConflictDoNothing()
    .returning({ milestone: orgMilestones.milestone });
  return inserted.length > 0;
}

export async function recordMilestone(orgId: string, milestone: Milestone, userId: string | null): Promise<boolean> {
  return withOrg(orgId, (tx) => recordMilestoneInTx(tx, orgId, milestone, userId));
}

/** Has the org reached this milestone? (Used to fill `is_first` in analytics events.) */
export async function hasMilestoneInTx(tx: TenantTx, orgId: string, milestone: Milestone): Promise<boolean> {
  const rows = await tx
    .select({ m: orgMilestones.milestone })
    .from(orgMilestones)
    .where(and(eq(orgMilestones.organizationId, orgId), eq(orgMilestones.milestone, milestone)))
    .limit(1);
  return rows.length > 0;
}

/** The checklist's state for this org: the same for every member, whenever they joined. */
export async function getOnboarding({ orgId }: { orgId: string }): Promise<OnboardingState> {
  return withOrg(orgId, async (tx) => {
    const [org] = await tx.select({ createdAt: organizations.createdAt }).from(organizations).where(eq(organizations.id, orgId));
    const rows = await tx
      .select({ milestone: orgMilestones.milestone, reachedAt: orgMilestones.reachedAt })
      .from(orgMilestones)
      .where(eq(orgMilestones.organizationId, orgId));
    return onboardingState(org.createdAt, new Map(rows.map((r) => [r.milestone, r.reachedAt])));
  });
}
