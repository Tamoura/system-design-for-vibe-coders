import type { Role } from './roles';

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
 * | monitor.write   create and edit monitors    |   ✓   |   ✓   |   ✓    |        |
 * | incident.write  update incidents            |   ✓   |   ✓   |   ✓    |        |
 * | page.publish    publish the status page     |   ✓   |   ✓   |        |        |
 * | member.manage   invite, change roles        |   ✓   |   ✓   |        |        |
 * | billing.manage  (used from lesson 3.1)      |   ✓   |       |        |        |
 * | org.delete      (1.2's 🔴 exercise)         |   ✓   |       |        |        |
 */
export const PERMISSIONS = {
  owner: ['monitor.read', 'monitor.write', 'incident.write', 'page.publish', 'member.manage', 'billing.manage', 'org.delete'],
  admin: ['monitor.read', 'monitor.write', 'incident.write', 'page.publish', 'member.manage'],
  member: ['monitor.read', 'monitor.write', 'incident.write'],
  viewer: ['monitor.read'],
} as const satisfies Record<Role, readonly string[]>;

export type Permission = (typeof PERMISSIONS)[Role][number];

/** Function-level check: may this role perform this action at all? */
export function can(role: Role, permission: Permission): boolean {
  return (PERMISSIONS[role] as readonly string[]).includes(permission);
}
