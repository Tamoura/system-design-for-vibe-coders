import { buildOpenApiDocument } from '@/core/openapi';

/**
 * GET /api/v1/openapi.json — lesson 5.2 (🟡): the machine-readable contract,
 * generated from the same Zod schemas the handlers validate with. Public, like
 * any API reference: it describes the API, it holds no data.
 */
export const dynamic = 'force-static';

export function GET() {
  return Response.json(buildOpenApiDocument(), { headers: { 'access-control-allow-origin': '*' } });
}
