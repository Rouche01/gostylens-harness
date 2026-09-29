---
name: aso-pulse
description: >-
  Pull App Store Connect engagement via harness script, summarize vs prior
  outputs, and optionally propose Notion ASO experiment ideas. Invoke with
  /aso-pulse.
disable-model-invocation: true
---

# ASO pulse

## When invoked

Run `./scripts/asc-analytics.sh`, interpret engagement, compare to recent `outputs/` ASC/ASO artifacts. See `context/integrations.md` → App Store Connect.

## Arguments

| User says | Do this |
|-----------|---------|
| `/aso-pulse` | Pull latest ASC engagement; summarize |
| `/aso-pulse --list-apps` | Run `./scripts/asc-analytics.sh --list-apps` only |
| `/aso-pulse --notion` | Propose/create ≤2 ASO Notion `idea` rows if conversion/impressions warrant |

## Required reads

1. `context/integrations.md` (ASC section)
2. `context/marketing/positioning.md` (for keyword/voice context)
3. `context/analytics-events.md` (pair with `auth_succeeded` if useful)
4. Recent files under `outputs/` matching `asc-analytics` / `aso`

## Steps

1. Ensure `.venv` deps if needed (PyJWT, cryptography) per integrations.md — do not invent setup beyond docs.
2. Run `./scripts/asc-analytics.sh` (note Apple lag 1–2 days).
3. Summarize product page views / impressions / engagement from pulled TSVs or summary JSON.
4. Compare to prior snapshot in `outputs/` if present.
5. Optional PostHog: organic-ish `auth_succeeded` trend same period (directional only).
6. Write `outputs/YYYY-MM-DD-aso-pulse.md`.
7. If `--notion`: dedupe (e.g. existing ASO title/subtitle experiment); create or update ideas with channel `aso`.

## Do not

- Treat ASC as live clickstream  
- Print private key material  
- Ship App Store Connect metadata changes from this skill (draft recommendations only)
