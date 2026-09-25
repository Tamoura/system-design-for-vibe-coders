import { SMS_OVERAGE_CENTS, type Entitlements } from './plans';

/*
 * Lesson 3.3: usage-based billing, the pure parts.
 *
 *   usage event → meter → aggregate per billing period → rate → invoice line
 *
 * The database side (recording, summing, reporting) is src/lib/usage.ts.
 */

/** Lesson 3.3: the meters Beacon records. The name is also the Stripe meter's event name. */
export const METERS = { sms: 'sms_segments', aiTokens: 'ai_tokens' } as const;
export type Meter = (typeof METERS)[keyof typeof METERS];

/**
 * Lesson 3.3 (🟢), "idempotency is the whole game": the key is derived from
 * the business fact, so a retried job produces the SAME key and the unique
 * constraint turns the duplicate into a no-op. A random UUID made at send
 * time would be different on every retry and bill the customer twice.
 */
export const usageKeys = {
  /** One SMS, by the provider's message id (Twilio's `SM…` SID). */
  sms: (messageSid: string) => `sms:${messageSid}`,
  /** Lesson 8.2: one model call, by its llm_usage row (tokens in + out). */
  aiCall: (usageId: string) => `ai:${usageId}`,
};

export type Period = { start: Date; end: Date };

/**
 * Lesson 3.3 (🟢): usage counts per BILLING period, which is anchored to the
 * subscription (Acme's cycle runs from the 14th to the 13th), not the calendar
 * month. Without a subscription (Free) there is no billing period, so Beacon
 * falls back to the calendar month in UTC.
 */
export function billingPeriod(subscription: { currentPeriodStart: Date | null; currentPeriodEnd: Date | null } | null, now: Date = new Date()): Period {
  if (subscription?.currentPeriodStart && subscription.currentPeriodEnd) {
    return { start: subscription.currentPeriodStart, end: subscription.currentPeriodEnd };
  }
  const start = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), 1));
  const end = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() + 1, 1));
  return { start, end };
}

/**
 * Lesson 3.3: rating, "included + overage". Pro includes 100 SMS; the 130th
 * costs $0.05, so 130 SMS → 30 × 5¢ = $1.50. Stripe does the same sum on the
 * invoice (a graduated price whose first tier is free, see docs/SOLUTIONS.md);
 * this copy is for the usage view ("projected overage").
 */
export function rateSms(used: number, ent: Pick<Entitlements, 'smsCreditsPerMonth'>) {
  const included = ent.smsCreditsPerMonth;
  const overageUnits = Math.max(0, used - included);
  return { used, included, overageUnits, overageCents: overageUnits * SMS_OVERAGE_CENTS };
}

export function formatCents(cents: number): string {
  return `$${(cents / 100).toFixed(2)}`;
}

/** Lesson 3.3 (🟡): alert at 80% and 100% of the included amount. */
export const USAGE_ALERT_THRESHOLDS = [80, 100] as const;

/** The thresholds `used` has reached, as percentages of `included`. */
export function reachedThresholds(used: number, included: number): number[] {
  if (included <= 0) return [];
  return USAGE_ALERT_THRESHOLDS.filter((t) => used * 100 >= included * t);
}
