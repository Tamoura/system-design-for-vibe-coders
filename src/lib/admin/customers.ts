import { and, asc, count, desc, eq, ilike, inArray, max, or } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { isUuid } from '@/core/validation';
import { getCurrentSubscription } from '../billing';
import { activeComp } from '../billing/plan';
import { getEntitlements, getMonitorUsage } from '../entitlements';
import { listOpenInvitations } from '../invitations';
import { listMembers } from '../members';
import { listAuditForStaff } from './audit';

const { organizations, memberships, users, sessions, incidents, monitors, impersonationSessions, staffUsers } = schema;

/*
 * Lesson 7.1 (🟢): the READ side of the admin panel: find a customer, see
 * their state. Reads are where generated admin screens shine; the point here
 * is that plan and usage come from the SAME entitlement code the product
 * uses (getEntitlements, getMonitorUsage), so support sees exactly the limits
 * the customer hits, not a second opinion computed differently.
 *
 * These read across orgs as the database owner: only staff reach them.
 */

export type CustomerHit = { id: string; name: string; slug: string; plan: string; members: number; matched: string };

/**
 * Find an org by (part of) its name or slug, (part of) a member's email, or
 * its Stripe customer id. Trigram indexes on users.email and
 * organizations.name (migration 0024) keep `ILIKE '%ana@%'` fast.
 */
export async function searchCustomers(query: string, limit = 20): Promise<CustomerHit[]> {
  const q = query.trim();
  if (q.length < 2) return [];
  const like = `%${q.replace(/[\\%_]/g, (c) => `\\${c}`)}%`;
  const matched = new Map<string, string>();

  if (/^cus_/.test(q)) {
    for (const o of await db.select({ id: organizations.id }).from(organizations).where(eq(organizations.stripeCustomerId, q)).limit(limit)) matched.set(o.id, 'Stripe customer');
  }
  if (isUuid(q)) {
    for (const o of await db.select({ id: organizations.id }).from(organizations).where(eq(organizations.id, q))) matched.set(o.id, 'org id');
  }
  const byName = await db
    .select({ id: organizations.id })
    .from(organizations)
    .where(or(ilike(organizations.name, like), ilike(organizations.slug, like)))
    .limit(limit);
  for (const o of byName) if (!matched.has(o.id)) matched.set(o.id, 'name');
  const byEmail = await db
    .select({ id: memberships.organizationId, email: users.email })
    .from(users)
    .innerJoin(memberships, eq(memberships.userId, users.id))
    .where(ilike(users.email, like))
    .limit(limit);
  for (const o of byEmail) if (!matched.has(o.id)) matched.set(o.id, `member ${o.email}`);

  const ids = [...matched.keys()].slice(0, limit);
  if (!ids.length) return [];
  const rows = await db
    .select({ id: organizations.id, name: organizations.name, slug: organizations.slug, plan: organizations.plan, members: count(memberships.userId) })
    .from(organizations)
    .leftJoin(memberships, eq(memberships.organizationId, organizations.id))
    .where(inArray(organizations.id, ids))
    .groupBy(organizations.id)
    .orderBy(asc(organizations.name));
  return rows.map((r) => ({ ...r, matched: matched.get(r.id)! }));
}

/** Everything the org page shows. Read-only; every write is a separate, audited action. */
export async function getCustomerOverview(orgId: string) {
  if (!isUuid(orgId)) return null;
  const [org] = await db.select().from(organizations).where(eq(organizations.id, orgId));
  if (!org) return null;
  const scope = { orgId };
  const [ent, usage, subscription, members, invitations, recentIncidents, audit, impersonations] = await Promise.all([
    getEntitlements(scope),
    getMonitorUsage(scope),
    getCurrentSubscription(scope),
    listMembersWithActivity(orgId),
    listOpenInvitations(scope),
    withOrg(orgId, (tx) =>
      tx
        .select({ id: incidents.id, cause: incidents.cause, openedAt: incidents.openedAt, resolvedAt: incidents.resolvedAt, monitorName: monitors.name })
        .from(incidents)
        .innerJoin(monitors, eq(monitors.id, incidents.monitorId))
        .where(eq(incidents.organizationId, orgId))
        .orderBy(desc(incidents.openedAt))
        .limit(10),
    ),
    listAuditForStaff({ orgId, limit: 15 }),
    db
      .select({ id: impersonationSessions.id, staffEmail: users.email, targetUserId: impersonationSessions.targetUserId, reason: impersonationSessions.reason, createdAt: impersonationSessions.createdAt, expiresAt: impersonationSessions.expiresAt, endedAt: impersonationSessions.endedAt })
      .from(impersonationSessions)
      .innerJoin(staffUsers, eq(staffUsers.id, impersonationSessions.staffUserId))
      .innerJoin(users, eq(users.id, staffUsers.userId))
      .where(eq(impersonationSessions.organizationId, orgId))
      .orderBy(desc(impersonationSessions.createdAt))
      .limit(5),
  ]);
  return { org, comp: activeComp(org) ? { plan: org.compPlan!, until: org.compPlanUntil } : null, ent, usage, subscription, members, invitations, recentIncidents, audit, impersonations };
}

export type CustomerOverview = NonNullable<Awaited<ReturnType<typeof getCustomerOverview>>>;

/** Members with what support asks first: verified? when were they last active? */
async function listMembersWithActivity(orgId: string) {
  const members = await listMembers({ orgId });
  if (!members.length) return [];
  const ids = members.map((m) => m.userId);
  const [verified, lastSeen] = await Promise.all([
    db.select({ id: users.id, emailVerified: users.emailVerified }).from(users).where(inArray(users.id, ids)),
    db
      .select({ userId: sessions.userId, at: max(sessions.updatedAt), n: count() })
      .from(sessions)
      .where(inArray(sessions.userId, ids))
      .groupBy(sessions.userId),
  ]);
  return members.map((m) => ({
    ...m,
    emailVerified: verified.find((v) => v.id === m.userId)?.emailVerified ?? false,
    lastActiveAt: lastSeen.find((s) => s.userId === m.userId)?.at ?? null,
    activeSessions: lastSeen.find((s) => s.userId === m.userId)?.n ?? 0,
  }));
}

/** Is this user a member of this org? (Every per-user support action checks it: the org page is the scope.) */
export async function findOrgMember(orgId: string, userId: string) {
  if (!isUuid(userId)) return null;
  const [row] = await db
    .select({ userId: users.id, name: users.name, email: users.email, emailVerified: users.emailVerified })
    .from(memberships)
    .innerJoin(users, eq(users.id, memberships.userId))
    .where(and(eq(memberships.organizationId, orgId), eq(memberships.userId, userId)));
  return row ?? null;
}

