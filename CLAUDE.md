# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

This is the **pr** plugin for Claude Code - a personal development toolkit that extends Claude with commands for feature development, MVP development, code cleanup, documentation, deployment, and git operations.

## Plugin Architecture

```
pr/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (name, version, author)
├── agents/                   # Subagent definitions (launched by commands)
│   ├── code-explorer.md     # Yellow - analyzes existing code, traces execution
│   ├── code-architect.md    # Green - designs implementations, creates blueprints
│   └── code-reviewer.md     # Red - reviews code, reports issues with confidence >= 80
├── commands/                 # Slash commands (invoked as /pr:command-name)
│   ├── feature-dev.md       # Single feature development with RFD tracking
│   ├── mvp-dev.md           # Full MVP development from PRD
│   ├── commit-push.md       # Git commit, push, merge, PR creation
│   ├── clean-codebase.md    # Code cleanup using code-reviewer
│   ├── update-docs.md       # Documentation updates using code-explorer
│   ├── run-local.md         # Start app locally
│   └── run-public.md        # Deploy publicly
└── skills/                   # Skills with supporting files
    ├── create-snapshot/
    │   ├── SKILL.md         # Codebase snapshot generation
    │   └── template.md      # Snapshot template
    └── create-prd/
        └── SKILL.md         # PRD generation through discovery
```

## Key Concepts

### RFD (Request for Development)
Documents that track feature requests and implementation progress. Located in `.claude/checkpoints/checkpoint-{N}/rfd/{N}-{feature-slug}/rfd-{YYYY-MM-DD}-{HHMM}.md`. Status values: Planning, In Progress, Completed, On Hold.

### PRD (Product Requirements Document)
Product vision and requirements document. Always located at `.claude/checkpoints/checkpoint-0/prd.md`.

### Checkpoints
Point-in-time documentation of project state. checkpoint-0 is pre-development (contains PRD), checkpoint-1+ contain snapshots and RFDs created during development.

## Agent Usage Pattern

Commands launch agents with specific prompts and wait for results:
- **code-explorer**: Returns 5-10 key files to read + analysis
- **code-architect**: Returns implementation blueprint with file paths
- **code-reviewer**: Returns issues with confidence scores (only >= 80 reported)

Commands typically launch 2-3 agents in parallel with different focuses, then consolidate findings.

## Command/Skill Format

Commands use YAML frontmatter:
```yaml
---
description: Brief description
argument-hint: "[optional: hint text]"
---
```

Skills use YAML frontmatter with additional fields:
```yaml
---
name: skill-name
description: Description
argument-hint: "[hint]"
---
```

Agents use:
```yaml
---
name: agent-name
description: Description
tools: Glob, Grep, Read, ...
model: sonnet
color: yellow|green|red
---
```
