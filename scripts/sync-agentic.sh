#!/usr/bin/env bash
# Sync the agentic course into this library's /agentic/ folder.
#
# The agentic course's CANONICAL source is the separate AI-agents repo
# (its framework folder, docs/). This library only hosts a published COPY under
# /agentic/. Run this after updating the agentic curriculum so the published
# site stays current.
#
# After the copy and the BLOCKED-text guard, two scripts run on the copied pages, in this order:
#   1. scripts/agentic-neutral.mjs  removes the name of the real organisation the pages were written
#                                   for (explicit rules, English and Arabic; fails if any mention is left)
#   2. scripts/agentic-nav.mjs      adds the site navigation
#
# Usage:
#   1. In the source repository, build the agentic pages (npm run docs:html in its framework folder).
#   2. Here:  AGENTIC_DOCS=/path/to/the/built/docs ./scripts/sync-agentic.sh
#      AGENTIC_DOCS is required; the source location is kept out of this public file on purpose.
#   3. Review `git diff agentic/`, then commit and push to publish.
#
# The text that must not be published (BLOCKED below) and the organisation-name rules are stored
# base64-encoded in scripts/blocked-text.b64 and read through scripts/blocked_text.py, so they do not
# appear here in plain text. That is obfuscation, not secrecy.
set -euo pipefail
if [ -z "${AGENTIC_DOCS:-}" ]; then
  echo "error: set AGENTIC_DOCS to the folder that holds the built agentic pages." >&2
  exit 1
fi
FILES=(index.html on-ramp-poster.html learning-path.html production-playbook.html assessment.html
       index.ar.html on-ramp-poster.ar.html learning-path.ar.html production-playbook.ar.html assessment.ar.html)

if [ ! -d "$AGENTIC_DOCS" ]; then
  echo "error: AGENTIC_DOCS directory not found: $AGENTIC_DOCS" >&2
  exit 1
fi

# Text that must not be published here: organisation-specific regulatory mapping and control-gap
# statements that an earlier version carried. If any comes back from the source, the sync stops and the
# previous pages are put back.
mapfile -t BLOCKED < <(python3 "$(dirname "$0")/blocked_text.py" --blocked)
if [ "${#BLOCKED[@]}" -eq 0 ]; then
  echo "error: could not read the blocked-text list (scripts/blocked-text.b64)." >&2
  exit 1
fi

mkdir -p agentic
BACKUP="$(mktemp -d)"
trap 'rm -rf "$BACKUP"' EXIT
SYNCED=()
for f in "${FILES[@]}"; do
  if [ ! -f "$AGENTIC_DOCS/$f" ]; then
    echo "warning: missing $AGENTIC_DOCS/$f — skipped" >&2
    continue
  fi
  if [ -f "agentic/$f" ]; then cp "agentic/$f" "$BACKUP/$f"; fi
  cp "$AGENTIC_DOCS/$f" "agentic/$f"
  SYNCED+=("$f")
  echo "synced agentic/$f"
done

# Guard: check every page just copied for the blocked text.
found=0
for f in ${SYNCED[@]+"${SYNCED[@]}"}; do
  for p in "${BLOCKED[@]}"; do
    if grep -qF -- "$p" "agentic/$f"; then
      echo "error: agentic/$f contains \"$p\"" >&2
      found=1
    fi
  done
done
if [ "$found" -ne 0 ]; then
  for f in "${SYNCED[@]}"; do
    if [ -f "$BACKUP/$f" ]; then cp "$BACKUP/$f" "agentic/$f"; else rm -f "agentic/$f"; fi
  done
  echo "error: the source pages still contain the regulatory mapping or control-gap statements listed above." >&2
  echo "       They must not be published here. Remove them in the source repository ($AGENTIC_DOCS) first," >&2
  echo "       rebuild there, then run this sync again. The previous agentic/ pages have been put back." >&2
  exit 1
fi
# Remove the real organisation's name from the copied pages (stops the sync if a mention is left).
node "$(dirname "$0")/agentic-neutral.mjs"
# The copied pages have no site navigation of their own; add it (top bar, module-level
# contents, mobile drawer). Idempotent, so it is safe to run after every sync.
node "$(dirname "$0")/agentic-nav.mjs"
echo "Done. Review 'git diff agentic/', then commit and push to publish the library."
