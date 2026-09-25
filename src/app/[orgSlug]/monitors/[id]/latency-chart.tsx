/**
 * Lesson 6.3: the feature behind the `monitor-latency-chart` beta flag. A
 * small response-time chart of the latest checks, drawn as inline SVG on the
 * server (no chart library for 20 points). The page decides whether to show
 * it with isEnabled(); this component knows nothing about flags.
 *
 * Accessibility (lesson 6.1): the SVG is one image with a text summary, and
 * failed checks are marked with a cross as well as a colour.
 */
export function LatencyChart({ checks }: { checks: { id: string; ok: boolean; latencyMs: number | null; checkedAt: Date }[] }) {
  const points = [...checks].reverse().filter((c) => c.latencyMs !== null) as { id: string; ok: boolean; latencyMs: number; checkedAt: Date }[];
  if (points.length < 2) return <p className="muted">The chart appears after two checks.</p>;
  const W = 600;
  const H = 120;
  const max = Math.max(...points.map((p) => p.latencyMs), 1);
  const x = (i: number) => (i / (points.length - 1)) * (W - 20) + 10;
  const y = (ms: number) => H - 10 - (ms / max) * (H - 20);
  const avg = Math.round(points.reduce((s, p) => s + p.latencyMs, 0) / points.length);
  const summary = `Response time of the last ${points.length} checks: average ${avg} ms, slowest ${max} ms, ${points.filter((p) => !p.ok).length} failed.`;
  return (
    <figure style={{ margin: 0 }} data-testid="latency-chart">
      <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label={summary} style={{ width: '100%', height: 'auto' }}>
        <polyline fill="none" stroke="var(--accent)" strokeWidth="2" points={points.map((p, i) => `${x(i)},${y(p.latencyMs)}`).join(' ')} />
        {points.map((p, i) =>
          p.ok ? (
            <circle key={p.id} cx={x(i)} cy={y(p.latencyMs)} r="3" fill="var(--up)" />
          ) : (
            <text key={p.id} x={x(i)} y={y(p.latencyMs) + 4} textAnchor="middle" fontSize="12" fill="var(--down)">✕</text>
          ),
        )}
      </svg>
      <figcaption className="muted">{summary}</figcaption>
    </figure>
  );
}
