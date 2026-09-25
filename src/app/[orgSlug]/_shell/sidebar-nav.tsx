'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import type { NavGroup } from './nav';

/**
 * Lesson 6.1: the sidebar's links. A client component only to mark the
 * current page with aria-current="page" (screen readers announce it, and the
 * CSS highlights it); the list itself was filtered by role on the server.
 */
export function SidebarNav({ orgSlug, groups }: { orgSlug: string; groups: NavGroup[] }) {
  const pathname = usePathname();
  return (
    <nav aria-label="Main" className="sidebar-nav">
      {groups.map((g) => (
        <div key={g.label ?? 'main'} className="nav-group">
          {g.label && <div className="nav-label">{g.label}</div>}
          <ul>
            {g.items.map((item) => {
              const href = `/${orgSlug}/${item.section}`;
              const current = pathname === href || pathname.startsWith(`${href}/`);
              return (
                <li key={item.section}>
                  <Link href={href} aria-current={current ? 'page' : undefined}>
                    {item.label}
                  </Link>
                </li>
              );
            })}
          </ul>
        </div>
      ))}
    </nav>
  );
}
