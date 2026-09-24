'use client';

import { useActionState } from 'react';
import type { ApiScope } from '@/core/api-keys';
import { createApiKeyAction, type CreateKeyState } from './actions';

/** `scopes` holds only the scopes this person may grant (canGrantScopes, on the server). */
export function CreateKeyForm({ orgSlug, scopes }: { orgSlug: string; scopes: { id: ApiScope; label: string }[] }) {
  const [state, action, pending] = useActionState<CreateKeyState, FormData>(createApiKeyAction.bind(null, orgSlug), {});
  return (
    <form action={action} className="card grid">
      <strong>Create an API key</strong>
      <div className="field">
        <label htmlFor="key-name">Name</label>
        <input id="key-name" name="name" placeholder="Terraform, status dashboard…" required maxLength={80} />
      </div>
      <fieldset className="grid" style={{ border: 0, padding: 0, gap: '.3rem' }}>
        <legend className="muted">Scopes: give each key only what it needs.</legend>
        {scopes.map((s) => (
          <label key={s.id} className="row" style={{ gap: '.4rem' }}>
            <input type="checkbox" name="scopes" value={s.id} defaultChecked={s.id.endsWith(':read')} /> <code>{s.id}</code> <span className="muted">{s.label}</span>
          </label>
        ))}
      </fieldset>
      <div className="row">
        <button className="btn" disabled={pending}>{pending ? 'Creating…' : 'Create key'}</button>
        {state.error && <span className="error">{state.error}</span>}
      </div>
      {state.created && (
        <div className="card grid" data-testid="new-api-key" style={{ borderColor: 'var(--up)' }}>
          <strong>“{state.created.name}” is ready. Copy the key now: Beacon does not keep it and cannot show it again.</strong>
          <code style={{ wordBreak: 'break-all', userSelect: 'all' }}>{state.created.key}</code>
          <span className="muted">
            Use it as <code>Authorization: Bearer {state.created.key.slice(0, 12)}…</code>. Lost it? Revoke it and create a new one.
          </span>
        </div>
      )}
    </form>
  );
}
