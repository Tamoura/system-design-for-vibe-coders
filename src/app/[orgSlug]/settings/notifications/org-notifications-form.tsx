'use client';

import { useActionState } from 'react';
import { CHANNEL_LABELS } from '@/core/notifications';
import type { getOrgNotificationSettings } from '@/lib/notifications';
import { saveOrgNotificationsAction, type PrefsState } from '../../notifications/actions';

type Settings = Awaited<ReturnType<typeof getOrgNotificationSettings>>;
const COLUMNS = ['email', 'sms', 'slack'] as const;

/** Lesson 4.2 (🟡): the org layer of preferences, and the org's Slack channel. */
export function OrgNotificationsForm({ orgSlug, settings }: { orgSlug: string; settings: Settings }) {
  const [state, run, pending] = useActionState(saveOrgNotificationsAction.bind(null, orgSlug), {} as PrefsState);
  return (
    <form action={run} className="card grid">
      <strong>Notifications for everyone in this organization</strong>
      <span className="muted">Untick a box to switch that channel off for all members. People choose the rest for themselves.</span>
      <table>
        <thead>
          <tr>
            <th>Category</th>
            {COLUMNS.map((c) => <th key={c}>{CHANNEL_LABELS[c]}</th>)}
          </tr>
        </thead>
        <tbody>
          {settings.rows.map((row) => (
            <tr key={row.category}>
              <td>{row.label}</td>
              {COLUMNS.map((c) => (
                <td key={c}>
                  {row.channels[c] !== undefined && (
                    <input type="checkbox" name={`${row.category}:${c}`} aria-label={`${row.label}: ${CHANNEL_LABELS[c]}`} defaultChecked={row.channels[c]} />
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <div className="field">
        <label htmlFor="slackWebhookUrl">Slack incoming webhook</label>
        <input id="slackWebhookUrl" name="slackWebhookUrl" placeholder={settings.slack.connected ? `Connected (${settings.slack.hint}). Paste a new URL to replace it.` : 'https://hooks.slack.com/services/…'} />
        {settings.slack.connected && (
          <label className="row muted">
            <input type="checkbox" name="removeSlack" /> Disconnect Slack
          </label>
        )}
      </div>
      <div className="row">
        <button className="btn" disabled={pending}>Save</button>
        {state.saved && <span className="muted">Saved.</span>}
        {state.error && <span className="error">{state.error}</span>}
      </div>
    </form>
  );
}
