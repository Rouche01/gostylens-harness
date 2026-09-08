# Experiments backlog (Notion)

Canonical experiment backlog for GoStylens. **Notion is source of truth** for status and decisions. This harness proposes, measures (PostHog), and writes back — it does not maintain a parallel backlog in git.

## Connection

| Field | Value |
|-------|-------|
| **Database name** | Experiments |
| **Location** | GoStylens teamspace → **GoStylens** page |
| **Database URL** | https://www.notion.so/3cf3d958f9998087b60ccea1e848d2ad |
| **Database ID** | `3cf3d958-f999-8087-b60c-cea1e848d2ad` |
| **Data source** | `collection://3cf3d958-f999-80e1-871e-000bbf29ff5f` |
| **Default template** | `New Experiment` — id `3cf3d958-f999-807b-9697-c7e052f6192f` |
| **Access** | Notion MCP in Cursor |
| **Env** | `NOTION_EXPERIMENTS_DATABASE_ID=3cf3d958-f999-8087-b60c-cea1e848d2ad` |

Priority bias: **user acquisition first**. Prefer `Domain(s)` = `User Acquisition`, or both domains when product work clearly serves acquisition.

## Database properties (lean)

Only fields needed for board views / filters live as properties:

| Property | Type | Options |
|----------|------|---------|
| **Name** | Title | One-line idea |
| **Domain(s)** | Multi-select | `User Acquisition` · `Product Feature` (both = mixed) |
| **Status** | Select | `idea` → `planned` → `running` → `post-decision` |
| **Priority** | Select | `P0` · `P1` · `P2` |
| **Decision** | Select | `scale` · `iterate` · `kill` · `park` (set at `post-decision`) |

Everything else lives in the **page body** using the template below.

## Page body template

Notion default template **New Experiment** (`template_id`: `3cf3d958-f999-807b-9697-c7e052f6192f`) is already applied for UI creates.

**Agents creating rows via Notion MCP must pass that `template_id`** (do not paste a duplicate body). After the template loads, fill Goal / Hypothesis / Primary metric / etc. Reference structure:

```markdown
## Goal
…
```

(Full section list matches the Notion template: Goal, Hypothesis, Primary metric, Channel & effort, Execution plan, Assets / links, Result, Decision notes, Dates.)

Channel & effort meanings:

**Channel** — where this runs (pick one or more):
- `tiktok` / `instagram` — organic or paid social
- `aso` — App Store / Play Store listing & keywords
- `lp` — gostylens.app landing page
- `email` — lifecycle / launch emails
- `in-app` — paywall, onboarding, in-product prompts
- `other` — anything else (note what)

**Effort** — rough build cost:
- `S` — hours · `M` — days · `L` — week+

Example: Channel(s): tiktok, lp · Effort: M

## Lifecycle rules

1. **Before `running`**: properties set; page body has Goal, Hypothesis, Primary metric, and Execution plan.
2. **While `running`**: don’t change Goal / Primary metric; adjust plan only if needed; set Started in Dates.
3. **At `post-decision`**: set **Decision** property; fill Result, Decision notes, Ended in the page body.
4. Primary metric must use **exact event names** from `context/analytics-events.md`.

## Agent workflow

1. Read `context/marketing/positioning.md` and `context/analytics-events.md`.
2. Query PostHog for evidence.
3. Search Notion Experiments for duplicates.
4. Create/update rows via Notion MCP: use `template_id` `3cf3d958-f999-807b-9697-c7e052f6192f`, set lean properties, then fill the template sections.
5. Prefer `User Acquisition` unless asked otherwise.

## Setup checklist

- [x] Experiments DB under GoStylens
- [x] Lean property schema
- [x] Default Notion template **New Experiment** wired (`template_id` above)
- [x] Set `NOTION_EXPERIMENTS_DATABASE_ID` in local `.env`
- [x] Seed acquisition `idea` rows from current funnel gaps
