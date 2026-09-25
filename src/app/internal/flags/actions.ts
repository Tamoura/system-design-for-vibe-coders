'use server';

import { revalidatePath } from 'next/cache';
import { refreshFlags } from '@/lib/flags';
import { FlagInputError, deleteStaleFlag, setFlagOverride, setFlagRule } from '@/lib/flags/store';
import type { AuditSource } from '@/core/audit';
import { requireStaff, staffAuditSourceFromRequest } from '@/lib/staff';

export type FlagFormState = { error?: string; saved?: string };

/*
 * Lesson 6.3: flip flags without a deploy. Every action checks the staff
 * session itself (a server action is a public POST endpoint), then reloads
 * this process's rules at once; other processes (the worker) follow within
 * FLAGS_REFRESH_SECONDS. Lesson 7.1: only staff roles with "flags.manage"
 * (engineer, superadmin); lesson 7.3: each change is a platform audit event.
 */
async function run(fn: (userId: string, source: AuditSource) => Promise<unknown>, saved: string): Promise<FlagFormState> {
  const staff = await requireStaff('flags.manage');
  try {
    await fn(staff.userId, await staffAuditSourceFromRequest(staff));
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
  return run((by, source) => setFlagRule(key, { rolloutPercent: percent }, by, source), `Rollout set to ${percent}%.`);
}

/** The kill switch: `enabled = false` turns the flag off for every org, overrides included. */
export async function setMasterSwitchAction(key: string, enabled: boolean): Promise<void> {
  await run((by, source) => setFlagRule(key, { enabled }, by, source), enabled ? 'Switched on.' : 'Switched off for everyone.');
}

export async function setOverrideAction(key: string, _prev: FlagFormState, formData: FormData): Promise<FlagFormState> {
  const slug = String(formData.get('orgSlug') ?? '').trim();
  const value = formData.get('value');
  const enabled = value === 'on' ? true : value === 'off' ? false : null;
  return run((by, source) => setFlagOverride(key, slug, enabled, by, source), enabled === null ? `Override for ${slug} removed.` : `${slug}: ${value}.`);
}

export async function removeOverrideAction(key: string, orgSlug: string): Promise<void> {
  await run((by, source) => setFlagOverride(key, orgSlug, null, by, source), `Override for ${orgSlug} removed.`);
}

export async function deleteStaleFlagAction(key: string): Promise<void> {
  await run(() => deleteStaleFlag(key), `${key} deleted.`);
}
