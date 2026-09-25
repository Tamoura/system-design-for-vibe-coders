CREATE TABLE "org_milestones" (
	"organization_id" uuid NOT NULL,
	"milestone" text NOT NULL,
	"reached_at" timestamp with time zone DEFAULT now() NOT NULL,
	"user_id" uuid,
	CONSTRAINT "org_milestones_organization_id_milestone_pk" PRIMARY KEY("organization_id","milestone")
);
--> statement-breakpoint
ALTER TABLE "organizations" ALTER COLUMN "status_page_public" SET DEFAULT false;--> statement-breakpoint
ALTER TABLE "org_milestones" ADD CONSTRAINT "org_milestones_organization_id_organizations_id_fk" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "org_milestones" ADD CONSTRAINT "org_milestones_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
-- Lesson 6.1, added by hand: only the milestones src/core/onboarding.ts knows.
ALTER TABLE "org_milestones" ADD CONSTRAINT "org_milestones_milestone_check"
  CHECK ("milestone" IN ('monitor_created', 'first_check', 'alert_channel_connected', 'teammate_invited', 'status_page_published'));--> statement-breakpoint
-- Lesson 2.4: tenant data, under the same row-level security policy as everything else.
ALTER TABLE "org_milestones" ENABLE ROW LEVEL SECURITY;--> statement-breakpoint
CREATE POLICY tenant_isolation ON "org_milestones"
  USING (organization_id = current_org_id())
  WITH CHECK (organization_id = current_org_id());--> statement-breakpoint
-- Lesson 6.1 (🟡), a data migration: organizations that existed before this
-- module already did some of these things. Record them, with the time they
-- happened, so their owners are not walked through "add your first monitor"
-- again. (Existing orgs keep status_page_public as it was: only the column's
-- DEFAULT changed above, for new orgs.)
INSERT INTO "org_milestones" ("organization_id", "milestone", "reached_at")
  SELECT organization_id, 'monitor_created', min(created_at) FROM monitors GROUP BY organization_id
ON CONFLICT DO NOTHING;--> statement-breakpoint
INSERT INTO "org_milestones" ("organization_id", "milestone", "reached_at")
  SELECT organization_id, 'first_check', min(checked_at) FROM check_results GROUP BY organization_id
ON CONFLICT DO NOTHING;--> statement-breakpoint
INSERT INTO "org_milestones" ("organization_id", "milestone", "reached_at")
  SELECT org_id, 'alert_channel_connected', min(at) FROM (
    SELECT id AS org_id, updated_at AS at FROM organizations WHERE slack_webhook_url IS NOT NULL
    UNION ALL
    SELECT organization_id, created_at FROM webhook_endpoints
  ) channels GROUP BY org_id
ON CONFLICT DO NOTHING;--> statement-breakpoint
INSERT INTO "org_milestones" ("organization_id", "milestone", "reached_at")
  SELECT organization_id, 'teammate_invited', min(at) FROM (
    SELECT organization_id, created_at AS at FROM invitations
    UNION ALL
    SELECT organization_id, created_at FROM memberships WHERE role <> 'owner'
  ) teammates GROUP BY organization_id
ON CONFLICT DO NOTHING;--> statement-breakpoint
INSERT INTO "org_milestones" ("organization_id", "milestone", "reached_at")
  SELECT id, 'status_page_published', created_at FROM organizations WHERE status_page_public
ON CONFLICT DO NOTHING;
