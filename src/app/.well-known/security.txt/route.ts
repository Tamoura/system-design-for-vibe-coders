import { securityContact, securityTxt } from '@/core/trust';

/**
 * GET /.well-known/security.txt — lesson 8.1: how a security researcher
 * reports a vulnerability (RFC 9116). It costs nothing, and it is often the
 * difference between a quiet private report and a public post.
 */
export function GET() {
  const body = securityTxt({ appUrl: process.env.APP_URL ?? 'http://localhost:3000', contact: securityContact() });
  return new Response(body, { headers: { 'content-type': 'text/plain; charset=utf-8', 'cache-control': 'public, max-age=3600' } });
}
