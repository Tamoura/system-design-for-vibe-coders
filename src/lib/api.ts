import { ZodError } from 'zod';
import { AccessError, InvalidRequestError, LimitExceededError } from './errors';
import { observeRequest } from './observability/http';

const STATUS = { unauthenticated: 401, not_found: 404, forbidden: 403 } as const;

/**
 * Wrap an API route handler so refusals become the right status code:
 * 401 no session, 404 not in this org (or no such object), 403 role lacks the
 * permission, 400 invalid body or a refused request (InvalidRequestError),
 * 402 the plan does not allow it (LimitExceededError, lesson 3.2: "Payment
 * Required" tells the client to upsell, where 403 would mean "your role").
 * Anything else is a real bug and stays a 500.
 *
 * Lesson 7.2: observeRequest() around it gives the request its id, a trace
 * span, RED metrics and an access log line, and reports a real bug (a 500)
 * to the error tracker.
 */
export function apiRoute<Ctx>(handler: (req: Request, context: Ctx) => Promise<Response>) {
  return (req: Request, context: Ctx): Promise<Response> => observeRequest(req, () => refusalsToStatus(req, context, handler));
}

async function refusalsToStatus<Ctx>(req: Request, context: Ctx, handler: (req: Request, context: Ctx) => Promise<Response>): Promise<Response> {
  try {
    return await handler(req, context);
  } catch (err) {
    if (err instanceof AccessError) return Response.json({ error: err.reason }, { status: STATUS[err.reason] });
    if (err instanceof LimitExceededError) {
      const { code, limit, allowed, upgradeTo, message } = err;
      return Response.json({ error: code, limit, allowed, upgradeTo, message }, { status: 402 });
    }
    if (err instanceof InvalidRequestError) return Response.json({ error: err.code, message: err.message }, { status: 400 });
    if (err instanceof ZodError) return Response.json({ error: 'invalid_body', issues: err.flatten().fieldErrors }, { status: 400 });
    if (err instanceof SyntaxError) return Response.json({ error: 'invalid_json' }, { status: 400 });
    throw err; // a real bug: observeRequest() reports it and answers 500
  }
}

export const notFoundResponse = () => Response.json({ error: 'not_found' }, { status: 404 });
