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

/**
 * Lesson 4.3 (🟡): reconnect delay for a browser that lost its live
 * connection. Exponential backoff with FULL jitter: a random delay between 0
 * and the exponential cap. When a server restarts, its 20,000 clients then
 * come back spread over several seconds instead of all in the same one.
 * `random` is injectable so the tests can pin it.
 */
export function reconnectDelayMs(attempt: number, random: () => number = Math.random, baseMs = 1000, capMs = 30_000): number {
  const ceiling = Math.min(capMs, baseMs * 2 ** Math.max(0, attempt));
  return Math.round(random() * ceiling);
}
