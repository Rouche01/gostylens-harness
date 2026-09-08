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

### App (`stylens`)

- Event taxonomy source: `stylens/lib/` analytics calls
- Sync helper: `./scripts/sync-event-taxonomy.sh ../stylens`

### Landing page (`stylens-lp`)

- Useful for acquisition / ASO / web funnel questions
- PostHog pageviews and custom events share the mobile project

### API (`stylens-lite-api`)

- Backend for analysis sessions, usage limits, subscription sync
- Staging / prod API hosts: see `context/product.md`

## Notion (Experiments backlog)

- **Canonical backlog**: [Experiments](https://www.notion.so/3cf3d958f9998087b60ccea1e848d2ad) under GoStylens teamspace → GoStylens
- **Schema / lifecycle**: `context/experiments.md`
- **Database ID**: `3cf3d958-f999-8087-b60c-cea1e848d2ad`
- **Harness role**: agents create/update rows via Notion MCP; PostHog supplies evidence; git does not mirror the backlog
- **Env**: `NOTION_EXPERIMENTS_DATABASE_ID` in `.env`
- **Priority bias**: `Domain(s)` = `User Acquisition` (or both domains when mixed)

## Future integrations

| Tool | Use case |
|------|----------|
| Slack | Weekly digest delivery |
| Linear | Eng / product issue tracking (experiments stay in Notion) |
| App Store Connect | ASO copy drafts vs. conversion data |
