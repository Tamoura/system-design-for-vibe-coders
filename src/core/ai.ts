import { createHash } from 'node:crypto';

/*
 * Lesson 8.2: the AI gateway's pure parts: model prices and the cache key.
 *
 * Tokens are cost of goods sold. The gateway records every call's tokens and
 * its cost here, per org and per feature (llm_usage), so "what does AI cost
 * us for Acme?" is a SQL query, and a monthly per-org sum can be compared with
 * the provider's dashboard.
 *
 * Prices are USD per million tokens (Anthropic's list prices; check
 * https://www.anthropic.com/pricing when you change models). Model ids live in
 * configuration (AI_MODEL, AI_FALLBACK_MODEL), never in feature code: models
 * are retired on the provider's schedule, not ours (lesson 8.2, model churn).
 */
export const MODEL_PRICES: Record<string, { inputPerMTok: number; outputPerMTok: number }> = {
  'claude-opus-5': { inputPerMTok: 5, outputPerMTok: 25 },
  'claude-sonnet-5': { inputPerMTok: 2, outputPerMTok: 10 },
  'claude-haiku-4-5': { inputPerMTok: 1, outputPerMTok: 5 },
  'claude-opus-4-8': { inputPerMTok: 5, outputPerMTok: 25 },
  fake: { inputPerMTok: 0, outputPerMTok: 0 },
};

/** The default models: the primary, and the fallback the gateway uses when the primary fails. */
export const DEFAULT_MODEL = 'claude-opus-5';
export const DEFAULT_FALLBACK_MODEL = 'claude-sonnet-5';

/**
 * Cost of one call in micro-dollars (millionths of a dollar). With prices per
 * MILLION tokens that is exactly tokens × price: integer, no rounding drift
 * when a month of calls is summed. An unknown model is priced like the most
 * expensive known one, so a new model never looks free.
 */
export function costMicros(model: string, inputTokens: number, outputTokens: number): number {
  const known = MODEL_PRICES[model] ?? MODEL_PRICES[Object.keys(MODEL_PRICES).find((m) => model.startsWith(m)) ?? ''];
  const price = known ?? Object.values(MODEL_PRICES).reduce((a, b) => (b.outputPerMTok > a.outputPerMTok ? b : a));
  return Math.round(inputTokens * price.inputPerMTok + outputTokens * price.outputPerMTok);
}

export function formatMicros(micros: number): string {
  return `$${(micros / 1_000_000).toFixed(micros < 10_000 ? 4 : 2)}`;
}

/** The cache key: the feature, the prompt version and the exact text the model would see. */
export function inputHash(parts: string[]): string {
  const h = createHash('sha256');
  for (const p of parts) h.update(p).update('\u0000');
  return h.digest('hex');
}

/** A rough token count (about 4 characters per token) for providers that do not report usage, like the fake. */
export function estimateTokens(text: string): number {
  return Math.max(1, Math.ceil(text.length / 4));
}
