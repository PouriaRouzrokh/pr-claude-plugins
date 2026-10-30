---
name: run-public
description: "Deploy the application publicly (preview, staging, or production), verify it is healthy, and report URLs and rollback steps. Confirms before any production deploy."
argument-hint: "[optional: target environment or instructions]"
disable-model-invocation: true
---

# Run Public

Deploy the application to a public environment, prove the deployment is healthy, and leave the user able to roll back.

**Instructions**: $ARGUMENTS. Empty means redeploy the current code to the project's usual target.

Deployments are visible to real users and can be hard to undo, so: confirm the target before deploying to production (or when the target is ambiguous), never tear down a running production instance without explicit approval, and never print secret values.

## 1. Identify the Target and Method

1. Read the README, CLAUDE.md, the latest snapshot, and deployment configuration: `vercel.json`, `netlify.toml`, `fly.toml`, `railway.json`, `render.yaml`, `Dockerfile`, `compose.prod.yaml`, `Procfile`, `.github/workflows/`, infrastructure code (Terraform, Pulumi).
2. Prefer the project's own entry point (`make deploy`, `npm run deploy`, `./deploy.sh`, a CI workflow) over platform commands.
3. If the project deploys through CI (push to main, a release tag, a manual workflow), deploying means triggering that pipeline, not bypassing it.
4. If an MCP server for the platform is connected (for example Vercel), use it for project status, deployment inspection, and logs; otherwise use the platform CLI.
5. Determine the environment (preview, staging, production). If it is production or unclear, confirm with the user now.

If the method is still unclear, ask: "I found X and Y; how do you usually deploy this?"

## 2. Check Readiness

- **Working tree**: what will be deployed (branch, commit, uncommitted changes). Deploying uncommitted work usually is a mistake; ask.
- **Configuration**: required environment variables are set on the platform (check names, never values), production database URLs point at the right environment, and secrets exist.
- **Migrations**: list pending database migrations and get explicit approval before running them in production.
- **Quality** (production web frontends): offer to run `web-quality-audit` against a local production build first.

## 3. Build

Run the production build the way the platform will (`npm run build`, `uv build`, `docker build`, `go build`, `cargo build --release`) and fix failures before deploying. Each Bash call runs in a fresh shell, so run tools through their environment (`uv run`, `poetry run`, `.venv/bin/...`) and install with the lockfile's package manager (`npm ci`, `pnpm install --frozen-lockfile`, `uv sync --no-dev`).

## 4. Deploy

Use the method from step 1. Common platform commands, for reference:

| Platform | Preview | Production |
|----------|---------|------------|
| Vercel | `vercel` | `vercel --prod` |
| Netlify | `netlify deploy` | `netlify deploy --prod` |
| Fly.io | `fly deploy --app {staging-app}` | `fly deploy` |
| Railway | `railway up --environment {env}` | `railway up` |
| Cloud Run | `gcloud run deploy --no-traffic --tag preview` | `gcloud run deploy` |
| Docker on a server | Build, push, then `docker compose -f compose.prod.yaml up -d` on the host | |

Note the previous deployment or image tag before deploying production, so rollback is one command. Warn the user first if the deploy causes downtime.

## 5. Verify

Wait for the deployment to finish (watch its status or logs with the Monitor tool rather than a foreground `sleep` loop), then check the public URL responds, health endpoints pass, the main user flow works (load the page or call the key endpoint), and logs show no new errors. If verification fails, show the evidence and offer to roll back.

## 6. Report

Give the public URLs, the environment and commit deployed, dashboard and log links, how to roll back (the exact command or dashboard step), and anything that needs attention (skipped migrations, warnings in logs).
