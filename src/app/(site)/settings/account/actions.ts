'use server';

import { headers } from 'next/headers';
import { redirect } from 'next/navigation';
import { auth } from '@/lib/auth';
import { requireUser } from '@/lib/session';
import { auditSourceFor } from '@/lib/access';
import { InvalidRequestError } from '@/lib/errors';
import { deleteAccount } from '@/lib/privacy/user-data';

/** Lesson 1.1: send the "confirm your email" link again. */
export async function resendVerificationAction() {
  const user = await requireUser('/settings/account');
  await auth.api.sendVerificationEmail({ body: { email: user.email, callbackURL: '/settings/account' }, headers: await headers() });
  redirect('/settings/account?verification=sent');
}

/**
 * Lesson 1.1 (🟡): explicit account linking. The user is already signed in with
 * their existing method, which is the confirmation the lesson asks for. Better
 * Auth then refuses the link unless GitHub says the same email is verified.
 */
export async function linkGithubAction() {
  await requireUser('/settings/account');
  const { url } = await auth.api.linkSocialAccount({
    body: { provider: 'github', callbackURL: '/settings/account', errorCallbackURL: '/settings/account' },
    headers: await headers(),
  });
  redirect(url);
}

/**
 * Lesson 8.1 (GDPR Art. 17): delete my account. The user types their email to
 * confirm; the rules for orgs they own are in src/lib/privacy/user-data.ts.
 * Their sessions are deleted with them, so they are signed out everywhere.
 */
export async function deleteAccountAction(formData: FormData) {
  const user = await requireUser('/settings/account');
  if (user.impersonation) redirect('/settings/account'); // staff never delete a customer's account (the proxy refuses the POST anyway)
  try {
    await deleteAccount(user, { confirmEmail: String(formData.get('confirmEmail') ?? ''), source: await auditSourceFor(user) });
  } catch (err) {
    if (err instanceof InvalidRequestError) redirect(`/settings/account?delete_error=${encodeURIComponent(err.message)}#delete`);
    throw err;
  }
  redirect('/?account=deleted');
}
