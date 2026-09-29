---
name: close-experiment
description: >-
  Close a GoStylens Notion experiment with PostHog evidence: fill Result and
  Decision notes, set Decision property (scale/iterate/kill/park). Invoke with
  /close-experiment.
disable-model-invocation: true
---

# Close experiment

## When invoked

Follow `agents/growth-analyst.md` → **Closing experiments**.

## Arguments

| User says | Do this |
|-----------|---------|
| `/close-experiment <Notion URL or name>` | Required — which experiment |
| `/close-experiment … scale` | Recommend/set Decision = scale (still verify with data) |
| `/close-experiment … iterate` / `kill` / `park` | Same for other decisions |

If Decision not given, recommend one from the numbers and ask before setting if ambiguous.

## Required reads

1. Fetch the Notion experiment page (Goal, Hypothesis, Primary metric, dates)
2. `context/analytics-events.md`
3. `context/experiments.md`
4. Query PostHog for the Primary metric over the experiment window

## Steps

1. Resolve experiment page; confirm Status and Primary metric events.
2. Query PostHog for the stated window (or Started→Ended / last 14–30d if blank).
3. Fill page body **Result** with numbers (+ optional insight URL).
4. Fill **Decision notes** (why).
5. Set **Decision** property: `scale` | `iterate` | `kill` | `park`.
6. Set **Status** = `post-decision`; set Ended date if present in Dates.
7. Summarize outcome in chat (2–3 sentences).

## Do not

- Change Goal / Primary metric while closing  
- Close without PostHog (or explicit user waiver that data is unavailable)  
- Invent metrics not in the experiment
