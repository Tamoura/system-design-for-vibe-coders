CREATE TABLE "analytics_events" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"organization_id" uuid NOT NULL,
	"user_id" uuid,
	"event" text NOT NULL,
	"properties" jsonb DEFAULT '{}'::jsonb NOT NULL,
	"org_plan" "plan_id" NOT NULL,
	"occurred_at" timestamp with time zone DEFAULT now() NOT NULL,
	"forwarded_at" timestamp with time zone
);
--> statement-breakpoint
ALTER TABLE "analytics_events" ADD CONSTRAINT "analytics_events_organization_id_organizations_id_fk" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "analytics_events" ADD CONSTRAINT "analytics_events_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "analytics_events_org_time_idx" ON "analytics_events" USING btree ("organization_id","occurred_at");--> statement-breakpoint
CREATE INDEX "analytics_events_event_time_idx" ON "analytics_events" USING btree ("event","occurred_at");--> statement-breakpoint
CREATE INDEX "analytics_events_unforwarded_idx" ON "analytics_events" USING btree ("organization_id","occurred_at") WHERE "analytics_events"."forwarded_at" is null;--> statement-breakpoint
-- Lesson 2.4, added by hand: events are tenant data, under row-level security.
ALTER TABLE "analytics_events" ENABLE ROW LEVEL SECURITY;--> statement-breakpoint
CREATE POLICY tenant_isolation ON "analytics_events"
  USING (organization_id = current_org_id())
  WITH CHECK (organization_id = current_org_id());
