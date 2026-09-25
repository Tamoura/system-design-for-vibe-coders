-- Lesson 8.1 (🟡): secrets Beacon stores for customers are encrypted by the application
-- (envelope encryption, src/lib/secrets). EXPAND step of expand/contract (docs/deployment.md):
-- new columns for the ciphertext; the plaintext columns become nullable. SQL cannot encrypt
-- (the key is not in the database, on purpose), so `npm run db:migrate` runs
-- encryptLegacySecrets() right after this file: it fills the new columns and empties the old ones.
-- A later migration drops the old columns (CONTRACT).
ALTER TABLE "webhook_endpoints" ALTER COLUMN "secret" DROP NOT NULL;--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "slack_webhook_url_encrypted" text;--> statement-breakpoint
ALTER TABLE "webhook_endpoints" ADD COLUMN "secret_encrypted" text;
