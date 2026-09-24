import { can } from '@/core/permissions';
import type { OrgContext } from './access';
import { findMembership } from './organizations';
import { subscribe, type RealtimeEvent } from './realtime';

/*
 * Lesson 4.3 (🟢/🟡): Server-Sent Events for one user in one org.
 *
 *   - authorized when it opens (the route calls requirePermission first:
 *     401 without a session, 404 for a non-member, like every org route);
 *   - authorized AGAIN every REALTIME_RECHECK_MS (30 s): removed from the
 *     org, role without "monitor.read", or signed out → an "event: revoked"
 *     and the stream ends. The lesson: "a socket opened yesterday shouldn't
 *     outlive today's revoked membership";
 *   - only this org's channel, and "notification.created" only for this user;
 *   - a comment line every 25 s so proxies and load balancers keep the idle
 *     connection open;
 *   - no replay: after a reconnect the browser refetches the page (resync),
 *     because pub/sub drops whatever was sent while it was away.
 */

const PING_MS = 25_000;

export type StreamOptions = {
  /** Checks the session behind the request is still valid (the route passes Better Auth's check). */
  sessionStillValid: () => Promise<boolean>;
  recheckMs?: number;
};

export function eventStream(req: Request, ctx: OrgContext, opts: StreamOptions): Response {
  const recheckMs = opts.recheckMs ?? Number(process.env.REALTIME_RECHECK_MS ?? 30_000);
  const encoder = new TextEncoder();
  let stop: () => Promise<void> = async () => {};

  const stream = new ReadableStream<Uint8Array>({
    async start(controller) {
      let closed = false;
      const send = (text: string) => {
        if (closed) return;
        try {
          controller.enqueue(encoder.encode(text));
        } catch {
          void stop(); // the client went away between two writes
        }
      };
      const forward = (event: RealtimeEvent) => {
        if (event.type === 'notification.created') {
          // Someone else's notification is none of this user's business, not even that it exists.
          if (event.userId === ctx.userId) send('event: notification\ndata: {}\n\n');
          return;
        }
        send(`event: ${event.type}\ndata: ${JSON.stringify(event)}\n\n`);
      };

      const unsubscribe = await subscribe(ctx.orgId, forward);
      const ping = setInterval(() => send(': ping\n\n'), PING_MS);
      const recheck = setInterval(async () => {
        if (!(await stillAllowed(ctx, opts))) {
          send('event: revoked\ndata: {}\n\n');
          await stop();
        }
      }, recheckMs);

      stop = async () => {
        if (closed) return;
        closed = true;
        clearInterval(ping);
        clearInterval(recheck);
        await unsubscribe();
        try {
          controller.close();
        } catch {
          // already closed by the client
        }
      };
      req.signal.addEventListener('abort', () => void stop());

      // "ready" tells the browser it is live, and that it should resync if this is a reconnect.
      send(': connected\n\nevent: ready\ndata: {}\n\n');
    },
    async cancel() {
      await stop();
    },
  });

  return new Response(stream, {
    headers: {
      'content-type': 'text/event-stream; charset=utf-8',
      'cache-control': 'no-cache, no-transform',
      connection: 'keep-alive',
      'x-accel-buffering': 'no', // nginx: do not buffer the stream
    },
  });
}

/** The same questions as when the stream opened, asked from scratch (no per-request cache). */
async function stillAllowed(ctx: OrgContext, opts: StreamOptions): Promise<boolean> {
  try {
    const membership = await findMembership(ctx.orgSlug, ctx.userId);
    if (!membership || membership.id !== ctx.orgId || !can(membership.role, 'monitor.read')) return false;
    return await opts.sessionStillValid();
  } catch {
    return true; // a database hiccup is not a revocation; ask again next time
  }
}
