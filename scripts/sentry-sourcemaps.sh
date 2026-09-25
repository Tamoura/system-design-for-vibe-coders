#!/bin/sh
# Lesson 7.2: "no source maps, no release tag" is a junior mistake. Run in the
# Docker build after `next build` (with SOURCE_MAPS=1):
#   with the sentry_auth_token build secret: inject debug ids, upload the maps
#   for release $NEXT_PUBLIC_APP_RELEASE (the git SHA); then, always, delete
#   them so the image never serves them to browsers.
set -eu
token_file=/run/secrets/sentry_auth_token
if [ -s "$token_file" ] && [ -n "${SENTRY_ORG:-}" ] && [ -n "${SENTRY_PROJECT:-}" ]; then
  SENTRY_AUTH_TOKEN=$(cat "$token_file")
  export SENTRY_AUTH_TOKEN
  npx --yes @sentry/cli sourcemaps inject .next/static
  npx --yes @sentry/cli sourcemaps upload --release "${NEXT_PUBLIC_APP_RELEASE:-unknown}" .next/static
  echo "source maps uploaded to Sentry for release ${NEXT_PUBLIC_APP_RELEASE:-unknown}"
else
  echo "no Sentry build secret: source maps not uploaded"
fi
find .next -name '*.map' -type f -delete
