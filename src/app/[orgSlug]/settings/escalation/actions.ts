'use server';

import { redirect } from 'next/navigation';
import { ESCALATION_CHANNELS, MAX_TIERS } from '@/core/escalation';
import { forPage, requirePermission } from '@/lib/access';
import { InvalidRequestError } from '@/lib/errors';
import { saveEscalationPolicy } from '@/lib/workflows';

/**
 * Lesson 5.4 (🟡): save the escalation policy (data, not code). A tier with
 * nobody ticked is left out. Incidents already escalating keep the policy
 * they started with; this one applies from the next incident.
 */
export async function saveEscalationAction(orgSlug: string, formData: FormData) {
  const back = `/${orgSlug}/settings/escalation`;
  const ctx = await forPage(requirePermission(orgSlug, 'notification.manage'), back);
  const tiers = [];
  for (let i = 0; i < MAX_TIERS; i++) {
    const userIds = formData.getAll(`tier${i}.users`).map(String);
    if (userIds.length === 0) continue;
    const channels = formData.getAll(`tier${i}.channels`).map(String).filter((c) => (ESCALATION_CHANNELS as readonly string[]).includes(c));
    tiers.push({ userIds, channels, waitMinutes: Number(formData.get(`tier${i}.wait`) ?? 5) });
  }
  try {
    await saveEscalationPolicy(ctx, { tiers: tiers as never });
  } catch (err) {
    const message = err instanceof InvalidRequestError ? err.message : err instanceof Error && 'issues' in err ? 'Each tier needs at least one channel and a wait of 1 to 1440 minutes.' : null;
    if (message) redirect(`${back}?error=${encodeURIComponent(message)}`);
    throw err;
  }
  redirect(`${back}?saved=1`);
}
