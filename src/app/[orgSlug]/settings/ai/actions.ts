'use server';

import { redirect } from 'next/navigation';
import { forPage, requirePermission } from '@/lib/access';
import { LimitExceededError } from '@/lib/errors';
import { setAiSummariesEnabled } from '@/lib/ai/incident-summary';

/** Lesson 8.2: the org's AI opt-in. "org.manage" (owners, admins), checked here, on the server. */
export async function setAiSummariesAction(orgSlug: string, enabled: boolean) {
  const back = `/${orgSlug}/settings/ai`;
  const ctx = await forPage(requirePermission(orgSlug, 'org.manage'), back);
  try {
    await setAiSummariesEnabled(ctx, enabled);
  } catch (err) {
    if (err instanceof LimitExceededError) redirect(`${back}?error=${encodeURIComponent(err.message)}`);
    throw err;
  }
  redirect(back);
}
