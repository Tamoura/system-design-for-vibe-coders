import Link from 'next/link';
import { safeRedirect } from '@/core/safe-redirect';
import { SignUpForm } from './signup-form';

export default async function SignUpPage({ searchParams }: { searchParams: Promise<Record<string, string | undefined>> }) {
  const params = await searchParams;
  const next = safeRedirect(params.next);
  return (
    <section style={{ maxWidth: 420 }}>
      <h1>Create your account</h1>
      <SignUpForm next={next} email={params.email ?? ''} />
      <p className="muted">
        Already have an account? <Link href={`/login?next=${encodeURIComponent(next)}`}>Sign in</Link>
      </p>
    </section>
  );
}
