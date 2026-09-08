# GoStylens analytics event taxonomy

Synced from the `stylens` app repo. Update this file when new events ship, or run `scripts/sync-event-taxonomy.sh` (future).

Source: `stylens/lib/` — PostHog via `AnalyticsService`.

## Auth

| Event | Properties | Notes |
|-------|------------|-------|
| `auth_otp_requested` | — | User requested login OTP |
| `auth_succeeded` | `method`, `is_new_user` | Successful login/signup |
| `auth_error` | `method`, `error_code` | Auth failure |
| `auth_logout` | — | User signed out |

## Intro / onboarding

| Event | Properties | Notes |
|-------|------------|-------|
| `intro_started` | — | Walkthrough began |
| `intro_completed` | — | Walkthrough finished |
| `intro_skipped` | `slide_index` | User skipped early |

## Style analysis

| Event | Properties | Notes |
|-------|------------|-------|
| `style_analysis_session_created` | `session_id` | In app code — **not observed in PostHog** (0 events as of 2026-09-04). Do not use for funnels until fixed. |
| `ai_stream_started` | `session_id`, `context_mode` | AI response streaming started — **live** |
| `ai_stream_completed` | `session_id`, … | Stream finished successfully — **use as activation** |
| `ai_stream_failed` | `session_id`, … | Stream failed |
| `message_sent` | `session_id`, `user_role`, `has_text`, `has_images` | User message in a styling session — soft activation signal |

## Subscriptions (RevenueCat)

| Event | Properties | Notes |
|-------|------------|-------|
| `subscription_initialized` | `user_id`, `has_customer_info`, `offerings_count`, `active_subscriptions`, `has_core_plan` | RC SDK ready |
| `purchase_started` | `package`, `package_type`, `price`, `currency`, `revenue` | Paywall CTA tapped |
| `purchase_completed` | same as started | Successful purchase |
| `purchase_failed` | `error_code`, + purchase props | Failed (not cancelled) |
| `purchase_restored` | — | Restore succeeded |
| `purchase_restore_empty` | — | Nothing to restore |

## Asset upload

| Event | Properties | Notes |
|-------|------------|-------|
| `asset_upload_started` | — | Upload began |
| `asset_upload_completed` | — | Upload succeeded |
| `asset_upload_failed` | — | Upload failed |

## Account

| Event | Properties | Notes |
|-------|------------|-------|
| `account_deleted` | — | User deleted account |

## Suggested PostHog insights to create

1. **Onboarding funnel**: `intro_started` → `intro_completed` → `auth_succeeded`
2. **Activation funnel**: `auth_succeeded` → `ai_stream_completed` (prefer over dead `style_analysis_session_created`)
3. **Monetization funnel**: `ai_stream_completed` → `purchase_started` → `purchase_completed`
4. **D1/D7 retention** by `auth_succeeded` cohort
5. **Purchase conversion** by `package_type` and platform

## Query tips for agents

- Always filter by time range (last 7/30/90 days).
- Segment by `platform` (ios/android) for subscription events.
- Use `is_new_user` on `auth_succeeded` for acquisition vs. returning analysis.
- Session replay is enabled — link qualitative drops to funnel steps.
