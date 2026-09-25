import { z } from 'zod';
import { PAID_PLANS } from './plans';

/*
 * Lesson 7.1: Beacon's STAFF, a second population of users with its own
 * roles. Staff are not customers with a flag: a staff role lives in its own
 * table (staff_users) and is checked by its own function (staffCan), so a bug
 * in the customer permission code (src/core/permissions.ts) can never open
 * the back office, and no customer role ("owner", "admin") means anything here.
 *
 * The lesson's starting set of roles:
 *
 * | Staff permission        | Support | Billing | Engineer | Superadmin |
 * |-------------------------|---------|---------|----------|------------|
 * | customers.read          |    ✓    |    ✓    |    ✓     |     ✓      |
 * | trial.extend (≤ 14 d)   |    ✓    |    ✓    |          |     ✓      |
 * | email.resend            |    ✓    |         |          |     ✓      |
 * | sessions.revoke         |    ✓    |         |          |     ✓      |
 * | impersonate (read-only) |    ✓    |         |    ✓     |     ✓      |
 * | plan.comp               |         |    ✓    |          |     ✓      |
 * | flags.manage            |         |         |    ✓     |     ✓      |
 * | audit.read (platform)   |         |         |    ✓     |     ✓      |
 * | staff.manage            |         |         |          |     ✓      |
 */
export const STAFF_ROLES = ['support', 'billing', 'engineer', 'superadmin'] as const;
export type StaffRole = (typeof STAFF_ROLES)[number];

export const STAFF_PERMISSIONS = {
  support: ['customers.read', 'trial.extend', 'email.resend', 'sessions.revoke', 'impersonate', 'analytics.read'],
  billing: ['customers.read', 'trial.extend', 'plan.comp', 'analytics.read'],
  engineer: ['customers.read', 'impersonate', 'flags.manage', 'audit.read', 'analytics.read'],
  superadmin: [
    'customers.read', 'trial.extend', 'email.resend', 'sessions.revoke', 'impersonate', 'plan.comp',
    'flags.manage', 'audit.read', 'analytics.read', 'staff.manage',
  ],
} as const satisfies Record<StaffRole, readonly string[]>;

export type StaffPermission = (typeof STAFF_PERMISSIONS)[StaffRole][number];

export function isStaffRole(value: unknown): value is StaffRole {
  return typeof value === 'string' && (STAFF_ROLES as readonly string[]).includes(value);
}

export function staffCan(role: StaffRole, permission: StaffPermission): boolean {
  return (STAFF_PERMISSIONS[role] as readonly string[]).includes(permission);
}

/** Lesson 7.1 (🟡): support may extend a trial by at most two weeks at a time. */
export const MAX_TRIAL_EXTENSION_DAYS = 14;

/** Lesson 7.1: an impersonation session dies after 30 minutes, active or not. No "remember me". */
export const IMPERSONATION_TTL_MS = 30 * 60 * 1000;

/**
 * "No reason field" is one of the lesson's junior mistakes: six months later
 * nobody knows why org 4411 has free Business. Every staff write takes one:
 * a sentence or a ticket link.
 */
const REASON_REQUIRED = 'Give a reason (a sentence or a ticket link, at least 8 characters)';
export const reasonInput = z.string({ error: REASON_REQUIRED }).trim().min(8, REASON_REQUIRED).max(500);

export const extendTrialInput = z.object({
  days: z.coerce.number().int().min(1, 'At least 1 day').max(MAX_TRIAL_EXTENSION_DAYS, `At most ${MAX_TRIAL_EXTENSION_DAYS} days at a time`),
  reason: reasonInput,
});

export const compPlanInput = z.object({
  plan: z.enum(PAID_PLANS),
  // Empty = until someone removes it. Otherwise a number of months.
  months: z.preprocess((v) => (v === '' || v === null || v === undefined ? undefined : v), z.coerce.number().int().min(1).max(24).optional()),
  reason: reasonInput,
});

export const reasonOnlyInput = z.object({ reason: reasonInput });

export const impersonateInput = z.object({ userId: z.string().uuid('Pick a member'), reason: reasonInput });

export const grantStaffInput = z.object({ email: z.string().trim().toLowerCase().email(), role: z.enum(STAFF_ROLES), reason: reasonInput });

/**
 * Lesson 7.1: HTTP methods an impersonation session may use. Everything else
 * (POST, PUT, PATCH, DELETE, and so server actions) is refused while the
 * impersonation cookie is present, except the few paths below.
 */
export const SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS'] as const;

/** Paths a read-only impersonation may still POST to: leaving it, signing out, and the staff area (which acts as the staff member, not the customer). */
export function impersonationMayPost(pathname: string): boolean {
  return (
    pathname === '/api/impersonation/exit' ||
    pathname === '/api/auth/sign-out' ||
    pathname.startsWith('/api/internal/') ||
    pathname === '/internal' ||
    pathname.startsWith('/internal/')
  );
}

export const IMPERSONATION_COOKIE = 'beacon_impersonation';
