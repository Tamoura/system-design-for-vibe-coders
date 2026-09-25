import Link from 'next/link';

// Lesson 6.1: static HTML, built once. Anything per-request here fails the build.
export const dynamic = 'error';

export default function Home() {
  return (
    <div className="grid marketing" style={{ gap: '2.5rem' }}>
      <section className="hero grid">
        <h1>Know your site is down before your customers do.</h1>
        <p className="lead">
          Beacon checks your URLs on a schedule, opens an incident when they fail, alerts your team by email, Slack
          or SMS, and keeps a public status page up to date.
        </p>
        <div className="row">
          {/* The one call to action: sign up. Onboarding takes it from there. */}
          <Link className="btn btn-lg" href="/signup">Start monitoring for free</Link>
          <Link href="/pricing">See pricing →</Link>
        </div>
        <p className="muted">Free plan: 5 monitors, checked every 5 minutes. No credit card.</p>
      </section>
      <section className="features" aria-label="Features">
        <div className="card">
          <h2>Checks on a schedule</h2>
          <p>From every 30 seconds to every 15 minutes, spread across the minute so your servers never see a spike.</p>
        </div>
        <div className="card">
          <h2>Incidents that page the right people</h2>
          <p>Three failures in a row open an incident. Email, Slack, SMS and escalation policies do the rest.</p>
        </div>
        <div className="card">
          <h2>A status page your customers trust</h2>
          <p>Publish it in one click, with your logo. Visitors subscribe to updates.</p>
        </div>
        <div className="card">
          <h2>An API and webhooks</h2>
          <p>Manage monitors from your own tools and get signed incident events.</p>
        </div>
      </section>
      <section className="card grid" style={{ justifyItems: 'start' }}>
        <h2 style={{ margin: 0 }}>Set up in two minutes</h2>
        <ol className="steps">
          <li>Create your account.</li>
          <li>Paste the URL to watch: Beacon checks it within a minute.</li>
          <li>Connect Slack or invite a teammate, then publish your status page.</li>
        </ol>
        <Link className="btn" href="/signup">Create your account</Link>
      </section>
    </div>
  );
}
