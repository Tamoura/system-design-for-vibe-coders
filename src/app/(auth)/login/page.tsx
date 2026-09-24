import Link from 'next/link';
import { githubEnabled } from '@/lib/auth';
import { safeRedirect } from '@/core/safe-redirect';
import { signInWithGithubAction } from '../actions';
import { LoginForm } from './login-form';

/** Messages for the ?error= codes Better Auth adds when an OAuth sign-in fails. */
function oauthError(code: string | undefined) {
  if (!code) return null;
  if (code.includes('not_linked') || code.includes('not linked')) {
    return 'An account with this email already exists. Sign in with your password, then link GitHub from your account page.';
  }
  return 'Sign-in with GitHub failed. Try again, or use your email and password.';
}

export default async function LoginPage({ searchParams }: { searchParams: Promise<Record<string, string | undefined>> }) {
  const params = await searchParams;
  const next = safeRedirect(params.next);
  const error = oauthError(params.error);
  return (
    <section style={{ maxWidth: 420 }} className="grid">
      <h1 style={{ margin: 0 }}>Sign in</h1>
      {params.reset === 'done' && <div className="card">Password changed. Sign in with your new password.</div>}
      {error && <div className="card error">{error}</div>}
      <LoginForm next={next} />
      {githubEnabled && (
        <form action={signInWithGithubAction}>
          <input type="hidden" name="next" value={next} />
          <button className="btn secondary">Sign in with GitHub</button>
        </form>
      )}
      <p className="muted">
        <Link href="/forgot-password">Forgot your password?</Link> · New to Beacon?{' '}
        <Link href={`/signup?next=${encodeURIComponent(next)}`}>Create an account</Link>
      </p>
    </section>
  );
}
