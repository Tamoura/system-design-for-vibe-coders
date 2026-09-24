import { forPage, requirePermission } from '@/lib/access';
import { NewMonitorForm } from './new-monitor-form';

export default async function NewMonitorPage({ params }: { params: Promise<{ orgSlug: string }> }) {
  const { orgSlug } = await params;
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.write'), `/${orgSlug}/monitors/new`);
  return <NewMonitorForm orgSlug={ctx.orgSlug} />;
}
