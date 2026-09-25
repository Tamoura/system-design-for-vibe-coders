'use client';

import { useActionState } from 'react';
import { payAction, type PayState } from '../../actions';

export function PayForm({ sessionId }: { sessionId: string }) {
  const [state, action, pending] = useActionState<PayState, FormData>(payAction.bind(null, sessionId), {});
  return (
    <form action={action}>
      <div className="field">
        <label htmlFor="card">Card number</label>
        <input id="card" name="card" defaultValue="4242 4242 4242 4242" autoComplete="off" />
        {state.error && <span className="error">{state.error}</span>}
      </div>
      <button className="btn" disabled={pending}>{pending ? 'Paying…' : 'Pay'}</button>
    </form>
  );
}
