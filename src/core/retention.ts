/*
 * Lesson 8.1 (GDPR, "Retention: decide how long you keep check results, logs
 * and deleted orgs' data, write it down, and enforce it with jobs (5.1)").
 *
 * This is the written-down part, as data: the nightly `retention.purge` job
 * (src/lib/privacy/retention.ts) enforces every row of RETENTION_RULES, the
 * trust page and docs/security/retention.md describe the same numbers. Change
 * a number here and both follow.
 */

export type RetentionRule = {
  /** What is deleted. */
  data: string;
  table: string;
  days: number;
  /** Why this long, in one line: the question a customer's DPO asks. */
  why: string;
};

export const RETENTION_RULES = {
  checkResults: { data: 'Check results (status, latency, error text)', table: 'check_results', days: 90, why: 'The dashboard shows 24 hours; 90 days covers uptime reports and incident reviews.' },
  webhookDeliveries: { data: 'Webhook events, messages and delivery attempts', table: 'webhook_events', days: 30, why: 'Long enough to debug and replay a failed delivery (lesson 5.3).' },
  notifications: { data: 'In-app notifications and their delivery log', table: 'notifications', days: 180, why: 'Who was told what, for an incident review; nobody reads older ones.' },
  emailOutbox: { data: 'Sent and failed emails (recipient, template, props)', table: 'email_outbox', days: 30, why: 'Enough to answer "did the email go out?"; the content is personal data.' },
  orgExports: { data: 'Organization export files', table: 'org_exports', days: 7, why: 'A full copy of an org is the last thing to leave lying around.' },
} as const satisfies Record<string, RetentionRule>;

/** Lesson 8.1: how long an org deletion can be cancelled. */
export const ORG_DELETION_GRACE_DAYS = 7;
export const ORG_EXPORT_TTL_DAYS = RETENTION_RULES.orgExports.days;

/**
 * Retention that lives elsewhere, listed so the documentation is complete:
 * the audit log by plan (lesson 7.3, src/core/plans.ts), backups and logs by
 * the platform's settings.
 */
export const OTHER_RETENTION = [
  { data: 'Audit log', rule: 'By plan: Business 365 days, Pro 30 days (then deleted by the nightly audit.retention job, lesson 7.3). Platform events: 2 years.' },
  { data: 'Deleted organizations', rule: `Recoverable for ${ORG_DELETION_GRACE_DAYS} days after an owner asks; then every row and file is deleted (org.delete job).` },
  { data: 'Database backups', rule: '30 days (docs/backup-and-restore.md); a deleted org disappears from backups as they age out.' },
  { data: 'Application logs', rule: '30 days at the log platform. Logs carry ids, never passwords, keys or AI prompt text (lesson 7.2 redaction).' },
  { data: 'Deleted user accounts', rule: 'Deleted at once. Audit events keep the name and email snapshot (evidence) until the audit retention removes them.' },
] as const;


export const DAY_MS = 86_400_000;

/** The moment before which a rule's rows are deleted. */
export function retentionCutoff(days: number, now: Date = new Date()): Date {
  return new Date(now.getTime() - days * DAY_MS);
}
