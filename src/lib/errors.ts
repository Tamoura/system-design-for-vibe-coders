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
