import { sql } from 'drizzle-orm';
import { db } from '@/db';
import { PLAN_IDS, type PlanId } from '@/core/plans';

/*
 * Lesson 6.2 (🟡): the activation funnel, for Beacon's own team
 * (/internal/analytics, staff only).
 *
 *   org_created ─► monitor_created ─► first monitor_check_completed within 24 h (= activated, lesson 6.1)
 *
 * Counted per ORGANIZATION, not per user (B2B: the org is the customer), and
 * broken down by the org's plan today, so "do orgs that end up on Pro activate
 * faster?" is one glance.
 *
 * This reads ACROSS tenants on purpose, as the database owner: it is an
 * internal report, never reachable by a customer (it is exempt from the
 * withOrg() lint in tests/tenant-scoping.test.ts for that reason). At scale it
 * runs on a replica or in the warehouse, not on the primary (lesson 6.2).
 */

export type FunnelRow = {
  plan: PlanId | 'all';
  /** The last row: every plan together. */
  isTotal: boolean;
  orgs: number;
  withMonitor: number;
  withCheck: number;
  activated: number;
  /** Median time from org_created to the first check, for activated orgs. */
  medianMinutesToActivation: number | null;
};

type Raw = { plan: PlanId | null; orgs: number; with_monitor: number; with_check: number; activated: number; median_seconds: number | null };

export async function activationFunnel(opts: { since: Date; until?: Date }): Promise<FunnelRow[]> {
  const until = opts.until ?? new Date();
  const result = (await db.execute(sql`
    with cohort as (
      select organization_id, min(occurred_at) as created_at
      from analytics_events
      where event = 'org_created' and occurred_at >= ${opts.since.toISOString()} and occurred_at < ${until.toISOString()}
      group by organization_id
    ),
    steps as (
      select c.organization_id, o.plan, c.created_at,
        (select min(occurred_at) from analytics_events e
          where e.organization_id = c.organization_id and e.event = 'monitor_created') as monitor_at,
        (select min(occurred_at) from analytics_events e
          where e.organization_id = c.organization_id and e.event = 'monitor_check_completed') as check_at
      from cohort c join organizations o on o.id = c.organization_id
    )
    select grouping(plan) = 1 as is_total, plan::text as plan,
      count(*)::int as orgs,
      count(monitor_at)::int as with_monitor,
      count(check_at)::int as with_check,
      (count(*) filter (where check_at <= created_at + interval '24 hours'))::int as activated,
      (percentile_cont(0.5) within group (order by extract(epoch from check_at - created_at))
        filter (where check_at <= created_at + interval '24 hours'))::float8 as median_seconds
    from steps
    group by rollup (plan)
  `)) as unknown as (Raw & { is_total: boolean })[] | { rows: (Raw & { is_total: boolean })[] };
  const rows = Array.isArray(result) ? result : result.rows;
  const byPlan = new Map(rows.filter((r) => !r.is_total).map((r) => [r.plan, r]));
  const total = rows.find((r) => r.is_total);
  const toRow = (plan: FunnelRow['plan'], r: Raw | undefined, isTotal = false): FunnelRow => ({
    plan,
    isTotal,
    orgs: r?.orgs ?? 0,
    withMonitor: r?.with_monitor ?? 0,
    withCheck: r?.with_check ?? 0,
    activated: r?.activated ?? 0,
    medianMinutesToActivation: r?.median_seconds == null ? null : Math.round(Number(r.median_seconds) / 60),
  });
  return [...PLAN_IDS.map((p) => toRow(p, byPlan.get(p))), toRow('all', total, true)];
}

export type RecentEvent = { event: string; orgSlug: string; orgPlan: string; userId: string | null; properties: Record<string, unknown>; occurredAt: Date };

/** The latest events across all orgs, so staff can see what is recorded (ids, enums and numbers; nothing personal). */
export async function recentEvents(limit = 25): Promise<RecentEvent[]> {
  const result = (await db.execute(sql`
    select e.event, o.slug as org_slug, e.org_plan::text as org_plan, e.user_id, e.properties, e.occurred_at
    from analytics_events e join organizations o on o.id = e.organization_id
    order by e.occurred_at desc
    limit ${limit}
  `)) as unknown as RawEvent[] | { rows: RawEvent[] };
  const rows = Array.isArray(result) ? result : result.rows;
  return rows.map((r) => ({ event: r.event, orgSlug: r.org_slug, orgPlan: r.org_plan, userId: r.user_id, properties: r.properties, occurredAt: new Date(r.occurred_at) }));
}
type RawEvent = { event: string; org_slug: string; org_plan: string; user_id: string | null; properties: Record<string, unknown>; occurred_at: string | Date };
