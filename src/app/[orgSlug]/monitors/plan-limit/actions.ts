'use server';

import { redirect } from 'next/navigation';
import { forPage, requirePermission } from '@/lib/access';
import { chooseRunningMonitors } from '@/lib/entitlements';
import { LimitExceededError } from '@/lib/errors';

/** Lesson 3.2 (🟡): the owner picks which monitors keep running after a downgrade. */
export async function chooseRunningAction(orgSlug: string, formData: FormData) {
  const back = `/${orgSlug}/monitors/plan-limit`;
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.write_any'), back);
  const keep = formData.getAll('keep').map(String);
  try {
    await chooseRunningMonitors(ctx, keep);
  } catch (err) {
    if (err instanceof LimitExceededError) redirect(`${back}?error=too_many`);
    throw err;
  }
  redirect(`/${ctx.orgSlug}/monitors`);
}
