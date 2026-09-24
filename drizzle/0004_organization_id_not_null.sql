ALTER TABLE "check_results" ALTER COLUMN "organization_id" SET NOT NULL;--> statement-breakpoint
ALTER TABLE "incidents" ALTER COLUMN "organization_id" SET NOT NULL;--> statement-breakpoint
ALTER TABLE "monitors" ALTER COLUMN "organization_id" SET NOT NULL;