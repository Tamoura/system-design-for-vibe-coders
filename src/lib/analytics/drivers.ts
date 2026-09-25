/*
 * Lesson 6.2 (🟡): where product events go after Postgres. One interface, the
 * way email (4.1) and storage (2.2) have one:
 *
 *   none (default)   events stay in Postgres (analytics_events). The internal
 *                    funnel at /internal/analytics reads them.
 *   posthog          ANALYTICS_DRIVER=posthog + POSTHOG_API_KEY (+ POSTHOG_HOST
 *                    for EU cloud or self-hosted): the worker forwards them.
 *   memory           the tests' fake: it records each batch.
 */

export type ForwardedEvent = {
  id: string;
  event: string;
  userId: string | null;
  properties: Record<string, unknown>;
  orgPlan: string;
  occurredAt: Date;
};

export type AnalyticsBatch = { orgId: string; plan: string; events: ForwardedEvent[] };

export interface AnalyticsDriver {
  readonly name: string;
  /** Send one org's batch. Throw to have the job retried. */
  send(batch: AnalyticsBatch): Promise<void>;
}

/**
 * PostHog's capture API, server to server (no browser SDK, so no ad blocker
 * in the way). Each batch:
 *
 *  - starts with `$groupidentify`: the org as a PostHog GROUP of type
 *    "organization" with its plan. This is the lesson's `group(orgId, { plan })`,
 *    sent with every batch, so funnels break down by organization and plan.
 *  - carries `$groups: { organization }` on every event (group analytics).
 *  - uses Beacon's user id as `distinct_id`, never the email. `identify` in a
 *    browser SDK exists to merge an anonymous visitor id into the user; with
 *    server-side capture the id is the user's from the start. Events without a
 *    person (a check result) use the org as the distinct id and create no person profile.
 *  - sends the event's row id as `uuid`, which PostHog deduplicates on: a job
 *    retried after "sent but not yet marked" does not double-count.
 */
export function createPostHogDriver(opts: { apiKey: string; host?: string; fetchImpl?: typeof fetch }): AnalyticsDriver {
  const host = (opts.host || 'https://us.i.posthog.com').replace(/\/$/, '');
  const doFetch = opts.fetchImpl ?? fetch;
  return {
    name: 'posthog',
    async send({ orgId, plan, events }) {
      const batch = [
        {
          event: '$groupidentify',
          distinct_id: `org_${orgId}`,
          timestamp: new Date().toISOString(),
          properties: { $group_type: 'organization', $group_key: orgId, $group_set: { plan }, $process_person_profile: false },
        },
        ...events.map((e) => ({
          event: e.event,
          uuid: e.id,
          distinct_id: e.userId ?? `org_${orgId}`,
          timestamp: e.occurredAt.toISOString(),
          properties: { ...e.properties, org_plan: e.orgPlan, $groups: { organization: orgId }, $process_person_profile: e.userId !== null },
        })),
      ];
      const res = await doFetch(`${host}/batch/`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ api_key: opts.apiKey, batch }),
        signal: AbortSignal.timeout(10_000),
      });
      if (!res.ok) throw new Error(`PostHog answered HTTP ${res.status}`);
    },
  };
}

/** The tests' driver: remembers every batch. `fail` makes the next sends throw (an outage). */
export function createMemoryAnalyticsDriver() {
  const batches: AnalyticsBatch[] = [];
  const driver = {
    name: 'memory',
    batches,
    fail: false,
    async send(batch: AnalyticsBatch) {
      if (driver.fail) throw new Error('analytics provider is down');
      batches.push(structuredClone(batch));
    },
  };
  return driver;
}

const g = globalThis as unknown as { beaconAnalyticsDriver?: AnalyticsDriver | null };

/** The configured driver, or null when events only stay in Postgres. */
export function getAnalyticsDriver(env: Record<string, string | undefined> = process.env): AnalyticsDriver | null {
  if (g.beaconAnalyticsDriver !== undefined) return g.beaconAnalyticsDriver;
  if (env.ANALYTICS_DRIVER === 'posthog' && env.POSTHOG_API_KEY) return createPostHogDriver({ apiKey: env.POSTHOG_API_KEY, host: env.POSTHOG_HOST });
  return null;
}

/** Tests: use this driver (or null for "none"); undefined goes back to the environment. */
export function setAnalyticsDriverForTests(driver: AnalyticsDriver | null | undefined) {
  g.beaconAnalyticsDriver = driver;
}
