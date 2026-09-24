import { describe, expect, it } from 'vitest';
import { can, canEditMonitor, canGrantRole, PERMISSIONS, roleChangeRefusal, type Permission } from '@/core/permissions';
import { ROLES } from '@/core/roles';

// Lesson 1.3: the role → permission map is the security policy, so pin it down.
// If you change the matrix on purpose, change this table with it.
const EXPECTED: Record<Permission, string[]> = {
  'monitor.read': ['owner', 'admin', 'member', 'viewer'],
  'member.read': ['owner', 'admin', 'member', 'viewer'],
  'monitor.write': ['owner', 'admin', 'member'],
  'monitor.write_any': ['owner', 'admin'],
  'incident.write': ['owner', 'admin', 'member'],
  'page.publish': ['owner', 'admin'],
  'member.manage': ['owner', 'admin'],
  'billing.read': ['owner', 'admin'], // lesson 3.1: plan and usage
  'billing.manage': ['owner'],
  'notification.manage': ['owner', 'admin'],
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

describe('canEditMonitor (ABAC: members edit only their own monitors)', () => {
  const mine = { createdBy: 'u1' };
  const theirs = { createdBy: 'u2' };
  it('lets members edit what they created, and nothing else', () => {
    expect(canEditMonitor({ userId: 'u1', role: 'member' }, mine)).toBe(true);
    expect(canEditMonitor({ userId: 'u1', role: 'member' }, theirs)).toBe(false);
  });
  it('lets owners and admins edit any monitor, including authorless ones', () => {
    expect(canEditMonitor({ userId: 'u1', role: 'admin' }, theirs)).toBe(true);
    expect(canEditMonitor({ userId: 'u1', role: 'owner' }, { createdBy: null })).toBe(true);
  });
  it('never lets viewers edit, even a monitor recorded as theirs', () => {
    expect(canEditMonitor({ userId: 'u1', role: 'viewer' }, mine)).toBe(false);
  });
});

describe('role changes', () => {
  const owner = { userId: 'o', role: 'owner' as const };
  const admin = { userId: 'a', role: 'admin' as const };
  const member = { userId: 'm', role: 'member' as const };
  const viewer = { userId: 'v', role: 'viewer' as const };

  it('nobody can change their own role', () => {
    expect(roleChangeRefusal(owner, owner, 'admin')).toMatch(/own role/);
    expect(roleChangeRefusal(admin, admin, 'viewer')).toMatch(/own role/);
  });
  it('an admin cannot promote anyone to owner, or touch an owner', () => {
    expect(roleChangeRefusal(admin, member, 'owner')).not.toBeNull();
    expect(roleChangeRefusal(admin, owner, 'viewer')).not.toBeNull();
  });
  it('an admin can move people at or below admin', () => {
    expect(roleChangeRefusal(admin, viewer, 'admin')).toBeNull();
    expect(roleChangeRefusal(admin, { userId: 'a2', role: 'admin' }, 'member')).toBeNull();
  });
  it('an owner can make another owner', () => expect(roleChangeRefusal(owner, admin, 'owner')).toBeNull());
  it('members and viewers cannot change roles', () => {
    expect(roleChangeRefusal(member, viewer, 'member')).not.toBeNull();
    expect(roleChangeRefusal(viewer, member, 'viewer')).not.toBeNull();
  });
  it('invitations follow the same ceiling', () => {
    expect(canGrantRole('admin', 'owner')).toBe(false);
    expect(canGrantRole('admin', 'admin')).toBe(true);
    expect(canGrantRole('member', 'viewer')).toBe(false);
  });
});
