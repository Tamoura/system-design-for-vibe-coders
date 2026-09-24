import { createHash } from 'node:crypto';

/**
 * Lesson 5.1: a DETERMINISTIC job id. The same key always gives the same
 * UUID, so enqueuing the same piece of work twice ("check monitor X for the
 * 12:00:30 slot", "send delivery Y") inserts one job: the queue's primary key
 * refuses the second. It is BullMQ's `jobId: \`incident-opened:${id}\`` from
 * the lesson, for a queue (pg-boss) whose job ids must be UUIDs.
 *
 * The UUID is the first 16 bytes of SHA-256(key), with the version nibble set
 * to 8 ("custom", RFC 9562) and the RFC variant bits, so it is a valid UUID
 * that can never collide with a random (version 4) one.
 */
export function stableUuid(key: string): string {
  const bytes = createHash('sha256').update(key).digest().subarray(0, 16);
  bytes[6] = (bytes[6] & 0x0f) | 0x80; // version 8
  bytes[8] = (bytes[8] & 0x3f) | 0x80; // variant 10xx
  const hex = bytes.toString('hex');
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
}

/*
 * Lesson 5.2: prefixed, opaque ids in the public API. `mon_3f2a…` says what it
 * is, in a log line or a support ticket, and a key's `key_…` cannot be pasted
 * where a monitor id belongs without an obvious error. Inside Beacon the ids
 * stay plain UUIDs; the API converts at its edge.
 */
export const ID_PREFIXES = { monitor: 'mon', incident: 'inc', apiKey: 'key', webhookEndpoint: 'ep', webhookMessage: 'msg' } as const;
export type IdKind = keyof typeof ID_PREFIXES;

export function toPublicId(kind: IdKind, uuid: string): string {
  return `${ID_PREFIXES[kind]}_${uuid.replaceAll('-', '')}`;
}

/** The UUID behind a public id, or null if it is not one of this kind (the caller answers 404). */
export function fromPublicId(kind: IdKind, publicId: string): string | null {
  const m = new RegExp(`^${ID_PREFIXES[kind]}_([0-9a-f]{32})$`).exec(publicId);
  if (!m) return null;
  const h = m[1];
  return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
}
