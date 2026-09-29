# Cursor Automations for GoStylens

Templates for scheduled agent workflows. Create these in Cursor's Automations editor (Agents window).

## 1. Weekly growth digest

| Field | Value |
|-------|-------|
| **Trigger** | Schedule — every Monday 9:00 AM |
| **Repo** | `gostylens-harness` |
| **Tools** | PostHog MCP, Notion MCP, file write |
| **Instructions** | Follow `agents/growth-analyst.md`. Run the weekly health check for the last 7 days. Save report to `outputs/YYYY-MM-DD-growth-report.md`. Summarize top 3 findings. If clear acquisition gaps appear, create or update Notion Experiments `idea` rows (`Domain(s)` = `User Acquisition`, or both for mixed) — do not duplicate existing rows. |

## 2. Monthly marketing experiment backlog

| Field | Value |
|-------|-------|
| **Trigger** | Schedule — 1st of month |
| **Repo** | `gostylens-harness` |
| **Tools** | PostHog MCP, Notion MCP |
| **Instructions** | Follow `agents/marketing.md` and `context/experiments.md`. Review last 30 days of funnel + retention data. Generate up to 5 acquisition-first experiment ideas. **Upsert into Notion Experiments** with lean properties (Status=`idea`, Domain(s), Priority) and the full page-body template (Goal, Hypothesis, Primary metric, Channel & effort, Execution plan). Optional short summary in `outputs/` — Notion remains canonical. |

## 3. Post-release insight snapshot

| Field | Value |
|-------|-------|
| **Trigger** | Git — tag push matching `v*` on `stylens` repo |
| **Repo** | `gostylens-harness` |
| **Tools** | PostHog MCP, Notion MCP (optional) |
| **Instructions** | Compare key metrics (signup, activation, purchase) for 7 days before vs 7 days after the release tag date. Note any significant shifts. Save to `outputs/YYYY-MM-DD-release-snapshot.md`. If a running Notion experiment relates to the release, update its Result with numbers. |

## 4. Monthly competitor scan (optional)

| Field | Value |
|-------|-------|
| **Trigger** | Schedule — 1st of month (or ad-hoc) |
| **Repo** | `gostylens-harness` |
| **Tools** | perplexity-search (preferred), WebSearch/WebFetch fallback, Browser for deep dives, Notion MCP if creating ideas |
| **Instructions** | Run `/competitor-scan monthly --notion` skill (see `.cursor/skills/competitor-scan/SKILL.md`). Follow `agents/marketing.md` competitor-scan template. Re-scan stale watchlist rows; save briefs to `outputs/`; upsert ≤5 Notion `idea` rows. |

## Setup checklist

- [ ] PostHog MCP connected in Cursor dashboard
- [ ] Notion MCP connected; Experiments DB URL/ID in `context/experiments.md` and `.env`
- [ ] `.env` filled with PostHog personal API key + `NOTION_EXPERIMENTS_DATABASE_ID`
- [ ] PostHog insights created for core funnels (see `context/analytics-events.md`)
- [ ] `context/marketing/positioning.md` filled in with real copy
- [ ] Automations created from templates above
- [ ] Optional: invoke `/competitor-scan` once manually to verify skill + research tools

## Manual runs

### Competitor scan (slash skill)

In Agent chat, type:

```text
/competitor-scan
```

Or target specific competitors / create Notion rows:

```text
/competitor-scan Lekondo
/competitor-scan Lekondo Acloset --notion
/competitor-scan monthly --notion
```

Skill lives at `.cursor/skills/competitor-scan/SKILL.md` (`disable-model-invocation: true` — only runs when you invoke it).

### Other marketing prompts

You can also trigger any agent prompt ad-hoc in Cursor chat:

```
@agents/marketing.md @context/marketing/positioning.md @context/experiments.md

Query PostHog for intro funnel last 14 days. Propose 3 TikTok hooks to improve intro completion.
Create acquisition experiments in Notion with Primary metrics from analytics-events.md.
```
