# CLAUDE.md

Claude Code plugin marketplace containing the **pr** plugin: a personal development toolkit of skills for feature and MVP development, debugging, testing, cleanup, documentation, deployment, git, frontend design, and Gemini image/SVG/video generation.

## Skills

All skills live in `pr/skills/<name>/SKILL.md` and run as `/pr:<name>`. There is no `commands/` directory: slash commands are skills.

| Skill | Purpose |
|-------|---------|
| `feature-dev`, `mvp-dev` | Feature and MVP development with RFD tracking (multi-agent) |
| `create-prd`, `create-snapshot`, `handle-claude-md`, `update-docs` | PRD, snapshots, CLAUDE.md, documentation |
| `systematic-debugging`, `test-driven-development` | Root-cause debugging; TDD with a verification gate (vendored from obra/superpowers) |
| `clean-codebase`, `web-quality-audit` | Code cleanup; Lighthouse/axe audits |
| `run-local`, `run-public`, `commit-push` | Run, deploy, commit (`run-public` and `commit-push` are user-invoked only) |
| `frontend-design`, `agentation` | UI design playbooks and React rules; annotation toolbar |
| `generate-image`, `generate-svg`, `generate-video` | Gemini API scripts (Nano Banana 2.1/Pro, Gemini 3.8 Flash, Omni Flash) |
| `atlas-development`, `writing-clearly-and-concisely` | ATLAS reference; prose quality |

## Quick Commands

| Task | Command |
|------|---------|
| Validate plugin and marketplace | `claude plugin validate ./pr && claude plugin validate .` |
| Test the Gemini scripts (offline, no API key) | `uv run --with pytest --with "google-genai>=2.3,<3" --with resvg-py pytest tests -q` |
| Try the working tree in Claude Code | `claude --plugin-dir ./pr` |

## Development Principles

### ATLAS Framework

ATLAS is a development philosophy — apply it based on task complexity:

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

**Anti-patterns:** Building before designing, skipping connection validation, no testing.

See `atlas-development` skill for complete framework details.

### Multi-Agent Strategy

When a task benefits from running multiple agents, choose the right approach:

- **Subagents (default)**: Lightweight workers that report results back. Use for independent parallel tasks — exploration, architecture proposals, code review. Cheaper and sufficient for most work.
- **Agent teams**: Independent sessions with inter-agent messaging. Use only when agents need to communicate, challenge each other, or coordinate (e.g., architecture debates, cross-layer coordination, adversarial review). Experimental, more expensive, higher coordination overhead.
- **User override**: Commands that support agents accept `--subagents` or `--team` flags. Respect the user's choice, but warn if the flag adds unnecessary overhead for the task.

**Priority**: Always default to subagents. Only propose agent teams when inter-agent communication has a clear benefit. See `atlas-development` skill for per-phase guidance.

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

- Use Playwright for browser automation and testing (`/plugin install playwright@claude-plugins-official`)
- Take screenshots to verify visual changes
- Test user flows and form interactions

### Testing & Code Quality Requirements

Before handing off work:

- **Test proactively**: Run your own code — call endpoints, execute functions, verify behavior
- Run all relevant test suites and verify they pass
- Fix any failures or regressions
- **Clean up test artifacts**: Remove all temporary scripts, debug statements, console.logs, and test data
- **Professionalize code**: Review every file changed for professional quality — no redundancies, no dead code, proper commenting, consistent naming, clean structure
- Code should read as if written by a senior engineer: well-organized, well-named, easy to follow

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
├── .claude-plugin/marketplace.json   # Marketplace manifest (version must match plugin.json)
├── pr/                               # The pr plugin
│   ├── .claude-plugin/plugin.json    # Plugin manifest
│   ├── agents/                       # code-explorer, code-architect, code-reviewer
│   └── skills/<name>/                # SKILL.md + references/, scripts/, NOTICE.md
├── tests/                            # Offline pytest suite for the Gemini scripts (not shipped)
├── CLAUDE.md
├── commitlog.md
└── README.md
```

## Plugin Conventions

**Skills** (`pr/skills/<name>/SKILL.md`):

```yaml
---
name: skill-name                  # must match the directory name
description: "What it does. Use when ..."   # third person, <= 1024 chars; quote it if it contains ': '
argument-hint: "[optional: hint]"
disable-model-invocation: true    # only for skills with outward side effects (deploy, push)
allowed-tools: Bash(uv run ${CLAUDE_SKILL_DIR}/scripts/x.py *)
license: "..."                    # vendored skills: upstream license + See NOTICE.md
---
```

- Keep SKILL.md under 500 lines; move templates and long material to `references/` (one level deep, table of contents when over 100 lines).
- Reference bundled files as `${CLAUDE_SKILL_DIR}/scripts/...` inside SKILL.md; Claude Code substitutes the absolute path. Reference files are not substituted.
- Scripts are Python with PEP 723 inline dependencies so `uv run` works from any project. Do not add Node scripts that import npm packages: they cannot resolve modules from the plugin cache.
- Vendored content keeps its upstream license in the skill's `NOTICE.md`.
- Bump `version` in both manifests on every release, or installed copies will not update.

**Agents** (`pr/agents/*.md`): read-only via `disallowedTools: Write, Edit, NotebookEdit`; they keep Bash for git and search, and inherit MCP tools such as Context7.

**Gemini model IDs** live in each script's `MODELS` dict. Verify them against https://ai.google.dev/gemini-api/docs/models before changing; preview IDs get shut down.

## Agent Colors

| Agent          | Color  | Purpose                                        |
| -------------- | ------ | ---------------------------------------------- |
| code-explorer  | Yellow | Traces execution paths, returns 5-10 key files |
| code-architect | Green  | Designs implementations with blueprints        |
| code-reviewer  | Red    | Reviews code, reports issues ≥80% confidence   |

## Key Concepts

- **ATLAS**: Development framework — Architect, Trace, Link, Assemble, Stress-test
- **RFD**: Request for Development - tracks feature requests and implementation
- **PRD**: Product Requirements Document - project vision at `checkpoint-0/prd.md`
- **Checkpoint**: Point-in-time documentation (checkpoint-0 = pre-dev, checkpoint-1+ = development)
- **commitlog.md**: Project commit history maintained by `/pr:commit-push`
