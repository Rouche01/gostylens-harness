---
name: sync-events
description: >-
  Sync PostHog event names from the stylens app into gostylens-harness taxonomy
  via script and update analytics-events.md. Invoke with /sync-events.
disable-model-invocation: true
---

# Sync events

## When invoked

Keep `context/analytics-events.md` aligned with `../stylens` analytics calls.

## Arguments

| User says | Do this |
|-----------|---------|
| `/sync-events` | Run sync script against `../stylens` |
| `/sync-events ../path/to/stylens` | Alternate checkout path |

## Required reads

1. `context/analytics-events.md` (current)
2. `context/integrations.md` (App / stylens path)
3. `README.md` → Keeping analytics context fresh

## Steps

1. Confirm sibling app path exists (`../stylens` or user path).
2. Run: `./scripts/sync-event-taxonomy.sh <stylens-path>` from harness root.
3. Diff script output vs `context/analytics-events.md`.
4. Update taxonomy tables for **new** events/properties; preserve harness notes (e.g. `style_analysis_session_created` unreliable).
5. Summarize: added / changed / unchanged. Do not invent events not found in app code.

## Do not

- Modify Flutter app code here  
- Remove documented caveats without evidence  
- Commit secrets
