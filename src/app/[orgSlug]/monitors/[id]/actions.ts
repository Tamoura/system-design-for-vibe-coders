'use server';

import { redirect } from 'next/navigation';
import { updateMonitorInput } from '@/core/validation';
import { forPage, requirePermission } from '@/lib/access';
import { deleteMonitor, resolveIncident, updateMonitor } from '@/lib/monitors';

// Lesson 1.3: each action checks its own permission before doing any work,
// then passes the org from that check (never from the form) to the query.
// updateMonitor/deleteMonitor add the object-level and ABAC checks.

export type EditState = { errors?: Record<string, string[] | undefined>; saved?: boolean };

export async function updateMonitorAction(orgSlug: string, monitorId: string, _prev: EditState, formData: FormData): Promise<EditState> {
  const back = `/${orgSlug}/monitors/${monitorId}`;
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.write'), back);
  const parsed = updateMonitorInput.safeParse({
    name: formData.get('name'),
    url: formData.get('url'),
    intervalSeconds: formData.get('intervalSeconds'),
    paused: formData.get('paused') === 'on',
  });
  if (!parsed.success) return { errors: parsed.error.flatten().fieldErrors };
  await forPage(updateMonitor(ctx, monitorId, parsed.data), back);
  return { saved: true };
}

export async function deleteMonitorAction(orgSlug: string, monitorId: string) {
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.write'), `/${orgSlug}/monitors`);
  await forPage(deleteMonitor(ctx, monitorId), `/${orgSlug}/monitors`);
  redirect(`/${ctx.orgSlug}/monitors`);
}

export async function resolveIncidentAction(orgSlug: string, monitorId: string, incidentId: string) {
  const ctx = await forPage(requirePermission(orgSlug, 'incident.write'), `/${orgSlug}/monitors/${monitorId}`);
  await resolveIncident(ctx, incidentId);
  redirect(`/${ctx.orgSlug}/monitors/${monitorId}`);
}
