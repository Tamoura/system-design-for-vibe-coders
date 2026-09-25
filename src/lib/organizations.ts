import { and, asc, eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { isUsableSlug, slugify, withRandomSuffix } from '@/core/slugs';
import type { Role } from '@/core/roles';

const { organizations, memberships } = schema;

export type OrganizationSummary = { id: string; name: string; slug: string; role: Role };

/**
 * Lesson 1.2: create an organization and make its creator the owner, in one
 * transaction, so there is never an org without an owner.
 */
export async function createOrganization(ownerUserId: string, name: string): Promise<{ id: string; slug: string }> {
  const base = slugify(name);
  let slug = isUsableSlug(base) ? base : withRandomSuffix(base);
  for (let attempt = 0; attempt < 5; attempt++) {
    try {
      return await db.transaction(async (tx) => {
        const [org] = await tx.insert(organizations).values({ name, slug }).returning();
        await tx.insert(memberships).values({ organizationId: org.id, userId: ownerUserId, role: 'owner' });
        return { id: org.id, slug: org.slug };
      });
    } catch (err) {
      if (!isUniqueViolation(err)) throw err;
      slug = withRandomSuffix(base); // "acme" is taken: try "acme-x7k2"
    }
  }
  throw new Error('Could not find a free slug for this organization');
}

/**
 * Lesson 1.2: every new user gets a personal organization, so there is never a
 * monitor without an org and never a second code path for solo users.
 */
export async function createPersonalOrganization(user: { id: string; name: string }) {
  const first = user.name.trim().split(/\s+/)[0] || 'My';
  return createOrganization(user.id, `${first}'s workspace`);
}

/** Every organization the user belongs to, for the org switcher and /dashboard. */
export async function listOrganizationsForUser(userId: string): Promise<OrganizationSummary[]> {
  return db
    .select({ id: organizations.id, name: organizations.name, slug: organizations.slug, role: memberships.role })
    .from(memberships)
    .innerJoin(organizations, eq(organizations.id, memberships.organizationId))
    .where(eq(memberships.userId, userId))
    .orderBy(asc(memberships.createdAt));
}

/**
 * Lesson 1.2: the org slug in the URL is a claim, not a fact. This lookup is
 * the fact: the user's membership in that org, or null.
 */
export async function findMembership(orgSlug: string, userId: string): Promise<OrganizationSummary | null> {
  const [row] = await db
    .select({ id: organizations.id, name: organizations.name, slug: organizations.slug, role: memberships.role })
    .from(memberships)
    .innerJoin(organizations, eq(organizations.id, memberships.organizationId))
    .where(and(eq(organizations.slug, orgSlug), eq(memberships.userId, userId)))
    .limit(1);
  return row ?? null;
}

/** For the public status page: no membership needed, but the org must have published it. */
export async function findPublicStatusPage(slug: string) {
  const [org] = await db
    .select({ id: organizations.id, name: organizations.name, statusPagePublic: organizations.statusPagePublic, logoFileId: organizations.logoFileId })
    .from(organizations)
    .where(eq(organizations.slug, slug))
    .limit(1);
  return org && org.statusPagePublic ? org : null;
}

/** Publish or hide /status/[slug]. The caller has checked "page.publish". */
export async function setStatusPagePublic({ orgId }: { orgId: string }, isPublic: boolean) {
  await db.update(organizations).set({ statusPagePublic: isPublic }).where(eq(organizations.id, orgId));
}

/**
 * Lesson 6.1 (🟡): rename the organization. The caller has checked
 * "org.manage" on the server (a Member gets 403 from the endpoint, not just a
 * hidden button). The slug, and so every URL, stays the same.
 */
export async function renameOrganization({ orgId }: { orgId: string }, name: string) {
  await db.update(organizations).set({ name }).where(eq(organizations.id, orgId));
}

export async function getOrganization({ orgId }: { orgId: string }) {
  const [org] = await db.select().from(organizations).where(eq(organizations.id, orgId)).limit(1);
  return org ?? null;
}

function isUniqueViolation(err: unknown): boolean {
  // Postgres error 23505. Drizzle may wrap the driver error, so look at `cause` too.
  const e = err as { code?: string; cause?: { code?: string } };
  return e?.code === '23505' || e?.cause?.code === '23505';
}
