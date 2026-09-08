#!/usr/bin/env bash
# Pull Meta Ads Insights for the GoStylens ad account.
# Usage:
#   ./scripts/meta-ads-insights.sh
#   ./scripts/meta-ads-insights.sh last_7d
#   ./scripts/meta-ads-insights.sh last_7d campaign
# Requires META_ACCESS_TOKEN + META_AD_ACCOUNT_ID in .env
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

TOKEN="${META_ACCESS_TOKEN:-}"
ACCOUNT_RAW="${META_AD_ACCOUNT_ID:-}"
VERSION="${META_GRAPH_VERSION:-v22.0}"
DATE_PRESET="${1:-last_7d}"
LEVEL="${2:-campaign}"

if [[ -z "$TOKEN" || -z "$ACCOUNT_RAW" ]]; then
  echo "Missing META_ACCESS_TOKEN or META_AD_ACCOUNT_ID in .env"
  echo "Copy keys from .env.example, then re-run."
  exit 1
fi

# Normalize act_ prefix
if [[ "$ACCOUNT_RAW" == act_* ]]; then
  ACCOUNT_ID="$ACCOUNT_RAW"
else
  ACCOUNT_ID="act_${ACCOUNT_RAW}"
fi

FIELDS="campaign_name,adset_name,ad_name,spend,impressions,reach,clicks,cpc,ctr,actions,inline_link_clicks,cost_per_inline_link_click"
OUT_DIR="outputs"
mkdir -p "$OUT_DIR"
STAMP="$(date -u +%Y-%m-%d)"
OUT_FILE="${OUT_DIR}/${STAMP}-meta-ads-insights-${LEVEL}-${DATE_PRESET}.json"

URL="https://graph.facebook.com/${VERSION}/${ACCOUNT_ID}/insights"

echo "Fetching ${LEVEL} insights (${DATE_PRESET}) for ${ACCOUNT_ID}..."
HTTP_CODE=$(curl -sS -o "$OUT_FILE" -w "%{http_code}" -G "$URL" \
  --data-urlencode "level=${LEVEL}" \
  --data-urlencode "date_preset=${DATE_PRESET}" \
  --data-urlencode "fields=${FIELDS}" \
  --data-urlencode "access_token=${TOKEN}")

if [[ "$HTTP_CODE" != "200" ]]; then
  echo "Meta API error (HTTP ${HTTP_CODE}):"
  cat "$OUT_FILE"
  echo
  exit 1
fi

echo "Wrote $OUT_FILE"
if command -v python3 >/dev/null 2>&1; then
  python3 - "$OUT_FILE" <<'PY'
import json, sys
path = sys.argv[1]
data = json.load(open(path))
rows = data.get("data") or []
if not rows:
    print("No rows (campaign may be new, paused, or outside date range).")
    err = data.get("error")
    if err:
        print(err)
    sys.exit(0)
print(f"{'name':<48} {'spend':>8} {'impr':>8} {'clicks':>7} {'cpc':>7} {'ctr':>7}")
for r in rows:
    name = r.get("campaign_name") or r.get("adset_name") or r.get("ad_name") or "(row)"
    print(f"{name[:48]:<48} {r.get('spend','—'):>8} {r.get('impressions','—'):>8} {r.get('clicks','—'):>7} {r.get('cpc','—'):>7} {r.get('ctr','—'):>7}")
PY
fi
