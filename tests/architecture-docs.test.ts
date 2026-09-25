import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { describe, expect, it } from 'vitest';

/*
 * Lesson 9.1: the architecture docs, the ADRs and the readiness review cite
 * the code by file path ("Every claim must match the code"). This keeps them
 * honest when code moves: every path in `backticks` that points into the
 * repo, and every relative Markdown link, must exist.
 */
const ROOT = resolve(__dirname, '..');
const DOCS = [
  'docs/architecture.md',
  'docs/readiness-review.md',
  ...readdirSync(join(ROOT, 'docs/adr')).filter((f) => f.endsWith('.md')).map((f) => `docs/adr/${f}`),
];
const REPO_PATH = /^(src|tests|docs|scripts|drizzle|ops|evals|\.github)\/[^\s]*$|^(Dockerfile|docker-compose[\w.-]*\.yml|package\.json)$/;

function citedPaths(markdown: string): string[] {
  const prose = markdown.replace(/^```[\s\S]*?^```/gm, ''); // code blocks hold diagrams and templates, not citations
  return [...prose.matchAll(/`([^`\n]+)`/g)].map((m) => m[1].trim()).filter((p) => REPO_PATH.test(p));
}

function relativeLinks(markdown: string): string[] {
  return [...markdown.matchAll(/\]\(([^)\s]+)\)/g)].map((m) => m[1].split('#')[0]).filter((l) => l && !/^[a-z]+:/i.test(l));
}

describe('the architecture docs cite files that exist', () => {
  it('there are at least the three documents and ten ADRs', () => {
    expect(DOCS.filter((d) => /docs\/adr\/\d{4}-/.test(d)).length).toBeGreaterThanOrEqual(10);
  });

  for (const doc of DOCS) {
    it(`${doc}: every cited path and relative link resolves`, () => {
      const text = readFileSync(join(ROOT, doc), 'utf8');
      const paths = citedPaths(text);
      expect(paths.length, `${doc} cites no file at all`).toBeGreaterThan(0);
      const missing = paths.filter((p) => !existsSync(join(ROOT, p)));
      const brokenLinks = relativeLinks(text).filter((l) => !existsSync(join(ROOT, dirname(doc), l)));
      expect({ missing, brokenLinks }).toEqual({ missing: [], brokenLinks: [] });
    });
  }

  it('each ADR has the sections of the template and fits on a page', () => {
    for (const doc of DOCS.filter((d) => /docs\/adr\/\d{4}-/.test(d))) {
      const text = readFileSync(join(ROOT, doc), 'utf8');
      for (const section of ['## Context', '## Decision', '## Alternatives rejected', '## Consequences', '## Revisit when']) {
        expect(text, `${doc} lacks "${section}"`).toContain(section);
      }
      const rejected = text.split('## Alternatives rejected')[1].split('## Consequences')[0];
      expect(rejected.match(/^\d\. /gm)?.length, `${doc}: two alternatives`).toBeGreaterThanOrEqual(2);
      expect(text.split('\n').length, `${doc} is longer than a page`).toBeLessThanOrEqual(75);
    }
  });
});
