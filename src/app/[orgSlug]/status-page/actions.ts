'use server';

import { redirect } from 'next/navigation';
import { forPage, requirePermission } from '@/lib/access';
import { setStatusPagePublic } from '@/lib/organizations';

/** Lesson 1.3: publishing the status page needs "page.publish" (owners and admins). Lesson 6.1: the last onboarding step. */
export async function setStatusPageAction(orgSlug: string, formData: FormData) {
  const ctx = await forPage(requirePermission(orgSlug, 'page.publish'), `/${orgSlug}/status-page`);
  await setStatusPagePublic(ctx, formData.get('public') === 'on');
  redirect(`/${ctx.orgSlug}/status-page?saved=1`);
}
