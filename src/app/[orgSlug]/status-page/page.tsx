import Link from 'next/link';
import { can } from '@/core/permissions';
import { forPage, requirePermission } from '@/lib/access';
import { getOrganization } from '@/lib/organizations';
import { FileUploader } from '@/app/_components/file-uploader';
import { setStatusPageAction } from './actions';

export const dynamic = 'force-dynamic';

/**
 * Lesson 6.1: the Status page section of the app shell. New orgs start
 * UNpublished (an empty status page helps nobody); publishing it is the last
 * onboarding step. Everyone in the org can see the state; "page.publish"
 * changes it (the action checks again).
 */
export default async function StatusPageSettings({ params, searchParams }: { params: Promise<{ orgSlug: string }>; searchParams: Promise<{ saved?: string }> }) {
  const { orgSlug } = await params;
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.read'), `/${orgSlug}/status-page`);
  const org = await getOrganization(ctx);
  const saved = (await searchParams).saved === '1';
  const canPublish = can(ctx.role, 'page.publish');
  const isPublic = Boolean(org?.statusPagePublic);
  return (
    <section className="grid page-narrow">
      <h1>Status page</h1>
      <div className="card grid">
        <div className="row">
          <strong>{isPublic ? 'Published' : 'Not published'}</strong>
          {isPublic && <Link href={`/status/${ctx.orgSlug}`}>Open /status/{ctx.orgSlug} →</Link>}
        </div>
        <p className="muted" style={{ margin: 0 }}>
          Your customers see your monitors’ state and your incident updates there, and can subscribe to them by email.
        </p>
        {canPublish ? (
          <form action={setStatusPageAction.bind(null, ctx.orgSlug)} className="grid">
            <label className="row">
              <input type="checkbox" name="public" defaultChecked={isPublic} />
              Publish the status page for anyone to see
            </label>
            <div className="row">
              <button className="btn">Save</button>
              {saved && <span className="muted" role="status">Saved.</span>}
            </div>
          </form>
        ) : (
          <p className="muted" style={{ margin: 0 }}>Only owners and admins can publish it.</p>
        )}
      </div>
      {/* Lesson 2.2 (🟢): the status page logo, uploaded straight to storage. */}
      <div className="card grid">
        <strong>Logo</strong>
        {org?.logoFileId ? (
          // Private file: shown through the download endpoint, which checks membership.
          <img src={`/api/orgs/${ctx.orgSlug}/files/${org.logoFileId}`} alt="Current logo" className="logo" data-testid="current-logo" />
        ) : (
          <span className="muted">No logo yet.</span>
        )}
        {canPublish && <FileUploader requestUrl={`/api/orgs/${ctx.orgSlug}/logo`} orgSlug={ctx.orgSlug} label="PNG, JPEG or WebP, up to 2 MB:" />}
      </div>
      <p className="muted">Custom domains (status.yourcompany.com) are not built yet: lesson 6.1’s 🔴 exercise.</p>
    </section>
  );
}
