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
FILES=(index.html on-ramp-poster.html learning-path.html production-playbook.html assessment.html)

if [ ! -d "$AGENTIC_DOCS" ]; then
  echo "error: AGENTIC_DOCS directory not found: $AGENTIC_DOCS" >&2
  echo "Point AGENTIC_DOCS at AI-agents/qdb-agent-framework/docs (run 'npm run docs:html' there first)." >&2
  exit 1
fi

mkdir -p agentic
for f in "${FILES[@]}"; do
  if [ ! -f "$AGENTIC_DOCS/$f" ]; then
    echo "warning: missing $AGENTIC_DOCS/$f — skipped" >&2
    continue
  fi
  cp "$AGENTIC_DOCS/$f" "agentic/$f"
  echo "synced agentic/$f"
done
# The copied pages have no site navigation of their own; add it (top bar, module-level
# contents, mobile drawer). Idempotent, so it is safe to run after every sync.
node "$(dirname "$0")/agentic-nav.mjs"
echo "Done. Review 'git diff agentic/', then commit and push to publish the library."
