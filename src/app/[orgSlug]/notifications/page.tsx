import Link from 'next/link';
import { CHANNEL_LABELS } from '@/core/notifications';
import { forPage, requirePermission } from '@/lib/access';
import { countUnread, listNotifications } from '@/lib/notifications';
import { goToNotification, markAllReadAction, markReadAction } from './actions';

export const dynamic = 'force-dynamic';

/**
 * Lesson 4.2 (🟢): the in-app inbox. Each notification also shows its
 * delivery log (🟡): which channels it went to and what happened on each.
 */
export default async function NotificationsPage({ params }: { params: Promise<{ orgSlug: string }> }) {
  const { orgSlug } = await params;
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.read'), `/${orgSlug}/notifications`);
  const [items, unread] = await Promise.all([listNotifications(ctx), countUnread(ctx)]);
  return (
    <section className="grid">
      <div className="row">
        <h1 style={{ margin: 0 }}>Notifications</h1>
        <span className="muted" data-testid="inbox-unread">{unread} unread</span>
        <span style={{ marginLeft: 'auto' }} className="row">
          <Link href={`/${ctx.orgSlug}/notifications/preferences`}>Preferences</Link>
          {unread > 0 && (
            <form action={markAllReadAction.bind(null, ctx.orgSlug)}>
              <button className="btn secondary" data-testid="mark-all-read">Mark all as read</button>
            </form>
          )}
        </span>
      </div>
      {items.length === 0 && <div className="card muted">Nothing yet. Incidents, and billing changes if you manage billing, show up here.</div>}
      {items.map((n) => (
        <div key={n.id} className={`card grid notification${n.read ? '' : ' unread'}`} data-testid="notification" data-category={n.category}>
          <div className="row">
            {!n.read && <span className="dot down" title="unread" />}
            <form action={goToNotification.bind(null, ctx.orgSlug, n.id, n.url)} style={{ flex: 1 }}>
              <button className="link-btn" style={{ fontWeight: n.read ? 400 : 700 }}>{n.title}</button>
            </form>
            <span className="muted">{n.createdAt.toISOString().slice(0, 16).replace('T', ' ')} UTC</span>
            {!n.read && (
              <form action={markReadAction.bind(null, ctx.orgSlug, n.id)}>
                <button className="link-btn">Mark as read</button>
              </form>
            )}
          </div>
          <div className="muted">{n.body}</div>
          <div className="row" style={{ gap: '.4rem' }}>
            {n.deliveries.map((d) => (
              <span key={d.channel} className={`badge delivery ${d.status}`} data-testid={`delivery-${d.channel}`} title={d.error ?? d.providerMessageId ?? undefined}>
                {CHANNEL_LABELS[d.channel]}: {d.status}
              </span>
            ))}
          </div>
        </div>
      ))}
    </section>
  );
}
