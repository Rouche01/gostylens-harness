#!/usr/bin/env python3
"""
App Store Connect Analytics — product page engagement pull.

Requires App Store Connect API key (Issuer ID, Key ID, .p8) with access
to App Analytics. Creates/reuses an ONGOING analytics report request, then
downloads APP_STORE_ENGAGEMENT report segments.

Usage:
  .venv/bin/python scripts/asc_analytics.py
  .venv/bin/python scripts/asc_analytics.py --list-apps
  .venv/bin/python scripts/asc_analytics.py --days 14

Env (.env):
  APPLE_ASC_ISSUER_ID
  APPLE_ASC_KEY_ID
  APPLE_ASC_PRIVATE_KEY_PATH   # path to AuthKey_XXXX.p8
  APPLE_ASC_APP_ID            # optional numeric Apple ID
  APPLE_ASC_BUNDLE_ID         # optional; used to resolve app if APP_ID unset
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import sys
import time
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import jwt
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.appstoreconnect.apple.com"


def load_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip("'").strip('"')
        os.environ.setdefault(k, v)


def make_token(issuer_id: str, key_id: str, private_key_pem: str) -> str:
    now = int(time.time())
    payload = {
        "iss": issuer_id,
        "iat": now,
        "exp": now + 20 * 60,
        "aud": "appstoreconnect-v1",
    }
    headers = {"alg": "ES256", "kid": key_id, "typ": "JWT"}
    return jwt.encode(payload, private_key_pem, algorithm="ES256", headers=headers)


def api_request(
    token: str,
    method: str,
    path: str,
    body: dict[str, Any] | None = None,
    query: dict[str, str] | None = None,
) -> dict[str, Any]:
    url = path if path.startswith("http") else f"{API}{path}"
    if query:
        url = f"{url}?{urllib.parse.urlencode(query, doseq=True)}"
    data = None
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read()
            if not raw:
                return {}
            return json.loads(raw.decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode(errors="replace")
        raise SystemExit(f"ASC API {method} {url} → HTTP {e.code}\n{err_body}") from e


def list_apps(token: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    path = "/v1/apps"
    query = {"limit": "200"}
    while path:
        payload = api_request(token, "GET", path, query=query)
        query = None
        out.extend(payload.get("data") or [])
        path = (payload.get("links") or {}).get("next") or ""
    return out


def resolve_app_id(token: str, app_id: str | None, bundle_id: str | None) -> str:
    if app_id:
        return app_id
    apps = list_apps(token)
    if bundle_id:
        for app in apps:
            if (app.get("attributes") or {}).get("bundleId") == bundle_id:
                return app["id"]
        raise SystemExit(f"No app with bundle id {bundle_id!r}. Use --list-apps.")
    if len(apps) == 1:
        return apps[0]["id"]
    names = [
        f"{a['id']}  {(a.get('attributes') or {}).get('name')}  "
        f"{(a.get('attributes') or {}).get('bundleId')}"
        for a in apps
    ]
    raise SystemExit(
        "Set APPLE_ASC_APP_ID or APPLE_ASC_BUNDLE_ID. Apps:\n  " + "\n  ".join(names)
    )


def ensure_ongoing_request(token: str, app_id: str) -> str:
    listed = api_request(
        token,
        "GET",
        f"/v1/apps/{app_id}/analyticsReportRequests",
        query={"filter[accessType]": "ONGOING", "limit": "10"},
    )
    for req in listed.get("data") or []:
        attrs = req.get("attributes") or {}
        if attrs.get("accessType") == "ONGOING" and not attrs.get("stoppedDueToInactivity"):
            return req["id"]

    created = api_request(
        token,
        "POST",
        "/v1/analyticsReportRequests",
        body={
            "data": {
                "type": "analyticsReportRequests",
                "attributes": {"accessType": "ONGOING"},
                "relationships": {
                    "app": {"data": {"type": "apps", "id": app_id}}
                },
            }
        },
    )
    return created["data"]["id"]


def paginate(token: str, path: str, query: dict[str, str] | None = None) -> list[dict]:
    rows: list[dict] = []
    q = query
    while path:
        payload = api_request(token, "GET", path, query=q)
        q = None
        rows.extend(payload.get("data") or [])
        path = (payload.get("links") or {}).get("next") or ""
    return rows


def download_url(url: str) -> bytes:
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=180) as resp:
        return resp.read()


def parse_tsv_bytes(blob: bytes) -> list[dict[str, str]]:
    # Segments may be plain TSV or zip of TSV(s)
    if blob[:2] == b"PK":
        rows: list[dict[str, str]] = []
        with zipfile.ZipFile(io.BytesIO(blob)) as zf:
            for name in zf.namelist():
                if name.endswith("/") or name.startswith("__"):
                    continue
                text = zf.read(name).decode("utf-8-sig", errors="replace")
                rows.extend(list(csv.DictReader(io.StringIO(text), delimiter="\t")))
        return rows
    text = blob.decode("utf-8-sig", errors="replace")
    return list(csv.DictReader(io.StringIO(text), delimiter="\t"))


INTERESTING_COL_HINTS = (
    "page view",
    "product page",
    "impression",
    "conversion",
    "download",
    "unit",
    "source",
    "date",
)


def summarize_rows(rows: list[dict[str, str]], days: int) -> dict[str, Any]:
    if not rows:
        return {"row_count": 0, "columns": [], "recent": []}

    cols = list(rows[0].keys())
    # Prefer a date-like column
    date_col = next(
        (c for c in cols if c.lower() in ("date", "day", "event date")),
        next((c for c in cols if "date" in c.lower()), None),
    )
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).date()

    recent = rows
    if date_col:
        filtered = []
        for r in rows:
            raw = (r.get(date_col) or "").strip()
            try:
                d = datetime.strptime(raw[:10], "%Y-%m-%d").date()
            except ValueError:
                continue
            if d >= cutoff:
                filtered.append(r)
        recent = filtered or rows

    # Aggregate numeric-looking columns that match engagement hints
    sums: dict[str, float] = {}
    for r in recent:
        for c, v in r.items():
            cl = c.lower()
            if not any(h in cl for h in INTERESTING_COL_HINTS):
                continue
            try:
                n = float(v.replace(",", "")) if v else 0.0
            except ValueError:
                continue
            sums[c] = sums.get(c, 0.0) + n

    # Sample of source breakdowns if present
    source_col = next(
        (c for c in cols if c.lower() in ("source", "source type", "page type")),
        None,
    )
    by_source: dict[str, int] = {}
    if source_col:
        for r in recent:
            key = (r.get(source_col) or "(blank)").strip() or "(blank)"
            by_source[key] = by_source.get(key, 0) + 1

    return {
        "row_count": len(recent),
        "columns": cols,
        "date_column": date_col,
        "sums": sums,
        "source_row_counts": dict(sorted(by_source.items(), key=lambda x: -x[1])[:20]),
        "sample_rows": recent[:5],
    }


def main() -> int:
    load_env()
    parser = argparse.ArgumentParser(description="Pull ASC App Store engagement analytics")
    parser.add_argument("--list-apps", action="store_true")
    parser.add_argument("--days", type=int, default=14, help="Summarize last N days of rows")
    parser.add_argument("--category", default="APP_STORE_ENGAGEMENT")
    args = parser.parse_args()

    issuer = os.environ.get("APPLE_ASC_ISSUER_ID", "").strip()
    key_id = os.environ.get("APPLE_ASC_KEY_ID", "").strip()
    key_path = os.environ.get("APPLE_ASC_PRIVATE_KEY_PATH", "").strip()
    app_id = os.environ.get("APPLE_ASC_APP_ID", "").strip() or None
    bundle_id = os.environ.get("APPLE_ASC_BUNDLE_ID", "").strip() or None

    if not issuer or not key_id or not key_path:
        print(
            "Missing APPLE_ASC_ISSUER_ID, APPLE_ASC_KEY_ID, or APPLE_ASC_PRIVATE_KEY_PATH in .env\n"
            "Create an API key in App Store Connect → Users and Access → Integrations →\n"
            "App Store Connect API, then fill .env (see .env.example).",
            file=sys.stderr,
        )
        return 1

    key_file = Path(key_path).expanduser()
    if not key_file.is_file():
        print(f"Private key not found: {key_file}", file=sys.stderr)
        return 1
    private_key = key_file.read_text()
    token = make_token(issuer, key_id, private_key)

    if args.list_apps:
        for app in list_apps(token):
            attrs = app.get("attributes") or {}
            print(f"{app['id']}\t{attrs.get('name')}\t{attrs.get('bundleId')}")
        return 0

    resolved_app = resolve_app_id(token, app_id, bundle_id)
    print(f"App ID: {resolved_app}")

    request_id = ensure_ongoing_request(token, resolved_app)
    print(f"Analytics report request (ONGOING): {request_id}")

    reports = paginate(
        token,
        f"/v1/analyticsReportRequests/{request_id}/reports",
        query={"filter[category]": args.category, "limit": "50"},
    )
    if not reports:
        print(
            f"No {args.category} reports yet.\n"
            "ONGOING requests can take hours–a day before first files appear.\n"
            "Re-run later, or check Analytics in App Store Connect UI."
        )
        out = {
            "app_id": resolved_app,
            "request_id": request_id,
            "category": args.category,
            "reports": [],
            "note": "empty — request may still be warming up",
        }
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        out_path = ROOT / "outputs" / f"{stamp}-asc-analytics-{args.category.lower()}.json"
        out_path.write_text(json.dumps(out, indent=2))
        print(f"Wrote {out_path}")
        return 0

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = ROOT / "outputs" / f"{stamp}-asc-analytics"
    out_dir.mkdir(parents=True, exist_ok=True)

    collected: list[dict[str, Any]] = []
    for report in reports:
        rattrs = report.get("attributes") or {}
        report_id = report["id"]
        report_name = rattrs.get("name") or report_id
        print(f"\nReport: {report_name} ({report_id})")

        instances = paginate(
            token,
            f"/v1/analyticsReports/{report_id}/instances",
            query={"limit": "20"},
        )
        # Prefer newest processingDate
        instances_sorted = sorted(
            instances,
            key=lambda i: (i.get("attributes") or {}).get("processingDate") or "",
            reverse=True,
        )
        for inst in instances_sorted[:3]:
            iattrs = inst.get("attributes") or {}
            inst_id = inst["id"]
            print(f"  Instance {inst_id}  processingDate={iattrs.get('processingDate')}  "
                  f"granularity={iattrs.get('granularity')}")
            segments = paginate(
                token,
                f"/v1/analyticsReportInstances/{inst_id}/segments",
                query={"limit": "50"},
            )
            for seg in segments:
                sattrs = seg.get("attributes") or {}
                url = sattrs.get("url")
                if not url:
                    continue
                blob = download_url(url)
                safe_name = "".join(
                    ch if ch.isalnum() or ch in "-_." else "_"
                    for ch in f"{report_name}-{inst_id}-{seg['id']}"
                )[:120]
                raw_path = out_dir / f"{safe_name}.bin"
                raw_path.write_bytes(blob)
                rows = parse_tsv_bytes(blob)
                tsv_path = out_dir / f"{safe_name}.tsv"
                if rows:
                    with tsv_path.open("w", newline="") as f:
                        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t")
                        w.writeheader()
                        w.writerows(rows)
                summary = summarize_rows(rows, args.days)
                print(
                    f"    Segment {seg['id']}: {summary['row_count']} rows "
                    f"(last ~{args.days}d), cols={len(summary['columns'])}"
                )
                if summary.get("sums"):
                    print("    Sums (hint-matched columns):")
                    for k, v in list(summary["sums"].items())[:12]:
                        print(f"      {k}: {v:g}")
                collected.append(
                    {
                        "report_id": report_id,
                        "report_name": report_name,
                        "instance_id": inst_id,
                        "processing_date": iattrs.get("processingDate"),
                        "segment_id": seg["id"],
                        "raw_file": str(raw_path.relative_to(ROOT)),
                        "tsv_file": str(tsv_path.relative_to(ROOT)) if rows else None,
                        "summary": summary,
                    }
                )

    meta_out = {
        "pulled_at": datetime.now(timezone.utc).isoformat(),
        "app_id": resolved_app,
        "request_id": request_id,
        "category": args.category,
        "days": args.days,
        "segments": collected,
    }
    summary_path = ROOT / "outputs" / f"{stamp}-asc-analytics-summary.json"
    summary_path.write_text(json.dumps(meta_out, indent=2))
    print(f"\nWrote {summary_path}")
    if not collected:
        print(
            "No downloadable segments yet — Apple often lags 1–2 days after enabling ONGOING."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
