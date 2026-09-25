#!/bin/sh
# Lesson 7.4: a logical backup of Beacon's database.
#
#   DATABASE_URL=postgres://… BACKUP_DIR=./backups sh scripts/backup.sh
#   docker compose -f docker-compose.prod.yml --profile backup run --rm backup
#
# pg_dump's custom format (-Fc): compressed, and pg_restore can restore it in
# parallel or pick single tables. One file per run, named by UTC time, plus a
# .sha256 so a restore can prove the file is the one that was written. Files
# older than BACKUP_KEEP_DAYS are deleted.
#
# This is the "nightly dump" level of backup (RPO: up to a day). A managed
# Postgres with point-in-time recovery (continuous WAL archiving) gets RPO down
# to minutes; use it in production, and keep this as the portable, self-hosted
# and restore-drill copy. Copy the files to ANOTHER account/region (object
# storage with a retention lock): a backup next to the database dies with it.
set -eu

: "${DATABASE_URL:?set DATABASE_URL}"
BACKUP_DIR="${BACKUP_DIR:-./backups}"
BACKUP_KEEP_DAYS="${BACKUP_KEEP_DAYS:-14}"
mkdir -p "$BACKUP_DIR"

stamp=$(date -u +%Y%m%dT%H%M%SZ)
file="$BACKUP_DIR/beacon-$stamp.dump"
started=$(date +%s)

# --no-owner/--no-privileges: restorable into a database with different role names.
pg_dump --format=custom --compress=6 --no-owner --no-privileges --file="$file.partial" "$DATABASE_URL"
mv "$file.partial" "$file" # only complete dumps get the final name
(cd "$BACKUP_DIR" && sha256sum "$(basename "$file")" > "$(basename "$file").sha256")

size=$(wc -c < "$file")
echo "{\"msg\":\"backup.completed\",\"file\":\"$file\",\"bytes\":$size,\"seconds\":$(( $(date +%s) - started ))}"

# Retention: the newest backups stay; old ones go (monitor that a fresh one exists, docs/backup-and-restore.md).
find "$BACKUP_DIR" -name 'beacon-*.dump*' -type f -mtime "+$BACKUP_KEEP_DAYS" -print -delete
