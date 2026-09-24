-- Lesson 5.1: the job queue (pg-boss, its own `pgboss` schema, installed by
-- `npm run db:migrate` after these migrations) takes over retries and
-- backoff, so the hand-made "next attempt" columns go. The rows stay as the
-- delivery log. check_results gets the scheduler's slot, unique per monitor,
-- so a check job that runs twice stores one result.
DROP INDEX "email_outbox_due_idx";--> statement-breakpoint
DROP INDEX "notification_deliveries_due_idx";--> statement-breakpoint
ALTER TABLE "check_results" ADD COLUMN "scheduled_at" timestamp with time zone;--> statement-breakpoint
CREATE UNIQUE INDEX "check_results_monitor_slot_idx" ON "check_results" USING btree ("monitor_id","scheduled_at") WHERE "check_results"."scheduled_at" is not null;--> statement-breakpoint
CREATE INDEX "email_outbox_pending_idx" ON "email_outbox" USING btree ("created_at") WHERE "email_outbox"."status" = 'pending';--> statement-breakpoint
CREATE INDEX "notification_deliveries_pending_idx" ON "notification_deliveries" USING btree ("organization_id","created_at") WHERE "notification_deliveries"."status" = 'pending';--> statement-breakpoint
ALTER TABLE "email_outbox" DROP COLUMN "next_attempt_at";--> statement-breakpoint
ALTER TABLE "notification_deliveries" DROP COLUMN "next_attempt_at";