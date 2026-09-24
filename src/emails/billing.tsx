import { Text } from '@react-email/components';
import { Action, EmailLayout, text } from './layout';

/*
 * Lessons 3.2 and 3.3, sent for real since 4.1. Billing mail is a *required*
 * category (lesson 4.2): it has no unsubscribe link, because an owner who
 * turned it off would miss the reason their monitors stopped.
 */

export type PlanDowngradedProps = {
  orgName: string;
  fromPlan: string;
  toPlan: string;
  maxMonitors: number;
  minIntervalSec: number;
  frozen: number;
  url: string;
};

export function PlanDowngraded(p: PlanDowngradedProps) {
  return (
    <EmailLayout preview={`${p.orgName} is now on the ${p.toPlan} plan.`} reason={`You are receiving this because you manage billing for ${p.orgName}.`}>
      <Text style={text}>
        Your {p.fromPlan} subscription for {p.orgName} has ended, so the organization is now on {p.toPlan}.
      </Text>
      <Text style={text}>
        {p.toPlan} runs up to {p.maxMonitors} monitors, checked at most every {p.minIntervalSec} seconds.
      </Text>
      <Text style={text}>
        {p.frozen > 0
          ? `We paused ${p.frozen} monitor${p.frozen === 1 ? '' : 's'} and kept all their data. Choose which monitors run, or upgrade again to switch them all back on.`
          : 'All your monitors keep running.'}
      </Text>
      <Action href={p.url} label={p.frozen > 0 ? 'Choose which monitors run' : 'Open billing'} />
    </EmailLayout>
  );
}

export type UsageAlertProps = { orgName: string; threshold: number; used: number; included: number; planName: string; url: string };

export function UsageAlert(p: UsageAlertProps) {
  return (
    <EmailLayout preview={`${p.orgName} has used ${p.threshold}% of its included SMS alerts.`} reason={`You are receiving this because you manage billing for ${p.orgName}.`}>
      <Text style={text}>
        {p.orgName} has sent {p.used} of the {p.included} SMS alerts included in {p.planName} this billing period.
        {p.threshold >= 100 ? ' Further SMS alerts are billed at $0.05 each.' : ''}
      </Text>
      <Action href={p.url} label="See usage" />
    </EmailLayout>
  );
}
