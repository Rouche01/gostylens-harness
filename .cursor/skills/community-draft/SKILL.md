---
name: community-draft
description: >-
  Draft GoStylens organic community replies/posts with intensity rules and
  scoring; produce human-gated drafts for stylens-ops — never auto-post. Invoke
  with /community-draft.
disable-model-invocation: true
---

# Community draft

## When invoked

Follow `agents/community.md`. Runtime posting stays in `../stylens-ops`.

## Arguments

| User says | Do this |
|-----------|---------|
| `/community-draft` | Ask for target (subreddit/thread/URL) or draft from user paste |
| `/community-draft reddit <sub or URL>` | Score + draft for that context |
| `/community-draft --notion` | Also create/update a User Acquisition experiment if this is a channel test |

## Required reads

1. `agents/community.md`
2. `context/marketing/positioning.md`
3. `context/product.md`
4. `context/integrations.md` → Ops (`stylens-ops`)
5. `context/experiments.md` (if `--notion`)

## Steps

1. Score opportunity 0–5 (problem fit, wants help, rules OK, freshness, value without app). Abort if score < 4.
2. Draft reply/post at intensity **0** or **1** by default; intensity **2** only if user asks and with disclose + UTM note.
3. Include abort/risk notes (self-promo bans, tone).
4. Output draft for human Approve/Edit/Abort (Telegram queue in ops — do not post).
5. Optional: save `outputs/YYYY-MM-DD-community-draft.md`.
6. If `--notion`: dedupe community experiments; idea row with PostHog metrics (`intro_started`, `auth_succeeded`, `ai_stream_completed`).

## Do not

- Auto-post, vote manipulate, multi-account, or karma farm  
- Ship Telegram/Reddit executor code in this repo  
- Commit Reddit/Telegram secrets
