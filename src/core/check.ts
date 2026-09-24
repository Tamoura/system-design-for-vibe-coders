/**
 * Run one uptime check: request the URL and report what happened.
 *
 * This is Beacon's core domain logic — the part no library gives you.
 * It deliberately knows nothing about the database, tenants or jobs, so the
 * scheduler (lesson 5.1) and the tests can both call it directly.
 */
export type CheckOutcome = {
  ok: boolean;
  statusCode: number | null;
  latencyMs: number | null;
  error: string | null;
};

export type CheckOptions = {
  timeoutMs?: number;
  /** Injected for tests; defaults to the global fetch. */
  fetchImpl?: typeof fetch;
};

export async function runCheck(url: string, opts: CheckOptions = {}): Promise<CheckOutcome> {
  const { timeoutMs = 10_000, fetchImpl = fetch } = opts;
  const started = performance.now();
  try {
    // TODO(5.3): customer-supplied URLs are an SSRF risk. Before this runs in
    // production, refuse private, loopback and link-local addresses — after DNS
    // resolution, and again after every redirect.
    const res = await fetchImpl(url, {
      method: 'GET',
      redirect: 'follow',
      signal: AbortSignal.timeout(timeoutMs),
      headers: { 'user-agent': 'BeaconBot/0.1 (+https://github.com/Tamoura/beacon)' },
    });
    // Drain the body so the connection can be reused; we only need the status.
    await res.arrayBuffer().catch(() => undefined);
    const latencyMs = Math.round(performance.now() - started);
    const ok = res.status >= 200 && res.status < 400;
    return { ok, statusCode: res.status, latencyMs, error: ok ? null : `HTTP ${res.status}` };
  } catch (err) {
    const latencyMs = Math.round(performance.now() - started);
    const e = err as Error & { cause?: { code?: string; message?: string } };
    const timedOut = e.name === 'TimeoutError' || e.name === 'AbortError';
    // Node's fetch hides the useful part (ECONNREFUSED, ENOTFOUND, a TLS error) in `cause`.
    const reason = e.cause?.code ?? e.cause?.message ?? e.message;
    return { ok: false, statusCode: null, latencyMs, error: timedOut ? `Timed out after ${timeoutMs} ms` : reason };
  }
}
