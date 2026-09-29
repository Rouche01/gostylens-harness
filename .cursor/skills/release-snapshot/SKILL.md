---
name: release-snapshot
description: >-
  Compare GoStylens PostHog metrics 7 days before vs after an app release tag;
  save release snapshot under outputs/; optionally update related Notion
  experiments. Invoke with /release-snapshot.
disable-model-invocation: true
---

# Release snapshot

## When invoked

Follow Automation #3 (Post-release insight snapshot) and `agents/growth-analyst.md` for metric discipline.

## Arguments

| User says | Do this |
|-----------|---------|
| `/release-snapshot` | Infer latest meaningful date from user or ask for tag/date |
| `/release-snapshot v1.2.3` | Use that version; resolve release date if possible (git tag in `../stylens` or user-provided date) |
| `/release-snapshot 2026-09-20` | Use that calendar date as release day |
| `/release-snapshot … --notion` | Update Result on related running Notion experiments if clearly tied |

## Required reads

1. `context/analytics-events.md`
2. `context/integrations.md`
3. `context/experiments.md` (if `--notion`)

## Steps

1. Fix release date `D`.
2. Query PostHog **7 days before D** vs **7 days after D** (exclude D or assign consistently; state which):
   - New `auth_succeeded` (`is_new_user`)
   - Activation: → `ai_stream_completed`
   - `purchase_started` / `purchase_completed`
   - Intro completion if relevant
3. Call out significant shifts only (with absolute numbers, not vibes).
4. Save `outputs/YYYY-MM-DD-release-snapshot.md` (include tag/date).
5. If `--notion`: search Experiments for release-related rows; append Result notes — do not change Goal/Primary metric.

## Do not

- Modify Flutter/`stylens` code  
- Invent events  
- Over-claim causality without noting confounders (ads, seasonality)
