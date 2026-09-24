'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useRealtime, useResyncOnReconnect } from './realtime';

/**
 * Lesson 4.2 (🟢) + 4.3: the bell. The server renders the count; a
 * "notification" event (sent only to its recipient) or a reconnect refetches
 * it from the API, so it is always the database's number, never a guess.
 */
export function NotificationBell({ orgSlug, unread }: { orgSlug: string; unread: number }) {
  const [count, setCount] = useState(unread);
  useEffect(() => setCount(unread), [unread]); // e.g. after "mark all as read" re-rendered the layout

  const refetch = async () => {
    const res = await fetch(`/api/orgs/${orgSlug}/notifications`, { cache: 'no-store' });
    if (res.ok) setCount((await res.json()).unread);
  };
  useRealtime('notification', () => void refetch());
  useResyncOnReconnect(() => void refetch());

  return (
    <Link href={`/${orgSlug}/notifications`} className="bell" aria-label={`Notifications, ${count} unread`}>
      🔔 <span className={`badge${count ? ' unread' : ''}`} data-testid="unread-count">{count}</span>
    </Link>
  );
}
