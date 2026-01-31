# PR Plugin

A personal development toolkit that extends Claude Code with commands for feature development, MVP development, code cleanup, documentation, deployment, and git operations.

## Prerequisites

This plugin relies on external tools that should be installed before use. Some are required, others enhance specific skills.

### Required

| Tool | Type | Used By | Installation |
|------|------|---------|--------------|
| [agent-browser](https://github.com/vercel-labs/agent-browser) | NPX package | `agent-browser` skill, UI testing | `npx agent-browser` (auto-installs on first use) |
| [Context7](https://github.com/upstash/context7) | MCP server | Package documentation lookup | Add to MCP settings, no API key needed |

### Optional

| Tool | Type | Used By | Installation |
|------|------|---------|--------------|
| Gemini API | API | `generate-image-nb` skill | Requires `GEMINI_API_KEY` environment variable |
| [Agentation](https://github.com/benjitaylor/agentation) | Next.js component | `agentation` skill | Installed per-project via skill |

### Setup Notes

- **agent-browser**: Runs headless Chrome for browser automation. First run downloads browser binaries.
- **Context7**: Provides up-to-date documentation for any library. Add to your `.claude/settings.json` MCP servers.
- **Gemini API**: The `generate-image-nb` skill uses the Gemini Nano Banana API for image generation. Get an API key from Google AI Studio.
- **Agentation**: Adds visual feedback toolbar to Next.js projects. Installed automatically when skill is used.

## Commands

| Command                                  | Description                                                                                            |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `/pr:feature-dev [description]`          | Develop a single feature with RFD tracking, codebase exploration, architecture design, and code review |
| `/pr:mvp-dev [focus]`                    | Develop an entire MVP from a PRD file, creating RFDs for each feature                                  |
| `/pr:commit-push [path] [--merge\|--pr]` | Commit changes, update commitlog.md, push to remote, optionally merge or create PR                     |
| `/pr:clean-codebase [path]`              | Clean and professionalize code using automated review to identify issues                               |
| `/pr:update-docs [path] [focus]`         | Update project documentation based on codebase changes                                                 |
| `/pr:update-claude-md [path]`            | Update CLAUDE.md files with current project state and development principles                           |
| `/pr:run-local [instructions]`           | Start and run the application locally for development                                                  |
| `/pr:run-public [instructions]`          | Deploy and run the application publicly                                                                |
| `/pr:create-prd [ideas]`                 | Generate a Product Requirements Document through interactive discovery and research                    |
| `/pr:create-snapshot [path]`             | Generate a comprehensive technical snapshot of the codebase for handoff or documentation               |

## Skills

| Skill | Description |
|-------|-------------|
| `agent-browser` | Browser automation for web testing, form filling, screenshots, and data extraction |
| `agentation` | Add Agentation visual feedback toolbar to Next.js projects |
| `create-prd` | Interactive PRD generation with web research |
| `frontend-design` | Create distinctive, production-grade frontend interfaces with high design quality |
| `generate-image-nb` | Generate and edit images via Gemini Nano Banana API |
| `writing-clearly-and-concisely` | Clear, direct prose following Strunk's principles |

## Agents

The plugin includes three specialized subagents used by commands:

| Agent            | Color  | Purpose                                                                        |
| ---------------- | ------ | ------------------------------------------------------------------------------ |
| `code-explorer`  | Yellow | Analyzes existing codebase by tracing execution paths and mapping architecture |
| `code-architect` | Green  | Designs feature architectures with implementation blueprints                   |
| `code-reviewer`  | Red    | Reviews code for bugs, quality issues, and convention adherence                |

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
