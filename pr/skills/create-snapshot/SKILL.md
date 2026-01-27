---
name: create-snapshot
description: Generate comprehensive technical snapshot of a codebase using code-explorer agents for deep analysis. Reads existing checkpoints, PRDs, RFDs, and references to build context. Saves to .claude/checkpoints/checkpoint-N/snapshot.md with auto-incrementing checkpoint numbers.
argument-hint: "[optional: path/to/project]"
---

# Project Snapshot Generator

Generate a comprehensive technical snapshot of a codebase that serves as a complete handoff document for developers unfamiliar with the project, using code-explorer agents for deep analysis.

## Core Principles

- **Read existing context first**: Always read PRDs, previous snapshots, and RFDs before exploring
- **Use agents for depth**: Launch code-explorer agents to understand codebase deeply
- **Be specific**: Use actual file paths, function names, and code references
- **Track evolution**: Note how things have changed from previous checkpoints

---

## Phase 0: Determine Target

**Goal**: Identify project root

**Target Directory**: $ARGUMENTS

- If `$ARGUMENTS` is provided, use that path as the project root
- If no argument is provided, use the current working directory

**Output Location**: `{project_root}/.claude/checkpoints/checkpoint-{N}/snapshot.md`

---

## Phase 1: Checkpoint Setup

**Goal**: Determine checkpoint number and create directory

**Actions**:

1. Check if `.claude/checkpoints/` directory exists

2. If it doesn't exist, create it and use `checkpoint-1`

3. If it exists, count existing checkpoint folders and increment:

```bash
CHECKPOINT_COUNT=$(find {project_root}/.claude/checkpoints -maxdepth 1 -type d -name "checkpoint-*" 2>/dev/null | wc -l)
NEXT_CHECKPOINT=$((CHECKPOINT_COUNT + 1))
```

4. Create the new checkpoint directory: `.claude/checkpoints/checkpoint-{N}/`

---

## Phase 2: Read Existing Documentation

**Goal**: Build context from existing documentation before exploring

**CRITICAL**: This phase must complete before codebase exploration.

**Actions**:

1. **List all existing checkpoints**:
```bash
ls -d {project_root}/.claude/checkpoints/checkpoint-* 2>/dev/null | sort -V
```

2. **For each checkpoint (in order), read**:
   - `prd.md` (if exists, typically in checkpoint-0)
   - `snapshot.md` (if exists)
   - All RFDs in the `rfd/` folder:
   ```bash
   find {project_root}/.claude/checkpoints/checkpoint-*/rfd -name "rfd-*.md" 2>/dev/null | sort
   ```

3. **Read all reference documents**:
```bash
find {project_root}/.claude/references -name "*.md" 2>/dev/null | sort
```

4. **Extract insights from existing documentation**:
   - Project vision and goals (from PRD)
   - Evolution of the codebase (from snapshots)
   - Feature requests and their implementation status (from RFDs)
   - Design decisions made along the way
   - Known issues and technical debt mentioned previously
   - Team guidelines and coding standards (from references)
   - Internal tooling and package usage (from references)
   - Workflow procedures (from references)

---

## Phase 3: Codebase Exploration with Agents

**Goal**: Deep understanding of the current codebase using code-explorer agents

**Actions**:

1. Launch 3 code-explorer agents in parallel with different focuses:

   **Agent 1 - Architecture Overview**:
   ```
   Analyze the overall architecture of this codebase. Focus on:
   - Directory structure and module organization
   - Technology stack (frontend, backend, database, infrastructure)
   - Design patterns and architectural decisions
   - Configuration and build setup
   - Entry points and main execution flow

   Return a list of 5-10 key architectural files to read.
   ```

   **Agent 2 - Feature Analysis**:
   ```
   Identify and analyze all features in this codebase. Focus on:
   - Completed features and their implementation
   - In-progress features (partial implementation, TODOs)
   - Planned features (mentioned in docs/comments)
   - Key components and their responsibilities

   Return a list of 5-10 key feature files to read.
   ```

   **Agent 3 - Development Context**:
   ```
   Analyze the development context of this codebase. Focus on:
   - Testing strategy and coverage
   - Deployment and CI/CD setup
   - Development workflow (scripts, commands)
   - Dependencies and third-party integrations
   - Known issues and technical debt

   Return a list of 5-10 key development files to read.
   ```

2. Wait for all agents to complete

