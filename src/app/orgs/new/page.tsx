'use client';

import { useActionState } from 'react';
import { createOrganizationAction, type NewOrgState } from './actions';

export default function NewOrganizationPage() {
  const [state, action, pending] = useActionState<NewOrgState, FormData>(createOrganizationAction, {});
  return (
    <section style={{ maxWidth: 520 }}>
      <h1>Create an organization</h1>
      <p className="muted">An organization owns monitors and status pages. Invite your team into it; you will be its owner.</p>
      <form action={action} className="card">
        <div className="field">
          <label htmlFor="name">Organization name</label>
          <input id="name" name="name" defaultValue={state.name} placeholder="Acme Inc" />
          {state.error && <span className="error">{state.error}</span>}
        </div>
        <button className="btn" disabled={pending}>{pending ? 'Creating…' : 'Create organization'}</button>
      </form>
    </section>
  );
}
