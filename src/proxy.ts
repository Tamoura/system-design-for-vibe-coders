import { NextResponse, type NextRequest } from 'next/server';
import { IMPERSONATION_COOKIE, impersonationMayPost, SAFE_METHODS } from '@/core/staff';
import { contentSecurityPolicy, cspOriginsFromEnv, makeNonce, originOf, OWN_CSP_PATHS, securityHeaders, STATIC_PAGES } from '@/core/security-headers';

/*
 * Next.js "proxy" (formerly middleware): runs before every page, action and
 * route. Beacon uses it for two things that must happen before any code runs.
 *
 * 1. Lesson 7.2: the REQUEST ID. Reuse the caller's `x-request-id` (a load
 *    balancer's) when it looks like one, else make one; pass it on to the app
 *    (every log line and error report carries it) and back in the response
 *    (so a customer can quote it to support).
 *
 * 2. Lesson 7.1: READ-ONLY IMPERSONATION. While the impersonation cookie is
 *    present, every mutating request (POST, PUT, PATCH, DELETE, and so every
 *    server action) is refused with 403, API routes included, except leaving
 *    the impersonation, signing out and the staff area itself. The check is
 *    deliberately dumb and early: it needs no database and cannot be skipped
 *    by a route that forgets to check. requirePermission() is the second lock.
 *
 * 3. Lesson 8.1: SECURITY HEADERS on every response, and a Content-Security-
 *    Policy with a fresh nonce per request (src/core/security-headers.ts).
 *    The CSP also goes on the REQUEST headers: that is where Next.js reads the
 *    nonce from to stamp it on its own <script> tags. Pages read it back with
 *    `(await headers()).get('x-nonce')` if they ever add a <Script>.
 */
export function proxy(request: NextRequest) {
  const incoming = request.headers.get('x-request-id');
  const requestId = incoming && /^[A-Za-z0-9._:-]{8,128}$/.test(incoming) ? incoming : crypto.randomUUID();

  const impersonating = request.cookies.has(IMPERSONATION_COOKIE);
  const safe = (SAFE_METHODS as readonly string[]).includes(request.method);
  if (impersonating && !safe && !impersonationMayPost(request.nextUrl.pathname)) {
    const body = { error: 'forbidden', message: 'Read-only impersonation: Beacon staff cannot change anything in a customer account.' };
    return NextResponse.json(body, { status: 403, headers: { 'x-request-id': requestId, ...securityHeaders() } });
  }

  const headers = new Headers(request.headers);
  headers.set('x-request-id', requestId);
  const csp = policyFor(request.nextUrl.pathname);
  if (csp) {
    headers.set('content-security-policy', csp.value);
    if (csp.nonce) headers.set('x-nonce', csp.nonce);
  }
  const response = NextResponse.next({ request: { headers } });
  response.headers.set('x-request-id', requestId);
  for (const [name, value] of Object.entries(securityHeaders())) response.headers.set(name, value);
  if (csp) response.headers.set('content-security-policy', csp.value);
  return response;
}

/** Lesson 8.1: which Content-Security-Policy this path gets (null: the route sets its own). */
function policyFor(pathname: string): { value: string; nonce?: string } | null {
  if ((OWN_CSP_PATHS as readonly string[]).includes(pathname)) return null;
  const fromEnv = cspOriginsFromEnv(process.env);
  if ((STATIC_PAGES as readonly string[]).includes(pathname)) {
    // Prerendered marketing pages: no nonce possible. Plausible (lesson 6.2) runs only here.
    const plausible = process.env.NEXT_PUBLIC_PLAUSIBLE_DOMAIN ? originOf(process.env.NEXT_PUBLIC_PLAUSIBLE_SRC || 'https://plausible.io/js/script.js') : null;
    const extra = plausible ? [plausible] : [];
    return { value: contentSecurityPolicy({ ...fromEnv, scriptOrigins: extra, connectOrigins: [...(fromEnv.connectOrigins ?? []), ...extra] }) };
  }
  const nonce = makeNonce();
  return { value: contentSecurityPolicy({ ...fromEnv, nonce }), nonce };
}

export const config = {
  // Everything except Next's static assets.
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};
