import { createHash, randomBytes } from 'node:crypto';

/*
 * Lesson 1.2 (🟡): the rules for invitation tokens. Same rules as a password
 * reset token (lesson 1.1): random, stored only as a hash, expiring, single use.
 */

export const INVITE_TTL_MS = 7 * 24 * 60 * 60 * 1000; // 7 days
/** Invitations send email from our domain to any address: cap them per org (lesson 1.2, invite spam). */
export const MAX_INVITES_PER_ORG_PER_HOUR = 20;

/** 256 random bits for the emailed link. Never stored, never logged by the app. */
export function newInviteToken(): string {
  return randomBytes(32).toString('base64url');
}

/**
 * What the database stores. A plain SHA-256 is enough here (unlike passwords)
 * because the token is 256 random bits: there is nothing to guess.
 */
export function hashToken(token: string): string {
  return createHash('sha256').update(token).digest('hex');
}

export type InviteState = 'pending' | 'accepted' | 'revoked' | 'expired';

export function inviteState(
  invite: { acceptedAt: Date | null; revokedAt: Date | null; expiresAt: Date },
  now = new Date(),
): InviteState {
  if (invite.acceptedAt) return 'accepted';
  if (invite.revokedAt) return 'revoked';
  if (invite.expiresAt <= now) return 'expired';
  return 'pending';
}

/**
 * Beacon's choice (lesson 1.2): the accepting user's email must match the
 * invited email, so a forwarded or leaked link is useless to anyone else.
 */
export function emailsMatch(a: string, b: string): boolean {
  return a.trim().toLowerCase() === b.trim().toLowerCase();
}
