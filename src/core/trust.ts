/*
 * Lesson 8.1: the trust material, as data. The /trust page, security.txt and
 * docs/security/ read from here, so the subprocessor list a customer's lawyer
 * reads is the same one the engineers edit when they add a vendor.
 *
 * Rule (lesson 8.1, "Forgetting subprocessors"): a new vendor that receives
 * customer personal data is added HERE, in the same pull request that adds the
 * integration, and customers are told before it goes live (the DPA says 30 days).
 */

export type Subprocessor = {
  name: string;
  purpose: string;
  /** What customer data it receives. */
  data: string;
  location: string;
  /** Only when the org (or Beacon's operator) turns the feature on. */
  when: string;
};

export const SUBPROCESSORS: Subprocessor[] = [
  { name: 'Your cloud provider (e.g. AWS, Hetzner, Fly.io)', purpose: 'Hosting: app servers, Postgres, object storage, backups', data: 'All customer data, encrypted at rest', location: 'The region you deploy to', when: 'Always' },
  { name: 'Stripe', purpose: 'Payments and invoices (lesson 3.1)', data: 'Billing contact, organization name, plan and usage counts', location: 'USA / EU', when: 'Paid plans' },
  { name: 'Resend (or your SMTP provider)', purpose: 'Transactional and alert email (lesson 4.1)', data: 'Recipient email address, email content', location: 'USA', when: 'Always' },
  { name: 'Twilio', purpose: 'SMS alerts (lesson 4.2)', data: 'Phone number, alert text', location: 'USA', when: 'Orgs with SMS alerts' },
  { name: 'Slack', purpose: 'Alerts to a Slack channel (lesson 4.2)', data: 'Alert text', location: 'USA', when: 'Orgs that connect Slack' },
  { name: 'PostHog', purpose: 'Product analytics (lesson 6.2)', data: 'Pseudonymous user and org ids, event names; no email or monitor content', location: 'EU or USA', when: 'When configured by the operator' },
  { name: 'Sentry', purpose: 'Error tracking (lesson 7.2)', data: 'Stack traces, request ids; personal data scrubbed', location: 'EU or USA', when: 'When configured by the operator' },
  {
    name: 'Anthropic',
    purpose: 'AI incident summaries (lesson 8.2)',
    data: 'The incident being summarised: monitor name and URL, check results, error text, timeline notes. Not used to train models.',
    location: 'USA',
    when: 'Only orgs that turn on AI summaries (off by default)',
  },
];

/**
 * Lesson 8.1 (🔴 section): security.txt, RFC 9116. `Contact` and `Expires` are
 * required. Expires must be less than a year away; a test fails 30 days before
 * this date so someone renews it (a stale security.txt is a sign nobody reads it).
 */
export const SECURITY_TXT_EXPIRES = '2027-06-30T00:00:00.000Z';

export function securityTxt(opts: { appUrl: string; contact: string }): string {
  const base = opts.appUrl.replace(/\/$/, '');
  return [
    `Contact: ${opts.contact}`,
    `Expires: ${SECURITY_TXT_EXPIRES}`,
    `Policy: ${base}/trust#disclosure`,
    'Preferred-Languages: en',
    `Canonical: ${base}/.well-known/security.txt`,
    '',
  ].join('\n');
}

/** The security contact: SECURITY_CONTACT (a mailto: or https: URI), else the placeholder address. */
export function securityContact(env: Record<string, string | undefined> = process.env): string {
  return env.SECURITY_CONTACT || 'mailto:security@beacon.dev';
}
