import { BlockList, isIP } from 'node:net';

/*
 * Lesson 5.3 (🟡): server-side request forgery (SSRF). Beacon fetches URLs
 * that customers type in, twice over: every HTTP monitor, and every webhook
 * endpoint. Without a guard, a "monitor" for http://169.254.169.254/latest/meta-data/
 * reads the cloud's instance credentials, and one for http://10.0.0.5:6379/
 * pokes the internal Redis. The fix is to refuse addresses that are not on
 * the public internet, and to check the ADDRESS (after DNS), never the text
 * of the URL: `http://0x7f000001/`, `http://[::ffff:127.0.0.1]/` and
 * `http://evil.example` resolving to 127.0.0.1 are all loopback.
 *
 * This file is the pure part: which addresses are off limits. The part that
 * resolves, pins the address and follows redirects is ./safe-fetch.ts.
 * Production-grade: send all customer-bound traffic through an egress proxy
 * such as Stripe's Smokescreen that enforces the same rules (lesson 5.3).
 */

type Range = [network: string, prefix: number, reason: string];

const IPV4: Range[] = [
  ['0.0.0.0', 8, '"this network"'],
  ['10.0.0.0', 8, 'private'],
  ['100.64.0.0', 10, 'carrier-grade NAT (CGNAT)'],
  ['127.0.0.0', 8, 'loopback'],
  ['169.254.0.0', 16, 'link-local (cloud metadata)'],
  ['172.16.0.0', 12, 'private'],
  ['192.0.0.0', 24, 'reserved (IETF)'],
  ['192.0.2.0', 24, 'documentation'],
  ['192.88.99.0', 24, '6to4 relay'],
  ['192.168.0.0', 16, 'private'],
  ['198.18.0.0', 15, 'benchmarking'],
  ['198.51.100.0', 24, 'documentation'],
  ['203.0.113.0', 24, 'documentation'],
  ['224.0.0.0', 4, 'multicast'],
  ['240.0.0.0', 4, 'reserved'],
];

// IPv4-mapped addresses (::ffff:127.0.0.1) are checked against the IPv4 list
// by BlockList itself. The transition prefixes that embed an IPv4 address
// (NAT64, 6to4, Teredo) are refused outright: no legitimate monitor or webhook
// needs them, and checking the address inside would be one more parser to get right.
const IPV6: Range[] = [
  ['::', 128, 'unspecified'],
  ['::1', 128, 'loopback'],
  ['::', 96, 'IPv4-compatible (deprecated)'],
  ['64:ff9b::', 96, 'NAT64'],
  ['64:ff9b:1::', 48, 'NAT64 (local)'],
  ['100::', 64, 'discard'],
  ['2001::', 32, 'Teredo'],
  ['2001:db8::', 32, 'documentation'],
  ['2002::', 16, '6to4'],
  ['fc00::', 7, 'unique local (private)'],
  ['fe80::', 10, 'link-local'],
  ['fec0::', 10, 'site-local (deprecated)'],
  ['ff00::', 8, 'multicast'],
];

const lists = [...IPV4.map((r) => ({ r, type: 'ipv4' as const })), ...IPV6.map((r) => ({ r, type: 'ipv6' as const }))].map(({ r: [net, prefix, reason], type }) => {
  const list = new BlockList();
  list.addSubnet(net, prefix, type);
  return { list, reason };
});

/**
 * Why this IP address must not be fetched, or null if it is a public address.
 * Anything that is not a valid IP address is refused too.
 */
export function blockedAddressReason(ip: string): string | null {
  const family = isIP(ip);
  if (family === 0) return 'not an IP address';
  const type = family === 4 ? 'ipv4' : 'ipv6';
  for (const { list, reason } of lists) if (list.check(ip, type)) return reason;
  return null;
}

/**
 * The URL rules that need no DNS: http(s) only, no user:password@ (it would
 * be sent to whatever the host turns out to be, and it hides the real host in
 * "https://trusted.com@evil.com"), and, if given, only these ports.
 * Returns the reason for refusing, or null.
 */
export function urlSyntaxProblem(url: URL, opts: { ports?: readonly number[] } = {}): string | null {
  if (url.protocol !== 'http:' && url.protocol !== 'https:') return 'only http:// and https:// URLs are allowed';
  if (url.username || url.password) return 'URLs with a user name or password are not allowed';
  if (opts.ports && !opts.ports.includes(effectivePort(url))) return `only ports ${opts.ports.join(' and ')} are allowed`;
  return null;
}

export function effectivePort(url: URL): number {
  return url.port ? Number(url.port) : url.protocol === 'https:' ? 443 : 80;
}

/** The host of a URL as an address or a name: `[::1]` → `::1`. */
export function hostOf(url: URL): string {
  return url.hostname.replace(/^\[|\]$/g, '');
}
