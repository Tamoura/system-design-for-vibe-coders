'use server';

import { redirect } from 'next/navigation';
import { forPage, requirePermission } from '@/lib/access';
import { InvalidRequestError } from '@/lib/errors';
import { cancelOrgDeletion, requestOrgDeletion, requestOrgExport } from '@/lib/privacy/org-data';

// Lesson 8.1: each action checks its own permission (a server action is a public POST endpoint, lesson 1.3).

export async function requestExportAction(orgSlug: string) {
  const back = `/${orgSlug}/settings/data`;
  const ctx = await forPage(requirePermission(orgSlug, 'org.export'), back);
  await requestOrgExport(ctx);
  redirect(`${back}?export=requested`);
}

export async function requestDeletionAction(orgSlug: string, formData: FormData) {
  const back = `/${orgSlug}/settings/data`;
  const ctx = await forPage(requirePermission(orgSlug, 'org.delete'), back);
  try {
    await requestOrgDeletion(ctx, String(formData.get('confirmSlug') ?? ''));
  } catch (err) {
    if (err instanceof InvalidRequestError) redirect(`${back}?delete_error=${encodeURIComponent(err.message)}#delete`);
    throw err;
  }
  redirect(`${back}#delete`);
}

export async function cancelDeletionAction(orgSlug: string) {
  const back = `/${orgSlug}/settings/data`;
  const ctx = await forPage(requirePermission(orgSlug, 'org.delete'), back);
  await cancelOrgDeletion(ctx);
  redirect(`${back}#delete`);
}
