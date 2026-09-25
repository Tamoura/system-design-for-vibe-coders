'use server';

import { revalidatePath } from 'next/cache';
import { organizationNameInput } from '@/core/validation';
import { forPage, requirePermission } from '@/lib/access';
import { renameOrganization } from '@/lib/organizations';

export type RenameState = { error?: string; saved?: boolean; name?: string };

/**
 * Lesson 6.1 (🟡): rename the organization. A server action is a public POST
 * endpoint (lesson 1.3), so it checks "org.manage" itself: a Member who posts
 * this form by hand gets the 403 page, whatever the UI showed them.
 */
export async function renameOrgAction(orgSlug: string, _prev: RenameState, formData: FormData): Promise<RenameState> {
  const ctx = await forPage(requirePermission(orgSlug, 'org.manage'), `/${orgSlug}/settings/general`);
  const parsed = organizationNameInput.safeParse({ name: formData.get('name') });
  if (!parsed.success) return { error: parsed.error.issues[0]?.message, name: String(formData.get('name') ?? '') };
  await renameOrganization(ctx, parsed.data.name);
  revalidatePath(`/${ctx.orgSlug}`, 'layout'); // the sidebar shows the name too
  return { saved: true, name: parsed.data.name };
}
