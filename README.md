# GoStylens Harness

**An AI agent workspace for GoStylens growth, marketing, and ops — kept separate from the Flutter app.**

This repo is the context and control plane for agents that work *on* GoStylens (campaign ideas, funnel analysis, weekly digests, experiment backlogs). It is **not** the product codebase. Product code lives in sibling repos: `stylens` (app), `stylens-lp` (landing page), and `stylens-lite-api` (backend).

---

## Why this exists

The Flutter app (`stylens`) is for shipping features. Mixing marketing prompts, brand docs, analytics playbooks, and scheduled agent jobs into that repo creates noise and risk.

This harness gives agents:

1. **Stable product context** — what GoStylens is, who it’s for, how the funnel works  
2. **Exact analytics vocabulary** — PostHog event names from the app, so queries don’t invent metrics  
3. **Task-specific agent roles** — marketing vs growth analyst vs future specialists  
4. **A place for automation** — weekly digests and experiment backlogs without touching app CI  
5. **A sink for outputs** — dated reports and drafts you can review or commit as history  

Agents combine this repo’s docs with live PostHog data (via MCP) and the Notion **Experiments** backlog to answer questions and run acquisition-first experiments grounded in real usage.

---

## What this repo does *not* do

- Change Flutter / iOS / Android code (that stays in `stylens`)
- Change landing page or API code (that stays in `stylens-lp` / `stylens-lite-api`)
- Replace PostHog, RevenueCat, or your backend
- Act as a public marketing site or CMS
- Store production secrets (use local `.env`; never commit keys)

---

## How it works

```text
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ stylens          │  │ stylens-lp       │  │ stylens-lite-api │
│ Flutter app      │  │ gostylens.app    │  │ Cloudflare API   │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         │                     │                     │
         └──────────┬──────────┴─────────────────────┘
                    ▼
           ┌──────────────────┐     ┌──────────────────┐
           │ PostHog          │     │ Notion           │
           │ n.gostylens.com  │     │ Experiments DB   │
           └────────┬─────────┘     └────────┬─────────┘
                    │ MCP                    │ MCP
┌───────────────────┐│                       │
│ gostylens-harness ├┘───────────────────────┘
│ context + agents  │──────────▶ AI agent in Cursor ──▶ outputs/*.md
└───────────────────┘              (backlog lives in Notion)
```

| Layer | Role |
|-------|------|
| `context/` | Source of truth for product, brand, events, integrations, experiment schema |
| `agents/` | Instructions for how the agent should behave on a given task |
| PostHog MCP | Live numbers (funnels, retention) |
| Notion MCP | Canonical **Experiments** backlog (idea → plan → result → decision) |
| `automations/` | Templates for scheduled Cursor Automations |
| `outputs/` | Generated reports and drafts (not the experiment backlog) |

---

## Repository layout

```text
gostylens-harness/
├── README.md                 ← you are here
├── .env.example              ← secrets template (copy to .env)
├── .cursor/rules/            ← Cursor rules for this repo
├── context/
│   ├── product.md            ← product overview & user journey
│   ├── analytics-events.md   ← PostHog event taxonomy
│   ├── integrations.md       ← PostHog, Notion, RevenueCat, repos
│   ├── experiments.md        ← Notion Experiments schema + DB link
│   └── marketing/
│       └── positioning.md    ← brand voice, ICP, messaging
├── agents/
│   ├── marketing.md          ← campaigns, copy, Notion experiments
│   └── growth-analyst.md     ← funnels, retention, weekly health
├── automations/
│   └── README.md             ← scheduled workflow templates
├── scripts/
│   └── sync-event-taxonomy.sh ← scan stylens for new event names
└── outputs/                  ← agent-generated artifacts (not the backlog)
```

---

## Quick start

### 1. Open this repo in Cursor

Open `/path/to/gostylens-harness` as its own workspace (separate from `stylens`).

### 2. Configure secrets

```bash
cp .env.example .env
```

Add a PostHog **personal API key** (project read access) — not the client SDK key from the mobile app.

### 3. Connect PostHog MCP

```bash
npx @posthog/wizard@latest mcp add
```

### 4. Connect Notion Experiments

