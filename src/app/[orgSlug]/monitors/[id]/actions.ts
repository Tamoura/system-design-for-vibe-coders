'use server';

import { redirect } from 'next/navigation';
import { forPage, requirePermission } from '@/lib/access';
import { deleteMonitor, resolveIncident } from '@/lib/monitors';

// Lesson 1.3: each action checks its own permission before doing any work,
// then passes the org from that check (never from the form) to the query.

export async function deleteMonitorAction(orgSlug: string, monitorId: string) {
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.write'), `/${orgSlug}/monitors`);
  await deleteMonitor(ctx, monitorId);
  redirect(`/${ctx.orgSlug}/monitors`);
}

export async function resolveIncidentAction(orgSlug: string, monitorId: string, incidentId: string) {
  const ctx = await forPage(requirePermission(orgSlug, 'incident.write'), `/${orgSlug}/monitors/${monitorId}`);
  await resolveIncident(ctx, incidentId);
  redirect(`/${ctx.orgSlug}/monitors/${monitorId}`);
}
