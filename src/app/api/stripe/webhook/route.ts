import { handleStripeWebhook } from '@/lib/billing/webhook';
import { observed } from '@/lib/observability/http';

/**
 * POST /api/stripe/webhook — lesson 3.1 (🟡).
 *
 * No session and no org in the URL: Stripe calls it, and the signature is the
 * authentication. Read the body as TEXT: the signature covers the exact
 * bytes, and req.json() would parse them away. The work is in
 * src/lib/billing/webhook.ts.
 *
 * Locally: `stripe listen --forward-to localhost:3000/api/stripe/webhook`.
 * Lesson 7.2: observed() logs it and reports a failed sync (then a 500, so Stripe retries).
 */
export const POST = observed(async (req: Request): Promise<Response> => {
  const rawBody = await req.text(); // raw body, never req.json()
  const { status, body } = await handleStripeWebhook(rawBody, req.headers.get('stripe-signature'));
  return new Response(body, { status, headers: { 'content-type': 'text/plain' } });
});
