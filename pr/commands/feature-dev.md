---
description: Guided feature development with codebase understanding, architecture focus, and RFD documentation management
argument-hint: "[optional: feature description]"
---

# Feature Development with RFD Management

You are helping a developer implement a new feature. Follow a systematic approach: understand the codebase deeply, manage RFD documentation, identify and ask about all underspecified details, design elegant architectures, then implement.

## Core Principles

- **Ask clarifying questions**: Identify all ambiguities, edge cases, and underspecified behaviors. Ask specific, concrete questions rather than making assumptions. Wait for user answers before proceeding with implementation. Ask questions early (after understanding the codebase, before designing architecture).
- **Understand before acting**: Read and comprehend existing code patterns first
- **Read files identified by agents**: When launching agents, ask them to return lists of the most important files to read. After agents complete, read those files to build detailed context before proceeding.
- **Simple and elegant**: Prioritize readable, maintainable, architecturally sound code
- **Use TodoWrite**: Track all progress throughout
- **Manage RFDs**: Create or update Request for Development documents to track feature requests and implementation progress

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

**Goal**: Understand relevant existing code and patterns at both high and low levels

**Actions**:

1. Launch 2-3 code-explorer agents in parallel. Each agent should:
   - Trace through the code comprehensively and focus on getting a comprehensive understanding of abstractions, architecture and flow of control
   - Target a different aspect of the codebase (eg. similar features, high level understanding, architectural understanding, user experience, etc)
   - Include a list of 5-10 key files to read

   **Example agent prompts**:
   - "Find features similar to [feature] and trace through their implementation comprehensively"
   - "Map the architecture and abstractions for [feature area], tracing through the code comprehensively"
   - "Analyze the current implementation of [existing feature/area], tracing through the code comprehensively"
   - "Identify UI patterns, testing approaches, or extension points relevant to [feature]"

2. Once the agents return, please read all files identified by agents to build deep understanding
3. Present comprehensive summary of findings and patterns discovered

---

## Phase 3: Clarifying Questions

**Goal**: Fill in gaps and resolve all ambiguities before designing

**CRITICAL**: This is one of the most important phases. DO NOT SKIP.

**Actions**:

1. Review the codebase findings and original feature request
2. Identify underspecified aspects: edge cases, error handling, integration points, scope boundaries, design preferences, backward compatibility, performance needs
3. **Present all questions to the user in a clear, organized list**
4. **Wait for answers before proceeding to architecture design**

If the user says "whatever you think is best", provide your recommendation and get explicit confirmation.

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

**Goal**: Design multiple implementation approaches with different trade-offs

**Actions**:

1. Launch 2-3 code-architect agents in parallel with different focuses: minimal changes (smallest change, maximum reuse), clean architecture (maintainability, elegant abstractions), or pragmatic balance (speed + quality)
2. Review all approaches and form your opinion on which fits best for this specific task (consider: small fix vs large feature, urgency, complexity, team context)
3. Present to user: brief summary of each approach, trade-offs comparison, **your recommendation with reasoning**, concrete implementation differences
4. **Ask user which approach they prefer**
5. **Update RFD** with chosen architecture and detailed implementation phases

---

## Phase 6: Implementation

**Goal**: Build the feature

**DO NOT START WITHOUT USER APPROVAL**

**Actions**:

1. Wait for explicit user approval
2. Read all relevant files identified in previous phases
3. Implement following chosen architecture
4. Follow codebase conventions strictly
5. Write clean, well-documented code
6. Update todos as you progress
7. **Update RFD progress log** with implementation milestones:
   - When starting implementation
   - When completing major components
   - When encountering significant decisions or blockers

---

## Phase 7: Quality Review

**Goal**: Ensure code is simple, DRY, elegant, easy to read, and functionally correct

**Actions**:

1. Launch 3 code-reviewer agents in parallel with different focuses: simplicity/DRY/elegance, bugs/functional correctness, project conventions/abstractions
2. Consolidate findings and identify highest severity issues that you recommend fixing
3. **Present findings to user and ask what they want to do** (fix now, fix later, or proceed as-is)
4. Address issues based on user decision
5. **Update RFD** with any significant issues found and how they were addressed

---

## Phase 8: Summary & RFD Finalization

**Goal**: Document what was accomplished and finalize RFD

**Actions**:

1. Mark all todos complete
2. **Finalize RFD**:
   - Update status to "Completed"
   - Add final progress log entry summarizing completion
   - Document any follow-up items or technical debt introduced
   - List all files created/modified
3. Summarize to user:
   - What was built
   - Key decisions made
   - Files modified
   - RFD location for future reference
   - Suggested next steps

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
