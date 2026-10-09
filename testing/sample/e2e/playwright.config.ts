import { defineConfig } from '@playwright/test';

// Starts the sample API (and its /app page) before the tests and stops it afterwards.
export default defineConfig({
  testDir: '.',
  fullyParallel: true,
  use: { baseURL: 'http://127.0.0.1:8000', trace: 'on-first-retry' },
  webServer: {
    command: `${process.env.PYTHON ?? 'python'} -m uvicorn najm.api:app --port 8000`,
    cwd: '..',
    url: 'http://127.0.0.1:8000/health',
    reuseExistingServer: !process.env.CI,
  },
});
