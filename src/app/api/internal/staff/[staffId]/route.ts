import { reasonOnlyInput } from '@/core/staff';
import { revokeStaff } from '@/lib/admin/staff';
import { staffRoute } from '@/lib/admin/route';

/** Lesson 7.1: POST /api/internal/staff/:staffId { reason }: remove a staff member. Superadmins only. */
export const POST = staffRoute<{ staffId: string }>('staff.manage', async (_req, { input, params, source, staff }) => {
  const { reason } = reasonOnlyInput.parse(input);
  await revokeStaff(params.staffId, reason, source, staff.staffId);
  return { back: '/internal/staff', message: 'Staff member removed.' };
});
