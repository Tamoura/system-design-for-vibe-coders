import { cookies } from 'next/headers';
import { IMPERSONATION_COOKIE } from '@/core/staff';
import { endImpersonation } from '@/lib/impersonation';
import { observed } from '@/lib/observability/http';
import { getSessionUser } from '@/lib/session';
import { findStaffMember, staffAuditSource } from '@/lib/staff';

/**
 * Lesson 7.1: POST /api/impersonation/exit, the banner's "Exit" button. One
 * of the few POSTs the proxy lets through while impersonating. Ends the
 * session (audited as impersonation.ended in the customer's log), clears the
 * cookie, and goes back to the org's admin page.
 */
export const POST = observed(async (req: Request) => {
  const jar = await cookies();
  const token = jar.get(IMPERSONATION_COOKIE)?.value;
  jar.delete(IMPERSONATION_COOKIE);
  const me = await getSessionUser();
  const staff = await findStaffMember(me);
  let location = '/dashboard';
  if (token && me && staff) {
    const ended = await endImpersonation(me.id, token, staffAuditSource(staff, req.headers));
    if (ended) location = `/internal/orgs/${ended.orgId}?done=${encodeURIComponent('Impersonation ended.')}`;
  }
  return new Response(null, { status: 303, headers: { location } });
});
