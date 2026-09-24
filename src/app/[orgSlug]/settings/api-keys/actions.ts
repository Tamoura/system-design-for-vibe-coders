'use server';

import { revalidatePath } from 'next/cache';
import { forPage, requirePermission } from '@/lib/access';
import { createApiKey, createApiKeyInput, revokeApiKey } from '@/lib/api-keys';
import { getEntitlements } from '@/lib/entitlements';

export type CreateKeyState = { error?: string; created?: { name: string; key: string } };

/**
 * Lesson 5.2 (🟢): create a key. The full key is in this one response and
 * nowhere else: the page shows it once, the database only has its hash.
 */
export async function createApiKeyAction(orgSlug: string, _prev: CreateKeyState, formData: FormData): Promise<CreateKeyState> {
  const ctx = await forPage(requirePermission(orgSlug, 'integration.manage'), `/${orgSlug}/settings/api-keys`);
  if (!(await getEntitlements(ctx)).api) return { error: 'Your plan does not include the API.' };
  const parsed = createApiKeyInput.safeParse({ name: formData.get('name'), scopes: formData.getAll('scopes') });
  if (!parsed.success) return { error: parsed.error.issues[0]?.message ?? 'Invalid input' };
  const { key } = await forPage(createApiKey(ctx, parsed.data), `/${orgSlug}/settings/api-keys`);
  revalidatePath(`/${ctx.orgSlug}/settings/api-keys`);
  return { created: { name: parsed.data.name, key } };
}

export async function revokeApiKeyAction(orgSlug: string, keyId: string) {
  const ctx = await forPage(requirePermission(orgSlug, 'integration.manage'), `/${orgSlug}/settings/api-keys`);
  await forPage(revokeApiKey(ctx, keyId), `/${orgSlug}/settings/api-keys`);
  revalidatePath(`/${ctx.orgSlug}/settings/api-keys`);
}
