---
name: funnel-diagnose
description: >-
  Diagnose a GoStylens PostHog funnel drop-off: step rates, segments, WoW,
  session-replay filters, optional Notion experiment ideas. Invoke with
  /funnel-diagnose.
disable-model-invocation: true
---

# Funnel diagnose

## When invoked

Follow `agents/growth-analyst.md` → **Funnel diagnosis**.

## Arguments

| User says | Do this |
|-----------|---------|
| `/funnel-diagnose` | Default: **intro → auth → activation** (`intro_started` → `intro_completed` → `auth_succeeded` → `ai_stream_completed`), last 30 days |
| `/funnel-diagnose activation` | `auth_succeeded` → `ai_stream_completed` |
| `/funnel-diagnose monetization` | `ai_stream_completed` → `purchase_started` → `purchase_completed` |
| `/funnel-diagnose intro` | `intro_started` → `intro_completed` → `auth_succeeded` |
| `/funnel-diagnose 14d …` | Override lookback |
| `/funnel-diagnose --notion` | Draft Notion `idea` rows for the worst drop |

## Required reads

1. `agents/growth-analyst.md`
2. `context/analytics-events.md`
3. `context/experiments.md` (if `--notion`)

## Steps

1. Confirm funnel steps with exact events (never invent names).
2. Query PostHog: step conversion, platform + new vs returning, WoW if possible.
3. Suggest session-replay filters for the worst step.
4. Separate **observation** vs **hypothesis** vs **experiment**.
5. Optional: save short note to `outputs/YYYY-MM-DD-funnel-{slug}.md`.
6. If `--notion`: dedupe; create ≤3 `idea` rows with Primary metric = this funnel; template_id `3cf3d958-f999-807b-9697-c7e052f6192f`.

## Do not

- Use `style_analysis_session_created` for activation  
- Create Notion rows without user `--notion` or explicit ask
