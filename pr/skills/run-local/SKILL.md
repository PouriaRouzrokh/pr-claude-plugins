---
name: run-local
description: "Starts the application locally for development: detects the stack, prepares the environment, restarts services in dependency order as background tasks, and verifies they respond. Use when the user asks to run, start, or restart the app locally."
argument-hint: "[optional: specific instructions]"
---

# Run Local

Start and run the application locally for development and testing.

## Core Principles

- **Restart by default**: Kill existing processes and start fresh unless instructed otherwise.
- **Abstract commands first**: Look for project commands (`make dev`, `npm run dev:all`) before individual commands.
- **Environment setup**: Configure virtual environments and dependencies.
- **Start in order**: Database → backend → frontend.

---

## Phase 0: Parse Instructions

**Goal**: Understand what to run

**Arguments**: $ARGUMENTS

- **Free text instructions**: Specific guidance on what to run or how to run it
- **If empty**: Run/restart all application components locally

**Default behavior**: Always restart (kill existing processes and start fresh) unless the user's instructions indicate otherwise (e.g., "just start the frontend" or "don't restart the database").

---

## Phase 1: Project Analysis

**Goal**: Identify what type of project this is and what needs to run

**Actions**:

1. **Identify project type** by looking for:

   **Web Applications** (most common):
   - Frontend: React, Vue, Angular, Next.js, Svelte (package.json with dev scripts)
   - Backend: Node/Express, Python/Flask/Django/FastAPI, Go, Rust
   - Database: PostgreSQL, MySQL, MongoDB, Redis (docker-compose, .env files)
   - Other services: Message queues, caching layers

   **Other Application Types**:
   - CLI tools: May just need compilation/build
   - Mobile apps: May need emulators or device connections
   - Desktop apps: May need specific build/run commands
   - Monorepos: May have multiple packages that need to run

2. If the project type is unclear, **ask the user** for clarification

---

## Phase 2: Check Running Processes

**Goal**: Identify what's already running

**Actions**:

1. Check for processes on the ports the project uses (from config, `.env`, or scripts), falling back to common ports (3000, 3001, 5000, 5173, 8000, 8080). On macOS/Linux: `lsof -nP -iTCP:<port> -sTCP:LISTEN`
2. Check for running Docker containers related to the project
3. Check for any background processes from previous runs

---

## Phase 3: Stop Existing Processes

**Goal**: Ensure a fresh start (default behavior)

**Actions**:

1. Stop any running dev servers (frontend, backend)
2. Stop Docker containers if using Docker
3. Kill processes on the ports that will be needed
4. **Be careful not to kill unrelated system processes**

---

## Phase 4: Identify Run Commands

**Goal**: Find the best way to start the application

**Priority 1 - Abstract Commands** (use if available):
- Makefile: `make dev`, `make run`, `make start`
- package.json: `npm run dev:all`, `npm run local`
- Shell scripts: `./run.sh`, `./dev.sh`
- docker-compose, task runners (Taskfile.yml, Justfile)

**Priority 2 - Individual Commands** (fallback):
- Node: `npm run dev`, `pnpm dev`, `yarn dev`, `bun dev`
- Python: `uv run manage.py runserver`, `uv run flask run`, `uv run uvicorn main:app --reload` (or the venv equivalents)
- Docker: `docker compose up -d`
- Go: `go run .`
- Rust: `cargo run`

---

## Phase 5: Environment Setup

**Goal**: Use the correct environment for every command

Each Bash tool call runs in a fresh shell, so `source .venv/bin/activate` or `conda activate` does not persist to the next call. Invoke the environment's tools directly instead.

**Python**:
- `uv.lock` or `[tool.uv]` in `pyproject.toml` → `uv sync`, then `uv run <cmd>`
- `poetry.lock` → `poetry install`, then `poetry run <cmd>`
- `.venv/` or `venv/` → call `.venv/bin/python`, `.venv/bin/uvicorn`, etc. directly
- `environment.yml` → `conda run -n <env> <cmd>`

**Node.js**: Pick the package manager from the lockfile (`pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lock`/`bun.lockb` → bun, otherwise npm). Install if `node_modules/` is missing. Check `.nvmrc` / `.node-version` / `engines` for the required Node version.

**Ruby**: Check `Gemfile`, run `bundle install` if needed, then `bundle exec <cmd>`.

If no environment exists, ask the user before creating one.

---

## Phase 6: Start Services

**Goal**: Launch services in correct dependency order

**Order** (if using individual commands):
1. **Database/Infrastructure first** (Docker containers, databases)
2. **Backend services** (API servers)
3. **Frontend** (dev server)

**For each service**:
- Start long-running processes with the Bash tool's `run_in_background` option so they survive and don't block the session
- Wait for each service to be ready (port listening or health endpoint responding) before starting services that depend on it
- Read the background output to surface startup errors

---

## Phase 7: Verification

**Goal**: Confirm everything is running

**Actions**:

1. Check that all expected ports are listening
2. Verify services respond (quick health checks if available)
3. Report the URLs where the user can access the application

**Example output**:
```
Database running on localhost:5432
Backend API running on http://localhost:8000
Frontend running on http://localhost:3000
```

---

## Phase 8: Summary

**Goal**: Inform user of status and next steps

**Actions**:

1. List all running services with their URLs/ports
2. Tell the user how to stop them later (background tasks can be stopped from Claude Code's task list; Docker services with `docker compose down`)
3. Note which background task runs which service

---

## Environment Considerations

- Use `.env.local` or `.env.development` if they exist
- **DO NOT** use production environment variables
- Ensure local database connections, not production
- Check for any required API keys or secrets for local development

---

## Special Cases

### Monorepo Projects
- May need to run multiple packages
- Check for workspace configurations (npm workspaces, yarn workspaces, turborepo, nx)
- Start services from correct directories

### Projects with Docker
- Prefer Docker Compose for local development if configured
- Check for dev-specific compose files (`compose.yaml`, `docker-compose.dev.yml`, `docker-compose.local.yml`)

### Projects Without Clear Run Commands
- Ask the user how they typically run the project locally
- Check README.md for instructions

---

## Safety Guidelines

**DO NOT:**
- Use production environment variables or connect to production databases
- Expose services publicly (this is for LOCAL testing only)
- Run destructive commands (database migrations without confirmation)
- Leave orphaned processes running without informing the user
