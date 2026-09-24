import { createHash } from 'node:crypto';
import { and, eq, lt } from 'drizzle-orm';
import { ZodError } from 'zod';
import { schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { bearerToken, type ApiScope } from '@/core/api-keys';
import { toPublicId } from '@/core/ids';
import { cheapestPlanWhere, entitlementsFor } from '@/core/plans';
import { problemBody, type ProblemType } from '@/core/problems';
import { perMinute, rateLimitHeaders, type RateLimitDecision, type RateLimitPolicy } from '@/core/rate-limit';
import type { Actor } from '@/core/permissions';
import type { Incident, Monitor } from '@/db/schema';
import { verifyApiKey } from './api-keys';
import { AccessError, InvalidRequestError, LimitExceededError } from './errors';
import { consumeRateLimit } from './rate-limit';

/*
 * Lesson 5.2: everything every /api/v1 request goes through, in this order:
 *
 *   1. rate limit per client IP, before authentication (slows down key guessing)
 *   2. the API key: Authorization: Bearer bk_live_…          → 401
 *   3. the plan: does the org's plan include the API?        → 402 (lesson 3.2)
 *   4. the key's scope for this endpoint                     → 403
 *   5. rate limit per org, sized by the plan                 → 429 + Retry-After
 *   6. the handler, with the org from the KEY (never from the URL or body)
 *   7. any error → RFC 9457 problem details; RateLimit headers on every response
 */

/** What a handler knows about the caller. */
export type ApiContext = {
  orgId: string;
  keyId: string;
  scopes: ApiScope[];
  /**
   * Who the lib functions see as acting (Module 1's rules still run). A key
   * is an org-level integration, not a person: with "monitors:write" (which
   * only owners and admins can grant, since it maps to monitor.write_any) it
   * may change any monitor; otherwise it is read-only. `userId` is the key's
   * creator, recorded as the author of monitors it creates.
   */
  actor: Actor & { userId: string };
  createdBy: string | null;
};

const IP_POLICY = perMinute('ip', 300);

export function problem(type: ProblemType, extra: Record<string, unknown> = {}, headers: Record<string, string> = {}): Response {
  const body = problemBody(type, extra);
  return new Response(JSON.stringify(body), { status: body.status, headers: { 'content-type': 'application/problem+json', ...headers } });
}

/** Behind a proxy, the client is the first address of X-Forwarded-For (trust it only behind your own proxy). */
function clientIp(req: Request): string {
  return req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() || req.headers.get('x-real-ip') || 'unknown';
}

export function publicApi<P = Record<string, never>>(scope: ApiScope, handler: (req: Request, api: ApiContext, params: P) => Promise<Response>) {
  return async (req: Request, context: { params: Promise<P> }): Promise<Response> => {
    const instance = new URL(req.url).pathname;
    let limitHeaders: Record<string, string> = {};
    try {
      const byIp = await consumeRateLimit(`ip:${clientIp(req)}`, IP_POLICY);
      if (!byIp.allowed) return tooMany(IP_POLICY, byIp, instance);

      const token = bearerToken(req.headers.get('authorization'));
      const key = token ? await verifyApiKey(token) : null;
      if (!key) {
        const detail = token ? 'This API key is not valid, or it was revoked.' : 'Send your API key as "Authorization: Bearer bk_live_…".';
        return problem('unauthenticated', { detail, instance }, { 'WWW-Authenticate': 'Bearer realm="beacon"' });
      }

      const ent = entitlementsFor(key.plan);
      if (!ent.api) {
        const upgradeTo = cheapestPlanWhere((e) => e.api);
        return problem('plan-upgrade-required', { detail: `The API is included in the ${upgradeTo ?? 'higher'} plan.`, instance, upgrade_to: upgradeTo });
      }
      if (!key.scopes.includes(scope)) {
        return problem('insufficient-scope', { detail: `This endpoint needs the "${scope}" scope.`, instance, required_scope: scope }, {
          'WWW-Authenticate': `Bearer error="insufficient_scope", scope="${scope}"`,
        });
      }

      // Lesson 5.2: one bucket per ORG (all its keys together), sized by the plan.
      const policy = perMinute('api', ent.apiRequestsPerMinute);
      const decision = await consumeRateLimit(`org:${key.orgId}`, policy);
      limitHeaders = rateLimitHeaders(policy, decision);
      if (!decision.allowed) return tooMany(policy, decision, instance);

      const api: ApiContext = {
        orgId: key.orgId,
        keyId: key.keyId,
        scopes: key.scopes,
        createdBy: key.createdBy,
        actor: { userId: key.createdBy ?? '', role: key.scopes.includes('monitors:write') ? 'admin' : 'viewer' },
      };
      return withHeaders(await handler(req, api, await context.params), limitHeaders);
    } catch (err) {
      return withHeaders(errorToProblem(err, instance), limitHeaders);
    }
  };
}

function tooMany(policy: RateLimitPolicy, d: RateLimitDecision, instance: string) {
  return problem('rate-limited', { detail: `Rate limit of ${policy.capacity} requests per minute reached. Retry in ${d.retryAfterSec} s.`, instance }, rateLimitHeaders(policy, d));
}

function withHeaders(res: Response, headers: Record<string, string>): Response {
  for (const [k, v] of Object.entries(headers)) res.headers.set(k, v);
  return res;
}

/** Every error becomes a problem document. An unexpected one is a 500 that says nothing about our internals. */
export function errorToProblem(err: unknown, instance: string): Response {
  if (err instanceof AccessError) {
    if (err.reason === 'forbidden') return problem('forbidden', { detail: 'The API key may not do this.', instance });
    if (err.reason === 'unauthenticated') return problem('unauthenticated', { instance });
    return problem('not-found', { instance });
  }
  if (err instanceof LimitExceededError) {
    return problem('limit-exceeded', { detail: err.message, instance, limit: err.limit, allowed: err.allowed, upgrade_to: err.upgradeTo });
  }
  if (err instanceof InvalidRequestError) {
    return problem(err.code === 'blocked_url' ? 'blocked-url' : 'invalid-parameter', { detail: err.message, instance });
  }
  if (err instanceof ZodError) {
    return problem('validation-failed', { instance, errors: err.issues.map((i) => ({ field: i.path.join('.') || '(body)', message: i.message })) });
  }
  if (err instanceof SyntaxError) return problem('invalid-json', { instance });
  console.error('[api] unexpected error', err);
  return problem('internal', { instance });
}

/*
 * Response bodies: allow-listed shapes (lesson 1.3), snake_case, prefixed ids.
 */
export function toApiMonitor(m: Monitor) {
  return {
    id: toPublicId('monitor', m.id),
    name: m.name,
    url: m.url,
    interval_seconds: m.intervalSeconds,
    paused: m.paused,
    paused_reason: m.pausedReason,
    created_at: m.createdAt.toISOString(),
  };
}

export function toApiIncident(i: Incident) {
  return {
    id: toPublicId('incident', i.id),
    monitor_id: toPublicId('monitor', i.monitorId),
    status: i.resolvedAt ? ('resolved' as const) : ('open' as const),
    cause: i.cause,
    opened_at: i.openedAt.toISOString(),
    resolved_at: i.resolvedAt?.toISOString() ?? null,
  };
}

/** A page for the list endpoints. */
export function page<T extends { id: string }>(data: T[], hasMore: boolean) {
  return { data, has_more: hasMore, next_cursor: hasMore ? (data.at(-1)?.id ?? null) : null };
}

/**
 * Lesson 5.2 (🟡): Idempotency-Key on POST. The client sends a unique key;
 * the first request with it runs and its (successful) response is stored;
 * a retry with the same key and the same body gets the stored response back,
 * byte for byte, instead of creating a second monitor.
 *
 *   same key, same body, first still running → 409 (try again in a moment)
 *   same key, different body                 → 422 (a client bug)
 *   no key                                   → no protection, as before
 *
 * The key is claimed with an INSERT first (the primary key makes two
 * concurrent claims impossible), so two retries racing each other cannot both
 * create. Only 2xx responses are kept; after an error the key is released, so
 * the client can retry the same request. Kept 24 hours.
 */
export async function idempotent(req: Request, orgId: string, rawBody: string, run: () => Promise<Response>): Promise<Response> {
  const key = req.headers.get('idempotency-key');
  if (!key) return run();
  const instance = new URL(req.url).pathname;
  if (key.length > 255) return problem('invalid-parameter', { detail: 'Idempotency-Key is longer than 255 characters.', instance });
  const { apiIdempotencyKeys: t } = schema;
  const requestHash = createHash('sha256').update(`${req.method} ${instance}\n${rawBody}`).digest('hex');
  const where = and(eq(t.organizationId, orgId), eq(t.key, key));

  const claim = await withOrg(orgId, async (tx) => {
    await tx.delete(t).where(and(where, lt(t.createdAt, new Date(Date.now() - 24 * 3600_000)))); // expired: forget it
    const [mine] = await tx
      .insert(t)
      .values({ organizationId: orgId, key, requestMethod: req.method, requestPath: instance, requestHash })
      .onConflictDoNothing()
      .returning({ key: t.key });
    if (mine) return null;
    const [existing] = await tx.select().from(t).where(where);
    return existing;
  });

  if (claim) {
    if (claim.requestHash !== requestHash) return problem('idempotency-key-reused', { detail: 'Use a new Idempotency-Key for a different request.', instance });
    if (claim.statusCode === null) return problem('idempotency-key-in-use', { detail: 'The first request with this key is still running.', instance }, { 'Retry-After': '1' });
    return Response.json(claim.responseBody, { status: claim.statusCode, headers: { 'Idempotent-Replayed': 'true' } });
  }

  const release = () => withOrg(orgId, (tx) => tx.delete(t).where(where));
  let res: Response;
  try {
    res = await run();
  } catch (err) {
    await release();
    throw err;
  }
  if (res.status < 200 || res.status >= 300) {
    await release();
    return res;
  }
  const body = await res.clone().json();
  await withOrg(orgId, (tx) => tx.update(t).set({ statusCode: res.status, responseBody: body }).where(where));
  return res;
}
