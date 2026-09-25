'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useRef } from 'react';
import type { Role } from '@/core/roles';
import { switchOrgHref } from './nav';

type Org = { slug: string; name: string; role: Role };

/**
 * Lesson 6.1 (🟢) / 1.2: the org switcher. Each entry is a plain link to the
 * same section in another org (see switchOrgHref), so switching changes the
 * URL, a reload keeps you where you are, and the server re-checks the
 * membership on the next request. The current org is never kept in client
 * state or localStorage.
 *
 * Keyboard: Tab to it, Enter or Space opens it (a native <details>), Tab
 * through the orgs, Escape closes it and puts focus back on the button.
 */
export function OrgSwitcher({ current, orgs }: { current: Org; orgs: Org[] }) {
  const pathname = usePathname();
  const details = useRef<HTMLDetailsElement>(null);
  function onKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'Escape' && details.current?.open) {
      details.current.open = false;
      details.current.querySelector('summary')?.focus();
    }
  }
  return (
    <details className="switcher" ref={details} onKeyDown={onKeyDown}>
      <summary aria-label={`Organization: ${current.name}. Switch organization`}>
        <span className="switcher-name">{current.name}</span>
        <span className="badge">{current.role}</span>
      </summary>
      <div className="card switcher-menu">
        <ul>
          {orgs.map((o) => (
            <li key={o.slug}>
              <Link href={switchOrgHref(pathname, o.slug, o.role)} aria-current={o.slug === current.slug ? 'true' : undefined} onClick={() => details.current?.removeAttribute('open')}>
                {o.name} <span className="muted">· {o.role}</span>
              </Link>
            </li>
          ))}
        </ul>
        <Link href="/orgs/new">+ New organization</Link>
      </div>
    </details>
  );
}
