import { readdirSync, readFileSync, statSync } from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { NextRequest } from 'next/server';
import { proxy } from '@/proxy';
import { contentSecurityPolicy, cspOriginsFromEnv, STATIC_PAGES } from '@/core/security-headers';
import { SECURITY_TXT_EXPIRES, securityTxt } from '@/core/trust';
import { GET as securityTxtRoute } from '@/app/.well-known/security.txt/route';
import { GET as apiDocsRoute } from '@/app/docs/api/route';

/*
 * Lesson 8.1 (🟢): "the status page response has CSP, HSTS and nosniff
 * headers, and security.txt has Contact and Expires".
 */

const get = (p: string) => proxy(new NextRequest(`http://localhost${p}`));

/** A directive's values, e.g. directive(csp, 'script-src') → ["'self'", "'nonce-…'", …]. */
function directive(csp: string, name: string): string[] {
  const part = csp.split(';').map((s) => s.trim()).find((s) => s.startsWith(`${name} `));
  return part ? part.split(/\s+/).slice(1) : [];
}

describe('security headers on every response (src/proxy.ts)', () => {
  it('the public status page gets a nonce CSP, HSTS, nosniff and the rest', () => {
    const res = get('/status/acme');
    const csp = res.headers.get('content-security-policy')!;
    expect(res.headers.get('strict-transport-security')).toMatch(/^max-age=\d{8}; includeSubDomains$/);
    expect(res.headers.get('x-content-type-options')).toBe('nosniff');
    expect(res.headers.get('referrer-policy')).toBe('strict-origin-when-cross-origin');
    expect(res.headers.get('x-frame-options')).toBe('DENY');
    expect(res.headers.get('permissions-policy')).toContain('camera=()');
    const script = directive(csp, 'script-src');
    expect(script).toContain("'strict-dynamic'");
    expect(script.some((s) => /^'nonce-[A-Za-z0-9+/=]{20,}'$/.test(s))).toBe(true);
    expect(script).not.toContain("'unsafe-inline'");
    expect(script).not.toContain("'unsafe-eval'");
    expect(directive(csp, 'object-src')).toEqual(["'none'"]);
    expect(directive(csp, 'frame-ancestors')).toEqual(["'none'"]);
    expect(directive(csp, 'base-uri')).toEqual(["'self'"]);
  });

  it('hands the same nonce to Next.js on the request, and a new one on every request', () => {
    const a = get('/acme/monitors');
    const b = get('/acme/monitors');
    const nonceA = a.headers.get('x-middleware-request-x-nonce');
    expect(nonceA).toBeTruthy();
    expect(a.headers.get('x-middleware-request-content-security-policy')).toBe(a.headers.get('content-security-policy'));
    expect(a.headers.get('content-security-policy')).toContain(`'nonce-${nonceA}'`);
    expect(b.headers.get('x-middleware-request-x-nonce')).not.toBe(nonceA);
  });

  it('the prerendered marketing pages get the static policy (no nonce is possible there)', () => {
    for (const p of STATIC_PAGES) {
      const csp = get(p).headers.get('content-security-policy')!;
      expect(csp, p).not.toContain('nonce-');
      expect(directive(csp, 'script-src')).toContain("'unsafe-inline'");
      expect(directive(csp, 'frame-ancestors')).toEqual(["'none'"]);
    }
  });

  it('API responses and error responses carry the headers too', async () => {
    expect(get('/api/v1/monitors').headers.get('x-content-type-options')).toBe('nosniff');
    const refused = proxy(new NextRequest('http://localhost/api/orgs/acme/monitors', { method: 'POST', headers: { cookie: 'beacon_impersonation=x' } }));
    expect(refused.status).toBe(403);
    expect(refused.headers.get('strict-transport-security')).toBeTruthy();
  });

  it('/docs/api sets its own policy (a pinned CDN script by nonce), and the proxy leaves it alone', async () => {
    expect(get('/docs/api').headers.get('content-security-policy')).toBeNull();
    const res = apiDocsRoute();
    const csp = res.headers.get('content-security-policy')!;
    const nonce = /'nonce-([^']+)'/.exec(csp)![1];
    const html = await res.text();
    expect(html.match(/<script nonce="([^"]+)"/g)).toHaveLength(2);
    expect(html).toContain(`nonce="${nonce}"`);
    expect(directive(csp, 'script-src')).not.toContain("'unsafe-inline'");
  });

  it('every page that declares itself static (`dynamic = "error"`) is in STATIC_PAGES, and nothing else is', () => {
    const files: string[] = [];
    const walk = (dir: string) => {
      for (const f of readdirSync(dir)) {
        const p = path.join(dir, f);
        if (statSync(p).isDirectory()) walk(p);
        else if (f === 'page.tsx' && /dynamic = 'error'/.test(readFileSync(p, 'utf8'))) files.push(p);
      }
    };
    walk('src/app');
    // src/app/(marketing)/pricing/page.tsx → /pricing (route groups in parentheses are not in the URL)
    const routes = files.map((f) => '/' + path.dirname(path.relative('src/app', f)).split(path.sep).filter((s) => s !== '.' && !s.startsWith('(')).join('/'));
    expect(routes.sort()).toEqual([...STATIC_PAGES].sort());
  });
});