1. Notion MCP should already be authenticated in Cursor.
2. Canonical DB: [Experiments](https://www.notion.so/3cf3d958f9998087b60ccea1e848d2ad) under GoStylens → GoStylens (see `context/experiments.md`).
3. Ensure `.env` includes `NOTION_EXPERIMENTS_DATABASE_ID=3cf3d958-f999-8087-b60c-cea1e848d2ad` (from `.env.example`).

Notion is the canonical experiment backlog (acquisition-first).

### 5. Fill brand context

Edit `context/marketing/positioning.md` with real positioning, ICP, and voice. Agents treat this as marketing source of truth.

### 6. Run a task

In Cursor chat, for example:

> Follow `agents/marketing.md`. Read positioning + analytics events. Query PostHog for the intro → auth → first style analysis funnel (last 30 days). Create 3 acquisition experiments in Notion with goals, hypotheses, and Primary metrics.

Or for analytics:

> Follow `agents/growth-analyst.md`. Produce a weekly health check for the last 7 days. Save to `outputs/`. Link any recommended actions to Notion experiment ideas.

---

## Built-in agents

| Agent | File | Use when you want |
|-------|------|-------------------|
| **Marketing** | `agents/marketing.md` | Campaign ideas, copy variants, Priority-ranked Notion experiments |
| **Growth analyst** | `agents/growth-analyst.md` | Funnel diagnosis, retention, weekly metric reports, closing experiment results |

Both agents **cite PostHog metrics**, use **exact event names** from `context/analytics-events.md`, and treat Notion **Experiments** as the backlog (`context/experiments.md`).

---

## Automation

See [`automations/README.md`](automations/README.md) for Cursor Automation templates:

| Automation | Trigger | Output |
|------------|---------|--------|
| Weekly growth digest | Monday schedule | `outputs/YYYY-MM-DD-growth-report.md` (+ Notion idea rows if useful) |
| Monthly experiment backlog | 1st of month | New/updated Notion Experiments rows (acquisition-first) |
| Post-release snapshot | App `v*` tag | Before/after metric comparison |

Create these in Cursor’s Automations editor; the templates describe triggers, tools, and prompts.

---

## Keeping analytics context fresh

When the app adds PostHog events, sync names from the sibling `stylens` checkout:

```bash
./scripts/sync-event-taxonomy.sh ../stylens
```

Then update `context/analytics-events.md` with any new events and properties.

---

## Related systems

Assume a local checkout layout under `~/Projects/` (siblings of this repo):

| Repo / system | Local path | Remote | Role |
|---------------|------------|--------|------|
| **stylens** | `../stylens` | [Rouche01/stylens](https://github.com/Rouche01/stylens) | Flutter mobile app (iOS + Android); primary PostHog event source |
| **stylens-lp** | `../stylens-lp` | [Rouche01/stylens-lp](https://github.com/Rouche01/stylens-lp) | Landing page for [gostylens.app](https://gostylens.app) (Cloudflare Pages); shares PostHog project |
| **stylens-lite-api** | `../stylens-lite-api` | [Rouche01/stylens-lite-api](https://github.com/Rouche01/stylens-lite-api) | Cloudflare Workers API (sessions, users, subscriptions; D1, R2, Supabase auth) |
| **PostHog** | — | `https://n.gostylens.com` | Product analytics, session replay |
| **Notion** | — | Experiments DB (see `context/experiments.md`) | Canonical experiment backlog |
| **RevenueCat** | — | — | Subscriptions; purchase events also mirrored in PostHog |

Agents in this harness treat product repos as **read-only context**. Code changes belong in those repos, not here.

---

## Principles

1. **Evidence over opinions** — recommendations should cite funnels, retention, or qualitative signals (e.g. session replay).  
2. **Separate concerns** — app code ≠ agent ops.  
3. **Exact event names** — never invent PostHog events; use the taxonomy file.  
4. **Notion owns experiments** — status/results/decisions live in the Experiments DB, not a parallel markdown backlog.  
5. **Dated outputs** — write reports under `outputs/` so runs are reviewable.  
6. **No secrets in git** — `.env` is gitignored; only `.env.example` is committed.

---

## Status

Scaffold is ready for interactive agent use. Next steps typically are:

1. Ensure Notion MCP is connected; Experiments DB is linked in `context/experiments.md`  
2. Complete `context/marketing/positioning.md`  
3. Create core PostHog funnel insights (see `context/analytics-events.md`)  
4. Wire the first Cursor Automation (weekly growth digest)