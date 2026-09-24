-- Lesson 2.4 (🟡): Postgres row-level security (RLS) as defence in depth.
-- A custom migration (drizzle-kit generate --custom): drizzle does not
-- generate roles, grants or policies from schema.ts, so they are written here.
--
-- How the app uses it: src/db/tenant.ts `withOrg(orgId, fn)` runs fn in a
-- transaction with `app.current_org = orgId` and `role = beacon_app`, both
-- local to that transaction. The policies below then filter every read and
-- check every write on the tenant tables.
--
-- 1. A role for tenant queries. It owns nothing and has no BYPASSRLS, so RLS
--    applies to it. Roles belong to the whole Postgres server, not to one
--    database, hence "create it unless it exists". NOLOGIN: nobody connects as
--    it; the app switches to it inside withOrg.
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'beacon_app') THEN
    CREATE ROLE beacon_app NOLOGIN;
  END IF;
END
$$;--> statement-breakpoint
-- The role that runs migrations (and the app's connection role) must be
-- allowed to switch to beacon_app. A superuser always may; on a managed
-- Postgres, the migration role created beacon_app and can grant it to itself.
GRANT beacon_app TO CURRENT_USER;--> statement-breakpoint
GRANT USAGE ON SCHEMA public TO beacon_app;--> statement-breakpoint
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO beacon_app;--> statement-breakpoint
-- Tables that later migrations create get the same privileges.
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO beacon_app;--> statement-breakpoint
-- 2. The current tenant, as set by withOrg. NULL when nothing is set, so a
--    query outside withOrg (as beacon_app) matches no rows: fail closed.
--    (current_setting(…, true) returns '' rather than NULL after a
--    transaction-local value has ended, hence the nullif.)
CREATE OR REPLACE FUNCTION current_org_id() RETURNS uuid
  LANGUAGE sql STABLE
  AS $$ SELECT nullif(current_setting('app.current_org', true), '')::uuid $$;--> statement-breakpoint
-- 3. The policies. USING filters what can be read (and which rows UPDATE and
--    DELETE can see); WITH CHECK refuses rows written with another org's id.
--
--    No FORCE ROW LEVEL SECURITY, on purpose: the table owner (the migration
--    role, and scripts such as db:seed) keeps seeing every row, so a future
--    data migration cannot silently backfill nothing. The app is protected
--    because its tenant queries run as beacon_app, which is not the owner.
--
--    Which tables: every table with organization_id except the ones read
--    *before* the org is known (memberships: "which orgs is this user in?";
--    invitations: "which org is this token for?"). tests/tenant-scoping.test.ts
--    fails if a new tenant table forgets its policy.
ALTER TABLE "monitors" ENABLE ROW LEVEL SECURITY;--> statement-breakpoint
CREATE POLICY tenant_isolation ON "monitors"
  USING (organization_id = current_org_id())
  WITH CHECK (organization_id = current_org_id());--> statement-breakpoint
ALTER TABLE "check_results" ENABLE ROW LEVEL SECURITY;--> statement-breakpoint
CREATE POLICY tenant_isolation ON "check_results"
  USING (organization_id = current_org_id())
  WITH CHECK (organization_id = current_org_id());--> statement-breakpoint
ALTER TABLE "incidents" ENABLE ROW LEVEL SECURITY;--> statement-breakpoint
CREATE POLICY tenant_isolation ON "incidents"
  USING (organization_id = current_org_id())
  WITH CHECK (organization_id = current_org_id());
