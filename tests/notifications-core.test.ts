import { describe, expect, it } from 'vitest';
import {
  CATEGORIES,
  countStateChanges,
  isFlapping,
  isPhoneNumber,
  lockedReason,
  orgWantsSlack,
  resolvePersonalChannels,
  smsSegments,
  smsText,
} from '@/core/notifications';
import { createLinkToken, readLinkToken } from '@/core/tokens';

/* Lesson 4.2: the decisions, without a database. */

describe('resolvePersonalChannels: required → org policy → person → default', () => {
  const base = { userPrefs: [], orgPolicy: [], hasPhone: true };

  it('defaults: in-app and email for incidents, SMS only when asked for', () => {
    expect(resolvePersonalChannels({ ...base, category: 'incident.opened' })).toEqual(['in_app', 'email']);
  });

  it('the person’s choice beats the default', () => {
    const userPrefs = [
      { channel: 'email' as const, enabled: false },
      { channel: 'sms' as const, enabled: true },
    ];
    expect(resolvePersonalChannels({ ...base, category: 'incident.resolved', userPrefs })).toEqual(['in_app', 'sms']);
  });

  it('in-app cannot be turned off: the inbox is the record', () => {
    const userPrefs = [{ channel: 'in_app' as const, enabled: false }];
    expect(resolvePersonalChannels({ ...base, category: 'incident.opened', userPrefs })).toContain('in_app');
  });

  it('the org policy beats the person: an admin switched SMS off for everyone', () => {
    const userPrefs = [{ channel: 'sms' as const, enabled: true }];
    const orgPolicy = [{ channel: 'sms' as const, enabled: false }];
    expect(resolvePersonalChannels({ ...base, category: 'incident.opened', userPrefs, orgPolicy })).toEqual(['in_app', 'email']);
  });

  it('required categories beat everything, and never use channels they do not have', () => {
    const userPrefs = [
      { channel: 'email' as const, enabled: false },
      { channel: 'sms' as const, enabled: true },
    ];
    const orgPolicy = [{ channel: 'email' as const, enabled: false }];
    expect(resolvePersonalChannels({ ...base, category: 'billing', userPrefs, orgPolicy })).toEqual(['in_app', 'email']);
  });

  it('no phone number, no SMS', () => {
    const userPrefs = [{ channel: 'sms' as const, enabled: true }];
    expect(resolvePersonalChannels({ ...base, hasPhone: false, category: 'incident.opened', userPrefs })).toEqual(['in_app', 'email']);
  });

  it('locks the cells a person cannot change', () => {
    expect(lockedReason('billing', 'email')).toMatch(/Required/);
    expect(lockedReason('incident.opened', 'in_app')).toMatch(/Always on/);
    expect(lockedReason('billing', 'sms')).toMatch(/Not available/);
    expect(lockedReason('incident.opened', 'email')).toBeNull();
  });

  it('every required category really is required and non-empty', () => {
    const required = Object.entries(CATEGORIES).filter(([, d]) => d.required).map(([id]) => id);
    expect(required).toEqual(['billing']);
  });
});

describe('orgWantsSlack', () => {
  it('needs a webhook, a category that uses Slack, and no "off" in the policy', () => {
    expect(orgWantsSlack('incident.opened', [], true)).toBe(true);
    expect(orgWantsSlack('incident.opened', [], false)).toBe(false);
    expect(orgWantsSlack('billing', [], true)).toBe(false);
    expect(orgWantsSlack('incident.resolved', [{ channel: 'slack', enabled: false }], true)).toBe(false);
  });
});

describe('flapping (🟡)', () => {
  const t = (min: number) => new Date(Date.UTC(2026, 8, 24, 3, min));
  it('counts opens and resolves inside the window', () => {
    const incidents = [
      { openedAt: t(0), resolvedAt: t(5) }, // before the window: opened doesn't count, resolved does
      { openedAt: t(10), resolvedAt: t(12) },
      { openedAt: t(20), resolvedAt: null },
    ];
    expect(countStateChanges(incidents, t(3))).toBe(4);
  });
  it('more than 4 changes in an hour is flapping; 4 is not', () => {
    expect(isFlapping(4)).toBe(false);
    expect(isFlapping(5)).toBe(true);
  });
});

describe('SMS text and segments', () => {
  it('keeps alert texts ASCII, short, with the link', () => {
    const text = smsText('“checkout” is down — 🔥 again', 'https://beacon.test/acme/monitors/1');
    expect(text).toBe('Beacon: "checkout" is down -  again https://beacon.test/acme/monitors/1');
    expect(smsSegments(text)).toBe(1);
  });
  it('drops the link’s #fragment so a typical alert stays within one segment', () => {
    const id = '0f6ef3a4-7b5c-4a53-9b4e-3f1f3c7c2d11';
    const text = smsText('Always broken (for testing incidents) is down', `https://beacon.example.com/acme/monitors/${id}#incident-${id}`);
    expect(text).not.toContain('#incident');
    expect(smsSegments(text)).toBe(1);
  });
  it('counts GSM-7 at 160/153 and UCS-2 at 70/67 per segment', () => {
    expect(smsSegments('a'.repeat(160))).toBe(1);
    expect(smsSegments('a'.repeat(161))).toBe(2);
    expect(smsSegments('€'.repeat(80))).toBe(1); // extension characters count double: 160 septets
    expect(smsSegments('€'.repeat(81))).toBe(2);
    expect(smsSegments(`${'a'.repeat(69)}🔥`)).toBe(2); // one emoji: UCS-2, 71 units
    expect(smsSegments('é'.repeat(70))).toBe(1); // é is in GSM-7
  });
  it('accepts E.164 phone numbers only', () => {
    expect(isPhoneNumber('+15551234567')).toBe(true);
    expect(isPhoneNumber('5551234567')).toBe(false);
    expect(isPhoneNumber('+1 555 123')).toBe(false);
  });
});

describe('signed links (unsubscribe, confirm)', () => {
  const payload = { kind: 'subscriber-unsubscribe' as const, orgId: 'o1', subscriberId: 's1' };
  it('round-trips', () => {
    expect(readLinkToken(createLinkToken(payload, 'secret'), 'secret')).toEqual(payload);
  });
  it('rejects a changed payload, a changed signature, another secret, and garbage', () => {
    const token = createLinkToken(payload, 'secret');
    const [data, sig] = token.split('.');
    const forged = Buffer.from(JSON.stringify({ ...payload, subscriberId: 's2' })).toString('base64url');
    expect(readLinkToken(`${forged}.${sig}`, 'secret')).toBeNull();
    expect(readLinkToken(`${data}.${sig.slice(0, -2)}xx`, 'secret')).toBeNull();
    expect(readLinkToken(token, 'other-secret')).toBeNull();
    expect(readLinkToken('nonsense', 'secret')).toBeNull();
    expect(readLinkToken(`${token}.extra`, 'secret')).toBeNull();
  });
});
