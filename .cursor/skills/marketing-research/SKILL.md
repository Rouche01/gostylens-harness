---
name: marketing-research
description: >-
  Spitball GoStylens marketing/growth ideas and get a data-backed verdict on
  whether each is a good experiment. Pulls PostHog, positioning, analytics
  events, and Notion Experiments; may compose other slash skills (funnel-diagnose,
  competitor-scan, aso-pulse, meta-ads-review, etc.) for evidence. Optionally
  creates Notion idea rows for keepers. Invoke with /marketing-research.
disable-model-invocation: true
---

# Marketing research (idea → experiment check)

Spitball workflow: you dump rough ideas → the agent grounds them in product data (and sibling skills when needed) and says **pursue / reshape / park / kill**.

This skill is an **orchestrator**: stay owned by `/marketing-research` for the verdict, but **read and follow other skills’ workflows** when they are the best way to gather evidence or draft a next step.

## When invoked

Follow `agents/marketing.md` → **Marketing research → idea check**. Do not invent product metrics or PostHog numbers.

**Always resolve:** (1) the user’s **idea(s)** (raw is fine), (2) a **goal** (default: acquisition), (3) lookback for PostHog (default: **14d**).

## Arguments

| User says | Do this |
|-----------|---------|
| `/marketing-research` | Ask them to spitball 1+ ideas (chat is fine; no polish required). |
| `/marketing-research <idea text…>` | Evaluate that idea (and any others in the message). |
| Multiple ideas in one message | Score each separately (max **5** per run; ask to prioritize if more). |
| `/marketing-research --goal acquisition` | Explicit TOF focus (default) |
| `/marketing-research --goal engagement` / `retention` / `monetization` | Goal lens for metrics + Domain(s) |
| `/marketing-research --goal <free text>` | Map to closest metric set; state mapping |
| `/marketing-research 30d …` | Override PostHog lookback |
| `/marketing-research --notion` | Create Notion `idea` rows only for **pursue** (and strong **reshape** if user agrees) — max **3** |
| `/marketing-research --dry-run` | Verdict only; never write Notion or `outputs/` |

### Examples

```text
/marketing-research what if we add an invite-a-friend after first style win
/marketing-research TikTok "rate my fit" hooks vs outcome-first closet hooks --goal acquisition
/marketing-research paywall after 3 analyses instead of 1 --goal monetization 30d
/marketing-research "ASO subtitle: snap outfit get feedback" --notion
```

## Goal → metrics

| Goal | Prefer Primary metrics | Notion Domain(s) |
|------|------------------------|------------------|
| **acquisition** (default) | `intro_started`, `intro_completed`, `auth_succeeded` (`is_new_user=true`) | `User Acquisition` |
| **engagement** | `ai_stream_completed`, `message_sent`, `asset_upload_completed` | `User Acquisition` and/or `Product Feature` |
| **retention** | Repeat `ai_stream_completed` / `message_sent` in 7d | `Product Feature` |
| **monetization** | `purchase_started`, `purchase_completed` | `User Acquisition` and/or `Product Feature` |

## Required reads / data pulls

Do these **before** giving a verdict (compose skills below when a pull is deeper than a quick PostHog query):

1. `context/marketing/positioning.md` — ICP + voice fit  
2. `context/product.md` — can we ship this?  
3. `context/analytics-events.md` — exact measurable events  
4. **PostHog** — funnel/step rates, volumes, and any segment relevant to the idea (lookback from args; default 14d). Never guess.  
5. Notion **Experiments** — search for duplicates / near-duplicates  
6. `context/marketing/competitors.md` + recent `outputs/*competitor*` only if the idea is competitor-inspired  
7. Optional external check via **perplexity-search** when the idea needs market/channel context (not a substitute for PostHog)

## Compose with other skills

Read the target skill’s `SKILL.md` and run its steps **inline** (same turn) when needed for evidence or a follow-through draft. Note in the verdict which skills you used (`Used: /funnel-diagnose, /aso-pulse`).

