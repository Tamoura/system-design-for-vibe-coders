#!/usr/bin/env node
/**
 * Check that every GitHub repository linked from the SaaS course still exists.
 *
 *   npm run saas:repos
 *
 * Uses the GitHub REST API. Set GITHUB_TOKEN to avoid the 60-requests/hour
 * anonymous limit (CI passes its own token). Reports repos that are missing,
 * renamed (the API redirects) or archived. Exits 1 if any are missing.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const files = ['saas/README.md', ...fs.readdirSync(path.join(ROOT, 'saas/modules')).filter((f) => f.endsWith('.md')).map((f) => `saas/modules/${f}`)];
const repos = new Map();
for (const f of files) {
  const md = fs.readFileSync(path.join(ROOT, f), 'utf8');
  for (const m of md.matchAll(/https:\/\/github\.com\/([\w.-]+)\/([\w.-]+?)(?=[/)#?\s>]|$)/g)) {
    const key = `${m[1]}/${m[2]}`.replace(/\.git$/, '');
    if (!repos.has(key.toLowerCase())) repos.set(key.toLowerCase(), { key, files: new Set() });
    repos.get(key.toLowerCase()).files.add(f);
  }
}

const headers = { 'User-Agent': 'saas-course-link-check', Accept: 'application/vnd.github+json' };
if (process.env.GITHUB_TOKEN) headers.Authorization = `Bearer ${process.env.GITHUB_TOKEN}`;

const missing = [], moved = [], archived = [], errors = [];
const list = [...repos.values()];
let i = 0;
async function worker() {
  while (i < list.length) {
    const r = list[i++];
    try {
      const res = await fetch(`https://api.github.com/repos/${r.key}`, { headers, redirect: 'follow' });
      if (res.status === 404) { missing.push(r); continue; }
      if (!res.ok) { errors.push(`${r.key}: HTTP ${res.status}`); continue; }
      const j = await res.json();
      if (j.full_name.toLowerCase() !== r.key.toLowerCase()) moved.push(`${r.key} → ${j.full_name}`);
      if (j.archived) archived.push(r.key);
    } catch (e) {
      errors.push(`${r.key}: ${e.message}`);
    }
  }
}
await Promise.all(Array.from({ length: 8 }, worker));

console.log(`Checked ${list.length} repositories.`);
if (moved.length) console.log(`\n↪ Renamed/moved (update the link):\n  ${moved.join('\n  ')}`);
if (archived.length) console.log(`\n🗄 Archived (say so in the lesson, or replace):\n  ${archived.join('\n  ')}`);
if (errors.length) console.log(`\n? Could not check:\n  ${errors.join('\n  ')}`);
if (missing.length) {
  console.log(`\n✗ Missing:\n  ${missing.map((r) => `${r.key}  (${[...r.files].join(', ')})`).join('\n  ')}`);
  process.exit(1);
}
console.log('\n✓ No missing repositories.');
