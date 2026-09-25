# Secrets

Lesson 8.1. A secret is any credential: the database URL, `BETTER_AUTH_SECRET`, Stripe and Resend keys, the
encryption keyring, `ANTHROPIC_API_KEY`. Beacon's rules:

1. **Never in git.** `.env.local` and `.env` are git-ignored; `.env.example` holds placeholders only. gitleaks
   runs before every commit (`npm run hooks:install`, then `.githooks/pre-commit`) and over the whole history in
   CI (the `secrets` job). Rules and the short allow-list are in `.gitleaks.toml`.
2. **Injected at runtime** from a secrets manager, never baked into the image (the Dockerfile copies no `.env`,
   and CI checks it, lesson 7.4).
3. **Checked at startup** by `src/lib/env.ts`: production refuses to start without `BETTER_AUTH_SECRET` and
   `ENCRYPTION_KEYS`.
4. **Rotated, not deleted**, when one leaks.

## A secrets manager: Infisical

Any manager works (a cloud secrets manager, OpenBao, Doppler, SOPS-encrypted files). With
[Infisical](https://infisical.com/docs), cloud or self-hosted:

```bash
infisical login
infisical init                                  # link this folder to the Beacon project
infisical secrets set BETTER_AUTH_SECRET="$(openssl rand -base64 32)" --env=dev
infisical secrets set ENCRYPTION_KEYS="k1:$(openssl rand -base64 32)" --env=dev
infisical run --env=dev -- npm run dev          # the app sees them as environment variables
infisical run --env=dev -- npm run worker
```

No `.env.local` on the laptop at all. In production the platform injects the same variables: an Infisical
machine identity in the deploy job, or the Kubernetes operator, or your PaaS's secret settings. CI uses its own
store (`secrets.*` in GitHub Actions) and only for what CI needs: CI can deploy, so treat it as production.

## When a secret leaks

It was committed, pasted in a ticket, printed in a log. In this order:

1. **Rotate** it at the provider (Stripe: roll the key; GitHub: regenerate the client secret; the database: change
   the password). Assume it was copied the moment it leaked; a force-push does not un-clone it.
2. Deploy the new value through the secrets manager.
3. Look for use of the old one in the provider's logs.
4. Only then clean up: remove it from the code, and allow-list the old commit in `.gitleaks.toml` so CI is green again.
5. If customer data may have been exposed, the incident process starts its 72-hour GDPR clock (lesson 8.1).

## Secrets Beacon stores for customers

Some secrets are customer data, stored in Postgres, and Beacon must read them back:

| Secret | Stored as | Lesson |
|---|---|---|
| API keys | SHA-256 hash only (verify, never read back) | 5.2 |
| Webhook signing secrets | envelope-encrypted: `webhook_endpoints.secret_encrypted` | 5.3, 8.1 |
| Slack incoming-webhook URLs | envelope-encrypted: `organizations.slack_webhook_url_encrypted` | 4.2, 8.1 |
| GitHub OAuth tokens (sign in with GitHub) | encrypted by Better Auth (`encryptOAuthTokens`) with `BETTER_AUTH_SECRET` | 1.1, 8.1 |
| Passwords | argon2id hashes | 1.1 |

### Envelope encryption

`src/lib/secrets/`: each value gets its own random data key (DEK); the DEK encrypts the value with AES-256-GCM,
and the key-encryption key (KEK) from the KMS encrypts ("wraps") the DEK. The column holds one string:

```
enc:v1:<kek id>:<wrapped DEK>:<iv>:<ciphertext + tag>
```

A database dump, a backup or a read-only SQL login shows only that. The ciphertext is also bound to its
organization and column (AES-GCM additional data), so copying org A's secret into org B's row does not decrypt.

The KMS is an interface (`src/lib/secrets/kms.ts`). The `local` driver keeps the KEKs in `ENCRYPTION_KEYS`, a
keyring: `k2:<base64 32 bytes>,k1:<base64 32 bytes>`, the FIRST one encrypts new values, all of them decrypt. In
production, a cloud KMS (AWS KMS, Google Cloud KMS) or OpenBao's transit engine implements the same two
methods, `wrapKey` and `unwrapKey`, and the KEK never leaves it.

### Rotating the encryption key

No downtime, no re-encryption of the data, only the small wrapped DEKs change:

```bash
# 1. Add a new key IN FRONT (it becomes the current one); keep the old one so existing values still decrypt.
ENCRYPTION_KEYS="k2:$(openssl rand -base64 32),k1:<the old key>"   # in the secrets manager; restart app and worker
# 2. Re-wrap every stored DEK with k2 (idempotent; safe to run while the app serves traffic).
npm run secrets -- rotate
npm run secrets -- status        # every value on k2?
# 3. Remove k1 from ENCRYPTION_KEYS and restart.
```

Both steps are audited (`secrets.rewrapped`, a platform event in `/internal/audit`). Without `ENCRYPTION_KEYS`,
development and tests use a fixed, public development key (and say so in the log); production refuses to start.

### Upgrading from Module 7

Module 7 stored webhook secrets and Slack URLs in plain text. `npm run db:migrate` adds the encrypted columns
(migration 0025), then encrypts every plaintext value and empties the old column, in the same run. It is
idempotent. The old columns stay (empty) until a later "contract" migration drops them (expand → migrate →
contract, docs/deployment.md). During the deploy, an old worker that picks up a webhook finds no plaintext
secret, fails the attempt, and the queue retries it with the new code.
