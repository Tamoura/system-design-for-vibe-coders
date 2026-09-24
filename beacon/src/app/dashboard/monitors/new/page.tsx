'use client';

import { useActionState } from 'react';
import { ALLOWED_INTERVALS } from '@/core/validation';
import { createMonitorAction, type FormState } from './actions';

export default function NewMonitor() {
  const [state, action, pending] = useActionState<FormState, FormData>(createMonitorAction, {});
  const err = (k: string) => state.errors?.[k]?.[0];
  return (
    <section style={{ maxWidth: 520 }}>
      <h1>Add a monitor</h1>
      <form action={action} className="card">
        <div className="field">
          <label htmlFor="name">Name</label>
          <input id="name" name="name" defaultValue={state.values?.name} placeholder="Checkout API" />
          {err('name') && <span className="error">{err('name')}</span>}
        </div>
        <div className="field">
          <label htmlFor="url">URL to check</label>
          <input id="url" name="url" defaultValue={state.values?.url} placeholder="https://example.com/health" />
          {err('url') && <span className="error">{err('url')}</span>}
        </div>
        <div className="field">
          <label htmlFor="intervalSeconds">Check every</label>
          {/* TODO(3.2): intervals below the plan's minimum should be disabled with an "Upgrade" hint. */}
          <select id="intervalSeconds" name="intervalSeconds" defaultValue={state.values?.intervalSeconds ?? '300'}>
            {ALLOWED_INTERVALS.map((s) => (
              <option key={s} value={s}>{s < 60 ? `${s} seconds` : `${s / 60} minute${s === 60 ? '' : 's'}`}</option>
            ))}
          </select>
          {err('intervalSeconds') && <span className="error">{err('intervalSeconds')}</span>}
        </div>
        <button className="btn" disabled={pending}>{pending ? 'Saving…' : 'Add monitor'}</button>
      </form>
    </section>
  );
}
