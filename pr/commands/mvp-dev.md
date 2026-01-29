---
description: Develop an entire MVP from a PRD with systematic feature-by-feature implementation and RFD tracking
argument-hint: "[optional: specific focus or priority features]"
---

# MVP Development with PRD and RFD Management

You are helping a developer implement a complete MVP (Minimum Viable Product) from a Product Requirements Document. Follow a systematic approach: understand the PRD deeply, break it into features, explore the codebase (if existing), design architecture, and implement feature by feature with RFD tracking.

## Core Principles

- **Leverage available MCP tools and skills**: Always check what MCP tools and skills are available in your current session. Use them proactively throughout development:
  - **context7** (MCP tool): Query up-to-date documentation for any package or library you're unfamiliar with
  - **vercel-labs/agent-browser** (skill): Use webapp-testing to verify UI behavior, take screenshots, and debug frontend issues
  - **Other MCP tools and skills**: Look for database tools, API clients, document generators, or other integrations that could assist development
  - When in doubt about a library's API or best practices, use context7 to look it up rather than guessing
- **PRD is the source of truth**: All features and requirements come from the PRD
- **One RFD per feature**: Each MVP feature gets its own RFD in checkpoint-0
- **Ask clarifying questions**: Identify ambiguities and get user input before implementing
- **Understand before acting**: Read and comprehend existing code patterns first (if any)
- **Read files identified by agents**: When launching agents, ask them to return lists of the most important files to read
- **Simple and elegant**: Prioritize readable, maintainable, architecturally sound code
- **Use TodoWrite**: Track all progress throughout
- **Sequential feature development**: Complete one feature before moving to the next

---

## Phase 0: PRD Discovery & Context

**Goal**: Load and understand the Product Requirements Document

**Actions**:

1. Check if `.claude/checkpoints/checkpoint-0/prd.md` exists:
```bash
ls .claude/checkpoints/checkpoint-0/prd.md 2>/dev/null
```

2. **If PRD does not exist**:
   - Inform the user: "No PRD found at .claude/checkpoints/checkpoint-0/prd.md"
   - Suggest: "Would you like me to help create a PRD using /pr:create-prd first?"
   - **STOP** - Cannot proceed without PRD

3. **If PRD exists**, read it thoroughly:
   - Read `.claude/checkpoints/checkpoint-0/prd.md`
   - Extract: project vision, target users, MVP features, tech stack, design guidelines
   - Note: success metrics, constraints, out-of-scope items

4. Check for existing RFDs in checkpoint-0:
```bash
find .claude/checkpoints/checkpoint-0/rfd -name "rfd-*.md" 2>/dev/null | sort
```

5. Read any existing RFDs to understand what's already been planned/implemented

6. Check for existing codebase:
   - If there's already code, note this as a "PRD for existing project"
   - If no code exists yet, this is a greenfield MVP

---

## Phase 1: Feature Extraction

**Goal**: Break down the PRD into implementable features with clear priorities

**Actions**:

1. From the PRD, extract all MVP features (typically marked P0/P1 or "Must Have")

2. Create a prioritized feature list:

| # | Feature Name | Priority | Dependencies | Complexity |
|---|--------------|----------|--------------|------------|
| 1 | [Feature 1]  | P0       | None         | Low/Med/High |
| 2 | [Feature 2]  | P0       | Feature 1    | Low/Med/High |
| ... | ... | ... | ... | ... |

3. Identify the optimal implementation order based on:
   - Dependencies (what features require other features)
   - Technical complexity (simpler foundation first)
   - User value (core functionality first)

4. Present the feature breakdown to the user:
   - List all MVP features with estimated complexity
   - Proposed implementation order
   - **Ask user to confirm or adjust the order**

5. Create master todo list with all features

---

## Phase 2: Architecture Planning

**Goal**: Design the overall MVP architecture before implementing any features

**Actions**:

1. If existing codebase:
   - Launch 2 code-explorer agents to understand existing patterns
   - Read key files identified by agents
   - Note existing conventions to follow

