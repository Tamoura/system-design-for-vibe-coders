import { z } from 'zod';
import { API_SCOPES } from './api-keys';
import { apiRegistry } from './api-schemas';
import { PROBLEMS } from './problems';

/*
 * Lesson 5.2 (🟡): the OpenAPI 3.1 document for /api/v1, GENERATED from the
 * Zod schemas the handlers validate with (./api-schemas.ts). Served at
 * /api/v1/openapi.json, rendered by Scalar at /docs/api, and committed as
 * docs/openapi.json: `npm run openapi` rewrites it, and CI's
 * `npm run openapi:check` fails when the committed copy is out of date.
 *
 * Deterministic on purpose (no dates, no environment): the same code always
 * produces the same bytes, which is what makes the CI check possible.
 */
const ref = (id: string) => ({ $ref: `#/components/schemas/${id}` });
const json = (schema: object) => ({ 'application/json': { schema } });
const problemResponse = (description: string) => ({ description, content: { 'application/problem+json': { schema: ref('Problem') } } });

const rateLimitHeaders = {
  RateLimit: { description: 'IETF draft: remaining requests (r) and seconds until the bucket is full (t).', schema: { type: 'string' }, example: '"api";r=117;t=2' },
  'RateLimit-Policy': { description: 'IETF draft: the quota (q) per window (w, seconds).', schema: { type: 'string' }, example: '"api";q=120;w=60' },
  'X-RateLimit-Limit': { schema: { type: 'integer' } },
  'X-RateLimit-Remaining': { schema: { type: 'integer' } },
  'X-RateLimit-Reset': { description: 'Seconds until the bucket is full again.', schema: { type: 'integer' } },
};

const errors = {
  '400': problemResponse('Malformed request: invalid JSON, a bad query parameter, or a URL Beacon refuses to check.'),
  '401': problemResponse('Missing, unknown or revoked API key.'),
  '402': problemResponse('The organization’s plan does not include the API, or this change is over a plan limit.'),
  '403': problemResponse('The key lacks the scope this endpoint needs.'),
  '429': {
    description: 'Rate limited. Wait Retry-After seconds.',
    headers: { 'Retry-After': { schema: { type: 'integer' } }, ...rateLimitHeaders },
    content: { 'application/problem+json': { schema: ref('Problem') } },
  },
};
const notFound = { '404': problemResponse('No such object in this organization.') };
const invalid = { '422': problemResponse('Validation failed; `errors` lists the fields.') };

const paging = [
  { name: 'limit', in: 'query', schema: { type: 'integer', minimum: 1, maximum: 100, default: 20 }, description: 'Page size (at most 100).' },
  { name: 'starting_after', in: 'query', schema: { type: 'string' }, description: 'Cursor: the `next_cursor` of the previous page (an object id).' },
];
const idParam = (prefix: string) => ({ name: 'id', in: 'path', required: true, schema: { type: 'string', pattern: `^${prefix}_[0-9a-f]{32}$` } });
const scope = (s: keyof typeof API_SCOPES) => [{ apiKey: [s] }];
const ok = (description: string, schema: object) => ({ description, headers: rateLimitHeaders, content: json(schema) });

/**
 * Remove what Zod adds that the document should not promise: `$id`/`$schema`,
 * the ±2^53 bounds of every integer, and `additionalProperties: false` on
 * responses. /v1 promises ADDITIVE changes, so a client must accept fields it
 * does not know yet; a schema saying "no other fields" would contradict that.
 */
function tidy(node: unknown): void {
  if (Array.isArray(node)) return node.forEach(tidy);
  if (!node || typeof node !== 'object') return;
  const o = node as Record<string, unknown>;
  delete o.$id;
  delete o.$schema;
  if (o.additionalProperties === false) delete o.additionalProperties;
  if (o.minimum === Number.MIN_SAFE_INTEGER) delete o.minimum;
  if (o.maximum === Number.MAX_SAFE_INTEGER) delete o.maximum;
  Object.values(o).forEach(tidy);
}

