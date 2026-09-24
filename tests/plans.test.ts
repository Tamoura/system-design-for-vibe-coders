import { readdirSync, readFileSync, statSync } from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import {
  cheapestPlanWhere,
  effectiveIntervalSec,
  entitlementsFor,
  hasPlanAtLeast,
  isDowngrade,
  planForPrice,
  planFreeze,
  planFromSubscriptions,
  PLANS,
  statusGrantsAccess,
} from '@/core/plans';
import { isDue } from '@/core/schedule';

/* Lesson 3.2: the plan config and the pure rules around it. */

const env = { STRIPE_PRICE_PRO: 'price_pro_live', STRIPE_PRICE_BUSINESS: 'price_business_live' };

describe('plans (lesson 3.2)', () => {
  it('matches the pricing page: Free 5 × 5 min, Pro 50 × 1 min + 100 SMS, Business 500 × 30 s + SSO, audit log, API', () => {
    expect(entitlementsFor('free')).toMatchObject({ maxMonitors: 5, minIntervalSec: 300, smsCreditsPerMonth: 0, sso: false });
    expect(entitlementsFor('pro')).toMatchObject({ maxMonitors: 50, minIntervalSec: 60, smsCreditsPerMonth: 100, api: false });
    expect(entitlementsFor('business')).toMatchObject({ maxMonitors: 500, minIntervalSec: 30, sso: true, auditLog: true, api: true });
  });

  it('every plan has the same entitlement keys', () => {
    const keys = Object.values(PLANS).map((p) => Object.keys(p.entitlements).sort().join());
    expect(new Set(keys).size).toBe(1);
  });

  it('names the cheapest plan that unlocks something, for upgrade prompts', () => {
    expect(cheapestPlanWhere((e) => e.minIntervalSec <= 60)).toBe('pro');
    expect(cheapestPlanWhere((e) => e.minIntervalSec <= 30)).toBe('business');
    expect(cheapestPlanWhere((e) => e.maxMonitors > 500)).toBeNull();
  });

  it('compares plans by rank', () => {
    expect(isDowngrade('pro', 'free')).toBe(true);
    expect(isDowngrade('free', 'business')).toBe(false);
    expect(hasPlanAtLeast('business', 'pro')).toBe(true);
    expect(hasPlanAtLeast('free', 'pro')).toBe(false);
  });

  it('`grep -rn "plan ===" src/` finds nothing outside the plans module (no plan name compared to a string)', () => {
    const walk = (p: string): string[] =>
      statSync(p).isDirectory() ? readdirSync(p).flatMap((f) => walk(path.join(p, f))) : /\.(ts|tsx)$/.test(p) ? [p] : [];
    const offenders = walk('src')
      .filter((f) => !f.endsWith(path.join('core', 'plans.ts')))
      .filter((f) => /plan\s*[!=]==\s*['"`]|['"`]\s*[!=]==\s*\w*plan\b/i.test(readFileSync(f, 'utf8')));
    expect(offenders).toEqual([]);
  });
});

describe('Stripe price → plan (lessons 3.1 and 3.2)', () => {
  it('maps the configured prices and fails closed for unknown ones', () => {
    expect(planForPrice('price_pro_live', env)).toBe('pro');
    expect(planForPrice('price_business_live', env)).toBe('business');
    expect(planForPrice('price_something_else', env)).toBe('free');
    expect(planForPrice(null, env)).toBe('free');
  });

  it('decides what each subscription status grants in one place', () => {
    for (const s of ['trialing', 'active', 'past_due']) expect(statusGrantsAccess(s)).toBe(true);
    for (const s of ['incomplete', 'incomplete_expired', 'canceled', 'unpaid', 'paused']) expect(statusGrantsAccess(s)).toBe(false);
  });

  it('a trialing or past_due Pro subscription is Pro, a canceled one is Free (not only "active")', () => {
    expect(planFromSubscriptions([{ status: 'trialing', priceId: 'price_pro_live' }], env)).toBe('pro');
    expect(planFromSubscriptions([{ status: 'past_due', priceId: 'price_pro_live' }], env)).toBe('pro');
    expect(planFromSubscriptions([{ status: 'canceled', priceId: 'price_business_live' }], env)).toBe('free');
    expect(planFromSubscriptions([], env)).toBe('free');
  });

  it('the best plan wins when an org has several subscriptions', () => {
    const subs = [
      { status: 'canceled', priceId: 'price_business_live' },
      { status: 'active', priceId: 'price_pro_live' },
    ];
    expect(planFromSubscriptions(subs, env)).toBe('pro');
  });
});

describe('the freeze policy (lesson 3.2 🟡)', () => {
  const at = (minute: number) => new Date(Date.UTC(2026, 0, 1, 0, minute));
  const monitors = (n: number) => Array.from({ length: n }, (_, i) => ({ id: `m${i + 1}`, createdAt: at(i), pausedReason: null as null | 'manual' | 'plan_limit' }));

  it('Pro → Free with 12 monitors: the 7 newest are frozen, the 5 oldest keep running', () => {
    const { freeze, unfreeze } = planFreeze(monitors(12), 5);
    expect(freeze).toEqual(['m6', 'm7', 'm8', 'm9', 'm10', 'm11', 'm12']);
    expect(unfreeze).toEqual([]);
  });

  it('an upgrade unfreezes the oldest plan-paused monitors, never manually paused ones', () => {
    const ms = monitors(8);
    ms[1].pausedReason = 'manual';
    for (const m of ms.slice(5)) m.pausedReason = 'plan_limit';
    const { freeze, unfreeze } = planFreeze(ms, 50);
    expect(freeze).toEqual([]);
    expect(unfreeze).toEqual(['m6', 'm7', 'm8']);
  });

  it('is idempotent: at the limit, nothing changes', () => {
    const ms = monitors(7);
    for (const m of ms.slice(5)) m.pausedReason = 'plan_limit';
    expect(planFreeze(ms, 5)).toEqual({ freeze: [], unfreeze: [] });
  });
});

describe('the check runner never runs faster than the plan allows (lesson 3.2 🟡)', () => {
  const now = new Date('2026-06-01T12:00:00Z');
  const ago = (s: number) => new Date(now.getTime() - s * 1000);
  const free = entitlementsFor('free');

  it('uses the larger of the monitor interval and the plan minimum', () => {
    expect(effectiveIntervalSec(60, free)).toBe(300);
    expect(effectiveIntervalSec(900, free)).toBe(900);
  });

  it('a 60-second monitor on Free is due only every 5 minutes', () => {
    expect(isDue({ paused: false, intervalSeconds: 60, lastCheckedAt: ago(90) }, free, now)).toBe(false);
    expect(isDue({ paused: false, intervalSeconds: 60, lastCheckedAt: ago(300) }, free, now)).toBe(true);
    expect(isDue({ paused: false, intervalSeconds: 60, lastCheckedAt: ago(90) }, entitlementsFor('pro'), now)).toBe(true);
  });

  it('never runs a paused monitor, and runs a new one at once', () => {
    expect(isDue({ paused: true, intervalSeconds: 300, lastCheckedAt: null }, free, now)).toBe(false);
    expect(isDue({ paused: false, intervalSeconds: 300, lastCheckedAt: null }, free, now)).toBe(true);
  });
});

