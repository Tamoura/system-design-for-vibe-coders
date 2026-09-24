/*
 * Lesson 3.2: plans, limits and entitlements — the ONE module that knows plan
 * names.
 *
 *   plan         a named package on the pricing page (Free, Pro, Business)
 *   entitlement  one thing an organization may do or have:
 *                  a feature gate  (sso, auditLog, api)
 *                  a limit         (maxMonitors, smsCreditsPerMonth)
 *                  a config value  (minIntervalSec)
 *
 * The rule: code everywhere else asks "is this org entitled to X?"
 * (`ent.maxMonitors`, `ent.sso`), never "which plan is this org on?". Adding
 * a "Starter" plan is then one entry below instead of forty `if`s across the
 * app. `grep -rn "plan ===" src/` finds nothing outside this file.
 *
 * The lesson calls this file lib/plans.ts. In Beacon it lives in src/core
 * because it is pure (no database, no network): the server enforces it, the
 * forms read it to disable options, and the tests import it directly.
 */

export const PLAN_IDS = ['free', 'pro', 'business'] as const;
export type PlanId = (typeof PLAN_IDS)[number];

export type Entitlements = {
  /** How many monitors the org may have. */
  maxMonitors: number;
  /** The shortest check interval, in seconds. */
  minIntervalSec: number;
  /** SMS segments included each billing period (lesson 3.3). 0 = no SMS alerts. */
  smsCreditsPerMonth: number;
  /** Feature gates. Their features arrive in later lessons (1.4, 7.3, 5.2). */
  sso: boolean;
  auditLog: boolean;
  api: boolean;
};

type Plan = {
  name: string;
  priceLabel: string;
  /** One line for the pricing cards. */
  pitch: string;
  entitlements: Entitlements;
};

/** Lesson 3.2's pricing table, as data. Order matters: cheapest first (see planRank). */
export const PLANS: Record<PlanId, Plan> = {
  free: {
    name: 'Free',
    priceLabel: '$0',
    pitch: '5 monitors, checked every 5 minutes',
    entitlements: { maxMonitors: 5, minIntervalSec: 300, smsCreditsPerMonth: 0, sso: false, auditLog: false, api: false },
  },
  pro: {
    name: 'Pro',
    priceLabel: '$29/month',
    pitch: '50 monitors, 1-minute checks, 100 SMS alerts a month',
    entitlements: { maxMonitors: 50, minIntervalSec: 60, smsCreditsPerMonth: 100, sso: false, auditLog: false, api: false },
  },
  business: {
    name: 'Business',
    priceLabel: '$99/month',
    pitch: '500 monitors, 30-second checks, 500 SMS, SSO, audit log and API',
    entitlements: { maxMonitors: 500, minIntervalSec: 30, smsCreditsPerMonth: 500, sso: true, auditLog: true, api: true },
  },
};

/** Lesson 3.3: SMS beyond the included credits costs $0.05 per segment. */
export const SMS_OVERAGE_CENTS = 5;

export function isPlanId(value: unknown): value is PlanId {
  return typeof value === 'string' && (PLAN_IDS as readonly string[]).includes(value);
}

export function entitlementsFor(plan: PlanId): Entitlements {
  return PLANS[plan].entitlements;
}

/** Free 0, Pro 1, Business 2. Only for comparing plans, never for gating a feature. */
export function planRank(plan: PlanId): number {
  return PLAN_IDS.indexOf(plan);
}

export function isDowngrade(from: PlanId, to: PlanId): boolean {
  return planRank(to) < planRank(from);
}

/** For "confirming your payment…": has the org reached (at least) the plan it paid for? */
export function hasPlanAtLeast(current: PlanId, target: PlanId): boolean {
  return planRank(current) >= planRank(target);
}

/** The plans a customer can buy in Checkout. */
export const PAID_PLANS = ['pro', 'business'] as const satisfies readonly PlanId[];
export type PaidPlanId = (typeof PAID_PLANS)[number];

export function isPaidPlanId(value: unknown): value is PaidPlanId {
  return typeof value === 'string' && (PAID_PLANS as readonly string[]).includes(value);
}

/**
 * The cheapest plan that grants something, for upgrade prompts: "Upgrade to
 * Business for 30-second checks". Null if no plan does.
 */
export function cheapestPlanWhere(test: (e: Entitlements) => boolean): PlanId | null {
  return PLAN_IDS.find((p) => test(entitlementsFor(p))) ?? null;
}

