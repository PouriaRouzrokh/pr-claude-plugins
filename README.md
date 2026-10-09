# PR Cloud Plugins

A Claude Code plugin marketplace by Pouria Rouzrokh. It hosts one plugin, **pr**: a personal development toolkit for building features and MVPs with documentation that survives between sessions, plus skills for debugging, testing, frontend design, deployment, and Gemini-powered image, SVG, and video generation.

## Installation

Inside Claude Code:

```
/plugin marketplace add PouriaRouzrokh/pr-claude-plugins
/plugin install pr@pr-cloud-plugins
```

To update later:

```
/plugin marketplace update pr-cloud-plugins
```

## Prerequisites

| Tool | Needed by | Setup |
|------|-----------|-------|
| [uv](https://docs.astral.sh/uv/) | `generate-image`, `generate-svg`, `generate-video` | `brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh \| sh`. The scripts declare their own dependencies, so `uv run` installs them automatically. |
| Gemini API key | `generate-image`, `generate-svg`, `generate-video` | Create one at [Google AI Studio](https://aistudio.google.com/apikey) and set `GEMINI_API_KEY` in your environment, the project's `.env` or `.claude/.env`, or `~/.claude/.env`. Video generation needs a paid-tier key. |
| OpenAI API key (optional) | `generate-image` with GPT Image models | Create one at [platform.openai.com](https://platform.openai.com/api-keys) and set `OPENAI_API_KEY` in the same places. OpenAI may require organization verification for image models. |
| Context7 | All development skills (library docs) | `/plugin install context7@claude-plugins-official` |
| Playwright | UI verification in `feature-dev`, `mvp-dev`, `frontend-design` | `/plugin install playwright@claude-plugins-official` |
| Node.js 22+ and Chrome | `web-quality-audit` (Lighthouse, axe), optional `svgo` | Any recent Node install. |
| ffmpeg (optional) | Reviewing and post-processing generated video | `brew install ffmpeg` |
| Agent teams (optional) | `--team` flag on multi-agent skills | Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` under `env` in `settings.json`. |

Without uv, the scripts also run with `python3` (3.10+) after `python3 -m pip install -U "google-genai>=2.3,<3" "openai>=2,<4"`.

## What's Inside

| Plugin | Description |
|--------|-------------|
| [pr](./pr/) | 20 skills (all invocable as `/pr:<name>`) and 3 read-only agents. See the [plugin README](./pr/README.md). |

The plugin follows the **ATLAS** framework (Architect, Trace, Link, Assemble, Stress-test) and keeps project memory in `.claude/checkpoints/`: a PRD, per-feature RFDs, and point-in-time snapshots.

## Upgrading From 1.x

- Slash commands are now skills. `/pr:feature-dev`, `/pr:commit-push`, and the rest work as before.
- `generate-image-nb` is now `generate-image` (still `/pr:generate-image`). It defaults to Nano Banana 2.1; the preview models it used before were shut down in June 2026.
- The JavaScript versions of the Gemini scripts were removed. They could not resolve `@google/genai` from the plugin's install location. Use `uv run` (or `python3`).
- New skills: `generate-video`, `systematic-debugging`, `test-driven-development`, `web-quality-audit`.

## Author

Pouria Rouzrokh
