'use client';

import { useActionState } from 'react';
import { requestPasswordResetAction, type AuthFormState } from '../actions';

export default function ForgotPasswordPage() {
  const [state, action, pending] = useActionState<AuthFormState, FormData>(requestPasswordResetAction, {});
  return (
    <section style={{ maxWidth: 420 }}>
      <h1>Reset your password</h1>
      {state.values?.sent ? (
        // Lesson 1.1: identical for known and unknown emails.
        <div className="card">If an account exists for that email, we have sent a reset link. It works once, for one hour.</div>
      ) : (
        <form action={action} className="card">
          <div className="field">
            <label htmlFor="email">Email</label>
            <input id="email" name="email" type="email" autoComplete="email" required />
          </div>
          <button className="btn" disabled={pending}>Email me a reset link</button>
        </form>
      )}
    </section>
  );
}
