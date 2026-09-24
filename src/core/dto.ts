import type { Monitor } from '@/db/schema';
import type { Entitlements } from './plans';

/*
 * Lesson 1.3: response DTOs. An API returns an allow-listed shape, never the
 * raw row, so a column added later (organization_id today, a secret tomorrow)
 * cannot leak into a response by accident.
 */

export type MonitorDto = {
  id: string;
  name: string;
  url: string;
  intervalSeconds: number;
  paused: boolean;
  /** Lesson 3.2: 'manual', or 'plan_limit' when a downgrade froze it. */
  pausedReason: 'manual' | 'plan_limit' | null;
  createdAt: string;
};

export function toMonitorDto(m: Monitor): MonitorDto {
  return {
    id: m.id,
    name: m.name,
    url: m.url,
    intervalSeconds: m.intervalSeconds,
    paused: m.paused,
    pausedReason: m.pausedReason,
    createdAt: m.createdAt.toISOString(),
  };
}

export type MemberDto = { userId: string; name: string; email: string; role: string; joinedAt: string };

export function toMemberDto(m: { userId: string; name: string; email: string; role: string; joinedAt: Date }): MemberDto {
  return { userId: m.userId, name: m.name, email: m.email, role: m.role, joinedAt: m.joinedAt.toISOString() };
}

/**
 * Lesson 3.1: what GET /api/orgs/:org/billing returns. No Stripe ids
 * (customer, subscription, price) and no org id: a client needs the plan, the
 * limits and the monitors, nothing it could use against Stripe.
 */
export type BillingDto = {
  plan: string;
  entitlements: Entitlements;
  monitors: { total: number; running: number; frozen: number; max: number };
  subscription: { status: string; cancelAtPeriodEnd: boolean; currentPeriodEnd: string | null } | null;
};

export function toBillingDto(o: {
  ent: Entitlements & { plan: string };
  monitors: { total: number; running: number; frozen: number };
  subscription: { status: string; cancelAtPeriodEnd: boolean; currentPeriodEnd: Date | null } | null;
}): BillingDto {
  const { plan, ...entitlements } = o.ent;
  return {
    plan,
    entitlements,
    monitors: { total: o.monitors.total, running: o.monitors.running, frozen: o.monitors.frozen, max: entitlements.maxMonitors },
    subscription: o.subscription
      ? { status: o.subscription.status, cancelAtPeriodEnd: o.subscription.cancelAtPeriodEnd, currentPeriodEnd: o.subscription.currentPeriodEnd?.toISOString() ?? null }
      : null,
  };
}