/* ---------------------------------------------------------------------------
 * Lesson 3.1 → 3.2: from a Stripe subscription to a plan.
 * ------------------------------------------------------------------------- */

/**
 * Lesson 3.1 (🟡): subscription status is a state machine, and what each state
 * grants is decided HERE, once. The classic bug is `status === 'active'`,
 * which locks out trialing customers and treats past_due like canceled.
 *
 *   trialing, active   the plan
 *   past_due           the plan, during the grace period while Stripe retries
 *   everything else    Free (incomplete: not paid yet; canceled, unpaid,
 *                      incomplete_expired, paused: the plan ended)
 */
const STATUSES_WITH_ACCESS = new Set(['trialing', 'active', 'past_due']);

export function statusGrantsAccess(status: string): boolean {
  return STATUSES_WITH_ACCESS.has(status);
}

/**
 * Stripe Price id → plan. Prices are immutable in Stripe, so a new price
 * (Pro goes from $29 to $39) is a new id; keep the old one in this map too
 * and existing customers stay on Pro (grandfathering, lesson 3.2 🟡).
 *
 * The ids come from the environment (test and live mode have different ids).
 * The `price_fake_…` defaults are what the fake billing provider uses when
 * BILLING_PROVIDER=fake (tests, the smoke test, a laptop without Stripe).
 */
export function stripePriceIds(env: Record<string, string | undefined> = process.env): Record<PaidPlanId, string> {
  return {
    pro: env.STRIPE_PRICE_PRO || 'price_fake_pro',
    business: env.STRIPE_PRICE_BUSINESS || 'price_fake_business',
  };
}

export function planForPrice(priceId: string | null, env?: Record<string, string | undefined>): PlanId {
  const ids = stripePriceIds(env);
  if (priceId === ids.business) return 'business';
  if (priceId === ids.pro) return 'pro';
  return 'free'; // a price we do not know grants nothing: fail closed
}

export function priceForPlan(plan: PaidPlanId, env?: Record<string, string | undefined>): string {
  return stripePriceIds(env)[plan];
}

/**
 * The plan an organization's subscriptions entitle it to: the best plan among
 * the subscriptions whose status grants access, or Free.
 */
export function planFromSubscriptions(subs: { status: string; priceId: string | null }[], env?: Record<string, string | undefined>): PlanId {
  let best: PlanId = 'free';
  for (const s of subs) {
    if (!statusGrantsAccess(s.status)) continue;
    const plan = planForPrice(s.priceId, env);
    if (planRank(plan) > planRank(best)) best = plan;
  }
  return best;
}

/* ---------------------------------------------------------------------------
 * Lesson 3.2 (🟡): downgrades. Beacon's policy is FREEZE: nothing is deleted,
 * the newest monitors beyond the limit are paused with reason "plan_limit",
 * and they run again after an upgrade (or when the owner picks them).
 * ------------------------------------------------------------------------- */

export type PausedReason = 'manual' | 'plan_limit';

/**
 * Which monitors to freeze or unfreeze so that at most `maxMonitors` run.
 *
 *  - more running than allowed → freeze the newest running ones
 *  - room to spare and some frozen → unfreeze the oldest frozen ones
 *
 * Monitors someone paused by hand ('manual') are never touched: an upgrade
 * must not switch on a monitor a person switched off.
 */
export function planFreeze(
  monitors: { id: string; createdAt: Date; pausedReason: PausedReason | null }[],
  maxMonitors: number,
): { freeze: string[]; unfreeze: string[] } {
  const oldestFirst = [...monitors].sort((a, b) => a.createdAt.getTime() - b.createdAt.getTime() || a.id.localeCompare(b.id));
  const running = oldestFirst.filter((m) => m.pausedReason === null);
  const frozen = oldestFirst.filter((m) => m.pausedReason === 'plan_limit');
  if (running.length > maxMonitors) return { freeze: running.slice(maxMonitors).map((m) => m.id), unfreeze: [] };
  return { freeze: [], unfreeze: frozen.slice(0, maxMonitors - running.length).map((m) => m.id) };
}

/**
 * Lesson 3.2 (🟡): "the scheduler never runs checks faster than the org's
 * current minimum". The interval a monitor actually runs at.
 */
export function effectiveIntervalSec(intervalSeconds: number, ent: Pick<Entitlements, 'minIntervalSec'>): number {
  return Math.max(intervalSeconds, ent.minIntervalSec);
}
