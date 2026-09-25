import { z } from 'zod';

/*
 * Lesson 7.4 (🟢): twelve-factor configuration. Everything that changes
 * between environments (local, preview, staging, production) comes from
 * environment variables, and this schema checks them ONCE, at startup:
 *
 *   the web app      src/instrumentation.ts register()
 *   the worker       scripts/worker.ts
 *   migrations       scripts/migrate.ts (the release step)
 *
 * A missing or malformed variable stops the process with a message that names
 * it ("DATABASE_URL: required: the Postgres connection string…") instead of
 * failing at 3 a.m. on the first request that needs it. The same image then
 * runs in every environment with different variables (build once, promote).
 *
 * Every variable has a description: `npm run env:docs` turns this schema into
 * docs/configuration.md, so the self-hosting docs cannot drift from the code.
 * Beacon code still reads process.env where it needs a value; this module is
 * the gate and the documentation, not a second place to look values up.
 */

const optionalUrl = (description: string) => z.string().url().optional().describe(description);
const flag = (values: readonly [string, ...string[]], description: string) => z.enum(values).optional().describe(description);

export const envSchema = z
  .object({
    NODE_ENV: z.enum(['development', 'test', 'production']).default('development').describe('Set by Next.js and Node tooling. `production` for `next start` and the Docker image.'),
    APP_ENV: flag(['development', 'preview', 'staging', 'production'], 'Which environment this is (lesson 7.4). Tags logs, traces and errors; `production` refuses development-only settings.'),
    APP_URL: z.string().url().default('http://localhost:3000').describe('The public URL of the app, used in emails and redirects. https:// makes cookies Secure.'),
    APP_RELEASE: z.string().min(1).optional().describe('The release: the git SHA the image was built from (set by the Dockerfile). Tags errors and traces.'),

    DATABASE_URL: z
      .string({ error: 'required: the Postgres connection string, e.g. postgres://beacon:beacon@localhost:5432/beacon' })
      .regex(/^postgres(ql)?:\/\//, 'must start with postgres:// or postgresql://')
      .describe('Required. Postgres 16 connection string (lesson 2.1). The worker and migrations use it too.'),
    BETTER_AUTH_SECRET: z.string().min(32, 'use at least 32 characters (openssl rand -base64 32)').optional().describe('Required in production. Signs session cookies and tokens (lesson 1.1).'),
    GITHUB_CLIENT_ID: z.string().optional().describe('Optional: "Sign in with GitHub" (with GITHUB_CLIENT_SECRET).'),
    GITHUB_CLIENT_SECRET: z.string().optional().describe('Optional: see GITHUB_CLIENT_ID.'),

    STORAGE_DRIVER: flag(['local', 's3'], 'Where uploaded files go (lesson 2.2). `local` (default): STORAGE_LOCAL_DIR. `s3`: any S3-compatible store.'),
    STORAGE_LOCAL_DIR: z.string().optional().describe('Directory for the local storage driver. Default `.storage`; a volume in Docker.'),
    STORAGE_LOCAL_SECRET: z.string().optional().describe('Signs local download URLs. Defaults to BETTER_AUTH_SECRET.'),
    S3_BUCKET: z.string().optional().describe('With STORAGE_DRIVER=s3: the bucket.'),
    S3_REGION: z.string().optional().describe('With STORAGE_DRIVER=s3: the region (`auto` for R2).'),
    S3_ENDPOINT: optionalUrl('With STORAGE_DRIVER=s3: the endpoint of a non-AWS store (R2, Garage, SeaweedFS).'),
    S3_FORCE_PATH_STYLE: flag(['true', 'false'], 'With STORAGE_DRIVER=s3: path-style URLs (most self-hosted stores).'),
    S3_ACCESS_KEY_ID: z.string().optional().describe('With STORAGE_DRIVER=s3.'),
    S3_SECRET_ACCESS_KEY: z.string().optional().describe('With STORAGE_DRIVER=s3.'),

    BILLING_PROVIDER: flag(['fake'], 'Development only: an in-memory stand-in for Stripe (lesson 3.1). Refused when APP_ENV=production.'),
    BILLING_TRIAL_DAYS: z.coerce.number().int().min(0).max(90).optional().describe('Free trial days for new subscriptions (0 = none). Support can extend a trial (lesson 7.1).'),
    STRIPE_SECRET_KEY: z.string().startsWith('sk_', 'must start with sk_').optional().describe('Optional: Stripe billing. Without it (and without BILLING_PROVIDER) billing is off and every org is on Free.'),
    STRIPE_WEBHOOK_SECRET: z.string().optional().describe('With Stripe: the webhook signing secret (whsec_…).'),
    STRIPE_PRICE_PRO: z.string().optional().describe('With Stripe: the Pro plan Price id.'),
    STRIPE_PRICE_BUSINESS: z.string().optional().describe('With Stripe: the Business plan Price id.'),

    EMAIL_DRIVER: flag(['smtp', 'resend', 'console', 'memory'], 'How email is sent (lesson 4.1). Default: smtp (SMTP_URL), or resend when RESEND_API_KEY is set.'),
    SMTP_URL: z.string().optional().describe('SMTP server, e.g. smtp://localhost:1025 (Mailpit).'),
    RESEND_API_KEY: z.string().optional().describe('Optional: send through Resend.'),
    EMAIL_FROM: z.string().optional().describe('From address of transactional email.'),
    EMAIL_FROM_STATUS: z.string().optional().describe('From address of status-page subscriber email.'),
    EMAIL_WEBHOOK_SECRET: z.string().optional().describe('Signing secret of the email provider’s bounce webhook.'),
    SMS_PROVIDER: flag(['fake'], 'Development: print SMS instead of sending (lesson 4.2). Twilio: set the TWILIO_* variables.'),
    SLACK_PROVIDER: flag(['fake'], 'Development: print Slack messages instead of posting them.'),
    OUTBOUND_ALLOWLIST: z.string().optional().describe('Development only: host:port pairs the SSRF guard lets through (lesson 5.3). Must be empty in production.'),
    ANALYTICS_DRIVER: flag(['posthog'], 'Optional: forward product events to PostHog (lesson 6.2).'),
    POSTHOG_API_KEY: z.string().optional().describe('With ANALYTICS_DRIVER=posthog.'),
    FLAGS_REFRESH_SECONDS: z.coerce.number().int().min(1).optional().describe('How often each process reloads feature-flag rules (lesson 6.3). Default 15.'),

    LOG_LEVEL: flag(['trace', 'debug', 'info', 'warn', 'error', 'fatal', 'silent'], 'Log level (lesson 7.2). Default `info`. Logs are JSON lines on stdout.'),
    SENTRY_DSN: optionalUrl('Optional: send server errors to Sentry or GlitchTip (lesson 7.2).'),
    NEXT_PUBLIC_SENTRY_DSN: optionalUrl('Optional, read at BUILD time: browser errors to Sentry.'),
    OTEL_EXPORTER_OTLP_ENDPOINT: optionalUrl('Optional: an OpenTelemetry collector (OTLP/HTTP), e.g. http://otel-collector:4318 (lesson 7.2).'),
    OTEL_EXPORTER: flag(['console'], 'Debugging: print spans and metrics to stdout instead.'),
    OTEL_SERVICE_NAME: z.string().optional().describe('Service name in logs and traces: beacon-web, beacon-worker.'),
    CHECK_REGION: z.string().optional().describe('The checker’s region label on check metrics (lesson 7.2). Default `local`.'),

    KMS_DRIVER: flag(['local'], 'Where the key-encryption keys live (lesson 8.1). `local` (default): ENCRYPTION_KEYS. A cloud KMS or OpenBao transit implements the same interface (src/lib/secrets/kms.ts).'),
    ENCRYPTION_KEYS: z
      .string()
      .regex(/^[a-z0-9_-]{1,32}:[A-Za-z0-9+/]{43}=(,\s*[a-z0-9_-]{1,32}:[A-Za-z0-9+/]{43}=)*$/, 'a keyring "k2:<base64 32 bytes>,k1:<…>" (npm run secrets -- generate-key)')
      .optional()
      .describe('Required in production. Keys that encrypt stored secrets (webhook secrets, Slack URLs), newest first: `k2:<base64>,k1:<base64>`. Rotation: docs/security/secrets.md.'),
    AI_PROVIDER: flag(['anthropic', 'fake'], 'The AI gateway’s provider (lesson 8.2). Default: `anthropic` when ANTHROPIC_API_KEY is set, else `fake` (deterministic, no network, no cost).'),
    ANTHROPIC_API_KEY: z.string().optional().describe('Optional: Claude for AI incident summaries (lesson 8.2). Server-side only; never NEXT_PUBLIC_.'),
    AI_MODEL: z.string().optional().describe('The primary model. Default `claude-opus-5`.'),
    AI_FALLBACK_MODEL: z.string().optional().describe('The model the gateway falls back to when the primary fails. Default `claude-sonnet-5`; `none` to disable.'),
    AI_PRIMARY_BASE_URL: optionalUrl('Send only the PRIMARY model’s requests to this base URL (a proxy such as LiteLLM, or a bad endpoint for the fallback drill). ANTHROPIC_BASE_URL moves both.'),
    AI_TIMEOUT_MS: z.coerce.number().int().min(1000).optional().describe('Timeout of one model request, in ms (the SDK retries it twice). Default 30000.'),
    SECURITY_CONTACT: z.string().regex(/^(mailto:|https:)/, 'a mailto: or https: URI').optional().describe('The `Contact:` of /.well-known/security.txt (lesson 8.1). Default mailto:security@beacon.dev.'),
  })
  .superRefine((env, ctx) => {
    const production = env.APP_ENV === 'production' || (env.NODE_ENV === 'production' && env.APP_ENV === undefined);
    const need = (key: keyof typeof env, why: string) => {
      if (!env[key]) ctx.addIssue({ code: 'custom', path: [key], message: `required ${why}` });
    };
    if (production) need('BETTER_AUTH_SECRET', 'in production (signs sessions): openssl rand -base64 32');
    // Lesson 8.1: without it, stored secrets would be encrypted with the public development key.
    if (production) need('ENCRYPTION_KEYS', 'in production (encrypts stored secrets): npm run secrets -- generate-key');
    if (env.APP_ENV === 'production' && env.BILLING_PROVIDER === 'fake') ctx.addIssue({ code: 'custom', path: ['BILLING_PROVIDER'], message: '`fake` is for development; remove it in production' });
    if (env.APP_ENV === 'production' && env.OUTBOUND_ALLOWLIST) ctx.addIssue({ code: 'custom', path: ['OUTBOUND_ALLOWLIST'], message: 'must be empty in production (it lets the SSRF guard through)' });
    if (env.STORAGE_DRIVER === 's3') for (const k of ['S3_BUCKET', 'S3_ACCESS_KEY_ID', 'S3_SECRET_ACCESS_KEY'] as const) need(k, 'with STORAGE_DRIVER=s3');
    if (env.STRIPE_SECRET_KEY) for (const k of ['STRIPE_WEBHOOK_SECRET', 'STRIPE_PRICE_PRO', 'STRIPE_PRICE_BUSINESS'] as const) need(k, 'with STRIPE_SECRET_KEY');
    if (env.ANALYTICS_DRIVER === 'posthog') need('POSTHOG_API_KEY', 'with ANALYTICS_DRIVER=posthog');
  });

export type Env = z.infer<typeof envSchema>;

export class EnvError extends Error {
  constructor(readonly problems: string[]) {
    super(`Invalid configuration:\n${problems.map((p) => `  - ${p}`).join('\n')}`);
  }
}

/** Parse and check the environment. Throws EnvError listing every problem, by variable name. */
export function loadEnv(env: Record<string, string | undefined> = process.env): Env {
  // An empty string means "not set" (a blank line in .env.example copied as-is).
  const cleaned = Object.fromEntries(Object.entries(env).filter(([, v]) => v !== undefined && v !== ''));
  const result = envSchema.safeParse(cleaned);
  if (result.success) return result.data;
  throw new EnvError(result.error.issues.map((i) => `${i.path.join('.') || '(env)'}: ${i.message}`));
}

/** For process entry points: a clear message and exit code 1 instead of a stack trace. */
export function validateEnvOrExit(service: string, env: Record<string, string | undefined> = process.env): Env {
  try {
    return loadEnv(env);
  } catch (err) {
    if (!(err instanceof EnvError)) throw err;
    // Plain stderr on purpose: this runs before logging is configured, and a person reads it.
    process.stderr.write(`\n✗ ${service} cannot start. ${err.message}\n  See .env.example and docs/configuration.md.\n\n`);
    process.exit(1);
  }
}
