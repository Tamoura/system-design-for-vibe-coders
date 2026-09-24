'use server';

import { redirect } from 'next/navigation';
import { createMonitorInput } from '@/core/validation';
import { forPage, requirePermission } from '@/lib/access';
import { InvalidRequestError, LimitExceededError } from '@/lib/errors';
import { createMonitor } from '@/lib/monitors';

export type FormState = { errors?: Record<string, string[] | undefined>; values?: Record<string, string> };

export async function createMonitorAction(orgSlug: string, _prev: FormState, formData: FormData): Promise<FormState> {
  // Lesson 1.3: a server action is a public POST endpoint. Check the permission
  // here, before any work, not only on the page that shows the form.
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.write'), `/${orgSlug}/monitors/new`);
  const values = Object.fromEntries(formData.entries()) as Record<string, string>;
  const parsed = createMonitorInput.safeParse(values);
  if (!parsed.success) {
    return { errors: parsed.error.flatten().fieldErrors, values };
  }
  try {
    await createMonitor(ctx, parsed.data);
  } catch (err) {
    // Lesson 3.2: the plan's limit, enforced on the server; show its message in the form.
    if (err instanceof LimitExceededError) return { errors: { form: [err.message] }, values };
    // Lesson 5.3: a URL inside our network (SSRF guard).
    if (err instanceof InvalidRequestError) return { errors: { url: [err.message] }, values };
    throw err;
  }
  redirect(`/${ctx.orgSlug}/monitors`);
}
