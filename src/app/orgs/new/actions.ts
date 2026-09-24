'use server';

import { redirect } from 'next/navigation';
import { createOrganizationInput } from '@/core/validation';
import { createOrganization } from '@/lib/organizations';
import { requireUser } from '@/lib/session';

export type NewOrgState = { error?: string; name?: string };

/** Lesson 1.2: any signed-in user may create an organization, and becomes its owner. */
export async function createOrganizationAction(_prev: NewOrgState, formData: FormData): Promise<NewOrgState> {
  const user = await requireUser('/orgs/new');
  const parsed = createOrganizationInput.safeParse({ name: formData.get('name') });
  if (!parsed.success) return { error: parsed.error.issues[0]?.message, name: String(formData.get('name') ?? '') };
  const org = await createOrganization(user.id, parsed.data.name);
  redirect(`/${org.slug}/monitors`);
}
