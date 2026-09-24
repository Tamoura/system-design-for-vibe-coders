'use client';

import { useActionState } from 'react';
import { subscribeAction, type SubscribeState } from './actions';

export function SubscribeForm({ slug }: { slug: string }) {
  const [state, run, pending] = useActionState(subscribeAction.bind(null, slug), {} as SubscribeState);
  if (state.message) return <p className="muted" data-testid="subscribe-result">{state.message}</p>;
  return (
    <form action={run} className="row">
      <label htmlFor="subscribe-email" className="muted">Get incident updates by email:</label>
      <input id="subscribe-email" name="email" type="email" required placeholder="you@example.com" style={{ flex: 1, minWidth: 200 }} />
      <button className="btn secondary" disabled={pending}>Subscribe</button>
      {state.error && <div className="error">{state.error}</div>}
    </form>
  );
}
