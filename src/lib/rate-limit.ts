import { eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { takeToken, type RateLimitDecision, type RateLimitPolicy } from '@/core/rate-limit';

const { rateLimitBuckets } = schema;

/**
 * Lesson 5.2: take one token from the bucket `key` ("org:<id>", "ip:<addr>").
 *
 * The bucket lives in Postgres so that every app instance shares it. One
 * short transaction per request: make sure the row exists, lock it
 * (SELECT … FOR UPDATE, so two requests for the same bucket take turns and
 * neither is lost), apply the pure arithmetic (src/core/rate-limit.ts), write
 * it back. Different keys never wait for each other.
 * (rate_limit_buckets is not a tenant table: a bucket can be for an IP address.)
 */
export async function consumeRateLimit(key: string, policy: RateLimitPolicy, now = new Date()): Promise<RateLimitDecision> {
  return db.transaction(async (tx) => {
    await tx.insert(rateLimitBuckets).values({ key, tokens: policy.capacity, updatedAt: now }).onConflictDoNothing();
    const [row] = await tx.select().from(rateLimitBuckets).where(eq(rateLimitBuckets.key, key)).for('update');
    const decision = takeToken(row, policy, now);
    await tx.update(rateLimitBuckets).set(decision.bucket).where(eq(rateLimitBuckets.key, key));
    return decision;
  });
}
