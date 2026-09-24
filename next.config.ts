import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // The check runner and scripts share code with the app; keep server-only
  // packages out of the client bundle.
  // @node-rs/argon2 is a native module (lesson 1.1's password hashing).
  serverExternalPackages: ['postgres', '@node-rs/argon2'],
  // Lesson 1.3: enables `forbidden()`, which renders app/forbidden.tsx with a
  // real 403 status when a role lacks a permission.
  experimental: { authInterrupts: true },
};

export default nextConfig;
