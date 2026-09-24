'use client';

import Link from 'next/link';
import { useActionState } from 'react';
import { WEBHOOK_EVENT_TYPES } from '@/core/webhooks';
import { createEndpointAction, type CreateEndpointState } from './actions';

/** Lesson 5.3 (🟢): register an endpoint; the signing secret is shown once. */
export function CreateEndpointForm({ orgSlug }: { orgSlug: string }) {
  const [state, action, pending] = useActionState<CreateEndpointState, FormData>(createEndpointAction.bind(null, orgSlug), {});
  return (
    <form action={action} className="card grid">
      <strong>Add an endpoint</strong>
      <div className="field">
        <label htmlFor="endpoint-url">URL (https, port 443 or 80)</label>
        <input id="endpoint-url" name="url" type="url" placeholder="https://hooks.example.com/beacon" required />
      </div>
      <div className="field">
        <label htmlFor="endpoint-description">Description (optional)</label>
        <input id="endpoint-description" name="description" maxLength={200} placeholder="On-call bot" />
      </div>
      <fieldset className="grid" style={{ border: 0, padding: 0, gap: '.3rem' }}>
        <legend className="muted">Events to send</legend>
        {Object.entries(WEBHOOK_EVENT_TYPES).map(([type, description]) => (
          <label key={type} className="row" style={{ gap: '.4rem' }}>
            <input type="checkbox" name="eventTypes" value={type} defaultChecked /> <code>{type}</code> <span className="muted">{description}</span>
          </label>
        ))}
      </fieldset>
      <div className="row">
        <button className="btn" disabled={pending}>{pending ? 'Adding…' : 'Add endpoint'}</button>
        {state.error && <span className="error" data-testid="endpoint-error">{state.error}</span>}
      </div>
      {state.created && (
        <div className="card grid" data-testid="new-endpoint-secret" style={{ borderColor: 'var(--up)' }}>
          <strong>Endpoint added. Copy its signing secret now: it will not be shown again.</strong>
          <code style={{ wordBreak: 'break-all', userSelect: 'all' }}>{state.created.secret}</code>
          <span className="muted">
            Verify each delivery with the Standard Webhooks library for your language: <code>new Webhook(secret).verify(body, headers)</code>.{' '}
            <Link href={`/${orgSlug}/settings/webhooks/${state.created.id}`}>Open its delivery log →</Link>
          </span>
        </div>
      )}
    </form>
  );
}
