import { beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));

import { db, schema } from '@/db';
import { createMonitor, getMonitor } from '@/lib/monitors';
import * as monitorsRoute from '@/app/api/orgs/[orgSlug]/monitors/route';
import * as monitorRoute from '@/app/api/orgs/[orgSlug]/monitors/[id]/route';
import * as membersRoute from '@/app/api/orgs/[orgSlug]/members/route';
import * as memberRoute from '@/app/api/orgs/[orgSlug]/members/[userId]/route';
import { makeOrg, makeUser, signInAs } from './helpers/fixtures';

/*
 * Lesson 1.3 (🟡): "an automated test calls each endpoint as each role and
 * checks the expected status codes". This table is the authorization spec for
 * the API; the loop below turns every cell into a test.
 */
type Actor = 'owner' | 'admin' | 'member' | 'viewer' | 'outsider' | 'anonymous';
const ACTORS: Actor[] = ['owner', 'admin', 'member', 'viewer', 'outsider', 'anonymous'];

//                                            owner admin member viewer outsider anon
const MATRIX: Record<string, number[]> = {
  'GET    /monitors':                         [200,  200,  200,   200,   404,     401],
  'POST   /monitors':                         [201,  201,  201,   403,   404,     401],
  'GET    /monitors/:id':                     [200,  200,  200,   200,   404,     401],
  'PATCH  /monitors/:id (someone else’s)':    [200,  200,  403,   403,   404,     401],
  'PATCH  /monitors/:id (the member’s own)':  [200,  200,  200,   403,   404,     401],
  'DELETE /monitors/:id':                     [204,  204,  403,   403,   404,     401],
  'GET    /members':                          [200,  200,  200,   200,   404,     401],
  'PATCH  /members/:userId (viewer→member)':  [200,  200,  403,   403,   404,     401],
};

let acme: Awaited<ReturnType<typeof makeOrg>>;
let globex: Awaited<ReturnType<typeof makeOrg>>;

beforeAll(async () => {
  acme = await makeOrg('Acme');
  globex = await makeOrg('Globex');
});

const json = (method: string, body?: unknown) =>
  new Request('http://test', { method, headers: { 'content-type': 'application/json' }, body: body === undefined ? undefined : JSON.stringify(body) });
const p = <T extends object>(params: T) => ({ params: Promise.resolve(params) });

function signInAsActor(actor: Actor) {
  if (actor === 'anonymous') return signInAs(null);
  signInAs(actor === 'outsider' ? globex.users.owner : acme.users[actor]);
}

async function acmeMonitor(createdBy: 'owner' | 'member') {
  const user = acme.users[createdBy];
  return createMonitor({ orgId: acme.id, userId: user.id }, { name: `by ${createdBy}`, url: 'https://acme.test', intervalSeconds: 300 });
}

/** Performs one request as `actor`. Fixtures are created fresh, so successful writes don't affect other cells. */
const CALLS: Record<string, (actor: Actor) => Promise<Response>> = {
  'GET    /monitors': async (actor) => {
    signInAsActor(actor);
    return monitorsRoute.GET(json('GET'), p({ orgSlug: acme.slug }));
  },
  'POST   /monitors': async (actor) => {
    signInAsActor(actor);
    return monitorsRoute.POST(json('POST', { name: 'New', url: 'https://new.test', intervalSeconds: 60 }), p({ orgSlug: acme.slug }));
  },
  'GET    /monitors/:id': async (actor) => {
    const m = await acmeMonitor('owner');
    signInAsActor(actor);
    return monitorRoute.GET(json('GET'), p({ orgSlug: acme.slug, id: m.id }));
  },
  'PATCH  /monitors/:id (someone else’s)': async (actor) => {
    const m = await acmeMonitor('owner');
    signInAsActor(actor);
    return monitorRoute.PATCH(json('PATCH', { name: 'Renamed' }), p({ orgSlug: acme.slug, id: m.id }));
  },
  'PATCH  /monitors/:id (the member’s own)': async (actor) => {
    const m = await acmeMonitor('member');
    signInAsActor(actor);
    return monitorRoute.PATCH(json('PATCH', { name: 'Renamed' }), p({ orgSlug: acme.slug, id: m.id }));
  },
  'DELETE /monitors/:id': async (actor) => {
    const m = await acmeMonitor('owner');
    signInAsActor(actor);
    return monitorRoute.DELETE(json('DELETE'), p({ orgSlug: acme.slug, id: m.id }));
  },
  'GET    /members': async (actor) => {
    signInAsActor(actor);
    return membersRoute.GET(json('GET'), p({ orgSlug: acme.slug }));
  },
  'PATCH  /members/:userId (viewer→member)': async (actor) => {
    const target = await makeUser('Target');
    await db.insert(schema.memberships).values({ organizationId: acme.id, userId: target.id, role: 'viewer' });
    signInAsActor(actor);
    return memberRoute.PATCH(json('PATCH', { role: 'member' }), p({ orgSlug: acme.slug, userId: target.id }));
  },
};