| Need | Skill | How to use |
|------|-------|------------|
| Funnel drop / step rates unclear | `/funnel-diagnose` | Run the matching funnel + lookback; fold step rates into **Problem evidence**. Do **not** create its Notion rows unless user passed `--notion` here. |
| Idea is competitor-inspired or “like X does” | `/competitor-scan` | Scan the named rival (or priority directs) with the same `--goal`; use brief signals as Obs/Inf — still score for GoStylens fit. |
| ASO / store listing idea | `/aso-pulse` | Pull ASC engagement; use as evidence for listing/keyword hypotheses. |
| Meta / paid social idea | `/meta-ads-review` | Pair Meta insights with PostHog activation when the spitball is ads-related. |
| Need weekly health context | `/growth-digest` | Skim latest digest under `outputs/` or run a lightweight digest pass if none is recent (~7d). |
| Release-tied idea | `/release-snapshot` | Compare pre/post metrics when the idea depends on a ship. |
| Events missing / wrong names | `/sync-events` | Sync taxonomy from `stylens` before parking as “unmeasurable.” |
| Verdict = pursue and user wants copy variants | `/copy-draft` | After the verdict, draft 2–3 variants tied to the experiment (only if asked or clearly needed for the smallest test). |
| Verdict = pursue and user wants community post | `/community-draft` | Human-gated draft only — never auto-post. |
| Closing / reading a related past test | `/close-experiment` | Pull Result + Decision from Notion when judging novelty vs a finished test. |

**Do not recurse forever:** at most **two** sibling skill deep-dives per idea, then verdict. Prefer existing `outputs/` from those skills over re-running when fresh enough.

**Ownership:** `/campaign-ideas` and `/experiment-backlog` invent ideas from drops — do **not** replace this spitball flow with them. You may cite their Notion rows for novelty checks only.

## Evaluation rubric (score each idea)

Score **1–5** on each dimension (state why in one line):

| Dimension | Ask |
|-----------|-----|
| **Problem evidence** | Does PostHog (or clear qualitative) show a real gap this idea addresses? |
| **Goal fit** | Does it move the active goal’s primary metrics? |
| **ICP / brand fit** | Matches positioning + voice (not luxury gatekeeping, not hype)? |
| **Measurability** | Clear primary metric with exact event names we already track? |
| **Effort vs learning** | S/M/L effort justified by expected learning? |
| **Novelty** | Not a duplicate of a Notion idea / running experiment? |

**Verdict**

| Verdict | When |
|---------|------|
| **pursue** | Strong evidence + measurable + goal fit; propose experiment form |
| **reshape** | Core insight OK but scope/metric/channel wrong — give a sharper version |
| **park** | Interesting but weak evidence, wrong timing, or blocked on instrumentation |
| **kill** | Conflicts with brand/ICP, unmeasurable, duplicate, or data contradicts the premise |

Be opinionated. Spitballing works when weak ideas die quickly.

## Output (chat-first)

For each idea, reply with this structure (keep tight):

```markdown
### Idea: {one-line restatement}
**Verdict:** pursue | reshape | park | kill
**Scores:** evidence _/5 · goal _/5 · ICP _/5 · measurable _/5 · effort-learn _/5 · novelty _/5

**Observation (data)**
- PostHog: {exact numbers + events + lookback}
- Other: {Notion dupes / competitor note / external — labeled Obs vs Inf}
- Skills used: {/funnel-diagnose | none | …}

**Why this verdict**
{2–4 sentences}

**If pursue / reshape — experiment form**
- Hypothesis: …
- Channel & effort: …
- Primary metric: `{exact_event}` …
- Smallest test: …
```

Then a short **Run ranking**: ordered list of ideas you’d actually run first.

### Optional artifacts

1. If useful and not `--dry-run`: `outputs/YYYY-MM-DD-idea-check-{slug}.md` (same content).  
2. If `--notion`: only **pursue** (ask once before creating **reshape**); dedupe; `Status=idea`, Domain(s) from goal table, Priority P0/P1/P2 from scores, `template_id` `3cf3d958-f999-807b-9697-c7e052f6192f`; link output path under Assets / links.

## Do not

- Rubber-stamp ideas without PostHog (say what’s missing and **park** if blocked)  
- Invent events or fabricate conversion rates  
- Create Notion rows without `--notion` or an explicit ask (sibling skills inherit this flag)  
- Expand one spitball into a campaign plan — stay on experiment fitness; skills are for evidence + smallest-test drafts only  
- Auto-post or touch `stylens-ops`  
- Hand-wave “users probably want…” without data — label inference and down-score evidence  
- Dump full sibling-skill reports in chat — fold only the evidence needed for the verdict
