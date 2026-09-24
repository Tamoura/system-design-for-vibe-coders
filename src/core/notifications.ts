import type { Permission } from './permissions';

/*
 * Lesson 4.2: the notification DECISIONS, as pure functions. No database, no
 * providers: what to send, to whom, on which channel, and when to hold back.
 * src/lib/notifications uses these; tests/notifications-core.test.ts pins them.
 *
 *   event ─► recipients (permission) ─► channels (required → org policy → user → default)
 *         ─► dedupe (one per event per person) ─► throttle (SMS) ─► channel jobs
 */

/** The channels. `in_app` is the inbox; `slack` is the ORG's channel, not a person's. */
export const CHANNELS = ['in_app', 'email', 'sms', 'slack'] as const;
export type Channel = (typeof CHANNELS)[number];
/** The channels a person chooses for themselves on the preferences page. */
export const PERSONAL_CHANNELS = ['in_app', 'email', 'sms'] as const satisfies readonly Channel[];
export type PersonalChannel = (typeof PERSONAL_CHANNELS)[number];

export const CHANNEL_LABELS: Record<Channel, string> = { in_app: 'In-app', email: 'Email', sms: 'SMS', slack: 'Slack' };

type CategoryDef = {
  label: string;
  description: string;
  /** Required categories cannot be turned off (lesson 4.2: security and billing). */
  required: boolean;
  /** Who is eligible at all (lesson 1.3): a member whose role has this permission. */
  permission: Permission;
  /** Channels this category may use. */
  channels: readonly Channel[];
  /** What a person gets before they touch their preferences. */
  defaults: Partial<Record<Channel, boolean>>;
};

export const CATEGORIES = {
  'incident.opened': {
    label: 'Incident opened',
    description: 'A monitor failed 3 checks in a row.',
    required: false,
    permission: 'monitor.read',
    channels: ['in_app', 'email', 'sms', 'slack'],
    defaults: { in_app: true, email: true, sms: false, slack: true },
  },
  'incident.resolved': {
    label: 'Incident resolved',
    description: 'The monitor is passing again.',
    required: false,
    permission: 'monitor.read',
    channels: ['in_app', 'email', 'sms', 'slack'],
    defaults: { in_app: true, email: true, sms: false, slack: true },
  },
  'monitor.flapping': {
    label: 'Monitor flapping',
    description: 'It keeps going up and down; one alert instead of many.',
    required: false,
    permission: 'monitor.read',
    channels: ['in_app', 'email', 'sms', 'slack'],
    defaults: { in_app: true, email: true, sms: false, slack: true },
  },
  billing: {
    label: 'Billing and plan',
    description: 'Plan changes, paused monitors, SMS usage alerts.',
    required: true,
    permission: 'billing.manage',
    channels: ['in_app', 'email'],
    defaults: { in_app: true, email: true },
  },
} as const satisfies Record<string, CategoryDef>;

export type Category = keyof typeof CATEGORIES;
export const CATEGORY_IDS = Object.keys(CATEGORIES) as [Category, ...Category[]];

export function isCategory(value: string): value is Category {
  return Object.hasOwn(CATEGORIES, value);
}

export function categoryUsesChannel(category: Category, channel: Channel): boolean {
  return (CATEGORIES[category].channels as readonly Channel[]).includes(channel);
}

export type ChannelSetting = { channel: Channel; enabled: boolean };

/**
 * Why a cell of the preferences matrix cannot be changed, or null if it can.
 * In-app is always on: the inbox is the record of everything (lesson 4.2's
 * channel table). Required categories are on for every channel they use.
 */
export function lockedReason(category: Category, channel: PersonalChannel): string | null {
  if (!categoryUsesChannel(category, channel)) return 'Not available for this category';
  if (channel === 'in_app') return 'Always on: the inbox keeps a record of every alert';
  if (CATEGORIES[category].required) return 'Required: this cannot be turned off';
  return null;
}

/**
 * Lesson 4.2 (🟡), "two layers of preferences". Which personal channels one
 * person gets for one category, resolved in the lesson's order:
 *
 *   1. required category      → every channel it uses, whatever anyone chose
 *   2. org policy             → an admin can switch a channel off for everyone
 *                               (e.g. "no SMS for resolved incidents")
 *   3. the person's choice    → their preferences page
 *   4. the default            → CATEGORIES[…].defaults
 *
 * SMS also needs a phone number. In-app is always on.
 */
