import Anthropic from '@anthropic-ai/sdk';
import { betaZodOutputFormat } from '@anthropic-ai/sdk/helpers/beta/zod';
import type { z } from 'zod';
import { ProviderError, type AiProvider, type GenerateRequest, type GenerateResult } from './providers';

/*
 * Lesson 8.2: Claude, through the official Anthropic SDK (@anthropic-ai/sdk).
 * The only file in Beacon that imports it; the API key is read here, on the
 * server, and nowhere else (the client bundle never contains it: nothing in
 * src/app imports this file from a client component).
 *
 *   structured output   output_config.format built from the SAME zod schema the gateway
 *                       validates with (betaZodOutputFormat). We call create(), not parse(),
 *                       and JSON.parse the text ourselves: parse() throws on a wrong shape
 *                       and the usage of that call (which we pay for) would be lost.
 *   effort: 'low'       a summary is a simple task; low effort is cheaper and faster.
 *   fallbacks           server-side refusal fallback ('default' routes a declined request to the
 *                       model Anthropic recommends for that refusal category). Beacon's own
 *                       fallback MODEL for outages is the gateway's job (./gateway.ts).
 *   timeout, retries    the SDK retries 408/409/429/5xx and connection errors (maxRetries) with
 *                       backoff, each attempt bounded by `timeout`.
 *   no tools            the model can only answer in the schema: nothing to call, nowhere to send data.
 */
export class AnthropicProvider implements AiProvider {
  readonly name = 'anthropic';
  private readonly client: Anthropic;

  constructor(
    readonly model: string,
    opts: { apiKey?: string; baseURL?: string; maxRetries?: number } = {},
  ) {
    this.client = new Anthropic({
      apiKey: opts.apiKey ?? process.env.ANTHROPIC_API_KEY,
      ...(opts.baseURL && { baseURL: opts.baseURL }),
      maxRetries: opts.maxRetries ?? 2,
    });
  }

  async generate<S extends z.ZodType>(req: GenerateRequest<S>): Promise<GenerateResult> {
    let response;
    try {
      response = await this.client.beta.messages.create(
        {
          model: this.model,
          max_tokens: req.maxOutputTokens,
          betas: ['server-side-fallback-2026-07-01'],
          fallbacks: 'default',
          system: req.system,
          messages: [{ role: 'user', content: req.prompt }],
          output_config: { effort: 'low', format: betaZodOutputFormat(req.schema) },
        },
        { timeout: req.timeoutMs },
      );
    } catch (err) {
      throw toProviderError(err);
    }
    const usage = { inputTokens: response.usage.input_tokens, outputTokens: response.usage.output_tokens };
    // Always check why it stopped before reading the content.
    if (response.stop_reason === 'refusal') throw new ProviderError('refused', `the model declined (${response.stop_details?.category ?? 'no category'})`, usage);
    if (response.stop_reason === 'max_tokens') throw new ProviderError('invalid_output', 'the answer was cut off at max_tokens', usage);
    const text = response.content.flatMap((b) => (b.type === 'text' ? [b.text] : [])).join('');
    let output: unknown;
    try {
      output = JSON.parse(text);
    } catch {
      throw new ProviderError('invalid_output', 'the answer was not JSON', usage);
    }
    return { output, usage, model: response.model };
  }
}

/** The SDK's typed errors, most specific first (never string-matching messages). */
function toProviderError(err: unknown): ProviderError {
  if (err instanceof Anthropic.APIConnectionTimeoutError) return new ProviderError('timeout', 'the request timed out');
  if (err instanceof Anthropic.APIConnectionError) return new ProviderError('unavailable', `cannot reach the provider (${err.message})`);
  if (err instanceof Anthropic.RateLimitError) return new ProviderError('rate_limited', 'rate limited by the provider');
  if (err instanceof Anthropic.AuthenticationError || err instanceof Anthropic.PermissionDeniedError) return new ProviderError('unavailable', 'the provider rejected the API key');
  if (err instanceof Anthropic.BadRequestError || err instanceof Anthropic.NotFoundError) return new ProviderError('bad_request', `the provider refused the request (${err.status})`);
  if (err instanceof Anthropic.APIError) return new ProviderError('unavailable', `provider error ${err.status ?? ''}`.trim());
  return new ProviderError('unavailable', (err as Error).message);
}
