/**
 * Lesson 7.4: the production image runs the worker, the migrations and the
 * admin CLIs with plain `node`, not `tsx` (a dev dependency, which the image
 * does not contain). This bundles each entry point's TypeScript, Beacon's own
 * code only, into dist/scripts/*.mjs; npm packages stay imports resolved from
 * node_modules at runtime.
 *
 *   npm run build:scripts     (the Dockerfile runs it after `next build`)
 */
import { build } from 'esbuild';

const entryPoints = ['worker', 'migrate', 'seed', 'staff', 'audit', 'jobs', 'flags'].map((name) => `scripts/${name}.ts`);

await build({
  entryPoints,
  outdir: 'dist/scripts',
  outExtension: { '.js': '.mjs' },
  bundle: true,
  platform: 'node',
  format: 'esm',
  target: 'node22',
  packages: 'external', // node_modules are installed in the image; only our code is bundled
  jsx: 'automatic', // the React Email templates (src/emails/*.tsx)
  sourcemap: true, // readable stack traces in logs and in Sentry
  logLevel: 'info',
});
