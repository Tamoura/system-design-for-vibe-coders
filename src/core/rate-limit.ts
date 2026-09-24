/*
 * Lesson 5.2: rate limiting with a TOKEN BUCKET. A bucket holds up to
 * `capacity` tokens and refills at `refillPerSec`; each request takes one.
 * A client can burst up to `capacity` requests, then settles at the refill
 * rate on average. Pure arithmetic here; src/lib/rate-limit.ts keeps the
 * buckets in Postgres so every app instance shares them.
 *
 * The headers tell clients where they stand, on EVERY response (not only on
 * the 429), so a good client slows down before it is refused:
 *
 *   RateLimit-Policy: "api";q=120;w=60      the IETF draft's structured fields
 *   RateLimit: "api";r=117;t=2
 *   X-RateLimit-Limit / -Remaining / -Reset the older names many clients read
 *   Retry-After: 3                          on a 429 (RFC 6585): seconds to wait
 */
export type RateLimitPolicy = {
  /** Shown in the headers: "api", "ip". */
  name: string;
  /** The burst: how many requests in a row. */
  capacity: number;
  /** The sustained rate. */
  refillPerSec: number;
};

export type Bucket = { tokens: number; updatedAt: Date };

export type RateLimitDecision = {
  allowed: boolean;
  bucket: Bucket;
  /** Whole requests left right now. */
  remaining: number;
  /** Seconds until one more request is allowed (0 if allowed now). */
  retryAfterSec: number;
  /** Seconds until the bucket is full again. */
  resetSec: number;
};

/** "N per minute": a bucket of N that refills N per 60 seconds. */
export function perMinute(name: string, n: number): RateLimitPolicy {
  return { name, capacity: n, refillPerSec: n / 60 };
}

export function takeToken(previous: Bucket | null, policy: RateLimitPolicy, now: Date): RateLimitDecision {
  const elapsedSec = previous ? Math.max(0, (now.getTime() - previous.updatedAt.getTime()) / 1000) : 0;
  let tokens = previous ? Math.min(policy.capacity, previous.tokens + elapsedSec * policy.refillPerSec) : policy.capacity;
  const allowed = tokens >= 1;
  if (allowed) tokens -= 1;
  return {
    allowed,
    bucket: { tokens, updatedAt: now },
    remaining: Math.floor(tokens),
    retryAfterSec: allowed ? 0 : Math.ceil((1 - tokens) / policy.refillPerSec),
    resetSec: Math.ceil((policy.capacity - tokens) / policy.refillPerSec),
  };
}

export function rateLimitHeaders(policy: RateLimitPolicy, d: RateLimitDecision): Record<string, string> {
  const windowSec = Math.round(policy.capacity / policy.refillPerSec);
  return {
    'RateLimit-Policy': `"${policy.name}";q=${policy.capacity};w=${windowSec}`,
    RateLimit: `"${policy.name}";r=${d.remaining};t=${d.resetSec}`,
    'X-RateLimit-Limit': String(policy.capacity),
    'X-RateLimit-Remaining': String(d.remaining),
    'X-RateLimit-Reset': String(d.resetSec),
    ...(!d.allowed && { 'Retry-After': String(d.retryAfterSec) }),
  };
}