export function resolvePersonalChannels(input: {
  category: Category;
  userPrefs: ChannelSetting[];
  orgPolicy: ChannelSetting[];
  hasPhone: boolean;
}): PersonalChannel[] {
  const def = CATEGORIES[input.category];
  const result: PersonalChannel[] = [];
  for (const channel of PERSONAL_CHANNELS) {
    if (!categoryUsesChannel(input.category, channel)) continue;
    if (channel === 'in_app' || def.required) {
      result.push(channel);
      continue;
    }
    if (input.orgPolicy.some((p) => p.channel === channel && !p.enabled)) continue;
    if (channel === 'sms' && !input.hasPhone) continue;
    const own = input.userPrefs.find((p) => p.channel === channel);
    if (own ? own.enabled : Boolean((def.defaults as Partial<Record<Channel, boolean>>)[channel])) result.push(channel);
  }
  return result;
}

/** The org-level Slack channel: needs a webhook, a category that uses Slack, and no "off" in the org policy. */
export function orgWantsSlack(category: Category, orgPolicy: ChannelSetting[], hasWebhook: boolean): boolean {
  if (!hasWebhook || !categoryUsesChannel(category, 'slack')) return false;
  return !orgPolicy.some((p) => p.channel === 'slack' && !p.enabled);
}

/*
 * Lesson 4.2 (🟡): anti-flapping. Hysteresis (3 failures to open, in
 * src/core/incidents.ts) removes most noise. What is left: a monitor that
 * opens and resolves incidents over and over. More than FLAPPING.maxChanges
 * state changes within FLAPPING.windowMs makes it "flapping": one
 * notification says so, and the rest are held back until it settles.
 */
export const FLAPPING = { windowMs: 60 * 60 * 1000, maxChanges: 4 } as const;

/** How many times a monitor changed state (an incident opened or resolved) since `since`. */
export function countStateChanges(incidents: { openedAt: Date; resolvedAt: Date | null }[], since: Date): number {
  let changes = 0;
  for (const i of incidents) {
    if (i.openedAt > since) changes++;
    if (i.resolvedAt && i.resolvedAt > since) changes++;
  }
  return changes;
}

export function isFlapping(changesInWindow: number): boolean {
  return changesInWindow > FLAPPING.maxChanges;
}

/*
 * Lesson 4.2 (🟡): SMS. At most SMS_PER_HOUR per person per hour; beyond
 * that the alert goes by email instead, saying how many SMS were held back.
 */
export const SMS_PER_HOUR = 5;

/**
 * The SMS text: short, plain ASCII and a link. Every non-GSM-7 character (an
 * emoji, a curly quote) switches the whole message to UCS-2 and cuts a
 * segment from 160 characters to 70, and SMS is billed per segment (3.3).
 * The link loses its #fragment: 46 characters of "#incident-<uuid>" can
 * be the difference between one segment and two.
 */
export function smsText(title: string, url: string): string {
  const ascii = title
    .normalize('NFKD')
    .replace(/[‘’]/g, "'")
    .replace(/[“”]/g, '"')
    .replace(/[–—]/g, '-')
    .replace(/[^\x20-\x7e]/g, '');
  return `Beacon: ${ascii.slice(0, 100)} ${url.split('#')[0]}`;
}

// The GSM 03.38 basic character set (one septet each) and its extension table (two septets each).
const GSM_BASIC = '@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞÆæßÉ !"#¤%&\'()*+,-./0123456789:;<=>?¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà';
const GSM_EXTENDED = '^{}\\[~]|€\f';

/** How many billable segments a text costs (lesson 3.3 meters segments, not messages). */
export function smsSegments(text: string): number {
  const chars = [...text];
  const gsm = chars.every((c) => GSM_BASIC.includes(c) || GSM_EXTENDED.includes(c));
  if (gsm) {
    const septets = chars.reduce((n, c) => n + (GSM_EXTENDED.includes(c) ? 2 : 1), 0);
    return septets <= 160 ? 1 : Math.ceil(septets / 153);
  }
  const units = text.length; // UTF-16 code units, which is what UCS-2 counts
  return units <= 70 ? 1 : Math.ceil(units / 67);
}

/** E.164 phone numbers only: "+15551234567". */
export function isPhoneNumber(value: string): boolean {
  return /^\+[1-9]\d{6,14}$/.test(value);
}
