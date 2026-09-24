import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import http from 'node:http';
import type { AddressInfo } from 'node:net';
import { runCheck } from '@/core/check';

let server: http.Server;
let base = '';

beforeAll(async () => {
  server = http.createServer((req, res) => {
    if (req.url === '/ok') return res.end('fine');
    if (req.url === '/redirect') { res.writeHead(302, { location: '/ok' }); return res.end(); }
    if (req.url === '/broken') { res.writeHead(503); return res.end('down'); }
    if (req.url === '/slow') { setTimeout(() => res.end('late'), 500); return; }
    res.writeHead(404); res.end();
  });
  await new Promise<void>((r) => server.listen(0, '127.0.0.1', r));
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
});
afterAll(() => new Promise<void>((r) => server.close(() => r())));

describe('runCheck', () => {
  it('reports a 200 as up, with latency', async () => {
    const r = await runCheck(`${base}/ok`);
    expect(r).toMatchObject({ ok: true, statusCode: 200, error: null });
    expect(r.latencyMs).toBeGreaterThanOrEqual(0);
  });

  it('follows redirects', async () => {
    expect((await runCheck(`${base}/redirect`)).statusCode).toBe(200);
  });

  it('reports a 5xx as down with the status in the error', async () => {
    expect(await runCheck(`${base}/broken`)).toMatchObject({ ok: false, statusCode: 503, error: 'HTTP 503' });
  });

  it('times out slow endpoints', async () => {
    const r = await runCheck(`${base}/slow`, { timeoutMs: 100 });
    expect(r.ok).toBe(false);
    expect(r.statusCode).toBeNull();
    expect(r.error).toMatch(/Timed out/);
  });

  it('reports connection errors instead of throwing', async () => {
    // Grab a free port, then close it so nothing is listening there.
    const probe = http.createServer();
    await new Promise<void>((r) => probe.listen(0, '127.0.0.1', r));
    const port = (probe.address() as AddressInfo).port;
    await new Promise<void>((r) => probe.close(() => r()));
    const r = await runCheck(`http://127.0.0.1:${port}/nothing`);
    expect(r.ok).toBe(false);
    expect(r.error).toBe('ECONNREFUSED');
  });
});
