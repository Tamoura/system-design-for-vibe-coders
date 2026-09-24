import type { listRuns } from '@/lib/workflows';

type Run = Awaited<ReturnType<typeof listRuns>>[number];

const ms = (a: Date, b: Date | null) => (b ? `${b.getTime() - a.getTime()} ms` : '…');
const json = (v: unknown) => (v === null || v === undefined ? '' : JSON.stringify(v));

/**
 * Lesson 5.4 (🟢): what an engine's dashboard shows, for this incident's runs:
 * each step with its status, input, output and timing. It is read from the
 * run's history (workflow_steps), the same rows that let a run resume.
 */
export function WorkflowRuns({ runs }: { runs: Run[] }) {
  if (runs.length === 0) return null;
  return (
    <details className="muted" style={{ marginTop: '.3rem' }} data-testid="workflow-runs">
      <summary>Workflows ({runs.map((r) => `${r.workflow}: ${r.status}`).join(', ')})</summary>
      {runs.map((r) => (
        <div key={r.id} style={{ margin: '.4rem 0' }}>
          <strong>{r.workflow}</strong> · {r.status}
          {r.status === 'waiting' && r.wakeAt && ` until ${r.wakeAt.toISOString().slice(11, 19)} UTC`}
          {r.error && <span className="error"> · {r.error}</span>}
          <table style={{ fontSize: '.8rem' }}>
            <tbody>
              {r.steps.map((s) => (
                <tr key={s.id}>
                  <td><code>{s.name}</code></td>
                  <td>{s.status}{s.attempts > 1 ? ` (${s.attempts} attempts)` : ''}</td>
                  <td>{s.startedAt.toISOString().slice(11, 19)}</td>
                  <td>{ms(s.startedAt, s.finishedAt)}</td>
                  <td style={{ maxWidth: 260, overflowWrap: 'anywhere' }}>{json(s.input)}</td>
                  <td style={{ maxWidth: 260, overflowWrap: 'anywhere' }}>{s.error ?? json(s.output)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </details>
  );
}
