import { readdirSync, readFileSync, statSync } from 'node:fs';
import path from 'node:path';
import { afterAll, beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));

import { eq } from 'drizzle-orm';
import { schema } from '@/db';
import { withOrg } from '@/db/tenant';
import type { CheckOutcome } from '@/core/check';
import { EMPTY_RULES, evaluateFlag, FLAGS, rolloutBucket, type FlagKey, type RuleSet } from '@/core/flags';
import { getEntitlements } from '@/lib/entitlements';
import { LimitExceededError } from '@/lib/errors';
import { BeaconFlagProvider, isEnabled, refreshFlags, useFlagProviderForTests } from '@/lib/flags';
import { FlagInputError, listFlagsForAdmin, loadRuleSet, setFlagOverride, setFlagRule } from '@/lib/flags/store';
import { recordCheckResult } from '@/lib/checks';
import { createMonitor } from '@/lib/monitors';
import { savePreferences } from '@/lib/notifications';
import { fakeSms } from '@/lib/notifications/providers';
import { scheduleChecks } from '@/lib/scheduler';
import { cliAuditSource } from '@/lib/audit';
import { makeOrg } from './helpers/fixtures';
import { clearQueues, jobsIn, runQueuedJobs } from './helpers/queue';

/** Lesson 7.3: flag changes are audited; the tests act as a CLI user. */
const SOURCE = cliAuditSource('test');

/*
 * Lesson 6.3: feature flags. The pure rules (hashing, targeting, the kill
 * switch), the flag registry's hygiene, the OpenFeature provider's local
 * evaluation and failure modes, the two flags wired into Beacon, and the
 * line between flags and entitlements.
 */
type Org = Awaited<ReturnType<typeof makeOrg>>;
const ids = (n: number) => Array.from({ length: n }, () => crypto.randomUUID());
const rules = (key: string, rule: { enabled: boolean; rolloutPercent: number }, overrides: Record<string, boolean> = {}): RuleSet => ({
  flags: { [key]: rule },
  overrides: { [key]: overrides },
});

describe('consistent hashing (🟢)', () => {
  it('the same org always gets the same answer for the same flag (1,000 calls)', () => {
    const org = crypto.randomUUID();
    const r = rules('new-scheduler', { enabled: true, rolloutPercent: 50 });
    const first = evaluateFlag(r, 'new-scheduler', org, false).value;
    for (let i = 0; i < 1000; i++) expect(evaluateFlag(r, 'new-scheduler', org, false).value).toBe(first);
    expect(rolloutBucket('new-scheduler', org)).toBe(rolloutBucket('new-scheduler', org));
  });

  it('spreads orgs evenly: 30% of 10,000 orgs is about 3,000', () => {
    const orgs = ids(10_000);
    const on = orgs.filter((o) => evaluateFlag(rules('f', { enabled: true, rolloutPercent: 30 }), 'f', o, false).value).length;
    expect(on).toBeGreaterThan(2800);
    expect(on).toBeLessThan(3200);
    // Every bucket 0–99 is used, none much more than another.
    const counts = new Array(100).fill(0);
    for (const o of orgs) counts[rolloutBucket('f', o)]++;
    expect(Math.min(...counts)).toBeGreaterThan(50);
    expect(Math.max(...counts)).toBeLessThan(150);
  });

  it('raising the rollout from 10% to 30% keeps every org that was already on', () => {
    const orgs = ids(2000);
    const at = (p: number) => new Set(orgs.filter((o) => evaluateFlag(rules('f', { enabled: true, rolloutPercent: p }), 'f', o, false).value));
    const ten = at(10);
    const thirty = at(30);
    expect(ten.size).toBeGreaterThan(100);
    for (const o of ten) expect(thirty.has(o)).toBe(true);
    expect(thirty.size).toBeGreaterThan(ten.size);
  });

  it('different flags pick different slices (the flag key is in the hash)', () => {
    const orgs = ids(2000);
    const a = orgs.filter((o) => rolloutBucket('flag-a', o) < 10);
    const both = a.filter((o) => rolloutBucket('flag-b', o) < 10);
    expect(both.length).toBeLessThan(a.length / 3); // about 10% of a, not all of it
  });
});

