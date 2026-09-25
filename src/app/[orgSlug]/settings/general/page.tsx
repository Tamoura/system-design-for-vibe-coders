import Link from 'next/link';
import { can } from '@/core/permissions';
import { forPage, requirePermission } from '@/lib/access';
import { getBillingOverview } from '@/lib/billing';
import { UsageCard } from '../../billing/usage-card';
import { RenameForm } from './rename-form';

export const dynamic = 'force-dynamic';

/**
 * Lesson 6.1 (🟡): Organization → General. Every member may look; only
 * "org.manage" (owners, admins) may change the name. The server action and
 * PATCH /api/orgs/:org/settings both check it, so hiding the form is only a courtesy.
 */
export default async function GeneralSettingsPage({ params }: { params: Promise<{ orgSlug: string }> }) {
  const { orgSlug } = await params;
  const ctx = await forPage(requirePermission(orgSlug, 'member.read'), `/${orgSlug}/settings/general`);
  const billing = can(ctx.role, 'billing.read') ? await getBillingOverview(ctx) : null; // lessons 3.2/3.3
  return (
    <section className="grid page-narrow">
      <h1>General</h1>
      {can(ctx.role, 'org.manage') ? (
        <RenameForm orgSlug={ctx.orgSlug} name={ctx.orgName} />
      ) : (
        <div className="card">
          <strong>{ctx.orgName}</strong>
          <p className="muted" style={{ margin: 0 }}>Only owners and admins can rename the organization.</p>
        </div>
      )}
      <div className="card">
        <strong>URL</strong> <code>/{ctx.orgSlug}</code>
        <p className="muted" style={{ margin: 0 }}>The slug stays the same when you rename, so links keep working.</p>
      </div>
      {billing && (
        <>
          <UsageCard overview={billing} />
          {can(ctx.role, 'billing.manage') && <div><Link href={`/${ctx.orgSlug}/billing`}>Change plan or manage billing →</Link></div>}
        </>
      )}
    </section>
  );
}
