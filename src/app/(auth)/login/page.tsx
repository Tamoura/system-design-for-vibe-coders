import Link from 'next/link';
import { safeRedirect } from '@/core/safe-redirect';
import { LoginForm } from './login-form';

export default async function LoginPage({ searchParams }: { searchParams: Promise<Record<string, string | undefined>> }) {
  const params = await searchParams;
  const next = safeRedirect(params.next);
  return (
    <section style={{ maxWidth: 420 }}>
      <h1>Sign in</h1>
      <LoginForm next={next} />
      <p className="muted">
        New to Beacon? <Link href={`/signup?next=${encodeURIComponent(next)}`}>Create an account</Link>
      </p>
    </section>
  );
}
