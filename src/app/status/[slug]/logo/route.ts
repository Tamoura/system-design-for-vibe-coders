import { publicLogoUrl } from '@/lib/files';

/**
 * GET /status/:slug/logo — the logo on the public status page.
 *
 * Lesson 2.2: the bucket stays private even for this genuinely public image.
 * While the org publishes its status page, anyone gets a redirect to a
 * short-lived signed URL; when it is hidden, or there is no logo, 404.
 */
export async function GET(_req: Request, { params }: { params: Promise<{ slug: string }> }) {
  const url = await publicLogoUrl((await params).slug);
  if (!url) return new Response('Not found', { status: 404 });
  return new Response(null, { status: 302, headers: { Location: url, 'Cache-Control': 'public, max-age=60' } });
}
