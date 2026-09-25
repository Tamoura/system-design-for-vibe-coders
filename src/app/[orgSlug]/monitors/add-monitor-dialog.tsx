'use client';

import { useEffect, useRef } from 'react';
import { MonitorForm } from './new/new-monitor-form';

type Props = { orgSlug: string; minIntervalSec: number; billingHref: string | null; label: string; openInitially?: boolean; primary?: boolean };

/**
 * Lesson 6.1 (🟢): "Add your first monitor" opens the form in a dialog.
 *
 * A native <dialog> opened with showModal() gives the keyboard behaviour for
 * free (the lesson's "don't build your own modals"): focus moves into it, the
 * page behind is inert, Tab stays inside, and Escape closes it. On close,
 * focus goes back to the button that opened it.
 */
export function AddMonitorDialog({ orgSlug, minIntervalSec, billingHref, label, openInitially = false, primary = true }: Props) {
  const dialog = useRef<HTMLDialogElement>(null);
  const trigger = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    if (openInitially) dialog.current?.showModal();
  }, [openInitially]);
  return (
    <>
      <button ref={trigger} type="button" className={primary ? 'btn' : 'btn secondary'} onClick={() => dialog.current?.showModal()} data-testid="add-monitor-button">
        {label}
      </button>
      <dialog ref={dialog} className="dialog" aria-labelledby="add-monitor-title" onClose={() => trigger.current?.focus()}>
        <div className="row dialog-head">
          <h2 id="add-monitor-title" className="h2">Add a monitor</h2>
          <button type="button" className="link-btn" onClick={() => dialog.current?.close()} aria-label="Close">✕</button>
        </div>
        <MonitorForm orgSlug={orgSlug} minIntervalSec={minIntervalSec} billingHref={billingHref} idPrefix="dialog" />
      </dialog>
    </>
  );
}
