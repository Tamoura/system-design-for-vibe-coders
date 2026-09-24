'use client';

import { useEffect, useState } from 'react';
import { useRealtime, useRefresh, useResyncOnReconnect } from '../../realtime';

/** Lesson 4.3: the monitor page refetches itself when this monitor gets a new check or an incident changes. */
export function LiveRefresh({ monitorId }: { monitorId: string }) {
  const refresh = useRefresh(500);
  const mine = (data: unknown) => (data as { monitorId?: string }).monitorId === monitorId;
  useRealtime('monitor.status', (data) => mine(data) && refresh());
  useRealtime('incident.changed', (data) => mine(data) && refresh());
  useResyncOnReconnect(refresh);
  return null;
}

type Viewer = { userId: string; name: string };

/**
 * Lesson 4.3 (🟡): "Alice and Bob are viewing". Heartbeat every 10 s (the
 * server forgets anyone silent for 30 s), ask again when someone joins or
 * leaves, and say goodbye when the tab closes.
 */
export function Presence({ orgSlug, topic, me }: { orgSlug: string; topic: string; me: string }) {
  const [viewers, setViewers] = useState<Viewer[]>([]);
  const url = `/api/orgs/${orgSlug}/presence`;

  const beat = async () => {
    const res = await fetch(url, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ topic }) });
    if (res.ok) setViewers((await res.json()).data);
  };

  useEffect(() => {
    void beat();
    const timer = setInterval(() => void beat(), 10_000);
    const bye = () => void fetch(`${url}?topic=${encodeURIComponent(topic)}`, { method: 'DELETE', keepalive: true });
    window.addEventListener('pagehide', bye);
    return () => {
      clearInterval(timer);
      window.removeEventListener('pagehide', bye);
      bye();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [url, topic]);
  useRealtime('presence.changed', (data) => {
    if ((data as { topic: string }).topic === topic) void beat();
  });

  const others = viewers.filter((v) => v.userId !== me).map((v) => v.name);
  if (others.length === 0) return <span className="muted" data-testid="presence">Only you are viewing this monitor.</span>;
  const names = others.length === 1 ? others[0] : `${others.slice(0, -1).join(', ')} and ${others.at(-1)}`;
  return (
    <span className="muted" data-testid="presence">
      👀 {names} {others.length === 1 ? 'is' : 'are'} also viewing this monitor.
    </span>
  );
}
