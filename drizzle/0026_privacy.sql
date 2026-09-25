-- Lesson 8.1 (GDPR): organization data export (org_exports) and organization deletion with a
-- 7-day grace period (organizations.deletion_scheduled_for). See src/lib/privacy/.
CREATE TYPE "public"."org_export_status" AS ENUM('pending', 'ready', 'failed');--> statement-breakpoint
CREATE TABLE "org_exports" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"organization_id" uuid NOT NULL,
	"requested_by" uuid,
	"status" "org_export_status" DEFAULT 'pending' NOT NULL,
	"storage_key" text,
	"size_bytes" integer,
	"error" text,
	"completed_at" timestamp with time zone,
	"expires_at" timestamp with time zone NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "deletion_scheduled_for" timestamp with time zone;--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "deletion_requested_by" uuid;--> statement-breakpoint
ALTER TABLE "org_exports" ADD CONSTRAINT "org_exports_organization_id_organizations_id_fk" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "org_exports" ADD CONSTRAINT "org_exports_requested_by_users_id_fk" FOREIGN KEY ("requested_by") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "org_exports_org_created_idx" ON "org_exports" USING btree ("organization_id","created_at");--> statement-breakpoint
ALTER TABLE "organizations" ADD CONSTRAINT "organizations_deletion_requested_by_users_id_fk" FOREIGN KEY ("deletion_requested_by") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
-- Tenant data, under row-level security like every other tenant table (lesson 2.4).
ALTER TABLE "org_exports" ENABLE ROW LEVEL SECURITY;--> statement-breakpoint
CREATE POLICY tenant_isolation ON "org_exports"
  USING (organization_id = current_org_id())
  WITH CHECK (organization_id = current_org_id());
