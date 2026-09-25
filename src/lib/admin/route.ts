import { ZodError } from 'zod';
import { staffCan, type StaffPermission } from '@/core/staff';
import type { AuditSource } from '@/core/audit';
import { AccessError, InvalidRequestError } from '../errors';
import { annotateContext } from '../observability/context';
import { observeRequest } from '../observability/http';
import { getStaffMember, staffAuditSource, type StaffMember } from '../staff';

/*
 * Lesson 7.1: every staff WRITE is a route handler under /api/internal/…,
 * wrapped in staffRoute(permission, …), which answers in this order:
 *
 *   not staff (or not signed in)    → 404   the back office does not exist for you
 *   cross-site request (Origin)     → 403   a page elsewhere cannot make a staff member's browser act
 *   staff, role lacks permission    → 403   support cannot comp a plan, even with curl
 *   invalid input (no reason…)      → 400, or back to the form with the message
 *   done                            → 303 back to the page (a plain HTML form), or JSON
 *
 * Plain routes rather than server actions so that "a direct POST returns
 * 403" is literally true, and a curl can test it. The handler gets the staff
 * member and the AuditSource to hand to the service functions: every staff
 * write is audited with who, from where, and the reason.
 */
export type StaffRequest<P> = { staff: StaffMember; source: AuditSource; params: P; input: Record<string, string> };
type Result = { back: string; message?: string; json?: Record<string, unknown> };

export function staffRoute<P>(permission: StaffPermission, handler: (req: Request, ctx: StaffRequest<P>) => Promise<Result | Response>) {
  return (req: Request, context: { params: Promise<P> }) =>
    observeRequest(req, async () => {
      const staff = await getStaffMember();
      if (!staff) return Response.json({ error: 'not_found' }, { status: 404 });
      annotateContext({ userId: staff.userId });
      if (!sameOrigin(req)) return Response.json({ error: 'forbidden', message: 'Cross-site request refused.' }, { status: 403 });
      if (!staffCan(staff.role, permission)) return Response.json({ error: 'forbidden', message: `Your staff role (${staff.role}) cannot do this.` }, { status: 403 });

      const input = await readInput(req);
      const wantsHtml = (req.headers.get('accept') ?? '').includes('text/html');
      const back = safeBack(input.back);
      try {
        const result = await handler(req, { staff, source: staffAuditSource(staff, req.headers), params: await context.params, input });
        if (result instanceof Response) return result;
        if (!wantsHtml) return Response.json({ ok: true, message: result.message ?? null, ...result.json });
        return redirect(withQuery(result.back, 'done', result.message ?? 'Done.'));
      } catch (err) {
        const message = err instanceof ZodError ? err.issues[0]?.message : err instanceof InvalidRequestError ? err.message : null;
        if (err instanceof AccessError) return Response.json({ error: err.reason }, { status: err.reason === 'forbidden' ? 403 : 404 });
        if (message === null || message === undefined) throw err;
        if (!wantsHtml) return Response.json({ error: 'invalid_request', message }, { status: 400 });
        return redirect(withQuery(back ?? '/internal', 'error', message));
      }
    });
}

async function readInput(req: Request): Promise<Record<string, string>> {
  const type = req.headers.get('content-type') ?? '';
  if (type.includes('application/json')) {
    const body = (await req.json().catch(() => ({}))) as Record<string, unknown>;
    return Object.fromEntries(Object.entries(body).map(([k, v]) => [k, String(v ?? '')]));
  }
  if (type.includes('form')) {
    const form = await req.formData();
    return Object.fromEntries([...form.entries()].map(([k, v]) => [k, typeof v === 'string' ? v : '']));
  }
  return {};
}

/** Browsers send Origin on every POST; it must be this site. (No Origin: curl or a server, allowed; the session cookie still has to be there.) */
function sameOrigin(req: Request): boolean {
  const origin = req.headers.get('origin');
  if (!origin) return true;
  const host = req.headers.get('x-forwarded-host') ?? req.headers.get('host') ?? new URL(req.url).host;
  try {
    return new URL(origin).host === host;
  } catch {
    return false;
  }
}

/** Only paths inside the staff area: never an open redirect. */
function safeBack(value: string | undefined): string | null {
  return value && value.startsWith('/internal') && !value.startsWith('//') ? value : null;
}

function withQuery(path: string, key: string, value: string): string {
  const url = new URL(path, 'http://x');
  url.searchParams.delete('done');
  url.searchParams.delete('error');
  url.searchParams.set(key, value);
  return `${url.pathname}${url.search}`;
}

function redirect(location: string): Response {
  return new Response(null, { status: 303, headers: { location } });
}
