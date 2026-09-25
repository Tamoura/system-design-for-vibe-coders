import Link from 'next/link';
import { can } from '@/core/permissions';
import { cheapestPlanWhere, PLANS } from '@/core/plans';
import { formatMicros } from '@/core/ai';
import { forPage, requirePermission } from '@/lib/access';
import { aiUsageForMonth, getAiSettings } from '@/lib/ai/incident-summary';
import { setAiSummariesAction } from './actions';

export const dynamic = 'force-dynamic';

/**
 * Lesson 8.2: Organization → AI summaries. The questions a security
 * questionnaire asks about AI, answered on the page that controls it: can we
 * turn it off (it starts off), which provider sees our data, is it used for
 * training, can a person check it before it is public, what does it cost.
 */
export default async function AiSettingsPage({ params, searchParams }: { params: Promise<{ orgSlug: string }>; searchParams: Promise<Record<string, string | undefined>> }) {
  const { orgSlug } = await params;
  const query = await searchParams;
  const ctx = await forPage(requirePermission(orgSlug, 'org.manage'), `/${orgSlug}/settings/ai`);
  const ai = await getAiSettings(ctx);
  if (!ai.entitled) {
    const upgradeTo = cheapestPlanWhere((e) => e.aiSummaries);
    return (
      <section className="grid page-narrow">
        <h1>AI incident summaries</h1>
        <div className="card grid" data-testid="ai-upgrade">
          <strong>Draft incident summaries with AI</strong>
          <p className="muted" style={{ margin: 0 }}>
            When an incident resolves, Beacon drafts a summary and a status-page update from its checks and timeline, for your team to
            edit and publish. AI summaries are part of the {upgradeTo ? PLANS[upgradeTo].name : 'higher'} plan.
          </p>
          {can(ctx.role, 'billing.manage') ? <div><Link className="btn" href={`/${ctx.orgSlug}/billing`}>Upgrade</Link></div> : <p className="muted">Ask an owner to upgrade.</p>}
        </div>
      </section>
    );
  }
  const usage = await aiUsageForMonth(ctx);
  return (
    <section className="grid page-narrow">
      <h1>AI incident summaries</h1>
      <div className="card grid">
        <strong>{ai.enabled ? 'On' : 'Off'}</strong>
        <p className="muted" style={{ margin: 0 }}>
          When on, Beacon sends a resolved incident’s data (monitor name and host, check results and error text, timeline notes, how many
          people were alerted; never email addresses or phone numbers) to <strong>{ai.providers.map((p) => (p.name === 'fake' ? 'a built-in stand-in (no provider configured)' : 'Anthropic')).filter((v, i, a) => a.indexOf(v) === i).join(', ')}</strong>{' '}
          to draft a summary. The provider does not train on it. Drafts never reach your status page until someone clicks Publish.
        </p>
        <form action={setAiSummariesAction.bind(null, ctx.orgSlug, !ai.enabled)}>
          <button className={ai.enabled ? 'btn secondary' : 'btn'} data-testid="ai-toggle">{ai.enabled ? 'Turn off AI summaries' : 'Turn on AI summaries'}</button>
        </form>
        {query.error && <div className="error" role="alert">{query.error}</div>}
      </div>
      <div className="card grid" data-testid="ai-usage">
        <strong>This month</strong>
        <p className="muted" style={{ margin: 0 }}>
          {usage.total.calls} model call{usage.total.calls === 1 ? '' : 's'}, {usage.total.inputTokens + usage.total.outputTokens} tokens, about {formatMicros(usage.total.costMicros)}.
          Tokens are metered to your usage (<code>ai_tokens</code>).
        </p>
        {usage.rows.length > 0 && (
          <table>
            <thead><tr><th>Model</th><th>Outcome</th><th>Calls</th><th>Input tokens</th><th>Output tokens</th><th>Cost</th></tr></thead>
            <tbody>
              {usage.rows.map((r) => (
                <tr key={`${r.model}-${r.outcome}`}><td>{r.model}</td><td>{r.outcome}</td><td>{r.calls}</td><td>{r.inputTokens}</td><td>{r.outputTokens}</td><td>{formatMicros(r.costMicros)}</td></tr>
              ))}
            </tbody>
          </table>
        )}
        <p className="muted" style={{ margin: 0 }}>Models: {ai.providers.map((p) => p.model).join(', then ')}.</p>
      </div>
    </section>
  );
}
