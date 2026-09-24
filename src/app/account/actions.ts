'use server';

import { headers } from 'next/headers';
import { redirect } from 'next/navigation';
import { auth } from '@/lib/auth';
import { requireUser } from '@/lib/session';

/** Lesson 1.1: send the "confirm your email" link again. */
export async function resendVerificationAction() {
  const user = await requireUser('/account');
  await auth.api.sendVerificationEmail({ body: { email: user.email, callbackURL: '/account' }, headers: await headers() });
  redirect('/account?verification=sent');
}

/**
 * Lesson 1.1 (🟡): explicit account linking. The user is already signed in with
 * their existing method, which is the confirmation the lesson asks for. Better
 * Auth then refuses the link unless GitHub says the same email is verified.
 */
export async function linkGithubAction() {
  await requireUser('/account');
  const { url } = await auth.api.linkSocialAccount({
    body: { provider: 'github', callbackURL: '/account', errorCallbackURL: '/account' },
    headers: await headers(),
  });
  redirect(url);
}
