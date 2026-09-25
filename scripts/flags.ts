/**
 * Lesson 6.3: feature flags from the command line, for on-call at 2 a.m. and
 * for scripts. The same functions as /internal/flags (src/lib/flags/store.ts).
 *
 *   npm run flags                                    list every flag, its rule, owner, expiry
 *   npm run flags -- rollout new-scheduler 10        on for 10% of orgs (stable hash: 10 → 30 keeps the first 10%)
 *   npm run flags -- override new-scheduler acme on  target one org (on | off | clear)
 *   npm run flags -- off disable-sms-sending         master switch off: off for EVERY org (the kill switch)
 *   npm run flags -- on disable-sms-sending          master switch on (rollout and overrides apply)
 *
 * Running processes pick a change up within FLAGS_REFRESH_SECONDS (15 s by default).
 * Lesson 7.3: every change is a platform audit event, named after the operating-system
 * user who ran the command (a shell on a production box is still an actor).
 */
import './load-env'; // lesson 7.4: .env.local, like Next.js (must be the first import)
import { sql } from '../src/db';
import { cliAuditSource } from '../src/lib/audit';
import { FlagInputError, listFlagsForAdmin, setFlagOverride, setFlagRule } from '../src/lib/flags/store';

const [command, key, ...rest] = process.argv.slice(2);

async function list() {
  for (const f of await listFlagsForAdmin()) {
    const rule = !f.rule ? 'no rule (safe default)' : f.rule.enabled ? `ON for ${f.rule.rolloutPercent}%` : 'OFF for everyone';
    console.log(`${f.key}  [${f.definition?.kind ?? 'NOT IN CODE: delete it'}]  ${rule}${f.expired ? '  ⚠ past its expiry' : ''}`);
    if (f.definition) console.log(`    owner: ${f.definition.owner} · expires: ${f.definition.expires ?? 'never (ops)'} · cleanup: ${f.definition.cleanup}`);
    for (const o of f.overrides) console.log(`    override ${o.orgSlug}: ${o.enabled ? 'on' : 'off'}`);
  }
}

try {
  switch (command) {
    case undefined:
    case 'list':
      await list();
      break;
    case 'rollout':
      await setFlagRule(key, { rolloutPercent: Number(rest[0]) }, null, cliAuditSource('npm run flags'));
      console.log(`✓ ${key}: rollout ${rest[0]}%`);
      break;
    case 'on':
    case 'off':
      await setFlagRule(key, { enabled: command === 'on' }, null, cliAuditSource('npm run flags'));
      console.log(`✓ ${key}: master switch ${command}`);
      break;
    case 'override': {
      const [slug, value] = rest;
      if (!slug || !['on', 'off', 'clear'].includes(value)) throw new FlagInputError('usage: npm run flags -- override <flag> <org-slug> on|off|clear');
      await setFlagOverride(key, slug, value === 'clear' ? null : value === 'on', null, cliAuditSource('npm run flags'));
      console.log(`✓ ${key}: ${slug} ${value}`);
      break;
    }
    default:
      throw new FlagInputError(`Unknown command "${command}". Commands: list, rollout, on, off, override.`);
  }
} catch (err) {
  if (!(err instanceof FlagInputError)) throw err;
  console.error(err.message);
  process.exitCode = 1;
} finally {
  await sql.end();
}
