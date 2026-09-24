'use client';

import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { reconnectDelayMs } from '@/core/retry';

/*
 * Lesson 4.3: ONE live connection per tab for everything under /[orgSlug]
 * (dashboard tiles, the bell, presence), shared through React context.
 * Browsers allow ~6 connections per origin over HTTP/1.1, so one per
 * component would soon block ordinary requests.
 *
 * EventSource reconnects on its own, but always after the same delay: when a
 * server restarts, every open dashboard would come back in the same second.
 * So on an error we close it and reconnect ourselves with exponential backoff
 * and full jitter (src/core/retry.ts): 20,000 dashboards spread their
 * reconnects over several seconds instead of one spike.
 *
 * On every (re)connect the server sends "ready", and listeners of
 * "connected" resync (refetch), because events sent while we were away are
 * gone: pub/sub does not replay.
 */

type Handler = (data: unknown) => void;
type Status = 'connecting' | 'live' | 'reconnecting' | 'stopped';
type Realtime = { on: (type: string, handler: Handler) => () => void; status: Status };

const RealtimeContext = createContext<Realtime | null>(null);
const EVENT_TYPES = ['monitor.status', 'incident.changed', 'notification', 'presence.changed'];

export function RealtimeProvider({ orgSlug, children }: { orgSlug: string; children: ReactNode }) {
  const handlers = useRef(new Map<string, Set<Handler>>());
  const [status, setStatus] = useState<Status>('connecting');
  const router = useRouter();

  useEffect(() => {
    let source: EventSource | null = null;
    let timer: ReturnType<typeof setTimeout> | undefined;
    let attempt = 0;
    let stopped = false;
    const emit = (type: string, data: unknown) => handlers.current.get(type)?.forEach((h) => h(data));

    const connect = () => {
      source = new EventSource(`/api/orgs/${orgSlug}/events`);
      source.addEventListener('ready', () => {
        attempt = 0;
        setStatus('live');
        emit('connected', {});
      });
      for (const type of EVENT_TYPES) {
        source.addEventListener(type, (e) => emit(type, JSON.parse((e as MessageEvent<string>).data)));
      }
      // The server says our access is gone (removed from the org, signed out): stop for good.
      source.addEventListener('revoked', () => {
        stopped = true;
        source?.close();
        setStatus('stopped');
        router.refresh(); // the page re-checks access too, and shows the 404

      });
      source.onerror = () => {
        source?.close();
        if (stopped) return;
        setStatus('reconnecting');
        timer = setTimeout(connect, reconnectDelayMs(attempt++));
      };
    };
    connect();
    return () => {
      stopped = true;
      clearTimeout(timer);
      source?.close();
    };
  }, [orgSlug, router]);

  // Stable, so components that subscribe do not resubscribe on every status change.
  const on = useCallback((type: string, handler: Handler) => {
    const set = handlers.current.get(type) ?? new Set<Handler>();
    set.add(handler);
    handlers.current.set(type, set);
    return () => {
      set.delete(handler);
    };
  }, []);
  const value = useMemo(() => ({ on, status }), [on, status]);
  return <RealtimeContext.Provider value={value}>{children}</RealtimeContext.Provider>;
}

/** Subscribe a component to one event type. The handler may change on every render. */
export function useRealtime(type: string, handler: Handler) {
  const realtime = useContext(RealtimeContext);
  const latest = useRef(handler);
  latest.current = handler;
  const on = realtime?.on;
  useEffect(() => on?.(type, (data) => latest.current(data)), [on, type]);
}

/** "● Live" in the nav: tells people (and the smoke test) whether updates are flowing. */
export function LiveStatus() {
  const status = useContext(RealtimeContext)?.status ?? 'connecting';
  const label = { connecting: 'connecting…', live: 'Live', reconnecting: 'reconnecting…', stopped: 'offline' }[status];
  return (
    <span className="muted live-status" data-testid="live-status" data-status={status} title="Live updates (lesson 4.3)">
      <span className={`dot ${status === 'live' ? 'up' : 'unknown'}`} style={{ display: 'inline-block', marginRight: '.3rem' }} />
      {label}
    </span>
  );
}

/**
 * router.refresh(), at most once per `ms`: re-renders the server components
 * of the current page with fresh data, without a reload (and keeps client
 * state such as a half-typed form).
 */
export function useRefresh(ms = 300) {
  const router = useRouter();
  const timer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);
  useEffect(() => () => clearTimeout(timer.current), []);
  return useCallback(() => {
    clearTimeout(timer.current);
    timer.current = setTimeout(() => router.refresh(), ms);
  }, [router, ms]);
}

/** Resync after a REconnect (the first "connected" is the page load itself, already fresh). */
export function useResyncOnReconnect(resync: () => void) {
  const first = useRef(true);
  useRealtime('connected', () => {
    if (first.current) first.current = false;
    else resync();
  });
}
