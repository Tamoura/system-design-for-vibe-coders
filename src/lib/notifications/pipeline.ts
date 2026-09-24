import { and, eq, inArray, isNotNull } from 'drizzle-orm';
import { schema } from '@/db';
import type { TenantTx } from '@/db/tenant';
import { CATEGORIES, orgWantsSlack, resolvePersonalChannels, type Category } from '@/core/notifications';
import { can } from '@/core/permissions';
import { entitlementsFor, type PlanId } from '@/core/plans';
import type { TemplateName, TemplateProps } from '@/emails';
import { appUrl, unsubscribeLinks } from '../urls';

const { organizations, memberships, users, notifications, notificationPreferences, orgNotificationPolicies, notificationDeliveries, statusPageSubscribers } =
  schema;

/**
 * An email to send for this event: a template and its props. The pipeline
 * adds `url` (the event's link) and, per recipient, the unsubscribe link.
 */
export type EmailSpec = { [N in TemplateName]: { template: N; props: Omit<TemplateProps<N>, 'unsubscribeUrl' | 'url'> } }[TemplateName];

/**
 * Lesson 4.2: one domain event, described once. Domain code (the check
 * runner, billing) builds it with the helpers in ./events.ts and hands it to
 * notify(); it never picks recipients or channels itself.
 */
export type NotifyEvent = {
  orgId: string;
  category: Category;
  /** What happened, exactly once: "incident.opened:<incident id>". Every dedupe key starts with it. */
  key: string;
  /** For the inbox, SMS and Slack. */
  title: string;
  body: string;
  /** A path inside Beacon, e.g. /acme/monitors/<id>. */
  path: string;
  monitorId?: string;
  email: EmailSpec;
  /** Incidents only: also tell the org's confirmed status-page subscribers (if the page is public). */
  statusPage?: { monitorName: string; state: 'opened' | 'resolved'; at: string };
};

/** What a delivery row carries to its channel worker. */
export type DeliveryPayload = {
  orgName: string;
  title: string;
  body: string;
  url: string;
  email?: { template: TemplateName; props: Record<string, unknown> };
  listUnsubscribe?: string | null;
};

type NewDelivery = typeof notificationDeliveries.$inferInsert & { payload: DeliveryPayload };

/**
 * Lesson 4.2 (🟢/🟡): the pipeline, inside the caller's transaction.
 *
 *   1. recipients   members whose role has the category's permission (1.3)
 *   2. dedupe       one notification per event per person (unique dedupe_key):
 *                   calling this twice for the same event adds nothing
 *   3. preferences  required → org policy → the person's choice → default
 *   4. deliveries   one row per channel: in-app is written as delivered;
 *                   email and SMS are queued for their channel workers;
 *                   the org's Slack channel and status-page subscribers too
 *
 * Only database writes happen here. Running inside the transaction that
 * opened the incident means both commit together: no incident without its
 * notifications, no notification for an incident that rolled back. The
 * sending happens after the commit (./deliver.ts).
 */
