-- Lesson 8.2: AI incident summaries (drafts a person publishes), the gateway's usage log and
-- response cache, and the per-org opt-in. All three tables are tenant data under RLS.
CREATE TYPE "public"."incident_summary_status" AS ENUM('generating', 'draft', 'published', 'failed');--> statement-breakpoint
CREATE TABLE "incident_summaries" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"organization_id" uuid NOT NULL,
	"incident_id" uuid NOT NULL,
	"status" "incident_summary_status" DEFAULT 'generating' NOT NULL,
	"headline" text,
	"body" text,
	"details" jsonb,
	"provider" text,
	"model" text,
	"input_hash" text,
	"error" text,
	"generated_at" timestamp with time zone,
	"edited_by" uuid,
	"edited_at" timestamp with time zone,
	"published_by" uuid,
	"published_at" timestamp with time zone,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "incident_summaries_incident_id_unique" UNIQUE("incident_id")
);
--> statement-breakpoint
CREATE TABLE "llm_cache" (
	"organization_id" uuid NOT NULL,
	"feature" text NOT NULL,
	"input_hash" text NOT NULL,
	"output" jsonb NOT NULL,
	"provider" text NOT NULL,
	"model" text NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "llm_cache_organization_id_feature_input_hash_pk" PRIMARY KEY("organization_id","feature","input_hash")
);
--> statement-breakpoint
CREATE TABLE "llm_usage" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"organization_id" uuid NOT NULL,
	"feature" text NOT NULL,
	"subject_id" uuid,
	"provider" text NOT NULL,
	"model" text NOT NULL,
	"outcome" text NOT NULL,
	"input_tokens" integer DEFAULT 0 NOT NULL,
	"output_tokens" integer DEFAULT 0 NOT NULL,
	"cost_micros" bigint DEFAULT 0 NOT NULL,
	"latency_ms" integer NOT NULL,
	"error" text,
	"request_id" text,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "ai_summaries_enabled" boolean DEFAULT false NOT NULL;--> statement-breakpoint
ALTER TABLE "incident_summaries" ADD CONSTRAINT "incident_summaries_organization_id_organizations_id_fk" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "incident_summaries" ADD CONSTRAINT "incident_summaries_incident_id_incidents_id_fk" FOREIGN KEY ("incident_id") REFERENCES "public"."incidents"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "incident_summaries" ADD CONSTRAINT "incident_summaries_edited_by_users_id_fk" FOREIGN KEY ("edited_by") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "incident_summaries" ADD CONSTRAINT "incident_summaries_published_by_users_id_fk" FOREIGN KEY ("published_by") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "llm_cache" ADD CONSTRAINT "llm_cache_organization_id_organizations_id_fk" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "llm_usage" ADD CONSTRAINT "llm_usage_organization_id_organizations_id_fk" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "incident_summaries_org_published_idx" ON "incident_summaries" USING btree ("organization_id","published_at");--> statement-breakpoint
CREATE INDEX "llm_cache_created_idx" ON "llm_cache" USING btree ("created_at");--> statement-breakpoint
CREATE INDEX "llm_usage_org_created_idx" ON "llm_usage" USING btree ("organization_id","created_at");--> statement-breakpoint
ALTER TABLE "incident_summaries" ENABLE ROW LEVEL SECURITY;--> statement-breakpoint
CREATE POLICY tenant_isolation ON "incident_summaries"
  USING (organization_id = current_org_id())
  WITH CHECK (organization_id = current_org_id());--> statement-breakpoint
ALTER TABLE "llm_usage" ENABLE ROW LEVEL SECURITY;--> statement-breakpoint
CREATE POLICY tenant_isolation ON "llm_usage"
  USING (organization_id = current_org_id())
  WITH CHECK (organization_id = current_org_id());--> statement-breakpoint
ALTER TABLE "llm_cache" ENABLE ROW LEVEL SECURITY;--> statement-breakpoint
CREATE POLICY tenant_isolation ON "llm_cache"
  USING (organization_id = current_org_id())
  WITH CHECK (organization_id = current_org_id());--> statement-breakpoint
-- The usage log is a metering record, like the audit log: the app adds rows and reads them, never
-- rewrites them. (Retention and org deletion run as the owner.)
REVOKE UPDATE, DELETE, TRUNCATE ON "llm_usage" FROM beacon_app;
