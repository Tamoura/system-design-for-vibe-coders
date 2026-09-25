# Backups and the restore drill

Lesson 7.4: "a backup you have never restored is a hope, not a backup."

## What is backed up, how

| Level | How | RPO (data you can lose) | Use it for |
|---|---|---|---|
| Point-in-time recovery | your managed Postgres (continuous WAL archiving) | minutes or less | production |
| Nightly logical dump | `scripts/backup.sh` (`pg_dump -Fc`, a `.sha256` next to each file, old files pruned after `BACKUP_KEEP_DAYS`) | up to a day | self-hosting, restore drills, a copy that does not depend on your provider |
| Uploaded files | the object store's versioning and replication (`STORAGE_DRIVER=s3`), or the `storage` volume | — | logos, screenshots |

Rules: backups live in **another account and region** than the database (a compromised credential or a regional
outage must not take both); alert when the newest backup is older than expected (a missing file is how backups fail
silently); back up what is not in the database too (object storage, secrets, the infrastructure-as-code state).

```bash
DATABASE_URL=postgres://… BACKUP_DIR=./backups sh scripts/backup.sh
docker compose -f docker-compose.prod.yml --profile backup run --rm backup   # the same, in the Compose install
```

## Restore

Into a **new, empty** database, never over the old one:

```bash
createdb beacon_restore
sh scripts/restore.sh backups/beacon-20260925T021159Z.dump postgres://…/beacon_restore
DATABASE_URL=postgres://…/beacon_restore npm run db:migrate     # installs the queue grants again; applies nothing else
DATABASE_URL=postgres://…/beacon_restore npm run audit -- verify
# point the app (DATABASE_URL) at it, check /api/ready, sign in
```

`restore.sh` checks the file's checksum, refuses a database that already has tables, recreates the `beacon_app` role
if the server lacks it, restores with `pg_restore --no-owner --no-privileges` (so it works on a server with other role
names), then grants the app role its privileges again, and prints the newest check result and audit event it found.

## The drill, as run for this branch

A drill on the smoke-test database (Postgres 16, local; 0.2 MB dump: small, so the numbers show the steps, not what a
big database costs; time yours):

| Step | Time |
|---|---|
| `scripts/backup.sh` | 0.2 s |
| `scripts/restore.sh` into a new database | 0.3 s |
| `npm run db:migrate` + `npm run audit -- verify` (2 chains, 7 events intact) | 2.5 s |
| `next start` against the restored database until `/api/ready` = 200 | 1.4 s |

- **RPO**: the newest check result in the restored database was 2026-09-25 02:10:38 UTC for a dump taken at
  02:11:59: nothing written after the dump survives. With nightly dumps that is up to 24 hours; with PITR, minutes.
- **RTO**: under 5 seconds of machine time here. In a real incident the human steps dominate (noticing, deciding to
  restore, finding the credentials, changing `DATABASE_URL` everywhere): write them down and time them too.
- **What went wrong**: a plain `pg_restore --no-privileges` produced a database where every tenant query failed with
  `permission denied for table monitors`: the grants to `beacon_app` (migrations 0007 and 0024) are privileges, which
  the dump left out, and the migrations do not run again on a restored database. **Fix**: `restore.sh` grants them
  again (and keeps the audit log append-only). A second catch: `ALTER DEFAULT PRIVILEGES` belongs to the server, not the
  database, so a table created later on the new server would not get them; the next migration run fixes grants for the
  queue only, so check that list after a real DR.
- Verified after the restore: sign-in, `GET /api/orgs/demo/monitors` 200, the audit log API returned the restored
  events, `/api/ready` 200.

Repeat the drill every quarter, and after any change to the schema's grants or roles.
