import { NextResponse, type NextRequest } from 'next/server';
import { IMPERSONATION_COOKIE, impersonationMayPost, SAFE_METHODS } from '@/core/staff';

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
 */
export function proxy(request: NextRequest) {
  const incoming = request.headers.get('x-request-id');
  const requestId = incoming && /^[A-Za-z0-9._:-]{8,128}$/.test(incoming) ? incoming : crypto.randomUUID();

  const impersonating = request.cookies.has(IMPERSONATION_COOKIE);
  const safe = (SAFE_METHODS as readonly string[]).includes(request.method);
  if (impersonating && !safe && !impersonationMayPost(request.nextUrl.pathname)) {
    const body = { error: 'forbidden', message: 'Read-only impersonation: Beacon staff cannot change anything in a customer account.' };
    return NextResponse.json(body, { status: 403, headers: { 'x-request-id': requestId } });
  }

  const headers = new Headers(request.headers);
  headers.set('x-request-id', requestId);
  const response = NextResponse.next({ request: { headers } });
  response.headers.set('x-request-id', requestId);
  return response;
}

export const config = {
  // Everything except Next's static assets.
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};
