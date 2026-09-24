'use client';

import { useActionState } from 'react';
import { CHANNEL_LABELS, PERSONAL_CHANNELS } from '@/core/notifications';
import type { PreferenceMatrix } from '@/lib/notifications';
import { savePreferencesAction, type PrefsState } from '../actions';

export function PreferencesForm({ orgSlug, matrix }: { orgSlug: string; matrix: PreferenceMatrix }) {
  const [state, run, pending] = useActionState(savePreferencesAction.bind(null, orgSlug), {} as PrefsState);
  return (
    <form action={run} className="card grid">
      <table>
        <thead>
          <tr>
            <th>Category</th>
            {PERSONAL_CHANNELS.map((c) => <th key={c}>{CHANNEL_LABELS[c]}</th>)}
          </tr>
        </thead>
        <tbody>
          {matrix.rows.map((row) => (
            <tr key={row.category}>
              <td>
                <strong>{row.label}</strong>
                {row.required && <span className="badge" style={{ marginLeft: '.4rem' }}>required</span>}
                <div className="muted">{row.description}</div>
              </td>
              {PERSONAL_CHANNELS.map((channel) => {
                const cell = row.cells[channel];
                const name = `${row.category}:${channel}`;
                return (
                  <td key={channel} title={cell.locked ?? undefined}>
                    <input type="checkbox" name={name} aria-label={`${row.label}: ${CHANNEL_LABELS[channel]}`} defaultChecked={cell.enabled} disabled={Boolean(cell.locked)} />
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
      <div className="field">
        <label htmlFor="phoneNumber">Phone number for SMS alerts</label>
        <input id="phoneNumber" name="phoneNumber" type="tel" placeholder="+15551234567" defaultValue={matrix.phoneNumber ?? ''} />
        <span className="muted">International format. At most 5 SMS an hour; beyond that, alerts come by email.</span>
      </div>
      <div className="row">
        <button className="btn" disabled={pending}>Save preferences</button>
        {state.saved && <span className="muted" data-testid="prefs-saved">Saved.</span>}
        {state.error && <span className="error">{state.error}</span>}
      </div>
    </form>
  );
}
