import { render } from '@react-email/components';
import { createElement, type ReactElement } from 'react';
import { Invitation, ResetPassword, VerifyEmail } from './account';
import { PlanDowngraded, UsageAlert } from './billing';
import { IncidentOpened, IncidentResolved, MonitorFlapping, SmsHeldBack } from './incidents';
import { WebhookDisabled } from './integrations';
import { ConfirmSubscription, StatusUpdate } from './status-page';

/*
 * Lesson 4.1 (🟢): every email Beacon sends, in one registry.
 *
 *   component  the React Email template (HTML and plain text come from it)
 *   subject    from the same props
 *   sample     props for the preview (`npm run email:preview`) and the tests
 *   stream     'transactional' (account, alerts, billing) or 'status' (mail to
 *              status-page subscribers: a separate From address, lesson 4.1's
 *              "keep your streams apart")
 *   essential  still sent to an address that complained (never to one that
 *              hard-bounced): you cannot reset a password without it
 *
 * The queue stores a template NAME and its props, so a job is plain JSON and
 * the email is rendered by the worker when it is sent.
 */
type Stream = 'transactional' | 'status';

type TemplateDef<P> = {
  component: (props: P) => ReactElement;
  subject: (props: P) => string;
  sample: P;
  stream: Stream;
  essential: boolean;
};

const define = <P,>(def: Omit<TemplateDef<P>, 'stream' | 'essential'> & Partial<Pick<TemplateDef<P>, 'stream' | 'essential'>>): TemplateDef<P> => ({
  stream: 'transactional',
  essential: false,
  ...def,
});

const APP = 'http://localhost:3000';
const OPENED = '2026-09-24T03:12:00.000Z';

export const TEMPLATES = {
  'verify-email': define({
    component: VerifyEmail,
    subject: () => 'Confirm your email for Beacon',
    sample: { name: 'Ada', url: `${APP}/api/auth/verify-email?token=sample` },
    essential: true,
  }),
  'reset-password': define({
    component: ResetPassword,
    subject: () => 'Reset your Beacon password',
    sample: { name: 'Ada', url: `${APP}/reset-password?token=sample` },
    essential: true,
  }),
  invitation: define({
    component: Invitation,
    subject: (p) => `${p.inviterEmail} invited you to ${p.orgName} on Beacon`,
    sample: { inviterEmail: 'ada@acme.test', orgName: 'Acme', role: 'member', url: `${APP}/invite/sample-token` },
  }),
  'incident-opened': define({
    component: IncidentOpened,
    subject: (p) => `[${p.orgName}] ${p.monitorName} is down`,
    sample: { orgName: 'Acme', monitorName: 'checkout-api', monitorUrl: 'https://checkout.acme.test/health', cause: 'HTTP 503', openedAt: OPENED, url: `${APP}/acme/monitors/1`, unsubscribeUrl: `${APP}/unsubscribe?token=sample` },
  }),
  'incident-resolved': define({
    component: IncidentResolved,
    subject: (p) => `[${p.orgName}] ${p.monitorName} is back up`,
    sample: { orgName: 'Acme', monitorName: 'checkout-api', openedAt: OPENED, resolvedAt: '2026-09-24T03:41:00.000Z', url: `${APP}/acme/monitors/1`, unsubscribeUrl: `${APP}/unsubscribe?token=sample` },
  }),
  'monitor-flapping': define({
    component: MonitorFlapping,
    subject: (p) => `[${p.orgName}] ${p.monitorName} is flapping`,
    sample: { orgName: 'Acme', monitorName: 'checkout-api', changes: 5, url: `${APP}/acme/monitors/1`, unsubscribeUrl: `${APP}/unsubscribe?token=sample` },
  }),
  'sms-held-back': define({
    component: SmsHeldBack,
    subject: (p) => `${p.title} (SMS limit reached)`,
    sample: { orgName: 'Acme', heldBack: 1, limit: 5, title: 'checkout-api is down', url: `${APP}/acme/monitors/1` },
  }),
  'plan-downgraded': define({
    component: PlanDowngraded,
    subject: (p) => `${p.orgName} is now on the ${p.toPlan} plan`,
    sample: { orgName: 'Acme', fromPlan: 'Pro', toPlan: 'Free', maxMonitors: 5, minIntervalSec: 300, frozen: 2, url: `${APP}/acme/monitors/plan-limit` },
  }),
  'usage-alert': define({
    component: UsageAlert,
    subject: (p) => `${p.orgName} has used ${p.threshold}% of its included SMS alerts`,
    sample: { orgName: 'Acme', threshold: 80, used: 80, included: 100, planName: 'Pro', url: `${APP}/acme/billing` },
  }),
  'webhook-disabled': define({
    component: WebhookDisabled,
    subject: (p) => `[${p.orgName}] Webhook endpoint disabled after repeated failures`,
    sample: { orgName: 'Acme', endpointUrl: 'https://hooks.acme.test/beacon', failingSince: '2026-09-19T03:12:00.000Z', lastError: 'HTTP 502', url: `${APP}/acme/settings/webhooks/1` },
  }),
  'confirm-subscription': define({
    component: ConfirmSubscription,
    subject: (p) => `Confirm your subscription to ${p.orgName} status updates`,
    sample: { orgName: 'Acme', url: `${APP}/status/acme/confirm?token=sample` },
    stream: 'status',
  }),
  'status-update': define({
    component: StatusUpdate,
    subject: (p) => (p.state === 'opened' ? `[${p.orgName} status] ${p.monitorName}: investigating` : `[${p.orgName} status] ${p.monitorName}: resolved`),
    sample: { orgName: 'Acme', monitorName: 'Checkout', state: 'opened', at: OPENED, url: `${APP}/status/acme`, unsubscribeUrl: `${APP}/unsubscribe?token=sample` },
    stream: 'status',
  }),
};

export type TemplateName = keyof typeof TEMPLATES;
export type TemplateProps<N extends TemplateName> = (typeof TEMPLATES)[N]['sample'];

export function isTemplateName(name: string): name is TemplateName {
  return Object.hasOwn(TEMPLATES, name);
}

export type RenderedEmail = { subject: string; html: string; text: string; stream: Stream; essential: boolean };

/**
 * Render one template to what a mail provider needs: subject, HTML, and the
 * plain-text alternative (lesson 4.1 🟡: always send one; spam filters and
 * screen readers both look for it). Both bodies come from the same component.
 */
export async function renderEmail<N extends TemplateName>(name: N, props: TemplateProps<N>): Promise<RenderedEmail> {
  // The registry is keyed by name; TypeScript cannot see that `props` matches this entry, so widen once here.
  const def = TEMPLATES[name] as unknown as TemplateDef<TemplateProps<N>>;
  const element = createElement(def.component, props as TemplateProps<N> & object);
  const [html, text] = await Promise.all([render(element), render(element, { plainText: true })]);
  return { subject: def.subject(props), html, text, stream: def.stream, essential: def.essential };
}
