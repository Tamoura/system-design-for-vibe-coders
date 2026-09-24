/**
 * Lesson 4.1 (🟡): how long a queued job (an email, a notification delivery)
 * waits before its next attempt after a failure. Exponential: 30 s, 2 min,
 * 8 min, 32 min, ~2 h, then every 6 hours, so a provider outage of a few
 * hours delays mail instead of losing it. After MAX_ATTEMPTS the job is
 * marked failed and shows up as such in the delivery log.
 */
export const MAX_ATTEMPTS = 8;

export function retryDelayMs(attempt: number): number {
  const base = 30_000 * 4 ** Math.max(0, attempt - 1);
  return Math.min(base, 6 * 60 * 60 * 1000);
}

