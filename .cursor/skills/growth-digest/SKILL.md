---
name: growth-digest
description: >-
  Run GoStylens weekly growth health check via PostHog: signups, activation,
  subscription, intro rates. Save dated report under outputs/. Optionally draft
  Notion experiment ideas. Invoke with /growth-digest.
disable-model-invocation: true
---

# Growth digest

## When invoked

Follow `agents/growth-analyst.md` → **Weekly health check**. Use exact event names from `context/analytics-events.md`.

## Arguments

| User says | Do this |
|-----------|---------|
| `/growth-digest` | Last **7 days** health check |
| `/growth-digest 14d` / `30d` | That lookback window |
| `/growth-digest --notion` | Also create/update Notion Experiments `idea` rows for clear acquisition gaps (dedupe first) |

## Required reads

1. `agents/growth-analyst.md`
2. `context/analytics-events.md`
3. `context/integrations.md`
4. `context/experiments.md` (if `--notion`)

## Steps

1. Query PostHog for the window:
   - New signups: `auth_succeeded` where `is_new_user=true`
   - Activation: signup → first `ai_stream_completed` (7-day window; do **not** use `style_analysis_session_created`)
   - Subscription: `purchase_completed` / `purchase_started`
   - Intro: `intro_completed` / `intro_started`
   - Top errors if available
2. Segment by platform where useful; note WoW if prior period available.
3. Write `outputs/YYYY-MM-DD-growth-report.md` using the growth-analyst output format.
4. If `--notion`: search Experiments for duplicates; create ≤3 `idea` rows (`User Acquisition`, template_id `3cf3d958-f999-807b-9697-c7e052f6192f`).
5. End with top 3 findings + recommended owners (marketing / product / eng).

## Do not

- Invent PostHog events  
- Treat markdown as the experiment backlog  
- Write marketing copy (use `/copy-draft` or marketing agent)
