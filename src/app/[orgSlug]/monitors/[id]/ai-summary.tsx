import Link from 'next/link';
import type { IncidentSummary } from '@/db/schema';
import { saveSummaryAction, summarizeIncidentAction } from './actions';

type Props = {
  orgSlug: string;
  monitorId: string;
  incidentId: string;
  summary: IncidentSummary | undefined;
  ai: { entitled: boolean; enabled: boolean };
  can: { write: boolean; publish: boolean; manageOrg: boolean; billing: boolean };
};

type Details = { impact?: string; suspectedCause?: string | null; timeline?: { at: string; event: string }[] };

/**
 * Lesson 8.2 (🟢): one incident's AI summary. The model's words are shown as
 * TEXT (React escapes them: never as HTML, lesson 8.2 "treat output as
 * untrusted"), in a form a person edits; only "Save and publish" puts them on
 * the public status page.
 */
export function AiSummary({ orgSlug, monitorId, incidentId, summary, ai, can }: Props) {
  if (!ai.entitled) {
    return (
      <div className="ai-summary muted" data-testid="ai-upgrade-prompt">
        ✨ AI incident summaries are on the Business plan.{' '}
        {can.billing ? <Link href={`/${orgSlug}/billing`}>Upgrade</Link> : 'Ask an owner to upgrade.'}
      </div>
    );
  }
  if (!ai.enabled) {
    return can.manageOrg ? (
      <div className="ai-summary muted">
        ✨ <Link href={`/${orgSlug}/settings/ai`}>Turn on AI summaries</Link> to get a draft when an incident resolves.
      </div>
    ) : null;
  }
  const ask = summarizeIncidentAction.bind(null, orgSlug, monitorId, incidentId);
  if (!summary) {
    return can.write ? (
      <form action={ask} className="ai-summary">
        <button className="link-btn" data-testid="ai-summarize">✨ Summarize with AI</button>
      </form>
    ) : null;
  }
  if (summary.status === 'generating') return <div className="ai-summary muted" data-testid="ai-generating">✨ Writing a summary…</div>;
  if (summary.status === 'failed') {
    return (
      <div className="ai-summary" data-testid="ai-failed">
        <span className="error">{summary.error}</span>{' '}
        {can.write && (
          <form action={ask} style={{ display: 'inline' }}>
            <button className="link-btn">Retry</button>
          </form>
        )}
      </div>
    );
  }
  const details = (summary.details ?? {}) as Details;
  if (summary.status === 'published') {
    return (
      <div className="ai-summary" data-testid="ai-published">
        <span className="badge">published</span> <strong>{summary.headline}</strong>
        <p style={{ margin: '.3rem 0 0' }}>{summary.body}</p>
      </div>
    );
  }
  return (
    <div className="ai-summary grid" data-testid="ai-draft">
      <div className="muted">
        ✨ Draft by AI ({summary.model}){summary.editedAt ? ', edited' : ''}. Check it before publishing: it is what your customers will read.
      </div>
      {details.impact && <div><span className="muted">Impact</span> {details.impact}</div>}
      {details.suspectedCause && <div><span className="muted">Suspected cause</span> {details.suspectedCause}</div>}
      {details.timeline && details.timeline.length > 0 && (
        <ul className="updates">
          {details.timeline.map((t) => (
            <li key={`${t.at}-${t.event}`}><span className="muted">{t.at.slice(11, 16)}</span> {t.event}</li>
          ))}
        </ul>
      )}
      {can.write ? (
        <form action={saveSummaryAction.bind(null, orgSlug, monitorId, incidentId)} className="grid" style={{ gap: '.4rem' }}>
          <input name="headline" defaultValue={summary.headline ?? ''} maxLength={120} required aria-label="Headline" />
          <textarea name="body" defaultValue={summary.body ?? ''} maxLength={600} rows={3} required aria-label="Status page update" />
          <div className="row" style={{ gap: '.4rem' }}>
            <button className="btn secondary" name="publish" value="no">Save draft</button>
            {can.publish && <button className="btn" name="publish" value="yes" data-testid="ai-publish">Save and publish to status page</button>}
            <button className="link-btn" formAction={summarizeIncidentAction.bind(null, orgSlug, monitorId, incidentId)} formNoValidate>Regenerate</button>
          </div>
        </form>
      ) : (
        <div><strong>{summary.headline}</strong><p style={{ margin: 0 }}>{summary.body}</p></div>
      )}
    </div>
  );
}
