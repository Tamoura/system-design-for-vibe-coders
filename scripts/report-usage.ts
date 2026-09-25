/**
 * Lesson 3.3 (🟡): send recorded usage (SMS segments) to the billing
 * provider's meter. By hand:
 *
 *   npm run usage:report
 *
 * Safe to run twice, or to crash half-way: each event is sent with its
 * idempotency key as the meter event's identifier, so the provider counts it
 * once. The work is reportPendingUsage() in src/lib/usage.ts.
 * Lesson 5.1: the worker runs the same function every 5 minutes (the
 * `usage.report` schedule), so cron is no longer needed; this is for by hand.
 */
import './load-env'; // lesson 7.4: .env.local, like Next.js (must be the first import)
import { sql } from '../src/db';
import { getBillingProvider } from '../src/lib/billing/provider';
import { reportPendingUsage } from '../src/lib/usage';

if (!getBillingProvider()) console.log('Billing is not configured (no STRIPE_SECRET_KEY): nothing to report to.');
const { reported, failed } = await reportPendingUsage();
console.log(`Reported ${reported} usage event(s)${failed ? `, ${failed} failed and will be retried next run` : ''}.`);
await sql.end();
if (failed) process.exitCode = 1;
