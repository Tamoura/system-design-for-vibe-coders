import { createHash } from 'node:crypto';

/*
 * Lesson 6.3: feature flags, the pure part (no database, no network).
 *
 * A flag is a runtime `if` whose condition lives OUTSIDE the code: the rules
 * are rows in `feature_flags` and `feature_flag_overrides`, changed from
 * /internal/flags or `npm run flags` without a deploy. This file knows:
 *
 *   FLAGS           which flags exist, their type, owner, expiry, safe default
 *                   and how to remove them. Reviewed in pull requests, like code.
 *   rolloutBucket   the consistent hash: flag key + org id → 0..99
 *   evaluateFlag    the rules → on or off for one org, and why
 *
 * Flags are NOT entitlements. "Business gets the API" is pricing and lives in
 * src/core/plans.ts (lesson 3.2); nothing here reads a plan, and nothing in
 * plans.ts reads a flag. A flag can hide a feature from an org that is
 * entitled to it, never show one to an org that is not (tests/flags.test.ts).
 */

/** Pete Hodgson's flag types (lesson 6.3). They decide how long a flag should live. */
export type FlagKind = 'release' | 'ops' | 'permission' | 'experiment';

export type FlagDefinition = {
  kind: FlagKind;
  description: string;
  /** Who answers for it, and who deletes it. */
  owner: string;
  /** Release, permission and experiment flags are temporary: the date to have removed it by. Ops flags live on (null). */
  expires: string | null;
  /** The value when there is no rule, or the rules cannot be loaded. Always the SAFE one: the old code path. */
  defaultValue: boolean;
  /** The removal ticket: what to delete when the flag is done. Never reuse the name afterwards (Knight Capital). */
  cleanup: string;
};

export const FLAGS = {
  // Lesson 6.3 (🟡): the release flag from the exercise. Grep for TODO(flag:new-scheduler) to find the branch to delete.
  'new-scheduler': {
    kind: 'release',
    description: "The scheduler's first-check rule: a monitor that has never been checked gets a check within a minute, instead of waiting for its first phase slot (up to its whole interval).",
    owner: 'platform team (scheduler)',
    expires: '2026-12-31',
    defaultValue: false,
    cleanup: 'TODO(flag:new-scheduler): once at 100% for two weeks, delete the flag, its `if` in src/lib/scheduler.ts (keep the new branch) and this entry.',
  },
  // Lesson 6.3 (🟡): the ops kill switch. ON means SMS are NOT sent. Long-lived by design.
  'disable-sms-sending': {
    kind: 'ops',
    description: 'Kill switch for on-call: stop sending SMS (for example during an SMS provider outage). Deliveries are logged as skipped; email, Slack and in-app still go out.',
    owner: 'on-call (infrastructure)',
    expires: null,
    defaultValue: false,
    cleanup: 'Permanent ops flag. Review yearly; delete it if SMS is ever removed.',
  },
  // A permission (beta) flag with a UI, for trying targeting by hand: a response-time chart on the monitor page.
  'monitor-latency-chart': {
    kind: 'permission',
    description: 'Beta: a response-time chart on the monitor page, for chosen organizations first.',
    owner: 'product (monitors)',
    expires: '2027-03-31',
    defaultValue: false,
    cleanup: 'TODO(flag:monitor-latency-chart): when released to everyone, delete the flag and the check in src/app/[orgSlug]/monitors/[id]/page.tsx.',
  },
} as const satisfies Record<string, FlagDefinition>;

export type FlagKey = keyof typeof FLAGS;

export function isFlagKey(key: unknown): key is FlagKey {
  return typeof key === 'string' && Object.hasOwn(FLAGS, key);
}

/** One flag's stored rule (a row of `feature_flags`). */
export type FlagRule = {
  /** The master switch. false = off for EVERY org, overrides included: the kill switch. */
  enabled: boolean;
  /** 0–100: the share of orgs (by hash) that get it. */
  rolloutPercent: number;
};

/** Everything a process needs to evaluate every flag locally, in memory. */
export type RuleSet = {
  flags: Record<string, FlagRule>;
  /** flag key → org id → on/off, for chosen orgs (your own org, a beta customer). */
  overrides: Record<string, Record<string, boolean>>;
};

export const EMPTY_RULES: RuleSet = { flags: {}, overrides: {} };

/**
 * Lesson 6.3 (🟡), "percentage rollouts need consistent hashing". The flag key
 * and the org id, hashed, give a number 0–99 that never changes:
 *
 *  - the same org gets the same answer on every request, in every process
 *    (the web app and the worker agree, with no shared state);
 *  - raising 10% → 30% keeps the first 10% in (bucket < 10 implies < 30);
 *  - the flag key is in the hash, so different flags pick different 10%
 *    slices and the same unlucky customers do not get every beta.
 *
 * Never Math.random(): an org would flip between old and new on every request.
 * SHA-256 is overkill for speed but built in; tools use MurmurHash3 or SHA-1.
 */
export function rolloutBucket(flagKey: string, orgId: string): number {
  const n = createHash('sha256').update(`${flagKey}:${orgId}`).digest().readUInt32BE(0);
  return n % 100;
}

export type EvaluationReason =
  | 'DEFAULT' //         no rule for this flag: its safe default
  | 'DISABLED' //        the master switch is off (kill switch): off for everyone
  | 'TARGETING_MATCH' // an override for this org
  | 'SPLIT'; //          the org's bucket against the rollout percentage

/**
 * Lesson 6.3 (🟢): the exercise's isEnabled(key, orgId), pure. In order:
 *
 *   1. no rule stored         → the flag's safe default
 *   2. master switch off      → off, for everyone (the kill switch beats overrides)
 *   3. an override for the org → that value ("on for our own org", "off for Acme")
 *   4. otherwise              → on if rolloutBucket(key, org) < rolloutPercent
 *
 * The exercise checks overrides first; Beacon puts the master switch above
 * them so one click turns a misbehaving feature off everywhere.
 */
export function evaluateFlag(rules: RuleSet, key: string, orgId: string, defaultValue: boolean): { value: boolean; reason: EvaluationReason } {
  const rule = rules.flags[key];
  if (!rule) return { value: defaultValue, reason: 'DEFAULT' };
  if (!rule.enabled) return { value: false, reason: 'DISABLED' };
  const override = rules.overrides[key]?.[orgId];
  if (override !== undefined) return { value: override, reason: 'TARGETING_MATCH' };
  return { value: rolloutBucket(key, orgId) < rule.rolloutPercent, reason: 'SPLIT' };
}

export function isValidRolloutPercent(n: unknown): n is number {
  return typeof n === 'number' && Number.isInteger(n) && n >= 0 && n <= 100;
}
