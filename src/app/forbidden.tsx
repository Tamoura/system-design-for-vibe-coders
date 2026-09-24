import Link from 'next/link';

// Lesson 1.3: shown (with HTTP 403) when you are in the org but your role lacks the permission.
export default function Forbidden() {
  return (
    <section className="card">
      <h1>You don&apos;t have permission to do that</h1>
      <p className="muted">Your role in this organization does not allow it. Ask an owner or admin if you need access.</p>
      <Link href="/dashboard">Back to the dashboard</Link>
    </section>
  );
}
