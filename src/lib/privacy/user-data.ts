import { and, eq, ne, or } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import type { AuditSource } from '@/core/audit';
import { recordAudit } from '../audit';
import { InvalidRequestError } from '../errors';
import { orgDeletionBlockers, scheduleOrgDeletionInTx } from './org-data';

const {
  users, accounts, sessions, memberships, organizations, staffUsers, notifications, notificationPreferences, notificationDeliveries,
  monitors, incidents, incidentUpdates, files, apiKeys, webhookEndpoints, invitations, orgMilestones, analyticsEvents, auditEvents,
  escalationPolicies, emailOutbox, incidentSummaries,
} = schema;

/*
 * Lesson 8.1 (GDPR data subject rights), for ONE PERSON:
 *
 *   exportUserData()  Art. 15/20, access and portability: everything Beacon holds
 *                     about this user, as JSON, from Account settings.
 *   deleteAccount()   Art. 17, erasure: the user row goes, and Postgres cascades
 *                     to their sessions, logins, memberships, notifications and
 *                     preferences; what they created in an org (monitors, notes)
 *                     stays with the org and forgets them (created_by → null).
 *
 * The org-ownership edge cases, decided up front (accountDeletionPlan):
 *   - the only owner of an org with other members: REFUSED until they make someone
 *     else owner (an org must never be left without an owner, lesson 1.2);
 *   - the only member of an org: the org is scheduled for deletion with the account
 *     (7-day grace, like an owner's request; Beacon support can still stop it);
 *   - such an org still paying: REFUSED until the subscription is cancelled;
 *   - Beacon staff: refused here; staff are removed with `npm run staff`.
 *
 * What is kept, on purpose: audit events keep the name and email the user had
 * when they acted. The audit log is evidence (lesson 7.3) and its hash chain
 * covers those fields; GDPR Art. 17(3) allows keeping it for legal claims,
 * and the audit retention deletes it on schedule. Status-page subscriptions
 * are the org's (the controller's) list, with one-click unsubscribe in every email.
 */

/**
 * Where each column that points at a user is handled, checked against the
 * database by tests/privacy.test.ts: a new `user_id` column fails that test
 * until someone decides whether it is in the export and what deletion does.
 */
export const USER_DATA_COVERAGE: Record<string, string> = {
  'sessions.user_id': 'exported (sessions); deleted with the user',
  'accounts.user_id': 'exported (loginMethods, without tokens or password hash); deleted with the user',
  'memberships.user_id': 'exported (organizations); deleted with the user',
  'notifications.user_id': 'exported; deleted with the user',
  'notification_preferences.user_id': 'exported; deleted with the user',
  'notification_deliveries.user_id': 'exported (deliveries); deleted with the user',
  'presence.user_id': 'not exported (ephemeral: the last 30 seconds); deleted with the user',
  'monitors.created_by': 'exported (monitorsCreated); kept by the org, author forgotten',
  'incidents.acknowledged_by': 'exported (incidentsAcknowledged); kept by the org, person forgotten',
  'incident_updates.author_id': 'exported (incidentUpdates); kept by the org, author forgotten',
  'files.uploaded_by': 'exported (filesUploaded); kept by the org, uploader forgotten',
  'api_keys.created_by': 'exported (apiKeysCreated, prefix only); kept by the org',
  'api_keys.revoked_by': 'kept by the org, person forgotten',
  'webhook_endpoints.created_by': 'exported (webhookEndpointsCreated); kept by the org',
  'invitations.invited_by': 'exported (invitationsSent); kept by the org',
  'invitations.accepted_by': 'kept by the org, person forgotten',
  'escalation_policies.updated_by': 'exported (escalationPoliciesEdited); kept by the org',
  'org_milestones.user_id': 'exported (milestones); kept by the org',
  'analytics_events.user_id': 'exported (productEvents); kept pseudonymously (user_id → null)',
  'organizations.deletion_requested_by': 'exported (organizations); person forgotten',
  'org_exports.requested_by': 'kept by the org, person forgotten',
  'feature_flags.updated_by': 'staff configuration, not customer data',
  'feature_flag_overrides.updated_by': 'staff configuration, not customer data',
  'staff_users.user_id': 'staff are not deleted here (npm run staff)',
  'impersonation_sessions.target_user_id': 'staff records; deleted with the user',
  'incident_summaries.edited_by': 'exported (aiSummariesEditedOrPublished); kept by the org, person forgotten',
  'incident_summaries.published_by': 'exported (aiSummariesEditedOrPublished); kept by the org, person forgotten',
};

