# PR Plugin

A personal development toolkit that extends Claude Code with commands for feature development, MVP development, code cleanup, documentation, deployment, and git operations.

## Prerequisites

This plugin relies on external tools that should be installed before use. Some are required, others enhance specific skills.

### Required

| Tool | Type | Used By | Installation |
|------|------|---------|--------------|
| [Context7](https://github.com/upstash/context7) | MCP server | Package documentation lookup | Add to MCP settings, no API key needed |

### Optional

| Tool | Type | Used By | Installation |
|------|------|---------|--------------|
| Gemini API | API | `generate-image-nb` skill | Requires `GEMINI_API_KEY` environment variable |
| [Agentation](https://github.com/benjitaylor/agentation) | Next.js component | `agentation` skill | Installed per-project via skill |
| [Playwright](https://github.com/anthropics/claude-code) | MCP server | UI testing, browser automation | Install via Claude Code: `/install-github-mcp playwright` |

### Setup Notes

- **Context7**: Provides up-to-date documentation for any library. Add to your `.claude/settings.json` MCP servers.
- **Playwright**: For browser automation and UI testing. Install via Claude Code by running `/install-github-mcp playwright` or add the Playwright MCP server to your settings.
- **Gemini API**: The `generate-image-nb` skill uses the Gemini Nano Banana API for image generation. Get an API key from Google AI Studio.
- **Agentation**: Adds visual feedback toolbar to Next.js projects. Installed automatically when skill is used.

## Commands

| Command                                  | Description                                                                                            | Agent Support |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------ | ------------- |
| `/pr:feature-dev [desc] [--subagents\|--team]` | Develop a single feature with RFD tracking, codebase exploration, architecture design, and code review | Yes |
| `/pr:mvp-dev [focus] [--subagents\|--team]`    | Develop an entire MVP from a PRD file, creating RFDs for each feature                                  | Yes |
| `/pr:commit-push [path] [--merge\|--pr]` | Commit changes, update commitlog.md, push to remote, optionally merge or create PR                     | No |
| `/pr:clean-codebase [path] [--subagents\|--team]` | Clean and professionalize code using automated review to identify issues                            | Yes |
| `/pr:update-docs [path] [focus] [--subagents\|--team]` | Update project documentation based on codebase changes                                          | Yes |
| `/pr:update-claude-md [path]`            | Update CLAUDE.md files with current project state and development principles                           | No |
| `/pr:run-local [instructions]`           | Start and run the application locally for development                                                  | No |
| `/pr:run-public [instructions]`          | Deploy and run the application publicly                                                                | No |
| `/pr:create-prd [ideas]`                 | Generate a Product Requirements Document through interactive discovery and research                    | No |
| `/pr:create-snapshot [path]`             | Generate a comprehensive technical snapshot of the codebase for handoff or documentation               | Yes |

## Skills

| Skill | Description |
|-------|-------------|
| `agentation` | Add Agentation visual feedback toolbar to Next.js projects |
| `atlas-development` | ATLAS framework for production-ready development (Architect, Trace, Link, Assemble, Stress-test) |
| `create-prd` | Interactive PRD generation with web research |
| `frontend-design` | Create distinctive, production-grade frontend interfaces with high design quality |
| `generate-image-nb` | Generate and edit images via Gemini Nano Banana API |
| `writing-clearly-and-concisely` | Clear, direct prose following Strunk's principles |

## ATLAS Development Framework

This plugin follows the **ATLAS** philosophy for building production-ready applications:

| Step | Phase | Purpose |
|------|-------|---------|
| **A** | Architect | Define problem, users, success metrics |
| **T** | Trace | Data schema, integrations map, stack proposal |
| **L** | Link | Validate ALL connections before building |
| **A** | Assemble | Build with layered architecture |
| **S** | Stress-test | Test functionality, error handling |

**When to apply:**
- **Full ATLAS**: New MVPs, features with integrations/schema changes
- **Partial (L+A+S)**: Features using existing patterns
- **Skip**: Bug fixes, one-line changes, documentation, refactoring

ATLAS is integrated into `create-prd`, `mvp-dev`, and `feature-dev` commands. See the `atlas-development` skill for complete framework details.

## Agents

The plugin includes three specialized subagents used by commands:

| Agent            | Color  | Purpose                                                                        |
| ---------------- | ------ | ------------------------------------------------------------------------------ |
| `code-explorer`  | Yellow | Analyzes existing codebase by tracing execution paths and mapping architecture |
| `code-architect` | Green  | Designs feature architectures with implementation blueprints                   |
| `code-reviewer`  | Red    | Reviews code for bugs, quality issues, and convention adherence                |

## Multi-Agent Strategy

Several commands in this plugin launch multiple agents in parallel for exploration, architecture design, and code review. These commands support two agent strategies:

### Subagents (Default)

Subagents are lightweight workers that run within your session and report results back. They work independently — each handles a focused task and returns findings. This is the default mode for all commands and requires no additional setup.

### Agent Teams (Experimental)

[Agent teams](https://docs.anthropic.com/en/docs/claude-code/agent-teams) are a Claude Code experimental feature that lets multiple Claude Code instances work together as a team with inter-agent messaging. Unlike subagents, teammates can communicate directly with each other, share findings, challenge each other's conclusions, and coordinate work through a shared task list.

Agent teams are useful when agents need to collaborate — for example, architecture agents debating design trade-offs, or reviewers cross-referencing each other's findings across different quality dimensions.

**Agent teams are more expensive** (each teammate is a separate Claude instance) and add coordination overhead. The plugin defaults to subagents and only recommends agent teams when inter-agent communication provides a clear advantage.

#### Enabling Agent Teams

Agent teams are disabled by default in Claude Code. To use the `--team` flag, you must first enable the feature:

**Option 1: Add to settings.json** (recommended):

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

**Option 2: Set as environment variable**:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

Without this setting enabled, the `--team` flag will not work.

### Using the Flags

Commands that support multi-agent strategies accept these flags:

| Flag | Behavior |
|------|----------|
| *(no flag)* | Claude decides the best strategy. Defaults to subagents unless the task clearly benefits from inter-agent communication. |
| `--subagents` | Force subagent mode regardless of task complexity. |
| `--team` | Force agent team mode. Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` to be enabled. |

### Which Commands Support Agent Flags?

| Command | Agent Phases | Best Case for Teams |
|---------|-------------|---------------------|
| `feature-dev` | Exploration, architecture, review | Architecture debate for complex multi-component features |
| `mvp-dev` | Exploration, architecture, per-feature dev, integration review | Architecture planning and integration review for tightly coupled MVPs |
| `clean-codebase` | Code review (dead code, comments) | Rarely needed — review tasks are independent |
| `update-docs` | Codebase exploration (changes, gaps) | Rarely needed — exploration tasks are independent |
| `create-snapshot` | Codebase exploration (4 agents) | Rarely needed — exploration tasks are independent |

## Documentation Structure

This plugin uses a structured documentation approach in projects:

```
.claude/
├── checkpoints/
│   ├── checkpoint-0/           # Pre-development (PRD, initial RFDs)
│   │   ├── prd.md              # Product Requirements Document
│   │   └── rfd/                # Request for Development documents
│   │       └── {N}-{feature}/
│   │           └── rfd-{date}-{time}.md
│   ├── checkpoint-1/           # First development checkpoint
│   │   ├── snapshot.md         # Technical snapshot
│   │   └── rfd/
│   └── checkpoint-{N}/         # Additional checkpoints
└── references/                 # Reference documents (guidelines, specs)
```

### Key Document Types

- **PRD (Product Requirements Document)**: Product vision, requirements, and specifications. Created in checkpoint-0 before development begins.
- **RFD (Request for Development)**: Tracks individual feature requests, implementation progress, and decisions. Created per feature.
- **Snapshot**: Comprehensive technical snapshot of the codebase at a point in time.

## Typical Workflows

### Starting a New Project

1. `/pr:create-prd` - Generate PRD through interactive discovery
2. `/pr:mvp-dev` - Develop the MVP from the PRD

### Adding a Feature to Existing Project

1. `/pr:feature-dev [description]` - Develop the feature with full workflow

### Maintenance Tasks

- `/pr:clean-codebase` - Clean up code
- `/pr:update-docs` - Update documentation
- `/pr:update-claude-md` - Update CLAUDE.md files
- `/pr:create-snapshot` - Capture current state
- `/pr:commit-push --pr` - Commit and create PR

## Version

1.0.0

## Author

Pouria Rouzrokh