export function buildOpenApiDocument() {
  const { schemas } = z.toJSONSchema(apiRegistry, { uri: (id) => `#/components/schemas/${id}`, io: 'output' }) as { schemas: Record<string, Record<string, unknown>> };
  // Input schemas describe what clients SEND (defaults are optional to send).
  const inputs = z.toJSONSchema(apiRegistry, { uri: (id) => `#/components/schemas/${id}`, io: 'input' }) as { schemas: Record<string, Record<string, unknown>> };
  for (const id of ['MonitorCreate', 'MonitorUpdate']) schemas[id] = inputs.schemas[id];
  for (const s of Object.values(schemas)) tidy(s);

  return {
    openapi: '3.1.0',
    info: {
      title: 'Beacon API',
      version: '1.0.0',
      description: [
        'Monitors and incidents of one Beacon organization, for your own scripts and tools.',
        '',
        '**Authentication.** Create a key in Settings → API keys and send it as `Authorization: Bearer bk_live_…`. A key belongs to the organization, has scopes, and can be revoked at any time.',
        '',
        '**Versioning.** `/v1` only ever gets additive changes: new endpoints, new optional parameters, new response fields. Ignore fields you do not know.',
        '',
        '**Errors** are RFC 9457 problem details (`application/problem+json`) with `type`, `title` and `status`.',
        '',
        '**Pagination.** Lists are newest first; pass `next_cursor` as `starting_after` while `has_more` is true.',
        '',
        '**Retries.** Send an `Idempotency-Key` header (any unique string, e.g. a UUID) on POST: a retry with the same key and body returns the first response instead of creating a second object. Keys are kept 24 hours.',
        '',
        '**Rate limits.** A token bucket per organization, sized by plan. Every response carries `RateLimit`/`RateLimit-Policy` (and `X-RateLimit-*`); a 429 has `Retry-After`.',
        '',
        '**Problem types:** ' + Object.entries(PROBLEMS).map(([slug, p]) => `\`${slug}\` (${p.status}, ${p.title})`).join(', ') + '.',
      ].join('\n'),
    },
    servers: [{ url: '/api/v1' }],
    security: [{ apiKey: [] }],
    paths: {
      '/monitors': {
        get: {
          operationId: 'listMonitors',
          summary: 'List monitors',
          security: scope('monitors:read'),
          parameters: paging,
          responses: { '200': ok('A page of monitors.', ref('MonitorList')), ...errors },
        },
        post: {
          operationId: 'createMonitor',
          summary: 'Create a monitor',
          security: scope('monitors:write'),
          parameters: [{ name: 'Idempotency-Key', in: 'header', schema: { type: 'string', maxLength: 255 }, description: 'Makes a retried POST safe (24 hours).' }],
          requestBody: { required: true, content: json(ref('MonitorCreate')) },
          responses: {
            '201': ok('Created.', ref('Monitor')),
            '409': problemResponse('A request with the same Idempotency-Key is still running.'),
            ...errors,
            ...invalid,
          },
        },
      },
      '/monitors/{id}': {
        parameters: [idParam('mon')],
        get: { operationId: 'getMonitor', summary: 'Get a monitor', security: scope('monitors:read'), responses: { '200': ok('The monitor.', ref('Monitor')), ...errors, ...notFound } },
        patch: {
          operationId: 'updateMonitor',
          summary: 'Update a monitor',
          security: scope('monitors:write'),
          requestBody: { required: true, content: json(ref('MonitorUpdate')) },
          responses: { '200': ok('The updated monitor.', ref('Monitor')), ...errors, ...notFound, ...invalid },
        },
        delete: {
          operationId: 'deleteMonitor',
          summary: 'Delete a monitor',
          security: scope('monitors:write'),
          responses: { '204': { description: 'Deleted.', headers: rateLimitHeaders }, ...errors, ...notFound },
        },
      },
      '/incidents': {
        get: {
          operationId: 'listIncidents',
          summary: 'List incidents',
          security: scope('incidents:read'),
          parameters: [
            ...paging,
            { name: 'status', in: 'query', schema: { type: 'string', enum: ['open', 'resolved'] } },
            { name: 'monitor_id', in: 'query', schema: { type: 'string' }, description: 'Only this monitor’s incidents.' },
          ],
          responses: { '200': ok('A page of incidents.', ref('IncidentList')), ...errors },
        },
      },
      '/incidents/{id}': {
        parameters: [idParam('inc')],
        get: { operationId: 'getIncident', summary: 'Get an incident', security: scope('incidents:read'), responses: { '200': ok('The incident.', ref('Incident')), ...errors, ...notFound } },
      },
    },
    components: {
      schemas,
      securitySchemes: {
        apiKey: {
          type: 'http',
          scheme: 'bearer',
          description: `An organization API key (bk_live_…). Scopes: ${Object.entries(API_SCOPES).map(([s, d]) => `\`${s}\` (${d.label})`).join(', ')}.`,
        },
      },
    },
  };
}
