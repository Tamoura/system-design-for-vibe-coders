/*
 * Lesson 5.2 (🟡): the public API's errors, RFC 9457 "Problem Details for
 * HTTP APIs". One format for every 4xx and 5xx:
 *
 *   HTTP/1.1 429 Too Many Requests
 *   Content-Type: application/problem+json
 *   { "type": "https://beacon.app/problems/rate-limited", "title": "Too many requests",
 *     "status": 429, "detail": "Retry in 3 seconds.", "instance": "/api/v1/monitors" }
 *
 * `type` identifies the KIND of problem (clients switch on it), `title` is
 * fixed per type, `detail` explains this occurrence. Status codes are used
 * honestly: 404 also for "exists, but in another organization".
 */
export const PROBLEM_BASE = 'https://beacon.app/problems/';

export const PROBLEMS = {
  'invalid-json': { status: 400, title: 'The request body is not valid JSON' },
  'invalid-parameter': { status: 400, title: 'A query parameter is not valid' },
  'blocked-url': { status: 400, title: 'Beacon cannot check this URL' },
  unauthenticated: { status: 401, title: 'Missing or invalid API key' },
  'plan-upgrade-required': { status: 402, title: 'Your plan does not include this' },
  'limit-exceeded': { status: 402, title: 'Over a plan limit' },
  'insufficient-scope': { status: 403, title: 'The API key lacks a scope' },
  forbidden: { status: 403, title: 'Not allowed' },
  'not-found': { status: 404, title: 'Not found' },
  'idempotency-key-in-use': { status: 409, title: 'A request with this Idempotency-Key is still in progress' },
  'validation-failed': { status: 422, title: 'The request has invalid fields' },
  'idempotency-key-reused': { status: 422, title: 'This Idempotency-Key was used with a different request' },
  'rate-limited': { status: 429, title: 'Too many requests' },
  internal: { status: 500, title: 'Something went wrong on our side' },
} as const satisfies Record<string, { status: number; title: string }>;

export type ProblemType = keyof typeof PROBLEMS;

export type ProblemBody = {
  type: string;
  title: string;
  status: number;
  detail?: string;
  instance?: string;
  [extension: string]: unknown;
};

export function problemBody(type: ProblemType, extra: { detail?: string; instance?: string; [k: string]: unknown } = {}): ProblemBody {
  const { status, title } = PROBLEMS[type];
  return { type: `${PROBLEM_BASE}${type}`, title, status, ...extra };
}
