import { Text } from '@react-email/components';
import { Action, duration, EmailLayout, muted, text, utc } from './layout';

/*
 * Lesson 4.1 (🟢) and 4.2: incident alerts to the org's members. The subject
 * and the first line say what broke; the rest is one click away in Beacon.
 * Optional mail, so it carries an unsubscribe link (per category, no login,
 * lesson 4.2) and the List-Unsubscribe headers (added by the sender).
 */

export type IncidentOpenedProps = {
  orgName: string;
  monitorName: string;
  monitorUrl: string;
  cause: string;
  openedAt: string; // ISO
  url: string;
  unsubscribeUrl?: string;
};

export function IncidentOpened(p: IncidentOpenedProps) {
  return (
    <EmailLayout
      preview={`${p.monitorName} is down: ${p.cause}`}
      reason={`You are receiving this because you are a member of ${p.orgName} on Beacon.`}
      unsubscribeUrl={p.unsubscribeUrl}
    >
      <Text style={text}>
        <strong>{p.monitorName}</strong> is down.
      </Text>
      <Text style={text}>
        {p.monitorUrl} failed its last checks: {p.cause}. Beacon opened an incident at {utc(p.openedAt)}.
      </Text>
      <Action href={p.url} label="Open the incident" />
    </EmailLayout>
  );
}

export type IncidentResolvedProps = {
  orgName: string;
  monitorName: string;
  openedAt: string;
  resolvedAt: string;
  url: string;
  unsubscribeUrl?: string;
};

export function IncidentResolved(p: IncidentResolvedProps) {
  return (
    <EmailLayout
      preview={`${p.monitorName} is back up after ${duration(p.openedAt, p.resolvedAt)}.`}
      reason={`You are receiving this because you are a member of ${p.orgName} on Beacon.`}
      unsubscribeUrl={p.unsubscribeUrl}
    >
      <Text style={text}>
        <strong>{p.monitorName}</strong> is back up.
      </Text>
      <Text style={text}>
        The incident opened at {utc(p.openedAt)} was resolved at {utc(p.resolvedAt)}, after {duration(p.openedAt, p.resolvedAt)}.
      </Text>
      <Action href={p.url} label="See what happened" />
    </EmailLayout>
  );
}

export type MonitorFlappingProps = { orgName: string; monitorName: string; changes: number; url: string; unsubscribeUrl?: string };

/** Lesson 4.2 (🟡): one email instead of an alert per state change. */
export function MonitorFlapping(p: MonitorFlappingProps) {
  return (
    <EmailLayout
      preview={`${p.monitorName} keeps going up and down. We will stay quiet until it settles.`}
      reason={`You are receiving this because you are a member of ${p.orgName} on Beacon.`}
      unsubscribeUrl={p.unsubscribeUrl}
    >
      <Text style={text}>
        <strong>{p.monitorName}</strong> is flapping: it changed state {p.changes} times in the last hour.
      </Text>
      <Text style={text}>
        To avoid burying you in alerts, Beacon holds back further “down” and “up” notifications for this monitor until it has been stable for an hour.
        The dashboard keeps showing its live state.
      </Text>
      <Action href={p.url} label="Open the monitor" />
    </EmailLayout>
  );
}

export type SmsHeldBackProps = { orgName: string; heldBack: number; limit: number; title: string; url: string };

/** Lesson 4.2 (🟡): the SMS throttle's fallback. The alert still reaches the person, by email. */
export function SmsHeldBack(p: SmsHeldBackProps) {
  return (
    <EmailLayout
      preview={`${p.title} (SMS limit reached)`}
      reason={`You are receiving this because you turned on SMS alerts for ${p.orgName} on Beacon.`}
    >
      <Text style={text}>
        <strong>{p.title}</strong>
      </Text>
      <Text style={text}>
        You have already had {p.limit} SMS alerts in the last hour, so Beacon sent this one by email instead.{' '}
        {p.heldBack === 1 ? '1 SMS alert has' : `${p.heldBack} SMS alerts have`} been held back this hour.
      </Text>
      <Action href={p.url} label="Open Beacon" />
      <Text style={muted}>SMS alerts start again once fewer than {p.limit} have been sent in the past hour.</Text>
    </EmailLayout>
  );
}

/**
 * Lesson 5.4: a page from the escalation policy. Required (the policy chose
 * this person and this channel), so no unsubscribe link; acknowledging the
 * incident is what stops the pages.
 */
export type IncidentEscalatedProps = {
  orgName: string;
  monitorName: string;
  cause: string;
  openedAt: string;
  tier: number;
  url: string;
};

export function IncidentEscalated(p: IncidentEscalatedProps) {
  return (
    <EmailLayout preview={`Escalation tier ${p.tier}: ${p.monitorName} is down and nobody has acknowledged it.`} reason={`You are on the escalation policy of ${p.orgName}.`}>
      <Text style={text}>
        <strong>{p.monitorName}</strong> is down ({p.cause}) since {utc(p.openedAt)}, and nobody has acknowledged it{p.tier > 1 ? ' yet' : ''}.
      </Text>
      <Text style={text}>You are on tier {p.tier} of the escalation policy. Acknowledge the incident to stop the escalation.</Text>
      <Action href={p.url} label="Acknowledge in Beacon" />
    </EmailLayout>
  );
}
