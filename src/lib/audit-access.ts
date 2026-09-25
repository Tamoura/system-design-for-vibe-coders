import { cheapestPlanWhere, PLANS } from '@/core/plans';
import type { OrgContext } from './access';
import { getEntitlements } from './entitlements';
import { LimitExceededError } from './errors';

/**
 * Lesson 7.3 (🟡): who may read an org's audit log, in the order the page
 * and the API check it:
 *   1. a member with "audit.read" (owners and admins)   else 403 (requirePermission)
 *   2. a plan with the `auditLog` entitlement            else 402 with the plan that has it
 * Returns the retention window: Pro sees 30 days, Business 365.
 */
export async function assertAuditLogAccess(ctx: OrgContext): Promise<{ retentionDays: number }> {
  const ent = await getEntitlements(ctx);
  if (!ent.auditLog) {
    const upgradeTo = cheapestPlanWhere((e) => e.auditLog);
    throw new LimitExceededError('auditLog', false, `The audit log is part of the ${upgradeTo ? PLANS[upgradeTo].name : 'higher'} plan.`, upgradeTo);
  }
  return { retentionDays: ent.auditLogRetentionDays };
}
