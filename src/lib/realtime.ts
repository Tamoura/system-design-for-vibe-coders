import { sql as drizzleSql } from 'drizzle-orm';
import { db, sql as client } from '@/db';
import type { TenantTx } from '@/db/tenant';

/*
 * Lesson 4.3: live updates, fanned out through Postgres LISTEN/NOTIFY.
 *
 *   check runner / app ──NOTIFY beacon_org_<id>──► Postgres ──► every app instance
 *   (any process)          (sent at COMMIT)                     that LISTENs on that
 *                                                                org's channel
 *                                                                   │
 *                                                   SSE route ◄─────┘ forwards to that
 *                                                   (./realtime-stream.ts) org's browsers
 *
 * Why Postgres and not Redis (the lesson's default): Beacon already has
 * Postgres, and NOTIFY inside a transaction is delivered only when the
 * transaction commits. "Write, then publish" can then never announce
 * something that rolled back. The limits, which is why Redis pub/sub or a
 * broker takes over at scale (docs/SOLUTIONS.md): payloads under 8,000
 * bytes, every LISTEN holds a database connection per instance, and like
 * any pub/sub it is fire-and-forget: a browser that was disconnected missed
 * the events and must resync (it refetches the page on reconnect).
 *
 * Send signals, not secrets (lesson 4.3): events carry ids and states only;
 * the browser refetches details through the normal, authorized pages.
 */
export type RealtimeEvent =
  | { type: 'monitor.status'; monitorId: string; state: 'up' | 'down'; checkedAt: string; latencyMs: number | null }
  | { type: 'incident.changed'; monitorId: string; incidentId: string; state: 'opened' | 'resolved' }
  | { type: 'notification.created'; userId: string }
  | { type: 'presence.changed'; topic: string };

/** One channel per organization, like the lesson's `org:{orgId}`. Channel names are identifiers: lower case, no dashes. */
export function channelFor(orgId: string): string {
  return `beacon_org_${orgId.replace(/-/g, '').toLowerCase()}`;
}

/** Publish inside a withOrg() transaction: delivered to listeners if, and when, it commits. */
export async function publishInTx(tx: TenantTx, orgId: string, event: RealtimeEvent): Promise<void> {
  await tx.execute(drizzleSql`select pg_notify(${channelFor(orgId)}, ${JSON.stringify(event)})`);
}

/** Publish now, outside a transaction (presence heartbeats). */
export async function publish(orgId: string, event: RealtimeEvent): Promise<void> {
  await db.execute(drizzleSql`select pg_notify(${channelFor(orgId)}, ${JSON.stringify(event)})`);
}

type Listener = (event: RealtimeEvent) => void;
type Channel = { listeners: Set<Listener>; stop: Promise<() => Promise<void>> };

// One LISTEN per org channel per process, however many browsers watch it.
// Kept on globalThis so Next.js dev reloads don't leak listeners.
const registry = ((globalThis as { beaconRealtime?: Map<string, Channel> }).beaconRealtime ??= new Map());

/**
 * LISTEN on the org's channel (once per process) and call `listener` for
 * each event. Returns the function that stops listening. Uses the app's
 * Postgres client: postgres.js in the app (its listen() keeps one dedicated
 * connection for all channels), PGlite in the tests.
 */
export async function subscribe(orgId: string, listener: Listener): Promise<() => Promise<void>> {
  const name = channelFor(orgId);
  let channel = registry.get(name);
  if (!channel) {
    const listeners = new Set<Listener>();
    const onPayload = (payload: string) => {
      let event: RealtimeEvent;
      try {
        event = JSON.parse(payload);
      } catch {
        return;
      }
      for (const l of listeners) l(event);
    };
    channel = { listeners, stop: listen(name, onPayload) };
    registry.set(name, channel);
  }
  channel.listeners.add(listener);
  await channel.stop;
  const current = channel;
  return async () => {
    current.listeners.delete(listener);
    if (current.listeners.size === 0 && registry.get(name) === current) {
      registry.delete(name);
      await (await current.stop)();
    }
  };
}

/** postgres.js resolves to `{ unlisten }`, PGlite to an unsubscribe function. */
async function listen(channel: string, onPayload: (payload: string) => void): Promise<() => Promise<void>> {
  const pg = client as unknown as { listen(channel: string, cb: (payload: string) => void): Promise<(() => Promise<void>) | { unlisten(): Promise<void> }> };
  const handle = await pg.listen(channel, onPayload);
  return typeof handle === 'function' ? handle : () => handle.unlisten();
}
