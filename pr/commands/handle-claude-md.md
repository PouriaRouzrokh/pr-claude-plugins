---
description: Initialize or update CLAUDE.md and project documentation structure. Creates CLAUDE.md, checkpoint folders, and PRD placement for new projects; updates CLAUDE.md and ensures structure integrity for existing ones.
argument-hint: "[optional: path/to/project] [optional: path/to/initial-docs or inline description]"
---

# Handle CLAUDE.md

Initialize or update CLAUDE.md and the `.claude/checkpoints/` documentation structure. Works for both empty/new projects and existing codebases.

## Core Philosophy

**What CLAUDE.md IS**: A stable guide containing development principles, key structural anchors (important files and folders), and instructions for loading project context from documentation.

**What CLAUDE.md is NOT**: A place for implementation details, exhaustive file listings, tech stack specifics, or anything that changes frequently as the project evolves.

**Why**: Implementation details belong in PRDs, RFDs, and snapshots. CLAUDE.md tells Claude *how to find* this information, not duplicate it.

**Writing Quality**: Use the `writing-clearly-and-concisely` skill. Active voice, omit needless words, avoid AI-isms.

---

## Phase 0: Parse Arguments

**Goal**: Identify target scope and any initial documentation input

**Target scope**: $ARGUMENTS

**Parse for**:
1. **A project path** — use as project root (default: current working directory)
2. **Initial documentation** — either:
   - A file path to existing docs (e.g., `prd.md`, `ideas.md`, `requirements.txt`)
   - Inline text description of the project

**Examples**:
- `/pr:handle-claude-md` → Init or update current directory
- `/pr:handle-claude-md ~/projects/myapp` → Target a specific project
- `/pr:handle-claude-md ~/projects/myapp ~/docs/prd.md` → Init with existing PRD
- `/pr:handle-claude-md "A task management app for small teams"` → Init with inline description

---

## Phase 1: Detect Project State

**Goal**: Determine whether this is a new/empty project or an existing codebase

**Actions**:

1. **Check for source files**:

```bash
# Look for common project indicators
ls {project_root}/package.json {project_root}/requirements.txt {project_root}/Cargo.toml {project_root}/go.mod {project_root}/Makefile 2>/dev/null
find {project_root} -maxdepth 2 -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.go" -o -name "*.rs" -o -name "*.java" 2>/dev/null | head -5
```

2. **Check for existing checkpoint structure**:

```bash
ls -d {project_root}/.claude/checkpoints/checkpoint-* 2>/dev/null
```

3. **Check for existing CLAUDE.md**:

```bash
ls {project_root}/CLAUDE.md 2>/dev/null
```

4. **Classify the project state**:

| Has Source Code | Has Checkpoints | Has CLAUDE.md | State |
|-----------------|-----------------|---------------|-------|
| No | No | No | **Empty project** → Phase 2A |
| No | No | Yes | **Partially initialized** → Phase 2A (skip CLAUDE.md creation) |
| Yes | No | No | **Existing codebase, uninitialized** → Phase 2B |
| Yes | No | Yes | **Existing codebase, partial init** → Phase 2B |
| Yes | Yes | Yes | **Fully initialized** → Phase 2C |
| Yes | Yes | No | **Structure exists, missing CLAUDE.md** → Phase 2C |

---

## Phase 2A: Initialize Empty Project

**Goal**: Set up full project documentation structure for a new project

**Actions**:

1. **Create checkpoint structure**:

```bash
mkdir -p {project_root}/.claude/checkpoints/checkpoint-0/rfd
mkdir -p {project_root}/.claude/references
```

2. **Handle initial documentation**:

   - **If user provided a file path**: Read the file.
     - If it looks like a PRD (has sections like "Features", "Requirements", "Architecture", "Problem Statement"): Copy it to `.claude/checkpoints/checkpoint-0/prd.md`
     - Otherwise: Use it as input context for generating a PRD via the `create-prd` skill, saving to `.claude/checkpoints/checkpoint-0/prd.md`

   - **If user provided inline text**: Use it as the project description seed. Ask the user:
     > "I have your project description. Would you like me to:
     > 1. Generate a full PRD from this (runs the `create-prd` skill interactively)
     > 2. Save this description as a minimal PRD placeholder and move on"

   - **If no documentation provided**: Ask the user:
     > "This is an empty project. To set up the documentation structure, I need some initial context. You can:
     > 1. Provide a path to an existing document (PRD, requirements, ideas)
     > 2. Describe the project briefly and I'll generate a PRD
     > 3. Skip the PRD for now (creates the folder structure only)"

