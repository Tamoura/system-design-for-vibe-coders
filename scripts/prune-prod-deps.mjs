#!/usr/bin/env node
/**
 * Lessons 7.4 and 8.1: delete dev tools that `npm ci --omit=dev` leaves in the image.
 *
 * Why they are there: a production package can declare an *optional peer* dependency on a dev tool
 * (better-auth does, for drizzle-kit and vitest, so its CLI can use them if you have them). Because
 * our package.json installs those tools as devDependencies, npm satisfies the peer with our copy and
 * marks it as a production package, and --omit=dev keeps it, along with everything it depends on.
 * That put vitest, vite, tsx, drizzle-kit and two old Go-compiled esbuild binaries in an image that
 * is supposed to hold production code only (lesson 7.4); a vulnerability scanner flags those binaries
 * as CRITICAL (lesson 8.1).
 *
 * What this does: walk package-lock.json from our own `dependencies`, following each package's
 * dependencies, optionalDependencies and *required* peers (never optional ones), resolving names the
 * way Node does (nearest node_modules first). Anything installed but not reached is deleted.
 *
 *   node scripts/prune-prod-deps.mjs            prune ./node_modules
 *   node scripts/prune-prod-deps.mjs --dry-run  only list what would go
 */
import fs from 'node:fs';
import path from 'node:path';

const dryRun = process.argv.includes('--dry-run');
const lock = JSON.parse(fs.readFileSync('package-lock.json', 'utf8'));
const pkgs = lock.packages;

/** Where Node would find `name` when required from the package installed at `from`. */
function resolve(from, name) {
  let dir = from;
  for (;;) {
    const candidate = `${dir ? `${dir}/` : ''}node_modules/${name}`;
    if (pkgs[candidate]) return candidate;
    if (!dir) return null;
    const i = dir.lastIndexOf('/node_modules/');
    dir = i === -1 ? '' : dir.slice(0, i);
  }
}

const keep = new Set();
const queue = [''];
while (queue.length) {
  const at = queue.pop();
  const p = pkgs[at];
  const names = [
    ...Object.keys(at === '' ? p.dependencies ?? {} : { ...p.dependencies, ...p.optionalDependencies }),
    ...Object.keys(p.peerDependencies ?? {}).filter((n) => !p.peerDependenciesMeta?.[n]?.optional),
  ];
  for (const name of names) {
    const target = resolve(at, name);
    if (target && !keep.has(target)) {
      keep.add(target);
      queue.push(target);
    }
  }
}

// Only look at packages npm actually installed (it skips optional packages for other platforms).
const installed = Object.keys(pkgs).filter((k) => k && fs.existsSync(k));
// Delete outermost first; a nested package disappears with its parent.
const remove = installed
  .filter((k) => !keep.has(k))
  .filter((k, _, all) => !all.some((o) => o !== k && k.startsWith(`${o}/`)));

for (const dir of remove) {
  if (dryRun) console.log(`would remove ${dir}`);
  else fs.rmSync(dir, { recursive: true, force: true });
}
// Dangling CLI shims for deleted packages.
const bin = 'node_modules/.bin';
if (!dryRun && fs.existsSync(bin)) {
  for (const f of fs.readdirSync(bin)) {
    if (!fs.existsSync(path.join(bin, f))) fs.rmSync(path.join(bin, f), { force: true });
  }
}
// Empty @scope folders left behind.
if (!dryRun) {
  for (const f of fs.readdirSync('node_modules')) {
    const dir = path.join('node_modules', f);
    if (f.startsWith('@') && fs.readdirSync(dir).length === 0) fs.rmdirSync(dir);
  }
}
console.log(`${dryRun ? 'would prune' : 'pruned'} ${remove.length} packages not needed in production`);
