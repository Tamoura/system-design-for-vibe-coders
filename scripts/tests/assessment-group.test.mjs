#!/usr/bin/env node
/**
 * Group-view injection test for every self-assessment page.
 *
 *   node scripts/tests/assessment-group.test.mjs
 *
 * The group view (the team view on the agentic pages) reads result files that other people send, so
 * every field in them is untrusted. For each generated page (<course>/assessment[.ar].html, and the vibe
 * course's pages at the repo root) and for agentic/assessment[.ar].html, this test opens the page in
 * headless Chromium, opens the group view, and feeds it hostile records through the paste box and the
 * file input: a script payload in the score, total, level, status, name and an unknown area id (on the
 * agentic pages: name, role, level, a rating and an unknown discipline id). It then checks that no
 * payload ran, that no injected element is in the page, and that a valid record still renders.
 *
 * Uses Chromium from PUPPETEER_EXECUTABLE_PATH when it is set. Exits 1 on any failure.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import puppeteer from 'puppeteer';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const AGENTIC = ['agentic/assessment.html', 'agentic/assessment.ar.html'];

/** Every page written by scripts/build-assessment.mjs: one pair per course that has assessment sources. */
function generatedPages() {
  const out = [];
  if (fs.existsSync(path.join(ROOT, 'assessment', 'areas.json'))) out.push('assessment.html', 'assessment.ar.html');
  for (const d of fs.readdirSync(ROOT, { withFileTypes: true })) {
    if (!d.isDirectory() || d.name.startsWith('.') || d.name === 'node_modules') continue;
    if (fs.existsSync(path.join(ROOT, d.name, 'assessment', 'areas.json'))) out.push(`${d.name}/assessment.html`, `${d.name}/assessment.ar.html`);
  }
  return out;
}

// Each payload tags what it injects with data-pwn and records its id in window.__pwned if it runs.
const run = (id) => `window.__pwned=(window.__pwned||[]).concat('${id}')`;
const P = (id) => `<img data-pwn src=x onerror="${run(id)}">`;
const Q = (id) => `"><img data-pwn src=x onerror="${run(id)}"><span x="`;
const S = (id) => `<svg data-pwn onload="${run(id)}"></svg><script data-pwn>${run(id)}</script>`;

/** What the page should not contain after rendering, anywhere in the document. */
async function injected(page, box) {
  return page.evaluate((box) => {
    const bad = [];
    if (window.__pwned) bad.push(`payload ran: ${[].concat(window.__pwned).join(',')}`);
    const tagged = document.querySelectorAll('[data-pwn]').length;
    if (tagged) bad.push(`${tagged} injected element(s)`);
    const out = document.querySelector(box);
    for (const el of out ? out.querySelectorAll('*') : []) {
      if (/^(IMG|SCRIPT|SVG|IFRAME|OBJECT|EMBED|VIDEO|AUDIO|STYLE|LINK|FORM|INPUT|BASE|META)$/i.test(el.tagName)) bad.push(`unexpected <${el.tagName.toLowerCase()}> in ${box}`);
      for (const a of el.getAttributeNames()) if (/^on/i.test(a)) bad.push(`event attribute ${a} in ${box}`);
    }
    return bad;
  }, box);
}

/** Paste text into a textarea and press the page's own "add" button. */
async function paste(page, area, button, text) {
  await page.$eval(area, (el, v) => { el.value = v; }, text);
  await page.click(button);
}

/** Hand a file to a file input the way a person picking a file would. */
async function upload(page, input, text) {
  await page.$eval(input, (el, v) => {
    const dt = new DataTransfer();
    dt.items.add(new File([v], 'results.json', { type: 'application/json' }));
    el.files = dt.files;
    el.dispatchEvent(new Event('change', { bubbles: true }));
  }, text);
}

const settle = () => new Promise((r) => setTimeout(r, 400));

/* ---------------------------------------------------------------- generated pages */

