---
description: Deploy and run the application publicly for testing or production use
argument-hint: "[optional: specific instructions]"
---

# Run Public

Deploy and run the application publicly (internet-accessible) for testing or production use.

## Core Principles

- **Restart by default**: Redeploy fresh unless instructed otherwise
- **Abstract commands first**: Look for project-specific deploy commands before platform-specific commands
- **Verify before and after**: Confirm environment configuration and deployment success
- **Never expose secrets**: Never log or display credentials in output

---

## Phase 0: Parse Instructions

**Goal**: Understand deployment request

**Arguments**: $ARGUMENTS

- **Free text instructions**: Specific guidance on what to deploy or how to deploy it
- **If empty**: Deploy/restart all application components publicly

**Default behavior**: Always restart (kill existing public instances and redeploy fresh) unless the user's instructions indicate otherwise.

---

## Phase 1: Project Analysis

**Goal**: Identify deployment setup and method

**Actions**:

1. **Determine application type and deployment method**

2. **Common Deployment Patterns**:

   **Cloud Platforms**:
   - Vercel (Next.js, frontend)
   - Netlify (static sites, frontend)
   - Railway, Render, Fly.io (full-stack)
   - Heroku
   - AWS (EC2, ECS, Lambda, Amplify)
   - Google Cloud (Cloud Run, App Engine)
   - Azure

   **Container-based**:
   - Docker + cloud VM
   - Kubernetes
   - Docker Compose on a server

   **Traditional**:
   - VPS with nginx/Apache
   - PM2 for Node.js processes
   - systemd services

---

## Phase 2: Find Deployment Commands

**Goal**: Identify the best way to deploy

**Priority 1 - Project-Specific Deployment Commands**:

Check these locations for commands that handle the entire deployment:
- **Makefile**: `make deploy`, `make deploy-prod`, `make release`, `make publish`
- **package.json scripts**: `npm run deploy`, `npm run deploy:prod`, `npm run release`
- **Shell scripts**: `./deploy.sh`, `./release.sh`, `scripts/deploy.sh`, `scripts/deploy-prod.sh`
- **Task runners**: `task deploy`, `just deploy` (Taskfile.yml, Justfile)
- **CI/CD triggers**: May just need to push to main or create a tag

**If you find an abstract deployment command, use that.**

**Priority 2 - Platform Configuration Files** (fallback):

Look for deployment configuration in:
- `vercel.json`, `netlify.toml`
- `fly.toml`, `railway.json`, `render.yaml`
- `Dockerfile`, `docker-compose.prod.yml`
- `.github/workflows/` (CI/CD pipelines)
- `Procfile` (Heroku)
- README.md deployment instructions

---

## Phase 3: Check Current Status

**Goal**: Understand current deployment state

**Actions**:

1. Check if services are currently running publicly
2. Identify what URLs/endpoints are active
3. Check deployment platform status (if using managed platforms)

---

## Phase 4: Environment Verification

**Goal**: Ensure production environment is properly configured

**Actions**:

1. Verify `.env.production` or production environment variables are set
2. Check that production database URLs are configured
3. Verify API keys and secrets are available for production
4. **NEVER log or expose secrets in output**

---

## Phase 5: Environment Setup

**Goal**: Prepare build environment

**Actions**:

**Python**:
- Activate virtual environment: `source venv/bin/activate`, `poetry shell`, `pipenv shell`
- Ensure dependencies are installed: `pip install -r requirements.txt`, `poetry install`, `pipenv install`
- For production: may need `--production` flag or exclude dev dependencies

**Node.js**:
- Ensure `node_modules/` exists: `npm ci` (preferred for CI/CD) or `npm install`
- Check for correct Node version (`.nvmrc`, `.node-version`)

**Other Languages**:
- Ensure dependencies are installed and environment is configured
- Check for setup scripts or documented setup procedures

---

## Phase 6: Build for Production

**Goal**: Create production build

**Actions**:

Most applications need a production build:

```bash
# Node.js / JavaScript
npm run build / yarn build / pnpm build

# Python
python manage.py collectstatic  # Django (static files)

# Go
go build -o app .

# Rust
cargo build --release
```

---

## Phase 7: Deploy

**Goal**: Execute the deployment

**Actions** (if no abstract deploy command was found):

**Managed Platforms**:
```bash
# Vercel
vercel --prod

# Netlify
netlify deploy --prod

# Railway
railway up

# Fly.io
fly deploy

# Heroku
git push heroku main
```

**Docker-based**:
```bash
# Build and push image
docker build -t app:latest .
docker push registry/app:latest

# On server
docker-compose -f docker-compose.prod.yml up -d
```

**Manual/SSH**:
- May need to SSH into server
- Pull latest code
- Restart services (PM2, systemd, etc.)

---

## Phase 8: Verification

**Goal**: Confirm deployment success

**Actions**:

1. Wait for services to be healthy
2. Check public URLs are accessible
3. Run basic health checks
4. Verify the deployment completed successfully

**Report to user**:
```
Frontend deployed to https://myapp.vercel.app
Backend API running at https://api.myapp.com
All health checks passing
```

---

## Phase 9: Summary

**Goal**: Provide access information and next steps

**Actions**:

Give the user:
- Public URLs where they can access the application
- Any relevant dashboard links (Vercel dashboard, etc.)
- How to monitor logs or check status
- How to rollback if needed

---

## Special Cases

### Monorepo with Multiple Deployables
- Deploy services in correct order (backend before frontend if frontend depends on API URL)
- Track deployment status of each component

### Preview/Staging vs Production
- If the project has staging environments, ask user which environment to deploy to
- Be extra careful with production deployments

### First-time Deployment
- May need additional setup (create project on platform, configure domains, etc.)
- Guide user through initial setup if needed
- Ask for confirmation before creating new resources

### CI/CD Pipelines
- If the project uses CI/CD, may just need to trigger the pipeline
- Could be: push to main branch, create a release, trigger GitHub Action manually

---

## Safety Guidelines

**DO NOT:**
- Deploy without verifying production environment configuration
- Expose secrets or credentials in logs or output
- Deploy to production without user awareness (confirm if deploying to prod vs staging)
- Skip build steps that are necessary
- Leave the application in a broken state (rollback if deployment fails)

**ALWAYS:**
- Verify deployment succeeded before reporting success
- Provide rollback instructions if something goes wrong
- Warn if deploying will cause downtime
- Ask for confirmation for destructive operations (database migrations, etc.)
- Ensure the user knows the public URLs

---

## If Deployment Method is Unclear

If you cannot determine how the project should be deployed publicly:
1. Check README.md for deployment instructions
2. Look for any deployment configuration files
3. Ask the user: "How do you typically deploy this project publicly? I found [X, Y, Z] but want to confirm the correct approach."
