import Link from 'next/link';
import { notFound } from 'next/navigation';
import { forPage, requirePermission } from '@/lib/access';
import { getEndpointLog } from '@/lib/webhooks';
import { deleteEndpointAction, replayFailedAction, resendMessageAction, setEndpointEnabledAction } from '../actions';
import { SinceInput } from './since-input';

export const dynamic = 'force-dynamic';

const time = (d: Date | null) => (d ? d.toISOString().slice(0, 19).replace('T', ' ') : '');

/**
 * Lesson 5.3 (🟡): the customer-facing delivery log. Every message with every
 * attempt (status code, time, the start of the response), a Resend button per
 * message, and "Replay failed since…": the page that turns "did you send it?"
 * support tickets into self-service.
 */
export default async function EndpointPage({ params, searchParams }: { params: Promise<{ orgSlug: string; id: string }>; searchParams: Promise<{ replayed?: string; resent?: string }> }) {
  const { orgSlug, id } = await params;
  const { replayed, resent } = await searchParams;
  const ctx = await forPage(requirePermission(orgSlug, 'integration.manage'), `/${orgSlug}/settings/webhooks/${id}`);
  const log = await getEndpointLog(ctx, id);
  if (!log) notFound();
  const { endpoint, messages } = log;
  return (
    <section className="grid" style={{ maxWidth: 900 }}>
      <div className="row">
        <h1 style={{ margin: 0, fontSize: '1.3rem', wordBreak: 'break-all' }}>{endpoint.url}</h1>
        <Link href={`/${ctx.orgSlug}/settings/webhooks`} className="muted">← Webhooks</Link>
      </div>
      <div className="card grid">
        <div>
          <span className="muted">Events</span> {endpoint.eventTypes.map((t) => <code key={t} style={{ marginRight: '.3rem' }}>{t}</code>)}
        </div>
        <div data-testid="endpoint-status">
          <span className="muted">Status</span>{' '}
          {endpoint.enabled ? (endpoint.failingSince ? <span className="error">enabled, failing since {time(endpoint.failingSince)}</span> : 'enabled') : <span className="error">disabled: {endpoint.disabledReason}</span>}
        </div>
        <div className="row">
          <form action={setEndpointEnabledAction.bind(null, ctx.orgSlug, endpoint.id, !endpoint.enabled)}>
            <button className="btn secondary">{endpoint.enabled ? 'Disable' : 'Enable'}</button>
          </form>
          <form action={deleteEndpointAction.bind(null, ctx.orgSlug, endpoint.id)}>
            <button className="btn secondary">Delete endpoint</button>
          </form>
        </div>
      </div>
      <form action={replayFailedAction.bind(null, ctx.orgSlug, endpoint.id)} className="card row">
        <label htmlFor="since">Replay every failed message since</label>
        <SinceInput />
        <button className="btn">Replay failed</button>
        {replayed !== undefined && <span className="muted" data-testid="replayed">{replayed} message(s) queued again.</span>}
        {resent && <span className="muted">Queued again.</span>}
      </form>
      <div className="card">
        {messages.length === 0 ? (
          <span className="muted">Nothing sent yet.</span>
        ) : (
          <table data-testid="delivery-log">
            <thead>
              <tr><th>Event</th><th>webhook-id</th><th>Created</th><th>Status</th><th>Attempts</th><th /></tr>
            </thead>
            <tbody>
              {messages.map((m) => (
                <tr key={m.id} data-testid={`message-${m.status}`}>
                  <td><code>{m.eventType}</code></td>
                  <td><code style={{ fontSize: '.75rem' }}>{m.webhookId}</code></td>
                  <td className="muted">{time(m.createdAt)}</td>
                  <td>{m.status === 'delivered' ? <span className="badge delivery sent">delivered</span> : m.status === 'failed' ? <span className="badge delivery failed">failed</span> : <span className="badge">pending</span>}</td>
                  <td>
                    <details>
                      <summary>{m.attempts.length} attempt(s)</summary>
                      <ol style={{ margin: '.3rem 0', paddingLeft: '1.2rem' }}>
                        {m.attempts.map((a) => (
                          <li key={a.id} className="muted">
                            {time(a.createdAt)} · {a.statusCode ?? 'no response'} · {a.durationMs} ms{a.trigger === 'manual' ? ' · manual' : ''}
                            {a.error && <div className="error">{a.error}</div>}
                            {a.responseBody && <pre style={{ whiteSpace: 'pre-wrap', margin: 0 }}>{a.responseBody}</pre>}
                          </li>
                        ))}
                      </ol>
                    </details>
                  </td>
                  <td>
                    <form action={resendMessageAction.bind(null, ctx.orgSlug, endpoint.id, m.id)}>
                      <button className="link-btn">Resend</button>
                    </form>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </section>
  );
}
