'use client';

import { useActionState } from 'react';
import { acceptInvitationAction, type AcceptState } from './actions';

export function AcceptForm({ token }: { token: string }) {
  const [state, action, pending] = useActionState<AcceptState, FormData>(acceptInvitationAction.bind(null, token), {});
  return (
    <form action={action}>
      {state.error && <p className="error">{state.error}</p>}
      <button className="btn" disabled={pending}>{pending ? 'Joining…' : 'Accept invitation'}</button>
    </form>
  );
}
