import { observed } from '@/lib/observability/http';
import { checkReadiness } from '@/lib/health';

/*
 * Lesson 7.4: READINESS. "Can this instance serve traffic right now?" A
 * rolling deploy sends traffic to a new instance only once this answers 200,
 * and takes an instance out of rotation (without restarting it) while it
 * answers 503: the database is unreachable, or the job queue's schema is
 * missing (migrations did not run: the release step failed).
 */
export const dynamic = 'force-dynamic';

export const GET = observed(async () => {
  const result = await checkReadiness();
  return Response.json(result, { status: result.status === 'ready' ? 200 : 503, headers: { 'cache-control': 'no-store' } });
});
