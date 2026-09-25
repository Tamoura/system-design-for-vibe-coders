import { describeLink } from '@/lib/notifications/subscribers';
import { LinkActionForm } from '@/app/(site)/unsubscribe/link-form';
import { confirmSubscriptionAction } from '../actions';

export const dynamic = 'force-dynamic';

/**
 * Lesson 4.2 (🟡): the second half of double opt-in. Opening the emailed
 * link shows a button; the subscription is confirmed by the POST, so an
 * email scanner that opens every link does not subscribe anyone.
 */
export default async function ConfirmSubscriptionPage({ searchParams }: { searchParams: Promise<{ token?: string }> }) {
  const token = (await searchParams).token ?? '';
  const link = await describeLink(token);
  return (
    <section className="card grid" style={{ maxWidth: 520 }}>
      <meta name="referrer" content="no-referrer" />
      <h1 style={{ margin: 0 }}>Status updates</h1>
      {link.ok && link.action === 'Confirm subscription' ? (
        <>
          <p>{link.message}</p>
          <LinkActionForm action={confirmSubscriptionAction.bind(null, token)} label="Confirm subscription" />
        </>
      ) : (
        <p className="error">{link.ok ? 'This is not a confirmation link.' : link.message}</p>
      )}
    </section>
  );
}
