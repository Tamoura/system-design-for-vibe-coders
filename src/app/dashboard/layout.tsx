import { requireUser } from '@/lib/session';

// Lesson 1.1: every page under /dashboard needs a signed-in user.
export default async function DashboardLayout({ children }: { children: React.ReactNode }) {
  await requireUser('/dashboard');
  return children;
}