3. Read all key files identified by agents

4. Synthesize findings into comprehensive understanding

---

## Phase 4: Compare with Previous Checkpoint

**Goal**: Identify changes since last snapshot

**Actions**:

1. If this is not checkpoint-1:
   - Compare current state with previous snapshot
   - Identify new features implemented
   - Note features modified or refactored
   - List bug fixes
   - Document dependency updates
   - Highlight architecture changes
   - Note configuration changes

2. If this is checkpoint-1:
   - Note: "First codebase snapshot - no previous checkpoint to compare."

---

## Phase 5: Generate Snapshot

**Goal**: Write comprehensive snapshot document

**Actions**:

Generate the snapshot following the template structure (see supporting template.md).

Key sections to include:

1. **Executive Summary** - Project overview, status, checkpoint info
2. **Changes Since Last Checkpoint** - What's new since previous snapshot
3. **User Context** - Target users, needs, use cases
4. **Project Vision & Goals** - Core purpose, objectives, philosophy
5. **Features Inventory** - Completed, in-progress, and planned features
6. **Architecture & System Design** - High-level architecture, tech stack, data flow
7. **Key Components Deep Dive** - Detailed component documentation
8. **Design & UX** - Design system, theming, responsive design, accessibility
9. **Development Guidelines** - Coding conventions, patterns, environment setup
10. **Testing Strategy** - Test framework, types, coverage
11. **Deployment & Operations** - Build process, deployment, monitoring
12. **Security Considerations** - Auth, authorization, data protection
13. **Dependencies & Third-Party Services** - Critical dependencies, external services
14. **Known Issues & Technical Debt** - Open issues, TODOs, tech debt
15. **RFD Summary** - Table of all RFDs with status
16. **References Summary** - Table of all reference documents
17. **Glossary** - Project-specific terms
18. **Quick Reference** - Common commands, important files

---

## Phase 6: Save and Report

**Goal**: Write file and confirm completion

**Actions**:

1. Write the snapshot to `{project_root}/.claude/checkpoints/checkpoint-{N}/snapshot.md`

2. Report completion with:
   - File path
   - Checkpoint number
   - Summary of key findings
   - Notable changes since last checkpoint (if applicable)

---

## Writing Guidelines

1. **Be Specific**: Use actual file paths, function names, and code references
2. **Be Honest**: If something is unclear or poorly documented, note it
3. **Be Complete**: Don't skip sections—mark as "N/A" or "Not found" if truly not applicable
4. **Be Practical**: Focus on information a new developer would actually need
5. **Use Code Examples**: Include short code snippets where they clarify understanding
6. **ASCII Diagrams**: Use text diagrams for architecture when helpful
7. **Reference RFDs**: When discussing features, reference their RFD documents if available
8. **Track Evolution**: Note how things have changed from previous checkpoints
9. **Document References**: List all available reference documents so developers know what resources exist

---

## .claude Folder Structure Reference

```
.claude/
├── checkpoints/                     # Project checkpoints (snapshots over time)
│   ├── checkpoint-0/                # Initial checkpoint (before development)
│   │   ├── prd.md                   # Product Requirements Document
│   │   └── rfd/                     # Request for Development documents
│   │       ├── 1-authentication/
│   │       │   └── rfd-2025-01-24-1430.md
│   │       └── ...
│   │
│   ├── checkpoint-1/                # First development checkpoint
│   │   ├── snapshot.md              # Codebase snapshot at this point
│   │   └── rfd/
│   │       └── ...
│   │
│   └── checkpoint-{N}/              # Additional checkpoints
│       ├── snapshot.md
│       └── rfd/
│
└── references/                      # Reference documents
    ├── team-guidelines/
    ├── package-docs/
    ├── workflows/
    ├── api-specs/
    └── {other-reference-folders}/
```

### Document Types

- **prd.md**: Product Requirements Document - exists in checkpoint-0, describes product vision and requirements
- **snapshot.md**: Technical snapshot of the codebase at a point in time (this is what you're creating)
- **rfd/**: Request for Development documents
  - Each RFD is in a numbered folder: `{N}-{feature-name}/`
  - Inside each folder: `rfd-{YYYY-MM-DD}-{HHMM}.md` with timestamp of creation
  - RFDs describe: user's feature request, implementation progress, current status
- **references/**: Reference documents providing context but not directly part of development
