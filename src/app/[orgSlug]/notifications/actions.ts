'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { forPage, requirePermission } from '@/lib/access';
import { InvalidRequestError } from '@/lib/errors';
import { markAllNotificationsRead, markNotificationsRead, saveOrgNotificationSettings, savePreferences } from '@/lib/notifications';

/*
 * Lesson 4.2. The inbox and preferences are personal: any member may use
 * them ("monitor.read" is every role), and every query is scoped to the org
 * AND the signed-in user. The org policy needs "notification.manage".
 */

export async function markReadAction(orgSlug: string, notificationId: string) {
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.read'), `/${orgSlug}/notifications`);
  await markNotificationsRead(ctx, [notificationId]);
  revalidatePath(`/${ctx.orgSlug}`, 'layout'); // the bell's count is in the layout
}

export async function markAllReadAction(orgSlug: string) {
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.read'), `/${orgSlug}/notifications`);
  await markAllNotificationsRead(ctx);
  revalidatePath(`/${ctx.orgSlug}`, 'layout');
}

export type PrefsState = { saved?: boolean; error?: string };

export async function savePreferencesAction(orgSlug: string, _prev: PrefsState, formData: FormData): Promise<PrefsState> {
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.read'), `/${orgSlug}/notifications/preferences`);
  const checked = new Set([...formData.keys()].filter((k) => k.includes(':')));
  try {
    await savePreferences(ctx, { checked, phoneNumber: String(formData.get('phoneNumber') ?? '') });
  } catch (err) {
    if (err instanceof InvalidRequestError) return { error: err.message };
    throw err;
  }
  revalidatePath(`/${ctx.orgSlug}/notifications/preferences`);
  return { saved: true };
}

export async function saveOrgNotificationsAction(orgSlug: string, _prev: PrefsState, formData: FormData): Promise<PrefsState> {
  const ctx = await forPage(requirePermission(orgSlug, 'notification.manage'), `/${orgSlug}/settings`);
  const allowed = new Set([...formData.keys()].filter((k) => k.includes(':')));
  const slack = formData.get('slackWebhookUrl');
  const removeSlack = formData.get('removeSlack') === 'on';
  try {
    await saveOrgNotificationSettings(ctx, {
      allowed,
      // Empty field = keep the current URL (we never show it back); the checkbox removes it.
      slackWebhookUrl: removeSlack ? null : typeof slack === 'string' && slack.trim() ? slack : undefined,
    });
  } catch (err) {
    if (err instanceof InvalidRequestError) return { error: err.message };
    throw err;
  }
  revalidatePath(`/${ctx.orgSlug}/settings`);
  return { saved: true };
}

export async function goToNotification(orgSlug: string, notificationId: string, url: string) {
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.read'), `/${orgSlug}/notifications`);
  await markNotificationsRead(ctx, [notificationId]);
  // Only paths inside this org: the stored url is always one, but never redirect elsewhere.
  redirect(url.startsWith(`/${ctx.orgSlug}/`) ? url : `/${ctx.orgSlug}/notifications`);
}
