import { SpanKind } from '@opentelemetry/api';
import { clientIpFrom, runWithContext, requestIdFrom } from './context';
import { captureError } from './errors';
import { logger } from './logger';
import { recordHttpRequest, routeTemplate } from './metrics';
import { withSpan } from './telemetry';

/*
 * Lesson 7.2: what every API request goes through, once, at the edge.
 *
 *   1. a request context (./context.ts) with the request id src/proxy.ts put
 *      in `x-request-id` (or a new one), so every log line of this request
 *      carries it; requireMembership() adds the org and the user
 *   2. a SERVER span named after the route template ("POST /api/orgs/:org/monitors")
 *   3. RED metrics: one count and one duration per request
 *   4. one access log line: `http.request` with method, route, status and ms
 *   5. an unexpected error (a real bug, not a 4xx) is captured (log + Sentry)
 *      and becomes a 500 that says nothing about Beacon's internals
 *   6. `x-request-id` on the response, so a customer can quote it to support
 *
 * apiRoute() (the dashboard's JSON) and publicApi() (/api/v1) both use it;
 * so do the webhooks and the health endpoints.
 */
export async function observeRequest(req: Request, handler: () => Promise<Response>): Promise<Response> {
  const requestId = requestIdFrom(req.headers.get('x-request-id'));
  const url = new URL(req.url);
  const route = routeTemplate(url.pathname);
  const started = performance.now();
  return runWithContext({ requestId, ip: clientIpFrom(req.headers), userAgent: req.headers.get('user-agent') }, () =>
    withSpan(`${req.method} ${route}`, { kind: SpanKind.SERVER, attributes: { 'http.request.method': req.method, 'http.route': route, 'beacon.request_id': requestId } }, async (span) => {
      let res: Response;
      try {
        res = await handler();
      } catch (err) {
        captureError(err, { method: req.method, route });
        res = Response.json({ error: 'internal_error', requestId }, { status: 500 });
      }
      const seconds = (performance.now() - started) / 1000;
      span.setAttribute('http.response.status_code', res.status);
      recordHttpRequest(req.method, route, res.status, seconds);
      logger.info({ method: req.method, route, status: res.status, ms: Math.round(seconds * 1000) }, 'http.request');
      return withRequestId(res, requestId);
    }),
  );
}

/** Wrap a plain route handler: `export const GET = observed(async (req) => …)`. */
export function observed<Ctx = unknown>(handler: (req: Request, context: Ctx) => Promise<Response>) {
  return (req: Request, context?: Ctx) => observeRequest(req, () => handler(req, context as Ctx));
}

function withRequestId(res: Response, requestId: string): Response {
  try {
    res.headers.set('x-request-id', requestId);
    return res;
  } catch {
    // Some responses (a redirect from Response.redirect) have immutable headers: copy it.
    const copy = new Response(res.body, res);
    copy.headers.set('x-request-id', requestId);
    return copy;
  }
}
