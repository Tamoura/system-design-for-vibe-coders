/**
 * Decide whether a monitor's latest results should open or resolve an incident.
 *
 * Pure function, no I/O: given whether an incident is already open and the most
 * recent results (newest first), return what to do. Requiring several failures
 * in a row avoids paging a team for one dropped packet — the cheapest defence
 * against alert fatigue (lesson 4.2).
 */
export type IncidentDecision = 'open' | 'resolve' | 'none';

export function decideIncident(
  hasOpenIncident: boolean,
  recentOkNewestFirst: boolean[],
  failuresToOpen = 2,
): IncidentDecision {
  if (recentOkNewestFirst.length === 0) return 'none';
  const latestOk = recentOkNewestFirst[0];
  if (hasOpenIncident) return latestOk ? 'resolve' : 'none';
  const streak = recentOkNewestFirst.slice(0, failuresToOpen);
  return streak.length === failuresToOpen && streak.every((ok) => !ok) ? 'open' : 'none';
}

/** Percentage of successful checks, to one decimal place. null when there is no data. */
export function uptimePercent(results: { ok: boolean }[]): number | null {
  if (results.length === 0) return null;
  const up = results.filter((r) => r.ok).length;
  return Math.round((up / results.length) * 1000) / 10;
}

export type OverallStatus = 'operational' | 'partial_outage' | 'major_outage' | 'unknown';

/** Roll individual monitor states up into the headline on the status page. */
export function overallStatus(states: ('up' | 'down' | 'unknown')[]): OverallStatus {
  const known = states.filter((s) => s !== 'unknown');
  if (known.length === 0) return 'unknown';
  const down = known.filter((s) => s === 'down').length;
  if (down === 0) return 'operational';
  return down === known.length ? 'major_outage' : 'partial_outage';
}
