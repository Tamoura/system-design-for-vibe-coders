import { lookup } from 'node:dns';
import { isIP } from 'node:net';
import { Agent, fetch as undiciFetch, type RequestInit, type Response } from 'undici';
import { blockedAddressReason, effectivePort, hostOf, urlSyntaxProblem } from './ssrf';

/*
 * Lesson 5.3 (🟡): every request to a customer-supplied URL goes through
 * here: HTTP monitors (src/core/check.ts) and webhooks (src/lib/webhooks).
 *
 *   1. check the URL itself (http/https, no credentials, allowed ports)
 *   2. RESOLVE the host and check EVERY address it resolves to (./ssrf.ts)
 *   3. connect only to an address that passed: the HTTP agent's DNS lookup
 *      is replaced by one that resolves, checks, and hands the connection
 *      exactly the addresses it checked. There is no second lookup, so a name
 *      that resolves to 1.2.3.4 at check time and 127.0.0.1 a millisecond
 *      later (DNS rebinding) cannot slip through: the check IS the lookup.
 *   4. redirects are never followed blindly: webhooks refuse them, monitors
 *      follow up to 5 hops and every hop goes through steps 1 to 3 again
 *
 * Development escape hatch: OUTBOUND_ALLOWLIST="localhost:3000,127.0.0.1:4555"
 * lets those host[:port] pairs through (a local webhook receiver, Beacon
 * monitoring itself). Leave it empty in production.
 */

export class BlockedUrlError extends Error {
  readonly code = 'blocked_url';
}

type Address = { address: string; family: number };
type Resolver = (host: string) => Promise<Address[]>;

const systemResolver: Resolver = (host) =>
  new Promise((ok, fail) => lookup(host, { all: true, verbatim: true }, (err, addresses) => (err ? fail(err) : ok(addresses))));
let resolve: Resolver = systemResolver;

/** Tests: answer DNS questions without the network ("evil.test" → 10.0.0.5). */
export function setResolverForTests(resolver: Resolver | null) {
  resolve = resolver ?? systemResolver;
}

function allowListed(url: URL): boolean {
  const entries = (process.env.OUTBOUND_ALLOWLIST ?? '').split(',').map((e) => e.trim().toLowerCase()).filter(Boolean);
  const host = hostOf(url).toLowerCase();
  return entries.includes(host) || entries.includes(`${host}:${effectivePort(url)}`);
}

/** Step 2 for one host: its addresses, if every one of them is public. */
async function resolvePublic(host: string): Promise<Address[]> {
  const addresses = isIP(host) ? [{ address: host, family: isIP(host) }] : await resolve(host);
  if (addresses.length === 0) throw new BlockedUrlError(`${host} has no address`);
  for (const a of addresses) {
    const reason = blockedAddressReason(a.address);
    if (reason) throw new BlockedUrlError(host === a.address ? `${host} is a ${reason} address` : `${host} resolves to ${a.address}, a ${reason} address`);
  }
  return addresses;
}

/**
 * Steps 1 and 2, for checking a URL when it is SAVED (a new monitor, a new
 * webhook endpoint): throws BlockedUrlError with a reason a person can read.
 * A name that does not resolve is accepted when `allowUnresolved` (a monitor
 * for a host that is down right now is legitimate); the guard runs again on
 * every request anyway.
 */
export async function assertPublicUrl(raw: string, opts: { ports?: readonly number[]; allowUnresolved?: boolean } = {}): Promise<URL> {
  let url: URL;
  try {
    url = new URL(raw);
  } catch {
    throw new BlockedUrlError('not a valid URL');
  }
  const allowed = allowListed(url); // development only: a named host:port, any port
  const problem = urlSyntaxProblem(url, allowed ? {} : opts);
  if (problem) throw new BlockedUrlError(problem);
  if (allowed) return url;
  try {
    await resolvePublic(hostOf(url));
  } catch (err) {
    if (err instanceof BlockedUrlError || !opts.allowUnresolved) throw err;
  }
  return url;
}

