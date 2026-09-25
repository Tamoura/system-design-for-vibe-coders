import { ErrorCode, type EvaluationContext, type JsonValue, type Provider, type ResolutionDetails } from '@openfeature/server-sdk';
import { evaluateFlag, type RuleSet } from '@/core/flags';

/*
 * Lesson 6.3 (🟡): an OpenFeature PROVIDER for Beacon's own flag rules.
 *
 * The app never talks to this class. It calls OpenFeature's vendor-neutral
 * API (./index.ts: client.getBooleanValue(key, default, { targetingKey: orgId })),
 * and OpenFeature asks whichever provider is plugged in. Moving to Unleash,
 * Flagsmith or flagd later is `OpenFeature.setProvider(new ThatProvider())`
 * (e.g. @openfeature/flagsmith-provider, @openfeature/flagd-provider); no call
 * site changes.
 *
 * LOCAL EVALUATION, like the Unleash and Flagsmith server SDKs: the provider
 * holds the whole rule set in memory and evaluates in microseconds, which is
 * what the check workers need (they ask for every org, every minute). It
 * reloads the rules when they are older than `refreshMs`, so a flag flipped
 * in /internal/flags reaches every process within one refresh interval, with
 * no deploy and no restart.
 *
 * When the rules cannot be loaded (the flag store is down):
 *   - it keeps evaluating with the LAST KNOWN rules and tries again later;
 *   - with no rules at all (it never loaded), every flag gets its safe default.
 * It never throws into the caller: a flag lookup must not take a request, or
 * a worker, down with it.
 */
export class BeaconFlagProvider implements Provider {
  readonly metadata = { name: 'beacon-postgres' } as const;
  readonly runsOn = 'server' as const;

  private rules: RuleSet | null = null;
  private lastAttempt = -Infinity;
  private inFlight: Promise<void> | null = null;
  private failing = false;

  constructor(
    private readonly opts: {
      load: () => Promise<RuleSet>;
      refreshMs: number;
      now?: () => number;
      log?: (message: string) => void;
    },
  ) {}

  private now() {
    return this.opts.now?.() ?? Date.now();
  }

  /** Called once by OpenFeature when the provider is set. Never throws: no rules yet just means safe defaults. */
  async initialize(): Promise<void> {
    await this.refresh();
  }

  /** Load the rules now (also used right after a change in this process, so its own admin sees it at once). */
  async refresh(): Promise<void> {
    this.inFlight ??= (async () => {
      this.lastAttempt = this.now();
      try {
        this.rules = await this.opts.load();
        if (this.failing) this.opts.log?.('[flags] rules loaded again');
        this.failing = false;
      } catch (err) {
        if (!this.failing) {
          this.opts.log?.(`[flags] could not load the rules (${(err as Error).message}); ${this.rules ? 'keeping the last known rules' : 'using safe defaults'}`);
        }
        this.failing = true;
      } finally {
        this.inFlight = null;
      }
    })();
    return this.inFlight;
  }

  /** How old the rules this process evaluates with are allowed to get. */
  private async currentRules(): Promise<RuleSet | null> {
    if (this.now() - this.lastAttempt >= this.opts.refreshMs) await this.refresh();
    return this.rules;
  }

  async resolveBooleanEvaluation(flagKey: string, defaultValue: boolean, context: EvaluationContext): Promise<ResolutionDetails<boolean>> {
    // B2B: the ORG is the rollout unit (lesson 6.3), so the targeting key is the org id.
    const orgId = context.targetingKey;
    if (!orgId) return { value: defaultValue, reason: 'ERROR', errorCode: ErrorCode.TARGETING_KEY_MISSING };
    const rules = await this.currentRules();
    if (!rules) return { value: defaultValue, reason: 'ERROR', errorCode: ErrorCode.PROVIDER_NOT_READY, errorMessage: 'flag rules unavailable; safe default' };
    const { value, reason } = evaluateFlag(rules, flagKey, orgId, defaultValue);
    return { value, reason: this.failing && reason !== 'DEFAULT' ? 'STALE' : reason };
  }

  // Beacon's flags are booleans. Other types are refused (OpenFeature then returns the caller's default).
  async resolveStringEvaluation(_k: string, defaultValue: string): Promise<ResolutionDetails<string>> {
    return { value: defaultValue, reason: 'ERROR', errorCode: ErrorCode.TYPE_MISMATCH };
  }
  async resolveNumberEvaluation(_k: string, defaultValue: number): Promise<ResolutionDetails<number>> {
    return { value: defaultValue, reason: 'ERROR', errorCode: ErrorCode.TYPE_MISMATCH };
  }
  async resolveObjectEvaluation<T extends JsonValue>(_k: string, defaultValue: T): Promise<ResolutionDetails<T>> {
    return { value: defaultValue, reason: 'ERROR', errorCode: ErrorCode.TYPE_MISMATCH };
  }
}
