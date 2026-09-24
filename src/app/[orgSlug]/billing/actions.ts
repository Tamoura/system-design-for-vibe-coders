'use server';

import { redirect } from 'next/navigation';
import { isPaidPlanId } from '@/core/plans';
import { forPage, requirePermission } from '@/lib/access';
import { openPortal, startCheckout } from '@/lib/billing';
import { InvalidRequestError } from '@/lib/errors';

/*
 * Lesson 3.1 (🟢): "Upgrade" and "Manage billing". A server action is a
 * public POST endpoint, so each checks "billing.manage" itself (lesson 1.3):
 * hiding the buttons from non-owners is only the courtesy half.
 */

export async function upgradeAction(orgSlug: string, plan: string) {
  const back = `/${orgSlug}/billing`;
  const ctx = await forPage(requirePermission(orgSlug, 'billing.manage'), back);
  if (!isPaidPlanId(plan)) redirect(`${back}?error=unknown_plan`);
  let url: string;
  try {
    ({ url } = await startCheckout(ctx, plan));
  } catch (err) {
    if (err instanceof InvalidRequestError) redirect(`${back}?error=${err.code}`);
    throw err;
  }
  redirect(url); // to Stripe's hosted Checkout page
}

export async function manageBillingAction(orgSlug: string) {
  const back = `/${orgSlug}/billing`;
  const ctx = await forPage(requirePermission(orgSlug, 'billing.manage'), back);
  let url: string;
  try {
    ({ url } = await openPortal(ctx));
  } catch (err) {
    if (err instanceof InvalidRequestError) redirect(`${back}?error=${err.code}`);
    throw err;
  }
  redirect(url); // to Stripe's hosted Customer Portal
}
