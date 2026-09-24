-- Lesson 1.2: expand → backfill → contract.
-- 0002 added organization_id as a NULLABLE column; this migration fills it in;
-- 0004 makes it NOT NULL. Doing it in one step would fail on any database that
-- already has monitors.
--
-- Before Module 1, Beacon was single-tenant: monitors belonged to nobody. They
-- move into one organization called "Default organization" (slug "default").
-- It has no members yet. After you sign up, make yourself its owner with:
--   npm run org:claim -- default you@example.com
INSERT INTO "organizations" ("name", "slug")
SELECT 'Default organization', 'default'
WHERE EXISTS (SELECT 1 FROM "monitors")
  AND NOT EXISTS (SELECT 1 FROM "organizations" WHERE "slug" = 'default');
--> statement-breakpoint
UPDATE "monitors"
SET "organization_id" = (SELECT "id" FROM "organizations" WHERE "slug" = 'default')
WHERE "organization_id" IS NULL;
--> statement-breakpoint
-- The tenant_id rule: child rows copy their monitor's organization_id.
UPDATE "check_results" AS cr
SET "organization_id" = m."organization_id"
FROM "monitors" AS m
WHERE cr."monitor_id" = m."id" AND cr."organization_id" IS NULL;
--> statement-breakpoint
UPDATE "incidents" AS i
SET "organization_id" = m."organization_id"
FROM "monitors" AS m
WHERE i."monitor_id" = m."id" AND i."organization_id" IS NULL;
--> statement-breakpoint
-- Users who signed up before organizations existed get the personal
-- organization that new users get at sign-up (src/lib/organizations.ts).
WITH lonely AS (
  SELECT u."id", u."name" FROM "users" AS u
  WHERE NOT EXISTS (SELECT 1 FROM "memberships" AS m WHERE m."user_id" = u."id")
), created AS (
  INSERT INTO "organizations" ("name", "slug")
  SELECT "name" || '''s workspace', 'personal-' || left(replace("id"::text, '-', ''), 12) FROM lonely
  RETURNING "id", "slug"
)
INSERT INTO "memberships" ("organization_id", "user_id", "role")
SELECT c."id", l."id", 'owner'
FROM created AS c
JOIN lonely AS l ON c."slug" = 'personal-' || left(replace(l."id"::text, '-', ''), 12);
