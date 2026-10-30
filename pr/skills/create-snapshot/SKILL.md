---
name: create-snapshot
description: "Writes a comprehensive technical snapshot of a codebase into a new checkpoint (.claude/checkpoints/checkpoint-N/snapshot.md): reads the PRD, previous snapshots, RFDs, and references, explores the code with four parallel pr:code-explorer agents (architecture, features, development context, and UI/UX or ML pipeline), compares with the previous checkpoint, and fills the snapshot template. Runs in its own context so the exploration does not fill the conversation. Use for handoffs, milestones, after an MVP, or when onboarding an existing codebase."
argument-hint: "[optional: path/to/project]"
context: fork
agent: general-purpose
background: false
allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/shared/checkpoint.py *)
---

# Create Snapshot

Write a snapshot that lets a developer who has never seen this project understand it fully: what it is for, how it is built, how it looks and behaves, how to run and change it, and how it got here. You are running in a separate context without the main conversation, and you cannot ask the user questions, so make reasonable decisions yourself and explain them in your final report.

**Project root**: $ARGUMENTS (empty means the current directory)

Documentation conventions are in `${CLAUDE_PLUGIN_ROOT}/shared/checkpoint-system.md`; read it first. The helper is `python3 ${CLAUDE_PLUGIN_ROOT}/shared/checkpoint.py` (pass `--root <path>` when a path was given).

## Rules

- **Never edit an earlier snapshot.** Snapshots are point-in-time records. Always create a new checkpoint, even if little has changed; record what changed in the new snapshot instead.
- Do not edit the PRD, RFDs, or reference documents. Read them for context only.
- Be specific: real file paths, function names, configuration values, versions, hex colors, commands.
- Be complete rather than brief. If a topic needs three paragraphs, write three. Mark a section "N/A — reason" instead of dropping it.

## Phase 1: Check the Project

1. Run `checkpoint.py status`.
2. If the project has no source code yet (no package manifest, no source files), do not create a checkpoint. Finish with a report recommending `/pr:create-prd` for a new project.
3. Note any numbering gaps or checkpoints without snapshots from the status output; mention them in your final report but do not renumber anything.

## Phase 2: Read Existing Documentation

Read, in order: the PRD (`checkpoint-0/prd.md`), the most recent previous snapshot (and skim older ones for how the project evolved), every RFD across all checkpoints (status, decisions, files), and every file under `.claude/references/`. Also read the project's CLAUDE.md and README.

Extract: the product vision, how the codebase evolved, which features are completed or in progress, design decisions and their reasons, known issues and technical debt, team guidelines.

## Phase 3: Explore the Code

Launch four `pr:code-explorer` agents in parallel. Give each the project root and ask for detailed findings with file:line references plus the 5–10 files most essential to its topic.

1. **Architecture**: directory structure and module boundaries, stack and versions (from manifests and lockfiles), design patterns, configuration and build, entry points and main execution flows, data model and storage, API surface.
2. **Features**: every user-facing feature with its implementation, partially implemented work (TODOs, flags, stubs), planned work mentioned in code or docs, key components and responsibilities.
3. **Development context**: tests (framework, locations, coverage, how to run), CI/CD and deployment, scripts and developer workflow, dependencies and external services, security-relevant code (auth, secrets handling), known issues and technical debt.
4. **Choose by project type**:
   - *Projects with a UI*: the design system and component library, color tokens (with values), typography, spacing scale, component styles, icons and media assets, animation, responsive breakpoints, accessibility, theming, CSS architecture.
   - *ML and data projects without a UI*: datasets and their sources, preprocessing and feature pipelines, model architectures, training configuration and entry points, experiment tracking, evaluation metrics and latest results, model artifacts and where they live, inference or serving path, reproducibility (seeds, environment, data versioning).

Read the files the agents return, plus anything else needed to fill gaps in their findings.

## Phase 4: Compare With the Previous Checkpoint

If there is an earlier snapshot, list what changed since then: new features (with their RFDs), modified or refactored areas, bug fixes, dependency upgrades, architecture and configuration changes. Use `git log` between the snapshot's date and now to catch changes that no RFD recorded, and point those out explicitly. For the first snapshot, say so.

## Phase 5: Write the Snapshot

1. Create the checkpoint with `checkpoint.py new-checkpoint` and note its number.
2. Write `snapshot.md` in it, following the template at `${CLAUDE_SKILL_DIR}/template.md` section by section:

   Executive summary · changes since the last checkpoint · user context · vision and goals · feature inventory · architecture and system design · key components · UI design · UX design · development guidelines · testing · deployment and operations · security · dependencies and external services · known issues and technical debt · RFD summary · references summary · glossary · quick reference.

   For ML projects without a UI, replace the UI and UX sections with "Data and model pipeline" and "Experiments and evaluation", covering the findings from the fourth explorer.
3. Use ASCII diagrams for architecture and data flow where they help, short code excerpts where they clarify, and links to RFDs wherever a feature is discussed.

Writing the file under `.claude/` may trigger a permission prompt; that is expected.

## Phase 6: Report

Finish with a short report for the main conversation: the snapshot path and checkpoint number, a summary of the project's current state, the most important changes since the last checkpoint, changes that no RFD documents, numbering issues found, and any assumptions you made.
