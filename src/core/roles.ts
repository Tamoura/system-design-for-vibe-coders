/**
 * Lesson 1.2: a membership links a user to an organization and carries one of
 * these roles. Ordered from most to least powerful. What each role may *do* is
 * decided in one place, src/core/permissions.ts (lesson 1.3).
 */
export const ROLES = ['owner', 'admin', 'member', 'viewer'] as const;
export type Role = (typeof ROLES)[number];

export function isRole(value: unknown): value is Role {
  return typeof value === 'string' && (ROLES as readonly string[]).includes(value);
}
