/*
 * Next.js runs register() once when a server starts, and onRequestError()
 * for every error thrown while rendering a page, running a server action or a
 * route handler. Beacon's start-up, in order:
 *
 *   1. lesson 7.4: check the configuration (src/lib/env.ts) and exit with a
 *      clear message if a variable is missing, before serving anything
 *   2. lesson 7.2: OpenTelemetry (traces + metrics) and error tracking
 *
 * Node.js runtime only: Beacon has no Edge code apart from src/proxy.ts,
 * which needs none of this.
 */
export async function register() {
  if (process.env.NEXT_RUNTIME !== 'nodejs') return;
  process.env.OTEL_SERVICE_NAME ??= 'beacon-web';
  const { validateEnvOrExit } = await import('./lib/env');
  validateEnvOrExit('beacon-web');
  const { initTelemetry } = await import('./lib/observability/telemetry');
  initTelemetry('beacon-web');
  const { initErrorTracking } = await import('./lib/observability/errors');
  await initErrorTracking('beacon-web');
  const { logger } = await import('./lib/observability/logger');
  logger.info({ release: process.env.APP_RELEASE ?? 'dev', env: process.env.APP_ENV ?? process.env.NODE_ENV }, 'web.started');
}

type RequestInfo = { path: string; method: string; headers: Record<string, string | string[] | undefined> };
type ErrorContext = { routePath: string; routeType: string };

/**
 * Lesson 7.2: errors in pages and server actions (route handlers under
 * apiRoute() are already reported by observeRequest()). One JSON line with
 * the request id that src/proxy.ts assigned, and Sentry when configured.
 */
export async function onRequestError(error: unknown, request: RequestInfo, context: ErrorContext) {
  if (process.env.NEXT_RUNTIME !== 'nodejs') return;
  // notFound(), redirect() and forbidden() are control flow, not errors.
  const digest = (error as { digest?: string })?.digest ?? '';
  if (digest.startsWith('NEXT_')) return;
  const { runWithContext, requestIdFrom } = await import('./lib/observability/context');
  const { captureError } = await import('./lib/observability/errors');
  const requestId = requestIdFrom(String(request.headers['x-request-id'] ?? ''));
  runWithContext({ requestId }, () => captureError(error, { path: request.path.split('?')[0], method: request.method, route: context.routePath, routeType: context.routeType }));
}
