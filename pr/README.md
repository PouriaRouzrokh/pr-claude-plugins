# PR Plugin

A personal development toolkit that extends Claude Code with commands for feature development, MVP development, code cleanup, documentation, deployment, and git operations.

## Commands

| Command                                  | Description                                                                                            |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `/pr:feature-dev [description]`          | Develop a single feature with RFD tracking, codebase exploration, architecture design, and code review |
| `/pr:mvp-dev [focus]`                    | Develop an entire MVP from a PRD file, creating RFDs for each feature                                  |
| `/pr:commit-push [path] [--merge\|--pr]` | Commit changes, update commitlog.md, push to remote, optionally merge or create PR                     |
| `/pr:clean-codebase [path]`              | Clean and professionalize code using automated review to identify issues                               |
| `/pr:update-docs [path] [focus]`         | Update project documentation based on codebase changes                                                 |
| `/pr:run-local [instructions]`           | Start and run the application locally for development                                                  |
| `/pr:run-public [instructions]`          | Deploy and run the application publicly                                                                |
| `/pr:create-prd [ideas]`                 | Generate a Product Requirements Document through interactive discovery and research                    |
| `/pr:create-snapshot [path]`             | Generate a comprehensive technical snapshot of the codebase for handoff or documentation               |

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
- `/pr:create-snapshot` - Capture current state
- `/pr:commit-push --pr` - Commit and create PR

## Version

1.0.0

## Author

Pouria Rouzrokh
