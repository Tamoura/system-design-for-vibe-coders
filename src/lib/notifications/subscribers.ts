import { and, count, eq, gt, isNull } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { CATEGORIES, isCategory } from '@/core/notifications';
import { sendEmail } from '../email';
import { findPublicStatusPage } from '../organizations';
import { appUrl, readLink, signLink } from '../urls';
import { setPreference } from './index';

const { organizations, statusPageSubscribers } = schema;

/*
 * Lesson 4.2 (🟡): status-page subscribers, and every link that works
 * without logging in.
 *
 *   subscribe (public form) ─► pending row + "confirm" email ─► confirm (button) ─► confirmed
 *   every update email ─► unsubscribe link / one-click header ─► row deleted
 */

/** At most this many confirmation emails per status page per hour: the form must not become a way to spam strangers. */
const CONFIRMATIONS_PER_HOUR = 30;
/** And at most one per address per 10 minutes. */
const RESEND_AFTER_MS = 10 * 60_000;

/**
 * Double opt-in: typing an address subscribes nobody. It creates a pending
 * row and emails a confirmation link to that address. The answer is the same
 * whether the address is new, pending or already confirmed, so the form does
 * not reveal who is subscribed.
 */
export async function subscribeToStatusPage(slug: string, rawEmail: string): Promise<'check_inbox' | 'not_found'> {
  const org = await findPublicStatusPage(slug);
  if (!org) return 'not_found';
  const email = rawEmail.trim().toLowerCase();
  const now = new Date();

  const toConfirm = await withOrg(org.id, async (tx) => {
    const [recent] = await tx
      .select({ n: count() })
      .from(statusPageSubscribers)
      .where(and(eq(statusPageSubscribers.organizationId, org.id), gt(statusPageSubscribers.confirmationSentAt, new Date(now.getTime() - 3600_000))));
    if (recent.n >= CONFIRMATIONS_PER_HOUR) return null;

    await tx.insert(statusPageSubscribers).values({ organizationId: org.id, email }).onConflictDoNothing();
    const [row] = await tx
      .select()
      .from(statusPageSubscribers)
      .where(and(eq(statusPageSubscribers.organizationId, org.id), eq(statusPageSubscribers.email, email)));
    if (row.confirmedAt) return null; // already subscribed: nothing to send
    if (row.confirmationSentAt && now.getTime() - row.confirmationSentAt.getTime() < RESEND_AFTER_MS) return null;
    await tx.update(statusPageSubscribers).set({ confirmationSentAt: now }).where(eq(statusPageSubscribers.id, row.id));
    return row;
  });

  if (toConfirm) {
    const token = signLink({ kind: 'subscriber-confirm', orgId: org.id, subscriberId: toConfirm.id });
    await sendEmail({
      to: email,
      template: 'confirm-subscription',
      props: { orgName: org.name, url: appUrl(`/status/${slug}/confirm?token=${encodeURIComponent(token)}`) },
      idempotencyKey: `subscribe:${toConfirm.id}:${now.getTime()}`,
    });
  }
  return 'check_inbox';
}

type LinkOutcome =
  | { ok: true; message: string; orgSlug: string }
  | { ok: false; message: string };

/** For the confirm page: what the link would do, without doing it (scanners open links too). */
export async function describeLink(token: string): Promise<LinkOutcome & { action?: string }> {
  const link = readLink(token);
  if (!link) return { ok: false, message: 'This link is not valid. It may have been cut off when copying.' };
  const [org] = await db.select({ name: organizations.name, slug: organizations.slug }).from(organizations).where(eq(organizations.id, link.orgId));
  if (!org) return { ok: false, message: 'This organization no longer exists.' };
  switch (link.kind) {
    case 'subscriber-confirm':
      return { ok: true, orgSlug: org.slug, message: `Get an email when ${org.name} has an incident, and when it is resolved.`, action: 'Confirm subscription' };
    case 'subscriber-unsubscribe':
      return { ok: true, orgSlug: org.slug, message: `Stop status emails from ${org.name}.`, action: 'Unsubscribe' };
    case 'unsubscribe-category': {
      const label = isCategory(link.category) ? CATEGORIES[link.category].label.toLowerCase() : link.category;
      return { ok: true, orgSlug: org.slug, message: `Stop “${label}” emails from ${org.name}. In-app notifications continue.`, action: 'Unsubscribe' };
    }
  }
}

/** Confirm a pending subscription (a POST from the confirm page). */
export async function confirmSubscription(token: string): Promise<LinkOutcome> {
  const link = readLink(token);
  if (!link || link.kind !== 'subscriber-confirm') return { ok: false, message: 'This confirmation link is not valid.' };
  const confirmed = await withOrg(link.orgId, (tx) =>
    tx
      .update(statusPageSubscribers)
      .set({ confirmedAt: new Date() })
      .where(and(eq(statusPageSubscribers.organizationId, link.orgId), eq(statusPageSubscribers.id, link.subscriberId), isNull(statusPageSubscribers.confirmedAt)))
      .returning({ id: statusPageSubscribers.id }),
  );
  const [org] = await db.select({ name: organizations.name, slug: organizations.slug }).from(organizations).where(eq(organizations.id, link.orgId));
  if (!org) return { ok: false, message: 'This organization no longer exists.' };
  // Confirming twice is fine; confirming a subscription that was since removed is not.
  const [still] = await withOrg(link.orgId, (tx) =>
    tx.select({ id: statusPageSubscribers.id }).from(statusPageSubscribers).where(and(eq(statusPageSubscribers.organizationId, link.orgId), eq(statusPageSubscribers.id, link.subscriberId))),
  );
  if (!confirmed.length && !still) return { ok: false, message: 'This subscription no longer exists. Subscribe again on the status page.' };
  return { ok: true, orgSlug: org.slug, message: `You are subscribed to ${org.name} status updates.` };
}

/**
 * Unsubscribe with a signed link: a status-page subscriber is removed; a
 * member's "email me about this category" is switched off (required
 * categories cannot be). Used by the /unsubscribe page and by the RFC 8058
 * one-click POST. Idempotent: a second click says the same thing.
 */
export async function unsubscribeWithToken(token: string): Promise<LinkOutcome> {
  const link = readLink(token);
  if (!link) return { ok: false, message: 'This unsubscribe link is not valid.' };
  const [org] = await db.select({ name: organizations.name, slug: organizations.slug }).from(organizations).where(eq(organizations.id, link.orgId));
  if (!org) return { ok: false, message: 'This organization no longer exists.' };
  if (link.kind === 'subscriber-unsubscribe') {
    await withOrg(link.orgId, (tx) =>
      tx.delete(statusPageSubscribers).where(and(eq(statusPageSubscribers.organizationId, link.orgId), eq(statusPageSubscribers.id, link.subscriberId))),
    );
    return { ok: true, orgSlug: org.slug, message: `You will no longer get status emails from ${org.name}.` };
  }
  if (link.kind === 'unsubscribe-category' && isCategory(link.category)) {
    const done = await setPreference({ orgId: link.orgId, userId: link.userId }, link.category, 'email', false);
    if (!done) return { ok: false, message: 'This kind of email cannot be turned off.' };
    return { ok: true, orgSlug: org.slug, message: `You will no longer get “${CATEGORIES[link.category].label.toLowerCase()}” emails from ${org.name}. Change this any time in your notification preferences.` };
  }
  return { ok: false, message: 'This unsubscribe link is not valid.' };
}