3. **Create CLAUDE.md** (if it doesn't exist): Generate using the template from Phase 4, adapted for a new project with no codebase to reference yet.

4. **Report what was created**:
   - Folder structure created
   - PRD status (created / placeholder / skipped)
   - CLAUDE.md created
   - Next steps: "Start building, then run `/pr:create-snapshot` when ready for your first checkpoint"

**Then skip to Phase 5 (Verify Conciseness).**

---

## Phase 2B: Initialize Existing Codebase

**Goal**: Set up documentation structure for an existing codebase that has no checkpoint system

**Actions**:

1. **Create checkpoint structure**:

```bash
mkdir -p {project_root}/.claude/checkpoints/checkpoint-0/rfd
mkdir -p {project_root}/.claude/references
```

2. **Handle PRD**:
   - If user provided a document path, handle it the same as Phase 2A step 2
   - If no document provided, ask:
     > "This existing codebase has no PRD. Would you like to:
     > 1. Create a PRD based on the current codebase (I'll analyze the code and interview you)
     > 2. Provide an existing requirements document to use as the PRD
     > 3. Skip the PRD for now"

3. **Create a snapshot**: The codebase exists but has no snapshot. Inform the user:
   > "I'll create an initial snapshot to capture the current codebase state."

   Then invoke the `create-snapshot` skill to generate `.claude/checkpoints/checkpoint-1/snapshot.md`.

4. **Proceed to Phase 3** to discover and create/update CLAUDE.md files.

---

## Phase 2C: Update Existing Project

**Goal**: Verify structure integrity and update CLAUDE.md for an already-initialized project

**Actions**:

1. **Verify checkpoint structure integrity**:
   - Ensure `.claude/checkpoints/` exists
   - Ensure `.claude/references/` exists
   - Check for sequential checkpoint numbering (no gaps)
   - Check for sequential RFD numbering within each checkpoint
   - If gaps found, warn user

2. **Check for latest snapshot**:

```bash
LATEST_CP=$(ls -d {project_root}/.claude/checkpoints/checkpoint-* 2>/dev/null | sort -V | tail -1)
ls "$LATEST_CP/snapshot.md" 2>/dev/null
```

   - If no snapshot exists in the latest checkpoint, inform the user:
     > "The latest checkpoint has no snapshot. Consider running `/pr:create-snapshot` to capture the current state."

3. **Ensure checkpoint-0 has a PRD**:

```bash
ls {project_root}/.claude/checkpoints/checkpoint-0/prd.md 2>/dev/null
```

   - If missing, note it in the report but don't block — some projects may not need one.

4. **Proceed to Phase 3** to update CLAUDE.md files.

---

## Phase 3: Discover All CLAUDE.md Files

**Goal**: Find all CLAUDE.md files that need updating

**Actions**:

1. Search for all CLAUDE.md files in the project:

```bash
find {project_root} -name "CLAUDE.md" -type f 2>/dev/null | sort
```

2. Common locations:
   - Project root: `CLAUDE.md`
   - Subdirectories: `*/CLAUDE.md`
   - Nested packages: `packages/*/CLAUDE.md`

3. If no CLAUDE.md exists at project root, create one.

4. For each CLAUDE.md found, note its location and scope (whole project, specific package, etc.)

---

## Phase 4: Update CLAUDE.md Files

**Goal**: Update each CLAUDE.md with stable content and documentation pointers

### Read Existing Content First

1. Read each CLAUDE.md file
2. Preserve project-specific customizations that are **stable** (development principles, workflows)
3. Identify implementation details that should be removed

### Check What Documentation Exists

1. Find the latest checkpoint:

```bash
ls -d .claude/checkpoints/checkpoint-* 2>/dev/null | sort -V | tail -1
```

2. Check what exists:
   - PRD at `.claude/checkpoints/checkpoint-0/prd.md`
   - Snapshot at latest checkpoint
   - RFDs at latest checkpoint's `rfd/` folder

3. Note the checkpoint structure for the Context Loading Instructions section

**NOTE**: Do NOT read these documents in detail. You're only checking what exists so CLAUDE.md can point to them.

### Required Sections

Every CLAUDE.md should contain these sections in this order:

1. **Header** - Brief one-line description (what the project is)
2. **Context Loading Instructions** - How to understand the project (CRITICAL - see template)
3. **Development Principles** - How to work on this project
4. **Documentation Hierarchy** - How docs are organized
5. **Key Files/Folders** (optional) - Stable structural anchors that help navigation
6. **Quick Commands** (optional) - Only the most stable, essential commands
7. **Key Concepts** (optional) - Only if there are stable terms/concepts unique to this project

### Context Loading Instructions Section (REQUIRED)

**This is the most important section. It tells Claude how to understand the project:**

```markdown
## Context Loading Instructions

To understand this project, read the documentation in this order:

### 1. Find the Latest Checkpoint

```bash
ls -d .claude/checkpoints/checkpoint-* 2>/dev/null | sort -V | tail -1
```

### 2. Read Project Context

- **If a snapshot exists** in the latest checkpoint: Read `snapshot.md` first - it contains the current technical state
- **If no snapshot exists**: Read the PRD at `.claude/checkpoints/checkpoint-0/prd.md` for project vision and requirements

### 3. Read All RFDs

Check the latest checkpoint's `rfd/` folder for Request for Development documents. These track feature implementations and decisions:

```bash
find .claude/checkpoints/checkpoint-*/rfd -name "*.md" 2>/dev/null | sort -V
```

Read the most recent RFDs to understand current work and decisions.

### Priority Order

1. Latest snapshot (current state)
2. PRD (original vision)
3. Recent RFDs (feature details)
```

### Development Principles Section (REQUIRED)

```markdown
## Development Principles

### Multi-Agent Strategy

When a task benefits from running multiple agents, choose the right approach:

- **Subagents (default)**: Lightweight workers that report results back. Use for independent parallel tasks. Cheaper and sufficient for most work.
- **Agent teams**: Independent sessions with inter-agent messaging. Use only when agents need to communicate or coordinate. Experimental, more expensive.
- Commands that support agents accept `--subagents` or `--team` flags.

### Leveraging Available Tools

Before starting any task, check what skills and MCP servers are available:

- Review available skills for specialized capabilities
- Check available MCP servers for enhanced functionality
- Always use Context7 MCP for library/API documentation without being explicitly asked

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

- Use Playwright for browser automation and testing, if available
- Take screenshots to verify visual changes
- Test user flows and form interactions

### Testing Requirements

Before handing off work:

- Run all relevant tests
- Verify changes work as expected
- Fix any failures or regressions
```

### Documentation Hierarchy Section (REQUIRED)

```markdown
## Documentation Hierarchy

```
.claude/checkpoints/
├── checkpoint-0/          # Pre-development
│   └── prd.md             # Product Requirements Document
└── checkpoint-N/          # Development milestones
    ├── snapshot.md        # Technical codebase snapshot
    └── rfd/               # Feature tracking
        └── {N}-{slug}/    # Individual feature RFDs
```

**Document relationships**: PRD (vision) → RFDs (features) → Snapshots (state) → CLAUDE.md (quick reference)
```

### Key Files/Folders Section (OPTIONAL)

Include only **stable structural anchors** — entry points and key directories:

**What to include:** Main entry points, key directories, configuration locations
**What NOT to include:** Exhaustive file listings, files that change frequently, implementation details

---

## Phase 5: Verify Conciseness

**Goal**: Ensure CLAUDE.md is minimal and stable

**Checklist**:

1. Target length: **under 150 lines** (less is better)
2. No implementation details that will change
3. Context Loading Instructions section is present and complete
4. Development Principles section is present
5. Documentation Hierarchy section is present
6. Content is scannable (headers, bullets, tables)

### Remove These Types of Content

- Detailed project descriptions (beyond one line)
- Technology stack specifics
- Architecture details
- API or endpoint documentation
- Exhaustive file structure listings
- Current development status
- Feature lists
- Configuration details

---

## Phase 6: Save and Report

**Goal**: Apply changes and summarize

**Actions**:

1. Save updates to each CLAUDE.md file

2. Report to user:
   - **Structure created/verified**: Which folders were created or already existed
   - **PRD status**: Created, placed, or missing
   - **Snapshot status**: Exists, just created, or suggested
   - **CLAUDE.md files**: Which were created vs updated, what was changed
   - **Warnings**: Any numbering gaps, missing docs, or structural issues
   - **Next steps**: Suggest relevant commands based on what's missing

---

## What DOES Belong in CLAUDE.md

| Content Type | Example | Why It's Stable |
|-------------|---------|-----------------|
| Context loading instructions | "Read the latest snapshot" | Process doesn't change |
| Development principles | RFD workflow, testing requirements | Workflow is stable |
| Documentation hierarchy | Checkpoint structure | Structure is stable |
| Key files/folders | `src/index.ts` - main entry | Structural anchors rarely change |
| Essential commands | `npm test`, `npm run dev` | Core commands rarely change |
| Key concepts | "RFD = Request for Development" | Terminology is stable |

## What Does NOT Belong in CLAUDE.md

| Content Type | Example | Where It Belongs |
|-------------|---------|------------------|
| Project description | "A marketplace for plugins" | PRD or snapshot |
| Tech stack | "Built with React, Node.js" | Snapshot |
| Architecture details | "Uses MVC pattern with..." | Snapshot |
| API documentation | "Endpoints: GET /users..." | Snapshot or references |
| Exhaustive file listings | "src/ has 15 components..." | Snapshot |
| Current status | "MVP complete, working on..." | RFDs |

---

## Safety Guidelines

**DO NOT:**

- Add implementation details that will change
- Duplicate content from PRD, snapshots, or RFDs
- Make CLAUDE.md longer than 150 lines
- Remove the Context Loading Instructions section
- Overwrite user-provided PRDs without confirmation
- Make git commits or push changes

**DO:**

- Always include Context Loading Instructions
- Always include Development Principles
- Always include Documentation Hierarchy
- Create missing folder structure automatically
- Keep content minimal and stable
- Point to detailed docs rather than duplicating
