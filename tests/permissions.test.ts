import { describe, expect, it } from 'vitest';
import { can, PERMISSIONS, type Permission } from '@/core/permissions';
import { ROLES } from '@/core/roles';

// Lesson 1.3: the role → permission map is the security policy, so pin it down.
// If you change the matrix on purpose, change this table with it.
const EXPECTED: Record<Permission, string[]> = {
  'monitor.read': ['owner', 'admin', 'member', 'viewer'],
  'monitor.write': ['owner', 'admin', 'member'],
  'incident.write': ['owner', 'admin', 'member'],
  'page.publish': ['owner', 'admin'],
  'member.manage': ['owner', 'admin'],
  'billing.manage': ['owner'],
  'org.delete': ['owner'],
};

describe('can(role, permission)', () => {
  for (const [permission, allowed] of Object.entries(EXPECTED) as [Permission, string[]][]) {
    it(`${permission}: only ${allowed.join(', ')}`, () => {
      const actual = ROLES.filter((role) => can(role, permission));
      expect(actual).toEqual(allowed);
    });
  }

  it('has no permission missing from the expected table', () => {
    const all = new Set(Object.values(PERMISSIONS).flat());
    expect([...all].sort()).toEqual(Object.keys(EXPECTED).sort());
  });

  it('gives every role at least what the role below it has', () => {
    for (let i = 1; i < ROLES.length; i++) {
      const lower = PERMISSIONS[ROLES[i]] as readonly string[];
      const higher = PERMISSIONS[ROLES[i - 1]] as readonly string[];
      expect(lower.every((p) => higher.includes(p))).toBe(true);
    }
  });
});
