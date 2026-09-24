import { beforeAll, beforeEach, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));
vi.mock('@/lib/email', () => ({ sendEmail: vi.fn() }));

import { eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { hashToken, inviteState, MAX_INVITES_PER_ORG_PER_HOUR } from '@/core/invitations';
import { sendEmail } from '@/lib/email';
import { requireMembership, type OrgContext } from '@/lib/access';
import { acceptInvitation, createInvitation, resendInvitation, revokeInvitation } from '@/lib/invitations';
import { makeOrg, makeUser, signInAs } from './helpers/fixtures';

/** The token only exists in the emailed link; fish it out of the last "email". */
function lastEmailedToken(): string {
  const text = vi.mocked(sendEmail).mock.lastCall![0].text;
  return text.match(/\/invite\/([\w-]+)/)![1];
}

let acme: Awaited<ReturnType<typeof makeOrg>>;
let owner: OrgContext;
let admin: OrgContext;

beforeAll(async () => {
  acme = await makeOrg('Acme');
  signInAs(acme.users.owner);
  owner = await requireMembership(acme.slug);
  signInAs(acme.users.admin);
  admin = await requireMembership(acme.slug);
});
beforeEach(() => vi.mocked(sendEmail).mockClear());

describe('invitation tokens', () => {
  it('stores only a hash of the token, and expires in 7 days', async () => {
    const inv = await createInvitation(owner, { email: 'hash@acme.test', role: 'member' });
    const token = lastEmailedToken();
    expect(inv.tokenHash).toBe(hashToken(token));
    expect(inv.tokenHash).not.toContain(token);
    const days = (inv.expiresAt.getTime() - Date.now()) / 86_400_000;
    expect(days).toBeGreaterThan(6.9);
    expect(days).toBeLessThanOrEqual(7);
  });

  it('knows expired, revoked and accepted apart', () => {
    const past = new Date(Date.now() - 1000);
    const future = new Date(Date.now() + 1000);
    expect(inviteState({ acceptedAt: null, revokedAt: null, expiresAt: future })).toBe('pending');
    expect(inviteState({ acceptedAt: null, revokedAt: null, expiresAt: past })).toBe('expired');
    expect(inviteState({ acceptedAt: null, revokedAt: past, expiresAt: future })).toBe('revoked');
    expect(inviteState({ acceptedAt: past, revokedAt: null, expiresAt: future })).toBe('accepted');
  });
});

describe('accepting', () => {
  it('creates a membership with the invited role, once', async () => {
    const sam = await makeUser('Sam', { emailVerified: false });
    await createInvitation(owner, { email: sam.email, role: 'viewer' });
    const token = lastEmailedToken();

    await expect(acceptInvitation(token, sam)).resolves.toEqual({ orgSlug: acme.slug });
    const [m] = await db.select().from(schema.memberships).where(eq(schema.memberships.userId, sam.id));
    expect(m).toMatchObject({ organizationId: acme.id, role: 'viewer' });
    // The click proves the invitee controls the address.
    const [u] = await db.select().from(schema.users).where(eq(schema.users.id, sam.id));
    expect(u.emailVerified).toBe(true);

    await expect(acceptInvitation(token, sam)).rejects.toThrow(/already used/);
  });

  it('refuses a user signed in with a different email, without using up the invite', async () => {
    const work = await makeUser('Work');
    const personal = await makeUser('Personal');
    await createInvitation(owner, { email: work.email, role: 'member' });
    const token = lastEmailedToken();
    await expect(acceptInvitation(token, personal)).rejects.toThrow(/sent to/);
    await expect(acceptInvitation(token, work)).resolves.toBeTruthy();
  });

  it('refuses expired and revoked invitations', async () => {
    const late = await makeUser('Late');
    const inv = await createInvitation(owner, { email: late.email, role: 'member' });
    const token = lastEmailedToken();
    await db.update(schema.invitations).set({ expiresAt: new Date(Date.now() - 1000) }).where(eq(schema.invitations.id, inv.id));
    await expect(acceptInvitation(token, late)).rejects.toThrow(/expired/);

    const gone = await makeUser('Gone');
    const inv2 = await createInvitation(owner, { email: gone.email, role: 'member' });
    const token2 = lastEmailedToken();
    await revokeInvitation(owner, inv2.id);
    await expect(acceptInvitation(token2, gone)).rejects.toThrow(/revoked/);
  });

  it('resend issues a new token and kills the old one', async () => {
    const pat = await makeUser('Pat');
    const inv = await createInvitation(owner, { email: pat.email, role: 'member' });
    const oldToken = lastEmailedToken();
    await resendInvitation(owner, inv.id);
    const newToken = lastEmailedToken();
    expect(newToken).not.toBe(oldToken);
    await expect(acceptInvitation(oldToken, pat)).rejects.toThrow();
    await expect(acceptInvitation(newToken, pat)).resolves.toBeTruthy();
  });
});

describe('who may invite', () => {
  it('an admin cannot invite an owner', async () => {
    await expect(createInvitation(admin, { email: 'boss@acme.test', role: 'owner' })).rejects.toThrow(/cannot invite/);
    await expect(createInvitation(admin, { email: 'peer@acme.test', role: 'admin' })).resolves.toBeTruthy();
  });

  it('an unverified user cannot send invitations', async () => {
    await expect(createInvitation({ ...owner, emailVerified: false }, { email: 'x@acme.test', role: 'member' })).rejects.toThrow(/Confirm/);
  });

  it('cannot invite someone twice or invite an existing member', async () => {
    await createInvitation(owner, { email: 'twice@acme.test', role: 'member' });
    await expect(createInvitation(owner, { email: 'twice@acme.test', role: 'member' })).rejects.toThrow(/Resend/);
    await expect(createInvitation(owner, { email: acme.users.viewer.email, role: 'member' })).rejects.toThrow(/already a member/);
  });

  it('is rate-limited per organization', async () => {
    const globex = await makeOrg('Globex');
    signInAs(globex.users.owner);
    const ctx = await requireMembership(globex.slug);
    for (let i = 0; i < MAX_INVITES_PER_ORG_PER_HOUR; i++) {
      await createInvitation(ctx, { email: `bulk${i}@globex.test`, role: 'viewer' });
    }
    await expect(createInvitation(ctx, { email: 'one-more@globex.test', role: 'viewer' })).rejects.toThrow(/last hour/);
    // Other organizations are not affected.
    await expect(createInvitation(owner, { email: 'still-fine@acme.test', role: 'viewer' })).resolves.toBeTruthy();
  });
});
