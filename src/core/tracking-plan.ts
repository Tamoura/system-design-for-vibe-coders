import { z } from 'zod';

/*
 * Lesson 6.2 (🟢): Beacon's TRACKING PLAN. The one place that says which
 * product events exist, what they carry, and why we want them.
 *
 * Rules, all enforced (tests/analytics.test.ts):
 *
 *  1. Names are object_action: a noun, then a past-tense verb, snake_case.
 *     `monitor_created`, never `createMonitor`, `Monitor Created` or `new-monitor`.
 *     Read the list alphabetically and the events group by object.
 *  2. Properties are enums, numbers and booleans only. No free text, so no
 *     email, name or monitored URL can ever end up in analytics (the lesson's
 *     "keep PII out of event properties"). Who did it is the event's user id
 *     and org id, never a property.
 *  3. Every event answers a question we actually ask: activation, retention,
 *     revenue or engagement.
 *  4. The plan is code: track() only accepts a name from this object, with
 *     exactly these properties. A typo does not compile, and an unknown
 *     property is refused at runtime too (`.strict()`).
 *
 * `source` says who sends it. 'server': written by the backend AFTER the
 * thing happened in the database (business events: an ad blocker cannot drop
 * them and a user cannot forge them). 'client': a pure UI interaction the
 * server cannot see, sent from the browser only with the user's consent.
 */

export type Question = 'activation' | 'retention' | 'revenue' | 'engagement';

type EventSpec = {
  source: 'server' | 'client';
  question: Question;
  why: string;
  properties: z.ZodObject;
};

const PLAN = z.enum(['free', 'pro', 'business']);
const ROLE = z.enum(['owner', 'admin', 'member', 'viewer']);

export const TRACKING_PLAN = {
  org_created: {
    source: 'server',
    question: 'activation',
    why: 'Top of every funnel: how many organizations start, and where from.',
    properties: z.object({ signup_source: z.enum(['signup', 'new_org']) }).strict(),
  },
  monitor_created: {
    source: 'server',
    question: 'activation',
    why: 'Activation step 1: did the new org set up the one thing Beacon is for?',
    properties: z
      .object({
        interval_seconds: z.number().int().positive(),
        is_first: z.boolean(),
        via: z.enum(['app', 'api']),
      })
      .strict(),
  },
  monitor_check_completed: {
    source: 'server',
    question: 'activation',
    why: "Activation step 2, value delivered: the monitor's FIRST check result (only the first per monitor, or this would be millions of rows).",
    properties: z.object({ status: z.enum(['up', 'down']), is_first_for_org: z.boolean() }).strict(),
  },
  alert_channel_connected: {
    source: 'server',
    question: 'retention',
    why: 'Do teams that route alerts to Slack or a webhook stay longer? (A retention predictor to test.)',
    properties: z.object({ channel: z.enum(['slack', 'webhook']) }).strict(),
  },
  teammate_invited: {
    source: 'server',
    question: 'retention',
    why: 'Multi-person orgs churn less. How many orgs invite someone in week one?',
    properties: z.object({ role: ROLE }).strict(),
  },
  invitation_accepted: {
    source: 'server',
    question: 'retention',
    why: 'Invitations that turn into members: the org is really a team now.',
    properties: z.object({ role: ROLE }).strict(),
  },
  status_page_published: {
    source: 'server',
    question: 'activation',
    why: 'The status page is what the customer shows THEIR customers: the last onboarding step.',
    properties: z.object({}).strict(),
  },
  incident_opened: {
    source: 'server',
    question: 'retention',
    why: 'Beacon caught a real outage. Orgs that get an alert see the value; "logged in" is not retention.',
    properties: z.object({}).strict(),
  },
  subscription_upgraded: {
    source: 'server',
    question: 'revenue',
    why: 'Revenue, from the Stripe webhook after the sync, never from a click on "Upgrade".',
    properties: z.object({ from_plan: PLAN, to_plan: PLAN }).strict(),
  },
  subscription_downgraded: {
    source: 'server',
    question: 'revenue',
    why: 'Contraction and churn: which plans do orgs leave, and after which step?',
    properties: z.object({ from_plan: PLAN, to_plan: PLAN }).strict(),
  },
  api_key_created: {
    source: 'server',
    question: 'engagement',
    why: 'Orgs that integrate through the API (a Business feature) are the stickiest.',
    properties: z.object({ scope_count: z.number().int().min(1).max(10) }).strict(),
  },
  command_palette_opened: {
    source: 'client',
    question: 'engagement',
    why: 'A UI behaviour the server never sees: do people find the ⌘K palette?',
    properties: z.object({ via: z.enum(['keyboard', 'button']) }).strict(),
  },
} as const satisfies Record<string, EventSpec>;

/** Every event name in the plan. `track('monitor_creatd', …)` is a compile error. */
export type EventName = keyof typeof TRACKING_PLAN;

/** The exact properties of one event, derived from its schema. */
export type EventProperties<E extends EventName> = z.infer<(typeof TRACKING_PLAN)[E]['properties']>;

/** Events the browser may send (through POST /api/orgs/:org/analytics, with consent). */
export type ClientEventName = { [E in EventName]: (typeof TRACKING_PLAN)[E]['source'] extends 'client' ? E : never }[EventName];

export const EVENT_NAMES = Object.keys(TRACKING_PLAN) as EventName[];

export function isEventName(name: unknown): name is EventName {
  return typeof name === 'string' && Object.hasOwn(TRACKING_PLAN, name);
}

export function isClientEvent(name: unknown): name is ClientEventName {
  return isEventName(name) && TRACKING_PLAN[name].source === 'client';
}

/** object_action, snake_case, and the action is past tense ("…ed"). */
export const EVENT_NAME_PATTERN = /^[a-z]+(_[a-z]+)*_[a-z]+ed$/;

/**
 * The last line of defence against personal data in analytics. The schemas
 * already allow only enums, numbers and booleans; this runs on every event
 * anyway, so a schema loosened by mistake (z.string()) is caught at runtime:
 * no property may look like an email address or a URL, and no key may be
 * named after personal data. Returns what is wrong, or an empty list.
 */
const PII_KEYS = /(^|_)(email|name|url|phone|ip|address|token|password)($|_)/;

export function findPii(properties: Record<string, unknown>): string[] {
  const problems: string[] = [];
  for (const [key, value] of Object.entries(properties)) {
    if (PII_KEYS.test(key)) problems.push(`property "${key}" is named after personal data`);
    if (typeof value === 'string') {
      if (/@/.test(value)) problems.push(`property "${key}" looks like an email address`);
      if (/:\/\/|^www\./i.test(value)) problems.push(`property "${key}" looks like a URL`);
    } else if (value !== null && typeof value === 'object') {
      problems.push(`property "${key}" is an object; properties are flat`);
    }
  }
  return problems;
}
