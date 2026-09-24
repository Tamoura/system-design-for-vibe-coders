import type { Metadata } from 'next';
import Link from 'next/link';
import { emailsMatch } from '@/core/invitations';
import { findInvitationByToken } from '@/lib/invitations';
import { getCurrentUser } from '@/lib/session';
import { signOutAction } from '../../(auth)/actions';
import { AcceptForm } from './accept-form';

export const dynamic = 'force-dynamic';
// The token is in this URL: don't send it to other sites in the Referer header.
export const metadata: Metadata = { referrer: 'no-referrer' };

/**
 * Lesson 1.2 (🟡): one link for new and existing users.
 *  - Signed out: sign up (email pre-filled) or sign in, then come back here.
 *  - Signed in as someone else: say so, and offer to switch accounts.
 *  - Signed in as the invited email: one button to accept.
 */
export default async function InvitePage({ params }: { params: Promise<{ token: string }> }) {
  const { token } = await params;
  const invite = await findInvitationByToken(token);
  if (!invite || invite.state !== 'pending') {
    return (
      <section className="card" style={{ maxWidth: 520 }}>
        <h1>Invitation not valid</h1>
        <p className="muted">This invitation is invalid, expired, revoked or already used. Ask for a new one.</p>
      </section>
    );
  }
  const user = await getCurrentUser();
  const here = `/invite/${token}`;
  return (
    <section className="card grid" style={{ maxWidth: 520 }}>
      <h1 style={{ margin: 0 }}>Join {invite.orgName}</h1>
      <p className="muted" style={{ margin: 0 }}>
        You have been invited as <strong>{invite.role}</strong> ({invite.email}).
      </p>
      {!user && (
        <div className="row">
          <Link className="btn" href={`/signup?email=${encodeURIComponent(invite.email)}&next=${encodeURIComponent(here)}`}>Create an account</Link>
          <Link href={`/login?next=${encodeURIComponent(here)}`}>I already have an account</Link>
        </div>
      )}
      {user && !emailsMatch(user.email, invite.email) && (
        <>
          <p className="error" style={{ margin: 0 }}>
            This invitation was sent to {invite.email}, but you are signed in as {user.email}.
          </p>
          <form action={signOutAction}><input type="hidden" name="next" value={here} /><button className="btn secondary">Sign out and switch account</button></form>
        </>
      )}
      {user && emailsMatch(user.email, invite.email) && <AcceptForm token={token} />}
    </section>
  );
}
