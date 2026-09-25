import { PLANS, planForPrice } from '@/core/plans';
import { requireFakeCheckoutSession } from '../../access';
import { PayForm } from './pay-form';

export const dynamic = 'force-dynamic';

/** A stand-in for Stripe's hosted Checkout page (BILLING_PROVIDER=fake). */
export default async function FakeCheckoutPage({ params }: { params: Promise<{ sessionId: string }> }) {
  const { sessionId } = await params;
  const { session, ctx } = await requireFakeCheckoutSession(sessionId);
  const plan = PLANS[planForPrice(session.priceId)];
  return (
    <section className="grid" style={{ maxWidth: 460 }}>
      <div className="card muted">Fake Stripe Checkout, test mode. No real payment is made.</div>
      <h1 style={{ margin: 0 }}>Subscribe to Beacon {plan.name}</h1>
      <div className="card grid">
        <div>{ctx.orgName}</div>
        <strong>{plan.priceLabel}</strong>
        {session.status === 'complete' ? <div className="muted">This session is already paid.</div> : <PayForm sessionId={sessionId} />}
        <a href={session.cancelUrl}>Cancel and go back</a>
      </div>
    </section>
  );
}
