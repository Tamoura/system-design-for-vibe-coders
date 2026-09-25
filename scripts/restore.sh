#!/bin/sh
# Lesson 7.4: restore a backup made by scripts/backup.sh into a SCRATCH
# database, for a restore drill (docs/backup-and-restore.md) or a real recovery.
#
#   sh scripts/restore.sh backups/beacon-20260925T020000Z.dump postgres://beacon@localhost:5432/beacon_restore
#
# It refuses a target database that already has tables (restore into a new,
# empty database, then point the app at it), checks the file's checksum, and
# prints how long it took: that number is your RTO's biggest part.
set -eu

file="${1:?usage: restore.sh <backup.dump> <target DATABASE_URL>}"
target="${2:?usage: restore.sh <backup.dump> <target DATABASE_URL>}"

if [ -f "$file.sha256" ]; then
  (cd "$(dirname "$file")" && sha256sum -c "$(basename "$file").sha256" >/dev/null) || { echo "✗ checksum mismatch: $file is not the file that was backed up" >&2; exit 1; }
fi

tables=$(psql "$target" -Atc "select count(*) from information_schema.tables where table_schema in ('public','pgboss')")
if [ "$tables" != "0" ]; then
  echo "✗ the target database already has $tables tables. Restore into a new, empty database." >&2
  exit 1
fi

started=$(date +%s)
# The app's role for row-level security (migration 0007) belongs to the server, not to the dump.
psql "$target" -v ON_ERROR_STOP=1 -qc "do \$\$ begin if not exists (select from pg_roles where rolname = 'beacon_app') then create role beacon_app nologin; end if; end \$\$; grant beacon_app to current_user;"
pg_restore --no-owner --no-privileges --exit-on-error --jobs=4 --dbname="$target" "$file"
# Grants were not in the dump (--no-privileges): give them back, as migration 0007/0024 did.
psql "$target" -v ON_ERROR_STOP=1 -q <<'SQL'
grant usage on schema public to beacon_app;
grant select, insert, update, delete on all tables in schema public to beacon_app;
revoke update, delete, truncate on audit_events from beacon_app;
revoke all on staff_users, impersonation_sessions from beacon_app;
SQL
seconds=$(( $(date +%s) - started ))

events=$(psql "$target" -Atc "select coalesce(max(occurred_at)::text, 'none') from audit_events")
checks=$(psql "$target" -Atc "select coalesce(max(checked_at)::text, 'none') from check_results")
echo "✓ restored $file in ${seconds}s"
echo "  newest check result: $checks   newest audit event: $events   (the gap to 'now' at the time of failure is your RPO)"
echo "  next: DATABASE_URL=$target npm run db:migrate && npm run audit -- verify && start the app against it"
