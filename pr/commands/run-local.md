---
description: Start and run the application locally for development with automatic environment setup
argument-hint: "[optional: specific instructions]"
---

# Run Local

Start and run the application locally for development and testing.

## Core Principles

- **Restart by default**: Kill existing processes and start fresh unless instructed otherwise
- **Abstract commands first**: Look for project-specific commands (make dev, npm run dev:all) before individual micro-commands
- **Environment setup**: Ensure virtual environments and dependencies are properly configured
- **Start in order**: Launch services in dependency order (database → backend → frontend)

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

1. Check for processes on common ports (3000, 3001, 5000, 8000, 8080, etc.)
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

**Priority 1 - Project-Specific Abstract Commands**:

Check these locations for commands that start everything at once:
- **Makefile**: `make dev`, `make run`, `make start`, `make local`, `make up`
- **package.json scripts**: `npm run dev:all`, `npm run start:all`, `npm run local`
- **Shell scripts**: `./run.sh`, `./start-local.sh`, `./dev.sh`, `scripts/dev.sh`
- **docker-compose**: `docker-compose up`
- **Task runners**: `task dev`, `just dev` (Taskfile.yml, Justfile)
- **README.md**: Check for documented "quick start" or "run locally" commands

**If you find an abstract command that handles all services, use that.**

**Priority 2 - Individual Commands** (fallback only):

```bash
# Node.js / JavaScript
npm run dev / npm start / yarn dev / pnpm dev

# Python
python manage.py runserver          # Django
flask run                           # Flask
uvicorn main:app --reload          # FastAPI
python app.py

# Docker
docker-compose up
docker-compose -f docker-compose.dev.yml up

# Go
go run . / go run main.go

# Rust
cargo run
```

---

## Phase 5: Environment Setup

**Goal**: Ensure correct environment is active before running

**Actions**:

**Python**:
- Check for `venv/`, `.venv/`, `env/` directories
- Check for `pyproject.toml` (Poetry), `Pipfile` (Pipenv), `requirements.txt`
- Activate the environment:
  ```bash
  source venv/bin/activate      # Standard
  source .venv/bin/activate
  poetry shell                  # Poetry
  pipenv shell                  # Pipenv
  ```
- If no virtual environment exists but dependencies are listed, ask user if they want to create one

**Node.js**:
- Check for `node_modules/` - if missing, run `npm install` or `yarn install` first
- Check for `.nvmrc` or `.node-version` for required Node version
- Use `nvm use` if version file exists

**Conda**:
- Check for `environment.yml` or `conda.yaml`
- Activate with: `conda activate <env-name>`

**Ruby**:
- Check for `Gemfile` - may need `bundle install`
- Check for `.ruby-version`

**Other**:
- Check for any environment setup scripts
- Look for documented setup in README.md

---

## Phase 6: Start Services

**Goal**: Launch services in correct dependency order

**Order** (if using individual commands):
1. **Database/Infrastructure first** (Docker containers, databases)
2. **Backend services** (API servers)
3. **Frontend** (dev server)

**For each service**:
- Start in background or separate terminal/process
- Wait for service to be ready before starting dependent services
- Capture and display startup logs

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
2. Inform user how to stop them later (e.g., "Run Ctrl+C in the terminal" or "docker-compose down")
3. If using multiple terminals, note which terminal has which service

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
- Prefer docker-compose for local development if configured
- Check for dev-specific compose files (docker-compose.dev.yml, docker-compose.local.yml)

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
