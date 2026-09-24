import type { Entitlements, PlanId } from '@/core/plans';

/**
 * Why access was refused. Pages and server actions turn it into a redirect, a
 * 404 page or a 403 page (forPage in ./access.ts); API routes turn it into a
 * status code (apiRoute in ./api.ts).
 *
 *  unauthenticated → 401   no session
 *  not_found       → 404   not in this org, or no such object *in this org*
 *  forbidden       → 403   in the org, but the role or a rule does not allow it
 */
export class AccessError extends Error {
  constructor(readonly reason: 'unauthenticated' | 'not_found' | 'forbidden') {
    super(reason);
  }
}

/**
 * A request we understood but refuse for a reason the user can fix (a file
 * too large, of the wrong type…). API routes answer 400 with `code`.
 */
export class InvalidRequestError extends Error {
  constructor(
    readonly code: string,
    message: string,
  ) {
    super(message);
  }
}

/**
 * Lesson 3.2: the org's plan does not allow this (a sixth monitor on Free, a
 * 30-second interval on Pro). A structured error, not "Something went wrong":
 * the API answers 402 with `{ error: 'limit_exceeded', limit, allowed,
 * upgradeTo }`, so any client can show a specific upgrade prompt.
 */
export class LimitExceededError extends Error {
  readonly code = 'limit_exceeded';
  constructor(
    readonly limit: keyof Entitlements | 'runningMonitors',
    readonly allowed: number | boolean,
    message: string,
    /** The cheapest plan that would allow it, or null. */
    readonly upgradeTo: PlanId | null,
  ) {
    super(message);
  }
}
