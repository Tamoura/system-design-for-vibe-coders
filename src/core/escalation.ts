import { z } from 'zod';

/*
 * Lesson 5.4 (🟡): escalation policies as DATA. The customer fills in a form
 * (tiers of people, channels and waits); one durable workflow in code
 * (src/lib/workflows/escalation.ts) interprets it:
 *
 *   tier 1: page Ana and Ben by SMS and email → wait 5 minutes for an ack
 *   tier 2: page the team lead                → wait 10 minutes
 *   …stop the moment someone acknowledges, or the incident resolves.
 *
 * A running escalation keeps the policy it started with (the workflow's
 * first step snapshots it), so editing the policy mid-incident changes the
 * NEXT incident, not this one.
 */
export const ESCALATION_CHANNELS = ['in_app', 'email', 'sms'] as const;
export type EscalationChannel = (typeof ESCALATION_CHANNELS)[number];

/** How many tiers the settings form offers. */
export const MAX_TIERS = 3;

export const escalationTier = z.object({
  userIds: z.array(z.uuid()).min(1, 'Pick at least one person').max(10),
  channels: z.array(z.enum(ESCALATION_CHANNELS)).min(1, 'Pick at least one channel'),
  waitMinutes: z.coerce.number().int().min(1).max(24 * 60),
});

export const escalationPolicyInput = z.object({
  tiers: z.array(escalationTier).max(5),
});

export type EscalationTier = z.infer<typeof escalationTier>;
export type EscalationPolicy = z.infer<typeof escalationPolicyInput>;

/** The signals that end an escalation: someone owns it, or it is over. */
export const ESCALATION_STOP_SIGNALS = ['incident.acknowledged', 'incident.resolved'] as const;
