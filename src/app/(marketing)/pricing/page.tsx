import type { Metadata } from 'next';
import Link from 'next/link';
import { PLAN_IDS, PLANS, SMS_OVERAGE_CENTS, type Entitlements } from '@/core/plans';
import { intervalLabel } from '@/core/validation';

export const metadata: Metadata = { title: 'Pricing — Beacon' };
// Lesson 6.1: static, like the rest of the marketing site.
export const dynamic = 'error';

/**
 * Lesson 6.1 + 3.2: the pricing page is DRAWN FROM src/core/plans.ts, the
 * same config the server enforces. Change a limit there and the page, the
 * upgrade prompts and the enforcement change together; the marketing copy
 * cannot promise 10 monitors while the API allows 5.
 */
function features(e: Entitlements): string[] {
  return [
    `${e.maxMonitors} monitors`,
    `Checks as often as every ${intervalLabel(e.minIntervalSec)}`,
    e.smsCreditsPerMonth ? `${e.smsCreditsPerMonth} SMS alerts a month` : 'Email, Slack and in-app alerts',
    'Public status page',
    ...(e.api ? [`Public API (${e.apiRequestsPerMinute} requests/minute) and webhooks`] : []),
    ...(e.sso ? ['Single sign-on (SSO)'] : []),
    ...(e.auditLog ? [`Audit log (${e.auditLogRetentionDays === 365 ? 'a year' : `${e.auditLogRetentionDays} days`} of history, CSV export)`] : []),
  ];
}

export default function PricingPage() {
  return (
    <div className="grid" style={{ gap: '1.5rem' }}>
      <h1 style={{ margin: 0 }}>Pricing</h1>
      <p className="lead" style={{ margin: 0 }}>Start free. Upgrade when you need more monitors or faster checks.</p>
      <div className="pricing" data-testid="pricing">
        {PLAN_IDS.map((id) => {
          const plan = PLANS[id];
          return (
            <section key={id} className={`card grid price-card${id === 'pro' ? ' featured' : ''}`} aria-labelledby={`plan-${id}`} data-plan={id}>
              <h2 id={`plan-${id}`} style={{ margin: 0 }}>{plan.name}</h2>
              <div className="price">{plan.priceLabel}</div>
              <p className="muted" style={{ margin: 0 }}>{plan.pitch}</p>
              <ul>
                {features(plan.entitlements).map((f) => (
                  <li key={f}>{f}</li>
                ))}
              </ul>
              {/* Every plan starts with sign-up; paid plans are chosen in Billing (lesson 3.1). */}
              <Link className={id === 'free' ? 'btn secondary' : 'btn'} href="/signup">
                {id === 'free' ? 'Start free' : `Start free, then upgrade to ${plan.name}`}
              </Link>
            </section>
          );
        })}
      </div>
      <p className="muted">{`Prices in USD, billed monthly through Stripe. SMS beyond the included credits cost $${(SMS_OVERAGE_CENTS / 100).toFixed(2)} each.`}</p>
    </div>
  );
}
