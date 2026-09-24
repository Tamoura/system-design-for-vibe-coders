'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { forPage, requirePermission } from '@/lib/access';
import { InvalidRequestError } from '@/lib/errors';
import { createEndpoint, createEndpointInput, deleteEndpoint, replayFailedSince, resendMessage, setEndpointEnabled } from '@/lib/webhooks';

/*
 * Lesson 5.3: webhook endpoints and their delivery log. Every action checks
 * "integration.manage" itself (a server action is a public POST endpoint),
 * and the lib functions put the org from that check into every query.
 */
const back = (orgSlug: string, id?: string) => `/${orgSlug}/settings/webhooks${id ? `/${id}` : ''}`;
const manager = (orgSlug: string, id?: string) => forPage(requirePermission(orgSlug, 'integration.manage'), back(orgSlug, id));

export type CreateEndpointState = { error?: string; created?: { id: string; url: string; secret: string } };

export async function createEndpointAction(orgSlug: string, _prev: CreateEndpointState, formData: FormData): Promise<CreateEndpointState> {
  const ctx = await manager(orgSlug);
  const parsed = createEndpointInput.safeParse({ url: formData.get('url'), description: formData.get('description') || undefined, eventTypes: formData.getAll('eventTypes') });
  if (!parsed.success) return { error: parsed.error.issues[0]?.message ?? 'Invalid input' };
  try {
    const { id, secret } = await createEndpoint(ctx, parsed.data);
    revalidatePath(back(ctx.orgSlug));
    return { created: { id, url: parsed.data.url, secret } };
  } catch (err) {
    // Lesson 5.3 (🟡): an internal address (SSRF), a port other than 80/443, a host that does not resolve.
    if (err instanceof InvalidRequestError) return { error: err.message };
    throw err;
  }
}

export async function setEndpointEnabledAction(orgSlug: string, id: string, enabled: boolean) {
  const ctx = await manager(orgSlug, id);
  await forPage(setEndpointEnabled(ctx, id, enabled), back(orgSlug, id));
  revalidatePath(back(ctx.orgSlug, id));
}

export async function deleteEndpointAction(orgSlug: string, id: string) {
  const ctx = await manager(orgSlug, id);
  await forPage(deleteEndpoint(ctx, id), back(orgSlug, id));
  redirect(back(ctx.orgSlug));
}

export async function resendMessageAction(orgSlug: string, endpointId: string, messageId: string) {
  const ctx = await manager(orgSlug, endpointId);
  await forPage(resendMessage(ctx, endpointId, messageId), back(orgSlug, endpointId));
  redirect(`${back(ctx.orgSlug, endpointId)}?resent=1`);
}

/**
 * "Replay failed since…". The form sends the browser's local date-time
 * ("2026-09-23T22:00") and its UTC offset in minutes; together they are one
 * instant, whatever the server's time zone. Default: 24 hours ago.
 */
export async function replayFailedAction(orgSlug: string, endpointId: string, formData: FormData) {
  const ctx = await manager(orgSlug, endpointId);
  const local = Date.parse(`${String(formData.get('since') ?? '')}:00Z`); // as if it were UTC…
  const offsetMin = Number(formData.get('tzOffsetMinutes') ?? 0) || 0; // …then shift by the browser's offset
  const since = Number.isNaN(local) ? new Date(Date.now() - 24 * 3600_000) : new Date(local + offsetMin * 60_000);
  const n = await forPage(replayFailedSince(ctx, endpointId, since), back(orgSlug, endpointId));
  redirect(`${back(ctx.orgSlug, endpointId)}?replayed=${n}`);
}
