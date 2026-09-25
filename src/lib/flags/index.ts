import { OpenFeature } from '@openfeature/server-sdk';
import { FLAGS, type FlagKey } from '@/core/flags';
import { BeaconFlagProvider } from './provider';
import { loadRuleSet } from './store';

/*
 * Lesson 6.3: how Beacon asks "is this flag on for this org?", everywhere:
 *
 *   if (await isEnabled('new-scheduler', org)) { … }
 *
 * On the SERVER only (pages, server actions, the worker). The browser gets
 * the result, never the rules: targeting lists and unreleased flag names
 * stay out of DevTools.
 *
 * Under the hood: OpenFeature's client with Beacon's provider (./provider.ts),
 * refreshing the rules every FLAGS_REFRESH_SECONDS (default 15). The default
 * passed to OpenFeature is the flag's safe default from src/core/flags.ts,
 * which is what every caller gets if anything goes wrong.
 */

const DOMAIN = 'beacon';
const refreshMs = () => Number(process.env.FLAGS_REFRESH_SECONDS ?? 15) * 1000;

const g = globalThis as unknown as { beaconFlags?: { provider: BeaconFlagProvider; ready: Promise<void> } };

function setUp(provider: BeaconFlagProvider) {
  g.beaconFlags = { provider, ready: OpenFeature.setProviderAndWait(DOMAIN, provider) };
  return g.beaconFlags;
}

function flags() {
  return g.beaconFlags ?? setUp(new BeaconFlagProvider({ load: loadRuleSet, refreshMs: refreshMs(), log: (m) => console.warn(m) }));
}

/** Is `key` on for this organization? Typed: only flags declared in src/core/flags.ts. */
export async function isEnabled(key: FlagKey, org: { id: string }): Promise<boolean> {
  const { ready } = flags();
  await ready;
  return OpenFeature.getClient(DOMAIN).getBooleanValue(key, FLAGS[key].defaultValue, { targetingKey: org.id });
}

/** After this process changed a rule: reload now instead of waiting for the refresh interval. */
export async function refreshFlags(): Promise<void> {
  await flags().provider.refresh();
}

/** Tests: evaluate with this provider (e.g. one whose loader fails). */
export async function useFlagProviderForTests(provider: BeaconFlagProvider): Promise<void> {
  await setUp(provider).ready;
}

export { BeaconFlagProvider } from './provider';
