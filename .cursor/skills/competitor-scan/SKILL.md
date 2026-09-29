---
name: competitor-scan
description: >-
  Run a GoStylens competitor marketing/growth scan: research watchlist rows,
  write dated briefs under outputs/, propose acquisition experiments, optionally
  create Notion idea rows. Invoke with /competitor-scan or when the user asks
  to scan competitors.
disable-model-invocation: true
---

# Competitor scan

Manual slash workflow for GoStylens competitive intel → experiment ideas.

## When invoked

Follow `agents/marketing.md` → **Competitor scan → experiments**. Do not invent product metrics.

## Arguments (from user message)

| User says | Do this |
|-----------|---------|
| `/competitor-scan` (no args) | Scan **priority directs** from `context/marketing/competitors.md` (Lekondo → Acloset → Alta), or any with stale `Last reviewed` (>30 days). Max **3** competitors. |
| `/competitor-scan Lekondo` | Deep brief for that name only. |
| `/competitor-scan Lekondo Acloset` | Those names only (max 3). |
| `/competitor-scan --notion` | Also create Notion Experiments `idea` rows (default: briefs + candidates only unless user asks for Notion). |
| `/competitor-scan monthly` | Re-scan watchlist rows with oldest `Last reviewed`; update dates; ≤5 Notion ideas if `--notion` or user asks. |

## Required reads

1. `context/marketing/competitors.md`
2. `context/marketing/positioning.md`
3. `context/analytics-events.md`
4. `context/experiments.md` (if creating Notion rows)
5. `agents/marketing.md` (brief structure + research tool chain)

## Research tool chain

1. **perplexity-search** first  
2. On failure / thin results → Cursor **WebSearch / WebFetch**; report `Failed: perplexity-search`  
3. **Browser MCP** only for deep dives (LP, App Store, paywall screenshots)

Label **observation** vs **inference**. Prefer recent sources.

## Outputs

1. Write `outputs/YYYY-MM-DD-competitor-{slug}.md` per the brief template in `agents/marketing.md`.
2. Set `Last reviewed` to today on scanned rows in `competitors.md`.
3. List experiment candidates with exact PostHog event names.
4. If Notion requested: search Experiments for duplicates; create `Status=idea`, `Domain(s)=User Acquisition`, Priority P1/P2, `template_id` `3cf3d958-f999-807b-9697-c7e052f6192f`; link brief path under Assets / links.
5. End with a short summary: who scanned, brief paths, top 3 transferable ideas.

## Do not

- Copy competitor strategies wholesale — filter through GoStylens ICP + positioning  
- Invent analytics events  
- Auto-post or touch `stylens-ops`  
- Maintain a parallel experiment backlog in git