/**
 * Step 3: one HTTP agent for all customer-bound traffic, whose DNS lookup is
 * resolvePublic(). A refused address fails the connection with BlockedUrlError
 * (as the `cause` of fetch's error). TLS still checks the certificate against
 * the host NAME.
 */
const guardedAgent = new Agent({
  connect: {
    lookup: (host: string, options: { all?: boolean }, callback: (err: Error | null, address?: string | Address[], family?: number) => void) => {
      resolvePublic(host).then(
        (addresses) => (options?.all ? callback(null, addresses) : callback(null, addresses[0].address, addresses[0].family)),
        (err) => callback(err),
      );
    },
  } as unknown as Agent.Options['connect'],
});

export type SafeFetchOptions = {
  /** 0 (webhooks): a redirect is returned as is, never followed. Monitors follow up to 5. */
  maxRedirects?: number;
  /** Webhooks: [80, 443]. Monitors may use any port. */
  ports?: readonly number[];
};

/**
 * fetch() for customer-supplied URLs: steps 1 to 4. Throws BlockedUrlError
 * (directly, or as the `cause` of fetch's TypeError) when the destination, or
 * a redirect's, is not on the public internet.
 */
export async function safeFetch(raw: string, init: RequestInit = {}, opts: SafeFetchOptions = {}): Promise<Response> {
  let current = raw;
  for (let hop = 0; ; hop++) {
    const url = new URL(current);
    const allowed = allowListed(url);
    const problem = urlSyntaxProblem(url, allowed ? {} : opts);
    if (problem) throw new BlockedUrlError(problem);
    // An IP address in the URL never reaches the lookup: check it here.
    if (!allowed && isIP(hostOf(url))) await resolvePublic(hostOf(url));
    const res = await undiciFetch(url, { ...init, redirect: 'manual', dispatcher: allowed ? undefined : guardedAgent });
    const location = res.headers.get('location');
    if (res.status >= 300 && res.status < 400 && location && hop < (opts.maxRedirects ?? 0)) {
      await res.body?.cancel().catch(() => undefined);
      current = new URL(location, url).toString(); // step 4: the next hop is checked like the first
      continue;
    }
    return res;
  }
}

/**
 * Lesson 8.1 (🟡): a response-size limit. A customer's URL can answer with 10 GB
 * (by accident or on purpose); Beacon reads at most `maxBytes` of it and hangs up.
 * Returns what was read, as text (for a delivery log's snippet) and whether it was cut.
 */
export const MAX_RESPONSE_BYTES = 64 * 1024;

/** Any response body: the web ReadableStream of fetch or of undici (their types differ, their readers do not). */
export type BodyStream = { getReader(): { read(): Promise<{ done: boolean; value?: unknown }>; cancel(reason?: unknown): Promise<void> } };

export async function readCapped(res: { body: BodyStream | null }, maxBytes = MAX_RESPONSE_BYTES): Promise<{ text: string; bytes: number; truncated: boolean }> {
  if (!res.body) return { text: '', bytes: 0, truncated: false };
  const reader = res.body.getReader();
  const chunks: Uint8Array[] = [];
  let bytes = 0;
  let truncated = false;
  try {
    for (;;) {
      const { done, value: chunk } = await reader.read();
      if (done) break;
      const value = chunk as Uint8Array;
      const room = maxBytes - bytes;
      chunks.push(value.length > room ? value.subarray(0, room) : value);
      bytes += Math.min(value.length, room);
      if (value.length >= room) {
        truncated = value.length > room || !(await reader.read().then((r) => r.done));
        break;
      }
    }
  } finally {
    await reader.cancel().catch(() => undefined); // stop the download; the socket is not reused, which is fine
  }
  const all = new Uint8Array(bytes);
  let at = 0;
  for (const c of chunks) {
    all.set(c, at);
    at += c.length;
  }
  return { text: new TextDecoder().decode(all), bytes, truncated };
}
