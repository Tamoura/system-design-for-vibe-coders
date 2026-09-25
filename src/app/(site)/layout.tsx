import { SiteFrame } from '@/app/_components/site-header';

/** Signed-in pages that belong to no single organization (account settings, new org, invitations). */
export default function SiteLayout({ children }: { children: React.ReactNode }) {
  return <SiteFrame>{children}</SiteFrame>;
}
