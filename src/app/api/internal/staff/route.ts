import { grantStaffInput } from '@/core/staff';
import { grantStaffRole } from '@/lib/admin/staff';
import { staffRoute } from '@/lib/admin/route';

/**
 * Lesson 7.1: POST /api/internal/staff { email, role, reason }: grant or
 * change a staff role. Superadmins only ("staff.manage"); a platform audit event.
 */
export const POST = staffRoute('staff.manage', async (_req, { input, source, staff }) => {
  const { email, role, reason } = grantStaffInput.parse(input);
  await grantStaffRole({ email, role, reason }, source, staff.staffId);
  return { back: '/internal/staff', message: `${email} is now ${role}.` };
});
