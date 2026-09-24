import { and, count, desc, eq, inArray, isNull } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import {
  CATEGORIES,
  CATEGORY_IDS,
  categoryUsesChannel,
  isPhoneNumber,
  lockedReason,
  PERSONAL_CHANNELS,
  resolvePersonalChannels,
  type Category,
  type Channel,
  type PersonalChannel,
} from '@/core/notifications';
import { isUuid } from '@/core/validation';
import { InvalidRequestError } from '../errors';
import { runAfterResponse } from '../jobs';
import { deliverPendingNotifications } from './deliver';
import { isSlackWebhookUrl } from './providers';
import { notifyInTx, smsIncluded, type NotifyEvent } from './pipeline';

export { notifyInTx, type NotifyEvent } from './pipeline';
export { deliverPendingNotifications } from './deliver';

const { notifications, notificationDeliveries, notificationPreferences, orgNotificationPolicies, organizations, users } = schema;

/*
 * Lesson 4.2: notifications, the parts pages and API routes use.
 *
 *   notify(event)          the one entry point for domain code
 *   the inbox              list, unread count, mark read, mark all read
 *   preferences            the person's category × channel matrix, and phone
 *   org settings           the org's policy and Slack channel (owners, admins)
 */

/**
 * The one entry point. Writes the notifications and their deliveries in one
 * transaction, then has the channel workers send after the response.
 * Code that already has a transaction open (the check runner) calls
 * notifyInTx() inside it instead, and runs the workers itself.
 */
export async function notify(event: NotifyEvent) {
  const result = await withOrg(event.orgId, (tx) => notifyInTx(tx, event));
  kickDeliveries(event.orgId);
  return result;
}

/** Send what notifyInTx() queued, once the current response is out (lesson 4.1's "not in the request"). */
export function kickDeliveries(orgId: string) {
  runAfterResponse(() => deliverPendingNotifications({ orgId }));
}

type Me = { orgId: string; userId: string };

/*
 * The inbox. Every query names the org AND the user: you only ever see and
 * change your own notifications, in the org you are in.
 */

export async function listNotifications(me: Me, opts: { limit?: number } = {}) {
  return withOrg(me.orgId, async (tx) => {
    const rows = await tx
      .select()
      .from(notifications)
      .where(and(eq(notifications.organizationId, me.orgId), eq(notifications.userId, me.userId)))
      .orderBy(desc(notifications.createdAt))
      .limit(opts.limit ?? 50);
    // The delivery log for these notifications: which channels, and what happened.
    const deliveries = rows.length
      ? await tx
          .select({
            notificationId: notificationDeliveries.notificationId,
            channel: notificationDeliveries.channel,
            status: notificationDeliveries.status,
            error: notificationDeliveries.error,
            providerMessageId: notificationDeliveries.providerMessageId,
          })
          .from(notificationDeliveries)
          .where(and(eq(notificationDeliveries.organizationId, me.orgId), inArray(notificationDeliveries.notificationId, rows.map((r) => r.id))))
          .orderBy(notificationDeliveries.createdAt)
      : [];
    return rows.map((n) => ({
      id: n.id,
      category: n.category,
      title: n.title,
      body: n.body,
      url: n.url,
      read: n.readAt !== null,
      createdAt: n.createdAt,
      deliveries: deliveries.filter((d) => d.notificationId === n.id).map(({ channel, status, error, providerMessageId }) => ({ channel, status, error, providerMessageId })),
    }));
  });
}

export async function countUnread(me: Me): Promise<number> {
  const [row] = await withOrg(me.orgId, (tx) =>
    tx
      .select({ n: count() })
      .from(notifications)
      .where(and(eq(notifications.organizationId, me.orgId), eq(notifications.userId, me.userId), isNull(notifications.readAt))),
  );
  return row.n;
}

export async function markNotificationsRead(me: Me, ids: string[]): Promise<number> {
  const valid = ids.filter(isUuid);
  if (valid.length === 0) return 0;
  const updated = await withOrg(me.orgId, (tx) =>
    tx
      .update(notifications)
      .set({ readAt: new Date() })
      .where(
        and(
          eq(notifications.organizationId, me.orgId),
          eq(notifications.userId, me.userId),
          inArray(notifications.id, valid),
          isNull(notifications.readAt),
        ),
      )
      .returning({ id: notifications.id }),
  );
  return updated.length;
}

