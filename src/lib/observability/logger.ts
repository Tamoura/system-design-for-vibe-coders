import { trace } from '@opentelemetry/api';
import pino, { type DestinationStream, type Logger } from 'pino';
import { getContext } from './context';

/*
 * Lesson 7.2 (🟢): structured logging with pino. A log line is a JSON object,
 * not a sentence:
 *
 *   {"level":"warn","time":"…","service":"beacon-worker","requestId":"9f1c…",
 *    "orgId":"0b6e…","queue":"check.run","monitorId":"…","status":503,"msg":"check.failed"}
 *
 * can be filtered by org, grouped by msg and counted; "check failed for m_91"
 * can only be grepped. The rules:
 *
 *  - msg is a stable event name (`check.failed`, `job.completed`), details are fields;
 *  - requestId, orgId and userId are added to EVERY line by `mixin`, from the
 *    request context (./context.ts), so no call site has to remember them;
 *    traceId/spanId too, so a log line links to its trace (lesson 7.2 🟡);
 *  - secrets and personal data never reach the log: `redact` replaces the
 *    usual suspects at any of the first three levels, and Beacon logs ids,
 *    not emails.
 *
 * Development: pipe it through `npx pino-pretty` if you want colours.
 */

/** Keys that are never logged, wherever they appear (lesson 7.2: "logging secrets and PII"). */
export const REDACTED_KEYS = ['password', 'newPassword', 'currentPassword', 'apiKey', 'api_key', 'secret', 'token', 'authorization', 'cookie', 'set-cookie', 'slackWebhookUrl'];

function redactPaths(): string[] {
  const paths: string[] = [];
  for (const k of REDACTED_KEYS) {
    const safe = /^[A-Za-z_$][\w$]*$/.test(k) ? k : `["${k}"]`;
    const join = (prefix: string) => (safe.startsWith('[') ? `${prefix}${safe}` : `${prefix}.${safe}`);
    paths.push(safe, join('*'), join('*.*'), join('*.*.*'));
  }
  return paths;
}

export function createLogger(options: { destination?: DestinationStream; level?: string; service?: string } = {}): Logger {
  return pino(
    {
      level: options.level ?? process.env.LOG_LEVEL ?? (process.env.VITEST ? 'silent' : 'info'),
      base: { service: options.service ?? process.env.OTEL_SERVICE_NAME ?? 'beacon' },
      // ISO timestamps: readable by people and every log backend.
      timestamp: pino.stdTimeFunctions.isoTime,
      // "level":"info" instead of "level":30.
      formatters: { level: (label) => ({ level: label }) },
      redact: { paths: redactPaths(), censor: '[redacted]' },
      mixin() {
        const ctx = getContext();
        const span = trace.getActiveSpan()?.spanContext();
        return {
          ...(ctx && { requestId: ctx.requestId, orgId: ctx.orgId, userId: ctx.userId, impersonatorId: ctx.impersonatorId, queue: ctx.queue, jobId: ctx.jobId }),
          ...(span && span.traceId !== '00000000000000000000000000000000' && { traceId: span.traceId, spanId: span.spanId }),
        };
      },
    },
    options.destination,
  );
}

const g = globalThis as unknown as { beaconLogger?: Logger };

/** The process's logger. The service name comes from OTEL_SERVICE_NAME (beacon-web, beacon-worker). */
export const logger: Logger = (g.beaconLogger ??= createLogger());

/** A logger for one module: every line carries `module`. */
export function moduleLogger(module: string): Logger {
  return logger.child({ module });
}
