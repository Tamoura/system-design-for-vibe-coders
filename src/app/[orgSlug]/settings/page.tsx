import { redirect } from 'next/navigation';

/** Lesson 6.1 (🟡): "Settings" is several pages now; /[org]/settings opens the first one. */
export default async function SettingsIndex({ params }: { params: Promise<{ orgSlug: string }> }) {
  const { orgSlug } = await params;
  redirect(`/${orgSlug}/settings/general`);
}
