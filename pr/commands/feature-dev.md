---
description: Guided feature development with codebase understanding, architecture focus, and RFD documentation management
argument-hint: "[optional: feature description]"
---

# Feature Development with RFD Management

Implement features systematically: understand the codebase, manage RFD documentation, clarify requirements, design architecture, then implement.

## Core Principles

- **Use available tools**: Check what MCP servers and skills are available. Use frontend-design for UIs, browser automation for testing, Context7 for package documentation.
- **Ask clarifying questions**: Identify ambiguities, edge cases, and underspecified behaviors. Ask specific questions early—after exploring the codebase, before designing.
- **Understand before acting**: Read existing code patterns first.
- **Read files from agents**: Ask agents to return 5-10 key files. Read those files before proceeding.
- **Simple and elegant**: Write readable, maintainable code.
- **Use TodoWrite**: Track progress throughout.
- **Manage RFDs**: Create or update RFDs to track feature requests and implementation.
- **Write clearly**: Use `writing-clearly-and-concisely` for RFDs. Active voice, omit needless words, avoid AI-isms (pivotal, crucial, leverage).

---

## Phase 0: RFD Discovery & Setup

**Goal**: Understand existing documentation and prepare RFD for this feature

**Actions**:

1. Check if `.claude/checkpoints/` directory exists
2. Find the latest checkpoint number:

```bash
CHECKPOINT_COUNT=$(find .claude/checkpoints -maxdepth 1 -type d -name "checkpoint-*" 2>/dev/null | wc -l)
CURRENT_CHECKPOINT=$((CHECKPOINT_COUNT > 0 ? CHECKPOINT_COUNT - 1 : 0))
```

3. Read existing documentation to understand context:
   - Read `.claude/checkpoints/checkpoint-0/prd.md` if it exists (product requirements)
   - Read the most recent `snapshot.md` if it exists
   - List existing RFDs across all checkpoints:

```bash
find .claude/checkpoints -path "*/rfd/*" -name "rfd-*.md" 2>/dev/null | sort
```

4. Check if an RFD already exists for this feature (search by feature name/keywords)
5. Determine RFD action:
   - If existing RFD found for this feature → will UPDATE it
   - If no existing RFD → will CREATE new one
6. Note the RFD path for later (don't create yet - wait until we have more details)

---

## Phase 1: Discovery

**Goal**: Understand what needs to be built

Initial request: $ARGUMENTS

**Actions**:

1. Create todo list with all phases (including RFD management)
2. If feature unclear, ask user for:
   - What problem are they solving?
   - What should the feature do?
   - Any constraints or requirements?
3. Summarize understanding and confirm with user
4. Record the feature request details for RFD

---

## Phase 2: Codebase Exploration

**Goal**: Understand existing code and patterns

**Actions**:

1. Launch 2-3 code-explorer agents in parallel, each targeting a different aspect:
   - Similar features and their implementation
   - Architecture and abstractions
   - UI patterns, testing, or extension points

   Each agent should return 5-10 key files to read.

2. Read all files identified by agents
3. Summarize findings and patterns

---

## Phase 3: Clarifying Questions

**Goal**: Resolve ambiguities before designing

**CRITICAL**: Do not skip this phase.

**Actions**:

1. Review codebase findings and original request
2. Identify underspecified aspects: edge cases, error handling, integration points, scope boundaries, backward compatibility
3. Present all questions in a clear list
4. Wait for answers before designing

If the user says "use your judgment", provide your recommendation and get confirmation.

---

## Phase 4: Create/Update RFD

**Goal**: Document the feature request and initial planning in an RFD

**Actions**:

1. Determine the RFD location:
   - Find the current/latest checkpoint number
   - If creating new RFD:
     - Count existing RFDs to get next number: `find .claude/checkpoints -path "*/rfd/*" -maxdepth 3 -type d 2>/dev/null | wc -l`
     - Create folder: `.claude/checkpoints/checkpoint-{current}/rfd/{next-rfd-number}-{feature-slug}/`
     - Create file: `rfd-{YYYY-MM-DD}-{HHMM}.md`
   - If updating existing RFD:
     - Use the existing RFD path found in Phase 0

2. Write/Update the RFD with this structure:

```markdown
# RFD-{N}: {Feature Name}

## Metadata

- **Created**: {YYYY-MM-DD HH:MM}
- **Last Updated**: {YYYY-MM-DD HH:MM}
- **Status**: Planning | In Progress | Completed | On Hold
- **Checkpoint**: checkpoint-{N}

## Feature Request

### Original Request

{User's original request verbatim}

### Clarified Requirements

{Summary of requirements after clarifying questions}

- Requirement 1
- Requirement 2
- ...

### Out of Scope

{Explicitly noted exclusions}

## Context

### Related Existing Features

{Features found during codebase exploration that are relevant}

### Key Files & Components

{Important files identified by code-explorer agents}

### Technical Constraints

{Any constraints discovered during exploration}

## Implementation Plan

### Chosen Architecture

{Brief description - will be filled in after Phase 5}

### Implementation Phases

{High-level phases - will be detailed after Phase 5}

## Progress Log

### {Date} - Initial Planning

- Created RFD
- Completed codebase exploration
- Clarified requirements with user

{Additional entries will be added as implementation progresses}

## Notes & Decisions

{Important decisions made and their rationale}
```

3. Confirm RFD creation/update with user

---

## Phase 5: Architecture Design

**Goal**: Design implementation approaches with trade-offs

**Actions**:

1. Launch 2-3 code-architect agents with different focuses: minimal changes, clean architecture, or pragmatic balance
2. Form your recommendation (consider: fix vs feature, urgency, complexity)
3. Present to user: summary of each approach, trade-offs, your recommendation, implementation differences
4. Ask which approach they prefer
5. Update RFD with chosen architecture and implementation phases

---

## Phase 6: Implementation

**Goal**: Build the feature

**Wait for user approval before starting.**

**Actions**:

1. Read all relevant files from previous phases
2. Implement following chosen architecture
3. Follow codebase conventions
4. Update todos as you progress
5. Update RFD progress log with milestones

---

## Phase 7: Quality Review

**Goal**: Verify code quality and correctness

**Actions**:

1. Launch 3 code-reviewer agents: simplicity/DRY, bugs/correctness, conventions/abstractions
2. Consolidate findings and identify high-severity issues
3. Present findings and ask user: fix now, fix later, or proceed?
4. Address issues based on decision
5. Update RFD with significant issues and resolutions

---

## Phase 8: Summary & RFD Finalization

**Goal**: Document completion and finalize RFD

**Actions**:

1. Mark all todos complete
2. Finalize RFD: update status to "Completed", add completion summary, list files changed
3. Summarize to user: what was built, key decisions, files modified, RFD location, next steps

---

## RFD Quick Reference

### RFD Status Values

- **Planning**: Initial request captured, exploring and clarifying
- **In Progress**: Implementation actively underway
- **Completed**: Feature fully implemented and reviewed
- **On Hold**: Paused due to blockers or priority changes

### RFD File Naming

- Folder: `{rfd-number}-{feature-slug}/` (e.g., `4-user-authentication/`)
- File: `rfd-{YYYY-MM-DD}-{HHMM}.md` (e.g., `rfd-2025-01-26-1430.md`)

### When to Update RFD

- After clarifying requirements (Phase 3)
- After choosing architecture (Phase 5)
- During implementation milestones (Phase 6)
- After quality review (Phase 7)
- At completion (Phase 8)
