import { unsubscribeWithToken } from '@/lib/notifications/subscribers';

/**
 * POST /api/unsubscribe?token=… — lesson 4.1/4.2: RFC 8058 one-click
 * unsubscribe. Mail clients (Gmail's "Unsubscribe" button) POST here with the
 * body "List-Unsubscribe=One-Click", no cookies, no login: the signed token
 * is the authorization, and it can only switch mail OFF.
 *
 * Only POST: a GET must never unsubscribe, because link scanners and
 * previews open every URL in an email. People clicking the link in the
 * footer land on /unsubscribe, which asks before doing it.
 */
export async function POST(req: Request) {
  const token = new URL(req.url).searchParams.get('token') ?? '';
  const result = await unsubscribeWithToken(token);
  return Response.json(result.ok ? { unsubscribed: true, message: result.message } : { error: 'invalid_token', message: result.message }, { status: result.ok ? 200 : 400 });
}
