#!/usr/bin/env node
/**
 * Keep the agentic course pages in agentic/ free of the name of the real organisation they were written for.
 *
 *   node scripts/agentic-neutral.mjs          rewrite agentic/*.html in place
 *   node scripts/agentic-neutral.mjs --check  exit 1, naming file and text, if any page still carries the name
 *
 * The pages are generated in a separate repository and copied here by scripts/sync-agentic.sh, which runs
 * this script after the copy and the BLOCKED guard, and before agentic-nav.mjs. The rules (in
 * scripts/blocked-text.b64) are an
 * ordered list of explicit replacements (exact strings or tight regexes), English and Arabic. Each one
 * rewrites a sentence so it still reads naturally and states nothing new; statements of fact about the
 * real organisation (its cloud region, its list of regulators, whether it falls under a regulation) were
 * turned into instructions for "your organisation" or dropped. The script is idempotent: once a rule has
 * fired, its source text is gone. After the rules, a final scan fails the run if the name is still there,
 * which is how a new sentence in the source gets noticed.
 *
 * Compatibility note: assessment pages stored progress in localStorage under an older key. The key is now
 * "agent-assessment-v1"; the page reads the old key once if the new one is empty, so learners keep their
 * saved answers. Reset clears both. (The page builds the old key from two pieces so the name scan stays clean.)
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIR = path.join(ROOT, 'agentic');
const CHECK = process.argv.includes('--check');
// The organisation's name and the rewrite rules are stored base64-encoded in scripts/blocked-text.b64 so this
// public file does not carry them in plain text (obfuscation, not secrecy; see scripts/blocked_text.py).
const RAW = fs.readFileSync(path.join(ROOT, 'scripts', 'blocked-text.b64'), 'utf8')
  .split('\n').filter((l) => !l.startsWith('#')).join('');
const DATA = JSON.parse(Buffer.from(RAW, 'base64').toString('utf8'));
const NAME = new RegExp(DATA.name_regex, 'gi');

const PAGES = ['index', 'on-ramp-poster', 'learning-path', 'production-playbook', 'assessment'];
const FILES = PAGES.flatMap((p) => [`${p}.html`, `${p}.ar.html`]);

// Each rule: { lang: 'en' | 'ar' | 'any', from: string, or re + flags for a regex, to: string, only?: file name }.
// They run in order; the sentence rules come before the generic code-name rules.
const rules = DATA.rules.map((r) => ({ ...r, from: r.re !== undefined ? new RegExp(r.re, r.flags) : r.from }));

const isAr = (f) => f.endsWith('.ar.html');
let bad = 0;
for (const f of FILES) {
  const file = path.join(DIR, f);
  if (!fs.existsSync(file)) continue;
  const before = fs.readFileSync(file, 'utf8');
  let s = before;
  if (!CHECK) {
    for (const r of rules) {
      if (r.lang === 'en' && isAr(f)) continue;
      if (r.lang === 'ar' && !isAr(f)) continue;
      if (r.only && r.only !== f) continue;
      s = typeof r.from === 'string' ? s.split(r.from).join(r.to) : s.replace(r.from, r.to);
    }
    if (s !== before) { fs.writeFileSync(file, s); console.log('neutralised agentic/' + f); }
  }
  for (const m of s.matchAll(NAME)) {
    bad++;
    const i = m.index;
    console.error(`agentic/${f}: still contains "${m[0]}" near: ${s.slice(Math.max(0, i - 50), i + 60).replace(/\s+/g, ' ')}`);
  }
}
if (bad) {
  console.error(`error: ${bad} mention(s) of the organisation name remain. Add or fix a rule in scripts/blocked-text.b64 (decode with python3 scripts/blocked_text.py --show).`);
  process.exit(1);
}
if (CHECK) console.log('agentic pages carry no organisation name');
