import { afterAll, beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));

import type { PGlite } from '@electric-sql/pglite';
import { and, eq } from 'drizzle-orm';
import * as dbModule from '@/db';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import type { CheckOutcome } from '@/core/check';
import { recordCheckResult } from '@/lib/checks';
import { memoryTransport } from '@/lib/email/memory';
import { setEmailTransportForTests } from '@/lib/email/transport';
import { acknowledgeIncident, createMonitor } from '@/lib/monitors';
import { savePreferences } from '@/lib/notifications';
import { fakeSms } from '@/lib/notifications/providers';
import { toApiIncident } from '@/lib/public-api';
import { defineWorkflow, startWorkflowInTx } from '@/lib/workflows/engine';
import { listRuns, runWorkflow, saveEscalationPolicy } from '@/lib/workflows';
import { makeOrg } from './helpers/fixtures';
import { runQueuedJobs } from './helpers/queue';

/*
 * Lesson 5.4: durable workflows on the job queue. The engine (replay from the
 * recorded history), the three-step incident fan-out, and escalation policies
 * as data interpreted by one workflow.
 */
type Org = Awaited<ReturnType<typeof makeOrg>>;
const DOWN: CheckOutcome = { ok: false, statusCode: 503, latencyMs: 5, error: null };
const UP: CheckOutcome = { ok: true, statusCode: 200, latencyMs: 5, error: null };
const pg = () => (dbModule as unknown as { sql: PGlite }).sql;

beforeAll(() => {
  vi.stubEnv('SMS_PROVIDER', 'fake');
  setEmailTransportForTests(memoryTransport);
});
afterAll(() => vi.unstubAllEnvs());

const run = () => runQueuedJobs(); // the worker, once

async function openIncident(org: Org, name: string) {
  const m = await createMonitor({ orgId: org.id, userId: org.users.owner.id }, { name, url: `https://${name}.test`, intervalSeconds: 300 });
  for (let i = 0; i < 3; i++) await recordCheckResult(org, m, DOWN, new Date(Date.now() - 10_000 + i));
  const [incident] = await withOrg(org.id, (tx) => tx.select().from(schema.incidents).where(eq(schema.incidents.monitorId, m.id)));
  return { monitor: m, incident };
}

async function runOf(org: Org, key: string) {
  const [r] = await withOrg(org.id, (tx) => tx.select().from(schema.workflowRuns).where(eq(schema.workflowRuns.key, key)));
  return r;
}

/** As if the run's current wait had timed out: its deadline is now, and the wake-up job is due. */
async function waitIsOver(runId: string) {
  await pg().query(`update workflow_steps set wake_at = now() - interval '2 seconds' where run_id = $1 and status = 'waiting'`, [runId]);
  await pg().query(`update pgboss.job set start_after = now() - interval '1 second' where name = 'workflow.run' and data->>'runId' = $1 and state = 'created'`, [runId]);
}

async function pagesFor(org: Org, userId: string) {
  return withOrg(org.id, (tx) =>
    tx.select().from(schema.notifications).where(and(eq(schema.notifications.userId, userId), eq(schema.notifications.category, 'incident.escalated'))),
  );
}

describe('the engine: replay from the recorded history', () => {
  const calls = { a: 0, b: 0, c: 0 };
  let failC = true;
  defineWorkflow('test-three-steps', async (ctx, input: { n: number }) => {
    const a = await ctx.step('a', async () => (calls.a++, input.n + 1));
    const b = await ctx.step('b', async () => (calls.b++, a * 2));
    const c = await ctx.step('c', async () => {
      calls.c++;
      if (failC) {
        failC = false;
        throw new Error('flaky step');
      }
      return b + 1;
    });
    return { c };
  });

  it('a failing step retries on its own, without running the earlier steps again', async () => {
    const org = await makeOrg('Engine');
    await withOrg(org.id, (tx) => startWorkflowInTx(tx, org.id, 'test-three-steps', 'test:1', { n: 1 }));
    await run(); // a, b ok; c throws → the job fails and is retried later
    expect(calls).toEqual({ a: 1, b: 1, c: 1 });
    await pg().query(`update pgboss.job set start_after = now() where state = 'retry'`);
    await run(); // the retry replays a and b from the history and runs c again
    expect(calls).toEqual({ a: 1, b: 1, c: 2 });
    const r = await runOf(org, 'test:1');
    expect(r).toMatchObject({ status: 'completed', output: { c: 5 } });
    const steps = await withOrg(org.id, (tx) => tx.select().from(schema.workflowSteps).where(eq(schema.workflowSteps.runId, r.id)).orderBy(schema.workflowSteps.startedAt));
    expect(steps.map((s) => [s.name, s.status, s.output, s.attempts])).toEqual([
      ['a', 'completed', 2, 1],
      ['b', 'completed', 4, 1],
      ['c', 'completed', 5, 2],
    ]);
    expect(steps.every((s) => s.finishedAt && s.finishedAt >= s.startedAt)).toBe(true);
  });

  it('starting the same key twice is one run', async () => {
    const org = await makeOrg('EngineKey');
    const first = await withOrg(org.id, (tx) => startWorkflowInTx(tx, org.id, 'test-three-steps', 'test:same', { n: 1 }));
    const second = await withOrg(org.id, (tx) => startWorkflowInTx(tx, org.id, 'test-three-steps', 'test:same', { n: 1 }));
    expect(first).toBeTruthy();
    expect(second).toBeNull();
  });
});

