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
