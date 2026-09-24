/**
 * Only follow `?next=` values that point back into Beacon.
 *
 * Login pages that redirect to any URL in the query string are "open
 * redirects": a phishing email links to beacon.app/login?next=https://evil.example
 * and the real login page forwards the victim there. Accept a same-site path,
 * reject everything else (including protocol-relative "//evil.example").
 */
export function safeRedirect(next: unknown, fallback = '/dashboard'): string {
  if (typeof next !== 'string') return fallback;
  if (!next.startsWith('/') || next.startsWith('//') || next.startsWith('/\\')) return fallback;
  return next;
}
