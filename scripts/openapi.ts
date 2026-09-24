/**
 * Lesson 5.2 (🟡): write the OpenAPI document (generated from the Zod
 * schemas in src/core/api-schemas.ts) to docs/openapi.json.
 *
 *   npm run openapi          regenerate it after changing the API; commit the result
 *   npm run openapi:check    CI: fail if the committed file is out of date
 *
 * Why commit a generated file: the diff shows reviewers exactly how the public
 * contract changed, and a change that was not meant to change it stands out.
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { buildOpenApiDocument } from '../src/core/openapi';

const FILE = 'docs/openapi.json';
const generated = `${JSON.stringify(buildOpenApiDocument(), null, 2)}\n`;

if (process.argv.includes('--check')) {
  let committed = '';
  try {
    committed = readFileSync(FILE, 'utf8');
  } catch {
    // missing: treated as out of date
  }
  if (committed !== generated) {
    console.error(`${FILE} is out of date. Run \`npm run openapi\` and commit the result.`);
    process.exit(1);
  }
  console.log(`✓ ${FILE} matches the code`);
} else {
  writeFileSync(FILE, generated);
  console.log(`✓ wrote ${FILE}`);
}
