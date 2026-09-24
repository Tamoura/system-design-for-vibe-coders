import { Text } from '@react-email/components';
import { Action, EmailLayout, muted, text, utc } from './layout';

/*
 * Lesson 4.1/4.2: mail to status-page subscribers. They are not Beacon users,
 * so everything works from signed links: confirm (double opt-in) and
 * unsubscribe (one click, RFC 8058). This is subscribed mail, sent from the
 * separate "status" stream (EMAIL_FROM_STATUS), so a complaint wave here does
 * not hurt the reputation of password resets.
 */

export type ConfirmSubscriptionProps = { orgName: string; url: string };

export function ConfirmSubscription({ orgName, url }: ConfirmSubscriptionProps) {
  return (
    <EmailLayout preview={`Confirm to get ${orgName} status updates.`} reason={`You are receiving this because this address was entered on the ${orgName} status page.`}>
      <Text style={text}>Confirm that you want an email when {orgName} has an incident, and when it is resolved.</Text>
      <Action href={url} label="Confirm subscription" />
      <Text style={muted}>If you did not ask for this, ignore this email: you will not be subscribed.</Text>
    </EmailLayout>
  );
}

export type StatusUpdateProps = {
  orgName: string;
  monitorName: string;
  state: 'opened' | 'resolved';
  at: string; // ISO
  url: string;
  unsubscribeUrl: string;
};

export function StatusUpdate(p: StatusUpdateProps) {
  return (
    <EmailLayout
      preview={p.state === 'opened' ? `${p.monitorName} is having problems.` : `${p.monitorName} is working again.`}
      reason={`You are receiving this because you subscribed to the ${p.orgName} status page.`}
      unsubscribeUrl={p.unsubscribeUrl}
    >
      <Text style={text}>
        {p.state === 'opened' ? (
          <>
            <strong>{p.monitorName}</strong> has been having problems since {utc(p.at)}. The team has been alerted.
          </>
        ) : (
          <>
            <strong>{p.monitorName}</strong> is working again (resolved at {utc(p.at)}).
          </>
        )}
      </Text>
      <Action href={p.url} label="View status page" />
    </EmailLayout>
  );
}
