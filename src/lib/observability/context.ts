import { AsyncLocalStorage } from 'node:async_hooks';
import { randomUUID } from 'node:crypto';

/*
 * Lesson 7.2: "set them once per request, not in every call". The request
 * context is what every log line, error report and trace needs to answer
 * "what happened to THIS request, for THIS customer?":
 *
 *   requestId  ties every line of one request (or one job) together
 *   orgId      "what happened to Acme?" (added once the org is known)
 *   userId     who was signed in (an internal id, never an email)
 *
 * It lives in an AsyncLocalStorage: a value that follows the async call chain
 * without being passed as an argument, so `logger.info(…)` deep inside
 * src/lib/monitors.ts still knows which request it belongs to. It is set at
 * the edges of the app:
 *
 *   API routes       apiRoute() and publicApi() (src/lib/observability/http.ts)
 *   queue jobs       the worker, from the job's payload (the request that
 *                    enqueued it passes its requestId and trace along)
 *   access checks    requireMembership() adds orgId and userId
 */
export type RequestContext = {
  requestId: string;
  orgId?: string;
  userId?: string;
  /** Lesson 7.1: set while Beacon staff view a customer's account. */
  impersonatorId?: string;
  /** For jobs: which queue and which job. */
  queue?: string;
  jobId?: string;
  /**
   * Where the request came from, for the AUDIT log (lesson 7.3), never for
   * the application log: an IP address is personal data, and the logger's
   * mixin leaves these two out on purpose.
   */
  ip?: string | null;
  userAgent?: string | null;
};

// One store per PROCESS, on globalThis: Next.js bundles this module into several
// server chunks (instrumentation, each route), and a store per copy would make
// the logger (created once) blind to the context a route handler set.
const g = globalThis as unknown as { beaconRequestContext?: AsyncLocalStorage<RequestContext> };
const storage = (g.beaconRequestContext ??= new AsyncLocalStorage<RequestContext>());

export function runWithContext<T>(ctx: RequestContext, fn: () => T): T {
  return storage.run(ctx, fn);
}

export function getContext(): RequestContext | undefined {
  return storage.getStore();
}

/** Add fields to the current context (e.g. the org, once the URL's slug is resolved). No-op outside one. */
export function annotateContext(fields: Partial<Omit<RequestContext, 'requestId'>>): void {
  const store = storage.getStore();
  if (!store) return;
  for (const [k, v] of Object.entries(fields)) if (v !== undefined) (store as Record<string, unknown>)[k] = v;
}

/**
 * The request id: reuse the caller's `x-request-id` (a load balancer, or
 * src/proxy.ts, set it) when it looks like an id, else make one. A bad value
 * is replaced rather than trusted: it ends up in every log line.
 */
export function requestIdFrom(value: string | null | undefined): string {
  return value && /^[A-Za-z0-9._:-]{8,128}$/.test(value) ? value : randomUUID();
}

/** Behind a proxy, the client is the first address of X-Forwarded-For (trust it only behind your own proxy). */
export function clientIpFrom(headers: Headers): string | null {
  return headers.get('x-forwarded-for')?.split(',')[0]?.trim() || headers.get('x-real-ip') || null;
}