describe('targeting and the kill switch (🟢)', () => {
  const acme = crypto.randomUUID();
  const globex = crypto.randomUUID();

  it('no rule → the safe default', () => {
    expect(evaluateFlag(EMPTY_RULES, 'new-scheduler', acme, false)).toEqual({ value: false, reason: 'DEFAULT' });
  });

  it('an override for your own org turns the flag on regardless of the percentage, only there', () => {
    const r = rules('f', { enabled: true, rolloutPercent: 0 }, { [acme]: true });
    expect(evaluateFlag(r, 'f', acme, false)).toEqual({ value: true, reason: 'TARGETING_MATCH' });
    expect(evaluateFlag(r, 'f', globex, false)).toEqual({ value: false, reason: 'SPLIT' });
  });

  it('an override can also keep one org out of a 100% rollout', () => {
    const r = rules('f', { enabled: true, rolloutPercent: 100 }, { [acme]: false });
    expect(evaluateFlag(r, 'f', acme, false).value).toBe(false);
    expect(evaluateFlag(r, 'f', globex, false).value).toBe(true);
  });

  it('the master switch off (kill switch) wins over everything, overrides included', () => {
    const r = rules('f', { enabled: false, rolloutPercent: 100 }, { [acme]: true });
    expect(evaluateFlag(r, 'f', acme, true)).toEqual({ value: false, reason: 'DISABLED' });
    expect(evaluateFlag(r, 'f', globex, true).value).toBe(false);
  });
});

