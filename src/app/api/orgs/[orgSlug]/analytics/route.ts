import { readConsent } from '@/core/consent';
import { isClientEvent } from '@/core/tracking-plan';
import { requireMembership } from '@/lib/access';
import { track, TrackingPlanError, validateEvent } from '@/lib/analytics';
import { apiRoute } from '@/lib/api';

type Params = { params: Promise<{ orgSlug: string }> };

/**
 * POST /api/orgs/:orgSlug/analytics  { event, properties }
 *
 * Lesson 6.2 (🟡): the browser's only way to record a product event. Guarded
 * like any other endpoint, and stricter than trackInTx():
 *   - a member of the org in the URL (the org is never taken from the body);
 *   - the user said yes (the consent cookie); otherwise 204 and nothing stored;
 *   - only events the tracking plan marks `source: 'client'`: the browser
 *     cannot fake `monitor_created` or `subscription_upgraded`;
 *   - exactly the plan's properties, and no PII (validateEvent).
 */
export const POST = apiRoute(async (req: Request, { params }: Params) => {
  const { orgSlug } = await params;
  const ctx = await requireMembership(orgSlug);
  if (readConsent(req.headers.get('cookie')) !== 'granted') return new Response(null, { status: 204 });
  const body = (await req.json()) as { event?: unknown; properties?: unknown };
  if (!isClientEvent(body.event)) return Response.json({ error: 'unknown_event', message: 'Not a client event in the tracking plan.' }, { status: 400 });
  const event = body.event;
  const properties = (body.properties ?? {}) as Parameters<typeof validateEvent<typeof event>>[1];
  try {
    validateEvent(event, properties);
  } catch (err) {
    if (err instanceof TrackingPlanError) return Response.json({ error: 'invalid_properties', message: err.message }, { status: 400 });
    throw err;
  }
  await track({ orgId: ctx.orgId, userId: ctx.userId }, event, properties);
  return Response.json({ recorded: true }, { status: 202 });
});
