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
