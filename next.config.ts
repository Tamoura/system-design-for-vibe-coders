import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // The check runner and scripts share code with the app; keep server-only
  // packages out of the client bundle.
  // @node-rs/argon2 is a native module (lesson 1.1's password hashing).
  serverExternalPackages: ['postgres', '@node-rs/argon2'],
};

export default nextConfig;
