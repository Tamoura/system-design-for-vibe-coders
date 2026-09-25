/**
 * Lesson 8.1 (🟡): encryption at rest, from the command line.
 *
 *   npm run secrets                 how many stored secrets each key wraps, and any plaintext left
 *   npm run secrets -- rotate       re-wrap every data key with the CURRENT key (the first in
 *                                   ENCRYPTION_KEYS). No data is re-encrypted; safe while the app runs.
 *   npm run secrets -- encrypt      encrypt plaintext left from before Module 8 (db:migrate does this)
 *   npm run secrets -- generate-key print a new random key for ENCRYPTION_KEYS
 *
 * The rotation runbook is in docs/security/secrets.md.
 */
import './load-env'; // lesson 7.4: .env.local, like Next.js (must be the first import)
import { randomBytes } from 'node:crypto';
import { sql } from '../src/db';
import { cliAuditSource } from '../src/lib/audit';
import { getKms } from '../src/lib/secrets/kms';
import { encryptLegacySecrets, rewrapAllSecrets, secretsStatus } from '../src/lib/secrets/maintenance';

const [command] = process.argv.slice(2);
const source = cliAuditSource(`npm run secrets ${command ?? ''}`.trim());

try {
  switch (command) {
    case undefined:
    case 'status': {
      const kms = getKms();
      const { byKey, plaintext } = await secretsStatus();
      console.log(`Current key: ${kms.currentKeyId} (keyring: ${kms.keyIds.join(', ')})`);
      for (const [id, n] of Object.entries(byKey)) console.log(`  ${String(n).padStart(5)} wrapped with ${id}${id === kms.currentKeyId ? '' : '   ← run: npm run secrets -- rotate'}`);
      if (plaintext) console.log(`  ${String(plaintext).padStart(5)} still in PLAIN TEXT   ← run: npm run secrets -- encrypt`);
      break;
    }
    case 'rotate': {
      const r = await rewrapAllSecrets({ source });
      console.log(`✓ re-wrapped ${r.webhookSecrets} webhook secret(s) and ${r.slackUrls} Slack URL(s) with key ${r.toKey}`);
      break;
    }
    case 'encrypt': {
      const r = await encryptLegacySecrets({ source });
      console.log(`✓ encrypted ${r.webhookSecrets} webhook secret(s) and ${r.slackUrls} Slack URL(s)`);
      break;
    }
    case 'generate-key':
      console.log(`k${Date.now().toString(36)}:${randomBytes(32).toString('base64')}`);
      break;
    default:
      console.error('Usage: npm run secrets [-- status | rotate | encrypt | generate-key]');
      process.exitCode = 1;
  }
} finally {
  await sql.end();
}
