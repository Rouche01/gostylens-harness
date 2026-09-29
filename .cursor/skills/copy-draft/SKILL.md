---
name: copy-draft
description: >-
  Draft GoStylens marketing copy (ASO, social, email) with 2–3 variants matching
  positioning voice; optionally link to a Notion experiment. Invoke with /copy-draft.
disable-model-invocation: true
---

# Copy draft

## When invoked

Follow `agents/marketing.md` → **Copy drafts**. Match brand voice from positioning.

## Arguments

| User says | Do this |
|-----------|---------|
| `/copy-draft aso` | App Store title/subtitle/description or screenshot captions (ask which if unclear) |
| `/copy-draft social` | TikTok/IG/organic hooks (2–3 variants) |
| `/copy-draft email` | Lifecycle/activation email draft(s) |
| `/copy-draft lp` | Landing page hero / CTA variants |
| `/copy-draft … --experiment <URL>` | Tie to Notion experiment; update that page Assets if useful |

## Required reads

1. `context/marketing/positioning.md`
2. `context/product.md`
3. `agents/marketing.md`
4. Optional: PostHog snippet if copy targets a known funnel drop

## Steps

1. Clarify channel + constraint (character limits for ASO).
2. Produce **2–3 variants** with rationale (why this might move the metric).
3. Note primary metric to watch (exact event names).
4. Optional: save to `outputs/YYYY-MM-DD-copy-{channel}.md`.
5. If `--experiment`: add best variant note under Assets / links on that Notion page.

## Do not

- Hypey / judgmental tone  
- Claim unverified user counts or press  
- Ship live App Store changes (draft only unless user asks to apply elsewhere)
