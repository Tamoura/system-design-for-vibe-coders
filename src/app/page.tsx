import Link from 'next/link';

export default function Home() {
  return (
    <section className="grid" style={{ gap: '1.2rem' }}>
      <h1>Know your site is down before your customers do.</h1>
      <p className="muted">
        Beacon checks your URLs every few minutes, opens an incident when they fail, and keeps a public
        status page up to date. This is the <strong>starter</strong>: the core product works, and every generic
        SaaS component is a TODO for you to build, lesson by lesson.
      </p>
      <div className="row">
        <Link className="btn" href="/signup">Create an account</Link>
        <Link href="/dashboard">Open the dashboard</Link>
        <Link href="/status/demo">See a status page →</Link>
      </div>
      {/* TODO(6.1): this is the marketing site. It will move to its own route group with pricing (3.2). */}
    </section>
  );
}
