import { apiRoute } from '@/lib/api';
import { AccessError, auditSourceFor } from '@/lib/access';
import { getCurrentUser } from '@/lib/session';
import { exportUserData, recordUserExport } from '@/lib/privacy/user-data';

/**
 * GET /api/account/export — lesson 8.1 (GDPR Art. 15 and 20): "download my
 * data", everything Beacon holds about the signed-in person, as one JSON file.
 * Beacon staff viewing an account (lesson 7.1) cannot download it.
 */
export const GET = apiRoute(async () => {
  const user = await getCurrentUser();
  if (!user) throw new AccessError('unauthenticated');
  if (user.impersonation) throw new AccessError('forbidden');
  const data = await exportUserData(user.id);
  if (!data) throw new AccessError('not_found');
  await recordUserExport(user.id, await auditSourceFor(user));
  return new Response(JSON.stringify(data, null, 2), {
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'content-disposition': `attachment; filename="beacon-my-data-${new Date().toISOString().slice(0, 10)}.json"`,
      'cache-control': 'no-store',
    },
  });
});
