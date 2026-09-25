import { ROLES, type Role } from './roles';

/*
 * Lesson 1.3: the ONE place that says what each role may do.
 *
 * Code everywhere else asks `can(role, 'monitor.write')`, never
 * `role === 'admin'`. Adding a role, or letting members publish status pages,
 * is then a one-line change here instead of a grep-and-pray exercise.
 *
 * This is the lesson's matrix:
 *
 * | Permission                                  | Owner | Admin | Member | Viewer |
 * |---------------------------------------------|-------|-------|--------|--------|
 * | monitor.read    view monitors, incidents    |   ✓   |   ✓   |   ✓    |   ✓    |
 * | member.read     see who is in the org       |   ✓   |   ✓   |   ✓    |   ✓    |
 * | monitor.write   create monitors, edit and   |   ✓   |   ✓   |   ✓    |        |
 * |                 delete their own            |       |       |        |        |
 * | monitor.write_any  edit/delete anyone's     |   ✓   |   ✓   |        |        |
 * | incident.write  update incidents            |   ✓   |   ✓   |   ✓    |        |
 * | page.publish    publish the status page     |   ✓   |   ✓   |        |        |
 * | org.manage      rename the org (lesson 6.1) |   ✓   |   ✓   |        |        |
 * | member.manage   invite, change roles        |   ✓   |   ✓   |        |        |
 * | billing.read    see the plan and usage      |   ✓   |   ✓   |        |        |
 * | notification.manage  org alert policy,     |   ✓   |   ✓   |        |        |
 * |                 Slack channel (lesson 4.2)  |       |       |        |        |
 * | integration.manage  API keys and webhook    |   ✓   |   ✓   |        |        |
 * |                 endpoints (lessons 5.2/5.3) |       |       |        |        |
 * | billing.manage  upgrade, manage billing     |   ✓   |       |        |        |
 * | org.delete      (1.2's 🔴 exercise)         |   ✓   |       |        |        |
 */
export const PERMISSIONS = {
  owner: [
    'monitor.read', 'member.read', 'monitor.write', 'monitor.write_any', 'incident.write',
    'page.publish', 'org.manage', 'member.manage', 'billing.read', 'billing.manage', 'notification.manage', 'integration.manage', 'org.delete',
  ],
  admin: [
    'monitor.read', 'member.read', 'monitor.write', 'monitor.write_any', 'incident.write',
    'page.publish', 'org.manage', 'member.manage', 'billing.read', 'notification.manage', 'integration.manage',
  ],
  member: ['monitor.read', 'member.read', 'monitor.write', 'incident.write'],
  viewer: ['monitor.read', 'member.read'],
} as const satisfies Record<Role, readonly string[]>;

export type Permission = (typeof PERMISSIONS)[Role][number];

/** Function-level check: may this role perform this action at all? */
export function can(role: Role, permission: Permission): boolean {
  return (PERMISSIONS[role] as readonly string[]).includes(permission);
}

/** How powerful a role is: owner 3 … viewer 0. Used only to compare roles. */
export function roleRank(role: Role): number {
  return ROLES.length - 1 - ROLES.indexOf(role);
}

/**
 * Lesson 1.2/1.3: may this role invite someone as `role`? Only with
 * "member.manage", and never above your own role — an admin cannot mint owners.
 */
export function canGrantRole(actorRole: Role, role: Role): boolean {
  return can(actorRole, 'member.manage') && roleRank(role) <= roleRank(actorRole);
}

/** Who is acting: enough to evaluate the rules below. */
export type Actor = { userId: string; role: Role };

/**
 * Lesson 1.3 (🟡), one ABAC rule: members may edit only the monitors they
 * created; owners and admins ("monitor.write_any") may edit any. Monitors
 * with no recorded author (created before Module 1) need "monitor.write_any".
 */
export function canEditMonitor(actor: Actor, monitor: { createdBy: string | null }): boolean {
  if (can(actor.role, 'monitor.write_any')) return true;
  return can(actor.role, 'monitor.write') && monitor.createdBy === actor.userId;
}

/**
 * Lesson 1.3 (🟡): role changes. Returns null when allowed, or the reason.
 *  - you need "member.manage";
 *  - you never change your own role (so the last owner cannot demote themselves);
 *  - you only touch people at or below your level, and only grant roles at or
 *    below your own: an admin can neither demote an owner nor create one.
 */
export function roleChangeRefusal(actor: Actor, target: Actor, newRole: Role): string | null {
  if (!can(actor.role, 'member.manage')) return 'You cannot change roles in this organization.';
  if (actor.userId === target.userId) return 'You cannot change your own role.';
  if (roleRank(target.role) > roleRank(actor.role)) return `As ${actor.role} you cannot change the role of an ${target.role}.`;
  if (roleRank(newRole) > roleRank(actor.role)) return `As ${actor.role} you cannot make someone ${newRole}.`;
  return null;
}
