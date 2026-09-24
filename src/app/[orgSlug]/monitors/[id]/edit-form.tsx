'use client';

import { useActionState } from 'react';
import { ALLOWED_INTERVALS } from '@/core/validation';
import { updateMonitorAction, type EditState } from './actions';

type Props = { orgSlug: string; monitor: { id: string; name: string; url: string; intervalSeconds: number; paused: boolean } };

export function EditMonitorForm({ orgSlug, monitor }: Props) {
  const [state, action, pending] = useActionState<EditState, FormData>(updateMonitorAction.bind(null, orgSlug, monitor.id), {});
  const err = (k: string) => state.errors?.[k]?.[0];
  return (
    <form action={action} className="card">
      <strong>Edit monitor</strong>
      <div className="field">
        <label htmlFor="name">Name</label>
        <input id="name" name="name" defaultValue={monitor.name} />
        {err('name') && <span className="error">{err('name')}</span>}
      </div>
      <div className="field">
        <label htmlFor="url">URL to check</label>
        <input id="url" name="url" defaultValue={monitor.url} />
        {err('url') && <span className="error">{err('url')}</span>}
      </div>
      <div className="field">
        <label htmlFor="intervalSeconds">Check every</label>
        <select id="intervalSeconds" name="intervalSeconds" defaultValue={String(monitor.intervalSeconds)}>
          {ALLOWED_INTERVALS.map((s) => (
            <option key={s} value={s}>{s < 60 ? `${s} seconds` : `${s / 60} minute${s === 60 ? '' : 's'}`}</option>
          ))}
        </select>
      </div>
      <label className="row" style={{ marginBottom: '1rem' }}>
        <input type="checkbox" name="paused" defaultChecked={monitor.paused} /> Paused
      </label>
      <div className="row">
        <button className="btn" disabled={pending}>{pending ? 'Saving…' : 'Save changes'}</button>
        {state.saved && <span className="muted">Saved.</span>}
      </div>
    </form>
  );
}
