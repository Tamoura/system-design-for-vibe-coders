'use server';

import { redirect } from 'next/navigation';
import { incidentUpdateInput, updateMonitorInput } from '@/core/validation';
import { forPage, requirePermission } from '@/lib/access';
import { acknowledgeIncident, deleteMonitor, resolveIncident, updateMonitor } from '@/lib/monitors';
import { addIncidentUpdate } from '@/lib/incidents';
import { InvalidRequestError, LimitExceededError } from '@/lib/errors';

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
  try {
    await forPage(updateMonitor(ctx, monitorId, parsed.data), back);
  } catch (err) {
    // Lesson 3.2: a plan limit (interval too short, no free running slot).
    if (err instanceof LimitExceededError) return { errors: { form: [err.message] } };
    if (err instanceof InvalidRequestError) return { errors: { url: [err.message] } }; // lesson 5.3: SSRF guard
    throw err;
  }
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

/** Lesson 5.4 (🟡): acknowledge an incident; its escalation stops within seconds. */
export async function acknowledgeIncidentAction(orgSlug: string, monitorId: string, incidentId: string) {
  const ctx = await forPage(requirePermission(orgSlug, 'incident.write'), `/${orgSlug}/monitors/${monitorId}`);
  await acknowledgeIncident(ctx, incidentId);
  redirect(`/${ctx.orgSlug}/monitors/${monitorId}#incident-${incidentId}`);
}

/** Lesson 2.3: post an incident update (the text full-text search finds). */
export async function addIncidentUpdateAction(orgSlug: string, monitorId: string, incidentId: string, formData: FormData) {
  const back = `/${orgSlug}/monitors/${monitorId}`;
  const ctx = await forPage(requirePermission(orgSlug, 'incident.write'), back);
  const parsed = incidentUpdateInput.safeParse({ body: formData.get('body') });
  if (parsed.success) await forPage(addIncidentUpdate(ctx, incidentId, parsed.data.body), back);
  redirect(`/${ctx.orgSlug}/monitors/${monitorId}#incident-${incidentId}`);
}
