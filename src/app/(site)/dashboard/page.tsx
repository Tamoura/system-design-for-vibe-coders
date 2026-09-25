import { redirect } from 'next/navigation';
import { listOrganizationsForUser } from '@/lib/organizations';
import { requireUser } from '@/lib/session';

export const dynamic = 'force-dynamic';

/** "/dashboard" has no org in it, so send the user to their first organization. */
export default async function Dashboard() {
  const user = await requireUser('/dashboard');
  const [first] = await listOrganizationsForUser(user.id);
  redirect(first ? `/${first.slug}/monitors` : '/orgs/new');
}
