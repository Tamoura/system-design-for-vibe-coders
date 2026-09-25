import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // The check runner and scripts share code with the app; keep server-only
  // packages out of the client bundle.
  // @node-rs/argon2 is a native module (lesson 1.1's password hashing), and
  // so is sharp (lesson 2.2's thumbnails). pg-boss (lesson 5.1) brings the pg driver.
  // Lesson 7.2: pino and the Sentry Node SDK load worker threads and native hooks at runtime.
  serverExternalPackages: ['postgres', '@node-rs/argon2', 'sharp', 'pg-boss', 'pg', 'pino', '@sentry/node'],
  // Lesson 1.3: enables `forbidden()`, which renders app/forbidden.tsx with a
  // real 403 status when a role lacks a permission.
  experimental: { authInterrupts: true },
  // Lesson 7.2: browser source maps, for readable stack traces in Sentry. Only in the Docker
  // build (SOURCE_MAPS=1), which uploads them and deletes them (scripts/sentry-sourcemaps.sh).
  productionBrowserSourceMaps: process.env.SOURCE_MAPS === '1',
  // Lesson 6.1 (🟡): account settings moved to /settings/account (user-level),
  // next to the org-level /[org]/settings/…. Old links keep working.
  async redirects() {
    return [{ source: '/account', destination: '/settings/account', permanent: true }];
  },
};

export default nextConfig;
