CREATE TABLE "api_idempotency_keys" (
	"organization_id" uuid NOT NULL,
	"key" text NOT NULL,
	"request_method" text NOT NULL,
	"request_path" text NOT NULL,
	"request_hash" text NOT NULL,
	"status_code" integer,
	"response_body" text,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "api_idempotency_keys_organization_id_key_pk" PRIMARY KEY("organization_id","key")
);
--> statement-breakpoint
CREATE TABLE "api_keys" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"organization_id" uuid NOT NULL,
	"name" text NOT NULL,
	"key_hash" text NOT NULL,
	"key_start" text NOT NULL,
	"key_last4" text NOT NULL,
	"scopes" text[] NOT NULL,
	"created_by" uuid,
	"last_used_at" timestamp with time zone,
	"revoked_at" timestamp with time zone,
	"revoked_by" uuid,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "api_keys_key_hash_unique" UNIQUE("key_hash")
);
--> statement-breakpoint
CREATE TABLE "rate_limit_buckets" (
	"key" text PRIMARY KEY NOT NULL,
	"tokens" double precision NOT NULL,
	"updated_at" timestamp with time zone NOT NULL
);
--> statement-breakpoint
ALTER TABLE "api_idempotency_keys" ADD CONSTRAINT "api_idempotency_keys_organization_id_organizations_id_fk" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "api_keys" ADD CONSTRAINT "api_keys_organization_id_organizations_id_fk" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "api_keys" ADD CONSTRAINT "api_keys_created_by_users_id_fk" FOREIGN KEY ("created_by") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "api_keys" ADD CONSTRAINT "api_keys_revoked_by_users_id_fk" FOREIGN KEY ("revoked_by") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "api_keys_org_idx" ON "api_keys" USING btree ("organization_id","created_at");--> statement-breakpoint
CREATE INDEX "incidents_org_created_idx" ON "incidents" USING btree ("organization_id","created_at","id");--> statement-breakpoint
-- Lesson 2.4, added by hand: stored API responses are tenant data. api_keys is
-- deliberately NOT under row-level security: the key is how a request finds
-- its org (see src/db/schema.ts), like memberships at login.
ALTER TABLE "api_idempotency_keys" ENABLE ROW LEVEL SECURITY;--> statement-breakpoint
CREATE POLICY tenant_isolation ON "api_idempotency_keys"
  USING (organization_id = current_org_id())
  WITH CHECK (organization_id = current_org_id());
