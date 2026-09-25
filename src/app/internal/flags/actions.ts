'use server';

import { revalidatePath } from 'next/cache';
import { refreshFlags } from '@/lib/flags';
import { FlagInputError, deleteStaleFlag, setFlagOverride, setFlagRule } from '@/lib/flags/store';
import { requireStaff } from '@/lib/staff';

export type FlagFormState = { error?: string; saved?: string };

/*
 * Lesson 6.3: flip flags without a deploy. Every action checks the staff
 * session itself (a server action is a public POST endpoint), then reloads
 * this process's rules at once; other processes (the worker) follow within
 * FLAGS_REFRESH_SECONDS. TODO(7.3): record each change in the audit log.
 */
async function run(fn: (userId: string) => Promise<unknown>, saved: string): Promise<FlagFormState> {
  const staff = await requireStaff();
  try {
    await fn(staff.id);
  } catch (err) {
    if (err instanceof FlagInputError) return { error: err.message };
    throw err;
  }
  await refreshFlags();
  revalidatePath('/internal/flags');
  return { saved };
}

export async function setRolloutAction(key: string, _prev: FlagFormState, formData: FormData): Promise<FlagFormState> {
  const percent = Number(formData.get('rolloutPercent'));
  return run((by) => setFlagRule(key, { rolloutPercent: percent }, by), `Rollout set to ${percent}%.`);
}

/** The kill switch: `enabled = false` turns the flag off for every org, overrides included. */
export async function setMasterSwitchAction(key: string, enabled: boolean): Promise<void> {
  await run((by) => setFlagRule(key, { enabled }, by), enabled ? 'Switched on.' : 'Switched off for everyone.');
}

export async function setOverrideAction(key: string, _prev: FlagFormState, formData: FormData): Promise<FlagFormState> {
  const slug = String(formData.get('orgSlug') ?? '').trim();
  const value = formData.get('value');
  const enabled = value === 'on' ? true : value === 'off' ? false : null;
  return run((by) => setFlagOverride(key, slug, enabled, by), enabled === null ? `Override for ${slug} removed.` : `${slug}: ${value}.`);
}

export async function removeOverrideAction(key: string, orgSlug: string): Promise<void> {
  await run((by) => setFlagOverride(key, orgSlug, null, by), `Override for ${orgSlug} removed.`);
}

export async function deleteStaleFlagAction(key: string): Promise<void> {
  await run(() => deleteStaleFlag(key), `${key} deleted.`);
}
