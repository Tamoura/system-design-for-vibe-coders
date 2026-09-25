import { and, asc, eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { FLAGS, isFlagKey, isValidRolloutPercent, type FlagKey, type RuleSet } from '@/core/flags';

const { featureFlags, featureFlagOverrides, organizations } = schema;

/*
 * Lesson 6.3: the flag rules in Postgres. Beacon's own tiny "flag service":
 * the provider (./provider.ts) loads the whole rule set, and staff change it
 * from /internal/flags or `npm run flags`. These are platform tables, not
 * tenant data, so they are read and written as the database owner.
 * TODO(7.3): write every change to the audit log ("who turned off SMS at 02:00?").
 */

/** Everything, for local evaluation: two small queries, whatever the number of orgs. */
export async function loadRuleSet(): Promise<RuleSet> {
  const [flags, overrides] = await Promise.all([db.select().from(featureFlags), db.select().from(featureFlagOverrides)]);
  const rules: RuleSet = { flags: {}, overrides: {} };
  for (const f of flags) rules.flags[f.key] = { enabled: f.enabled, rolloutPercent: f.rolloutPercent };
  for (const o of overrides) (rules.overrides[o.key] ??= {})[o.organizationId] = o.enabled;
  return rules;
}

export class FlagInputError extends Error {}

function assertKnown(key: string): asserts key is FlagKey {
  // Only flags declared in src/core/flags.ts, with an owner and an expiry, can be set.
  if (!isFlagKey(key)) throw new FlagInputError(`Unknown flag "${key}". Declare it in src/core/flags.ts first.`);
}

/**
 * Change a flag's rule. A key with no row yet gets one: master switch ON and
 * 0% (nobody, except overrides), unless the change says otherwise.
 */
export async function setFlagRule(key: string, change: { enabled?: boolean; rolloutPercent?: number }, updatedBy: string | null) {
  assertKnown(key);
  if (change.rolloutPercent !== undefined && !isValidRolloutPercent(change.rolloutPercent)) throw new FlagInputError('Rollout must be a whole number from 0 to 100.');
  const set = { ...change, updatedBy };
  await db
    .insert(featureFlags)
    .values({ key, enabled: change.enabled ?? true, rolloutPercent: change.rolloutPercent ?? 0, updatedBy })
    .onConflictDoUpdate({ target: featureFlags.key, set });
}

/** Target one org: on, off, or (null) back to the percentage. */
export async function setFlagOverride(key: string, orgSlug: string, enabled: boolean | null, updatedBy: string | null) {
  assertKnown(key);
  const [org] = await db.select({ id: organizations.id }).from(organizations).where(eq(organizations.slug, orgSlug));
  if (!org) throw new FlagInputError(`No organization with slug "${orgSlug}".`);
  if (enabled === null) {
    await db.delete(featureFlagOverrides).where(and(eq(featureFlagOverrides.key, key), eq(featureFlagOverrides.organizationId, org.id)));
    return;
  }
  // An override needs its flag's row (foreign key): create it switched on at 0%.
  await db.insert(featureFlags).values({ key, enabled: true, rolloutPercent: 0, updatedBy }).onConflictDoNothing();
  await db
    .insert(featureFlagOverrides)
    .values({ key, organizationId: org.id, enabled, updatedBy })
    .onConflictDoUpdate({ target: [featureFlagOverrides.key, featureFlagOverrides.organizationId], set: { enabled, updatedBy } });
}

export type FlagAdminRow = {
  key: string;
  /** null: in the database but no longer in the code. Delete it (and never reuse the name). */
  definition: (typeof FLAGS)[FlagKey] | null;
  rule: { enabled: boolean; rolloutPercent: number; updatedAt: Date } | null;
  overrides: { orgSlug: string; orgName: string; enabled: boolean }[];
  /** A temporary flag past its expiry date: flag debt. */
  expired: boolean;
};

/** For /internal/flags and `npm run flags`: every flag in the code, plus stale rows only in the database. */
export async function listFlagsForAdmin(now = new Date()): Promise<FlagAdminRow[]> {
  const rules = await db.select().from(featureFlags);
  const overrides = await db
    .select({ key: featureFlagOverrides.key, enabled: featureFlagOverrides.enabled, orgSlug: organizations.slug, orgName: organizations.name })
    .from(featureFlagOverrides)
    .innerJoin(organizations, eq(organizations.id, featureFlagOverrides.organizationId))
    .orderBy(asc(organizations.slug));
  const keys = [...new Set([...Object.keys(FLAGS), ...rules.map((r) => r.key)])];
  return keys.map((key) => {
    const definition = isFlagKey(key) ? FLAGS[key] : null;
    const rule = rules.find((r) => r.key === key);
    return {
      key,
      definition,
      rule: rule ? { enabled: rule.enabled, rolloutPercent: rule.rolloutPercent, updatedAt: rule.updatedAt } : null,
      overrides: overrides.filter((o) => o.key === key).map(({ orgSlug, orgName, enabled }) => ({ orgSlug, orgName, enabled })),
      expired: Boolean(definition?.expires && new Date(`${definition.expires}T23:59:59Z`) < now),
    };
  });
}

/** Remove a stale row (a flag deleted from the code). Its overrides go with it (ON DELETE CASCADE). */
export async function deleteStaleFlag(key: string) {
  if (isFlagKey(key)) throw new FlagInputError(`"${key}" is still declared in src/core/flags.ts. Remove it from the code first.`);
  await db.delete(featureFlags).where(eq(featureFlags.key, key));
}
