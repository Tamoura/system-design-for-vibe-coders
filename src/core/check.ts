/**
 * Run one uptime check: request the URL and report what happened.
 *
 * This is Beacon's core domain logic — the part no library gives you.
 * It deliberately knows nothing about the database, tenants or jobs, so the
 * scheduler (lesson 5.1) and the tests can both call it directly.
 */
import { BlockedUrlError, readCapped, safeFetch, type BodyStream } from './safe-fetch';

export type CheckOutcome = {
  ok: boolean;
  statusCode: number | null;
  latencyMs: number | null;
  error: string | null;
};

type Fetch = (url: string, init: { method: string; signal: AbortSignal; headers: Record<string, string> }) => Promise<{ status: number; body: BodyStream | null }>;

export type CheckOptions = {
  timeoutMs?: number;
  /** Injected for tests; defaults to safeFetch, which follows up to 5 redirects. */
  fetchImpl?: Fetch;
};

/**
 * Lesson 5.3 (🟡): a monitor's URL is typed in by a customer, so the request
 * goes through safeFetch(): the host is resolved, every address must be
 * public (no loopback, private, link-local/metadata, CGNAT…), the connection
 * uses exactly the checked address, and each redirect hop is checked again.
 */
const guardedFetch: Fetch = (url, init) => safeFetch(url, init, { maxRedirects: 5 });

export async function runCheck(url: string, opts: CheckOptions = {}): Promise<CheckOutcome> {
  const { timeoutMs = 10_000, fetchImpl = guardedFetch } = opts;
  const started = performance.now();
  try {
    const res = await fetchImpl(url, {
      method: 'GET',
      signal: AbortSignal.timeout(timeoutMs),
      headers: { 'user-agent': 'BeaconBot/0.1 (+https://github.com/Tamoura/system-design-for-vibe-coders/tree/beacon/starter)' },
    });
    // We only need the status. Lesson 8.1 (🟡): read at most 64 KB of the body, then hang up,
    // so a monitored URL that answers with gigabytes cannot tie up a worker (the timeout covers the rest).
    await readCapped(res).catch(() => undefined);
    const latencyMs = Math.round(performance.now() - started);
    const ok = res.status >= 200 && res.status < 400;
    return { ok, statusCode: res.status, latencyMs, error: ok ? null : `HTTP ${res.status}` };
  } catch (err) {
    const latencyMs = Math.round(performance.now() - started);
    const e = err as Error & { cause?: { code?: string; message?: string } };
    // Refused by the SSRF guard (directly, or as the cause of fetch's error).
    const blocked = err instanceof BlockedUrlError ? err : e.cause instanceof BlockedUrlError ? e.cause : null;
    if (blocked) return { ok: false, statusCode: null, latencyMs: Math.round(performance.now() - started), error: `Blocked: ${blocked.message}` };
    const timedOut = e.name === 'TimeoutError' || e.name === 'AbortError';
    // Node's fetch hides the useful part (ECONNREFUSED, ENOTFOUND, a TLS error) in `cause`.
    const reason = e.cause?.code ?? e.cause?.message ?? e.message;
    return { ok: false, statusCode: null, latencyMs, error: timedOut ? `Timed out after ${timeoutMs} ms` : reason };
  }
}
