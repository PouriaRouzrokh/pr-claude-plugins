---
name: handle-claude-md
description: "Initializes or updates CLAUDE.md and the .claude/checkpoints documentation structure. For new projects it creates the structure and places or generates the PRD; for existing codebases it sets up checkpoints and triggers a first snapshot; for initialized projects it checks structure integrity and refreshes CLAUDE.md to a concise, stable guide. Use when setting up a project for this workflow or when CLAUDE.md has drifted."
argument-hint: "[optional: path/to/project] [optional: path/to/initial-docs or inline description]"
allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/shared/checkpoint.py *)
---

# Handle CLAUDE.md

CLAUDE.md is loaded into every session, so every line costs context in every conversation. Keep it to what is stable and universally useful: how to load project context, how to work on this project, where things are, and the few commands everyone needs. Implementation details change and belong in the PRD, RFDs, and snapshots, which CLAUDE.md points to.

**Arguments**: $ARGUMENTS. They may contain a project path (default: the current directory) and initial documentation, either a file path (PRD, ideas, requirements) or an inline description.

Documentation conventions are in `${CLAUDE_PLUGIN_ROOT}/shared/checkpoint-system.md`; the helper is `python3 ${CLAUDE_PLUGIN_ROOT}/shared/checkpoint.py` (add `--root <path>` for another project). Use `writing-clearly-and-concisely` for the prose.

## Phase 1: Detect the Project State

Check for source code (package manifests, source files), run `checkpoint.py status`, and look for instruction files (`find . \( -name CLAUDE.md -o -name AGENTS.md -o -name CLAUDE.local.md \) -not -path '*/node_modules/*'`) and a `.claude/rules/` folder.

Claude Code reads `AGENTS.md` only when no `CLAUDE.md` exists, so creating a CLAUDE.md next to an existing AGENTS.md would hide it. In that case, start the new CLAUDE.md with an `@AGENTS.md` import line and put only Claude-specific content below it.

| Source code | Checkpoints | Next |
|-------------|-------------|------|
| No | No | Phase 2A: new project |
| Yes | No | Phase 2B: existing codebase |
| Yes or No | Yes | Phase 2C: initialized project |

## Phase 2A: New Project

1. Run `checkpoint.py init` to create `checkpoint-0/rfd/` and `references/`.
2. Handle the initial documentation:
   - A file that already reads as a PRD (problem, users, requirements, features): copy it to `checkpoint-0/prd.md`.
   - Other notes or an inline description: offer to run `create-prd` with them as input, or to save a short placeholder PRD for now.
   - Nothing: ask whether the user wants to provide a document, describe the project for a PRD, or skip the PRD.
3. Continue with Phase 3.

## Phase 2B: Existing Codebase

1. Ask whether to add a PRD: written from the code plus an interview (`create-prd`), from an existing document, or skipped. If one is added, run `checkpoint.py init` and save it as `checkpoint-0/prd.md`; otherwise just create `.claude/references/`.
2. Run the `create-snapshot` skill to capture the current state as checkpoint-1. New RFDs will go there.
3. Continue with Phase 3.

## Phase 2C: Initialized Project

1. Review the `checkpoint.py status` output: report numbering gaps or duplicates, checkpoints missing a snapshot, and a missing PRD. Do not renumber or create documents without asking.
2. If many RFDs were completed since the latest snapshot, suggest `/pr:create-snapshot`.
3. Continue with Phase 3.

## Phase 3: Write or Update CLAUDE.md

For each CLAUDE.md found (root, packages, subprojects), read it and keep what is stable and project-specific: development principles the user wrote, conventions, essential commands, structural anchors. Remove what will go stale: stack descriptions, feature lists, status, architecture detail, API documentation, exhaustive file listings.

Detect the project's essential commands (install, dev server, test, lint, build) from its manifests and scripts; include only those.

A root CLAUDE.md contains these sections in order. Adapt the wording to the project; do not copy the template blindly.

````markdown
# CLAUDE.md

{One line: what this project is.}

## Context Loading

Before starting work, load the project's memory from `.claude/checkpoints/`:

1. Find the latest checkpoint: `ls -d .claude/checkpoints/checkpoint-* | sort -V | tail -1`
2. Read its `snapshot.md` (current technical state). Without a snapshot, read `.claude/checkpoints/checkpoint-0/prd.md`.
3. Read the RFDs related to your task: `find .claude/checkpoints -path '*/rfd/*' -name 'rfd-*.md' | sort -V`

Priority: latest snapshot, then the PRD, then recent RFDs.

## Development Principles

- **Plan before building.** For features, significant fixes, and architectural changes, write or update an RFD before coding (`/pr:feature-dev` manages this). Path: `.claude/checkpoints/checkpoint-{C}/rfd/{N}-{slug}/rfd-{YYYY-MM-DD}-{HHMM}.md`, where `{C}` is the latest checkpoint and `{N}` the next RFD number in it.
- **Match rigor to the task** (ATLAS): full process for new features with integrations or schema changes; lighter for changes that follow existing patterns; none for one-line fixes.
- **Find the root cause before fixing bugs**, and add a regression test (`systematic-debugging`, `test-driven-development`).
- **Verify with evidence.** Run the tests, exercise the behavior, and check UI changes in a browser at mobile and desktop widths before calling work done. Report actual results.
- **Look up library and API behavior** in current documentation (Context7 MCP when available) instead of relying on memory.
- **Leave it clean.** Remove temporary scripts, debug output, and test data; keep real tests. Code should read as if a careful senior engineer wrote it.
- **Agents**: use subagents for independent parallel exploration and review; use agent teams only when agents must coordinate.
- Writing to `.claude/` prompts for permission; allow edits to `.claude/` for the session when asked.

## Documentation

```
.claude/checkpoints/
├── checkpoint-0/          # prd.md + RFDs before the first snapshot
└── checkpoint-N/          # snapshot.md (never edited) + RFDs for later work
.claude/references/        # Guidelines and specs
```

PRD (vision) → RFDs (features and decisions) → snapshots (state) → CLAUDE.md (how to work here)

## Commands

| Task | Command |
|------|---------|
| {Install / Dev / Test / Lint / Build} | `{command}` |

## Key Locations

- `{path}` — {why it matters}
````

- **Commands** and **Key Locations** are optional; include them only with stable, essential entries (entry points, main source and test folders, configuration).
- A package-level CLAUDE.md covers only what differs for that package; it does not repeat the root file. Rules that apply only to certain files (for example API handlers or tests) can go in `.claude/rules/<topic>.md` with a `paths:` list in its frontmatter instead; Claude Code loads them only when it works on matching files.
- Preserve user-written rules even when they don't fit a section; put them under Development Principles.

## Phase 4: Check

- Root CLAUDE.md under ~100 lines; nothing that changes as features land.
- Context Loading, Development Principles, and Documentation sections present.
- Every command listed actually runs (try the cheap ones).
- No duplication of PRD, snapshot, or RFD content.

In the report, suggest that the user run `/doctor prompt-audit`, which checks instruction files for outdated or conflicting content and proposes edits without applying them.

## Phase 5: Report

Summarize: structure created or verified, PRD status, snapshot status, CLAUDE.md files created or updated (with the main changes), warnings, and next steps (`/pr:create-prd`, `/pr:create-snapshot`, `/pr:feature-dev`). Do not commit.
