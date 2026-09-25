import { cookies } from 'next/headers';
import { compPlanInput, extendTrialInput, IMPERSONATION_COOKIE, impersonateInput, reasonOnlyInput, type StaffPermission } from '@/core/staff';
import { staffRoute, type StaffRequest } from '@/lib/admin/route';
import { resendVerificationEmail, revokeUserSessions } from '@/lib/admin/support';
import { compPlan, extendTrial, removeComp } from '@/lib/billing/support';
import { AccessError, InvalidRequestError } from '@/lib/errors';
import { startImpersonation } from '@/lib/impersonation';
import { InvitationError, resendInvitationAsSupport } from '@/lib/invitations';
import { isUuid } from '@/core/validation';
import { getOrganization } from '@/lib/organizations';
import { PLANS } from '@/core/plans';

/*
 * Lesson 7.1 (🟡): the admin panel's write actions on one customer org.
 * POST /api/internal/orgs/:orgId/:action, from the forms on /internal/orgs/:orgId.
 *
 * The table below IS the policy: which staff permission each action needs
 * (src/core/staff.ts says which roles have it). staffRoute() checks it before
 * the action runs: a support engineer's direct POST to comp-plan is a 403.
 * Every action validates a reason and calls the service layer, which writes
 * the audit event in the same transaction as the change.
 */
type Params = { orgId: string; action: string };
type Action = { permission: StaffPermission; run: (req: Request, ctx: StaffRequest<Params>) => Promise<{ back: string; message: string } | Response> };

const back = (orgId: string) => `/internal/orgs/${orgId}`;

const ACTIONS: Record<string, Action> = {
  'extend-trial': {
    permission: 'trial.extend',
    run: async (_req, { params, input, source }) => {
      const { days, reason } = extendTrialInput.parse(input);
      const { after } = await extendTrial(params.orgId, days, reason, source);
      return { back: back(params.orgId), message: `Trial extended by ${days} day(s), to ${after.toISOString().slice(0, 10)}.` };
    },
  },
  'comp-plan': {
    permission: 'plan.comp',
    run: async (_req, { params, input, source }) => {
      const { plan, months, reason } = compPlanInput.parse(input);
      const result = await compPlan(params.orgId, { plan, months }, reason, source);
      return { back: back(params.orgId), message: `${PLANS[plan].name} given free of charge${months ? ` for ${months} month(s)` : ''}. The org is now on ${PLANS[result.plan].name}.` };
    },
  },
  'remove-comp': {
    permission: 'plan.comp',
    run: async (_req, { params, input, source }) => {
      const { reason } = reasonOnlyInput.parse(input);
      const result = await removeComp(params.orgId, reason, source);
      return { back: back(params.orgId), message: result ? `Complimentary plan removed. The org is now on ${PLANS[result.plan].name}.` : 'There was no complimentary plan.' };
    },
  },
  'resend-invitation': {
    permission: 'email.resend',
    run: async (_req, { params, input, source }) => {
      const { reason } = reasonOnlyInput.parse(input);
      try {
        await resendInvitationAsSupport(params.orgId, input.invitationId ?? '', reason, source);
      } catch (err) {
        if (err instanceof InvitationError) throw new InvalidRequestError('invitation', err.message);
        throw err;
      }
      return { back: back(params.orgId), message: 'Invitation sent again with a new link.' };
    },
  },
  'resend-verification': {
    permission: 'email.resend',
    run: async (_req, { params, input, source }) => {
      const { reason } = reasonOnlyInput.parse(input);
      await resendVerificationEmail(params.orgId, input.userId ?? '', reason, source);
      return { back: back(params.orgId), message: 'Verification email sent.' };
    },
  },
  'revoke-sessions': {
    permission: 'sessions.revoke',
    run: async (_req, { params, input, source }) => {
      const { reason } = reasonOnlyInput.parse(input);
      const { revoked } = await revokeUserSessions(params.orgId, input.userId ?? '', reason, source);
      return { back: back(params.orgId), message: `Signed out of ${revoked} session(s).` };
    },
  },
  /**
   * Read-only impersonation (lesson 7.1): an audited row, then an HttpOnly
   * cookie that lives exactly as long as the session (30 minutes), then the
   * customer's app. src/proxy.ts refuses every write while the cookie exists.
   */
  impersonate: {
    permission: 'impersonate',
    run: async (_req, { params, input, source, staff }) => {
      const { userId, reason } = impersonateInput.parse(input);
      const { token, expiresAt, orgSlug } = await startImpersonation(staff, { orgId: params.orgId, targetUserId: userId, reason }, source);
      (await cookies()).set(IMPERSONATION_COOKIE, token, {
        httpOnly: true,
        sameSite: 'lax',
        secure: (process.env.APP_URL ?? '').startsWith('https://'),
        path: '/',
        expires: expiresAt,
      });
      return new Response(null, { status: 303, headers: { location: `/${orgSlug}/monitors` } });
    },
  },
};

export const POST = async (req: Request, context: { params: Promise<Params> }) => {
  const { orgId, action } = await context.params;
  const spec = Object.hasOwn(ACTIONS, action) ? ACTIONS[action] : null;
  if (!spec || !isUuid(orgId)) return Response.json({ error: 'not_found' }, { status: 404 });
  return staffRoute<Params>(spec.permission, async (r, ctx) => {
    if (!(await getOrganization({ orgId }))) throw new AccessError('not_found');
    return spec.run(r, ctx);
  })(req, context);
};
