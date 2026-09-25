import Link from 'next/link';
import { ESCALATION_CHANNELS, MAX_TIERS } from '@/core/escalation';
import { CHANNEL_LABELS } from '@/core/notifications';
import { forPage, requirePermission } from '@/lib/access';
import { listMembers } from '@/lib/members';
import { getEscalationPolicy } from '@/lib/workflows';
import { saveEscalationAction } from './actions';

export const dynamic = 'force-dynamic';

/**
 * Lesson 5.4 (🟡): the escalation policy form. "A well-designed form over a
 * fixed shape covers most needs": up to three tiers of people, channels and a
 * wait. The workflow that interprets it is src/lib/workflows/escalation.ts.
 */
export default async function EscalationPage({ params, searchParams }: { params: Promise<{ orgSlug: string }>; searchParams: Promise<{ saved?: string; error?: string }> }) {
  const { orgSlug } = await params;
  const { saved, error } = await searchParams;
  const ctx = await forPage(requirePermission(orgSlug, 'notification.manage'), `/${orgSlug}/settings/escalation`);
  const [policy, members] = await Promise.all([getEscalationPolicy(ctx), listMembers(ctx)]);
  return (
    <section className="grid" style={{ maxWidth: 760 }}>
      <div className="row">
        <h1 style={{ margin: 0 }}>Escalation policy</h1>
      </div>
      <p className="muted" style={{ margin: 0 }}>
        When an incident opens, Beacon pages tier 1, waits, then tier 2, and so on, until someone clicks <strong>Acknowledge</strong> or the
        incident resolves. Changes apply to the next incident; an escalation that is already running keeps the policy it started with.
      </p>
      <form action={saveEscalationAction.bind(null, ctx.orgSlug)} className="grid">
        {Array.from({ length: MAX_TIERS }, (_, i) => {
          const tier = policy.tiers[i];
          return (
            <fieldset key={i} className="card grid" data-testid={`tier-${i + 1}`}>
              <legend><strong>Tier {i + 1}</strong>{i > 0 && <span className="muted"> (optional)</span>}</legend>
              <div className="row" style={{ flexWrap: 'wrap' }}>
                {members.map((m) => (
                  <label key={m.userId} className="row" style={{ gap: '.3rem' }}>
                    <input type="checkbox" name={`tier${i}.users`} value={m.userId} defaultChecked={tier?.userIds.includes(m.userId)} /> {m.name}
                  </label>
                ))}
              </div>
              <div className="row">
                {ESCALATION_CHANNELS.map((c) => (
                  <label key={c} className="row" style={{ gap: '.3rem' }}>
                    <input type="checkbox" name={`tier${i}.channels`} value={c} defaultChecked={tier ? tier.channels.includes(c) : c !== 'sms'} /> {CHANNEL_LABELS[c]}
                  </label>
                ))}
                <label className="row" style={{ gap: '.3rem' }}>
                  then wait <input name={`tier${i}.wait`} type="number" min={1} max={1440} defaultValue={tier?.waitMinutes ?? 5} style={{ width: '5rem' }} /> minutes
                </label>
              </div>
            </fieldset>
          );
        })}
        <div className="row">
          <button className="btn">Save policy</button>
          {saved && <span className="muted">Saved. It applies from the next incident.</span>}
          {error && <span className="error">{error}</span>}
        </div>
      </form>
    </section>
  );
}
