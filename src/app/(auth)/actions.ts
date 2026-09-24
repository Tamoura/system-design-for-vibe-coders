'use server';

import { headers } from 'next/headers';
import { redirect } from 'next/navigation';
import { APIError } from 'better-auth/api';
import { auth } from '@/lib/auth';
import { safeRedirect } from '@/core/safe-redirect';
import { signUpInput } from '@/core/validation';

export type AuthFormState = { error?: string; fieldErrors?: Record<string, string[] | undefined>; values?: Record<string, string> };

/** Lesson 1.1: sign in with email and password. Better Auth sets the session cookie. */
export async function signInAction(_prev: AuthFormState, formData: FormData): Promise<AuthFormState> {
  const email = String(formData.get('email') ?? '').trim().toLowerCase();
  const password = String(formData.get('password') ?? '');
  try {
    await auth.api.signInEmail({ body: { email, password }, headers: await headers() });
  } catch (err) {
    if (!(err instanceof APIError)) throw err;
    // One message for "no such user" and "wrong password": anything more
    // specific tells attackers which emails have accounts (lesson 1.1).
    const error = err.statusCode === 429 ? 'Too many attempts. Wait a minute and try again.' : 'Email or password is incorrect.';
    return { error, values: { email } };
  }
  redirect(safeRedirect(formData.get('next')));
}

/** Lesson 1.1: create a user with a password. Lesson 1.2 adds their personal organization. */
export async function signUpAction(_prev: AuthFormState, formData: FormData): Promise<AuthFormState> {
  const values = Object.fromEntries(formData.entries()) as Record<string, string>;
  const parsed = signUpInput.safeParse(values);
  const safeValues = { name: values.name ?? '', email: values.email ?? '' }; // never echo the password back
  if (!parsed.success) return { fieldErrors: parsed.error.flatten().fieldErrors, values: safeValues };
  const next = safeRedirect(formData.get('next'));
  try {
    await auth.api.signUpEmail({ body: { ...parsed.data, callbackURL: next }, headers: await headers() });
  } catch (err) {
    if (!(err instanceof APIError)) throw err;
    // Sign-up is the one place where "this email is taken" is useful enough to
    // show; the lesson discusses the trade-off.
    return { error: err.message, values: safeValues };
  }
  redirect(next);
}

/** Lesson 1.1: logout deletes the session row, not just the cookie. */
export async function signOutAction() {
  await auth.api.signOut({ headers: await headers() });
  redirect('/login');
}

/**
 * Lesson 1.1 (🟡): "email me a reset link". The answer is the same whether or
 * not the email has an account, so this form cannot be used to find out who
 * your customers are (account enumeration).
 */
export async function requestPasswordResetAction(_prev: AuthFormState, formData: FormData): Promise<AuthFormState> {
  const email = String(formData.get('email') ?? '').trim().toLowerCase();
  if (email) {
    await auth.api
      .requestPasswordReset({ body: { email, redirectTo: '/reset-password' }, headers: await headers() })
      .catch(() => undefined); // rate limited or malformed: still say the same thing
  }
  return { error: undefined, values: { sent: 'yes' } };
}

/** Lesson 1.1 (🟡): set a new password with a one-time token from the email. */
export async function resetPasswordAction(_prev: AuthFormState, formData: FormData): Promise<AuthFormState> {
  const token = String(formData.get('token') ?? '');
  const newPassword = String(formData.get('password') ?? '');
  if (newPassword.length < 12) return { fieldErrors: { password: ['Use at least 12 characters'] } };
  try {
    // Better Auth consumes the token (second use fails) and deletes every
    // session this user has, because a reset often means "someone else is in".
    await auth.api.resetPassword({ body: { token, newPassword }, headers: await headers() });
  } catch (err) {
    if (!(err instanceof APIError)) throw err;
    return { error: 'This reset link is invalid, expired or already used. Ask for a new one.' };
  }
  redirect('/login?reset=done');
}

/**
 * Lesson 1.1 (🟡): "Sign in with GitHub". Better Auth builds the authorization
 * URL with a PKCE code challenge and a `state` value it checks on the way back.
 */
export async function signInWithGithubAction(formData: FormData) {
  const next = safeRedirect(formData.get('next'));
  const { url } = await auth.api.signInSocial({
    body: { provider: 'github', callbackURL: next, errorCallbackURL: '/login' },
    headers: await headers(),
  });
  if (!url) throw new Error('GitHub sign-in is not configured');
  redirect(url);
}
