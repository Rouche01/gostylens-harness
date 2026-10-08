---
name: meta-ads-review
description: >-
  Pull Meta Ads insights via harness script and pair with PostHog activation
  metrics for GoStylens acquisition review. Invoke with /meta-ads-review.
disable-model-invocation: true
---

# Meta ads review

## When invoked

Run `./scripts/meta-ads-insights.sh`, then interpret with PostHog. See `context/integrations.md` → Meta Ads.

## Arguments

| User says | Do this |
|-----------|---------|
| `/meta-ads-review` | `last_7d` at **campaign** level |
| `/meta-ads-review last_14d` / `last_30d` | That date preset |
| `/meta-ads-review … adset` / `ad` | Level override |
| `/meta-ads-review --notion` | Optional Notion `idea` if clear creative/targeting gap |

## Required reads

1. `context/integrations.md` (Meta section)
2. `context/analytics-events.md`
3. `.env` presence for `META_ACCESS_TOKEN`, `META_AD_ACCOUNT_ID` (do not print secrets)

## Steps

1. Run: `./scripts/meta-ads-insights.sh [date_preset] [level]` from repo root; capture JSON/output under `outputs/` if the script writes there, else summarize from stdout.
2. Report spend, clicks, CPC, CTR by campaign/adset/ad.
3. If `APPSFLYER_API_TOKEN` is set: run `./scripts/appsflyer-pull.sh <from> <to> both facebook` for the same window; report AF installs + `af_complete_registration` / `af_activation`. Prefer AF install CPI over Meta’s lagged iOS install column.
4. Query PostHog same window: `auth_succeeded` (new), `ai_stream_completed` — note Meta cannot show true activation alone.
5. Observations vs hypotheses; flag wasted spend or strong CTR/weak activation.
6. Optional: `outputs/YYYY-MM-DD-meta-ads-review.md`.
7. If `--notion`: dedupe; ≤2 acquisition `idea` rows with Primary metric including PostHog activation.

## Do not

- Commit tokens or dump full `.env`  
- Optimize only on Meta CTR without product events  
- Change live Meta campaigns (review only unless user asks)