export async function markAllNotificationsRead(me: Me): Promise<number> {
  const updated = await withOrg(me.orgId, (tx) =>
    tx
      .update(notifications)
      .set({ readAt: new Date() })
      .where(and(eq(notifications.organizationId, me.orgId), eq(notifications.userId, me.userId), isNull(notifications.readAt)))
      .returning({ id: notifications.id }),
  );
  return updated.length;
}

/*
 * Lesson 4.2 (🟡): preferences.
 */

export type PreferenceCell = { enabled: boolean; locked: string | null };
export type PreferenceMatrix = {
  phoneNumber: string | null;
  rows: { category: Category; label: string; description: string; required: boolean; cells: Record<PersonalChannel, PreferenceCell> }[];
};

/** The matrix as the person will actually experience it (org policy and missing phone included). */
export async function getPreferenceMatrix(me: Me): Promise<PreferenceMatrix> {
  const [user] = await db.select({ phoneNumber: users.phoneNumber }).from(users).where(eq(users.id, me.userId));
  const [org] = await db.select({ plan: organizations.plan }).from(organizations).where(eq(organizations.id, me.orgId));
  const smsOnPlan = org ? smsIncluded(org.plan) : false;
  const { prefs, policy } = await withOrg(me.orgId, async (tx) => ({
    prefs: await tx
      .select()
      .from(notificationPreferences)
      .where(and(eq(notificationPreferences.organizationId, me.orgId), eq(notificationPreferences.userId, me.userId))),
    policy: await tx.select().from(orgNotificationPolicies).where(eq(orgNotificationPolicies.organizationId, me.orgId)),
  }));
  return {
    phoneNumber: user?.phoneNumber ?? null,
    rows: CATEGORY_IDS.map((category) => {
      const def = CATEGORIES[category];
      const orgPolicy = policy.filter((p) => p.category === category);
      // What resolves if the person has no phone problem: shows their choice even while SMS waits for a number.
      const on = resolvePersonalChannels({ category, userPrefs: prefs.filter((p) => p.category === category), orgPolicy, hasPhone: true });
      const cells = Object.fromEntries(
        PERSONAL_CHANNELS.map((channel) => {
          const orgOff = orgPolicy.some((p) => p.channel === channel && !p.enabled) && !def.required && channel !== 'in_app';
          const noSms = channel === 'sms' && !smsOnPlan && categoryUsesChannel(category, 'sms');
          const locked =
            lockedReason(category, channel) ??
            (noSms
              ? 'SMS alerts need a plan that includes SMS (Pro or Business)'
              : orgOff
                ? 'Turned off for this organization by an admin'
                : null);
          return [channel, { enabled: on.includes(channel) && !orgOff && !noSms, locked }];
        }),
      ) as Record<PersonalChannel, PreferenceCell>;
      return { category, label: def.label, description: def.description, required: def.required, cells };
    }),
  };
}

/**
 * Save the matrix from the form: a checkbox named "<category>:<channel>" per
 * cell. Locked cells are ignored (a hand-crafted POST cannot turn off a
 * required category). Unchecked boxes send nothing, so every editable cell
 * is written explicitly: true or false. `editable` limits the write to the
 * cells the form showed as changeable, so a cell disabled for now (SMS on a
 * plan without SMS, a channel the org switched off) keeps the person's choice.
 */
