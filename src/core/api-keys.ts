import { createHash, randomBytes, timingSafeEqual } from 'node:crypto';
import { can, type Permission } from './permissions';
import type { Role } from './roles';

/*
 * Lesson 5.2 (🟢): API keys, the way Stripe and Unkey do them.
 *
 *   bk_live_Q2hMvT8…  (8-character prefix + 32 random bytes, base64url)
 *
 *  - PREFIXED: people (and GitHub's secret scanning) can tell what it is.
 *  - HASHED at rest: the table keeps SHA-256(key), the first 12 characters
 *    and the last 4, for display. A fast hash is fine: unlike a password, 32
 *    random bytes cannot be guessed, so a database leak leaks nothing usable.
 *  - SHOWN ONCE: the full key exists only in the response that created it.
 *  - SCOPED: a key can do only what its scopes say (and never more than the
 *    role that created it, lesson 1.3).
 *  - OWNED BY THE ORG, with "created by" kept for history: when that person
 *    leaves, the integration keeps working. Revocable, with last-used time.
 */
export const API_KEY_PREFIX = 'bk_live_';

export function generateApiKey(): { key: string; hash: string; start: string; last4: string } {
  const key = `${API_KEY_PREFIX}${randomBytes(32).toString('base64url')}`;
  return { key, hash: hashApiKey(key), start: key.slice(0, 12), last4: key.slice(-4) };
}

export function hashApiKey(key: string): string {
  return createHash('sha256').update(key).digest('hex');
}

/** Does this look like a Beacon key at all? (Cheap filter before any database work.) */
export function looksLikeApiKey(value: string): boolean {
  return value.startsWith(API_KEY_PREFIX) && /^[A-Za-z0-9_-]{40,60}$/.test(value.slice(API_KEY_PREFIX.length));
}

/** `Authorization: Bearer bk_live_…` → the key, or null. */
export function bearerToken(header: string | null): string | null {
  const m = /^Bearer\s+(\S+)\s*$/i.exec(header ?? '');
  return m ? m[1] : null;
}

/** Constant-time comparison of two hex hashes (the lookup is by hash; this double-checks it). */
export function sameHash(a: string, b: string): boolean {
  const x = Buffer.from(a, 'hex');
  const y = Buffer.from(b, 'hex');
  return x.length === y.length && timingSafeEqual(x, y);
}

/**
 * The scopes a key can have, and the Module 1 permission each one stands for.
 * A person may only give a key scopes their own role has (canGrantScopes).
 * Writing monitors through the API means any monitor of the org, so it needs
 * "monitor.write_any" (owners and admins), not just "monitor.write".
 */
export const API_SCOPES = {
  'monitors:read': { permission: 'monitor.read', label: 'Read monitors' },
  'monitors:write': { permission: 'monitor.write_any', label: 'Create, change and delete monitors' },
  'incidents:read': { permission: 'monitor.read', label: 'Read incidents' },
} as const satisfies Record<string, { permission: Permission; label: string }>;

export type ApiScope = keyof typeof API_SCOPES;
export const API_SCOPE_IDS = Object.keys(API_SCOPES) as [ApiScope, ...ApiScope[]];

export function isApiScope(value: string): value is ApiScope {
  return Object.hasOwn(API_SCOPES, value);
}

export function canGrantScopes(role: Role, scopes: readonly ApiScope[]): boolean {
  return can(role, 'integration.manage') && scopes.every((s) => can(role, API_SCOPES[s].permission));
}
