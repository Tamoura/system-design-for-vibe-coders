'use client';

import { useActionState } from 'react';
import type { LinkState } from './actions';

/** One button that runs a signed-link action and then shows what happened. Used by /unsubscribe and /status/…/confirm. */
export function LinkActionForm({ action, label }: { action: (prev: LinkState) => Promise<LinkState>; label: string }) {
  const [state, run, pending] = useActionState(action, {});
  if (state.done) {
    return (
      <p className={state.ok ? '' : 'error'} data-testid="link-result">
        {state.message}
      </p>
    );
  }
  return (
    <form action={run}>
      <button className="btn" disabled={pending}>{label}</button>
    </form>
  );
}
