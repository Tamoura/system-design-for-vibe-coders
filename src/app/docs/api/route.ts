import { makeNonce } from '@/core/security-headers';

/**
 * GET /docs/api — lesson 5.2 (🟡): the API reference, rendered by Scalar from
 * the OpenAPI document (/api/v1/openapi.json), with a built-in "try it"
 * client. Scalar is loaded from its CDN, pinned to a version, rather than
 * installed: it is 47 MB of dependencies for one page.
 * Without network access to the CDN, the page still links the raw document.
 */
const SCALAR = 'https://cdn.jsdelivr.net/npm/@scalar/api-reference@1.72.0';

/**
 * Lesson 8.1: this page loads a third-party script, so it has its own
 * Content-Security-Policy (src/proxy.ts leaves it alone, OWN_CSP_PATHS): the
 * CDN and our one inline script, by nonce. Nothing else may run here either.
 */
function policy(nonce: string): string {
  return [
    "default-src 'self'",
    `script-src 'nonce-${nonce}' https://cdn.jsdelivr.net`,
    "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.scalar.com",
    "font-src 'self' https://fonts.scalar.com https://cdn.jsdelivr.net",
    "img-src 'self' data: https:",
    "connect-src 'self'",
    "object-src 'none'",
    "base-uri 'self'",
    "frame-ancestors 'none'",
  ].join('; ');
}

export function GET() {
  const nonce = makeNonce();
  const html = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Beacon API reference</title>
  </head>
  <body>
    <noscript>The interactive reference needs JavaScript. The document itself: <a href="/api/v1/openapi.json">/api/v1/openapi.json</a></noscript>
    <p id="fallback" style="font-family: system-ui; padding: 1rem">Loading the API reference… If it does not appear, read <a href="/api/v1/openapi.json">/api/v1/openapi.json</a>.</p>
    <div id="app"></div>
    <script nonce="${nonce}" src="${SCALAR}"></script>
    <script nonce="${nonce}">
      if (window.Scalar) {
        document.getElementById('fallback').remove();
        Scalar.createApiReference('#app', { url: '/api/v1/openapi.json', hideClientButton: false });
      }
    </script>
  </body>
</html>`;
  return new Response(html, { headers: { 'content-type': 'text/html; charset=utf-8', 'content-security-policy': policy(nonce) } });
}
