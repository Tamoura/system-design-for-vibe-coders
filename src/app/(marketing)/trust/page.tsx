import type { Metadata } from 'next';
import Link from 'next/link';
import { SUBPROCESSORS } from '@/core/trust';
import { ORG_DELETION_GRACE_DAYS, OTHER_RETENTION, RETENTION_RULES } from '@/core/retention';

export const metadata: Metadata = { title: 'Trust and security — Beacon' };
// Lesson 6.1: static, like the rest of the marketing site (and listed in STATIC_PAGES for its CSP, lesson 8.1).
export const dynamic = 'error';

/**
 * Lesson 8.1: the trust center, "the page that answers the security
 * questionnaire before it is sent". A starting point, drawn from the same
 * data as the code (src/core/trust.ts): who processes customer data, how it
 * is protected, how long it is kept, and how to report a vulnerability.
 * A real one adds the SOC 2 report behind an NDA click-through and the DPA.
 */
export default function TrustPage() {
  return (
    <div className="grid" style={{ gap: '1.5rem' }}>
      <h1 style={{ margin: 0 }}>Trust and security</h1>
      <p className="lead" style={{ margin: 0 }}>
        Customers trust Beacon with their URLs, their incidents and their alert contacts. This page says who else sees that data, how we
        protect it and how long we keep it.
      </p>

      <section className="card grid" aria-labelledby="subprocessors">
        <h2 id="subprocessors" style={{ margin: 0 }}>Subprocessors</h2>
        <p className="muted" style={{ margin: 0 }}>
          Vendors that process customer personal data on our behalf. We give 30 days’ notice before adding one.
        </p>
        <table data-testid="subprocessors">
          <thead>
            <tr><th>Vendor</th><th>Purpose</th><th>Data</th><th>Location</th><th>When</th></tr>
          </thead>
          <tbody>
            {SUBPROCESSORS.map((s) => (
              <tr key={s.name}><td><strong>{s.name}</strong></td><td>{s.purpose}</td><td>{s.data}</td><td>{s.location}</td><td>{s.when}</td></tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="card grid" aria-labelledby="practices">
        <h2 id="practices" style={{ margin: 0 }}>How we protect your data</h2>
        <ul style={{ margin: 0 }}>
          <li>Every organization’s data is separated by the application and again by Postgres row-level security.</li>
          <li>Webhook signing secrets and Slack webhook URLs are encrypted by the application (AES-256-GCM, envelope encryption with rotatable keys); API keys are stored only as hashes.</li>
          <li>TLS everywhere, HSTS, a strict Content-Security-Policy, and an SSRF guard on every URL Beacon fetches for you.</li>
          <li>Every sensitive change is written to a tamper-evident audit log, visible to your admins on Pro and Business.</li>
          <li>Secrets never live in our repository: gitleaks runs on every commit and in CI; dependencies and images are scanned for known vulnerabilities.</li>
          <li>AI incident summaries are off by default, per organization; drafts are never published without a person clicking Publish.</li>
        </ul>
      </section>

      <section className="card grid" aria-labelledby="privacy">
        <h2 id="privacy" style={{ margin: 0 }}>Your data, your choice</h2>
        <ul style={{ margin: 0 }}>
          <li>Every user can download their personal data and delete their account from <strong>Account settings</strong>.</li>
          <li>Organization owners can export all of the organization’s data as JSON and delete the organization from <strong>Settings → Data &amp; privacy</strong>. Deletion happens after a {ORG_DELETION_GRACE_DAYS}-day grace period and removes the data from our database and file storage.</li>
          {Object.values(RETENTION_RULES).map((r) => (
            <li key={r.table}>{r.data}: kept {r.days} days.</li>
          ))}
          {OTHER_RETENTION.map((r) => (
            <li key={r.data}>{r.data}: {r.rule}</li>
          ))}
        </ul>
      </section>

      <section className="card grid" aria-labelledby="disclosure-title" id="disclosure">
        <h2 id="disclosure-title" style={{ margin: 0 }}>Reporting a vulnerability</h2>
        <p style={{ margin: 0 }}>
          Please report security issues privately. Contact details are in our <a href="/.well-known/security.txt">security.txt</a>. We
          acknowledge reports within two business days, do not pursue good-faith research, and credit you if you wish.
        </p>
      </section>

      <p className="muted">
        Live uptime: <Link href="/status/demo">our own status page</Link>.
      </p>
    </div>
  );
}