describe('the incident fan-out as a three-step workflow (🟢)', () => {
  it('records load-incident, notify-channels and record-deliveries, with inputs, outputs and timings', async () => {
    const org = await makeOrg('Fanout');
    const { incident } = await openIncident(org, 'fanout');
    await run();
    const [r] = await listRuns(org.id, [incident.id]);
    expect(r).toMatchObject({ workflow: 'incident-notify', status: 'completed' });
    expect(r.steps.map((s) => [s.name, s.status])).toEqual([
      ['load-incident', 'completed'],
      ['notify-channels', 'completed'],
      ['record-deliveries', 'completed'],
    ]);
    expect(r.steps[1].output).toEqual({ notified: 4, deliveries: 8 });
    expect(r.steps[2].output).toBe('Alert sent: 4 in-app, 4 email.');
    const updates = await withOrg(org.id, (tx) => tx.select().from(schema.incidentUpdates).where(eq(schema.incidentUpdates.incidentId, incident.id)));
    expect(updates.map((u) => u.body)).toContain('Alert sent: 4 in-app, 4 email.');
  });

  it('a worker that dies after step 2 resumes at step 3 and notifies nobody twice', async () => {
    const org = await makeOrg('Crash');
    memoryTransport.reset();
    const { incident } = await openIncident(org, 'crash');
    await run();
    const [r] = await listRuns(org.id, [incident.id]);
    const before = await withOrg(org.id, (tx) => tx.select().from(schema.notificationDeliveries));
    // The crash: step 2 committed, step 3 never ran (its history is gone, the run is not finished).
    await pg().query(`delete from workflow_steps where run_id = $1 and name = 'record-deliveries'`, [r.id]);
    await pg().query(`delete from incident_updates where incident_id = $1 and body like 'Alert sent%'`, [incident.id]);
    await pg().query(`update workflow_runs set status = 'running', completed_at = null where id = $1`, [r.id]);
    expect(await runWorkflow(org.id, r.id)).toMatchObject({ status: 'completed' });
    await run();
    const after = await withOrg(org.id, (tx) => tx.select().from(schema.notificationDeliveries));
    expect(after).toHaveLength(before.length);
    for (const user of Object.values(org.users)) expect(memoryTransport.to(user.email)).toHaveLength(1);
    const [resumed] = await listRuns(org.id, [incident.id]);
    expect(resumed.steps.find((s) => s.name === 'record-deliveries')).toMatchObject({ status: 'completed' });
  });
});

