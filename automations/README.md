# Cursor Automations for GoStylens

Templates for scheduled agent workflows. Create these in Cursor's Automations editor (Agents window).

## 1. Weekly growth digest

| Field | Value |
|-------|-------|
| **Trigger** | Schedule — every Monday 9:00 AM |
| **Repo** | `gostylens-harness` |
| **Tools** | PostHog MCP, file write |
| **Instructions** | Follow `agents/growth-analyst.md`. Run the weekly health check for the last 7 days. Save report to `outputs/YYYY-MM-DD-growth-report.md`. Summarize top 3 findings in the automation output. |

## 2. Monthly marketing experiment backlog

| Field | Value |
|-------|-------|
| **Trigger** | Schedule — 1st of month |
| **Repo** | `gostylens-harness` |
| **Tools** | PostHog MCP, file write |
| **Instructions** | Follow `agents/marketing.md`. Review last 30 days of funnel + retention data. Generate 5 experiment ideas ranked by ICE score. Save to `outputs/YYYY-MM-01-experiment-backlog.md`. |

## 3. Post-release insight snapshot

| Field | Value |
|-------|-------|
| **Trigger** | Git — tag push matching `v*` on `stylens` repo |
| **Repo** | `gostylens-harness` |
| **Tools** | PostHog MCP |
| **Instructions** | Compare key metrics (signup, activation, purchase) for 7 days before vs 7 days after the release tag date. Note any significant shifts. Save to `outputs/YYYY-MM-DD-release-snapshot.md`. |

## Setup checklist

- [ ] PostHog MCP connected in Cursor dashboard
- [ ] `.env` filled with PostHog personal API key
- [ ] PostHog insights created for core funnels (see `context/analytics-events.md`)
- [ ] `context/marketing/positioning.md` filled in with real copy
- [ ] Automations created from templates above

## Manual runs

You can also trigger any agent prompt ad-hoc in Cursor chat:

```
@agents/marketing.md @context/marketing/positioning.md

Query PostHog for intro funnel last 14 days. Propose 3 TikTok hooks to improve intro completion.
```
