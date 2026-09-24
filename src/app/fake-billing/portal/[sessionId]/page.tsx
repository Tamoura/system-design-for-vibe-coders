import { PLANS, planForPrice } from '@/core/plans';
import { fakeBilling } from '@/lib/billing/provider';
import { requireFakePortalSession } from '../../access';
import { changeSubscriptionAction } from '../../actions';

export const dynamic = 'force-dynamic';

/** A stand-in for Stripe's hosted Customer Portal (BILLING_PROVIDER=fake). */
export default async function FakePortalPage({ params }: { params: Promise<{ sessionId: string }> }) {
  const { sessionId } = await params;
  const { session, ctx } = await requireFakePortalSession(sessionId);
  const subs = await fakeBilling().listSubscriptions(session.customerId);
  return (
    <section className="grid" style={{ maxWidth: 560 }}>
      <div className="card muted">Fake Stripe Customer Portal, test mode.</div>
      <h1 style={{ margin: 0 }}>{ctx.orgName}: billing</h1>
      {subs.length === 0 && <div className="card muted">No subscriptions.</div>}
      {subs.map((s) => (
        <div key={s.id} className="card grid" data-testid="portal-subscription">
          <strong>Beacon {PLANS[planForPrice(s.priceId)].name}</strong>
          <div>
            Status: {s.status}
            {s.cancelAtPeriodEnd && ` · cancels on ${s.currentPeriodEnd?.toISOString().slice(0, 10)}`}
          </div>
          {s.status !== 'canceled' && (
            <div className="row">
              {s.cancelAtPeriodEnd ? (
                <form action={changeSubscriptionAction.bind(null, sessionId, s.id, 'resume')}>
                  <button className="btn secondary">Don’t cancel</button>
                </form>
              ) : (
                <form action={changeSubscriptionAction.bind(null, sessionId, s.id, 'cancel_at_period_end')}>
                  <button className="btn secondary">Cancel at period end</button>
                </form>
              )}
              <form action={changeSubscriptionAction.bind(null, sessionId, s.id, 'cancel_now')}>
                <button className="btn secondary">Cancel now</button>
              </form>
            </div>
          )}
        </div>
      ))}
      <a href={session.returnUrl}>Return to Beacon</a>
    </section>
  );
}
