'use server';

import { redirect } from 'next/navigation';
import { createMonitorInput } from '@/core/validation';
import { forPage, requireMembership } from '@/lib/access';
import { createMonitor } from '@/lib/monitors';

export type FormState = { errors?: Record<string, string[] | undefined>; values?: Record<string, string> };

export async function createMonitorAction(orgSlug: string, _prev: FormState, formData: FormData): Promise<FormState> {
  // A server action is a public POST endpoint: check access here, not only on the page.
  const ctx = await forPage(requireMembership(orgSlug), `/${orgSlug}/monitors/new`);
  const values = Object.fromEntries(formData.entries()) as Record<string, string>;
  const parsed = createMonitorInput.safeParse(values);
  if (!parsed.success) {
    return { errors: parsed.error.flatten().fieldErrors, values };
  }
  await createMonitor(ctx, parsed.data);
  redirect(`/${ctx.orgSlug}/monitors`);
}
