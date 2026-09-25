/*
 * Lesson 8.1 (🟢): security headers, "cheap wins, set once in middleware".
 * Pure functions, so the tests can check every header without a browser;
 * src/proxy.ts sets them on every response.
 *
 *   Content-Security-Policy     which scripts, styles, images and connections a page may use.
 *                               The main defence in depth against XSS on the PUBLIC status page,
 *                               which shows text a customer (or an attacker who got into a
 *                               customer's account) typed.
 *   Strict-Transport-Security   "only ever talk to this host over HTTPS" (browsers ignore it on http://)
 *   X-Content-Type-Options      nosniff: a JSON or text response is never run as a script
 *   Referrer-Policy             other sites see our origin, never a full URL with ids in it
 *   X-Frame-Options + frame-ancestors   nobody may frame Beacon (clickjacking)
 *   Permissions-Policy          no camera, microphone, geolocation… Beacon uses none of them
 *   Cross-Origin-Opener-Policy  a page we open (a customer's URL) cannot reach back into ours
 *
 * Two kinds of Content-Security-Policy:
 *
 *   NONCE (every dynamic page: the app, sign-in, the status page, /internal)
 *     script-src 'nonce-<random per request>' 'strict-dynamic'. Next.js reads the nonce from the
 *     request's CSP header and puts it on its own <script> tags; an injected <script> has no
 *     nonce, so the browser refuses to run it.
 *
 *   STATIC (the prerendered marketing pages in STATIC_PAGES)
 *     A page built once at build time cannot carry a per-request nonce, and Next.js puts inline
 *     <script> tags in it (the React payload). Those pages render no user input at all, so they
 *     get 'self' 'unsafe-inline' for scripts. The alternative, making the marketing site dynamic
 *     to get nonces, costs every visitor a server render. A page missing from STATIC_PAGES gets
 *     the nonce policy and breaks loudly (its scripts are blocked): the safe failure.
 *
 * Styles use 'unsafe-inline' everywhere: React renders style="…" attributes, which a nonce cannot
 * cover, and injected CSS is a much smaller risk than injected script.
 */

/** Prerendered marketing pages (they declare `dynamic = 'error'`; tests/security-headers.test.ts checks the list). */
export const STATIC_PAGES = ['/', '/pricing', '/trust'] as const;

/** Paths that set their own CSP (a third-party script on one page): the proxy leaves the header to them. */
export const OWN_CSP_PATHS = ['/docs/api'] as const;

export type CspOptions = {
  /** Per-request nonce. Omitted: the STATIC policy. */
  nonce?: string;
  /** `next dev`: React needs eval for its error overlay, and the dev server a websocket. */
  dev?: boolean;
  /** APP_URL is https: also ask the browser to upgrade any http:// subresource. */
  https?: boolean;
  /** Extra origins scripts may load from (Plausible on the marketing site). */
  scriptOrigins?: string[];
  /** Extra origins the page may fetch/PUT to (the S3 bucket for direct uploads, Sentry, Plausible). */
  connectOrigins?: string[];
  /** Extra origins images may come from (signed URLs of the S3 bucket). */
  imgOrigins?: string[];
};

/** A fresh, unguessable nonce: 16 random bytes, base64. One per request, never reused. */
export function makeNonce(): string {
  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);
  return btoa(String.fromCharCode(...bytes));
}

export function contentSecurityPolicy(opts: CspOptions = {}): string {
  const script = opts.nonce
    ? ["'self'", `'nonce-${opts.nonce}'`, "'strict-dynamic'"]
    : ["'self'", "'unsafe-inline'", ...(opts.scriptOrigins ?? [])];
  if (opts.dev) script.push("'unsafe-eval'");
  const directives: Record<string, string[]> = {
    'default-src': ["'self'"],
    'script-src': script,
    'style-src': ["'self'", "'unsafe-inline'"],
    'img-src': ["'self'", 'data:', 'blob:', ...(opts.imgOrigins ?? [])],
    'font-src': ["'self'"],
    'connect-src': ["'self'", ...(opts.connectOrigins ?? []), ...(opts.dev ? ['ws:'] : [])],
    'object-src': ["'none'"],
    'base-uri': ["'self'"],
    // Plain HTML forms only post to Beacon, or to Stripe's hosted pages (lesson 3.1).
    'form-action': ["'self'", 'https://checkout.stripe.com', 'https://billing.stripe.com'],
    'frame-ancestors': ["'none'"],
  };
  const parts = Object.entries(directives).map(([name, values]) => `${name} ${[...new Set(values)].join(' ')}`);
  if (opts.https) parts.push('upgrade-insecure-requests');
  return parts.join('; ');
}

/** Every response gets these, whatever its CSP. */
export function securityHeaders(): Record<string, string> {
  return {
    // Two years, the value hstspreload.org asks for. `preload` is a separate, hard-to-undo decision.
    'Strict-Transport-Security': 'max-age=63072000; includeSubDomains',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'X-Frame-Options': 'DENY',
    'Permissions-Policy': 'camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()',
    'Cross-Origin-Opener-Policy': 'same-origin',
  };
}

/** The origin of a URL ("https://o1.ingest.sentry.io"), or null for anything unparsable. */
export function originOf(url: string | undefined): string | null {
  if (!url) return null;
  try {
    return new URL(url).origin;
  } catch {
    return null;
  }
}

/**
 * Where the browser talks to besides Beacon itself, from the configuration:
 * the S3-compatible bucket (direct uploads, signed image URLs, lesson 2.2) and
 * Sentry (browser errors, lesson 7.2). Local storage is same-origin.
 */
export function cspOriginsFromEnv(env: Record<string, string | undefined>): Pick<CspOptions, 'connectOrigins' | 'imgOrigins' | 'https' | 'dev'> {
  const bucket =
    env.STORAGE_DRIVER === 's3'
      ? (originOf(env.S3_ENDPOINT) ?? (env.S3_BUCKET ? `https://${env.S3_BUCKET}.s3.${env.S3_REGION ?? 'us-east-1'}.amazonaws.com` : null))
      : null;
  const sentry = originOf(env.NEXT_PUBLIC_SENTRY_DSN);
  return {
    connectOrigins: [bucket, sentry].filter((o): o is string => Boolean(o)),
    imgOrigins: bucket ? [bucket] : [],
    https: (env.APP_URL ?? '').startsWith('https://'),
    dev: env.NODE_ENV === 'development',
  };
}
