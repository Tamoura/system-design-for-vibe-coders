import { and, eq, gt, lt } from 'drizzle-orm';
import { schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { isUuid } from '@/core/validation';
import { AccessError } from './errors';
import { publish } from './realtime';

const { presence, monitors, users } = schema;

/*
 * Lesson 4.3 (🟡): presence. A tab POSTs a heartbeat every HEARTBEAT_MS; the
 * people whose last heartbeat is younger than TTL_MS are "viewing". Joining
 * and leaving publish "presence.changed", so the other tabs ask again at
 * once instead of waiting for their next heartbeat. Approximate by design:
 * a crashed tab stays listed for up to TTL_MS.
 */
export const HEARTBEAT_MS = 10_000;
export const TTL_MS = 30_000;

type Me = { orgId: string; userId: string };

/** Topics are "monitor:<id>", and the monitor must be in this org (else 404, like any object from another tenant). */
async function assertTopic(me: Me, topic: string): Promise<void> {
  const [kind, id] = topic.split(':');
  if (kind !== 'monitor' || !id || !isUuid(id)) throw new AccessError('not_found');
  const [found] = await withOrg(me.orgId, (tx) =>
    tx.select({ id: monitors.id }).from(monitors).where(and(eq(monitors.organizationId, me.orgId), eq(monitors.id, id))),
  );
  if (!found) throw new AccessError('not_found');
}

/** "I am still here". Returns everyone currently viewing the topic. */
export async function heartbeat(me: Me, topic: string, now = new Date()) {
  await assertTopic(me, topic);
  const cutoff = new Date(now.getTime() - TTL_MS);
  const { joined, viewers } = await withOrg(me.orgId, async (tx) => {
    const [before] = await tx
      .select({ lastSeenAt: presence.lastSeenAt })
      .from(presence)
      .where(and(eq(presence.organizationId, me.orgId), eq(presence.topic, topic), eq(presence.userId, me.userId)));
    await tx
      .insert(presence)
      .values({ organizationId: me.orgId, topic, userId: me.userId, lastSeenAt: now })
      .onConflictDoUpdate({ target: [presence.organizationId, presence.topic, presence.userId], set: { lastSeenAt: now } });
    // Housekeeping: forget rows nobody has refreshed for a while.
    await tx.delete(presence).where(and(eq(presence.organizationId, me.orgId), lt(presence.lastSeenAt, new Date(now.getTime() - 10 * TTL_MS))));
    const viewers = await tx
      .select({ userId: users.id, name: users.name })
      .from(presence)
      .innerJoin(users, eq(users.id, presence.userId))
      .where(and(eq(presence.organizationId, me.orgId), eq(presence.topic, topic), gt(presence.lastSeenAt, cutoff)))
      .orderBy(users.name);
    return { joined: !before || before.lastSeenAt <= cutoff, viewers };
  });
  if (joined) await publish(me.orgId, { type: 'presence.changed', topic });
  return viewers;
}

/** The tab is closing. */
export async function leave(me: Me, topic: string) {
  await assertTopic(me, topic);
  const removed = await withOrg(me.orgId, (tx) =>
    tx
      .delete(presence)
      .where(and(eq(presence.organizationId, me.orgId), eq(presence.topic, topic), eq(presence.userId, me.userId)))
      .returning({ userId: presence.userId }),
  );
  if (removed.length) await publish(me.orgId, { type: 'presence.changed', topic });
}
