'use client';

import { useActionState } from 'react';
import { setOverrideAction, setRolloutAction, type FlagFormState } from './actions';

function Status({ state }: { state: FlagFormState }) {
  if (state.error) return <span className="error" role="alert">{state.error}</span>;
  if (state.saved) return <span className="muted" role="status">{state.saved}</span>;
  return null;
}

export function RolloutForm({ flagKey, percent }: { flagKey: string; percent: number }) {
  const [state, action, pending] = useActionState<FlagFormState, FormData>(setRolloutAction.bind(null, flagKey), {});
  const id = `rollout-${flagKey}`;
  return (
    <form action={action} className="row">
      <label htmlFor={id}>Rollout to</label>
      <input id={id} name="rolloutPercent" type="number" min={0} max={100} step={1} defaultValue={percent} style={{ width: '5.5rem' }} required />
      <span>% of organizations</span>
      <button className="btn secondary" disabled={pending}>Save</button>
      <Status state={state} />
    </form>
  );
}

export function OverrideForm({ flagKey }: { flagKey: string }) {
  const [state, action, pending] = useActionState<FlagFormState, FormData>(setOverrideAction.bind(null, flagKey), {});
  const id = `override-${flagKey}`;
  return (
    <form action={action} className="row">
      <label htmlFor={id}>Target an organization (slug)</label>
      <input id={id} name="orgSlug" placeholder="acme" required style={{ width: '10rem' }} />
      <select name="value" aria-label="Value for this organization" defaultValue="on">
        <option value="on">on</option>
        <option value="off">off</option>
      </select>
      <button className="btn secondary" disabled={pending}>Add override</button>
      <Status state={state} />
    </form>
  );
}
