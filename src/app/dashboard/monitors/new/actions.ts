'use server';

import { redirect } from 'next/navigation';
import { createMonitorInput } from '@/core/validation';
import { createMonitor } from '@/lib/monitors';

export type FormState = { errors?: Record<string, string[] | undefined>; values?: Record<string, string> };

export async function createMonitorAction(_prev: FormState, formData: FormData): Promise<FormState> {
  const values = Object.fromEntries(formData.entries()) as Record<string, string>;
  const parsed = createMonitorInput.safeParse(values);
  if (!parsed.success) {
    return { errors: parsed.error.flatten().fieldErrors, values };
  }
  await createMonitor(parsed.data);
  redirect('/dashboard');
}
