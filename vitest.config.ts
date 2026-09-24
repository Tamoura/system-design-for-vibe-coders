import { defineConfig } from 'vitest/config';
import path from 'node:path';

export default defineConfig({
  resolve: { alias: { '@': path.resolve(import.meta.dirname, 'src') } },
  // Database tests boot an in-memory Postgres and run the migrations first.
  test: {
    include: ['tests/**/*.test.ts'],
    environment: 'node',
    testTimeout: 30_000,
    hookTimeout: 60_000,
    // Lesson 4.1: tests never send real mail; the memory driver keeps it in an array.
    env: { EMAIL_DRIVER: 'memory' },
  },
});