2. Launch 2 code-architect agents in parallel:

   **Agent 1 - Foundation Architecture**:
   ```
   Based on the PRD requirements for [project], design the foundational architecture:
   - Project structure and organization
   - Technology stack setup (from PRD)
   - Shared components and utilities
   - Database schema for all MVP features
   - API structure and patterns

   Make decisive architectural choices. Return file structure and setup steps.
   ```

   **Agent 2 - Feature Architecture Map**:
   ```
   Based on the PRD requirements, create an architecture map for all MVP features:
   - How each feature fits into the overall architecture
   - Shared code between features
   - Integration points between features
   - Build sequence for optimal development

   Return a feature-by-feature implementation blueprint.
   ```

3. Review architecture proposals and form recommendation

4. Present to user:
   - Overall architecture design
   - How features will be structured
   - Build sequence recommendation
   - **Ask user to approve architecture before proceeding**

5. **Create Architecture RFD** (RFD-0):
   - Create `.claude/checkpoints/checkpoint-0/rfd/0-architecture/rfd-{YYYY-MM-DD}-{HHMM}.md`
   - Document the chosen architecture, tech stack, and overall structure
   - This RFD tracks the foundational architecture decisions

---

## Phase 3: Foundation Setup

**Goal**: Set up project foundation before implementing features

**Actions**:

1. If greenfield project, create initial project structure:
   - Initialize project (npm init, poetry init, etc.)
   - Set up tech stack from PRD
   - Create directory structure
   - Set up linting, formatting, testing infrastructure
   - Create initial configuration files
   - Set up database schema (if applicable)

2. If existing project, verify foundation supports MVP:
   - Check if tech stack matches PRD
   - Identify any gaps in infrastructure
   - Set up any missing components

3. Update Architecture RFD with foundation implementation status

4. **Commit foundation** (suggest user run /pr:commit-push)

---

## Phase 4: Feature Development Loop

**Goal**: Implement each feature systematically with its own RFD

**For each feature in priority order, execute this loop:**

### 4.1: Feature Discovery

**Actions**:

1. Re-read relevant PRD section for this feature
2. Identify specific requirements and acceptance criteria
3. Create feature RFD:
   - Path: `.claude/checkpoints/checkpoint-0/rfd/{N}-{feature-slug}/rfd-{YYYY-MM-DD}-{HHMM}.md`
   - Include: feature request from PRD, requirements, acceptance criteria
   - Status: Planning

### 4.2: Feature Exploration (if existing code)

**Actions**:

1. Launch 1-2 code-explorer agents:
   ```
   Analyze the codebase for implementing [feature]. Focus on:
   - Existing patterns to follow
   - Components to reuse
   - Integration points
   - Similar features for reference

   Return 5-10 key files to read.
   ```

2. Read files identified by agents
3. Update RFD with context about existing code

### 4.3: Feature Clarification

**Actions**:

1. Review PRD requirements for this feature
2. Identify any ambiguities or gaps:
   - Edge cases not covered
   - Error handling not specified
   - Design preferences unclear
   - Integration details missing

3. **Present clarifying questions to user**
4. **Wait for answers before proceeding**

5. Update RFD with clarified requirements

### 4.4: Feature Architecture

**Actions**:

1. Launch 1-2 code-architect agents:
   ```
   Design the implementation for [feature] that fits within the MVP architecture.
   Requirements: [from PRD]
   Constraints: [from clarification]

   Provide:
   - Files to create/modify
   - Component design
   - Implementation steps as checklist
   ```

2. Review and select approach

3. Present to user:
   - Implementation approach
   - Files that will be created/modified
   - **Ask for approval to proceed**

4. Update RFD with chosen architecture and implementation plan
5. Update RFD status: In Progress

### 4.5: Feature Implementation

**Actions**:

1. Implement following the chosen architecture
2. Follow codebase conventions strictly
3. Write clean, well-documented code
4. Update todos as you progress
5. Update RFD progress log with milestones

### 4.6: Feature Review

**Actions**:

1. Launch 2 code-reviewer agents:
   ```
   Review the implementation of [feature] for:
   - Bugs and logic errors
   - Code quality and conventions
   - Security issues
   - Acceptance criteria compliance

   Only report issues with confidence >= 80.
   ```

2. Present findings to user
3. Fix any critical issues

4. Update RFD with review findings and fixes

### 4.7: Feature Completion

**Actions**:

1. Verify all acceptance criteria are met
2. Update RFD:
   - Status: Completed
   - Add completion log entry
   - List all files created/modified

3. **Suggest commit** for this feature

4. Move to next feature in priority order

---

## Phase 5: MVP Integration

**Goal**: Ensure all features work together as a cohesive MVP

