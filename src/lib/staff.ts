import { cache } from 'react';
import { headers } from 'next/headers';
import { forbidden, notFound } from 'next/navigation';
import { eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import type { AuditSource } from '@/core/audit';
import { staffCan, type StaffPermission, type StaffRole } from '@/core/staff';
import { clientIpFrom, requestIdFrom } from './observability/context';
import { getSessionUser, type CurrentUser } from './session';

const { staffUsers, users } = schema;

/*
 * Lesson 7.1: who is Beacon staff, and what may they do.
 *
 * Module 6's stopgap (BEACON_STAFF_EMAILS) is gone. A staff member is a
 * Beacon account (with a VERIFIED email) that has a row in `staff_users`,
 * with one staff role (src/core/staff.ts). The staff area:
 *
 *  - uses the REAL signed-in person (getSessionUser), never the customer a
 *    staff member is impersonating;
 *  - answers 404 to everyone who is not staff, on every page and route, so
 *    the back office does not even admit it exists (like a foreign org, 1.2);
 *  - answers 403 to staff whose ROLE lacks the permission (support cannot
 *    comp a plan: no button, and a direct POST is refused).
 *
 * Production, per the lesson: staff sign in through the company's identity
 * provider with phishing-resistant MFA, on a separate hostname
 * (admin.beacon.internal) behind an identity-aware proxy. Beacon keeps one
 * app and one login for the course; docs/SOLUTIONS.md says where each of
 * those controls would go.
 */
export type StaffMember = { staffId: string; userId: string; email: string; name: string; role: StaffRole };

/** The staff row behind a user, if any. Unverified emails never count. */
export async function findStaffMember(user: Pick<CurrentUser, 'id' | 'emailVerified'> | null): Promise<StaffMember | null> {
  if (!user?.emailVerified) return null;
  const [row] = await db
    .select({ staffId: staffUsers.id, userId: users.id, email: users.email, name: users.name, role: staffUsers.role })
    .from(staffUsers)
    .innerJoin(users, eq(users.id, staffUsers.userId))
    .where(eq(staffUsers.userId, user.id));
  return row ?? null;
}

export const getStaffMember = cache(async (): Promise<StaffMember | null> => findStaffMember(await getSessionUser()));

/**
 * For /internal pages and their server actions: the staff member, or a 404
 * page. With a permission: a 403 page for staff whose role lacks it.
 */
export async function requireStaff(permission?: StaffPermission): Promise<StaffMember> {
  const staff = await getStaffMember();
  if (!staff) notFound();
  if (permission && !staffCan(staff.role, permission)) forbidden();
  return staff;
}

/** Who the audit log names for a staff action, and from where. */
export function staffAuditSource(staff: StaffMember, requestHeaders: Headers): AuditSource {
  return {
    actor: { type: 'staff', id: staff.staffId, name: staff.name, email: staff.email },
    ip: clientIpFrom(requestHeaders),
    userAgent: requestHeaders.get('user-agent'),
    requestId: requestIdFrom(requestHeaders.get('x-request-id')),
    via: 'admin',
  };
}

export async function staffAuditSourceFromRequest(staff: StaffMember): Promise<AuditSource> {
  return staffAuditSource(staff, await headers());
}
