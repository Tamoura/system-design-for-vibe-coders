'use client';

import { useActionState } from 'react';
import { resetPasswordAction, type AuthFormState } from '../actions';

export function ResetPasswordForm({ token }: { token: string }) {
  const [state, action, pending] = useActionState<AuthFormState, FormData>(resetPasswordAction, {});
  return (
    <form action={action} className="card">
      <input type="hidden" name="token" value={token} />
      <div className="field">
        <label htmlFor="password">New password</label>
        <input id="password" name="password" type="password" autoComplete="new-password" />
        {state.fieldErrors?.password && <span className="error">{state.fieldErrors.password[0]}</span>}
      </div>
      {state.error && <p className="error">{state.error}</p>}
      <p className="muted">Changing your password signs you out on every device.</p>
      <button className="btn" disabled={pending}>Set new password</button>
    </form>
  );
}