export async function notifyInTx(tx: TenantTx, event: NotifyEvent): Promise<{ notified: number; deliveries: number }> {
  const def = CATEGORIES[event.category];
  const [org] = await tx
    .select({
      name: organizations.name,
      slug: organizations.slug,
      plan: organizations.plan,
      slackWebhookUrl: organizations.slackWebhookUrl,
      statusPagePublic: organizations.statusPagePublic,
    })
    .from(organizations)
    .where(eq(organizations.id, event.orgId));
  if (!org) return { notified: 0, deliveries: 0 };

  // 1. Who may know about this at all: the permission map decides, not a role name.
  const members = await tx
    .select({ userId: users.id, email: users.email, phone: users.phoneNumber, role: memberships.role })
    .from(memberships)
    .innerJoin(users, eq(users.id, memberships.userId))
    .where(eq(memberships.organizationId, event.orgId));
  const eligible = members.filter((m) => can(m.role, def.permission));

  const prefs = eligible.length
    ? await tx
        .select()
        .from(notificationPreferences)
        .where(
          and(
            eq(notificationPreferences.organizationId, event.orgId),
            eq(notificationPreferences.category, event.category),
            inArray(notificationPreferences.userId, eligible.map((m) => m.userId)),
          ),
        )
    : [];
  const policy = await tx
    .select({ channel: orgNotificationPolicies.channel, enabled: orgNotificationPolicies.enabled })
    .from(orgNotificationPolicies)
    .where(and(eq(orgNotificationPolicies.organizationId, event.orgId), eq(orgNotificationPolicies.category, event.category)));
  // Lesson 3.2 meets 4.2: SMS costs money, so it is an entitlement. A plan
  // with no SMS included (Free) has no subscription to bill them to: off.
  if (!smsIncluded(org.plan)) policy.push({ channel: 'sms', enabled: false });

  const base = { orgName: org.name, title: event.title, body: event.body, url: appUrl(event.path) };
  const deliveries: NewDelivery[] = [];
  let notified = 0;

  for (const m of eligible) {
    // 2. Dedupe: the unique key makes a repeated call a no-op for this person.
    const [created] = await tx
      .insert(notifications)
      .values({
        organizationId: event.orgId,
        userId: m.userId,
        category: event.category,
        dedupeKey: `${event.key}:${m.userId}`,
        title: event.title,
        body: event.body,
        url: event.path,
        monitorId: event.monitorId ?? null,
      })
      .onConflictDoNothing({ target: notifications.dedupeKey })
      .returning({ id: notifications.id });
    if (!created) continue;
    notified++;

    // 3. Preferences, in the lesson's order (src/core/notifications.ts).
    const channels = resolvePersonalChannels({
      category: event.category,
      userPrefs: prefs.filter((p) => p.userId === m.userId),
      orgPolicy: policy,
      hasPhone: Boolean(m.phone),
    });

    // 4. One delivery per channel.
    const row = { organizationId: event.orgId, notificationId: created.id, userId: m.userId };
    for (const channel of channels) {
      const dedupeKey = `${event.key}:${m.userId}:${channel}`;
      if (channel === 'in_app') {
        // The inbox row IS the in-app delivery; it is logged like the others.
        deliveries.push({ ...row, channel, dedupeKey, recipient: m.userId, payload: base, status: 'sent', sentAt: new Date(), providerMessageId: created.id });
      } else if (channel === 'email') {
        // Optional categories carry a per-person, per-category unsubscribe link (no login needed).
        const links = def.required ? null : unsubscribeLinks({ kind: 'unsubscribe-category', orgId: event.orgId, userId: m.userId, category: event.category });
        const props = { ...event.email.props, url: base.url, ...(links && { unsubscribeUrl: links.page }) };
        deliveries.push({ ...row, channel, dedupeKey, recipient: m.email, payload: { ...base, email: { template: event.email.template, props }, listUnsubscribe: links?.oneClick ?? null } });
      } else if (channel === 'sms' && m.phone) {
        deliveries.push({ ...row, channel, dedupeKey, recipient: m.phone, payload: base });
      }
    }
  }

  // The org's Slack channel: once per event, not once per person.
  if (orgWantsSlack(event.category, policy, Boolean(org.slackWebhookUrl))) {
    deliveries.push({ organizationId: event.orgId, channel: 'slack', dedupeKey: `${event.key}:slack`, recipient: 'slack', payload: base });
  }

  // Status-page subscribers: confirmed ones only (double opt-in), from the separate status stream.
  if (event.statusPage && org.statusPagePublic) {
    const subscribers = await tx
      .select({ id: statusPageSubscribers.id, email: statusPageSubscribers.email })
      .from(statusPageSubscribers)
      .where(and(eq(statusPageSubscribers.organizationId, event.orgId), isNotNull(statusPageSubscribers.confirmedAt)));
    const statusUrl = appUrl(`/status/${org.slug}`);
    for (const s of subscribers) {
      const links = unsubscribeLinks({ kind: 'subscriber-unsubscribe', orgId: event.orgId, subscriberId: s.id });
      deliveries.push({
        organizationId: event.orgId,
        subscriberId: s.id,
        channel: 'email',
        dedupeKey: `${event.key}:subscriber:${s.id}`,
        recipient: s.email,
        payload: {
          ...base,
          url: statusUrl,
          email: { template: 'status-update', props: { orgName: org.name, ...event.statusPage, url: statusUrl, unsubscribeUrl: links.page } },
          listUnsubscribe: links.oneClick,
        },
      });
    }
  }

  // TODO(4.2 🔴): a status page with 50,000 subscribers needs batched, throttled fan-out on its own stream.
  for (let i = 0; i < deliveries.length; i += 500) {
    await tx.insert(notificationDeliveries).values(deliveries.slice(i, i + 500)).onConflictDoNothing({ target: notificationDeliveries.dedupeKey });
  }
  return { notified, deliveries: deliveries.length };
}

/** Does the plan include SMS alerts at all? (Free: 0 included, and nothing to bill overage to.) */
export function smsIncluded(plan: PlanId): boolean {
  return entitlementsFor(plan).smsCreditsPerMonth > 0;
}
