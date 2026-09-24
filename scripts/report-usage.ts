/**
 * Lesson 3.3 (🟡): send recorded usage (SMS segments) to the billing
 * provider's meter. Run it from cron (every few minutes), or by hand:
 *
 *   npm run usage:report
 *
 * Safe to run twice, or to crash half-way: each event is sent with its
 * idempotency key as the meter event's identifier, so the provider counts it
 * once. The work is reportPendingUsage() in src/lib/usage.ts.
 * TODO(5.1): a scheduled job in the queue replaces cron + script.
 */
import { sql } from '../src/db';
import { getBillingProvider } from '../src/lib/billing/provider';
import { reportPendingUsage } from '../src/lib/usage';

if (!getBillingProvider()) console.log('Billing is not configured (no STRIPE_SECRET_KEY): nothing to report to.');
const { reported, failed } = await reportPendingUsage();
console.log(`Reported ${reported} usage event(s)${failed ? `, ${failed} failed and will be retried next run` : ''}.`);
await sql.end();
if (failed) process.exitCode = 1;
