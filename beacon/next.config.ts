import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // The check runner and scripts share code with the app; keep server-only
  // packages out of the client bundle.
  serverExternalPackages: ['postgres'],
};

export default nextConfig;
