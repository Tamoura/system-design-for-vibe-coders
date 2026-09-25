/*
 * Lesson 7.2: Beacon's observability in one import.
 *
 *   logger, moduleLogger       structured JSON logs (pino), request context on every line
 *   runWithContext, …          the request context (request id, org, user)
 *   captureError               error tracking (Sentry when SENTRY_DSN is set)
 *   initTelemetry, withSpan    OpenTelemetry traces and metrics
 *   recordCheck, …             the product and RED metrics
 */
export { logger, moduleLogger, createLogger } from './logger';
export { runWithContext, getContext, annotateContext, requestIdFrom, clientIpFrom, type RequestContext } from './context';
export { captureError, initErrorTracking, flushErrors } from './errors';
export { initTelemetry, shutdownTelemetry, withSpan, injectTraceContext, extractTraceContext, SpanKind, type TraceCarrier } from './telemetry';
export { recordCheck, recordHttpRequest, recordJob, routeTemplate, checkRegion } from './metrics';
export { observeRequest, observed } from './http';