/** Everything Beacon holds about one user, across every org they are in. */
export async function exportUserData(userId: string, now = new Date()) {
  const [user] = await db.select().from(users).where(eq(users.id, userId));
  if (!user) return null;
  const loginMethods = await db
    .select({ provider: accounts.providerId, accountId: accounts.accountId, createdAt: accounts.createdAt })
    .from(accounts)
    .where(eq(accounts.userId, userId));
  const sessionRows = await db
    .select({ createdAt: sessions.createdAt, expiresAt: sessions.expiresAt, ipAddress: sessions.ipAddress, userAgent: sessions.userAgent })
    .from(sessions)
    .where(eq(sessions.userId, userId));
  const orgs = await db
    .select({ id: organizations.id, name: organizations.name, slug: organizations.slug, role: memberships.role, joinedAt: memberships.createdAt })
    .from(memberships)
    .innerJoin(organizations, eq(organizations.id, memberships.organizationId))
    .where(eq(memberships.userId, userId));

  // Per org, inside withOrg: row-level security applies to the export like to everything else.
  const perOrg = [];
  for (const org of orgs) {
    perOrg.push(
      await withOrg(org.id, async (tx) => ({
        organization: org,
        notifications: await tx.select().from(notifications).where(and(eq(notifications.organizationId, org.id), eq(notifications.userId, userId))),
        notificationPreferences: await tx.select().from(notificationPreferences).where(and(eq(notificationPreferences.organizationId, org.id), eq(notificationPreferences.userId, userId))),
        deliveries: await tx
          .select({ channel: notificationDeliveries.channel, recipient: notificationDeliveries.recipient, status: notificationDeliveries.status, sentAt: notificationDeliveries.sentAt, createdAt: notificationDeliveries.createdAt })
          .from(notificationDeliveries)
          .where(and(eq(notificationDeliveries.organizationId, org.id), eq(notificationDeliveries.userId, userId))),
        monitorsCreated: await tx.select({ id: monitors.id, name: monitors.name, url: monitors.url, createdAt: monitors.createdAt }).from(monitors).where(and(eq(monitors.organizationId, org.id), eq(monitors.createdBy, userId))),
        incidentsAcknowledged: await tx.select({ id: incidents.id, acknowledgedAt: incidents.acknowledgedAt }).from(incidents).where(and(eq(incidents.organizationId, org.id), eq(incidents.acknowledgedBy, userId))),
        incidentUpdates: await tx.select({ incidentId: incidentUpdates.incidentId, body: incidentUpdates.body, createdAt: incidentUpdates.createdAt }).from(incidentUpdates).where(and(eq(incidentUpdates.organizationId, org.id), eq(incidentUpdates.authorId, userId))),
        filesUploaded: await tx.select({ id: files.id, name: files.originalName, kind: files.kind, createdAt: files.createdAt }).from(files).where(and(eq(files.organizationId, org.id), eq(files.uploadedBy, userId))),
        apiKeysCreated: await tx.select({ name: apiKeys.name, keyStart: apiKeys.keyStart, createdAt: apiKeys.createdAt, revokedAt: apiKeys.revokedAt }).from(apiKeys).where(and(eq(apiKeys.organizationId, org.id), eq(apiKeys.createdBy, userId))),
        webhookEndpointsCreated: await tx.select({ url: webhookEndpoints.url, createdAt: webhookEndpoints.createdAt }).from(webhookEndpoints).where(and(eq(webhookEndpoints.organizationId, org.id), eq(webhookEndpoints.createdBy, userId))),
        invitationsSent: await tx.select({ email: invitations.email, role: invitations.role, sentAt: invitations.sentAt }).from(invitations).where(and(eq(invitations.organizationId, org.id), eq(invitations.invitedBy, userId))),
        escalationPoliciesEdited: await tx.select({ updatedAt: escalationPolicies.updatedAt }).from(escalationPolicies).where(and(eq(escalationPolicies.organizationId, org.id), eq(escalationPolicies.updatedBy, userId))),
        aiSummariesEditedOrPublished: await tx
          .select({ incidentId: incidentSummaries.incidentId, headline: incidentSummaries.headline, editedAt: incidentSummaries.editedAt, publishedAt: incidentSummaries.publishedAt })
          .from(incidentSummaries)
          .where(and(eq(incidentSummaries.organizationId, org.id), or(eq(incidentSummaries.editedBy, userId), eq(incidentSummaries.publishedBy, userId)))),
        milestones: await tx.select().from(orgMilestones).where(and(eq(orgMilestones.organizationId, org.id), eq(orgMilestones.userId, userId))),
        productEvents: await tx.select({ event: analyticsEvents.event, properties: analyticsEvents.properties, occurredAt: analyticsEvents.occurredAt }).from(analyticsEvents).where(and(eq(analyticsEvents.organizationId, org.id), eq(analyticsEvents.userId, userId))),
        // What they did, from the audit log (their own actions, in this org).
        auditEvents: await tx
          .select({ action: auditEvents.action, occurredAt: auditEvents.occurredAt, targetType: auditEvents.targetType, targetName: auditEvents.targetName, ipAddress: auditEvents.ipAddress, userAgent: auditEvents.userAgent })
          .from(auditEvents)
          .where(and(eq(auditEvents.organizationId, org.id), eq(auditEvents.actorId, userId))),
      })),
    );
  }
  return {
    format: 'beacon-personal-data-export',
    version: 1,
    exportedAt: now.toISOString(),
    profile: { id: user.id, name: user.name, email: user.email, emailVerified: user.emailVerified, phoneNumber: user.phoneNumber, image: user.image, createdAt: user.createdAt },
    loginMethods,
    sessions: sessionRows,
    organizations: perOrg,
  };
}

