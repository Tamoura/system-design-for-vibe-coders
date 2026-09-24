import Link from 'next/link';
import { forPage, requirePermission } from '@/lib/access';
import { getOrganization } from '@/lib/organizations';
import { can } from '@/core/permissions';
import { getBillingOverview } from '@/lib/billing';
import { FileUploader } from '@/app/_components/file-uploader';
import { getOrgNotificationSettings } from '@/lib/notifications';
import { UsageCard } from '../billing/usage-card';
import { OrgNotificationsForm } from './org-notifications-form';
import { setStatusPageAction } from './actions';

export const dynamic = 'force-dynamic';

export default async function SettingsPage({ params }: { params: Promise<{ orgSlug: string }> }) {
  const { orgSlug } = await params;
  const ctx = await forPage(requirePermission(orgSlug, 'page.publish'), `/${orgSlug}/settings`);
  const org = await getOrganization(ctx);
  // Lessons 3.2/3.3: plan and usage, for roles with "billing.read".
  const billing = can(ctx.role, 'billing.read') ? await getBillingOverview(ctx) : null;
  // Lesson 4.2 (🟡): the org's notification policy and Slack channel.
  const notifications = can(ctx.role, 'notification.manage') ? await getOrgNotificationSettings(ctx) : null;
  // TODO(6.1): organization settings (name, custom domain) grow here.
  return (
    <section className="grid" style={{ maxWidth: 560 }}>
      <h1 style={{ margin: 0 }}>Settings</h1>
      {billing && (
        <>
          <UsageCard overview={billing} />
          {can(ctx.role, 'billing.manage') && (
            <div><Link href={`/${ctx.orgSlug}/billing`}>Change plan or manage billing →</Link></div>
          )}
        </>
      )}
      <form action={setStatusPageAction.bind(null, ctx.orgSlug)} className="card grid">
        <strong>Public status page</strong>
        <label className="row">
          <input type="checkbox" name="public" defaultChecked={org?.statusPagePublic} />
          Publish <Link href={`/status/${ctx.orgSlug}`}>/status/{ctx.orgSlug}</Link> for anyone to see
        </label>
        <div><button className="btn">Save</button></div>
      </form>
      {notifications && <OrgNotificationsForm orgSlug={ctx.orgSlug} settings={notifications} />}
      {notifications && (
        <div className="card">
          <Link href={`/${ctx.orgSlug}/settings/escalation`}>Escalation policy →</Link> <span className="muted">who is paged when nobody acknowledges an incident</span>
        </div>
      )}
      {/* Module 5: what other software uses to reach Beacon, and to hear from it. */}
      {can(ctx.role, 'integration.manage') && (
        <div className="card grid" data-testid="integrations">
          <strong>Integrations</strong>
          <Link href={`/${ctx.orgSlug}/settings/api-keys`}>API keys →</Link>
          <Link href={`/${ctx.orgSlug}/settings/webhooks`}>Webhooks →</Link>
        </div>
      )}
      {/* Lesson 2.2 (🟢): the status page logo, uploaded straight to storage. */}
      <div className="card grid">
        <strong>Status page logo</strong>
        {org?.logoFileId ? (
          // Private file: shown through the download endpoint, which checks membership.
          <img src={`/api/orgs/${ctx.orgSlug}/files/${org.logoFileId}`} alt="Current logo" className="logo" data-testid="current-logo" />
        ) : (
          <span className="muted">No logo yet.</span>
        )}
        <FileUploader requestUrl={`/api/orgs/${ctx.orgSlug}/logo`} orgSlug={ctx.orgSlug} label="PNG, JPEG or WebP, up to 2 MB:" />
      </div>
    </section>
  );
}
