import Link from 'next/link';
import { forPage, requirePermission } from '@/lib/access';
import { getPreferenceMatrix } from '@/lib/notifications';
import { PreferencesForm } from './preferences-form';

export const dynamic = 'force-dynamic';

/** Lesson 4.2 (🟡): the category × channel matrix, per person, per org. */
export default async function PreferencesPage({ params }: { params: Promise<{ orgSlug: string }> }) {
  const { orgSlug } = await params;
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.read'), `/${orgSlug}/notifications/preferences`);
  const matrix = await getPreferenceMatrix(ctx);
  return (
    <section className="grid" style={{ maxWidth: 720 }}>
      <div className="row">
        <h1 style={{ margin: 0 }}>Notification preferences</h1>
        <Link href={`/${ctx.orgSlug}/notifications`} style={{ marginLeft: 'auto' }}>← Inbox</Link>
      </div>
      <p className="muted" style={{ margin: 0 }}>
        For {ctx.orgName} only. Locked boxes are decided for you: the inbox keeps every alert, billing notices are required, and
        admins can switch a channel off for the whole organization.
      </p>
      <PreferencesForm orgSlug={ctx.orgSlug} matrix={matrix} />
    </section>
  );
}
