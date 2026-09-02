# GoStylens product context

## What GoStylens is

GoStylens is an AI-powered personal styling app. Users capture outfit photos, get style analysis and feedback from an AI stylist, and build a digital closet over time.

## Core user journey

1. **Intro walkthrough** — `intro_started` → `intro_completed`
2. **Auth** — email OTP (`auth_otp_requested` → `auth_succeeded`)
3. **Onboarding** — name, gender, preferences
4. **Home** — three tabs: Closet, Capture, History
5. **Capture** — take/upload outfit photos for analysis
6. **Style analysis** — streaming AI stylist session (`style_analysis_session_created`)
7. **Subscription** — RevenueCat paywall (`purchase_started` → `purchase_completed`)

## Key features

- **Capture** — photo-based outfit input with pose guidance
- **Style analysis** — conversational AI styling sessions with streaming responses
- **Closet** — saved looks and wardrobe management
- **History** — past styling sessions
- **Subscriptions** — core plan via RevenueCat (iOS + Android)

## Environments

| Env | API | Notes |
|-----|-----|-------|
| Staging | `stg-api.gostylens.app` | Pre-production testing |
| Production | `api.gostylens.app` | Live users |

## Tech stack

| Layer | Stack | Repo |
|-------|-------|------|
| Mobile app | Flutter (iOS + Android), RevenueCat, PostHog | `../stylens` |
| Landing page | Static site on Cloudflare Pages, PostHog | `../stylens-lp` |
| API | Cloudflare Workers, D1, R2, Supabase auth | `../stylens-lite-api` |
| Auth | Supabase | (via app + API) |
| Analytics | PostHog (`https://n.gostylens.com`) | shared across app + LP |

## Links

| What | Where |
|------|-------|
| App | `../stylens` → [Rouche01/stylens](https://github.com/Rouche01/stylens) |
| Landing page | `../stylens-lp` → [Rouche01/stylens-lp](https://github.com/Rouche01/stylens-lp) |
| API | `../stylens-lite-api` → [Rouche01/stylens-lite-api](https://github.com/Rouche01/stylens-lite-api) |
| This harness | `.` → local `gostylens-harness` |
| Website | [gostylens.app](https://gostylens.app) |
| PostHog | [n.gostylens.com](https://n.gostylens.com) |