describe('contentSecurityPolicy()', () => {
  it('development adds eval and the dev server websocket; production never has them', () => {
    expect(directive(contentSecurityPolicy({ nonce: 'n', dev: true }), 'script-src')).toContain("'unsafe-eval'");
    expect(directive(contentSecurityPolicy({ nonce: 'n', dev: true }), 'connect-src')).toContain('ws:');
    expect(contentSecurityPolicy({ nonce: 'n' })).not.toMatch(/unsafe-eval|ws:/);
  });

  it('upgrade-insecure-requests only when the app is served over https (it would break http://localhost)', () => {
    expect(contentSecurityPolicy({ https: true })).toContain('upgrade-insecure-requests');
    expect(contentSecurityPolicy({ https: false })).not.toContain('upgrade-insecure-requests');
  });

  it('allows the S3 bucket for uploads and images, and Sentry for browser errors, from the configuration', () => {
    const o = cspOriginsFromEnv({ STORAGE_DRIVER: 's3', S3_ENDPOINT: 'https://acct.r2.cloudflarestorage.com/x', NEXT_PUBLIC_SENTRY_DSN: 'https://k@o1.ingest.sentry.io/2' });
    const csp = contentSecurityPolicy({ nonce: 'n', ...o });
    expect(directive(csp, 'connect-src')).toEqual(["'self'", 'https://acct.r2.cloudflarestorage.com', 'https://o1.ingest.sentry.io']);
    expect(directive(csp, 'img-src')).toContain('https://acct.r2.cloudflarestorage.com');
    expect(cspOriginsFromEnv({ STORAGE_DRIVER: 's3', S3_BUCKET: 'b', S3_REGION: 'eu-west-1' }).imgOrigins).toEqual(['https://b.s3.eu-west-1.amazonaws.com']);
    expect(cspOriginsFromEnv({}).connectOrigins).toEqual([]); // local storage: same origin
  });
});

describe('/.well-known/security.txt (RFC 9116)', () => {
  it('has Contact and Expires (and a policy link), as text/plain', async () => {
    const res = securityTxtRoute();
    expect(res.headers.get('content-type')).toMatch(/^text\/plain/);
    const body = await res.text();
    expect(body).toMatch(/^Contact: (mailto:|https:)/m);
    expect(body).toMatch(/^Expires: \d{4}-\d{2}-\d{2}T/m);
    expect(body).toMatch(/^Policy: .*\/trust#disclosure$/m);
    expect(securityTxt({ appUrl: 'https://beacon.dev/', contact: 'mailto:s@x' })).toContain('Canonical: https://beacon.dev/.well-known/security.txt');
  });

  it('Expires is less than a year away and more than 30 days away: renew it before this test fails', () => {
    const days = (new Date(SECURITY_TXT_EXPIRES).getTime() - Date.now()) / 86_400_000;
    expect(days).toBeLessThan(366);
    expect(days, 'security.txt expires within 30 days: move SECURITY_TXT_EXPIRES in src/core/trust.ts').toBeGreaterThan(30);
  });
});
