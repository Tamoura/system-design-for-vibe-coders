'use server';

import { redirect } from 'next/navigation';
import { forPage, requirePermission } from '@/lib/access';
import { setStatusPagePublic } from '@/lib/organizations';

/** Lesson 1.3: publishing the status page needs "page.publish" (owners and admins). */
export async function setStatusPageAction(orgSlug: string, formData: FormData) {
  const ctx = await forPage(requirePermission(orgSlug, 'page.publish'), `/${orgSlug}/settings`);
  await setStatusPagePublic(ctx, formData.get('public') === 'on');
  redirect(`/${ctx.orgSlug}/settings`);
}
