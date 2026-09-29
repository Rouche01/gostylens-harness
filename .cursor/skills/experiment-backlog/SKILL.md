---
name: experiment-backlog
description: >-
  Review last 30 days of GoStylens PostHog funnel/retention and upsert up to 5
  acquisition-first Notion Experiments idea rows. Invoke with /experiment-backlog.
disable-model-invocation: true
---

# Experiment backlog

## When invoked

Follow `agents/marketing.md` → **Campaign ideas / Experiment backlog** and Automation #2. Notion is source of truth.

## Arguments

| User says | Do this |
|-----------|---------|
| `/experiment-backlog` | Last **30 days**; propose and **create** ≤5 Notion `idea` rows |
| `/experiment-backlog 14d` | Shorter lookback |
| `/experiment-backlog --dry-run` | Propose only; do not create Notion rows |

## Required reads

1. `agents/marketing.md`
2. `context/marketing/positioning.md`
3. `context/analytics-events.md`
4. `context/experiments.md`
5. Query PostHog for funnel + retention signal

## Steps

1. Pull last N days: intro, auth (new users), activation (`ai_stream_completed`), purchase funnel.
2. Search Notion Experiments for duplicates / related running ideas.
3. Generate up to **5** acquisition-first experiments (P0/P1 bias).
4. Unless `--dry-run`: create rows with `Status=idea`, `Domain(s)=User Acquisition` (add Product Feature if mixed), Priority, `template_id` `3cf3d958-f999-807b-9697-c7e052f6192f`; wait for template; fill Goal / Hypothesis / Primary metric / Channel & effort / Execution plan.
5. Optional: short summary in `outputs/YYYY-MM-DD-experiment-backlog.md`.

## Do not

- Parallel markdown backlog instead of Notion  
- Invent event names  
- More than 5 new rows per run
