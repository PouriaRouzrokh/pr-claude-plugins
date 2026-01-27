# pr-claude-plugins Commit Log

This file tracks significant commits and changes to the pr-claude-plugins marketplace.

---

### 1/27/2026 (main)

- **Add marketplace configuration and simplify installation docs**
  - Created `.claude-plugin/marketplace.json` with marketplace name `pr-cloud-plugins`
  - Simplified README with GitHub-based installation instructions
  - Removed local testing and development installation sections
  - Updated git remote to `git@github.com:PouriaRouzrokh/pr-claude-plugins.git`

---

### 1/27/2026 - 00:30 (main)

- **Release v1.0.0: Add commitlog.md and standardize commit log naming**
  - Updated version to 1.0.0 in plugin.json and README.md
  - Created commitlog.md to track project changes
  - Updated commit-push.md command to use commitlog.md instead of commit-log.md
  - Added Phase 0.5 to detect and rename commit log file variations (commit_log.md, commit-log.md, COMMIT_LOG.md, etc.)
  - Normalized reference filenames (removed spaces)

---

### 1/27/2026 - 00:09 (main)

- **Initial Release: pr plugin v1.0.0**
  - Plugin manifest with name, description, version, author
  - Three specialized agents: code-explorer (yellow), code-architect (green), code-reviewer (red)
  - Seven commands: feature-dev, mvp-dev, commit-push, clean-codebase, update-docs, run-local, run-public
  - Two skills: create-prd (PRD generation through discovery), create-snapshot (codebase snapshot generation)
  - Supporting documentation: CLAUDE.md, README.md, references folder
  - Comprehensive RFD/PRD/checkpoint documentation management system
