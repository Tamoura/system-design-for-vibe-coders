import Link from 'next/link';
import { forPage, requirePermission } from '@/lib/access';
import { getOrgNotificationSettings } from '@/lib/notifications';
import { OrgNotificationsForm } from './org-notifications-form';

export const dynamic = 'force-dynamic';

/**
 * Lesson 6.1 (🟡): Organization → Alert channels (lesson 4.2's org policy and
 * Slack channel, moved out of the old one-page settings). Connecting Slack
 * here, or adding a webhook, is the "connect an alert channel" onboarding step.
 */
export default async function AlertChannelsPage({ params }: { params: Promise<{ orgSlug: string }> }) {
  const { orgSlug } = await params;
  const ctx = await forPage(requirePermission(orgSlug, 'notification.manage'), `/${orgSlug}/settings/notifications`);
  const settings = await getOrgNotificationSettings(ctx);
  return (
    <section className="grid page-narrow">
      <h1>Alert channels</h1>
      <OrgNotificationsForm orgSlug={ctx.orgSlug} settings={settings} />
      <div className="card grid">
        <Link href={`/${ctx.orgSlug}/settings/webhooks`}>Webhooks →</Link>
        <span className="muted">Send signed incident events to your own systems.</span>
        <Link href={`/${ctx.orgSlug}/settings/escalation`}>Escalation policy →</Link>
        <span className="muted">Who is paged when nobody acknowledges an incident.</span>
      </div>
    </section>
  );
}
