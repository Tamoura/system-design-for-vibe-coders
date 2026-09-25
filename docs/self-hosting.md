# Self-hosting Beacon

Lesson 7.4 (🔴 in the course; the essentials are here because `docker-compose.prod.yml` is also the production shape).
Run Beacon on one machine with Docker. No Stripe, email provider or analytics account is needed: without billing,
every organization is on the Free plan; without an email provider, emails are printed in the logs.

(Written against the Compose file and image of this branch. The course sandbox has no Docker daemon, so this exact
sequence was not run there; its pieces were: the image's runtime layout, the bundled worker and migrations, the seed
and staff scripts, and the backup/restore scripts.)

## Install

```bash
git clone -b beacon/module-8-solution --single-branch https://github.com/Tamoura/system-design-for-vibe-coders.git beacon
cd beacon
cat > .env <<EOF
BETTER_AUTH_SECRET=$(openssl rand -base64 32)
ENCRYPTION_KEYS=k1:$(openssl rand -base64 32)
POSTGRES_PASSWORD=$(openssl rand -hex 16)
APP_URL=http://localhost:3000
EOF
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
```

Open <http://localhost:3000> and sign up. Order of start-up: Postgres → `migrate` (runs the migrations, then exits) →
`web` and `worker`. `docker compose -f docker-compose.prod.yml logs -f web worker` shows JSON logs.

Optional demo data and staff accounts (password `beacon-demo-password`; never on a public server):
`docker compose -f docker-compose.prod.yml --profile demo up seed`.

Make yourself staff (the admin panel at `/internal`), after signing up and verifying your email:

```bash
docker compose -f docker-compose.prod.yml run --rm web node dist/scripts/staff.mjs add you@example.com superadmin "installed Beacon"
```

## Configure

Every variable, its default and whether it is required: [configuration.md](configuration.md). The usual ones:

| Want | Set |
|---|---|
| real email | `SMTP_URL=smtp://user:pass@smtp.example.com:587` (or `RESEND_API_KEY`), `EMAIL_DRIVER=smtp`, `EMAIL_FROM` |
| HTTPS | put a reverse proxy (Caddy, Traefik, nginx) in front of port 3000, and `APP_URL=https://…` (cookies become Secure) |
| files in S3/R2/MinIO | `STORAGE_DRIVER=s3` and the `S3_*` variables |
| paid plans | `STRIPE_*` (see docs/SOLUTIONS.md, Module 3) |
| errors, traces | `SENTRY_DSN`; `OTEL_EXPORTER_OTLP_ENDPOINT` and `docker-compose.observability.yml` |
| more workers | `docker compose -f docker-compose.prod.yml up -d --scale worker=3` |

## Upgrade

```bash
git pull
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d      # migrate runs first; web and worker restart after it
```

Migrations are safe to run again and are applied in order, so skipping versions works: a release's migrations never
assume the code of a release you did not install.

## Back up

`docker compose -f docker-compose.prod.yml --profile backup run --rm backup` writes a dump to `./backups`. Schedule it
(cron), copy the files off the machine, and practise a restore: [backup-and-restore.md](backup-and-restore.md).

Not built (the rest of the 🔴 exercise): license keys that unlock paid features offline, a Helm chart.
