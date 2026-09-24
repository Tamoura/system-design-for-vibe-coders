CREATE TYPE "public"."workflow_run_status" AS ENUM('running', 'waiting', 'completed', 'failed');--> statement-breakpoint
CREATE TYPE "public"."workflow_step_status" AS ENUM('running', 'waiting', 'completed', 'failed');--> statement-breakpoint
ALTER TYPE "public"."notification_category" ADD VALUE 'incident.escalated' BEFORE 'billing';--> statement-breakpoint
CREATE TABLE "escalation_policies" (
	"organization_id" uuid PRIMARY KEY NOT NULL,
	"tiers" jsonb NOT NULL,
	"updated_by" uuid,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "workflow_runs" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"organization_id" uuid NOT NULL,
	"workflow" text NOT NULL,
	"key" text NOT NULL,
	"subject_id" uuid,
	"input" jsonb NOT NULL,
	"status" "workflow_run_status" DEFAULT 'running' NOT NULL,
	"output" jsonb,
	"error" text,
	"wake_at" timestamp with time zone,
	"completed_at" timestamp with time zone,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "workflow_runs_key_unique" UNIQUE("key")
);
--> statement-breakpoint
CREATE TABLE "workflow_signals" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"organization_id" uuid NOT NULL,
	"run_id" uuid NOT NULL,
	"name" text NOT NULL,
	"payload" jsonb,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "workflow_steps" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"organization_id" uuid NOT NULL,
	"run_id" uuid NOT NULL,
	"name" text NOT NULL,
	"status" "workflow_step_status" NOT NULL,
	"input" jsonb,
	"output" jsonb,
	"error" text,
	"attempts" integer DEFAULT 0 NOT NULL,
	"wake_at" timestamp with time zone,
	"started_at" timestamp with time zone DEFAULT now() NOT NULL,
	"finished_at" timestamp with time zone,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
ALTER TABLE "incidents" ADD COLUMN "acknowledged_at" timestamp with time zone;--> statement-breakpoint
ALTER TABLE "incidents" ADD COLUMN "acknowledged_by" uuid;--> statement-breakpoint
ALTER TABLE "escalation_policies" ADD CONSTRAINT "escalation_policies_organization_id_organizations_id_fk" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "escalation_policies" ADD CONSTRAINT "escalation_policies_updated_by_users_id_fk" FOREIGN KEY ("updated_by") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "workflow_runs" ADD CONSTRAINT "workflow_runs_organization_id_organizations_id_fk" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "workflow_signals" ADD CONSTRAINT "workflow_signals_organization_id_organizations_id_fk" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "workflow_signals" ADD CONSTRAINT "workflow_signals_run_id_workflow_runs_id_fk" FOREIGN KEY ("run_id") REFERENCES "public"."workflow_runs"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "workflow_steps" ADD CONSTRAINT "workflow_steps_organization_id_organizations_id_fk" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "workflow_steps" ADD CONSTRAINT "workflow_steps_run_id_workflow_runs_id_fk" FOREIGN KEY ("run_id") REFERENCES "public"."workflow_runs"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "workflow_runs_subject_idx" ON "workflow_runs" USING btree ("organization_id","subject_id");--> statement-breakpoint
CREATE INDEX "workflow_signals_run_idx" ON "workflow_signals" USING btree ("run_id","created_at");--> statement-breakpoint
CREATE UNIQUE INDEX "workflow_steps_run_name_idx" ON "workflow_steps" USING btree ("run_id","name");--> statement-breakpoint
ALTER TABLE "incidents" ADD CONSTRAINT "incidents_acknowledged_by_users_id_fk" FOREIGN KEY ("acknowledged_by") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
-- Lesson 2.4, added by hand: workflow runs, steps, signals and escalation
-- policies are tenant data, under the same row-level security policy.
ALTER TABLE "workflow_runs" ENABLE ROW LEVEL SECURITY;--> statement-breakpoint
CREATE POLICY tenant_isolation ON "workflow_runs"
  USING (organization_id = current_org_id())
  WITH CHECK (organization_id = current_org_id());--> statement-breakpoint
ALTER TABLE "workflow_steps" ENABLE ROW LEVEL SECURITY;--> statement-breakpoint
CREATE POLICY tenant_isolation ON "workflow_steps"
  USING (organization_id = current_org_id())
  WITH CHECK (organization_id = current_org_id());--> statement-breakpoint
ALTER TABLE "workflow_signals" ENABLE ROW LEVEL SECURITY;--> statement-breakpoint
CREATE POLICY tenant_isolation ON "workflow_signals"
  USING (organization_id = current_org_id())
  WITH CHECK (organization_id = current_org_id());--> statement-breakpoint
ALTER TABLE "escalation_policies" ENABLE ROW LEVEL SECURITY;--> statement-breakpoint
CREATE POLICY tenant_isolation ON "escalation_policies"
  USING (organization_id = current_org_id())
  WITH CHECK (organization_id = current_org_id());
