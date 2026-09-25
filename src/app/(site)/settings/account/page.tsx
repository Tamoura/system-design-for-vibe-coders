import { headers } from 'next/headers';
import { auth, githubEnabled } from '@/lib/auth';
import { requireUser } from '@/lib/session';
import { linkGithubAction, resendVerificationAction } from './actions';

export const dynamic = 'force-dynamic';

export default async function AccountPage({ searchParams }: { searchParams: Promise<Record<string, string | undefined>> }) {
  const user = await requireUser('/settings/account');
  const params = await searchParams;
  const logins = await auth.api.listUserAccounts({ headers: await headers() });
  const hasGithub = logins.some((a) => a.providerId === 'github');
  return (
    <section className="grid" style={{ maxWidth: 560 }}>
      {/* Lesson 6.1 (🟡): the USER's settings, the same in every org, so not under /[org]/settings. */}
      <h1 style={{ margin: 0 }}>Your account</h1>
      <div className="card grid">
        <div><strong>{user.name}</strong> · {user.email}</div>
        {user.emailVerified ? (
          <div className="muted">Email confirmed.</div>
        ) : (
          <form action={resendVerificationAction} className="row">
            <span className="error">Email not confirmed yet. You need a confirmed email to invite teammates.</span>
            <button className="btn secondary">Resend the link</button>
          </form>
        )}
        {params.verification === 'sent' && <div className="muted">Sent. Check your inbox (in development: Mailpit at http://localhost:8025).</div>}
      </div>
      <div className="card grid">
        <strong>Ways to sign in</strong>
        <ul style={{ margin: 0 }}>
          {logins.map((a) => (
            <li key={a.id}>{a.providerId === 'credential' ? 'Email and password' : a.providerId}</li>
          ))}
        </ul>
        {githubEnabled && !hasGithub && (
          <form action={linkGithubAction}>
            <button className="btn secondary">Link GitHub</button>
          </form>
        )}
        {params.error && <div className="error">Could not link GitHub ({params.error}). GitHub must report the same, verified email.</div>}
      </div>
      <p className="muted">Alert preferences (which incidents reach you by email or SMS) are per organization: open one and choose “My alert preferences”.</p>
    </section>
  );
}
