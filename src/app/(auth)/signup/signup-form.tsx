'use client';

import { useActionState } from 'react';
import { signUpAction, type AuthFormState } from '../actions';

export function SignUpForm({ next, email }: { next: string; email: string }) {
  const [state, action, pending] = useActionState<AuthFormState, FormData>(signUpAction, {});
  const err = (k: string) => state.fieldErrors?.[k]?.[0];
  return (
    <form action={action} className="card">
      <input type="hidden" name="next" value={next} />
      <div className="field">
        <label htmlFor="name">Your name</label>
        <input id="name" name="name" autoComplete="name" defaultValue={state.values?.name} />
        {err('name') && <span className="error">{err('name')}</span>}
      </div>
      <div className="field">
        <label htmlFor="email">Work email</label>
        <input id="email" name="email" type="email" autoComplete="email" defaultValue={state.values?.email ?? email} />
        {err('email') && <span className="error">{err('email')}</span>}
      </div>
      <div className="field">
        <label htmlFor="password">Password</label>
        <input id="password" name="password" type="password" autoComplete="new-password" />
        <span className="muted">At least 12 characters. A long passphrase is better than a clever short one.</span>
        {err('password') && <span className="error">{err('password')}</span>}
      </div>
      {state.error && <p className="error">{state.error}</p>}
      <button className="btn" disabled={pending}>{pending ? 'Creating…' : 'Create account'}</button>
    </form>
  );
}
