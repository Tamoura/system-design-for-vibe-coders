import { headers } from 'next/headers';
import { auth, githubEnabled } from '@/lib/auth';
import { requireUser } from '@/lib/session';
import { ConsentSetting } from '@/app/_components/analytics-consent';
import { accountDeletionPlan } from '@/lib/privacy/user-data';
import { deleteAccountAction, linkGithubAction, resendVerificationAction } from './actions';

export const dynamic = 'force-dynamic';

export default async function AccountPage({ searchParams }: { searchParams: Promise<Record<string, string | undefined>> }) {
  const user = await requireUser('/settings/account');
  const params = await searchParams;
  const logins = await auth.api.listUserAccounts({ headers: await headers() });
  const hasGithub = logins.some((a) => a.providerId === 'github');
  const deletion = await accountDeletionPlan(user.id); // lesson 8.1: what deleting would do, before anyone clicks
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
      <ConsentSetting />
      {/* Lesson 8.1 (GDPR Art. 15/20): access and portability. */}
      <div className="card grid" id="your-data">
        <strong>Your data</strong>
        <p className="muted" style={{ margin: 0 }}>
          Everything Beacon holds about you, across all your organizations: profile, sign-in methods and sessions, notifications and
          preferences, what you created and your actions in the audit log. One JSON file.
        </p>
        <div><a className="btn secondary" href="/api/account/export" data-testid="export-my-data">Download my data</a></div>
      </div>
      {/* Lesson 8.1 (GDPR Art. 17): erasure, with the org-ownership edge cases spelled out first. */}
      <div className="card grid" id="delete">
        <strong>Delete your account</strong>
        {deletion.orgsToLeave.length > 0 && <p className="muted" style={{ margin: 0 }}>You will leave: {deletion.orgsToLeave.map((o) => o.name).join(', ')}. What you created there stays with the organization; API keys you created are revoked.</p>}
        {deletion.orgsToDelete.length > 0 && (
          <p className="muted" style={{ margin: 0 }}>
            You are the only member of {deletion.orgsToDelete.map((o) => o.name).join(', ')}: {deletion.orgsToDelete.length === 1 ? 'it is' : 'they are'} deleted
            too, after a 7-day grace period.
          </p>
        )}
        {deletion.blockers.length > 0 ? (
          <ul className="error" style={{ margin: 0 }} data-testid="delete-blockers">
            {deletion.blockers.map((b) => <li key={b}>{b}</li>)}
          </ul>
        ) : (
          <form action={deleteAccountAction} className="row">
            <label htmlFor="confirmEmail" className="muted">Type <strong>{user.email}</strong> to confirm</label>
            <input id="confirmEmail" name="confirmEmail" autoComplete="off" required style={{ flex: 1 }} />
            <button className="btn danger" data-testid="delete-account">Delete my account</button>
          </form>
        )}
        {params.delete_error && <div className="error" role="alert">{params.delete_error}</div>}
      </div>
      <p className="muted">Alert preferences (which incidents reach you by email or SMS) are per organization: open one and choose “My alert preferences”.</p>
    </section>
  );
}
