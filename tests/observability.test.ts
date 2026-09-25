import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn(), getSessionUser: vi.fn() }));
// Lesson 7.2: capture what the app logs. The real logger (same redaction, same mixin), writing into an array.
vi.mock('@/lib/observability/logger', async (importOriginal) => {
  const real = await importOriginal<typeof import('@/lib/observability/logger')>();
  const lines: Record<string, unknown>[] = [];
  const logger = real.createLogger({ level: 'debug', service: 'test', destination: { write: (s: string) => void lines.push(JSON.parse(s)) } });
  return { ...real, logger, moduleLogger: (module: string) => logger.child({ module }), lines };
});

import { trace } from '@opentelemetry/api';
import { AggregationTemporality, InMemoryMetricExporter, PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics';
import { InMemorySpanExporter } from '@opentelemetry/sdk-trace-node';
import * as loggerModule from '@/lib/observability/logger';
import { runWithContext } from '@/lib/observability/context';
import { routeTemplate } from '@/lib/observability/metrics';
import { initTelemetry, withSpan, SpanKind } from '@/lib/observability/telemetry';
import { observeRequest } from '@/lib/observability/http';
import { EnvError, loadEnv, validateEnvOrExit } from '@/lib/env';
import { enqueue } from '@/lib/queue';
import { runScheduledCheck } from '@/lib/scheduler';
import { createMonitor } from '@/lib/monitors';
import * as healthRoute from '@/app/api/health/route';
import * as readyRoute from '@/app/api/ready/route';
import * as monitorsRoute from '@/app/api/orgs/[orgSlug]/monitors/route';
import { makeOrg, signInAs } from './helpers/fixtures';
import { clearQueues, runQueuedJobs } from './helpers/queue';
import { db } from '@/db';

/*
 * Lesson 7.2: structured logs with context on every line, redaction, error
 * capture, traces across the queue, RED and check-lag metrics, health and
 * readiness. Lesson 7.4: configuration validated at startup.
 */
const lines = (loggerModule as unknown as { lines: Record<string, unknown>[] }).lines;
const spans = new InMemorySpanExporter();
const metricExporter = new InMemoryMetricExporter(AggregationTemporality.CUMULATIVE);
const metricReader = new PeriodicExportingMetricReader({ exporter: metricExporter, exportIntervalMillis: 3_600_000 });

let acme: Awaited<ReturnType<typeof makeOrg>>;

beforeAll(async () => {
  initTelemetry('beacon-test', { spanExporter: spans, metricReader });
  acme = await makeOrg('Obs Acme');
});
afterEach(() => {
  lines.length = 0;
});

describe('🟢 structured JSON logs: request id and org on every line', () => {
  it('an API request: one access line with requestId (the caller’s x-request-id) and orgId, and the id is in the response', async () => {
    signInAs(acme.users.owner);
    const res = await monitorsRoute.GET(new Request('http://test/api/orgs/x/monitors', { headers: { 'x-request-id': 'req-obs-000001' } }), { params: Promise.resolve({ orgSlug: acme.slug }) });
    expect(res.headers.get('x-request-id')).toBe('req-obs-000001');
    const access = lines.find((l) => l.msg === 'http.request');
    expect(access).toMatchObject({ level: 'info', requestId: 'req-obs-000001', orgId: acme.id, userId: acme.users.owner.id, route: '/api/orgs/:org/monitors', status: 200, method: 'GET' });
    expect(access!.time).toMatch(/^\d{4}-\d\d-\d\dT/);
  });

  it('a request without an id gets one; an unauthenticated request still has requestId (no orgId)', async () => {
    signInAs(null);
    const res = await monitorsRoute.GET(new Request('http://test/api/orgs/x/monitors'), { params: Promise.resolve({ orgSlug: acme.slug }) });
    expect(res.status).toBe(401);
    const id = res.headers.get('x-request-id');
    expect(id).toMatch(/^[0-9a-f-]{36}$/);
    expect(lines.find((l) => l.msg === 'http.request')).toMatchObject({ requestId: id, status: 401 });
    expect(lines.find((l) => l.msg === 'http.request')).not.toHaveProperty('orgId');
  });

  it('redacts passwords, API keys, tokens, cookies and authorization headers, at any depth', () => {
    loggerModule.logger.info({ password: 'hunter2hunter2', apiKey: 'bk_live_x', body: { password: 'p', user: { token: 't' } }, req: { headers: { authorization: 'Bearer bk_live_y', cookie: 'session=abc' } } }, 'redaction.check');
    const line = lines.find((l) => l.msg === 'redaction.check')!;
    const text = JSON.stringify(line);
    for (const secret of ['hunter2hunter2', 'bk_live_x', 'bk_live_y', 'session=abc', '"p"', '"t"']) expect(text).not.toContain(secret);
    expect(line).toMatchObject({ password: '[redacted]', apiKey: '[redacted]', body: { password: '[redacted]', user: { token: '[redacted]' } } });
  });

  it('a bug becomes a 500 with the request id, and an error line (which is what goes to Sentry)', async () => {
    const res = await observeRequest(new Request('http://test/api/orgs/acme/boom', { headers: { 'x-request-id': 'req-boom-0001' } }), async () => {
      throw new TypeError('a.b is not a function');
    });
    expect(res.status).toBe(500);
    expect(await res.json()).toEqual({ error: 'internal_error', requestId: 'req-boom-0001' });
    expect(lines.find((l) => l.msg === 'error.unexpected')).toMatchObject({ level: 'error', requestId: 'req-boom-0001', err: { type: 'TypeError', message: 'a.b is not a function' } });
  });

  it('route labels are templates (no org slug, no ids): one time series per endpoint, not per customer', () => {
    expect(routeTemplate('/api/orgs/acme/monitors/0b6e5a1c-5a4f-4b4b-9b1e-1f2a3b4c5d6e')).toBe('/api/orgs/:org/monitors/:id');
    expect(routeTemplate('/api/v1/monitors/mon_3kT9xQ2')).toBe('/api/v1/monitors/:id');
  });
});

describe('🟡 context and traces cross the queue', () => {
  it('a job enqueued during a request logs with THAT request’s id and org, and its span continues the request’s trace', async () => {
    await clearQueues();
    spans.reset();
    let traceId = '';
    await runWithContext({ requestId: 'req-enqueue-01', orgId: acme.id }, () =>
      withSpan('POST /api/orgs/:org/monitors', { kind: SpanKind.SERVER }, async () => {
        traceId = trace.getActiveSpan()!.spanContext().traceId;
        await enqueue('analytics.forward', { orgId: acme.id });
      }),
    );
    lines.length = 0;
    await runQueuedJobs({ queues: ['analytics.forward'] }); // the worker, once
    const done = lines.find((l) => l.msg === 'job.completed');
    expect(done).toMatchObject({ requestId: 'req-enqueue-01', orgId: acme.id, queue: 'analytics.forward', traceId });

    const finished = spans.getFinishedSpans();
    const producer = finished.find((s) => s.name === 'enqueue analytics.forward')!;
    const consumer = finished.find((s) => s.name === 'job analytics.forward')!;
    expect(producer.spanContext().traceId).toBe(traceId);
    expect(consumer.spanContext().traceId).toBe(traceId); // one trace: request → enqueue → job
    expect(consumer.parentSpanContext?.spanId).toBe(producer.spanContext().spanId);
  });

  it('a cron job (nobody asked) still gets an id: job:<id>', async () => {
    await clearQueues();
    await enqueue('usage.report', {});
    lines.length = 0;
    await runQueuedJobs({ queues: ['usage.report'] });
    expect(lines.find((l) => l.msg === 'job.completed')?.requestId).toMatch(/^job:/);
  });
});

describe('🟡 product metrics: checks_executed_total and check_lag_seconds', () => {
  it('a check that runs 12 s after its slot is counted, with its lag, per region; HTTP requests are counted by route and status class', async () => {
    const m = await createMonitor({ orgId: acme.id, userId: acme.users.owner.id }, { name: 'lagging', url: 'https://lag.test', intervalSeconds: 60 });
    await runScheduledCheck({ orgId: acme.id, monitorId: m.id, scheduledAt: new Date(Date.now() - 12_000).toISOString() }, async () => ({ ok: true, statusCode: 200, latencyMs: 5, error: null }));
    await metricReader.forceFlush();
    const metrics = metricExporter.getMetrics().flatMap((rm) => rm.scopeMetrics.flatMap((sm) => sm.metrics));
    const byName = (n: string) => metrics.filter((x) => x.descriptor.name === n).at(-1)!;
    const executed = byName('checks_executed_total').dataPoints.find((p) => p.attributes.result === 'up')!;
    expect(executed.attributes).toEqual({ region: 'local', result: 'up' });
    expect(executed.value).toBeGreaterThanOrEqual(1);
    const lag = byName('check_lag_seconds').dataPoints[0].value as { sum: number; count: number };
    expect(lag.count).toBeGreaterThanOrEqual(1);
    expect(lag.sum).toBeGreaterThanOrEqual(12);
    const http = byName('http_server_requests_total').dataPoints.map((p) => p.attributes);
    expect(http).toContainEqual({ method: 'GET', route: '/api/orgs/:org/monitors', status_class: '2xx' });
    for (const labels of http) expect(Object.values(labels).join()).not.toContain(acme.slug); // no tenant in a label
  });
});

describe('health (liveness) and readiness', () => {
  it('/api/health answers without touching the database', async () => {
    const spy = vi.spyOn(db, 'execute');
    const res = await healthRoute.GET(new Request('http://test/api/health'));
    expect(res.status).toBe(200);
    expect(await res.json()).toMatchObject({ status: 'ok' });
    expect(spy).not.toHaveBeenCalled();
    spy.mockRestore();
  });

  it('/api/ready checks the database and the queue: 200 when both answer, 503 (and why) when one does not', async () => {
    const ok = await readyRoute.GET(new Request('http://test/api/ready'));
    expect(ok.status).toBe(200);
    expect(await ok.json()).toMatchObject({ status: 'ready', checks: { database: { ok: true }, queue: { ok: true } } });
    const spy = vi.spyOn(db, 'execute').mockRejectedValue(new Error('connection refused'));
    const down = await readyRoute.GET(new Request('http://test/api/ready'));
    expect(down.status).toBe(503);
    expect(await down.json()).toMatchObject({ status: 'not_ready', checks: { database: { ok: false, error: 'connection refused' } } });
    spy.mockRestore();
  });
});

describe('lesson 7.4: configuration is validated at startup', () => {
  const base = { DATABASE_URL: 'postgres://beacon@localhost:5432/beacon' };

  it('a minimal development config is valid; defaults are filled in', () => {
    expect(loadEnv(base)).toMatchObject({ NODE_ENV: 'development', APP_URL: 'http://localhost:3000' });
  });

  it('a missing DATABASE_URL is an error that names the variable', () => {
    expect(() => loadEnv({})).toThrow(EnvError);
    expect(() => loadEnv({})).toThrow(/DATABASE_URL: required/);
    expect(() => loadEnv({ DATABASE_URL: 'mysql://nope' })).toThrow(/DATABASE_URL: must start with postgres/);
  });

  it('production rules: a signing secret, no fake billing, no SSRF allow-list; Stripe needs its companions', () => {
    const prod = { ...base, NODE_ENV: 'production', APP_ENV: 'production' };
    expect(() => loadEnv(prod)).toThrow(/BETTER_AUTH_SECRET: required in production/);
    const secret = 'x'.repeat(40);
    expect(() => loadEnv({ ...prod, BETTER_AUTH_SECRET: secret, BILLING_PROVIDER: 'fake' })).toThrow(/BILLING_PROVIDER/);
    expect(() => loadEnv({ ...prod, BETTER_AUTH_SECRET: secret, OUTBOUND_ALLOWLIST: 'localhost:3000' })).toThrow(/OUTBOUND_ALLOWLIST/);
    expect(() => loadEnv({ ...base, STRIPE_SECRET_KEY: 'sk_test_123' })).toThrow(/STRIPE_WEBHOOK_SECRET: required with STRIPE_SECRET_KEY/);
    expect(loadEnv({ ...prod, BETTER_AUTH_SECRET: secret })).toMatchObject({ APP_ENV: 'production' });
  });

  it('validateEnvOrExit prints what is wrong and exits with code 1 (no stack trace)', () => {
    const exit = vi.spyOn(process, 'exit').mockImplementation((() => undefined) as never);
    const stderr = vi.spyOn(process.stderr, 'write').mockImplementation(() => true);
    validateEnvOrExit('beacon-web', {});
    expect(exit).toHaveBeenCalledWith(1);
    expect(String(stderr.mock.calls[0][0])).toMatch(/beacon-web cannot start[\s\S]*DATABASE_URL/);
    exit.mockRestore();
    stderr.mockRestore();
  });

  it('every variable in the schema is documented (it generates docs/configuration.md)', async () => {
    const { envSchema } = await import('@/lib/env');
    const entries = Object.entries(envSchema.shape);
    expect(entries.length).toBeGreaterThan(30);
    for (const [key, field] of entries) expect(field.description, key).toBeTruthy();
  });
});
