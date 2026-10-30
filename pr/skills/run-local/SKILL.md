---
name: run-local
description: "Starts the application locally for development: detects the stack and services, prepares the environment, stops stale processes, starts databases, backends, and frontends in dependency order as background tasks, and verifies each responds. Use when the user asks to run, start, or restart the app or its services locally."
argument-hint: "[optional: specific instructions]"
---

# Run Local

Get the whole application running locally from a clean start, and prove it responds. For quickly seeing a single change in a running app, Claude Code's built-in `/run` may be enough; this skill sets up and restarts the full stack.

**Instructions**: $ARGUMENTS. Empty means start or restart everything. By default, restart: stop existing processes and start fresh, unless the instructions say otherwise ("just the frontend", "don't touch the database").

Local means local: never point at production databases or use production credentials, and never expose services publicly.

## 1. Understand the Project

Read the README, CLAUDE.md, and the latest snapshot if present. Identify the components: frontend (Next.js, Vite, ...), backend (FastAPI, Express, Django, ...), databases and caches (Postgres, Redis, ...), workers, and how they connect. Note monorepo workspaces (pnpm/npm/yarn workspaces, Turborepo, Nx). If the setup is unclear, ask how the user usually runs it.

## 2. Find the Run Commands

Prefer the project's own entry points, which encode its conventions:

1. A single command: `make dev`, `just dev`, `task dev`, `npm run dev:all`, `./dev.sh`, or a Compose file (`compose.yaml`, `docker-compose.dev.yml`).
2. Otherwise per component: `npm|pnpm|yarn|bun run dev`, `uv run uvicorn app.main:app --reload`, `uv run manage.py runserver`, `go run .`, `cargo run`.

## 3. Prepare the Environment

Each Bash tool call runs in a fresh shell, so activation (`source .venv/bin/activate`, `conda activate`) does not carry over. Run tools through their environment instead:

- **Python**: `uv sync` then `uv run ...` (uv projects); `poetry install` then `poetry run ...`; `.venv/bin/python ...`; `conda run -n {env} ...`.
- **Node**: use the lockfile's package manager (`pnpm-lock.yaml`, `yarn.lock`, `bun.lock`, else npm); install if `node_modules/` is missing; respect `.nvmrc`, `.node-version`, or `engines`.
- **Environment variables**: use `.env.local` / `.env.development` when present. If required variables are missing, list them (names only) and ask; never print secret values.

Ask before creating a new virtual environment or installing global tools.

## 4. Stop What Is Running

Find processes on the project's ports (from configuration or scripts; common: 3000, 5173, 8000, 8080, 5432) with `lsof -nP -iTCP:{port} -sTCP:LISTEN`, and running project containers with `docker compose ps`. Stop only processes that belong to this project; confirm before killing anything you did not start or cannot attribute.

## 5. Start in Dependency Order

1. Infrastructure: databases, caches, queues (Compose or local services). Apply pending migrations only after confirming with the user.
2. Backend services.
3. Frontend.

Start each long-running process with the Bash tool's `run_in_background` option. Before starting a dependent service, wait until its dependency is ready (port listening or health endpoint responding). Do the waiting with the Monitor tool, for example `until curl -sf http://localhost:8000/health; do sleep 1; done; echo ready`, rather than a foreground `sleep` loop, which blocks the session; a watch ends at its deadline, so start another if a service is slow. Read the background output for startup errors.

## 6. Verify

Confirm every service responds (`curl -sf` a health or root endpoint; for UIs, load the page). If something fails, read its logs and fix the cause (use `systematic-debugging` for anything non-obvious) before reporting.

## 7. Report

List each service with its URL or port and its background task, how to stop them (stop the background tasks; `docker compose down` for containers), and anything that needs the user's attention (missing variables, skipped migrations). If the project has no launch recipe for Claude Code's `/run` and `/verify` yet, mention that the user can run `/run-skill-generator` to record one.