describe('escalation policies (🟡)', () => {
  let org: Org;
  const tiers = (o: Org) => [
    { userIds: [o.users.admin.id], channels: ['in_app', 'email'] as const, waitMinutes: 5 },
    { userIds: [o.users.owner.id], channels: ['in_app', 'email'] as const, waitMinutes: 10 },
  ];

  beforeAll(async () => {
    org = await makeOrg('Escalate');
    await saveEscalationPolicy({ orgId: org.id, userId: org.users.owner.id }, { tiers: tiers(org).map((t) => ({ ...t, channels: [...t.channels] })) });
  });

  it('pages tier 1, waits (holding no worker), pages tier 2 after the wait, and stops on acknowledge', async () => {
    const { incident } = await openIncident(org, 'escalating');
    await run();
    const esc = await runOf(org, `incident-escalation:${incident.id}`);
    expect(esc.status).toBe('waiting');
    expect(esc.wakeAt!.getTime() - Date.now()).toBeGreaterThan(4 * 60_000); // the tier's 5 minutes
    expect(await pagesFor(org, org.users.admin.id)).toHaveLength(1);
    expect(await pagesFor(org, org.users.owner.id)).toHaveLength(0);

    await waitIsOver(esc.id);
    await run();
    expect(await pagesFor(org, org.users.owner.id)).toHaveLength(1); // tier 2

    expect(await acknowledgeIncident({ orgId: org.id, userId: org.users.member.id }, incident.id)).toBe(true);
    await run(); // the signal enqueued a wake-up at once: "within seconds"
    const done = await runOf(org, `incident-escalation:${incident.id}`);
    expect(done).toMatchObject({ status: 'completed', output: { outcome: 'acknowledged', afterTier: 2, by: { userId: org.users.member.id } } });
    const [row] = await withOrg(org.id, (tx) => tx.select().from(schema.incidents).where(eq(schema.incidents.id, incident.id)));
    expect(toApiIncident(row).acknowledged_at).toEqual(expect.any(String)); // lesson 5.2: added to v1 without breaking it
    expect(await acknowledgeIncident({ orgId: org.id, userId: org.users.owner.id }, incident.id)).toBe(false); // once
  });

  it('resolving the incident before anyone acknowledges cancels the remaining tiers', async () => {
    const { incident, monitor } = await openIncident(org, 'self-healing');
    await run();
    await recordCheckResult(org, monitor, UP); // resolves, and signals the escalation
    await run();
    const esc = await runOf(org, `incident-escalation:${incident.id}`);
    expect(esc).toMatchObject({ status: 'completed', output: { outcome: 'resolved', afterTier: 1 } });
    await waitIsOver(esc.id);
    await run();
    const owners = (await pagesFor(org, org.users.owner.id)).filter((n) => n.title.includes('self-healing'));
    expect(owners).toHaveLength(0); // tier 2 never paged
  });

  it('editing the policy mid-incident does not change the running escalation, but applies to the next incident', async () => {
    const edited = await makeOrg('Edited');
    await saveEscalationPolicy({ orgId: edited.id, userId: edited.users.owner.id }, { tiers: [{ userIds: [edited.users.admin.id], channels: ['in_app'], waitMinutes: 5 }] });
    const first = await openIncident(edited, 'before-edit');
    await run();
    await saveEscalationPolicy({ orgId: edited.id, userId: edited.users.owner.id }, {
      tiers: [
        { userIds: [edited.users.member.id], channels: ['in_app'], waitMinutes: 5 },
        { userIds: [edited.users.owner.id], channels: ['in_app'], waitMinutes: 5 },
      ],
    });
    const esc = await runOf(edited, `incident-escalation:${first.incident.id}`);
    await waitIsOver(esc.id);
    await run();
    expect(await runOf(edited, esc.key)).toMatchObject({ status: 'completed', output: { outcome: 'exhausted' } }); // one tier: its snapshot
    expect(await pagesFor(edited, edited.users.member.id)).toHaveLength(0);
    expect(await pagesFor(edited, edited.users.owner.id)).toHaveLength(0);

    await openIncident(edited, 'after-edit');
    await run();
    expect(await pagesFor(edited, edited.users.member.id)).toHaveLength(1); // the new policy
  });

  it('SMS pages use an idempotency key derived from the run and the tier, so a re-run step never pages twice', async () => {
    const sms = await makeOrg('Pager'); // Business: SMS included
    await savePreferences({ orgId: sms.id, userId: sms.users.admin.id }, { checked: new Set(), phoneNumber: '+15550001234' });
    await saveEscalationPolicy({ orgId: sms.id, userId: sms.users.owner.id }, { tiers: [{ userIds: [sms.users.admin.id], channels: ['sms'], waitMinutes: 5 }] });
    const { incident } = await openIncident(sms, 'paging');
    await run();
    const esc = await runOf(sms, `incident-escalation:${incident.id}`);
    const [delivery] = await withOrg(sms.id, (tx) => tx.select().from(schema.notificationDeliveries).where(and(eq(schema.notificationDeliveries.channel, 'sms'), eq(schema.notificationDeliveries.recipient, '+15550001234'))));
    expect(delivery.dedupeKey).toBe(`escalation:${esc.id}:tier-1:${sms.users.admin.id}:sms`); // also the provider's idempotency key
    const sent = fakeSms.sent.filter((s) => s.to === '+15550001234').length;
    expect(sent).toBe(1);
    // The step runs again (a crash before its result was recorded): nothing new is sent.
    await pg().query(`delete from workflow_steps where run_id = $1 and name = 'notify-tier-1'`, [esc.id]);
    await pg().query(`update workflow_runs set status = 'running' where id = $1`, [esc.id]);
    await runWorkflow(sms.id, esc.id);
    await run();
    expect(fakeSms.sent.filter((s) => s.to === '+15550001234')).toHaveLength(1);
  });

  it('only members can be on a policy; another org cannot acknowledge or see these runs', async () => {
    const other = await makeOrg('Stranger');
    await expect(saveEscalationPolicy({ orgId: org.id, userId: org.users.owner.id }, { tiers: [{ userIds: [other.users.owner.id], channels: ['email'], waitMinutes: 5 }] })).rejects.toThrow(/member/);
    const { incident } = await openIncident(org, 'private');
    expect(await acknowledgeIncident({ orgId: other.id, userId: other.users.owner.id }, incident.id)).toBe(false);
    expect(await listRuns(other.id, [incident.id])).toEqual([]);
    const leaked = await withOrg(other.id, (tx) => tx.select().from(schema.workflowRuns));
    expect(leaked).toEqual([]);
    const [still] = await db.select().from(schema.incidents).where(eq(schema.incidents.id, incident.id));
    expect(still.acknowledgedAt).toBeNull();
  });
});
