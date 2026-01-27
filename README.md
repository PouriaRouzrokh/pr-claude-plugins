# PR Plugin for Claude Code

A personal development toolkit that extends Claude Code with commands for feature development, MVP development, code cleanup, documentation, deployment, and git operations.

## Installation

### Option 1: Test During Development (Recommended First)

Use the `--plugin-dir` flag to load your plugin without installing it:

```bash
claude --plugin-dir /path/to/pr-dev
```

For example, if your plugin is at `~/plugins/pr-dev`:

```bash
claude --plugin-dir ~/plugins/pr-dev
```

This lets you iterate quickly - just restart Claude Code to pick up changes.

### Option 2: Install Permanently

#### Step 1: Create a Local Marketplace

Create a `marketplace.json` file in a directory (e.g., `~/my-marketplaces/`):

```json
{
  "plugins": [
    {
      "name": "pr-dev",
      "source": "/absolute/path/to/pr-dev"
    }
  ]
}
```

#### Step 2: Add the Marketplace to Claude Code

Inside Claude Code, run:

```
/plugin marketplace add ~/my-marketplaces/marketplace.json
```

#### Step 3: Install the Plugin

```
/plugin install pr-dev
```

Or via CLI:

```bash
claude plugin install pr-dev --scope user
```

---

## Verify It's Working

Once Claude Code is running with your plugin:

### 1. Check available commands

Type `/` and look for your command:

```
/pr-dev:feature
```

### 2. Run the help command

```
/help
```

Your plugin commands should appear under the `pr-dev` namespace.

### 3. Test the command

```
/pr-dev:feature Add user authentication to the app
```

### 4. Check for errors

Inside Claude Code:

```
/plugin
```

Then go to the Errors tab to see any loading issues.

### Debug Mode

If something isn't working, run Claude Code with debug output:

```bash
claude --debug --plugin-dir ~/plugins/pr-dev
```

This shows:
- Plugin loading status
- Any manifest errors
- Command/agent registration

### Quick Checklist

| Check | Command |
| ----- | ------- |
| Plugin structure correct? | Verify `.claude-plugin/plugin.json` exists at root |
| Commands visible? | Type `/pr-dev:` and see if feature appears |
| Agents loaded? | Type `/agents` to see if your agents appear |
| Any errors? | Check `/plugin` → Errors tab |

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

## Skills

| Skill                        | Description                                                                              |
| ---------------------------- | ---------------------------------------------------------------------------------------- |
| `/pr:create-snapshot [path]` | Generate a comprehensive technical snapshot of the codebase for handoff or documentation |
| `/pr:create-prd [ideas]`     | Generate a Product Requirements Document through interactive discovery and research      |

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
