# CLAUDE.md

Claude Code plugin marketplace containing the **pr** plugin - a personal development toolkit for feature development, MVP development, code cleanup, documentation, deployment, and git operations.

## Quick Commands

| Command                                  | Description                   |
| ---------------------------------------- | ----------------------------- |
| `/pr:feature-dev [desc]`                 | Feature dev with RFD tracking |
| `/pr:mvp-dev [focus]`                    | MVP from PRD                  |
| `/pr:commit-push [path] [--merge\|--pr]` | Commit, push, merge/PR        |
| `/pr:clean-codebase [path]`              | Code cleanup                  |
| `/pr:update-docs [path]`                 | Update documentation          |
| `/pr:update-claude-md [path]`            | Update CLAUDE.md files        |
| `/pr:create-prd [ideas]`                 | Generate PRD                  |
| `/pr:create-snapshot [path]`             | Technical snapshot            |
| `/pr:run-local`                          | Start local dev server        |
| `/pr:run-public`                         | Deploy publicly               |

## Skills

| Skill                           | Description                                        |
| ------------------------------- | -------------------------------------------------- |
| `agent-browser`                 | Browser automation for web testing and screenshots |
| `create-prd`                    | Interactive PRD generation with web research       |
| `create-snapshot`               | Technical codebase snapshot generation             |
| `frontend-design`               | Production-grade frontend interfaces               |
| `writing-clearly-and-concisely` | Clear, direct prose following Strunk's principles  |

## Development Principles

### Leveraging Available Tools

Before starting any task, check what skills and MCP servers are available in your current context:

- Review the available skills list for specialized capabilities that can help with the task
- Check available MCP servers for tools that provide enhanced functionality
- Use the most appropriate tools for each task rather than doing everything manually
- Always use Context7 MCP when I need library/API documentation, code generation, setup or configuration steps without me having to explicitly ask.

### RFD Documentation

For significant changes (features, bug fixes, architectural changes - not one-line fixes), create or update an RFD:

- **Path**: `.claude/checkpoints/checkpoint-{N}/rfd/{N}-{feature-slug}/rfd-{YYYY-MM-DD}-{HHMM}.md`
- **Workflow**: Write question → Document plan → Implement → Update RFD with results

### Planning First

Always plan before implementation:

- Write RFD first for features requiring them
- Think through approach before coding
- Consider edge cases, error handling, testing upfront

### Package Documentation

When working with unfamiliar packages:

1. **First**: Check available MCP servers for documentation tools
2. **Second**: Search online for documentation
3. **Third**: Ask the user for clarification

### UI/Web Testing

For frontend development:

- Check available skills for browser automation/testing capabilities
- Take screenshots to verify visual changes
- Test user flows and form interactions

### Testing Requirements

Before handing off work:

- Run all relevant tests
- Verify changes work as expected
- Fix any failures or regressions

## Documentation Hierarchy

```
.claude/checkpoints/
├── checkpoint-0/          # Pre-development
│   └── prd.md             # Product Requirements Document
└── checkpoint-N/          # Development milestones
    ├── snapshot.md        # Technical codebase snapshot
    └── rfd/               # Feature tracking
```

**Document relationships**: PRD (vision) → RFDs (features) → Snapshots (state) → CLAUDE.md (quick reference)

## Repository Structure

```
pr-claude-plugins/
├── .claude-plugin/marketplace.json   # Marketplace manifest
├── pr/                               # The pr plugin
│   ├── .claude-plugin/plugin.json    # Plugin manifest
│   ├── agents/                       # code-explorer, code-architect, code-reviewer
│   ├── commands/                     # Slash commands (10 total)
│   └── skills/                       # Skills with SKILL.md + references/
│       ├── agent-browser/            # Browser automation
│       ├── create-prd/               # PRD generation
│       ├── create-snapshot/          # Snapshot generation
│       ├── frontend-design/          # UI development
│       └── writing-clearly-and-concisely/  # Writing quality
├── CLAUDE.md
├── commitlog.md
└── README.md
```

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
---
```

**Agents** (`agents/*.md`):

```yaml
---
name: agent-name
tools: Glob, Grep, Read, ...
model: sonnet
color: yellow|green|red
---
```

## Agent Colors

| Agent          | Color  | Purpose                                        |
| -------------- | ------ | ---------------------------------------------- |
| code-explorer  | Yellow | Traces execution paths, returns 5-10 key files |
| code-architect | Green  | Designs implementations with blueprints        |
| code-reviewer  | Red    | Reviews code, reports issues ≥80% confidence   |

## Key Concepts

- **RFD**: Request for Development - tracks feature requests and implementation
- **PRD**: Product Requirements Document - project vision at `checkpoint-0/prd.md`
- **Checkpoint**: Point-in-time documentation (checkpoint-0 = pre-dev, checkpoint-1+ = development)
- **commitlog.md**: Project commit history maintained by `/pr:commit-push`
