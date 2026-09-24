/**
 * Lesson 4.1 (🟢): "every template renders in a preview". Renders each
 * template in src/emails with its sample props to .email-preview/:
 *
 *   npm run email:preview      then open .email-preview/index.html
 *
 * Each template gets <name>.html and <name>.txt (the plain-text part), so
 * you see both bodies a mail client can show. Mailpit (http://localhost:8025)
 * is the other preview: it shows real sent mail and checks the HTML against
 * email-client support.
 */
import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { renderEmail, TEMPLATES, type TemplateName } from '../src/emails';

const out = path.resolve('.email-preview');
mkdirSync(out, { recursive: true });
const rows: string[] = [];
for (const name of Object.keys(TEMPLATES) as TemplateName[]) {
  const email = await renderEmail(name, TEMPLATES[name].sample);
  writeFileSync(path.join(out, `${name}.html`), email.html);
  writeFileSync(path.join(out, `${name}.txt`), `Subject: ${email.subject}\n\n${email.text}`);
  rows.push(`<tr><td><a href="${name}.html">${name}</a></td><td><a href="${name}.txt">text</a></td><td>${email.stream}</td><td>${escape(email.subject)}</td></tr>`);
  console.log(`✓ ${name}: ${email.subject}`);
}
writeFileSync(
  path.join(out, 'index.html'),
  `<!doctype html><meta charset="utf-8"><title>Beacon emails</title><body style="font-family:sans-serif"><h1>Beacon email templates</h1><table cellpadding="6">${rows.join('')}</table>`,
);
console.log(`\nOpen ${path.join(out, 'index.html')}`);

function escape(s: string) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
}
