/**
 * Lesson 1.2: the organization's slug goes in the URL (/acme/monitors), so it
 * must be URL-safe, unique, and must not collide with Beacon's own top-level
 * routes: an org called "Login" must not take over /login.
 */
export const RESERVED_SLUGS = new Set([
  'account', 'api', 'dashboard', 'forgot-password', 'invite', 'login', 'logout', 'orgs',
  'reset-password', 'settings', 'signup', 'status', 'admin', 'app', 'www', 'help', 'docs', '_next',
]);

export function slugify(name: string): string {
  const slug = name
    .normalize('NFKD')
    .replace(/[̀-ͯ]/g, '') // "Café" → "Cafe"
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 40)
    .replace(/-+$/, '');
  return slug.length >= 2 ? slug : 'org';
}

export function isUsableSlug(slug: string): boolean {
  return /^[a-z0-9](?:[a-z0-9-]{0,38}[a-z0-9])?$/.test(slug) && !RESERVED_SLUGS.has(slug);
}

/** "acme" → "acme-x7k2", used when the plain slug is taken or reserved. */
export function withRandomSuffix(slug: string, random: () => number = Math.random): string {
  const suffix = Array.from({ length: 4 }, () => 'abcdefghijkmnpqrstuvwxyz23456789'[Math.floor(random() * 32)]).join('');
  return `${slug.slice(0, 35)}-${suffix}`;
}
