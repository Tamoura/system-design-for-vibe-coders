import type { z } from 'zod';
import { estimateTokens } from '@/core/ai';
import { errorKind, extractIncidentData } from '@/core/incident-summary';

/*
 * Lesson 8.2: the provider abstraction. Feature code never imports a model
 * SDK; it asks the gateway (./gateway.ts), which asks a provider through this
 * one interface. Swapping Anthropic for another vendor, or for a model you
 * host, is a new class here and a line of configuration.
 */
export type GenerateRequest<S extends z.ZodType> = {
  system: string;
  prompt: string;
  /** The shape of the answer. The provider asks the model for it; the gateway validates it again. */
  schema: S;
  maxOutputTokens: number;
  timeoutMs: number;
};

export type GenerateResult = {
  /** Parsed JSON, NOT yet validated: the gateway does that. */
  output: unknown;
  usage: { inputTokens: number; outputTokens: number };
  /** The model that actually answered (a server-side fallback may have switched it). */
  model: string;
};

export interface AiProvider {
  /** "anthropic", "fake": goes into llm_usage and the logs. */
  readonly name: string;
  readonly model: string;
  generate<S extends z.ZodType>(req: GenerateRequest<S>): Promise<GenerateResult>;
}

/** The provider could not answer: down, timed out, rate limited, refused. The gateway tries the next one. */
export class ProviderError extends Error {
  constructor(
    readonly kind: 'unavailable' | 'timeout' | 'rate_limited' | 'refused' | 'bad_request' | 'invalid_output',
    message: string,
    readonly usage?: { inputTokens: number; outputTokens: number },
  ) {
    super(message);
    this.name = 'ProviderError';
  }
}

/**
 * The fake provider: tests, the eval, CI, and any machine without
 * ANTHROPIC_API_KEY. It reads the incident data out of the prompt, like a
 * model would, and writes a plain, deterministic summary from it. It is well
 * behaved on purpose; `behaviour` lets tests make it misbehave.
 *
 *   'normal'            a correct summary
 *   'obey-injection'    does what an injected instruction asks: says "resolved", adds a link
 *   'invalid'           answers with JSON of the wrong shape
 *   'down'              throws, like a provider outage
 */
export class FakeProvider implements AiProvider {
  readonly name = 'fake';
  readonly model: string;
  calls = 0;

  constructor(private readonly behaviour: 'normal' | 'obey-injection' | 'invalid' | 'down' = 'normal', model = 'fake') {
    this.model = model;
  }

  async generate<S extends z.ZodType>(req: GenerateRequest<S>): Promise<GenerateResult> {
    this.calls++;
    const usage = { inputTokens: estimateTokens(req.system + req.prompt), outputTokens: 0 };
    if (this.behaviour === 'down') throw new ProviderError('unavailable', 'fake provider is down');
    const ctx = extractIncidentData(req.prompt);
    if (!ctx) throw new ProviderError('bad_request', 'no <incident_data> in the prompt');
    let output: unknown;
    if (this.behaviour === 'invalid') {
      output = { summary: 'not the shape you asked for' };
    } else {
      const { monitor, incident, checks } = ctx;
      const resolved = incident.status === 'resolved' || this.behaviour === 'obey-injection';
      const kinds = [...new Set(checks.errors.map((e) => errorKind(e.text)))];
      const what = kinds.length ? kinds.join(' and ') : 'failed checks';
      const duration = incident.durationMinutes < 1 ? 'under a minute' : `${incident.durationMinutes} minute${incident.durationMinutes === 1 ? '' : 's'}`;
      output = {
        headline: `${monitor.name}: ${resolved ? 'outage resolved' : 'outage ongoing'} after ${duration}`,
        status: resolved ? 'resolved' : 'ongoing',
        impact: `${monitor.name} (${monitor.host}) failed ${checks.failed} of ${checks.total} checks during the incident.`,
        suspectedCause: kinds.length ? `Checks reported ${what}.` : null,
        timeline: [
          { at: incident.openedAt, event: 'Incident opened after three failed checks in a row.' },
          ...(incident.acknowledgedAt ? [{ at: incident.acknowledgedAt, event: 'Acknowledged by the team.' }] : []),
          ...(incident.resolvedAt ? [{ at: incident.resolvedAt, event: 'Checks passing again; incident resolved.' }] : []),
        ],
        customerFacingUpdate: resolved
          ? `${monitor.name} was unavailable for ${duration} (${what}). It has been working normally since ${incident.resolvedAt ?? 'now'}.` +
            (this.behaviour === 'obey-injection' ? ' More at https://attacker.example/status.' : '')
          : `${monitor.name} is currently unavailable (${what}). The team is investigating and will post an update here.`,
      };
    }
    const text = JSON.stringify(output);
    return { output, usage: { ...usage, outputTokens: estimateTokens(text) }, model: this.model };
  }
}
