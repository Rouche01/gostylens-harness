---
name: competitor-scan
description: >-
  Run a GoStylens competitor marketing/growth scan with an optional goal lens
  (acquisition/top-of-funnel, engagement, retention, monetization). Research
  watchlist rows, write dated briefs under outputs/, propose experiments, optionally
  create Notion idea rows. Invoke with /competitor-scan.
disable-model-invocation: true
---

# Competitor scan

Manual slash workflow for GoStylens competitive intel → experiment ideas.

## When invoked

Follow `agents/marketing.md` → **Competitor scan → experiments**. Do not invent product metrics.

**Always resolve a goal** (default: acquisition / top-of-funnel). Research depth, transferable bullets, and experiment candidates must optimize for that goal — not a generic “everything they do” dump.

## Arguments (from user message)

Combine freely: names + goal + flags.

| User says | Do this |
|-----------|---------|
| `/competitor-scan` | Goal = **acquisition** (default). Scan priority directs (Lekondo → Acloset → Alta) or stale `Last reviewed` (>30 days). Max **3**. |
| `/competitor-scan Lekondo` | Deep brief for that name only (default goal). |
| `/competitor-scan Lekondo Acloset` | Those names only (max 3). |
| `/competitor-scan --goal acquisition` | Explicit top-of-funnel / user acquisition focus |
| `/competitor-scan --goal engagement` | Activation / habit / in-product engagement focus |
| `/competitor-scan --goal retention` | Return / D7 / repeat-use focus |
| `/competitor-scan --goal monetization` | Trial, paywall, freemium → paid focus |
| `/competitor-scan --goal <free text>` | Custom goal (e.g. `--goal organic APAC growth`); map to closest metric set below |
| Shortcuts | `--goal tof` / `top-of-funnel` → acquisition; `activation` → engagement |
| `/competitor-scan --notion` | Also create Notion Experiments `idea` rows |
| `/competitor-scan monthly` | Re-scan oldest `Last reviewed`; ≤5 Notion ideas if `--notion` |

### Examples

```text
/competitor-scan --goal acquisition --notion
/competitor-scan Lekondo Alta --goal engagement
/competitor-scan --goal retention monthly --notion
/competitor-scan --goal "get as many new installs as possible"
```

## Goal lenses

State the active goal at the top of every brief and in the chat summary.

| Goal | Research bias (what to hunt) | Prefer Primary metrics | Notion Domain(s) |
|------|------------------------------|------------------------|------------------|
| **acquisition** (default) | ASO, LP, paid/organic channels, referral, creative hooks, install CTAs, freemium top-of-funnel | `intro_started`, `intro_completed`, `auth_succeeded` (`is_new_user=true`) | `User Acquisition` |
| **engagement** | Onboarding to first value, habit loops, challenges, occasion prompts, chat/stylist UX, notifications | `ai_stream_completed`, `message_sent`, `asset_upload_completed` | `User Acquisition` and/or `Product Feature` |
| **retention** | Calendars, OOTD logging, communities/lookbooks, re-engagement, wear tracking | Repeat `ai_stream_completed` / `message_sent` in 7d; cohort return after `auth_succeeded` | `Product Feature` (add `User Acquisition` if re-install/win-back) |
| **monetization** | Trial length, paywall timing, item caps, premium features, pricing pages | `purchase_started`, `purchase_completed` (after `ai_stream_completed` when relevant) | `User Acquisition` and/or `Product Feature` |

Still capture other signals briefly under secondary headings, but **What’s transferable** and **Experiment candidates** must be goal-first (2–3 ideas that serve the goal).

## Required reads

1. `context/marketing/competitors.md`
2. `context/marketing/positioning.md`
3. `context/analytics-events.md`
4. `context/experiments.md` (if creating Notion rows)
5. `agents/marketing.md` (brief structure + research tool chain)

## Research tool chain

1. **perplexity-search** first (queries should include the goal, e.g. “Lekondo user acquisition growth referral”)  
2. On failure / thin results → Cursor **WebSearch / WebFetch**; report `Failed: perplexity-search`  
3. **Browser MCP** only for deep dives (landing page, App Store, paywall screenshots)

Label **observation** vs **inference**. Prefer recent sources.

## Outputs

1. Write `outputs/YYYY-MM-DD-competitor-{slug}.md` (include **Goal** in the brief header).
2. Set `Last reviewed` to today on scanned rows in `competitors.md`.
3. List experiment candidates aimed at the goal, with exact PostHog event names.
4. If Notion requested: search Experiments for duplicates; create `Status=idea` rows with Domain(s) from the goal table, Priority P1/P2, `template_id` `3cf3d958-f999-807b-9697-c7e052f6192f`; link brief path under Assets / links; put goal in Goal/Hypothesis.
5. End with a short summary: **goal**, who scanned, brief paths, top 3 transferable ideas for that goal.

## Do not

- Copy competitor strategies wholesale — filter through GoStylens ICP + positioning + **active goal**  
- Propose retention experiments when the user asked for acquisition (unless clearly dual-purpose and labeled secondary)  
- Invent analytics events  
- Auto-post or touch `stylens-ops`  
- Maintain a parallel experiment backlog in git
