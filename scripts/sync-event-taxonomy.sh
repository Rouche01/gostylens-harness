#!/usr/bin/env bash
# Extract PostHog event names from the stylens app repo.
# Usage: ./scripts/sync-event-taxonomy.sh [path-to-stylens]
set -euo pipefail

STYLENS_DIR="${1:-../stylens}"
OUTPUT="context/analytics-events.md"

if [[ ! -d "$STYLENS_DIR/lib" ]]; then
  echo "Error: stylens repo not found at $STYLENS_DIR"
  echo "Clone stylens as a sibling: ../stylens"
  exit 1
fi

echo "Scanning $STYLENS_DIR/lib for capture() event names..."

EVENTS=$(rg -o "capture\(\s*['\"]([a-z_]+)['\"]" "$STYLENS_DIR/lib" -r '$1' | sort -u)

echo "Found events:"
echo "$EVENTS"
echo ""
echo "Update $OUTPUT manually or extend this script to regenerate the full taxonomy file."
