import { observed } from '@/lib/observability/http';

/*
 * Lesson 7.2 / 7.4: LIVENESS. "Is this process alive and able to answer?"
 * Nothing else: no database, no queue. A load balancer or Kubernetes restarts
 * an instance that stops answering here; if this checked Postgres, a database
 * blip would restart every web instance at once and make things worse.
 * Beacon also monitors ITSELF through this URL (the seed's "Beacon itself"
 * monitor, lesson 7.2's dogfooding), next to an outside probe.
 */
export const dynamic = 'force-dynamic';

export const GET = observed(async () =>
  Response.json({ status: 'ok', release: process.env.APP_RELEASE ?? 'dev', uptimeSeconds: Math.round(process.uptime()) }, { headers: { 'cache-control': 'no-store' } }),
);
