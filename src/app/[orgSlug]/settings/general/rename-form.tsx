'use client';

import { useActionState } from 'react';
import { renameOrgAction, type RenameState } from './actions';

export function RenameForm({ orgSlug, name }: { orgSlug: string; name: string }) {
  const [state, action, pending] = useActionState<RenameState, FormData>(renameOrgAction.bind(null, orgSlug), {});
  return (
    <form action={action} className="card grid" aria-labelledby="org-name-heading">
      <h2 id="org-name-heading" className="h2">Organization name</h2>
      <div className="field">
        <label htmlFor="org-name">Name</label>
        <input id="org-name" name="name" defaultValue={state.name ?? name} required minLength={2} maxLength={60} aria-invalid={Boolean(state.error)} aria-describedby={state.error ? 'org-name-error' : undefined} />
        {state.error && <span id="org-name-error" className="error" role="alert">{state.error}</span>}
      </div>
      <div className="row">
        <button className="btn" disabled={pending}>{pending ? 'Saving…' : 'Save'}</button>
        {state.saved && <span className="muted" role="status">Saved.</span>}
      </div>
    </form>
  );
}
