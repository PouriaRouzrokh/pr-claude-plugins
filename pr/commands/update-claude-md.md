---
description: Update CLAUDE.md files with development principles, key structure, and documentation pointers
argument-hint: "[optional: path/to/project]"
---

# Update CLAUDE.md

Update all CLAUDE.md files in the project to contain **stable content**: development principles, key files/folders, and instructions for finding detailed documentation.

## Core Philosophy

**What CLAUDE.md IS**: A stable guide containing development principles, key structural anchors (important files and folders), and instructions for loading project context from documentation.

**What CLAUDE.md is NOT**: A place for implementation details, exhaustive file listings, tech stack specifics, or anything that changes frequently as the project evolves.

**Why**: Implementation details belong in PRDs, RFDs, and snapshots. These documents are updated as the project changes. CLAUDE.md should tell Claude *how to find* this information, not duplicate it.

**Writing Quality**: Use the `writing-clearly-and-concisely` skill. Apply Strunk's principles: active voice, omit needless words, be specific. Avoid AI-isms (pivotal, crucial, leverage, robust, seamless).

---

## Phase 0: Parse Arguments

**Goal**: Identify target scope

**Target scope**: $ARGUMENTS

- If a path is provided, use that as the project root
- If no path is provided, use the current working directory

---

## Phase 1: Discover All CLAUDE.md Files

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

3. For each CLAUDE.md found, note:
   - Its location
   - What scope it covers (whole project, specific package, etc.)

---

## Phase 2: Read Existing CLAUDE.md Files

**Goal**: Understand current state of each file

**Actions**:

1. Read each CLAUDE.md file found in Phase 1
2. Note existing sections and structure
3. Preserve project-specific customizations that are **stable** (development principles, workflows)
4. Identify implementation details that should be removed

---

## Phase 3: Check Checkpoint Structure

**Goal**: Verify what documentation exists to point to

**Actions**:

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

---

## Phase 4: Update CLAUDE.md Files

**Goal**: Update each CLAUDE.md with stable content and documentation pointers

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

Include only **stable structural anchors** - entry points and key directories that help Claude navigate:

```markdown
## Key Files/Folders

| Path | Purpose |
|------|---------|
| `src/index.ts` | Main entry point |
| `src/config/` | Configuration files |
| `commands/` | Slash command definitions |
| `agents/` | Agent definitions |
```

**What to include:**
- Main entry points
- Key directories that organize major functionality
- Configuration locations
- Files/folders Claude needs to know about to work effectively

**What NOT to include:**
- Exhaustive file listings
- Every subdirectory
- Files that change frequently
- Implementation details about what's in each file

---

## Phase 5: Remove Implementation Details

**Goal**: Ensure CLAUDE.md contains only stable content

**Remove these types of content**:

- Detailed project descriptions (beyond one line)
- Technology stack specifics
- Architecture details
- API or endpoint documentation
- Exhaustive file structure listings (keep only key structural anchors)
- Current development status
- Feature lists
- Configuration details
- Database schema information
- Implementation details
- Anything that would change as the project evolves

**Keep only**:

- One-line project description
- Context loading instructions
- Development principles and workflows
- Documentation hierarchy
- Key files/folders (structural anchors, not exhaustive listings)
- Truly stable commands (if the project has them)
- Key concept definitions (only if stable and unique to project)

---

## Phase 6: Verify Conciseness

**Goal**: Ensure CLAUDE.md is minimal and stable

**Checklist**:

1. Target length: **under 150 lines** (less is better)
2. No implementation details that will change
3. Context Loading Instructions section is present and complete
4. Development Principles section is present
5. Documentation Hierarchy section is present
6. Content is scannable (headers, bullets, tables)

---

## Phase 7: Save and Report

**Goal**: Apply changes and summarize

**Actions**:

1. Save updates to each CLAUDE.md file

2. Report to user:
   - Which CLAUDE.md files were updated
   - What was removed (implementation details)
   - What was added (context loading instructions)
   - Confirmation that checkpoint documentation exists to point to

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
| Feature list | "Supports X, Y, Z features" | PRD or snapshot |
| Configuration details | "Environment variables..." | Snapshot or references |
| Implementation details | "Uses Redux for state..." | Snapshot |

---

## Example CLAUDE.md Structure

```markdown
# CLAUDE.md

Brief one-line description of what this project is.

## Context Loading Instructions

[Include the full Context Loading Instructions section from Phase 4]

## Development Principles

[Include the full Development Principles section from Phase 4]

## Documentation Hierarchy

[Include the Documentation Hierarchy section from Phase 4]

## Key Files/Folders

| Path | Purpose |
|------|---------|
| `src/index.ts` | Main entry point |
| `src/config/` | Configuration |
| `commands/` | Slash commands |

## Quick Commands

| Task  | Command       |
|-------|---------------|
| Dev   | `npm run dev` |
| Test  | `npm test`    |
| Build | `npm run build` |

## Key Concepts

- **RFD**: Request for Development - tracks feature implementations
- **PRD**: Product Requirements Document - project vision
- **Checkpoint**: Point-in-time documentation snapshot
```

---

## Safety Guidelines

**DO NOT:**

- Add implementation details that will change
- Duplicate content from PRD, snapshots, or RFDs
- Make CLAUDE.md longer than 150 lines
- Remove the Context Loading Instructions section
- Create new CLAUDE.md files (only update existing ones)

**DO:**

- Always include Context Loading Instructions
- Always include Development Principles
- Always include Documentation Hierarchy
- Keep content minimal and stable
- Point to detailed docs rather than duplicating
