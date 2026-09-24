import Link from 'next/link';
import { forPage, requirePermission } from '@/lib/access';
import { listEndpoints } from '@/lib/webhooks';
import { CreateEndpointForm } from './create-endpoint-form';

export const dynamic = 'force-dynamic';

/** Lesson 5.3 (🟢): the org's webhook endpoints. Owners and admins ("integration.manage"). */
export default async function WebhooksPage({ params }: { params: Promise<{ orgSlug: string }> }) {
  const { orgSlug } = await params;
  const ctx = await forPage(requirePermission(orgSlug, 'integration.manage'), `/${orgSlug}/settings/webhooks`);
  const endpoints = await listEndpoints(ctx);
  return (
    <section className="grid" style={{ maxWidth: 760 }}>
      <div className="row">
        <h1 style={{ margin: 0 }}>Webhooks</h1>
        <Link href={`/${ctx.orgSlug}/settings`} className="muted">← Settings</Link>
      </div>
      <p className="muted" style={{ margin: 0 }}>
        Beacon POSTs a signed JSON event to your URL when an incident opens or resolves. Answer 2xx quickly; failed deliveries are
        retried for about a day and a half. Deliveries can arrive twice or out of order: deduplicate on the <code>webhook-id</code> header.
      </p>
      <CreateEndpointForm orgSlug={ctx.orgSlug} />
      <div className="card">
        {endpoints.length === 0 ? (
          <span className="muted">No endpoints yet.</span>
        ) : (
          <table>
            <tbody>
              {endpoints.map((e) => (
                <tr key={e.id}>
                  <td>
                    <Link href={`/${ctx.orgSlug}/settings/webhooks/${e.id}`}>{e.url}</Link>
                    {e.description && <div className="muted">{e.description}</div>}
                  </td>
                  <td>{e.eventTypes.map((t) => <code key={t} style={{ marginRight: '.3rem' }}>{t}</code>)}</td>
                  <td>
                    {!e.enabled ? (
                      <span className="error">disabled</span>
                    ) : e.failingSince ? (
                      <span className="error">failing since {e.failingSince.toISOString().slice(0, 16).replace('T', ' ')}</span>
                    ) : (
                      <span className="badge">active</span>
                    )}
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
