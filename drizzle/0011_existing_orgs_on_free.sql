-- Lesson 3.2 (🟡): every organization that existed before Module 3 starts on
-- Free, because nobody has paid yet. Apply Free's limits to their data the
-- way a downgrade would (the FREEZE policy): nothing is deleted.
--
--   1. Intervals below Free's minimum (300 s) are raised to it.
--   2. At most 5 monitors keep running per org: the oldest running ones.
--      The newer ones are paused with reason 'plan_limit', so an upgrade (or
--      the owner's choice on /<org>/monitors/plan-limit) switches them back on.
--      Monitors paused by hand stay paused by hand.
--
-- The numbers are copied from PLANS.free in src/core/plans.ts on the day this
-- migration was written, on purpose: a migration is history and must give the
-- same result forever, so it never imports application code that can change.
UPDATE "monitors" SET "interval_seconds" = 300 WHERE "interval_seconds" < 300;
--> statement-breakpoint
WITH ranked AS (
  SELECT "id",
         row_number() OVER (PARTITION BY "organization_id" ORDER BY "created_at", "id") AS n
  FROM "monitors"
  WHERE NOT "paused"
)
UPDATE "monitors" m
   SET "paused" = true, "paused_reason" = 'plan_limit'
  FROM ranked
 WHERE m."id" = ranked."id" AND ranked.n > 5;