**Actions**:

1. Launch integration review agents:
   ```
   Review the complete MVP implementation for:
   - Integration between features
   - Consistent patterns across codebase
   - Missing error handling
   - Performance concerns
   - Security vulnerabilities

   Focus on how features interact with each other.
   ```

2. Address any integration issues found

3. Run full test suite (if tests exist)

4. Verify MVP meets PRD success criteria

---

## Phase 6: MVP Summary & Documentation

**Goal**: Document the completed MVP and finalize all RFDs

**Actions**:

1. Mark all todos complete

2. Update all RFDs to Completed status

3. Create MVP completion summary:

```markdown
# MVP Development Complete

## Features Implemented
| # | Feature | RFD | Status |
|---|---------|-----|--------|
| 0 | Architecture | rfd/0-architecture/... | Completed |
| 1 | [Feature 1] | rfd/1-{slug}/... | Completed |
| 2 | [Feature 2] | rfd/2-{slug}/... | Completed |
| ... | ... | ... | ... |

## Files Created
[List of all files created]

## Files Modified
[List of all files modified]

## Key Decisions
[Important decisions made during development]

## Next Steps
[Suggested post-MVP enhancements from PRD]

## RFD Locations
All RFDs for this MVP are in:
`.claude/checkpoints/checkpoint-0/rfd/`
```

4. Suggest creating a snapshot: "/pr:create-snapshot to capture this state"

5. Suggest commit for final MVP state

---

## RFD Structure for MVP Features

Each feature RFD should follow this structure:

```markdown
# RFD-{N}: {Feature Name}

## Metadata

- **Created**: {YYYY-MM-DD HH:MM}
- **Last Updated**: {YYYY-MM-DD HH:MM}
- **Status**: Planning | In Progress | Completed | On Hold
- **MVP Feature**: Yes
- **PRD Reference**: Section [X.X]

## Feature Request

### From PRD
{Exact requirements from PRD}

### Acceptance Criteria
- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] ...

### Clarified Requirements
{Additional requirements after clarification with user}

### Out of Scope
{What this feature explicitly does NOT include}

## Context

### Related Features
{Other MVP features this connects to}

### Key Files & Components
{Files identified by code-explorer agents}

### Technical Constraints
{Any constraints from PRD or architecture}

## Implementation Plan

### Chosen Architecture
{Architecture decision from code-architect agents}

### Implementation Phases
1. [ ] {Phase 1}
2. [ ] {Phase 2}
3. [ ] ...

## Progress Log

### {Date} - Initial Planning
- Created RFD from PRD requirements
- Clarified requirements with user

### {Date} - Implementation Started
- {Progress notes}

### {Date} - Implementation Complete
- All acceptance criteria met
- Code reviewed and issues fixed

## Notes & Decisions

{Important decisions made and their rationale}

## Files

### Created
- `path/to/file1`
- `path/to/file2`

### Modified
- `path/to/existing/file`
```

---

## Important Notes

### RFD Organization
- All MVP RFDs go in `checkpoint-0/rfd/` because MVP development happens before the first snapshot
- RFD-0 is always the Architecture RFD
- Feature RFDs are numbered 1, 2, 3... in implementation order
- After MVP is complete, future features will go in subsequent checkpoints

### Handling PRD Changes
If user wants to change requirements mid-development:
1. Note the change in the relevant RFD
2. Update affected RFDs
3. Reassess implementation order if needed
4. Continue with updated requirements

### When to Ask User
- Before starting each feature
- When requirements are ambiguous
- When making significant architectural decisions
- When choosing between implementation approaches
- Before committing major changes

### Progress Tracking
- Update RFD status as you progress
- Log milestones in RFD progress log
- Keep todos current
- Provide regular status updates to user

---

## RFD Quick Reference

### Status Values
- **Planning**: Extracting requirements, clarifying with user
- **In Progress**: Implementation actively underway
- **Completed**: Feature fully implemented and reviewed
- **On Hold**: Blocked or deprioritized

### File Naming
- Folder: `{N}-{feature-slug}/` (e.g., `1-user-authentication/`)
- File: `rfd-{YYYY-MM-DD}-{HHMM}.md` (e.g., `rfd-2025-01-26-1430.md`)

### When to Update RFD
- After clarifying requirements
- After choosing architecture
- During implementation milestones
- After code review
- At feature completion
