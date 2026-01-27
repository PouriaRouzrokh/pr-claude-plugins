# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

This is the **pr-cloud-plugins** marketplace - a Claude Code plugin repository containing the **pr** plugin, a personal development toolkit for feature development, MVP development, code cleanup, documentation, deployment, and git operations.

## Repository Structure

```
pr-claude-plugins/
├── .claude-plugin/
│   └── marketplace.json     # Marketplace manifest (name: pr-cloud-plugins)
├── pr/                       # The pr plugin
│   ├── .claude-plugin/
│   │   └── plugin.json      # Plugin manifest (name, version, author)
│   ├── agents/              # Subagents launched by commands
│   ├── commands/            # Slash commands (/pr:command-name)
│   └── skills/              # Skills with supporting files
├── commitlog.md             # Project commit history
└── README.md                # Marketplace installation docs
```

## Key Concepts

### RFD (Request for Development)
Documents tracking feature requests and implementation. Path: `.claude/checkpoints/checkpoint-{N}/rfd/{N}-{feature-slug}/rfd-{YYYY-MM-DD}-{HHMM}.md`. Status: Planning, In Progress, Completed, On Hold.

### PRD (Product Requirements Document)
Product vision document at `.claude/checkpoints/checkpoint-0/prd.md`.

### Checkpoints
Point-in-time project documentation. checkpoint-0 is pre-development (PRD), checkpoint-1+ contain snapshots and RFDs.

## Agent Colors and Purposes

| Agent | Color | Purpose |
|-------|-------|---------|
| code-explorer | Yellow | Traces execution paths, maps architecture, returns 5-10 key files |
| code-architect | Green | Designs implementations, creates blueprints with file paths |
| code-reviewer | Red | Reviews code, reports issues with confidence >= 80 |

Commands typically launch 2-3 agents in parallel with different focuses, then consolidate findings.

## Plugin Component Formats

**Commands** (`commands/*.md`):
```yaml
---
description: Brief description
argument-hint: "[optional: hint text]"
---
```

**Skills** (`skills/*/SKILL.md`):
```yaml
---
name: skill-name
description: Description
argument-hint: "[hint]"
---
```

**Agents** (`agents/*.md`):
```yaml
---
name: agent-name
description: Description
tools: Glob, Grep, Read, ...
model: sonnet
color: yellow|green|red
---
```

## Commands

| Command | Description |
|---------|-------------|
| `/pr:feature-dev [desc]` | Single feature dev with RFD tracking |
| `/pr:mvp-dev [focus]` | MVP from PRD |
| `/pr:commit-push [path] [--merge\|--pr]` | Commit, push, optionally merge/PR |
| `/pr:clean-codebase [path]` | Code cleanup via code-reviewer |
| `/pr:update-docs [path] [focus]` | Update documentation based on changes |
| `/pr:run-local [instructions]` | Start app locally for development |
| `/pr:run-public [instructions]` | Deploy and run app publicly |
| `/pr:create-prd [ideas]` | Generate PRD through discovery |
| `/pr:create-snapshot [path]` | Technical codebase snapshot |

## Working with commitlog.md

The `/pr:commit-push` command maintains `commitlog.md` in the project root. It auto-renames variations (commit-log.md, COMMIT_LOG.md, etc.) to `commitlog.md` for consistency.
