'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useRealtime, useRefresh, useResyncOnReconnect } from '../realtime';

/** What the server hands over for each tile (dates as ISO strings). */
export type MonitorTile = {
  id: string;
  name: string;
  url: string;
  intervalSeconds: number;
  pausedReason: 'manual' | 'plan_limit' | null;
  state: 'up' | 'down' | 'unknown';
  lastCheckedAt: string | null;
  lastLatencyMs: number | null;
  uptime24h: number | null;
  openIncident: { cause: string } | null;
};

type Live = { state: 'up' | 'down'; checkedAt: string; latencyMs: number | null };

function ago(iso: string | null, now: number) {
  if (!iso) return 'never';
  const s = Math.max(0, Math.round((now - Date.parse(iso)) / 1000));
  if (s < 60) return `${s}s ago`;
  if (s < 3600) return `${Math.round(s / 60)}m ago`;
  return `${Math.round(s / 3600)}h ago`;
}

/**
 * Lesson 4.3 (🟢): the dashboard without polling. A "monitor.status" event
 * updates its tile in place (dot, latency, "checked … ago"); an incident
 * opening or resolving, a monitor we do not know yet, or a reconnect
 * refetches the whole list from the server, which is the resync.
 */
export function LiveMonitorList({ orgSlug, monitors, renderedAt }: { orgSlug: string; monitors: MonitorTile[]; renderedAt: number }) {
  const [live, setLive] = useState<Record<string, Live>>({});
  const [now, setNow] = useState(renderedAt);
  const refresh = useRefresh();

  // Fresh data from the server replaces what the events told us.
  useEffect(() => setLive({}), [monitors]);
  useEffect(() => {
    const timer = setInterval(() => setNow(Date.now()), 5000);
    return () => clearInterval(timer);
  }, []);

  useRealtime('monitor.status', (data) => {
    const e = data as Live & { monitorId: string };
    if (!monitors.some((m) => m.id === e.monitorId)) return refresh();
    setLive((prev) => ({ ...prev, [e.monitorId]: { state: e.state, checkedAt: e.checkedAt, latencyMs: e.latencyMs } }));
    setNow(Date.now());
  });
  useRealtime('incident.changed', () => refresh());
  useResyncOnReconnect(refresh);

  return (
    <>
      {monitors.map((m) => {
        const l = live[m.id];
        const state = l?.state ?? m.state;
        const latency = l ? l.latencyMs : m.lastLatencyMs;
        return (
          <div className="card row" key={m.id} data-testid="monitor-tile" data-monitor-id={m.id} data-state={state}>
            <span className={`dot ${state}`} title={state} />
            <div style={{ flex: 1, minWidth: 200 }}>
              <Link href={`/${orgSlug}/monitors/${m.id}`}><strong>{m.name}</strong></Link>
              <div className="muted">{m.url}</div>
            </div>
            <div className="muted">
              every {m.intervalSeconds}s{m.pausedReason === 'manual' ? ' · paused' : m.pausedReason === 'plan_limit' ? ' · paused (plan limit)' : ''}
            </div>
            <div className="muted">{m.uptime24h === null ? '—' : `${m.uptime24h}%`} 24h</div>
            <div className="muted" data-testid="checked-ago">
              {latency === null ? '' : `${latency} ms · `}checked {ago(l?.checkedAt ?? m.lastCheckedAt, now)}
            </div>
            {m.openIncident && <div className="error">Incident open: {m.openIncident.cause}</div>}
          </div>
        );
      })}
    </>
  );
}
