import { afterAll, afterEach, beforeAll, describe, expect, it, vi } from 'vitest';
import http from 'node:http';
import type { AddressInfo } from 'node:net';
import { runCheck } from '@/core/check';
import { assertPublicUrl, BlockedUrlError, safeFetch, setResolverForTests } from '@/core/safe-fetch';
import { blockedAddressReason } from '@/core/ssrf';

/*
 * Lesson 5.3 (🟡): the SSRF guard, for monitors and webhooks alike. DNS is
 * faked where a test needs a name to resolve somewhere specific.
 */

const FAKE_DNS: Record<string, string[]> = {
  'public.test': ['93.184.215.14'],
  'intranet.test': ['10.1.2.3'],
  'sneaky.test': ['93.184.215.14', '127.0.0.1'], // one bad address is enough to refuse
  'v6-local.test': ['fd00::1'],
};

beforeAll(() =>
  setResolverForTests(async (host) => {
    const addresses = FAKE_DNS[host];
    if (!addresses) throw Object.assign(new Error(`getaddrinfo ENOTFOUND ${host}`), { code: 'ENOTFOUND' });
    return addresses.map((address) => ({ address, family: address.includes(':') ? 6 : 4 }));
  }),
);
afterAll(() => setResolverForTests(null));
afterEach(() => vi.unstubAllEnvs());

describe('which addresses are off limits', () => {
  it.each([
    ['127.0.0.1', 'loopback'],
    ['10.0.0.5', 'private'],
    ['172.16.9.9', 'private'],
    ['192.168.1.1', 'private'],
    ['169.254.169.254', 'link-local (cloud metadata)'],
    ['100.64.0.1', 'carrier-grade NAT (CGNAT)'],
    ['0.0.0.0', '"this network"'],
    ['::1', 'loopback'],
    ['::ffff:127.0.0.1', 'loopback'], // IPv4-mapped IPv6
    ['::ffff:a9fe:a9fe', 'link-local (cloud metadata)'], // 169.254.169.254, mapped and in hex
    ['fe80::1', 'link-local'],
    ['fd00:ec2::254', 'unique local (private)'], // AWS's IPv6 metadata address
    ['64:ff9b::7f00:1', 'NAT64'],
  ])('%s is refused (%s)', (ip, reason) => {
    expect(blockedAddressReason(ip)).toBe(reason);
  });

  it.each(['93.184.215.14', '1.1.1.1', '2606:4700:4700::1111'])('%s is public', (ip) => {
    expect(blockedAddressReason(ip)).toBeNull();
  });
});

describe('assertPublicUrl(): when a monitor or webhook URL is saved', () => {
  it.each([
    ['http://127.0.0.1/', /127\.0\.0\.1 is a loopback address/],
    ['http://169.254.169.254/latest/meta-data/', /link-local/],
    ['http://[::1]:8080/', /::1 is a loopback address/],
    ['http://0x7f000001/', /loopback/], // odd encodings: the URL parser normalises them to 127.0.0.1
    ['http://2130706433/', /loopback/],
    ['http://[::ffff:127.0.0.1]/', /loopback/],
    ['http://intranet.test/', /intranet\.test resolves to 10\.1\.2\.3, a private address/],
    ['http://sneaky.test/', /resolves to 127\.0\.0\.1/],
    ['http://v6-local.test/', /unique local/],
    ['ftp://public.test/', /only http/],
    ['https://user:pass@public.test/', /user name or password/],
  ])('%s is refused', async (url, message) => {
    await expect(assertPublicUrl(url)).rejects.toThrow(message);
  });

  it('a public host passes; a host that does not resolve passes only when allowed (a monitor for a host that is down)', async () => {
    await expect(assertPublicUrl('https://public.test/health')).resolves.toBeInstanceOf(URL);
    await expect(assertPublicUrl('https://nowhere.test/')).rejects.toThrow(/ENOTFOUND/);
    await expect(assertPublicUrl('https://nowhere.test/', { allowUnresolved: true })).resolves.toBeInstanceOf(URL);
  });

  it('webhooks may be limited to ports 80 and 443', async () => {
    await expect(assertPublicUrl('https://public.test:6379/', { ports: [80, 443] })).rejects.toThrow(/only ports 80 and 443/);
    await expect(assertPublicUrl('https://public.test/', { ports: [80, 443] })).resolves.toBeInstanceOf(URL);
  });

  it('the development allow-list lets a named host:port through, and only that one', async () => {
    vi.stubEnv('OUTBOUND_ALLOWLIST', '127.0.0.1:4555');
    await expect(assertPublicUrl('http://127.0.0.1:4555/hooks')).resolves.toBeInstanceOf(URL);
    await expect(assertPublicUrl('http://127.0.0.1:4556/hooks')).rejects.toThrow(/loopback/);
  });
});

describe('safeFetch() and runCheck(): when the request is made', () => {
  let server: http.Server;
  let port = 0;

  beforeAll(async () => {
    server = http.createServer((req, res) => {
      if (req.url === '/to-metadata') {
        res.writeHead(302, { location: 'http://169.254.169.254/latest/meta-data/' });
        return res.end();
      }
      if (req.url === '/hop') {
        res.writeHead(302, { location: '/ok' });
        return res.end();
      }
      res.end('ok');
    });
    await new Promise<void>((r) => server.listen(0, '127.0.0.1', r));
    port = (server.address() as AddressInfo).port;
  });
  afterAll(() => new Promise<void>((r) => server.close(() => r())));

  it('a monitor pointing at loopback or the metadata service fails its check with the reason, and no request is made', async () => {
    const hits = vi.fn();
    server.on('request', hits);
    expect(await runCheck(`http://127.0.0.1:${port}/`)).toMatchObject({ ok: false, error: expect.stringMatching(/^Blocked: 127\.0\.0\.1 is a loopback address/) });
    expect(await runCheck('http://169.254.169.254/latest/meta-data/')).toMatchObject({ ok: false, error: expect.stringMatching(/^Blocked: .*link-local/) });
    server.off('request', hits);
    expect(hits).not.toHaveBeenCalled();
  });

  it('a name resolving to a private address is refused at connection time too (the check is the lookup)', async () => {
    const res = await runCheck(`http://intranet.test:${port}/`);
    expect(res).toMatchObject({ ok: false, error: expect.stringMatching(/Blocked: intranet\.test resolves to 10\.1\.2\.3/) });
  });

  it('a redirect to an internal address is checked again, and refused', async () => {
    vi.stubEnv('OUTBOUND_ALLOWLIST', `127.0.0.1:${port}`); // the first hop is our test server
    const res = await runCheck(`http://127.0.0.1:${port}/to-metadata`);
    expect(res).toMatchObject({ ok: false, error: expect.stringMatching(/Blocked: .*169\.254\.169\.254.*link-local/) });
    expect(await runCheck(`http://127.0.0.1:${port}/hop`)).toMatchObject({ ok: true, statusCode: 200 }); // a harmless hop is followed
  });

  it('webhooks do not follow redirects at all: the 3xx is the answer', async () => {
    vi.stubEnv('OUTBOUND_ALLOWLIST', `127.0.0.1:${port}`);
    const res = await safeFetch(`http://127.0.0.1:${port}/hop`, { method: 'POST' }, { maxRedirects: 0 });
    expect(res.status).toBe(302);
  });

  it('BlockedUrlError is what callers catch', async () => {
    await expect(safeFetch('http://10.0.0.1/')).rejects.toBeInstanceOf(BlockedUrlError);
  });
});
