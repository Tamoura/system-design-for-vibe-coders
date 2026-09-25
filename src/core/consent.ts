/*
 * Lesson 6.2 (🟡): consent for client-side tracking.
 *
 * Beacon's product events are recorded on the SERVER, about the org's use of
 * the product, with internal ids only (covered by the privacy policy and the
 * DPA, lesson 8.1). The browser sends one kind of event on its own: UI
 * behaviour the server cannot see (opening the ⌘K palette). That is optional,
 * so it needs the user's consent first (ePrivacy/GDPR), and "no" must be as
 * easy as "yes".
 *
 * The choice is kept in a first-party cookie, which is allowed without
 * consent because it only stores the choice itself. No answer = no tracking.
 * The server checks the same cookie, so a client that ignores it gains nothing.
 */
export const CONSENT_COOKIE = 'beacon_analytics_consent';
export type Consent = 'granted' | 'denied';

/** The choice in a Cookie header (or document.cookie), or null when the user has not answered. */
export function readConsent(cookieHeader: string | null | undefined): Consent | null {
  const match = (cookieHeader ?? '').match(new RegExp(`(?:^|;\\s*)${CONSENT_COOKIE}=(granted|denied)(?:;|$)`));
  return (match?.[1] as Consent | undefined) ?? null;
}

/** The Set-Cookie / document.cookie value for a choice: a year, whole site, never sent cross-site. */
export function consentCookie(choice: Consent): string {
  return `${CONSENT_COOKIE}=${choice}; Path=/; Max-Age=${365 * 24 * 3600}; SameSite=Lax`;
}
