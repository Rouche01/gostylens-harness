# Integrations

Reference for agents and scripts. Secrets live in `.env` (never committed).

## PostHog

- **Host**: `https://n.gostylens.com`
- **Client SDK key**: in `stylens` app (`POSTHOG_API_KEY` in env config) — ingestion only
- **Personal API key**: in this repo's `.env` — for MCP / API queries
- **MCP setup**: `npx @posthog/wizard@latest mcp add`

Agents should query PostHog for quantitative context (funnels, retention, experiments).

## RevenueCat

- Subscriptions managed in app via RevenueCat SDK
- Key events mirrored in PostHog (`purchase_*`, `subscription_initialized`)
- Optional: sync RC data into PostHog warehouse for LTV analysis

## Supabase

- Auth backend for the app
- Not typically queried from this harness unless building ops tooling

## Product repos (siblings under `~/Projects/`)

Agents treat these as **read-only**. Ship code changes in those repos, not here.

| Repo | Path | Remote | Role |
|------|------|--------|------|
| **stylens** | `../stylens` | [Rouche01/stylens](https://github.com/Rouche01/stylens) | Flutter app; primary PostHog event source (`lib/` analytics calls) |
| **stylens-lp** | `../stylens-lp` | [Rouche01/stylens-lp](https://github.com/Rouche01/stylens-lp) | Landing page ([gostylens.app](https://gostylens.app)); Cloudflare Pages; same PostHog project |
| **stylens-lite-api** | `../stylens-lite-api` | [Rouche01/stylens-lite-api](https://github.com/Rouche01/stylens-lite-api) | Cloudflare Workers API — style sessions, users, subscriptions (D1, R2, Supabase) |
| **stylens-ops** | `../stylens-ops` | (local scaffold; remote TBD) | Runnable ops — community HITL, Telegram approval, future channels. Strategy stays in this harness. |

### App (`stylens`)

- Event taxonomy source: `stylens/lib/` analytics calls
- Sync helper: `./scripts/sync-event-taxonomy.sh ../stylens`

### Landing page (`stylens-lp`)

- Useful for acquisition / ASO / web funnel questions
- PostHog pageviews and custom events share the mobile project

### API (`stylens-lite-api`)

- Backend for analysis sessions, usage limits, subscription sync
- Staging / prod API hosts: see `context/product.md`

### Ops (`stylens-ops`)

- **Role:** execute approved ops (bots, crons, webhooks) — not experiment design
- **First capability:** community scout → draft → Telegram Approve/Edit/Abort → Reddit execute
- **Hard rule:** never auto-post; human gate required
- **Plan:** `../stylens-ops/.cursor/plans/stylens_ops_community_hitl.plan.md` (canonical; open in the `stylens-ops` workspace)
- Agents propose copy/rules here; ship runtime code in `stylens-ops`

## Notion (Experiments backlog)

- **Canonical backlog**: [Experiments](https://www.notion.so/3cf3d958f9998087b60ccea1e848d2ad) under GoStylens teamspace → GoStylens
- **Schema / lifecycle**: `context/experiments.md`
- **Database ID**: `3cf3d958-f999-8087-b60c-cea1e848d2ad`
- **Harness role**: agents create/update rows via Notion MCP; PostHog supplies evidence; git does not mirror the backlog
- **Env**: `NOTION_EXPERIMENTS_DATABASE_ID` in `.env`
- **Priority bias**: `Domain(s)` = `User Acquisition` (or both domains when mixed)

## Meta Ads (Marketing API)

- **Use:** read campaign / ad set / ad Insights (spend, clicks, CPC, CTR) for acquisition experiments
- **Env:** `META_ACCESS_TOKEN`, `META_AD_ACCOUNT_ID` (optional `META_GRAPH_VERSION`)
- **Script:** `./scripts/meta-ads-insights.sh [date_preset] [level]`
  - Examples: `./scripts/meta-ads-insights.sh last_7d campaign`
  - Levels: `campaign` | `adset` | `ad`
- **Privacy policy URL** (App Dashboard → Settings → Basic): `https://gostylens.app/privacy`
- **Mode:** Development is enough to read **your own** ad account; Live not required for that
- **Token:** System User (preferred) or Graph API Explorer user token with `ads_read`
- Pair Meta cost metrics with PostHog product events (`auth_succeeded`, `ai_stream_completed`) — Meta alone won’t show true activation without the app SDK

## App Store Connect (Analytics API)

- **Use:** product page views, impressions, conversion-ish engagement vs Meta LPVs / PostHog installs
- **Env:** `APPLE_ASC_ISSUER_ID`, `APPLE_ASC_KEY_ID`, `APPLE_ASC_PRIVATE_KEY_PATH`
  - Optional: `APPLE_ASC_BUNDLE_ID` (default GoStylens: `com.stylenslab.gostylens`) or `APPLE_ASC_APP_ID`
- **Script:** `./scripts/asc-analytics.sh` (Python helper: `scripts/asc_analytics.py`)
  - First run creates an **ONGOING** analytics report request if missing
  - Pulls `APP_STORE_ENGAGEMENT` report segments into `outputs/`
  - `./scripts/asc-analytics.sh --list-apps` to resolve Apple IDs
- **Deps:** local `.venv` with `PyJWT` + `cryptography` (`python3 -m venv .venv && .venv/bin/pip install PyJWT cryptography`)
- **Caveats:** Apple often lags **1–2 days**; first ONGOING files can take hours after enable. Not live clickstream.
- **Key setup:** App Store Connect → Users and Access → Integrations → App Store Connect API (Admin / access to App Analytics)

## Future integrations

| Tool | Use case |
|------|----------|
| Telegram | HITL approvals for `stylens-ops` (community drafts); optional digests |
| Slack | Optional team digests (prefer Telegram for solo HITL) |
| Linear | Eng / product issue tracking (experiments stay in Notion) |