export async function savePreferences(me: Me, input: { checked: Set<string>; phoneNumber: string; editable?: Set<string> }) {
  const phone = input.phoneNumber.replace(/[\s()-]/g, '');
  if (phone && !isPhoneNumber(phone)) throw new InvalidRequestError('invalid_phone', 'Enter the phone number in international format, like +15551234567.');
  await db.update(users).set({ phoneNumber: phone || null }).where(eq(users.id, me.userId));
  const rows = CATEGORY_IDS.flatMap((category) =>
    PERSONAL_CHANNELS.filter((channel) => !lockedReason(category, channel) && (!input.editable || input.editable.has(`${category}:${channel}`))).map((channel) => ({
      organizationId: me.orgId,
      userId: me.userId,
      category,
      channel,
      enabled: input.checked.has(`${category}:${channel}`),
    })),
  );
  await withOrg(me.orgId, async (tx) => {
    for (const row of rows) {
      await tx
        .insert(notificationPreferences)
        .values(row)
        .onConflictDoUpdate({
          target: [notificationPreferences.organizationId, notificationPreferences.userId, notificationPreferences.category, notificationPreferences.channel],
          set: { enabled: row.enabled },
        });
    }
  });
}

/** One cell, e.g. from an unsubscribe link. Required categories cannot be turned off. */
export async function setPreference(me: Me, category: Category, channel: PersonalChannel, enabled: boolean): Promise<boolean> {
  if (lockedReason(category, channel)) return false;
  await withOrg(me.orgId, (tx) =>
    tx
      .insert(notificationPreferences)
      .values({ organizationId: me.orgId, userId: me.userId, category, channel, enabled })
      .onConflictDoUpdate({
        target: [notificationPreferences.organizationId, notificationPreferences.userId, notificationPreferences.category, notificationPreferences.channel],
        set: { enabled },
      }),
  );
  return true;
}

/*
 * Lesson 4.2 (🟡): the org layer. Owners and admins ("notification.manage")
 * can switch a channel off for everyone per category, and connect Slack.
 */

/** Channels the org policy can switch off: not in-app, and only for optional categories. */
export const ORG_POLICY_CHANNELS = ['email', 'sms', 'slack'] as const satisfies readonly Channel[];

export async function getOrgNotificationSettings({ orgId }: { orgId: string }) {
  const [org] = await db.select({ slackWebhookUrl: organizations.slackWebhookUrl }).from(organizations).where(eq(organizations.id, orgId));
  const policy = await withOrg(orgId, (tx) => tx.select().from(orgNotificationPolicies).where(eq(orgNotificationPolicies.organizationId, orgId)));
  return {
    // Never send the secret back to the browser: only whether it is set, and its ending.
    slack: org?.slackWebhookUrl ? { connected: true, hint: `…${org.slackWebhookUrl.slice(-6)}` } : { connected: false, hint: null },
    rows: CATEGORY_IDS.filter((c) => !CATEGORIES[c].required).map((category) => ({
      category,
      label: CATEGORIES[category].label,
      channels: Object.fromEntries(
        ORG_POLICY_CHANNELS.filter((ch) => categoryUsesChannel(category, ch)).map((channel) => [
          channel,
          !policy.some((p) => p.category === category && p.channel === channel && !p.enabled),
        ]),
      ) as Partial<Record<(typeof ORG_POLICY_CHANNELS)[number], boolean>>,
    })),
  };
}

export async function saveOrgNotificationSettings(
  { orgId }: { orgId: string },
  input: { allowed: Set<string>; slackWebhookUrl?: string | null },
) {
  if (input.slackWebhookUrl !== undefined) {
    const url = input.slackWebhookUrl?.trim() || null;
    if (url && !isSlackWebhookUrl(url)) {
      throw new InvalidRequestError('invalid_slack_url', 'Paste a Slack incoming-webhook URL: https://hooks.slack.com/services/…');
    }
    await db.update(organizations).set({ slackWebhookUrl: url }).where(eq(organizations.id, orgId));
  }
  const rows = CATEGORY_IDS.filter((c) => !CATEGORIES[c].required).flatMap((category) =>
    ORG_POLICY_CHANNELS.filter((ch) => categoryUsesChannel(category, ch)).map((channel) => ({
      organizationId: orgId,
      category,
      channel,
      enabled: input.allowed.has(`${category}:${channel}`),
    })),
  );
  await withOrg(orgId, async (tx) => {
    for (const row of rows) {
      await tx
        .insert(orgNotificationPolicies)
        .values(row)
        .onConflictDoUpdate({ target: [orgNotificationPolicies.organizationId, orgNotificationPolicies.category, orgNotificationPolicies.channel], set: { enabled: row.enabled } });
    }
  });
}
