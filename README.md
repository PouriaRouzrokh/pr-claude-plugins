# PR Cloud Plugins

A Claude Code plugin marketplace by Pouria Rouzrokh.

## Installation

### Step 1: Add the Marketplace

Inside Claude Code, run:

```
/plugin marketplace add PouriaRouzrokh/pr-claude-plugins
```

### Step 2: Install a Plugin

```
/plugin install pr@pr-cloud-plugins
```

## Prerequisites

This plugin relies on external tools that should be installed before use. Some are required, others enhance specific skills.

### Required

| Tool | Type | Used By | Installation |
|------|------|---------|--------------|
| [Context7](https://github.com/upstash/context7) | MCP server | Package documentation lookup | Add to MCP settings, no API key needed |

### Optional

| Tool | Type | Used By | Installation |
|------|------|---------|--------------|
| Gemini API | API | `generate-image-nb`, `generate-svg` skills | Requires `GEMINI_API_KEY` environment variable |
| [Agentation](https://github.com/benjitaylor/agentation) | Next.js component | `agentation` skill | Installed per-project via skill |
| [Playwright](https://github.com/anthropics/claude-code) | MCP server | UI testing, browser automation | Install via Claude Code (see below) |
| Agent Teams | Claude Code feature | `--team` flag on supported commands | Enable in settings (see below) |

### Setup Notes

- **Context7**: Provides up-to-date documentation for any library. Add to your `.claude/settings.json` MCP servers.
- **Gemini API**: Used by `generate-image-nb` and `generate-svg` skills. Get an API key from Google AI Studio and set `GEMINI_API_KEY` in your environment, project `.env`, `.claude/.env`, or `~/.claude/.env`.
- **Agentation**: Adds visual feedback toolbar to Next.js projects. Installed automatically when skill is used.
- **Playwright**: For browser automation and UI testing. Install via Claude Code by running `/install-github-mcp playwright` or add the Playwright MCP server to your settings. Playwright is used by commands and skills that need browser testing, if available.
- **Agent Teams**: Several commands support running agents as a coordinated team (via Claude Code's experimental [agent teams](https://docs.anthropic.com/en/docs/claude-code/agent-teams) feature). This is optional — commands default to subagents. To enable agent teams, add to your `settings.json`:
  ```json
  {
    "env": {
      "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
    }
  }
  ```
  Then pass `--team` to supported commands (e.g., `/pr:feature-dev my feature --team`). See the [pr plugin README](./pr/README.md#multi-agent-strategy) for details.

## Available Plugins

| Plugin      | Description                                                                                                                                      |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| [pr](./pr/) | Personal development toolkit with commands for feature development, MVP development, code cleanup, documentation, deployment, and git operations |

The **pr** plugin implements the **ATLAS development framework** (Architect, Trace, Link, Assemble, Stress-test) for building production-ready applications. See the [pr plugin README](./pr/README.md) for details.

## Updating

To get the latest plugins, run:

```
/plugin marketplace update pr-cloud-plugins
```

## Author

Pouria Rouzrokh
