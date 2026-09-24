CREATE TABLE "usage_alerts" (
	"organization_id" uuid NOT NULL,
	"meter" text NOT NULL,
	"period_start" timestamp with time zone NOT NULL,
	"threshold" integer NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "usage_alerts_organization_id_meter_period_start_threshold_pk" PRIMARY KEY("organization_id","meter","period_start","threshold")
);
--> statement-breakpoint
CREATE TABLE "usage_events" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"organization_id" uuid NOT NULL,
	"idempotency_key" text NOT NULL,
	"meter" text NOT NULL,
	"quantity" integer NOT NULL,
	"occurred_at" timestamp with time zone NOT NULL,
	"reported_at" timestamp with time zone,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "usage_events_idempotency_key_unique" UNIQUE("idempotency_key"),
	CONSTRAINT "usage_events_quantity_positive" CHECK ("usage_events"."quantity" > 0)
);
--> statement-breakpoint
ALTER TABLE "usage_alerts" ADD CONSTRAINT "usage_alerts_organization_id_organizations_id_fk" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "usage_events" ADD CONSTRAINT "usage_events_organization_id_organizations_id_fk" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "usage_events_org_meter_time_idx" ON "usage_events" USING btree ("organization_id","meter","occurred_at");--> statement-breakpoint
CREATE INDEX "usage_events_unreported_idx" ON "usage_events" USING btree ("organization_id") WHERE "usage_events"."reported_at" is null;--> statement-breakpoint
-- Lesson 2.4, added by hand: the usage tables are tenant tables, with the
-- same row-level security policy as the others (0007).
ALTER TABLE "usage_events" ENABLE ROW LEVEL SECURITY;--> statement-breakpoint
CREATE POLICY tenant_isolation ON "usage_events"
  USING (organization_id = current_org_id())
  WITH CHECK (organization_id = current_org_id());--> statement-breakpoint
ALTER TABLE "usage_alerts" ENABLE ROW LEVEL SECURITY;--> statement-breakpoint
CREATE POLICY tenant_isolation ON "usage_alerts"
  USING (organization_id = current_org_id())
  WITH CHECK (organization_id = current_org_id());
