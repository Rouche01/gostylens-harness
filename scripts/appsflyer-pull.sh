#!/usr/bin/env bash
# Pull AppsFlyer raw installs / in-app events (Pull API v5, V2 bearer token).
# Usage:
#   ./scripts/appsflyer-pull.sh
#   ./scripts/appsflyer-pull.sh 2026-10-06 2026-10-12
#   ./scripts/appsflyer-pull.sh 2026-10-06 2026-10-12 installs
#   ./scripts/appsflyer-pull.sh 2026-10-06 2026-10-12 events
#   ./scripts/appsflyer-pull.sh 2026-10-06 2026-10-12 both facebook
#
# Reports: installs | events | both (default)
# Optional 4th arg / APPSFLYER_MEDIA_SOURCE: facebook | (omit = all non-organic)
#
# Requires in .env:
#   APPSFLYER_API_TOKEN   — Admin API V2 token (Bearer)
#   APPSFLYER_APP_ID      — iOS Pull API id, e.g. id6760427902
#
# Docs: https://dev.appsflyer.com/hc/reference/raw_data_pull_api_tokenv2-overview
# Token: AppsFlyer → Security center → API tokens (V2). Admin only.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

TOKEN="${APPSFLYER_API_TOKEN:-}"
APP_RAW="${APPSFLYER_APP_ID:-}"
FROM="${1:-}"
TO="${2:-}"
REPORT="${3:-both}"
MEDIA="${4:-${APPSFLYER_MEDIA_SOURCE:-}}"
EVENTS="${APPSFLYER_EVENT_NAMES:-af_complete_registration,af_activation}"
BASE="https://hq1.appsflyer.com/api/raw-data/export/app"

if [[ -z "$TOKEN" || -z "$APP_RAW" ]]; then
  echo "Missing APPSFLYER_API_TOKEN or APPSFLYER_APP_ID in .env"
  echo "1. AppsFlyer → Security center → API tokens → create/copy V2 token (admin)"
  echo "2. Set APPSFLYER_APP_ID=id6760427902  (iOS Pull API form: id + Apple ID)"
  echo "See context/integrations.md → AppsFlyer"
  exit 1
fi

# Normalize iOS app id: accept 6760427902 or id6760427902
if [[ "$APP_RAW" == id* ]]; then
  APP_ID="$APP_RAW"
else
  APP_ID="id${APP_RAW}"
fi

if [[ -z "$FROM" || -z "$TO" ]]; then
  # Default: last 7 days UTC through today
  if date -u -v-6d +%Y-%m-%d >/dev/null 2>&1; then
    FROM="$(date -u -v-6d +%Y-%m-%d)"
  else
    FROM="$(date -u -d '6 days ago' +%Y-%m-%d)"
  fi
  TO="$(date -u +%Y-%m-%d)"
fi

OUT_DIR="outputs"
mkdir -p "$OUT_DIR"
STAMP="$(date -u +%Y-%m-%d)"

pull_report() {
  local kind="$1"   # installs | events
  local path_suffix
  local out_file
  local url
  local http
  local tmp

  case "$kind" in
    installs)
      path_suffix="installs_report/v5"
      out_file="${OUT_DIR}/${STAMP}-appsflyer-installs-${FROM}_to_${TO}.csv"
      ;;
    events)
      path_suffix="in_app_events_report/v5"
      out_file="${OUT_DIR}/${STAMP}-appsflyer-events-${FROM}_to_${TO}.csv"
      ;;
    *)
      echo "Unknown report kind: $kind"
      exit 1
      ;;
  esac

  url="${BASE}/${APP_ID}/${path_suffix}"
  tmp="$(mktemp)"

  echo "Fetching AppsFlyer ${kind} (${FROM} → ${TO}) for ${APP_ID}..."

  # Build curl args
  # HQ returns 302 → rawdata.appsflyer.com; follow redirects (-L).
  local -a curl_args=(
    -sS -L -G "$url"
    -H "Authorization: Bearer ${TOKEN}"
    -H "Accept: text/csv"
    --data-urlencode "from=${FROM}"
    --data-urlencode "to=${TO}"
  )

  if [[ -n "$MEDIA" ]]; then
    # Meta/Facebook: category=facebook & media_source=facebook
    if [[ "$MEDIA" == "facebook" || "$MEDIA" == "meta" || "$MEDIA" == "Facebook Ads" ]]; then
      curl_args+=(--data-urlencode "category=facebook" --data-urlencode "media_source=facebook")
      echo "  filter: Facebook / Meta"
    else
      curl_args+=(--data-urlencode "category=standard" --data-urlencode "media_source=${MEDIA}")
      echo "  filter: media_source=${MEDIA}"
    fi
  fi

  if [[ "$kind" == "events" && -n "$EVENTS" ]]; then
    curl_args+=(--data-urlencode "event_name=${EVENTS}")
    echo "  events: ${EVENTS}"
  fi

  http=$(curl "${curl_args[@]}" -o "$tmp" -w "%{http_code}")

  if [[ "$http" != "200" ]]; then
    echo "AppsFlyer API error (HTTP ${http}):"
    head -c 2000 "$tmp"
    echo
    rm -f "$tmp"
    exit 1
  fi

  # Empty / no data often returns empty body or a short message
  if [[ ! -s "$tmp" ]]; then
    echo "No rows returned for ${kind}."
    rm -f "$tmp"
    return 0
  fi

  mv "$tmp" "$out_file"
  echo "Wrote $out_file"

  if command -v python3 >/dev/null 2>&1; then
    python3 - "$out_file" "$kind" <<'PY'
import csv, sys
from collections import Counter

path, kind = sys.argv[1], sys.argv[2]
with open(path, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

if not rows:
    print("CSV has header only (0 data rows).")
    sys.exit(0)

print(f"Rows: {len(rows)}")

def col(row, *names):
    for n in names:
        if n in row and row[n] not in (None, ""):
            return row[n]
    return ""

if kind == "installs":
    by_source = Counter(col(r, "Media Source", "media_source") or "(unknown)" for r in rows)
    by_geo = Counter(col(r, "Country Code", "country_code") or "?" for r in rows)
    print("Installs by media source:")
    for k, v in by_source.most_common(10):
        print(f"  {k}: {v}")
    print("Installs by country (top):")
    for k, v in by_geo.most_common(8):
        print(f"  {k}: {v}")
else:
    by_event = Counter(col(r, "Event Name", "event_name") or "(unknown)" for r in rows)
    by_source = Counter(col(r, "Media Source", "media_source") or "(unknown)" for r in rows)
    print("Events by name:")
    for k, v in by_event.most_common(15):
        print(f"  {k}: {v}")
    print("Events by media source:")
    for k, v in by_source.most_common(10):
        print(f"  {k}: {v}")
PY
  fi
}

case "$REPORT" in
  installs)
    pull_report installs
    ;;
  events)
    pull_report events
    ;;
  both)
    pull_report installs
    pull_report events
    ;;
  *)
    echo "Usage: $0 [from YYYY-MM-DD] [to YYYY-MM-DD] [installs|events|both] [facebook]"
    exit 1
    ;;
esac
