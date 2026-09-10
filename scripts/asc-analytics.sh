#!/usr/bin/env bash
# Pull App Store Connect Analytics (App Store engagement / product page metrics).
# Usage:
#   ./scripts/asc-analytics.sh
#   ./scripts/asc-analytics.sh --list-apps
#   ./scripts/asc-analytics.sh --days 14
# Requires APPLE_ASC_ISSUER_ID, APPLE_ASC_KEY_ID, APPLE_ASC_PRIVATE_KEY_PATH in .env
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PY="${ROOT}/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "Missing .venv — run: python3 -m venv .venv && .venv/bin/pip install PyJWT cryptography"
  exit 1
fi

exec "$PY" "${ROOT}/scripts/asc_analytics.py" "$@"
