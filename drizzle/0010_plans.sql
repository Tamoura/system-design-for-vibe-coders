CREATE TYPE "public"."paused_reason" AS ENUM('manual', 'plan_limit');--> statement-breakpoint
CREATE TYPE "public"."plan_id" AS ENUM('free', 'pro', 'business');--> statement-breakpoint
ALTER TABLE "monitors" ADD COLUMN "paused_reason" "paused_reason";--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "plan" "plan_id" DEFAULT 'free' NOT NULL;--> statement-breakpoint
-- Lesson 3.2 (🟡), added by hand: monitors paused before this migration were
-- paused by a person. Backfill the reason BEFORE the check constraint below,
-- which would otherwise refuse every paused row.
UPDATE "monitors" SET "paused_reason" = 'manual' WHERE "paused" AND "paused_reason" IS NULL;--> statement-breakpoint
ALTER TABLE "monitors" ADD CONSTRAINT "monitors_paused_reason_check" CHECK ("monitors"."paused" = ("monitors"."paused_reason" is not null));