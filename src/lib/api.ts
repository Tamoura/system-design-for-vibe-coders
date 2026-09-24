import { ZodError } from 'zod';
import { AccessError, InvalidRequestError } from './errors';

const STATUS = { unauthenticated: 401, not_found: 404, forbidden: 403 } as const;

/**
 * Wrap an API route handler so refusals become the right status code:
 * 401 no session, 404 not in this org (or no such object), 403 role lacks the
 * permission, 400 invalid body or a refused request (InvalidRequestError).
 * Anything else is a real bug and stays a 500.
 */
export function apiRoute<Ctx>(handler: (req: Request, context: Ctx) => Promise<Response>) {
  return async (req: Request, context: Ctx): Promise<Response> => {
    try {
      return await handler(req, context);
    } catch (err) {
      if (err instanceof AccessError) return Response.json({ error: err.reason }, { status: STATUS[err.reason] });
      if (err instanceof InvalidRequestError) return Response.json({ error: err.code, message: err.message }, { status: 400 });
      if (err instanceof ZodError) return Response.json({ error: 'invalid_body', issues: err.flatten().fieldErrors }, { status: 400 });
      if (err instanceof SyntaxError) return Response.json({ error: 'invalid_json' }, { status: 400 });
      throw err;
    }
  };
}

export const notFoundResponse = () => Response.json({ error: 'not_found' }, { status: 404 });
