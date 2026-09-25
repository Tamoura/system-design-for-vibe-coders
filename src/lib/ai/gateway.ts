import { and, eq, gt } from 'drizzle-orm';
import type { z } from 'zod';
import { schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { costMicros, DEFAULT_FALLBACK_MODEL, DEFAULT_MODEL, inputHash } from '@/core/ai';
import { DAY_MS } from '@/core/retention';
import { METERS, usageKeys } from '@/core/usage';
import { getEntitlements } from '../entitlements';
import { consumeRateLimit } from '../rate-limit';
import { getContext } from '../observability/context';
import { logger } from '../observability/logger';
import { recordLlmCall } from '../observability/metrics';
import { withSpan } from '../observability/telemetry';
import { AnthropicProvider } from './anthropic';
import { FakeProvider, ProviderError, type AiProvider } from './providers';

const { llmUsage, llmCache, usageEvents } = schema;

/*
 * Lesson 8.2 (🟡): the AI GATEWAY, a thin in-house module (the lesson's
 * alternative to running LiteLLM). Every model call in Beacon goes through
 * generateStructured(), which does, in order:
 *
 *   1. per-org rate limit       a token bucket per org, sized by the plan (aiCallsPerHour):
 *                               one org looping the feature cannot run up the bill
 *   2. cache                    the same prompt for the same org within 7 days → the stored
 *                               answer, no call (llm_cache, keyed by a hash of the input)
 *   3. providers in order       the primary model, then the fallback model: an outage,
 *                               a timeout, a refusal or an answer that fails validation
 *                               moves on to the next one
 *   4. validation               the zod schema, then the feature's own checks (`check`)
 *   5. metering                 EVERY call → llm_usage (tokens, cost, latency, outcome), what
 *                               Beacon pays; each successful one → usage_events, meter
 *                               ai_tokens, what the customer is billed (lesson 3.3's pipeline)
 *   6. observability            one log line, metrics and a span per call, with the model,
 *                               tokens, cost and latency, and NEVER the prompt or the answer
 *                               (they are customer data: lesson 7.2's redaction, 8.1's rules)
 *
 * Provider keys are read only inside the providers, on the server.
 */

export type GatewayRequest<S extends z.ZodType> = {
  orgId: string;
  /** "incident_summary": the llm_usage feature, a metric label, part of the cache key. */
  feature: string;
  /** What the call is about (an incident id), for "show me this incident's AI calls". */
  subjectId?: string;
  system: string;
  prompt: string;
  /** Changing the prompt's wording? Bump the version: old cache entries stop matching. */
  promptVersion: string;
  schema: S;
  /** Extra checks on a schema-valid answer; any problem counts as an invalid answer. */
  check?: (output: z.infer<S>) => string[];
  maxOutputTokens?: number;
};

export type GatewayResult<T> = { output: T; provider: string; model: string; inputHash: string; cached: boolean };

/** Too many calls for this org right now (the gateway's own limit, before any provider is asked). */
export class AiRateLimitedError extends Error {
  constructor(readonly retryAfterSec: number) {
    super(`Too many AI requests for this organization. Try again in ${Math.ceil(retryAfterSec / 60)} minute(s).`);
    this.name = 'AiRateLimitedError';
  }
}

/** Every provider failed. `reasons` has one entry per provider tried (never customer data). */
export class AiUnavailableError extends Error {
  constructor(readonly reasons: string[]) {
    super(`The AI provider could not produce a valid answer (${reasons.join('; ')})`);
    this.name = 'AiUnavailableError';
  }
}

/* ---------------------------------------------------------------------------
 * Configuration: which providers, in which order.
 * ------------------------------------------------------------------------- */

export const CACHE_TTL_DAYS = 7;

let testProviders: AiProvider[] | null = null;
export function setProvidersForTests(providers: AiProvider[] | null) {
  testProviders = providers;
}

/**
 * AI_PROVIDER=anthropic (the default when ANTHROPIC_API_KEY is set): AI_MODEL,
 * then AI_FALLBACK_MODEL ("none" for no fallback). AI_PRIMARY_BASE_URL points
 * only the primary somewhere else (a proxy, or a bad endpoint for the
 * fallback drill). Otherwise, the fake provider: no key, no network, no cost.
 */
export function providerChain(env: Record<string, string | undefined> = process.env): AiProvider[] {
  if (testProviders) return testProviders;
  const kind = env.AI_PROVIDER ?? (env.ANTHROPIC_API_KEY ? 'anthropic' : 'fake');
  if (kind !== 'anthropic') return [new FakeProvider()];
  const primary = new AnthropicProvider(env.AI_MODEL || DEFAULT_MODEL, { baseURL: env.AI_PRIMARY_BASE_URL });
  const fallbackModel = env.AI_FALLBACK_MODEL || DEFAULT_FALLBACK_MODEL;
  return fallbackModel === 'none' ? [primary] : [primary, new AnthropicProvider(fallbackModel)];
}

const timeoutMs = () => Number(process.env.AI_TIMEOUT_MS ?? 30_000);

/* ---------------------------------------------------------------------------
 * The call.
 * ------------------------------------------------------------------------- */

export async function generateStructured<S extends z.ZodType>(req: GatewayRequest<S>): Promise<GatewayResult<z.infer<S>>> {
  const hash = inputHash([req.feature, req.promptVersion, req.system, req.prompt]);

  // 1. Per-org rate limit (lesson 5.2's token bucket), sized by the plan.
  const ent = await getEntitlements({ orgId: req.orgId });
  const perHour = Math.max(1, ent.aiCallsPerHour);
  const limit = await consumeRateLimit(`ai:${req.orgId}`, { name: 'ai', capacity: perHour, refillPerSec: perHour / 3600 });
  if (!limit.allowed) {
    logger.warn({ feature: req.feature, orgId: req.orgId }, 'llm.rate_limited');
    throw new AiRateLimitedError(limit.retryAfterSec);
  }

  // 2. The cache.
  const since = new Date(Date.now() - CACHE_TTL_DAYS * DAY_MS);
  const [hit] = await withOrg(req.orgId, (tx) =>
    tx
      .select()
      .from(llmCache)
      .where(and(eq(llmCache.organizationId, req.orgId), eq(llmCache.feature, req.feature), eq(llmCache.inputHash, hash), gt(llmCache.createdAt, since))),
  );
  if (hit) {
    const parsed = req.schema.safeParse(hit.output);
    if (parsed.success) {
      await record(req, { provider: hit.provider, model: hit.model, outcome: 'cached', inputTokens: 0, outputTokens: 0, latencyMs: 0, hash });
      return { output: parsed.data, provider: hit.provider, model: hit.model, inputHash: hash, cached: true };
    }
  }

  // 3–4. Each provider in turn, until one gives a valid answer.
  const reasons: string[] = [];
  for (const provider of providerChain()) {
    const started = performance.now();
    const attributes = { 'gen_ai.system': provider.name, 'gen_ai.request.model': provider.model, 'beacon.ai.feature': req.feature };
    const attempt = await withSpan('llm.generate', { attributes }, async (span) => {
      try {
        const result = await provider.generate({ system: req.system, prompt: req.prompt, schema: req.schema, maxOutputTokens: req.maxOutputTokens ?? 16_000, timeoutMs: timeoutMs() });
        span.setAttributes({ 'gen_ai.response.model': result.model, 'gen_ai.usage.input_tokens': result.usage.inputTokens, 'gen_ai.usage.output_tokens': result.usage.outputTokens });
        const parsed = req.schema.safeParse(result.output);
        const problems = parsed.success ? (req.check?.(parsed.data) ?? []) : [`schema: ${parsed.error.issues.map((i) => `${i.path.join('.') || '(root)'} ${i.message}`).join(', ')}`];
        return { ok: problems.length === 0, result, output: parsed.success ? parsed.data : null, problems };
      } catch (err) {
        const e = err instanceof ProviderError ? err : new ProviderError('unavailable', (err as Error).message);
        return { ok: false, result: null, output: null, problems: [`${e.kind}: ${e.message}`], usage: e.usage };
      }
    });
    const latencyMs = Math.round(performance.now() - started);
    const usage = attempt.result?.usage ?? ('usage' in attempt ? attempt.usage : undefined) ?? { inputTokens: 0, outputTokens: 0 };
    const model = attempt.result?.model ?? provider.model;
    if (attempt.ok && attempt.output !== null) {
      await record(req, { provider: provider.name, model, outcome: 'ok', ...usage, latencyMs, hash, meter: true });
      await withOrg(req.orgId, (tx) =>
        tx
          .insert(llmCache)
          .values({ organizationId: req.orgId, feature: req.feature, inputHash: hash, output: attempt.output as object, provider: provider.name, model })
          .onConflictDoUpdate({ target: [llmCache.organizationId, llmCache.feature, llmCache.inputHash], set: { output: attempt.output as object, provider: provider.name, model, createdAt: new Date() } }),
      );
      return { output: attempt.output as z.infer<S>, provider: provider.name, model, inputHash: hash, cached: false };
    }
    const outcome = attempt.result ? 'invalid_output' : 'error';
    await record(req, { provider: provider.name, model, outcome, ...usage, latencyMs, hash, error: attempt.problems.join('; ').slice(0, 300) });
    reasons.push(`${provider.name}/${provider.model}: ${attempt.problems.join('; ')}`.slice(0, 300));
  }
  throw new AiUnavailableError(reasons);
}

type CallRecord = {
  provider: string;
  model: string;
  outcome: 'ok' | 'error' | 'invalid_output' | 'cached';
  inputTokens: number;
  outputTokens: number;
  latencyMs: number;
  hash: string;
  error?: string;
  /** Bill the customer for it (successful calls only: our failures are our cost). */
  meter?: boolean;
};

/** 5–6: the usage row (and the billable usage event) in one transaction, then the log line and metrics. */
async function record(req: GatewayRequest<z.ZodType>, call: CallRecord) {
  const cost = call.outcome === 'cached' ? 0 : costMicros(call.model, call.inputTokens, call.outputTokens);
  const requestId = getContext()?.requestId ?? null;
  await withOrg(req.orgId, async (tx) => {
    const [row] = await tx
      .insert(llmUsage)
      .values({
        organizationId: req.orgId,
        feature: req.feature,
        subjectId: req.subjectId ?? null,
        provider: call.provider,
        model: call.model,
        outcome: call.outcome,
        inputTokens: call.inputTokens,
        outputTokens: call.outputTokens,
        costMicros: cost,
        latencyMs: call.latencyMs,
        error: call.error ?? null,
        requestId,
      })
      .returning({ id: llmUsage.id, createdAt: llmUsage.createdAt });
    const tokens = call.inputTokens + call.outputTokens;
    if (call.meter && tokens > 0) {
      await tx
        .insert(usageEvents)
        .values({ organizationId: req.orgId, idempotencyKey: usageKeys.aiCall(row.id), meter: METERS.aiTokens, quantity: tokens, occurredAt: row.createdAt })
        .onConflictDoNothing({ target: usageEvents.idempotencyKey });
    }
  });
  // The log line: ids, numbers and the input HASH (to correlate repeated calls), never the text.
  logger.info(
    { feature: req.feature, provider: call.provider, model: call.model, outcome: call.outcome, inputTokens: call.inputTokens, outputTokens: call.outputTokens, costMicros: cost, latencyMs: call.latencyMs, inputHash: call.hash.slice(0, 16), subjectId: req.subjectId, ...(call.error && { error: call.error }) },
    'llm.call',
  );
  recordLlmCall({ feature: req.feature, provider: call.provider, model: call.model, outcome: call.outcome, inputTokens: call.inputTokens, outputTokens: call.outputTokens, costMicros: cost, seconds: call.latencyMs / 1000 });
}
