'use client';

import { useEffect, useState } from 'react';
import { consentCookie, readConsent, type Consent } from '@/core/consent';
import type { ClientEventName, EventProperties } from '@/core/tracking-plan';

/*
 * Lesson 6.2 (🟡): the browser side of product analytics. Only events the
 * tracking plan marks `source: 'client'`, only after consent, and only to
 * Beacon's own endpoint (which records them server-side like any other event,
 * so there is no third-party script in the app at all).
 */

export function trackClientEvent<E extends ClientEventName>(orgSlug: string, event: E, properties: EventProperties<E>) {
  if (readConsent(document.cookie) !== 'granted') return; // no answer, or "no": nothing leaves the browser
  fetch(`/api/orgs/${orgSlug}/analytics`, {
    method: 'POST',
    keepalive: true,
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ event, properties }),
  }).catch(() => {}); // analytics never gets in the user's way
}

function useConsent(): [Consent | null | undefined, (c: Consent) => void] {
  // undefined until mounted: the server cannot see document.cookie, so render nothing first.
  const [consent, setConsent] = useState<Consent | null | undefined>(undefined);
  useEffect(() => setConsent(readConsent(document.cookie)), []);
  return [
    consent,
    (choice) => {
      document.cookie = consentCookie(choice);
      setConsent(choice);
    },
  ];
}

/** The banner in the app shell, until the user answers. "No thanks" is as easy as "Allow". */
export function ConsentBanner() {
  const [consent, choose] = useConsent();
  if (consent !== null) return null;
  return (
    <section className="consent card" role="region" aria-label="Usage analytics">
      <p style={{ margin: 0 }}>
        May Beacon record how you use the interface (for example, opening the ⌘K palette) to improve it? Only an event
        name and your user id, never what you type. You can change this in your account settings.
      </p>
      <div className="row">
        <button className="btn" onClick={() => choose('granted')}>Allow</button>
        <button className="btn secondary" onClick={() => choose('denied')}>No thanks</button>
      </div>
    </section>
  );
}

/** The same choice on /settings/account, to change it later. */
export function ConsentSetting() {
  const [consent, choose] = useConsent();
  if (consent === undefined) return null;
  return (
    <fieldset className="card grid">
      <legend>Usage analytics in your browser</legend>
      <label className="row">
        <input type="radio" name="analytics-consent" checked={consent === 'granted'} onChange={() => choose('granted')} /> Allowed
      </label>
      <label className="row">
        <input type="radio" name="analytics-consent" checked={consent !== 'granted'} onChange={() => choose('denied')} /> Not allowed
      </label>
      <span className="muted">Server-side product events about your organization (a monitor was created) use ids only; see the privacy policy.</span>
    </fieldset>
  );
}