async function testGenerated(page) {
  const { tool, ids, levels } = await page.evaluate(() => ({ tool: D.cfg.tool, ids: D.areas.map((a) => a.id), levels: T.levels.map((l) => l[0]) }));
  const [a0, a1] = ids;
  const hostile = [
    { tool, name: P('name'), level: 1, score: 3, total: 4, areas: { [a0]: { status: 1 } } },
    { tool, name: 'bad-score', level: 1, score: P('score'), total: 4, areas: {} },
    { tool, name: 'bad-total', level: 1, score: 3, total: P('total'), areas: {} },
    { tool, name: 'bad-level', level: P('level'), score: 3, total: 4, areas: {} },
    { tool, name: 'bad-status', level: 1, score: 3, total: 4, areas: { [a0]: { status: Q('status') }, [a1]: { status: P('status2') } } },
    { tool, name: 'bad-area', level: 1, score: 3, total: 4, areas: { [P('area-id')]: { status: 2 }, [Q('area-id2')]: { status: P('area-status') } } },
    { tool, name: 'bad-proto', level: 'constructor', score: '__proto__', total: 'toString', areas: { constructor: { status: 1 }, ['__proto__']: { status: S('proto') } } },
    { tool, name: 'bad-range', level: 9, score: 99, total: 4, areas: { [a0]: { status: -1 }, [a1]: { status: 7 } } },
    { tool, name: 'numeric-strings', level: '1', score: ' 3 ', total: '4', areas: { [a0]: { status: '2' }, [a1]: { status: '1.5' } } },
    { tool, name: 'fractions', level: 1.5, score: 2.5, total: 4, areas: { [a0]: { status: 1.5 } } },
    { tool, name: S('name2'), level: [1], score: [3], total: [4], areas: { [a0]: [2] } },
    { tool, name: 'areas-array', level: 1, score: 3, total: 4, areas: [{ status: P('array') }] },
    { tool: P('tool'), name: P('tool-name'), level: 1, score: 3, total: 4, areas: {} },
  ];
  // An export from before this change (no aware/practised/practice fields) and one from after it.
  const valid = { tool, version: 1, name: 'Valid Learner', date: '2026-01-01', lang: 'en', level: 2, score: 7, total: 10,
    areas: { [a0]: { k: 4, e: 2, status: 2 }, [a1]: { k: 3, e: 0, status: 1 } } };
  const valid2 = { ...valid, name: 'Valid Learner Two', level: 3, score: 9, aware: 2, practised: 1, practice: { ticked: 2, total: 4, selfReported: true } };

  await page.click('[data-tab="group"]');
  await paste(page, '#gpaste', '#gadd', JSON.stringify([...hostile, valid]));
  await paste(page, '#gpaste', '#gadd', hostile.map((o) => JSON.stringify(o)).join('\n') + '\n' + JSON.stringify(valid2));
  await upload(page, '#gfiles', JSON.stringify(hostile));
  await settle();

  const bad = await injected(page, '#gout');
  const rows = await page.$$eval('#gout tbody tr', (trs) => trs.map((tr) => ({
    cells: [...tr.children].map((td) => td.textContent),
    st: [...tr.querySelectorAll('.st')].map((s) => s.className),
  })));
  const row = (name) => rows.find((r) => r.cells[0] === name);
  const expect = (cond, msg) => { if (!cond) bad.push(msg); };
  for (const [name, lvl, score] of [['Valid Learner', levels[2], '7/10'], ['Valid Learner Two', levels[3], '9/10']]) {
    const r = row(name);
    expect(r, `valid record "${name}" did not render`);
    if (r) {
      expect(r.cells[1] === lvl, `"${name}": level shows "${r.cells[1]}", expected "${lvl}"`);
      expect(r.cells[2] === score, `"${name}": score shows "${r.cells[2]}", expected "${score}"`);
      expect(/\bst2\b/.test(r.st[0]) && /\bst1\b/.test(r.st[1]), `"${name}": statuses not shown (${r.st.slice(0, 2).join(' | ')})`);
    }
  }
  expect(rows.some((r) => r.cells[0].startsWith('<img data-pwn src=x onerror=')), 'a name with markup should show as plain text');
  expect(row('bad-score')?.cells[2] === '—', 'a non-numeric score should show as —');
  expect(row('bad-total')?.cells[2] === '—', 'a non-numeric total should show as —');
  expect(row('bad-level')?.cells[1] === '?', 'a non-numeric level should show as ?');
  expect(row('bad-range')?.cells[1] === '?' && row('bad-range')?.cells[2] === '—', 'out-of-range level and score should not show');
  expect(row('bad-status') && row('bad-status').st.every((c) => /^st st0$/.test(c)), 'a non-numeric status should count as Not yet');
  const ns = row('numeric-strings');
  expect(ns && ns.cells[1] === levels[1] && ns.cells[2] === '3/4' && /\bst2\b/.test(ns.st[0]) && /\bst0\b/.test(ns.st[1]), 'whole numbers written as text should be read as numbers');
  const fr = row('fractions');
  expect(fr && fr.cells[1] === '?' && fr.cells[2] === '—' && /\bst0\b/.test(fr.st[0]), 'fractions should not be accepted as a level, score or status');
  expect(!row('areas-array') && !row(P('tool-name')), 'records with areas as a list or a wrong tool should be refused');
  return bad;
}

