---
name: campaign-ideas
description: >-
  From a named GoStylens funnel drop-off, propose 3 acquisition experiments and
  create Notion idea rows with full template. Invoke with /campaign-ideas.
disable-model-invocation: true
---

# Campaign ideas

## When invoked

Follow `agents/marketing.md` → **Campaign ideas → Notion rows**. Narrower than `/experiment-backlog` (one drop → exactly 3 ideas).

## Arguments

| User says | Do this |
|-----------|---------|
| `/campaign-ideas` | Infer worst drop from last 14d PostHog (state which) → 3 ideas |
| `/campaign-ideas activation` | Focus auth → `ai_stream_completed` |
| `/campaign-ideas intro` / `monetization` / `retention` | That focus |
| `/campaign-ideas --dry-run` | Propose 3; do not create Notion rows |

## Required reads

1. `agents/marketing.md`
2. `context/marketing/positioning.md`
3. `context/analytics-events.md`
4. `context/experiments.md`
5. PostHog for the named drop

## Steps

1. Quantify the drop with exact events.
2. Search Notion for duplicates.
3. Propose **exactly 3** experiments (observation / hypothesis / experiment separated).
4. Unless `--dry-run`: create 3 Notion rows (`idea`, `User Acquisition`, Priority P1/P2, template_id `3cf3d958-f999-807b-9697-c7e052f6192f`); fill Goal / Hypothesis / Primary metric / Channel & effort / Execution plan.
5. Optional short draft under `outputs/`.

## Do not

- More than 3 rows  
- Skip PostHog evidence  
- Overlap blindly with `/experiment-backlog` monthly dump — stay tied to one drop
