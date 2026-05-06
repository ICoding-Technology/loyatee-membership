# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository layout

Two independent sub-projects in this monorepo, each with its own dependencies and tooling:

- `api/` — Flask 3 + ArangoDB + Redis backend (Python 3.12, Gunicorn, Docker Compose).
- `webpage/` — Nuxt 4 frontend (Vue 3, Nuxt UI, Tailwind, `bun.lock` is committed).

There is no top-level package manager or build orchestration — run commands from inside `api/` or `webpage/`.

## Common commands

### Backend (`api/`)

```bash
cp .env.example .env                  # first-time setup
docker compose up --build             # run API + ArangoDB together
docker compose down -v                # stop and wipe DB volume
```

- API listens on **http://localhost:5001** (host) → 5000 inside the container.
- ArangoDB web UI: **http://localhost:8529** (user `root`, password from `.env`).
- The Flask app entrypoint is `wsgi.py` → `create_app()` (factory pattern). To run without Docker: `pip install -r requirements.txt && python wsgi.py` (requires reachable ArangoDB and Redis).
- Hot reload is enabled in dev: the compose file bind-mounts `./:/app` and runs Gunicorn with `--reload`. Code edits on the host trigger a worker reload — no rebuild needed. Rebuild only when `requirements.txt` or `Dockerfile` changes (`make build`).
- There are no tests or linters configured in the API project yet.

### Frontend (`webpage/`)

`bun.lock` is the source of truth — prefer `bun install` / `bun run dev`. The README uses `npm` but the lockfile is bun's.

```bash
bun install                           # or: npm install
bun run dev                           # http://localhost:3000
bun run build                         # production build
bun run generate                      # static site generation
bun run preview                       # preview prod build
```

No test runner or linter is configured in `webpage/` either.

## Architecture

### API — layered Flask app

Request flow: `routes/*` (blueprint, thin) → `controllers/*` (validation, errors, orchestration) → `models/*` (AQL queries against ArangoDB).

- `app/__init__.py::create_app` is the factory: loads config, enables CORS, calls `init_db`, registers blueprints + error handlers.
- `app/extensions.py` owns the ArangoDB client. `init_db` creates the `loyatee` database if missing, the `members` collection, and a **unique hash index on `phone`**. `get_db()` caches the DB handle on Flask's `g` per request.
- Blueprints are mounted in `app/routes/__init__.py`:
  - `health_bp` → `/health`
  - `auth_bp` → `/api/auth` (`/request-otp`, `/verify-otp`, `/google`, `/telegram`)
  - `members_bp` → `/api/members` (CRUD, `<member_id>` is the Arango `_key`)
- Errors are raised as typed exceptions (`BadRequest`, `Unauthorized`, `NotFound`, `Conflict`) from `controllers/errors.py` and converted to JSON by `register_error_handlers`.

**Member document shape** (see `models/member.py`): `_key`, `phone`, `name`, `email`, `avatar_url`, `google_id`, `telegram_id`, `points` (int, default 0), `created_at`, `updated_at` (UTC ISO). `phone`, `google_id`, and `telegram_id` each have **sparse unique** indexes (created in `extensions.py::_ensure_unique_index`) so a member can be identified by any of them but isn't required to have all. `_serialize` renames `_key` → `id`; `update()` only patches `phone`/`name`/`email`/`avatar_url`/`points`.

**Auth is partially stubbed:**
- OTPs are stored in Redis under key `otp:<phone>` with a TTL from `OTP_TTL_SECONDS` (default 300). Initialized in `app/extensions.py::init_redis`, accessed via `get_redis()`.
- `request-otp` still returns the OTP in the response as `otp_debug` for testing — gate behind `app.debug` before deploying.
- `verify-otp`, `/google`, `/telegram` all return the literal string `"stub-token"` — no JWT yet.
- `/google` verifies the Google ID token via `google-auth` (requires `GOOGLE_CLIENT_ID`), then find-or-creates a member by `google_id`, falling back to `email` match.
- `/telegram` verifies the Telegram Login Widget HMAC signature against `SHA256(TELEGRAM_BOT_TOKEN)` per https://core.telegram.org/widgets/login#checking-authorization, then find-or-creates by `telegram_id`. Auth payloads older than `TELEGRAM_AUTH_MAX_AGE` (default 86400s) are rejected.

When extending auth, the stub token is the next thing to replace.

### Frontend — Nuxt 4 SPA-style app

- `app.vue` wraps everything in `<UApp>` (Nuxt UI) and renders `<NuxtPage />`. Routing is file-based via `pages/`.
- `pages/` covers the membership flow: `index`, `login`, `register`, `otp-verify`, `term`, `privacy`, `home`, `detail`, `card-detail`, `edit-profile`, `change-password`.
- `components/` is flat (no subdirectories) — reusable form primitives (`Button`, `TextField`, `FormField`, `ErrorMessage`, `FormPageLayout`), layout (`Header`, `NavBar`, `BottomNavigation`, `BottomNavItem`), and feature components (`MembershipCard`, `MyQR`, `TransactionList`, `TransactionItem`, `TotalPoint`, `ProfileInfo`, `SettingsMenu`).
- Styling: Tailwind + Nuxt UI, with theme tokens defined as CSS variables in `assets/css/main.css` (`--color-primary: #4169E1` royal blue, plus text/border/error tokens). Body font is Quicksand; `.font-number` switches to Manrope. Both are loaded from Google Fonts via `nuxt.config.ts`.
- The frontend does **not** currently call the Flask API — there is no `useFetch`/API client wired up. Adding one means pointing at `http://localhost:5001` and handling CORS (already enabled globally on the API).

## Environment variables (`api/.env`)

`FLASK_ENV`, `FLASK_DEBUG`, `SECRET_KEY`, `PORT`, `ARANGO_URL`, `ARANGO_DB`, `ARANGO_USER`, `ARANGO_PASSWORD`, `REDIS_URL`, `OTP_TTL_SECONDS`, `GOOGLE_CLIENT_ID`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_AUTH_MAX_AGE`. Defaults in `config.py` assume local dev (`http://localhost:8529`, `redis://localhost:6379/0`, db `loyatee`, user `root`, OTP TTL 300s, social-sign-in disabled). Inside Docker Compose, `ARANGO_URL` and `REDIS_URL` are overridden to the in-network hostnames (`http://arangodb:8529`, `redis://redis:6379/0`).

The frontend reads `NUXT_PUBLIC_GOOGLE_CLIENT_ID` and `NUXT_PUBLIC_TELEGRAM_BOT_NAME` from the environment (exposed via `runtimeConfig.public` in `nuxt.config.ts`); when empty, the social-sign-in section on `/login` falls back to a hint message instead of rendering empty widgets.