/* ---------------------------------------------------------------- agentic pages */

async function testAgentic(page) {
  const ids = await page.evaluate(() => DISC.map((d) => d.id));
  const [d0, d1] = ids;
  const hostile = [
    { name: P('name'), role: 'developer', level: 'L1', ratings: { [d0]: 1 } },
    { name: 'bad-role', role: P('role'), level: 'L1', ratings: { [d0]: 1 } },
    { name: 'bad-level', role: 'developer', level: P('level'), ratings: {} },
    { name: 'bad-rating', role: 'developer', level: 'L1', ratings: { [d0]: Q('rating'), [d1]: P('rating2') } },
    { name: 'bad-disc', role: 'developer', level: 'L1', ratings: { [P('disc')]: 3, [Q('disc2')]: P('disc3') } },
    { name: 'bad-proto', role: '__proto__', level: S('proto'), ratings: { constructor: 2, ['__proto__']: P('proto2') } },
    { name: 'bad-tostring', role: 'toString', level: 'L1', ratings: { [d0]: 9 } },
    { name: S('name2'), role: Q('role2'), level: ['L1'], ratings: { [d0]: [2] } },
  ];
  const valid = { v: 1, toolVersion: '1.3', name: 'Valid Learner', role: 'developer', level: 'L2', knowledge: '10/20',
    ratings: { [d0]: 2, [d1]: 3 }, detail: {}, exportedAt: '2026-01-01T00:00:00.000Z' };

  await page.click('#tb-team');
  await paste(page, '#team-paste', 'button[onclick="loadTeamPaste()"]', JSON.stringify([...hostile, valid]));
  await paste(page, '#team-paste', 'button[onclick="loadTeamPaste()"]', hostile.map((o) => JSON.stringify(o)).join('\n'));
  await upload(page, '#team-files', JSON.stringify(hostile[0]));
  await settle();

  const bad = await injected(page, '#team-out');
  const rows = await page.$$eval('#team-out table:first-of-type tbody tr', (trs) => trs.map((tr) => ({
    name: tr.querySelector('td b')?.textContent, cells: [...tr.querySelectorAll('td.num')].map((td) => td.textContent),
  })));
  const r = rows.find((x) => x.name === 'Valid Learner');
  if (!r) bad.push('valid record did not render');
  else if (!r.cells[0].startsWith('2') || !r.cells[1].startsWith('3')) bad.push(`valid record ratings show ${r.cells.slice(0, 2).join(', ')}, expected 2, 3`);
  if (!rows.find((x) => x.name === P('name'))) bad.push('a name with markup should show as plain text');
  const rr = rows.find((x) => x.name === 'bad-rating');
  if (!rr || !rr.cells[0].startsWith('0') || !rr.cells[1].startsWith('0')) bad.push('a non-numeric rating should count as 0');
  return bad;
}

/* ---------------------------------------------------------------- run */

const pages = [...generatedPages().map((f) => ({ f, test: testGenerated })), ...AGENTIC.filter((f) => fs.existsSync(path.join(ROOT, f))).map((f) => ({ f, test: testAgentic }))];
const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'], executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || undefined });
let failed = 0;
try {
  for (const { f, test } of pages) {
    const page = await browser.newPage();
    const errors = [];
    page.on('dialog', (d) => d.dismiss());
    page.on('pageerror', (e) => errors.push(`page error: ${e.message}`));
    let bad;
    try {
      await page.goto(pathToFileURL(path.join(ROOT, f)).href, { waitUntil: 'load', timeout: 30000 });
      bad = [...await test(page), ...errors];
    } catch (e) {
      bad = [`could not run: ${e.message}`, ...errors];
    }
    await page.close();
    if (bad.length) { failed++; console.error(`✗ ${f}\n  ${bad.join('\n  ')}`); }
  }
} finally {
  await browser.close();
}
const expected = 22 + AGENTIC.length;
if (pages.length < expected) console.error(`✗ found ${pages.length} assessment pages, expected at least ${expected}`);
console.log(`${failed || pages.length < expected ? '✗' : '✓'} assessment group view: ${pages.length} pages, ${pages.length - failed} passed, ${failed} failed`);
process.exit(failed || pages.length < expected ? 1 : 0);
