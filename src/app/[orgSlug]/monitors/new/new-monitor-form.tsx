'use client';

import { useActionState } from 'react';
import { IntervalSelect } from '@/app/_components/interval-select';
import { createMonitorAction, type FormState } from './actions';

type Props = { orgSlug: string; minIntervalSec: number; billingHref: string | null };

export function NewMonitorForm({ orgSlug, minIntervalSec, billingHref }: Props) {
  // The org travels as a bound argument; the action re-checks the membership on the server.
  const [state, action, pending] = useActionState<FormState, FormData>(createMonitorAction.bind(null, orgSlug), {});
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
          {/* Lesson 3.2: intervals below the plan's minimum are disabled, with an upgrade hint. */}
          <IntervalSelect minIntervalSec={minIntervalSec} defaultValue={state.values?.intervalSeconds ?? String(Math.max(300, minIntervalSec))} billingHref={billingHref} />
          {err('intervalSeconds') && <span className="error">{err('intervalSeconds')}</span>}
        </div>
        {err('form') && <p className="error" data-testid="form-error">{err('form')}</p>}
        <button className="btn" disabled={pending}>{pending ? 'Saving…' : 'Add monitor'}</button>
      </form>
    </section>
  );
}