describe('flag hygiene: owners, expiries, cleanup tickets (🟡)', () => {
  const sources = (dir: string): string[] =>
    readdirSync(dir).flatMap((f) => {
      const p = path.join(dir, f);
      return statSync(p).isDirectory() ? sources(p) : /\.(ts|tsx)$/.test(p) ? [p] : [];
    });

  it('every flag has a type, an owner, a description, a safe default and a cleanup note', () => {
    for (const [key, f] of Object.entries(FLAGS)) {
      expect(key).toMatch(/^[a-z]+(-[a-z]+)+$/);
      expect(f.owner.length, key).toBeGreaterThan(3);
      expect(f.description.length, key).toBeGreaterThan(20);
      expect(f.cleanup.length, key).toBeGreaterThan(10);
      expect(typeof f.defaultValue).toBe('boolean');
    }
  });

  it('temporary flags have an expiry date; ops kill switches do not (long-lived by design)', () => {
    for (const [key, f] of Object.entries(FLAGS)) {
      if (f.kind === 'ops') expect(f.expires, key).toBeNull();
      else expect(f.expires, key).toMatch(/^\d{4}-\d{2}-\d{2}$/);
    }
  });

  it('each temporary flag has a removal ticket, TODO(flag:<key>), at the code it guards', () => {
    const code = sources('src').filter((f) => !f.endsWith(path.join('core', 'flags.ts'))).map((f) => readFileSync(f, 'utf8')).join('\n');
    for (const [key, f] of Object.entries(FLAGS)) {
      if (f.kind === 'ops') continue;
      expect(f.cleanup).toContain(`TODO(flag:${key})`);
      expect(code, `TODO(flag:${key}) next to the isEnabled() call`).toContain(`TODO(flag:${key})`);
    }
  });

  it('the flags module knows nothing about plans, and the entitlements know nothing about flags', () => {
    const read = (p: string) => readFileSync(p, 'utf8');
    for (const f of ['src/core/flags.ts', ...sources('src/lib/flags')]) expect(read(f), f).not.toMatch(/plans'|entitlements'/);
    for (const f of ['src/core/plans.ts', 'src/lib/entitlements.ts']) expect(read(f), f).not.toMatch(/flags'/);
  });
});

describe('the OpenFeature provider: local evaluation, refresh, and failure (🟡)', () => {
  const org = crypto.randomUUID();
  let clock = 0;
  let current: RuleSet = rules('monitor-latency-chart', { enabled: true, rolloutPercent: 0 });
  let failing = false;
  let loads = 0;
  const provider = new BeaconFlagProvider({
    refreshMs: 15_000,
    now: () => clock,
    load: async () => {
      loads++;
      if (failing) throw new Error('connection refused');
      return structuredClone(current);
    },
  });

  beforeAll(async () => {
    await useFlagProviderForTests(provider);
  });

  it('evaluates in memory: no load per evaluation within the refresh interval', async () => {
    const before = loads;
    for (let i = 0; i < 50; i++) await isEnabled('monitor-latency-chart', { id: org });
    expect(loads).toBe(before);
  });

  it('a change reaches the process within one refresh interval, with no deploy', async () => {
    current = rules('monitor-latency-chart', { enabled: true, rolloutPercent: 100 });
    clock += 5_000;
    expect(await isEnabled('monitor-latency-chart', { id: org })).toBe(false); // still the cached rules
    clock += 10_000;
    expect(await isEnabled('monitor-latency-chart', { id: org })).toBe(true); // refreshed
  });

  it('the flag store going down does not crash anything: the last known rules keep working', async () => {
    failing = true;
    clock += 60_000;
    expect(await isEnabled('monitor-latency-chart', { id: org })).toBe(true);
    const details = await (await import('@openfeature/server-sdk')).OpenFeature.getClient('beacon').getBooleanDetails('monitor-latency-chart', false, { targetingKey: org });
    expect(details).toMatchObject({ value: true, reason: 'STALE' });
    failing = false;
  });

  it('with no rules ever loaded, every flag gets its SAFE default', async () => {
    const neverLoaded = new BeaconFlagProvider({ refreshMs: 1000, load: async () => Promise.reject(new Error('down')) });
    await useFlagProviderForTests(neverLoaded);
    for (const key of Object.keys(FLAGS) as FlagKey[]) expect(await isEnabled(key, { id: org })).toBe(FLAGS[key].defaultValue);
  });

  it('without an org (targeting key) it answers the default instead of throwing', async () => {
    await useFlagProviderForTests(provider);
    expect(await isEnabled('monitor-latency-chart', { id: '' })).toBe(false);
  });
});

describe('flags in Postgres, per org, through the real provider', () => {
  let acme: Org;
  let globex: Org;

  beforeAll(async () => {
    acme = await makeOrg('Flag Acme');
    globex = await makeOrg('Flag Globex');
    await useFlagProviderForTests(new BeaconFlagProvider({ load: loadRuleSet, refreshMs: 60_000 }));
  });

  it('only flags declared in the code can be set; rollouts are 0–100', async () => {
    await expect(setFlagRule('power-peg', { enabled: true }, null, SOURCE)).rejects.toBeInstanceOf(FlagInputError);
    await expect(setFlagRule('monitor-latency-chart', { rolloutPercent: 101 }, null, SOURCE)).rejects.toBeInstanceOf(FlagInputError);
    await expect(setFlagOverride('monitor-latency-chart', 'no-such-org', true, null, SOURCE)).rejects.toBeInstanceOf(FlagInputError);
  });

  it('at 0% the feature is hidden; targeting one org shows it there and nowhere else; the kill switch turns it off', async () => {
    await setFlagRule('monitor-latency-chart', { enabled: true, rolloutPercent: 0 }, null, SOURCE);
    await refreshFlags();
    expect(await isEnabled('monitor-latency-chart', acme)).toBe(false);
    expect(await isEnabled('monitor-latency-chart', globex)).toBe(false);

    await setFlagOverride('monitor-latency-chart', acme.slug, true, acme.users.owner.id, SOURCE);
    await refreshFlags();
    expect(await isEnabled('monitor-latency-chart', acme)).toBe(true);
    expect(await isEnabled('monitor-latency-chart', globex)).toBe(false);

    await setFlagRule('monitor-latency-chart', { enabled: false }, null, SOURCE); // the kill switch
    await refreshFlags();
    expect(await isEnabled('monitor-latency-chart', acme)).toBe(false);

    const [row] = (await listFlagsForAdmin()).filter((f) => f.key === 'monitor-latency-chart');
    expect(row).toMatchObject({ rule: { enabled: false, rolloutPercent: 0 }, overrides: [{ orgSlug: acme.slug, enabled: true }], expired: false });
  });
});

describe('`disable-sms-sending`: the ops kill switch (🟡)', () => {
  const DOWN: CheckOutcome = { ok: false, statusCode: 503, latencyMs: 12, error: null };
  let pager: Org;

  beforeAll(async () => {
    vi.stubEnv('SMS_PROVIDER', 'fake');
    vi.stubEnv('EMAIL_DRIVER', 'memory');
    pager = await makeOrg('Kill Switch Pager');
    await savePreferences({ orgId: pager.id, userId: pager.users.member.id }, { checked: new Set(['incident.opened:sms', 'incident.opened:email']), phoneNumber: '+15550006001' });
    await useFlagProviderForTests(new BeaconFlagProvider({ load: loadRuleSet, refreshMs: 60_000 }));
  });
  afterAll(() => vi.unstubAllEnvs());

  it('on-call flips it and the next SMS is not sent (logged as skipped); email still goes out', async () => {
    await setFlagRule('disable-sms-sending', { enabled: true, rolloutPercent: 100 }, null, SOURCE);
    await refreshFlags(); // the worker would pick it up within FLAGS_REFRESH_SECONDS
    const m = await createMonitor({ orgId: pager.id, userId: pager.users.owner.id }, { name: 'sms-kill', url: 'https://sms-kill.test', intervalSeconds: 60 });
    for (let i = 0; i < 3; i++) await recordCheckResult(pager, m, DOWN, new Date(Date.now() - 60_000 + i * 1000));
    const sentBefore = fakeSms.sent.length;
    await runQueuedJobs();
    expect(fakeSms.sent.length).toBe(sentBefore);
    const deliveries = await withOrg(pager.id, (tx) => tx.select().from(schema.notificationDeliveries).where(eq(schema.notificationDeliveries.organizationId, pager.id)));
    const sms = deliveries.find((d) => d.channel === 'sms' && d.userId === pager.users.member.id);
    expect(sms).toMatchObject({ status: 'skipped', error: expect.stringMatching(/disable-sms-sending/) });
    expect(deliveries.find((d) => d.channel === 'email' && d.userId === pager.users.member.id)?.status).toBe('sent');
  });

  it('flipped back, SMS flow again', async () => {
    await setFlagRule('disable-sms-sending', { enabled: false }, null, SOURCE);
    await refreshFlags();
    const m = await createMonitor({ orgId: pager.id, userId: pager.users.owner.id }, { name: 'sms-back', url: 'https://sms-back.test', intervalSeconds: 60 });
    for (let i = 0; i < 3; i++) await recordCheckResult(pager, m, DOWN, new Date(Date.now() - 30_000 + i * 1000));
    await runQueuedJobs();
    expect(fakeSms.sent.some((s) => s.to === '+15550006001' && s.body.includes('sms-back'))).toBe(true);
  });
});

describe('`new-scheduler`: the release flag, per org, in the worker (🟡)', () => {
  let on: Org;
  let off: Org;

  beforeAll(async () => {
    on = await makeOrg('Scheduler New');
    off = await makeOrg('Scheduler Old');
    await useFlagProviderForTests(new BeaconFlagProvider({ load: loadRuleSet, refreshMs: 60_000 }));
    await setFlagRule('new-scheduler', { enabled: true, rolloutPercent: 0 }, null, SOURCE);
    await setFlagOverride('new-scheduler', on.slug, true, null, SOURCE);
    await refreshFlags();
  });

  it('checks a never-checked monitor right away only in orgs that have the flag', async () => {
    await clearQueues();
    // 900 s: the first phase slot is usually minutes away, outside the scheduler's 90-second window.
    const a = await createMonitor({ orgId: on.id, userId: on.users.owner.id }, { name: 'new-a', url: 'https://new-a.test', intervalSeconds: 900 });
    const b = await createMonitor({ orgId: off.id, userId: off.users.owner.id }, { name: 'old-b', url: 'https://old-b.test', intervalSeconds: 900 });
    const now = new Date();
    await scheduleChecks(now);
    const jobs = await jobsIn('check.run');
    const first = jobs.filter((j) => j.data.scheduledAt === now.toISOString());
    expect(first.map((j) => j.data.monitorId)).toEqual([a.id]);
    expect(first.some((j) => j.data.monitorId === b.id)).toBe(false);
  });

  it('once the monitor has a result, it is back on its normal slots', async () => {
    await clearQueues();
    const [m] = await withOrg(on.id, (tx) => tx.select().from(schema.monitors).where(eq(schema.monitors.organizationId, on.id)));
    await recordCheckResult(on, m, { ok: true, statusCode: 200, latencyMs: 5, error: null });
    const now = new Date();
    await scheduleChecks(now);
    expect((await jobsIn('check.run')).filter((j) => j.data.scheduledAt === now.toISOString())).toEqual([]);
  });
});

describe('flags never bypass entitlements (lesson 3.2 vs 6.3)', () => {
  it('a Free org with every flag forced on still gets Free limits, and no API', async () => {
    const free = await makeOrg('Flagged Free', { plan: 'free' });
    for (const key of Object.keys(FLAGS)) {
      await setFlagRule(key, { enabled: true, rolloutPercent: 100 }, null, SOURCE);
      await setFlagOverride(key, free.slug, true, null, SOURCE);
    }
    await refreshFlags();
    expect(await isEnabled('monitor-latency-chart', free)).toBe(true); // the flags really are on
    const ent = await getEntitlements({ orgId: free.id });
    expect(ent).toMatchObject({ plan: 'free', api: false, minIntervalSec: 300, maxMonitors: 5, smsCreditsPerMonth: 0 });
    // The server still refuses what the plan does not include.
    await expect(createMonitor({ orgId: free.id, userId: free.users.owner.id }, { name: 'fast', url: 'https://fast.test', intervalSeconds: 30 })).rejects.toBeInstanceOf(LimitExceededError);
    for (const key of Object.keys(FLAGS)) await setFlagRule(key, { enabled: false }, null, SOURCE);
    await refreshFlags();
  });
});
