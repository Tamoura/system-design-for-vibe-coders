'use client';

import { useActionState, useRef, useState } from 'react';
import { IntervalSelect } from '@/app/_components/interval-select';
import { createMonitorInput } from '@/core/validation';
import { createMonitorAction, type FormState } from './actions';

type Props = { orgSlug: string; minIntervalSec: number; billingHref: string | null; idPrefix?: string };
type Errors = Record<string, string[] | undefined>;

/**
 * Lesson 6.1 (🟢): "add a monitor", validated TWICE with ONE schema.
 *
 *   in the browser  createMonitorInput.safeParse() on submit: an invalid URL
 *                   shows its message next to the field, and no request is sent;
 *   on the server   the action (and POST /api/orgs/:org/monitors, and the
 *                   public API) parse the same schema again. That is the check
 *                   that counts: anyone can skip this form with curl, and
 *                   they get the same message back.
 *
 * The server also checks what the browser cannot: the permission (1.3), the
 * plan's limits (3.2) and the SSRF guard (5.3).
 */
export function MonitorForm({ orgSlug, minIntervalSec, billingHref, idPrefix = 'monitor' }: Props) {
  const [state, action, pending] = useActionState<FormState, FormData>(createMonitorAction.bind(null, orgSlug), {});
  const [clientErrors, setClientErrors] = useState<Errors | null>(null);
  const form = useRef<HTMLFormElement>(null);
  const errors: Errors = clientErrors ?? state.errors ?? {};
  const err = (k: string) => errors[k]?.[0];
  const id = (k: string) => `${idPrefix}-${k}`;

  function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    const values = Object.fromEntries(new FormData(e.currentTarget).entries());
    const parsed = createMonitorInput.safeParse(values);
    if (parsed.success) {
      setClientErrors(null);
      return; // valid: the server action runs (and validates again)
    }
    e.preventDefault(); // invalid: no network request at all
    const fieldErrors = parsed.error.flatten().fieldErrors as Errors;
    setClientErrors(fieldErrors);
    // Lesson 6.1 (a11y): move focus to the first field with an error; its message is announced.
    const first = ['name', 'url', 'intervalSeconds'].find((k) => fieldErrors[k]);
    if (first) form.current?.querySelector<HTMLElement>(`[name="${first}"]`)?.focus();
  }

  const field = (k: string) => ({
    'aria-invalid': Boolean(err(k)) || undefined,
    'aria-describedby': err(k) ? id(`${k}-error`) : undefined,
    onInput: () => clientErrors?.[k] && setClientErrors({ ...clientErrors, [k]: undefined }),
  });

  return (
    <form ref={form} action={action} onSubmit={onSubmit} noValidate className="grid" data-testid="monitor-form">
      <div className="field">
        <label htmlFor={id('name')}>Name</label>
        <input id={id('name')} name="name" defaultValue={state.values?.name} placeholder="Checkout API" autoComplete="off" {...field('name')} />
        {err('name') && <span id={id('name-error')} className="error" role="alert">{err('name')}</span>}
      </div>
      <div className="field">
        <label htmlFor={id('url')}>URL to check</label>
        <input id={id('url')} name="url" type="url" inputMode="url" defaultValue={state.values?.url} placeholder="https://example.com/health" {...field('url')} />
        {err('url') && <span id={id('url-error')} className="error" role="alert" data-testid="url-error">{err('url')}</span>}
      </div>
      <div className="field">
        <label htmlFor="intervalSeconds">Check every</label>
        {/* Lesson 3.2: intervals below the plan's minimum are disabled, with an upgrade hint. */}
        <IntervalSelect minIntervalSec={minIntervalSec} defaultValue={state.values?.intervalSeconds ?? String(Math.max(300, minIntervalSec))} billingHref={billingHref} />
        {err('intervalSeconds') && <span className="error" role="alert">{err('intervalSeconds')}</span>}
      </div>
      {err('form') && <p className="error" role="alert" data-testid="form-error">{err('form')}</p>}
      <div>
        <button className="btn" disabled={pending}>{pending ? 'Saving…' : 'Add monitor'}</button>
      </div>
    </form>
  );
}

/** /[org]/monitors/new: the same form on its own page (a link to share, and it works before JavaScript loads). */
export function NewMonitorForm(props: Omit<Props, 'idPrefix'>) {
  return (
    <section className="page-narrow">
      <h1>Add a monitor</h1>
      <div className="card">
        <MonitorForm {...props} />
      </div>
    </section>
  );
}
