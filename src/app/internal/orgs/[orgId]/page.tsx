import Link from 'next/link';
import { notFound } from 'next/navigation';
import { AUDIT_ACTIONS, isAuditAction } from '@/core/audit';
import { PAID_PLANS, PLANS } from '@/core/plans';
import { MAX_TRIAL_EXTENSION_DAYS, staffCan } from '@/core/staff';
import { getCustomerOverview } from '@/lib/admin/customers';
import { requireStaff } from '@/lib/staff';

export const dynamic = 'force-dynamic';

const fmt = (d: Date | null | undefined) => (d ? d.toISOString().replace('T', ' ').slice(0, 16) + ' UTC' : '—');

/** Every staff write needs a reason (lesson 7.1): "why does org 4411 have free Business?" */
function Reason({ id }: { id: string }) {
  return (
    <label htmlFor={id} className="grid" style={{ gap: '.2rem' }}>
      <span className="muted">Reason or ticket link (required, recorded in the audit log)</span>
      <input id={id} name="reason" required minLength={8} maxLength={500} placeholder="e.g. TICKET-1234: owner is travelling, outage in progress" />
    </label>
  );
}

/**
 * Lesson 7.1: one customer, read-only, with the few write actions next to
 * the facts they change. Plan and usage come from the product's own
 * entitlement code. Buttons appear only for staff roles that may use them;
 * the routes behind them check again (a support engineer's POST to
 * comp-plan is a 403 whether or not the button is shown).
 */
