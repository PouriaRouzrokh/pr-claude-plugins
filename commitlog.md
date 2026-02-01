# pr-claude-plugins Commit Log

This file tracks significant commits and changes to the pr-claude-plugins marketplace.

---

### 1/31/2026 - 14:45 (main)

- **Feature: Integrate ATLAS development framework**
  - Added new `atlas-development` skill documenting the ATLAS philosophy
    - ATLAS: Architect, Trace, Link, Assemble, Stress-test
    - Includes guidance on when to apply full, partial, or skip ATLAS
    - Anti-patterns section to avoid common "vibe coding" failures
  - Updated `create-prd` skill with ATLAS Foundation section
    - PRD now implements Architect phase with clear problem/user/success questions
    - Added ATLAS Brief section to PRD template
  - Updated `mvp-dev` command with ATLAS philosophy
    - Added Link Validation step in Phase 3 (connection validation before building)
    - Guidance on when to use vs when NOT to use this command
  - Updated `feature-dev` command with contextual ATLAS application
    - Full process for complex features, simplified for small changes
    - Added "Match process depth to task complexity" principle
  - Updated `CLAUDE.md` with ATLAS framework section and "When to apply" guidance
  - Updated README files with ATLAS skill and framework documentation

---

### 1/31/2026 - 12:20 (main)

- **Feature: Add new skills and update generate-image-nb**
  - Updated `generate-image-nb` skill to use Gemini Nano Banana API directly
    - Replaced outdated Gemini CLI extension commands with Python/JavaScript scripts
    - Added `scripts/generate_image.py` and `scripts/generate_image.mjs`
    - Supports text-to-image, image editing, aspect ratios, model selection (flash/pro)
    - Uses `google-genai` (Python) and `@google/genai` (JavaScript) packages
  - Added new skills:
    - `agentation`: Add visual feedback toolbar to Next.js projects
    - `frontend-design`: Production-grade frontend interfaces (Apache 2.0, based on Anthropic skill)
    - `writing-clearly-and-concisely`: Clear prose following Strunk's principles
  - Removed `create-snapshot` skill files (functionality moved to command)
  - Updated README files with current skills list and corrected prerequisites
  - Various command file updates from prior sessions

---

### 1/28/2026 - 22:07 (main)

- **Feature: Add /pr:update-claude-md command (RFD-2)**
  - Updated the CLAUDE.md file using the /pr:update-claude-md command.

### 1/28/2026 - 22:00 (main)

- **Feature: Add /pr:update-claude-md command (RFD-2)**
  - New command to update CLAUDE.md files with project state and development principles
  - Enforces required sections: Development Principles, Documentation Hierarchy
  - Development Principles include: RFD workflow, Context7 MCP for docs, agent-browser for UI testing, testing requirements
  - Reads from existing checkpoints/snapshots (no agent exploration needed)
  - Target: keep CLAUDE.md under 200 lines to avoid context bloat
  - Removed CLAUDE.md handling from /pr:update-docs (Phase 5.5 removed)
  - Added Skills section to project CLAUDE.md
  - Created RFD-2 documenting the feature

---

### 1/28/2026 (main)

- **Add agent-browser skill from vercel-labs**
  - Browser automation skill for web testing, form filling, screenshots, data extraction
  - Includes references: authentication, proxy-support, session-management, snapshot-refs, video-recording
  - Includes templates: form-automation.sh, authenticated-session.sh, capture-workflow.sh

---

### 1/28/2026 (main)

- **Add MCP tools and skills guidance to feature-dev and mvp-dev**
  - Added core principle to leverage available MCP tools and skills
  - Examples: context7 for docs, vercel-labs/agent-skills for UI testing
  - Encourages proactive use of available integrations during development

---

### 1/28/2026 (main)

- **RFD-1: Skill-command consolidation (complete)**
  - Phase 1: Removed 1014 lines of duplicate embedded content from commands (`c6e24ce`)
  - Phase 2: Re-added thin wrapper commands (7 lines each) that delegate to skills
  - Commands provide frontmatter for discoverability; skills provide implementation
  - Created RFD-1 documenting the consolidation (`1182cd4`)

---

### 1/27/2026 (main)

- **Workaround: Embed skill content into commands due to Claude Code bug**
  - Embedded full skill content, templates, and examples directly into `create-prd.md` and `create-snapshot.md` commands
  - This is a workaround for [claude-code#15178](https://github.com/anthropics/claude-code/issues/15178) where skills are not directly readable
  - Original skill files retained for future reversion when bug is fixed
  - Condensed snapshot template for brevity while keeping all 19 sections
  - Updated README.md with Known Limitations section documenting the bug

---

### 1/27/2026 (main)

- **Add initial checkpoint-1 snapshot**
  - Created `.claude/checkpoints/checkpoint-1/snapshot.md` - first technical snapshot of the codebase
  - Documents complete plugin architecture, commands, agents, skills, and patterns
  - Serves as a comprehensive handoff document for understanding the pr-claude-plugins repository

---

### 1/27/2026 (main)

- **Add commands for create-prd and create-snapshot skills**
  - Created `pr/commands/create-prd.md` - wrapper command for PRD generation skill
  - Created `pr/commands/create-snapshot.md` - wrapper command for snapshot generation skill
  - Skills are now directly invocable as `/pr:create-prd` and `/pr:create-snapshot`
  - Updated pr/README.md to list all 9 commands (removed separate Skills section)
  - Updated CLAUDE.md with complete command list and improved documentation

---

### 1/27/2026 (main)

- **Separate README files for marketplace and plugin**
  - Root README now focuses on marketplace installation and plugin listing
  - Created `pr/README.md` with plugin-specific documentation (commands, skills, agents, workflows)

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
