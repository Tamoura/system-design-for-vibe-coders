import { and, desc, eq, isNull, lt, or } from 'drizzle-orm';
import { z } from 'zod';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { trackInTx } from './analytics';
import { API_SCOPE_IDS, canGrantScopes, generateApiKey, hashApiKey, looksLikeApiKey, sameHash, type ApiScope } from '@/core/api-keys';
import type { Role } from '@/core/roles';
import { isUuid } from '@/core/validation';
import { AccessError } from './errors';

const { apiKeys, organizations } = schema;

/*
 * Lesson 5.2 (🟢): API keys, managed in Settings → API keys by roles with
 * "integration.manage", and checked on every public API request.
 */

export const createApiKeyInput = z.object({
  name: z.string().trim().min(1, 'Give the key a name, e.g. "Terraform"').max(80),
  scopes: z.array(z.enum(API_SCOPE_IDS)).min(1, 'Pick at least one scope'),
});

type Manager = { orgId: string; userId: string; role: Role };

/** The list in Settings: never the key, only what identifies it. */
export async function listApiKeys({ orgId }: { orgId: string }) {
  return withOrg(orgId, (tx) =>
    tx
      .select({
        id: apiKeys.id,
        name: apiKeys.name,
        keyStart: apiKeys.keyStart,
        keyLast4: apiKeys.keyLast4,
        scopes: apiKeys.scopes,
        lastUsedAt: apiKeys.lastUsedAt,
        revokedAt: apiKeys.revokedAt,
        createdAt: apiKeys.createdAt,
        createdByName: schema.users.name,
      })
      .from(apiKeys)
      .leftJoin(schema.users, eq(schema.users.id, apiKeys.createdBy))
      .where(eq(apiKeys.organizationId, orgId))
      .orderBy(desc(apiKeys.createdAt)),
  );
}

/**
 * Create a key. Returns the full key ONCE: the caller shows it and forgets it.
 * Lesson 1.3: you cannot mint a key that can do more than your role can.
 */
export async function createApiKey(ctx: Manager, input: z.infer<typeof createApiKeyInput>): Promise<{ id: string; key: string }> {
  if (!canGrantScopes(ctx.role, input.scopes)) throw new AccessError('forbidden');
  const { key, hash, start, last4 } = generateApiKey();
  const scopes = [...new Set(input.scopes)];
  const row = await withOrg(ctx.orgId, async (tx) => {
    const [created] = await tx
      .insert(apiKeys)
      .values({ organizationId: ctx.orgId, name: input.name, keyHash: hash, keyStart: start, keyLast4: last4, scopes, createdBy: ctx.userId })
      .returning({ id: apiKeys.id });
    await trackInTx(tx, ctx, 'api_key_created', { scope_count: scopes.length }); // lesson 6.2: how many scopes, never the key or its name
    return created;
  });
  return { id: row.id, key };
}

/** Revoke: the very next request with the key gets a 401 (there is no cache to wait for). */
export async function revokeApiKey(ctx: Manager, keyId: string): Promise<void> {
  if (!isUuid(keyId)) throw new AccessError('not_found');
  const updated = await withOrg(ctx.orgId, (tx) =>
    tx
      .update(apiKeys)
      .set({ revokedAt: new Date(), revokedBy: ctx.userId })
      .where(and(eq(apiKeys.organizationId, ctx.orgId), eq(apiKeys.id, keyId)))
      .returning({ id: apiKeys.id, revokedAt: apiKeys.revokedAt }),
  );
  if (updated.length === 0) throw new AccessError('not_found');
}

export type VerifiedKey = { keyId: string; orgId: string; plan: (typeof organizations.$inferSelect)['plan']; scopes: ApiScope[]; createdBy: string | null };

/**
 * The hot path: is this a live key, and whose? Hash it and look the hash up
 * (the unique index makes it one index read). A revoked key, or anything that
 * is not a key, is null → 401. Also returns the org's plan, for the `api`
 * entitlement and the rate limit.
 */
export async function verifyApiKey(presented: string, now = new Date()): Promise<VerifiedKey | null> {
  if (!looksLikeApiKey(presented)) return null;
  const hash = hashApiKey(presented);
  const [row] = await db
    .select({ key: apiKeys, plan: organizations.plan })
    .from(apiKeys)
    .innerJoin(organizations, eq(organizations.id, apiKeys.organizationId))
    .where(eq(apiKeys.keyHash, hash));
  if (!row || row.key.revokedAt || !sameHash(row.key.keyHash, hash)) return null;
  await touchLastUsed(row.key.id, now);
  return { keyId: row.key.id, orgId: row.key.organizationId, plan: row.plan, scopes: row.key.scopes as ApiScope[], createdBy: row.key.createdBy };
}

/**
 * "Last used", for spotting dead keys. At most one write per key per minute:
 * a busy integration should not turn every GET into an UPDATE.
 */
async function touchLastUsed(keyId: string, now: Date) {
  const aMinuteAgo = new Date(now.getTime() - 60_000);
  await db
    .update(apiKeys)
    .set({ lastUsedAt: now })
    .where(and(eq(apiKeys.id, keyId), or(isNull(apiKeys.lastUsedAt), lt(apiKeys.lastUsedAt, aMinuteAgo))));
}
