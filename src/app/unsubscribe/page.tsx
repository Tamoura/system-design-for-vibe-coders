import { describeLink } from '@/lib/notifications/subscribers';
import { unsubscribeAction } from './actions';
import { LinkActionForm } from './link-form';

export const dynamic = 'force-dynamic';

/**
 * Lesson 4.2 (🟡): unsubscribe without logging in. The page explains what the
 * signed link does and asks for one click; nothing happens on GET.
 */
export default async function UnsubscribePage({ searchParams }: { searchParams: Promise<{ token?: string }> }) {
  const token = (await searchParams).token ?? '';
  const link = await describeLink(token);
  return (
    <section className="card grid" style={{ maxWidth: 520 }}>
      <meta name="referrer" content="no-referrer" />
      <h1 style={{ margin: 0 }}>Unsubscribe</h1>
      {link.ok && link.action === 'Unsubscribe' ? (
        <>
          <p>{link.message}</p>
          <LinkActionForm action={unsubscribeAction.bind(null, token)} label="Unsubscribe" />
        </>
      ) : (
        <p className="error">{link.ok ? 'This is not an unsubscribe link.' : link.message}</p>
      )}
    </section>
  );
}