/** Record that the user downloaded their data (a platform event: it is about the person, not one org). */
export async function recordUserExport(userId: string, source: AuditSource) {
  await db.transaction((tx) => recordAudit(tx, { orgId: null, action: 'account.data_exported', source, target: { type: 'user', id: userId } }));
}

export type AccountDeletionPlan = {
  /** Why it cannot happen yet (empty = it can). */
  blockers: string[];
  /** Orgs where this user is the only member: deleted with the account. */
  orgsToDelete: { id: string; name: string }[];
  /** Orgs the user simply leaves. */
  orgsToLeave: { id: string; name: string }[];
};

export async function accountDeletionPlan(userId: string): Promise<AccountDeletionPlan> {
  const plan: AccountDeletionPlan = { blockers: [], orgsToDelete: [], orgsToLeave: [] };
  const [staff] = await db.select({ id: staffUsers.id }).from(staffUsers).where(eq(staffUsers.userId, userId));
  if (staff) plan.blockers.push('This is a Beacon staff account. Staff are removed with `npm run staff -- remove`.');
  const mine = await db
    .select({ id: organizations.id, name: organizations.name, role: memberships.role })
    .from(memberships)
    .innerJoin(organizations, eq(organizations.id, memberships.organizationId))
    .where(eq(memberships.userId, userId));
  for (const org of mine) {
    const others = await db.select({ role: memberships.role }).from(memberships).where(and(eq(memberships.organizationId, org.id), ne(memberships.userId, userId)));
    if (others.length === 0) {
      plan.orgsToDelete.push({ id: org.id, name: org.name });
      const blockers = await withOrg(org.id, (tx) => orgDeletionBlockers(tx, org.id));
      for (const b of blockers) plan.blockers.push(`${org.name}: ${b}`);
    } else {
      plan.orgsToLeave.push({ id: org.id, name: org.name });
      if (org.role === 'owner' && !others.some((o) => o.role === 'owner')) {
        plan.blockers.push(`You are the only owner of ${org.name}. Make another member owner first (Members), or remove the other members and delete the organization.`);
      }
    }
  }
  return plan;
}

/**
 * Delete the account, in ONE transaction as the database owner (it spans
 * several orgs and the users table): schedule the orgs the user was alone in,
 * note in every other org's audit log that they left, delete their queued
 * emails and the user row. Everything commits together or nothing does.
 */
export async function deleteAccount(user: { id: string; email: string }, opts: { confirmEmail: string; source: AuditSource; now?: Date }) {
  if (opts.confirmEmail.trim().toLowerCase() !== user.email.toLowerCase()) {
    throw new InvalidRequestError('confirmation_mismatch', 'Type your email address exactly to confirm.');
  }
  const plan = await accountDeletionPlan(user.id);
  if (plan.blockers.length) throw new InvalidRequestError('deletion_blocked', plan.blockers.join(' '));
  await db.transaction(async (tx) => {
    for (const org of plan.orgsToDelete) await scheduleOrgDeletionInTx(tx, org.id, { requestedBy: null, source: opts.source, now: opts.now });
    for (const org of plan.orgsToLeave) {
      await recordAudit(tx, { orgId: org.id, action: 'member.account_deleted', source: opts.source, target: { type: 'user', id: user.id } });
    }
    await tx.delete(emailOutbox).where(eq(emailOutbox.to, user.email.toLowerCase()));
    await recordAudit(tx, {
      orgId: null,
      action: 'account.deleted',
      source: opts.source,
      target: { type: 'user', id: user.id },
      metadata: { orgs_left: plan.orgsToLeave.length, orgs_scheduled_for_deletion: plan.orgsToDelete.length },
    });
    // The cascade: sessions (signed out everywhere), logins, memberships, notifications, preferences…
    await tx.delete(users).where(eq(users.id, user.id));
  });
  return plan;
}