export default async function CustomerPage({ params, searchParams }: { params: Promise<{ orgId: string }>; searchParams: Promise<{ done?: string; error?: string }> }) {
  const staff = await requireStaff('customers.read');
  const { orgId } = await params;
  const flash = await searchParams;
  const o = await getCustomerOverview(orgId);
  if (!o) notFound();
  const may = (p: Parameters<typeof staffCan>[1]) => staffCan(staff.role, p);
  const action = (name: string) => `/api/internal/orgs/${o.org.id}/${name}`;
  const back = `/internal/orgs/${o.org.id}`;
  const trialing = o.subscription?.status === 'trialing';

  return (
    <section className="grid" data-testid="customer-page">
      {flash.done && <p className="card" role="status" data-testid="flash-done">✓ {flash.done}</p>}
      {flash.error && <p className="card error" role="alert" data-testid="flash-error">{flash.error}</p>}

      <div className="row">
        <h1 style={{ margin: 0 }}>{o.org.name}</h1>
        <span className="badge" data-testid="org-plan">{PLANS[o.ent.plan].name}</span>
        {o.comp && <span className="badge">comped: {PLANS[o.comp.plan].name} until {o.comp.until ? fmt(o.comp.until) : 'removed'}</span>}
      </div>
      <p className="muted" style={{ margin: 0 }}>
        /{o.org.slug} · id <code>{o.org.id}</code> · Stripe customer <code>{o.org.stripeCustomerId ?? 'none'}</code> · created {fmt(o.org.createdAt)}
      </p>

      <div className="card grid" data-testid="usage">
        <h2>Plan and usage</h2>
        <div>
          Monitors: <strong data-testid="monitor-usage">{o.usage.total} of {o.ent.maxMonitors}</strong> ({o.usage.running} running, {o.usage.frozen} frozen by the plan)
          {o.usage.atLimit && <span className="badge status-down" style={{ marginLeft: '.5rem' }}>at the limit</span>}
        </div>
        <div className="muted">
          Checks at most every {o.ent.minIntervalSec} s · SMS {o.ent.smsCreditsPerMonth}/month · API {o.ent.api ? 'yes' : 'no'} · audit log{' '}
          {o.ent.auditLog ? `${o.ent.auditLogRetentionDays} days` : 'no'}
        </div>
        <div>
          Subscription:{' '}
          {o.subscription ? (
            <span data-testid="subscription">
              <code>{o.subscription.id}</code> {o.subscription.status}
              {o.subscription.trialEnd && <> · trial ends <strong data-testid="trial-end">{fmt(o.subscription.trialEnd)}</strong></>}
              {' '}· period ends {fmt(o.subscription.currentPeriodEnd)}
            </span>
          ) : (
            'none'
          )}
        </div>
      </div>

      {(may('trial.extend') || may('plan.comp') || may('impersonate')) && (
        <div className="card grid" data-testid="support-actions">
          <h2>Support actions</h2>
          {may('trial.extend') && (
            <form method="post" action={action('extend-trial')} className="grid" data-testid="extend-trial-form">
              <input type="hidden" name="back" value={back} />
              <strong>Extend trial</strong>
              {!trialing && <span className="muted">No subscription is in a trial right now: the action will say so.</span>}
              <label className="row">
                Days <input name="days" type="number" min={1} max={MAX_TRIAL_EXTENSION_DAYS} defaultValue={2} required style={{ width: '5rem' }} />
                <span className="muted">(1–{MAX_TRIAL_EXTENSION_DAYS}; changes Stripe, then our copy)</span>
              </label>
              <Reason id="trial-reason" />
              <div><button className="btn">Extend trial</button></div>
            </form>
          )}
          {may('plan.comp') && (
            <form method="post" action={action('comp-plan')} className="grid" data-testid="comp-plan-form">
              <input type="hidden" name="back" value={back} />
              <strong>Comp plan</strong>
              <label className="row">
                Plan
                <select name="plan" defaultValue="pro">
                  {PAID_PLANS.map((p) => <option key={p} value={p}>{PLANS[p].name}</option>)}
                </select>
                for <input name="months" type="number" min={1} max={24} placeholder="∞" style={{ width: '5rem' }} /> months
              </label>
              <Reason id="comp-reason" />
              <div><button className="btn">Comp plan</button></div>
            </form>
          )}
          {may('plan.comp') && o.comp && (
            <form method="post" action={action('remove-comp')} className="grid">
              <input type="hidden" name="back" value={back} />
              <strong>Remove the complimentary plan</strong>
              <Reason id="uncomp-reason" />
              <div><button className="btn secondary">Remove comp</button></div>
            </form>
          )}
          {may('impersonate') && (
            <form method="post" action={action('impersonate')} className="grid" data-testid="impersonate-form">
              <input type="hidden" name="back" value={back} />
              <strong>View as a member (read-only, 30 minutes)</strong>
              <label className="row">
                Member
                <select name="userId" required>
                  {o.members.map((m) => <option key={m.userId} value={m.userId}>{m.name} ({m.email}, {m.role})</option>)}
                </select>
              </label>
              <Reason id="impersonate-reason" />
              <div>
                <button className="btn secondary">Start read-only session</button>{' '}
                <span className="muted">Recorded in the customer’s own audit log as “Beacon support”.</span>
              </div>
            </form>
          )}
        </div>
      )}

      <div className="card">
        <h2>Members</h2>
        <table data-testid="members">
          <thead>
            <tr><th scope="col">Name</th><th scope="col">Email</th><th scope="col">Role</th><th scope="col">Verified</th><th scope="col">Last active</th><th scope="col">Support</th></tr>
          </thead>
          <tbody>
            {o.members.map((m) => (
              <tr key={m.userId}>
                <td>{m.name}</td>
                <td>{m.email}</td>
                <td>{m.role}</td>
                <td>{m.emailVerified ? 'yes' : 'no'}</td>
                <td>{fmt(m.lastActiveAt)} ({m.activeSessions} session{m.activeSessions === 1 ? '' : 's'})</td>
                <td>
                  {may('email.resend') && !m.emailVerified && (
                    <details>
                      <summary>Resend verification</summary>
                      <form method="post" action={action('resend-verification')} className="grid">
                        <input type="hidden" name="back" value={back} />
                        <input type="hidden" name="userId" value={m.userId} />
                        <Reason id={`verify-${m.userId}`} />
                        <button className="btn secondary">Send</button>
                      </form>
                    </details>
                  )}
                  {may('sessions.revoke') && m.activeSessions > 0 && (
                    <details>
                      <summary>Sign out everywhere</summary>
                      <form method="post" action={action('revoke-sessions')} className="grid">
                        <input type="hidden" name="back" value={back} />
                        <input type="hidden" name="userId" value={m.userId} />
                        <Reason id={`revoke-${m.userId}`} />
                        <button className="btn secondary">Sign out</button>
                      </form>
                    </details>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {o.invitations.length > 0 && (
        <div className="card">
          <h2>Open invitations</h2>
          <table data-testid="invitations">
            <thead>
              <tr><th scope="col">Email</th><th scope="col">Role</th><th scope="col">State</th><th scope="col">Expires</th><th scope="col">Support</th></tr>
            </thead>
            <tbody>
              {o.invitations.map((i) => (
                <tr key={i.id}>
                  <td>{i.email}</td>
                  <td>{i.role}</td>
                  <td>{i.state}</td>
                  <td>{fmt(i.expiresAt)}</td>
                  <td>
                    {may('email.resend') && (
                      <details>
                        <summary>Resend invite</summary>
                        <form method="post" action={action('resend-invitation')} className="grid">
                          <input type="hidden" name="back" value={back} />
                          <input type="hidden" name="invitationId" value={i.id} />
                          <Reason id={`invite-${i.id}`} />
                          <button className="btn secondary">Resend</button>
                        </form>
                      </details>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="card">
        <h2>Last 10 incidents</h2>
        {o.recentIncidents.length === 0 ? (
          <p className="muted">None.</p>
        ) : (
          <table data-testid="incidents">
            <thead>
              <tr><th scope="col">Monitor</th><th scope="col">Cause</th><th scope="col">Opened</th><th scope="col">Resolved</th></tr>
            </thead>
            <tbody>
              {o.recentIncidents.map((i) => (
                <tr key={i.id}><td>{i.monitorName}</td><td>{i.cause}</td><td>{fmt(i.openedAt)}</td><td>{fmt(i.resolvedAt)}</td></tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="card">
        <h2>Recent audit events</h2>
        <table data-testid="org-audit">
          <thead>
            <tr><th scope="col">When</th><th scope="col">Action</th><th scope="col">Actor</th><th scope="col">Target</th><th scope="col">Reason</th></tr>
          </thead>
          <tbody>
            {o.audit.map((e) => (
              <tr key={e.id} data-action={e.action}>
                <td>{fmt(e.occurredAt)}</td>
                <td title={isAuditAction(e.action) ? AUDIT_ACTIONS[e.action].description : ''}><code>{e.action}</code></td>
                <td>{e.actorType === 'staff' ? `staff ${e.actorEmail ?? ''}` : (e.actorEmail ?? e.actorName ?? e.actorType)}{e.onBehalfOfName ? ` (as ${e.onBehalfOfName})` : ''}</td>
                <td>{e.targetType} {e.targetName ?? ''}</td>
                <td className="muted">{e.reason ?? ''}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {staffCan(staff.role, 'audit.read') && <p className="muted"><Link href={`/internal/audit?org=${o.org.id}`}>All of this org’s events</Link></p>}
      </div>

      {o.impersonations.length > 0 && (
        <div className="card">
          <h2>Impersonation sessions</h2>
          <ul>
            {o.impersonations.map((s) => (
              <li key={s.id}>
                {fmt(s.createdAt)} · {s.staffEmail} · {s.endedAt ? `ended ${fmt(s.endedAt)}` : s.expiresAt < new Date() ? 'expired' : `active until ${fmt(s.expiresAt)}`} · <span className="muted">{s.reason}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}
