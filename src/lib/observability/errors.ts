import { getContext } from './context';
import { logger } from './logger';

/*
 * Lesson 7.2 (🟢): error tracking, behind one small interface.
 *
 *   captureError(err, extra)   log it (always), and send it to the error
 *                              tracker when one is configured
 *
 * Two trackers:
 *   SENTRY_DSN set    Sentry (or GlitchTip, which speaks the same protocol),
 *                     tagged with the RELEASE (APP_RELEASE: the git SHA the
 *                     Docker image was built from, lesson 7.4) and with the
 *                     request id, org id and user id of the request context,
 *                     so "one angry customer" and "everyone" look different.
 *   not set           the log line is the whole report.
 *
 * The browser side is src/instrumentation-client.ts (NEXT_PUBLIC_SENTRY_DSN).
 * Source maps: `npm run build` with SENTRY_AUTH_TOKEN set also uploads them
 * (see the CI workflow), so a minified stack trace reads as src/app/….tsx.
 */
type Tracker = { capture(err: unknown, tags: Record<string, string | undefined>, extra: Record<string, unknown>): void; flush(): Promise<void> };

const g = globalThis as unknown as { beaconErrorTracker?: Tracker | null };

export async function initErrorTracking(service: string): Promise<void> {
  if (g.beaconErrorTracker !== undefined) return;
  g.beaconErrorTracker = null;
  const dsn = process.env.SENTRY_DSN;
  if (!dsn) return;
  // Loaded only when configured: no Sentry code runs for anyone who has not asked for it.
  const Sentry = await import('@sentry/node');
  Sentry.init({
    dsn,
    release: process.env.APP_RELEASE,
    environment: process.env.APP_ENV ?? process.env.NODE_ENV,
    serverName: service,
    // Beacon has its own OpenTelemetry setup (./telemetry.ts): Sentry must not
    // register a competing tracer provider. It only tracks errors here.
    enableOpenTelemetrySetup: false,
    tracesSampleRate: 0,
  });
  g.beaconErrorTracker = {
    capture(err, tags, extra) {
      Sentry.withScope((scope) => {
        for (const [k, v] of Object.entries(tags)) if (v) scope.setTag(k, v);
        if (tags.userId) scope.setUser({ id: tags.userId }); // an id, never an email
        scope.setExtras(extra);
        Sentry.captureException(err);
      });
    },
    flush: async () => {
      await Sentry.flush(2000);
    },
  };
  logger.info({ service }, 'error_tracking.enabled');
}

/** Report an unexpected error: one JSON log line (with the request context) and, if configured, Sentry. */
export function captureError(err: unknown, extra: Record<string, unknown> = {}): void {
  const ctx = getContext();
  logger.error({ err, ...extra }, 'error.unexpected');
  g.beaconErrorTracker?.capture(err, { requestId: ctx?.requestId, orgId: ctx?.orgId, userId: ctx?.userId, queue: ctx?.queue }, extra);
}

export async function flushErrors(): Promise<void> {
  await g.beaconErrorTracker?.flush();
}
