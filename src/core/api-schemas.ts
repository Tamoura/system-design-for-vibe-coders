import { z } from 'zod';
import { ALLOWED_INTERVALS, createMonitorInput } from './validation';

/*
 * Lesson 5.2 (🟡): the public API's shapes, defined ONCE. The route handlers
 * validate requests with them, and src/core/openapi.ts generates the OpenAPI
 * document from them, so the documentation cannot drift from the code (CI
 * fails when docs/openapi.json is out of date: `npm run openapi`).
 *
 * The public API is its own contract, deliberately separate from the
 * dashboard's internal JSON (/api/orgs/…): snake_case fields, prefixed ids
 * (mon_…, inc_…), RFC 3339 times. The dashboard can change freely; this
 * cannot, within /v1, except by ADDING fields.
 */

/** Every schema that becomes a named component in the OpenAPI document. */
export const apiRegistry = z.registry<{ id: string }>();

const dateTime = (description: string) => z.string().meta({ format: 'date-time', description, example: '2026-03-01T12:00:00.000Z' });
const interval = z
  .number()
  .int()
  .refine((n) => (ALLOWED_INTERVALS as readonly number[]).includes(n), 'Pick one of 30, 60, 300 or 900')
  .meta({ description: 'Seconds between checks: 30, 60, 300 or 900. Never below your plan’s minimum.', enum: [...ALLOWED_INTERVALS], example: 300 });

// The field rules come from the form's schema (src/core/validation.ts): one set of rules for both.
export const MonitorCreate = z
  .object({
    name: createMonitorInput.shape.name.meta({ example: 'Checkout API' }),
    url: createMonitorInput.shape.url.meta({ format: 'uri', example: 'https://api.example.com/health' }),
    interval_seconds: interval.default(300),
  })
  .meta({ description: 'A new monitor.' });
apiRegistry.add(MonitorCreate, { id: 'MonitorCreate' });

export const MonitorUpdate = z
  .object({
    name: MonitorCreate.shape.name,
    url: MonitorCreate.shape.url,
    interval_seconds: interval,
    paused: z.boolean().meta({ description: 'Pause or resume checks.' }),
  })
  .partial()
  .meta({ description: 'The fields to change; omitted fields stay as they are.' });
apiRegistry.add(MonitorUpdate, { id: 'MonitorUpdate' });

export const Monitor = z
  .object({
    id: z.string().meta({ description: 'Prefixed id.', example: 'mon_3f2a9c7e5b1d4e8fa6c0b2d4e6f80a1c' }),
    name: z.string(),
    url: z.string().meta({ format: 'uri' }),
    interval_seconds: z.number().int(),
    paused: z.boolean(),
    paused_reason: z.enum(['manual', 'plan_limit']).nullable().meta({ description: '"plan_limit": frozen after a downgrade.' }),
    created_at: dateTime('When the monitor was created.'),
  })
  .meta({ description: 'An uptime monitor.' });
apiRegistry.add(Monitor, { id: 'Monitor' });

export const Incident = z
  .object({
    id: z.string().meta({ example: 'inc_9f0e1d2c3b4a59687766554433221100' }),
    monitor_id: z.string().meta({ example: 'mon_3f2a9c7e5b1d4e8fa6c0b2d4e6f80a1c' }),
    status: z.enum(['open', 'resolved']),
    cause: z.string().meta({ example: 'HTTP 503' }),
    opened_at: dateTime('When the outage began.'),
    // Lesson 5.4, added to v1 without breaking it: a new field, never a renamed one.
    acknowledged_at: dateTime('When someone acknowledged it (this stops the escalation), or null.').nullable(),
    resolved_at: dateTime('When it was resolved.').nullable(),
  })
  .meta({ description: 'An outage of one monitor.' });
apiRegistry.add(Incident, { id: 'Incident' });

const list = <T extends z.ZodType>(item: T, what: string) =>
  z.object({
    data: z.array(item),
    has_more: z.boolean().meta({ description: 'More items after these: ask again with starting_after = next_cursor.' }),
    next_cursor: z.string().nullable().meta({ description: `The id of the last ${what} in this page, or null.` }),
  });

export const MonitorList = list(Monitor, 'monitor').meta({ description: 'A page of monitors, newest first.' });
apiRegistry.add(MonitorList, { id: 'MonitorList' });
export const IncidentList = list(Incident, 'incident').meta({ description: 'A page of incidents, newest first.' });
apiRegistry.add(IncidentList, { id: 'IncidentList' });

/** RFC 9457 problem details: every 4xx and 5xx of the API has this body, as application/problem+json. */
export const Problem = z
  .object({
    type: z.string().meta({ format: 'uri', description: 'Identifies the kind of problem; documented at that URL.', example: 'https://beacon.app/problems/rate-limited' }),
    title: z.string().meta({ description: 'A short, fixed summary of the kind of problem.', example: 'Too many requests' }),
    status: z.number().int().meta({ example: 429 }),
    detail: z.string().optional().meta({ description: 'What happened this time.' }),
    instance: z.string().optional().meta({ description: 'The request path.' }),
    errors: z
      .array(z.object({ field: z.string(), message: z.string() }))
      .optional()
      .meta({ description: 'Validation problems, one per field.' }),
  })
  .meta({ description: 'RFC 9457 problem details.' });
apiRegistry.add(Problem, { id: 'Problem' });

/** Query parameters of the list endpoints. */
export const pageParams = z.object({
  limit: z.coerce.number().int().min(1).max(100).default(20),
  starting_after: z.string().optional(),
});
export const MAX_PAGE_SIZE = 100;

export const incidentListParams = pageParams.extend({
  status: z.enum(['open', 'resolved']).optional(),
  monitor_id: z.string().optional(),
});
