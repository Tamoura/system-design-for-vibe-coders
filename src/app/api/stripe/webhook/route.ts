import { handleStripeWebhook } from '@/lib/billing/webhook';

/**
 * POST /api/stripe/webhook — lesson 3.1 (🟡).
 *
 * No session and no org in the URL: Stripe calls it, and the signature is the
 * authentication. Read the body as TEXT: the signature covers the exact
 * bytes, and req.json() would parse them away. The work is in
 * src/lib/billing/webhook.ts.
 *
 * Locally: `stripe listen --forward-to localhost:3000/api/stripe/webhook`.
 */
export async function POST(req: Request): Promise<Response> {
  const rawBody = await req.text(); // raw body, never req.json()
  const { status, body } = await handleStripeWebhook(rawBody, req.headers.get('stripe-signature'));
  return new Response(body, { status, headers: { 'content-type': 'text/plain' } });
}
