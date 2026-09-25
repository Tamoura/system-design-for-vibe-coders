import type { Permission } from './permissions';

/*
 * Lesson 6.1 (🟡): onboarding as a state machine stored ON THE ORG.
 *
 * Each milestone is recorded once, with its time, when it happens: a row in
 * `org_milestones` (organization, milestone, reached_at). Not in the browser's
 * localStorage: a second admin who joins later sees the org's progress, not
 * their own empty one, and the timestamps feed the activation metric (6.2).
 *
 * The checklist on the Monitors page is drawn from this list, in this order,
 * and hides itself once every step is done.
 */
export const MILESTONES = ['monitor_created', 'first_check', 'alert_channel_connected', 'teammate_invited', 'status_page_published'] as const;
export type Milestone = (typeof MILESTONES)[number];

export type ChecklistStep = {
  milestone: Milestone;
  title: string;
  hint: string;
  /** Where the step is done, relative to /[orgSlug]; null when it happens by itself. */
  path: string | null;
  /** Who can do it: the call to action is shown only to them (the server checks again). */
  permission: Permission | null;
};

export const CHECKLIST: readonly ChecklistStep[] = [
  { milestone: 'monitor_created', title: 'Add your first monitor', hint: 'Paste a URL; Beacon checks it on a schedule.', path: '/monitors?add=1', permission: 'monitor.write' },
  { milestone: 'first_check', title: 'Get your first check result', hint: 'Happens by itself within minutes of adding a monitor.', path: null, permission: null },
  { milestone: 'alert_channel_connected', title: 'Connect an alert channel', hint: 'Send incidents to Slack or to a webhook.', path: '/settings/notifications', permission: 'notification.manage' },
  { milestone: 'teammate_invited', title: 'Invite a teammate', hint: 'Outages are a team sport.', path: '/members', permission: 'member.manage' },
  { milestone: 'status_page_published', title: 'Publish your status page', hint: 'Tell your customers what is up, before they ask.', path: '/status-page', permission: 'page.publish' },
];

/**
 * Lesson 6.1/6.2: ACTIVATION, Beacon's one "this org got value" event: the
 * first check result arrived within 24 hours of the org being created
 * (it created a monitor, and Beacon checked it).
 */
export const ACTIVATION_WINDOW_MS = 24 * 60 * 60 * 1000;

export function activatedAt(orgCreatedAt: Date, firstCheckAt: Date | null | undefined): Date | null {
  if (!firstCheckAt) return null;
  return firstCheckAt.getTime() - orgCreatedAt.getTime() <= ACTIVATION_WINDOW_MS ? firstCheckAt : null;
}

export type OnboardingState = {
  steps: (ChecklistStep & { reachedAt: Date | null })[];
  done: number;
  total: number;
  /** Every step done: the checklist hides itself. */
  complete: boolean;
  activatedAt: Date | null;
};

export function onboardingState(orgCreatedAt: Date, reached: ReadonlyMap<Milestone, Date>): OnboardingState {
  const steps = CHECKLIST.map((s) => ({ ...s, reachedAt: reached.get(s.milestone) ?? null }));
  const done = steps.filter((s) => s.reachedAt).length;
  return { steps, done, total: steps.length, complete: done === steps.length, activatedAt: activatedAt(orgCreatedAt, reached.get('first_check')) };
}
