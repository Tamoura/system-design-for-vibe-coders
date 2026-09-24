import Link from 'next/link';
import { ResetPasswordForm } from './reset-form';

// Better Auth checks the emailed link, then redirects here with ?token=… (or ?error=INVALID_TOKEN).
export default async function ResetPasswordPage({ searchParams }: { searchParams: Promise<Record<string, string | undefined>> }) {
  const { token, error } = await searchParams;
  return (
    <section style={{ maxWidth: 420 }}>
      <h1>Choose a new password</h1>
      {token && !error ? (
        <ResetPasswordForm token={token} />
      ) : (
        <div className="card">
          This reset link is invalid, expired or already used. <Link href="/forgot-password">Ask for a new one</Link>.
        </div>
      )}
    </section>
  );
}
