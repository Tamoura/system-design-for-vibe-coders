import { Text } from '@react-email/components';
import { Action, EmailLayout, text } from './layout';

/*
 * Lesson 5.3 (🟡): an endpoint that failed every delivery for days is
 * switched off, and the people who can fix it are told. Sent to the org's
 * owners and admins (the roles with "integration.manage").
 */
export type WebhookDisabledProps = { orgName: string; endpointUrl: string; failingSince: string; lastError: string; url: string };

export function WebhookDisabled(p: WebhookDisabledProps) {
  return (
    <EmailLayout preview={`Beacon stopped sending webhooks to ${p.endpointUrl}.`} reason={`You are receiving this because you manage integrations for ${p.orgName}.`}>
      <Text style={text}>
        Every delivery to your webhook endpoint {p.endpointUrl} has failed since {p.failingSince.slice(0, 16).replace('T', ' ')} UTC, so Beacon has
        disabled it. The last error was: {p.lastError}
      </Text>
      <Text style={text}>
        Nothing is lost: the events are kept. Fix the endpoint, enable it again, and replay the failed messages from the delivery log.
      </Text>
      <Action href={p.url} label="Open the delivery log" />
    </EmailLayout>
  );
}
