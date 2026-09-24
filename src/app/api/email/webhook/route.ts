import { handleEmailEvent, verifyWebhookSignature } from '@/lib/email/webhook';

/**
 * POST /api/email/webhook — lesson 4.1 (🟡): bounce and complaint events from
 * the email provider (Resend → Webhooks, signing secret in EMAIL_WEBHOOK_SECRET).
 *
 * 400 for anything unsigned, forged or stale; 200 for everything verified,
 * including events we ignore, so the provider does not retry them.
 */
export async function POST(req: Request) {
  const secret = process.env.EMAIL_WEBHOOK_SECRET;
  if (!secret) return Response.json({ error: 'webhook_not_configured' }, { status: 503 });
  const body = await req.text(); // the RAW body: the signature covers these exact bytes
  const ok = verifyWebhookSignature(body, {
    id: req.headers.get('svix-id'),
    timestamp: req.headers.get('svix-timestamp'),
    signature: req.headers.get('svix-signature'),
  }, secret);
  if (!ok) return Response.json({ error: 'invalid_signature' }, { status: 400 });
  let event: unknown;
  try {
    event = JSON.parse(body);
  } catch {
    return Response.json({ error: 'invalid_json' }, { status: 400 });
  }
  const { suppressed } = await handleEmailEvent(event as Parameters<typeof handleEmailEvent>[0]);
  return Response.json({ received: true, suppressed: suppressed.length });
}
