import { PLANS, entitlementsFor, type PlanId } from '@/core/plans';
import type { NotifyEvent } from './pipeline';

/*
 * Lesson 4.2: the events Beacon notifies about, built in one place. Each
 * `key` names the event exactly once ("incident.opened:<id>"), which is what
 * makes notify() safe to call twice.
 */
type Org = { id: string; name: string; slug: string };
type MonitorRef = { id: string; name: string; url: string };

const monitorPath = (org: Org, monitorId: string) => `/${org.slug}/monitors/${monitorId}`;

export function incidentOpenedEvent(org: Org, monitor: MonitorRef, incident: { id: string; cause: string; openedAt: Date }): NotifyEvent {
  const openedAt = incident.openedAt.toISOString();
  return {
    orgId: org.id,
    category: 'incident.opened',
    key: `incident.opened:${incident.id}`,
    title: `${monitor.name} is down`,
    body: incident.cause,
    path: `${monitorPath(org, monitor.id)}#incident-${incident.id}`,
    monitorId: monitor.id,
    email: {
      template: 'incident-opened',
      props: { orgName: org.name, monitorName: monitor.name, monitorUrl: monitor.url, cause: incident.cause, openedAt },
    },
    statusPage: { monitorName: monitor.name, state: 'opened', at: openedAt },
  };
}

export function incidentResolvedEvent(org: Org, monitor: MonitorRef, incident: { id: string; openedAt: Date; resolvedAt: Date }): NotifyEvent {
  const resolvedAt = incident.resolvedAt.toISOString();
  return {
    orgId: org.id,
    category: 'incident.resolved',
    key: `incident.resolved:${incident.id}`,
    title: `${monitor.name} is back up`,
    body: 'Checks are passing again.',
    path: `${monitorPath(org, monitor.id)}#incident-${incident.id}`,
    monitorId: monitor.id,
    email: {
      template: 'incident-resolved',
      props: { orgName: org.name, monitorName: monitor.name, openedAt: incident.openedAt.toISOString(), resolvedAt },
    },
    statusPage: { monitorName: monitor.name, state: 'resolved', at: resolvedAt },
  };
}

/** One per flapping episode: the key carries the moment it started flapping. */
export function monitorFlappingEvent(org: Org, monitor: MonitorRef, since: Date, changes: number): NotifyEvent {
  return {
    orgId: org.id,
    category: 'monitor.flapping',
    key: `monitor.flapping:${monitor.id}:${since.toISOString()}`,
    title: `${monitor.name} is flapping`,
    body: `${changes} state changes in the last hour. Further up/down alerts are held back until it settles.`,
    path: monitorPath(org, monitor.id),
    monitorId: monitor.id,
    email: { template: 'monitor-flapping', props: { orgName: org.name, monitorName: monitor.name, changes } },
  };
}

/** Lesson 3.2's downgrade notice, now a required notification (in-app + email to billing managers). */
export function planDowngradedEvent(org: Org, change: { from: PlanId; to: PlanId; frozen: number; at: Date }): NotifyEvent {
  const ent = entitlementsFor(change.to);
  return {
    orgId: org.id,
    category: 'billing',
    key: `billing.downgraded:${org.id}:${change.at.toISOString()}`,
    title: `${org.name} is now on the ${PLANS[change.to].name} plan`,
    body: change.frozen > 0 ? `${change.frozen} monitor(s) paused to fit the plan. Their data is kept.` : 'All monitors keep running.',
    path: change.frozen > 0 ? `/${org.slug}/monitors/plan-limit` : `/${org.slug}/billing`,
    email: {
      template: 'plan-downgraded',
      props: {
        orgName: org.name,
        fromPlan: PLANS[change.from].name,
        toPlan: PLANS[change.to].name,
        maxMonitors: ent.maxMonitors,
        minIntervalSec: ent.minIntervalSec,
        frozen: change.frozen,
      },
    },
  };
}

/** Lesson 3.3's usage alert, once per org, period and threshold (the key says which). */
export function usageAlertEvent(org: Org & { plan: PlanId }, alert: { threshold: number; used: number; included: number; periodStart: Date }): NotifyEvent {
  return {
    orgId: org.id,
    category: 'billing',
    key: `billing.usage:${org.id}:sms:${alert.periodStart.toISOString()}:${alert.threshold}`,
    title: `${alert.threshold}% of included SMS alerts used`,
    body: `${alert.used} of ${alert.included} SMS alerts included in ${PLANS[org.plan].name} this billing period.`,
    path: `/${org.slug}/billing`,
    email: {
      template: 'usage-alert',
      props: { orgName: org.name, planName: PLANS[org.plan].name, threshold: alert.threshold, used: alert.used, included: alert.included },
    },
  };
}
