# Cursor Automations for GoStylens

Templates for scheduled agent workflows. Create these in Cursor's Automations editor (Agents window).

## 1. Weekly growth digest

| Field | Value |
|-------|-------|
| **Trigger** | Schedule — every Monday 9:00 AM |
| **Repo** | `gostylens-harness` |
| **Tools** | PostHog MCP, Notion MCP, file write |
| **Skill** | `/growth-digest` (`.cursor/skills/growth-digest/SKILL.md`) |
| **Instructions** | Equivalent to `/growth-digest --notion`. Follow `agents/growth-analyst.md`. Run the weekly health check for the last 7 days. Save report to `outputs/YYYY-MM-DD-growth-report.md`. Summarize top 3 findings. If clear acquisition gaps appear, create or update Notion Experiments `idea` rows (`Domain(s)` = `User Acquisition`, or both for mixed) — do not duplicate existing rows. |

## 2. Monthly marketing experiment backlog

| Field | Value |
|-------|-------|
| **Trigger** | Schedule — 1st of month |
| **Repo** | `gostylens-harness` |
| **Tools** | PostHog MCP, Notion MCP |
| **Skill** | `/experiment-backlog` (`.cursor/skills/experiment-backlog/SKILL.md`) |
| **Instructions** | Equivalent to `/experiment-backlog`. Follow `agents/marketing.md` and `context/experiments.md`. Review last 30 days of funnel + retention data. Generate up to 5 acquisition-first experiment ideas. **Upsert into Notion Experiments** with lean properties (Status=`idea`, Domain(s), Priority) and the full page-body template (Goal, Hypothesis, Primary metric, Channel & effort, Execution plan). Optional short summary in `outputs/` — Notion remains canonical. |

## 3. Post-release insight snapshot

| Field | Value |
|-------|-------|
| **Trigger** | Git — tag push matching `v*` on `stylens` repo |
| **Repo** | `gostylens-harness` |
| **Tools** | PostHog MCP, Notion MCP (optional) |
| **Skill** | `/release-snapshot` (`.cursor/skills/release-snapshot/SKILL.md`) |
| **Instructions** | Equivalent to `/release-snapshot <tag> --notion`. Compare key metrics (signup, activation, purchase) for 7 days before vs 7 days after the release tag date. Note any significant shifts. Save to `outputs/YYYY-MM-DD-release-snapshot.md`. If a running Notion experiment relates to the release, update its Result with numbers. |

## 4. Monthly competitor scan

Optional after the manual `/competitor-scan` loop works (briefs + Notion ideas verified once). Prefer scheduling on a **different day** than automation #2 (e.g. 1st = experiment backlog, **15th** = competitor scan) so agents don’t compete for the same Notion edits.

| Field | Value |
|-------|-------|
| **Trigger** | Schedule — 15th of month 10:00 AM (or ad-hoc via `/competitor-scan`) |
| **Repo** | `gostylens-harness` |
| **Tools** | perplexity-search (preferred) → WebSearch/WebFetch fallback → Browser MCP for LP/ASO deep dives; Notion MCP for ideas |
| **Skill** | `.cursor/skills/competitor-scan/SKILL.md` |
| **Instructions** | Follow `agents/marketing.md` → Competitor scan → experiments. Equivalent prompt: `/competitor-scan monthly --notion`. Re-scan watchlist rows with `Last reviewed` empty or older than ~30 days (max 3 unless monthly mode). Write `outputs/YYYY-MM-DD-competitor-{slug}.md`. Update `Last reviewed` in `context/marketing/competitors.md`. Dedupe Notion Experiments; create ≤5 `idea` rows (`Domain(s)` = `User Acquisition`, Priority P1/P2, template_id `3cf3d958-f999-807b-9697-c7e052f6192f`). Link brief paths under Assets / links. End with a short summary of who was scanned and top transferable ideas. |

### Cadence (manual + scheduled)

| Cadence | How | Output |
|---------|-----|--------|
| Ad hoc | `/competitor-scan Lekondo` (or names) | Brief(s) under `outputs/`; Notion only with `--notion` |
| Monthly | Automation #4 or `/competitor-scan monthly --notion` | Stale watchlist re-scan; ≤5 Notion ideas |
| After experiment closes | Chat: revisit related competitor notes in briefs | Optional brief refresh; update Notion Result if relevant |

No `stylens-ops` involvement. Do not auto-post.

## Setup checklist

- [ ] PostHog MCP connected in Cursor dashboard
- [ ] Notion MCP connected; Experiments DB URL/ID in `context/experiments.md` and `.env`
- [ ] `.env` filled with PostHog personal API key + `NOTION_EXPERIMENTS_DATABASE_ID`
- [ ] PostHog insights created for core funnels (see `context/analytics-events.md`)
- [ ] `context/marketing/positioning.md` filled in with real copy
- [ ] Automations created from templates above
- [ ] Optional: invoke `/competitor-scan` and `/growth-digest` once manually to verify skills + MCPs

## Manual runs

### Slash skills (preferred)

All live under `.cursor/skills/*/SKILL.md` with `disable-model-invocation: true` — type `/skill-name` in Agent chat.

| Skill | Use for |
|-------|---------|
| `/growth-digest` | Weekly health check → `outputs/` (+ `--notion`) |
| `/funnel-diagnose` | Named funnel drop diagnosis |
| `/experiment-backlog` | Monthly-style ≤5 Notion acquisition ideas |
| `/campaign-ideas` | One drop → exactly 3 Notion ideas |
| `/close-experiment` | Fill Result + Decision on a Notion experiment |
| `/copy-draft` | ASO / social / email / LP variants |
| `/competitor-scan` | Competitor briefs → optional Notion |
| `/release-snapshot` | Pre/post release PostHog compare |
| `/meta-ads-review` | Meta script + PostHog activation pairing |
| `/aso-pulse` | ASC analytics pull + ASO summary |
| `/community-draft` | Human-gated community drafts (no auto-post) |
| `/sync-events` | Sync event taxonomy from `stylens` |

### Competitor scan examples

```text
/competitor-scan
/competitor-scan Lekondo
/competitor-scan Lekondo Acloset --notion
/competitor-scan monthly --notion
```

### Other examples

```text
/growth-digest --notion
/funnel-diagnose activation 14d
/close-experiment https://app.notion.com/p/…
/meta-ads-review last_7d campaign
/aso-pulse
/sync-events
```

### Freeform (still works)

```
@agents/marketing.md @context/marketing/positioning.md @context/experiments.md

Query PostHog for intro funnel last 14 days. Propose 3 TikTok hooks to improve intro completion.
Create acquisition experiments in Notion with Primary metrics from analytics-events.md.
```
