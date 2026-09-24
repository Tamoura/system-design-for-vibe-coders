CREATE TABLE "presence" (
	"organization_id" uuid NOT NULL,
	"topic" text NOT NULL,
	"user_id" uuid NOT NULL,
	"last_seen_at" timestamp with time zone DEFAULT now() NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "presence_organization_id_topic_user_id_pk" PRIMARY KEY("organization_id","topic","user_id")
);
--> statement-breakpoint
ALTER TABLE "presence" ADD CONSTRAINT "presence_organization_id_organizations_id_fk" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "presence" ADD CONSTRAINT "presence_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
-- Lesson 2.4, added by hand: presence is tenant data like the rest (0007).
ALTER TABLE "presence" ENABLE ROW LEVEL SECURITY;--> statement-breakpoint
CREATE POLICY tenant_isolation ON "presence"
  USING (organization_id = current_org_id())
  WITH CHECK (organization_id = current_org_id());
