# PR Plugin

A personal development toolkit for Claude Code: ATLAS-guided feature and MVP development with RFD tracking, systematic debugging and TDD, code cleanup, documentation, local and public deployment, git workflows, frontend design, web quality audits, and Gemini-powered image, SVG, and video generation.

## Installation

```
/plugin install pr --marketplace PouriaRouzrokh/pr-claude-plugins
```

or, after `/plugin marketplace add PouriaRouzrokh/pr-claude-plugins`, run `/plugin install pr@pr-cloud-plugins`. Prerequisites (uv, a Gemini API key, Context7, Playwright) are listed in the [marketplace README](../README.md#prerequisites).

## Skills

Every skill can be run as `/pr:<name>`. Claude also loads most of them automatically when a task matches; `commit-push` and `run-public` run only when you invoke them, because they push code and deploy.

### Development workflow

| Skill | What it does | Agents |
|-------|--------------|--------|
| `/pr:create-prd [ideas]` | Interviews you, researches the stack, and writes a PRD to `checkpoint-0/prd.md` | Research |
| `/pr:mvp-dev [focus]` | Builds an MVP from the PRD one feature at a time, each with an RFD, tests, and your sign-off | Yes |
| `/pr:feature-dev [desc]` | Explores, clarifies, designs, implements, tests, and documents one feature in an RFD | Yes |
| `/pr:systematic-debugging` | Root cause first: reproduce, gather evidence, test one hypothesis, fix with a regression test | |
| `/pr:test-driven-development` | Red-green-refactor plus a verification gate before any "done" claim | |
| `/pr:atlas-development` | The ATLAS framework reference (Architect, Trace, Link, Assemble, Stress-test) | |

### Quality and documentation

| Skill | What it does | Agents |
|-------|--------------|--------|
| `/pr:clean-codebase [path]` | Removes dead code, stale comments, and outdated docstrings without changing behavior | Yes |
| `/pr:update-docs [path] [focus]` | Brings README, API docs, and RFDs in line with the code | Yes |
| `/pr:create-snapshot [path]` | Writes a technical snapshot to a new checkpoint | Yes |
| `/pr:handle-claude-md [path] [docs]` | Creates or updates CLAUDE.md and the checkpoint structure | |
| `/pr:writing-clearly-and-concisely` | Strunk's rules and a catalog of AI-writing tells for any prose | |
| `/pr:web-quality-audit [url]` | Lighthouse and axe measurements: Core Web Vitals, WCAG 2.2 AA, SEO | |

### Ship

| Skill | What it does |
|-------|--------------|
| `/pr:run-local [instructions]` | Detects the stack, prepares the environment, and starts services as background tasks |
| `/pr:run-public [instructions]` | Builds and deploys to preview, staging, or production; confirms before production |
| `/pr:commit-push [path] [--merge\|--pr]` | Commits, prepends a `commitlog.md` entry, pushes, and optionally merges or opens a PR |

### Design and media

| Skill | What it does |
|-------|--------------|
| `/pr:frontend-design` | Distinctive, production-grade UI: design process, craft floor, critique/audit/polish playbooks, Vercel's React rules, Tailwind v4 |
| `/pr:generate-image [desc]` | Nano Banana 2.1 / Pro image generation and editing, with search grounding and conversational refinement |
| `/pr:generate-svg [desc]` | Gemini-written SVGs (hero, icon, illustration, logo, component), validated, sanitized, and previewed as PNG |
| `/pr:generate-video [desc]` | Gemini Omni Flash clips: text-to-video, image-to-video, editing, and extension |
| `/pr:agentation [mcp\|manual]` | Adds the Agentation annotation toolbar to a React app, optionally synced to Claude through MCP |

## Agents

Three read-only subagents support the multi-agent skills. They can read, search, run read-only shell commands (git, ls, rg), and look up documentation, but cannot edit files.

| Agent | Model | Purpose |
|-------|-------|---------|
| `code-explorer` | Sonnet | Traces execution paths and returns the 5–10 files essential to a topic |
| `code-architect` | Session model | Designs implementation blueprints that follow existing patterns |
| `code-reviewer` | Session model | Reviews changes and reports only issues at ≥80% confidence |

## ATLAS Development Framework

| Step | Phase | Purpose |
|------|-------|---------|
| **A** | Architect | Define the problem, users, and success metrics |
| **T** | Trace | Data schema, integrations map, stack proposal |
| **L** | Link | Validate every connection before building |
| **A** | Assemble | Build with layered architecture |
| **S** | Stress-test | Test functionality and error handling, then verify with evidence |

Use full ATLAS for new MVPs and features with integrations or schema changes, the last three steps for features that reuse existing patterns, and skip it for bug fixes (use `systematic-debugging`), one-line changes, and docs.

## Multi-Agent Strategy

Skills marked "Yes" above launch agents in parallel and accept a flag:

| Flag | Behavior |
|------|----------|
| *(none)* | Claude decides; defaults to subagents |
| `--subagents` | Always use subagents: lightweight workers that report back |
| `--team` | Use an [agent team](https://code.claude.com/docs/en/agent-teams): separate sessions that message each other. Experimental; requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` |

Teams cost more and add coordination overhead. They pay off mainly in architecture debates (`feature-dev`, `mvp-dev`) and cross-cutting integration reviews.

## Documentation Structure

The workflow skills keep project memory in the project itself:

```
.claude/
├── checkpoints/
│   ├── checkpoint-0/            # Before development
│   │   ├── prd.md               # Product Requirements Document
│   │   └── rfd/{N}-{feature}/rfd-{YYYY-MM-DD}-{HHMM}.md
│   └── checkpoint-{N}/          # Development milestones
│       ├── snapshot.md          # Immutable technical snapshot
│       └── rfd/
└── references/                  # Guidelines, specs, package docs
```

- **PRD**: product vision and requirements.
- **RFD** (Request for Development): one per feature or significant fix, covering request, plan, decisions, tests, and files changed.
- **Snapshot**: the codebase state at a point in time; never edited after creation.

## Typical Workflows

- **New project**: `/pr:handle-claude-md` → `/pr:create-prd` → `/pr:mvp-dev` → `/pr:create-snapshot`
- **New feature**: `/pr:feature-dev <description>` → `/pr:commit-push --pr`
- **Bug**: describe it; `systematic-debugging` and `test-driven-development` guide the fix
- **Before a release**: `/pr:web-quality-audit` → `/pr:run-public`
- **Maintenance**: `/pr:clean-codebase`, `/pr:update-docs`, `/pr:create-snapshot`

## Third-Party Content

Several skills adapt open-source work; each skill folder's `NOTICE.md` has the details and license text:

- `frontend-design`: Anthropic's frontend-design and Paul Bakaus's impeccable (Apache-2.0); Vercel's react-best-practices and Seth Hobson's tailwind-design-system (MIT)
- `systematic-debugging`, `test-driven-development`: obra/superpowers (MIT)
- `web-quality-audit`: addyosmani/web-quality-skills (MIT)
- `writing-clearly-and-concisely`: softaworks/agent-toolkit (MIT); Wikipedia's "Signs of AI writing" (CC BY-SA 4.0)
- `agentation`: benjitaylor/agentation (PolyForm Shield 1.0.0)

## Version

2.0.0

## Author

Pouria Rouzrokh
