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
