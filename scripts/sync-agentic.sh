#!/usr/bin/env bash
# Sync the agentic course into this library's /agentic/ folder.
#
# The agentic course's CANONICAL source is the separate AI-agents repo
# (qdb-agent-framework/docs). This library only hosts a published COPY under
# /agentic/. Run this after updating the agentic curriculum so the published
# site stays current.
#
# Usage:
#   1. In the AI-agents repo:  cd qdb-agent-framework && npm run docs:html
#   2. Here:  AGENTIC_DOCS=/path/to/AI-agents/qdb-agent-framework/docs ./scripts/sync-agentic.sh
#      (AGENTIC_DOCS defaults to a sibling checkout: ../AI-agents/qdb-agent-framework/docs)
#   3. Review `git diff agentic/`, then commit and push to publish.
set -euo pipefail
AGENTIC_DOCS="${AGENTIC_DOCS:-../AI-agents/qdb-agent-framework/docs}"
FILES=(index.html on-ramp-poster.html learning-path.html production-playbook.html assessment.html
       index.ar.html on-ramp-poster.ar.html learning-path.ar.html production-playbook.ar.html assessment.ar.html)

if [ ! -d "$AGENTIC_DOCS" ]; then
  echo "error: AGENTIC_DOCS directory not found: $AGENTIC_DOCS" >&2
  echo "Point AGENTIC_DOCS at AI-agents/qdb-agent-framework/docs (run 'npm run docs:html' there first)." >&2
  exit 1
fi

# Text that must not be published here. These pages carry a real organisation's name, and an earlier
# version listed that organisation's regulatory mapping and its control gaps. That content was removed from
# this copy; if it comes back from the source, the sync stops and the previous pages are put back.
BLOCKED=(
  "Regulatory mapping for QDB"
  "regulatory-mapping-for-qdb"
  "remain gaps"
  "Gap in current framework"
  "largest current gap"
  "largest gap between the current framework"
  "biggest real gap"
  "current framework gap"
  "المواءمة التنظيمية (regulatory mapping) لبنك قطر للتنمية"
  "لا تزال عدة ضوابط (controls) فجوات"
  "فجوة في الإطار (framework) الحالي"
  "أكبر فجوة حالية"
  "أكبر فجوة بين الإطار (framework) الحالي"
  "أكبر فجوة حقيقية في الإطار"
  "الفجوة (gap) الحالية في الإطار"
)

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
# The copied pages have no site navigation of their own; add it (top bar, module-level
# contents, mobile drawer). Idempotent, so it is safe to run after every sync.
node "$(dirname "$0")/agentic-nav.mjs"
echo "Done. Review 'git diff agentic/', then commit and push to publish the library."