describe('API authorization matrix', () => {
  for (const [endpoint, statuses] of Object.entries(MATRIX)) {
    describe(endpoint.replace(/\s+/g, ' '), () => {
      ACTORS.forEach((actor, i) => {
        it(`${actor} → ${statuses[i]}`, async () => {
          const res = await CALLS[endpoint](actor);
          expect(res.status).toBe(statuses[i]);
        });
      });
    });
  }
});

describe('mass assignment: the body cannot choose the org, the author or a role', () => {
  it('POST ignores organizationId and createdBy in the body', async () => {
    signInAs(acme.users.member);
    const res = await monitorsRoute.POST(
      json('POST', { name: 'Sneaky', url: 'https://x.test', intervalSeconds: 60, organizationId: globex.id, orgId: globex.id, createdBy: globex.users.owner.id }),
      p({ orgSlug: acme.slug }),
    );
    expect(res.status).toBe(201);
    const { data } = await res.json();
    const row = await getMonitor({ orgId: acme.id }, data.id);
    expect(row).toMatchObject({ organizationId: acme.id, createdBy: acme.users.member.id });
  });

  it('PATCH ignores organizationId in the body', async () => {
    const m = await acmeMonitor('owner');
    signInAs(acme.users.owner);
    const res = await monitorRoute.PATCH(json('PATCH', { organizationId: globex.id, name: 'Still Acme' }), p({ orgSlug: acme.slug, id: m.id }));
    expect(res.status).toBe(200);
    expect(await getMonitor({ orgId: acme.id }, m.id)).toMatchObject({ name: 'Still Acme', organizationId: acme.id });
  });

  it('an admin cannot promote anyone to owner', async () => {
    signInAs(acme.users.admin);
    const res = await memberRoute.PATCH(json('PATCH', { role: 'owner' }), p({ orgSlug: acme.slug, userId: acme.users.member.id }));
    expect(res.status).toBe(403);
  });

  it('nobody can change their own role, not even an owner', async () => {
    signInAs(acme.users.owner);
    const res = await memberRoute.PATCH(json('PATCH', { role: 'viewer' }), p({ orgSlug: acme.slug, userId: acme.users.owner.id }));
    expect(res.status).toBe(403);
  });

  it('rejects an invalid body with 400', async () => {
    signInAs(acme.users.owner);
    const res = await monitorsRoute.POST(json('POST', { name: '', url: 'ftp://x', intervalSeconds: 7 }), p({ orgSlug: acme.slug }));
    expect(res.status).toBe(400);
  });
});

describe('response DTOs', () => {
  it('monitor responses contain exactly the DTO fields', async () => {
    const m = await acmeMonitor('owner');
    signInAs(acme.users.viewer);
    const { data } = await (await monitorRoute.GET(json('GET'), p({ orgSlug: acme.slug, id: m.id }))).json();
    expect(Object.keys(data).sort()).toEqual(['createdAt', 'id', 'intervalSeconds', 'name', 'paused', 'url']);
  });

  it('member responses contain exactly the DTO fields', async () => {
    signInAs(acme.users.viewer);
    const { data } = await (await membersRoute.GET(json('GET'), p({ orgSlug: acme.slug }))).json();
    expect(Object.keys(data[0]).sort()).toEqual(['email', 'joinedAt', 'name', 'role', 'userId']);
  });
});
