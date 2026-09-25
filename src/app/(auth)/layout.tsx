import { SiteFrame } from '@/app/_components/site-header';

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return <SiteFrame>{children}</SiteFrame>;
}
