import Link from 'next/link';
import { API_SCOPES, API_SCOPE_IDS, canGrantScopes } from '@/core/api-keys';
import { can } from '@/core/permissions';
import { cheapestPlanWhere, PLANS } from '@/core/plans';
import { forPage, requirePermission } from '@/lib/access';
import { listApiKeys } from '@/lib/api-keys';
import { getEntitlements } from '@/lib/entitlements';
import { revokeApiKeyAction } from './actions';
import { CreateKeyForm } from './create-key-form';

export const dynamic = 'force-dynamic';

const when = (d: Date | null) => (d ? d.toISOString().slice(0, 16).replace('T', ' ') : 'never');

/** Lesson 5.2 (🟢): the org's API keys. Owners and admins ("integration.manage"). */
export default async function ApiKeysPage({ params }: { params: Promise<{ orgSlug: string }> }) {
  const { orgSlug } = await params;
  const ctx = await forPage(requirePermission(orgSlug, 'integration.manage'), `/${orgSlug}/settings/api-keys`);
  const [keys, ent] = await Promise.all([listApiKeys(ctx), getEntitlements(ctx)]);
  const grantable = API_SCOPE_IDS.filter((s) => canGrantScopes(ctx.role, [s])).map((id) => ({ id, label: API_SCOPES[id].label }));
  const upgradeTo = cheapestPlanWhere((e) => e.api);
  return (
    <section className="grid" style={{ maxWidth: 760 }}>
      <div className="row">
        <h1 style={{ margin: 0 }}>API keys</h1>
      </div>
      <p className="muted" style={{ margin: 0 }}>
        Keys belong to the organization, not to you: they keep working when people leave. Reference:{' '}
        <a href="/docs/api">API docs</a> · <a href="/api/v1/openapi.json">openapi.json</a>
      </p>
      {ent.api ? (
        <CreateKeyForm orgSlug={ctx.orgSlug} scopes={grantable} />
      ) : (
        <div className="card">
          The API is part of the {upgradeTo ? PLANS[upgradeTo].name : 'higher'} plan.{' '}
          {can(ctx.role, 'billing.manage') && <Link href={`/${ctx.orgSlug}/billing`}>Upgrade →</Link>}
        </div>
      )}
      <div className="card">
        {keys.length === 0 ? (
          <span className="muted">No keys yet.</span>
        ) : (
          <table>
            <thead>
              <tr><th>Name</th><th>Key</th><th>Scopes</th><th>Created</th><th>Last used</th><th /></tr>
            </thead>
            <tbody>
              {keys.map((k) => (
                <tr key={k.id} data-testid={`api-key-${k.name}`}>
                  <td>{k.name}</td>
                  <td><code>{k.keyStart}…{k.keyLast4}</code></td>
                  <td>{k.scopes.map((s) => <code key={s} style={{ marginRight: '.3rem' }}>{s}</code>)}</td>
                  <td className="muted">{when(k.createdAt)}{k.createdByName ? ` by ${k.createdByName}` : ''}</td>
                  <td className="muted">{when(k.lastUsedAt)}</td>
                  <td>
                    {k.revokedAt ? (
                      <span className="badge">revoked</span>
                    ) : (
                      <form action={revokeApiKeyAction.bind(null, ctx.orgSlug, k.id)}>
                        <button className="link-btn">Revoke</button>
                      </form>
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
