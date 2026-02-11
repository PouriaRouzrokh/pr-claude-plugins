---
description: Develop an entire MVP from a PRD with systematic feature-by-feature implementation and RFD tracking
argument-hint: "[optional: specific focus or priority features] [--subagents | --team]"
---

# MVP Development with PRD and RFD Management

Implement an MVP from a PRD systematically: understand the PRD, break it into features, design architecture, and implement feature by feature with RFD tracking.

## ATLAS Development Philosophy

This command implements the full **ATLAS** framework for building production-ready MVPs.

**When to use this command:**
- Building a new MVP from a PRD
- Implementing multiple related features systematically
- Projects requiring architecture planning and integration validation

**When NOT to use this command:**
- Single feature additions → use `/pr:feature-dev` instead
- Bug fixes or small changes → just fix directly
- Quick prototypes where validation isn't critical

### ATLAS Phase Mapping

| Phase | How This Command Applies It |
|-------|----------------------------|
| **A** (Architect) | PRD contains problem, users, success metrics |
| **T** (Trace) | Phase 2-3 extracts features, designs architecture, maps integrations |
| **L** (Link) | Phase 3 validates connections before building |
| **A** (Assemble) | Phase 4 implements features with layered architecture |
| **S** (Stress-test) | Phase 4.6-4.7 proactively tests and professionalizes code before proceeding |

**Key principle:** Never build before designing. Never skip connection validation. Never ship without testing.

For complete ATLAS framework, see `atlas-development` skill.

## Multi-Agent Strategy

MVP development involves many agent-assisted phases: exploration, architecture, implementation support, and review. Decide which agent strategy to use based on MVP complexity and user flags.

### Choosing Between Subagents and Agent Teams

**Use subagents (default)** — lightweight workers that report results back:
- Per-feature exploration and architecture (most MVP features are developed sequentially)
- Code review agents checking different quality dimensions
- Standard feature-by-feature development where features are relatively independent

**Use agent teams** — independent sessions with inter-agent messaging:
- Architecture planning (Phase 2) for MVPs with tightly coupled features where architects need to coordinate shared components, database schema, and API contracts
- Integration review (Phase 5) where reviewers should cross-check how features interact, challenge each other's findings, and coordinate on cross-cutting issues
- Full-stack features where frontend, backend, and data agents need to coordinate file ownership and avoid conflicts

### User Override

Parse `$ARGUMENTS` for these flags:
- `--subagents` — Force subagent mode for all agent phases
- `--team` — Force agent team mode for inter-agent collaboration

If `--team` is passed but the MVP is simple (few features, no complex integrations), explain the overhead and ask if the user wants to proceed. If `--subagents` is passed, respect their choice.

**Without flags**: Default to subagents for individual feature phases. Consider proposing agent teams for architecture planning (Phase 2) and integration review (Phase 5) if the MVP has many interconnected features — explain the benefit before proceeding. Agent teams are experimental, more expensive, and add coordination overhead.

---

## Core Principles

- **Use available tools**: Check MCP servers and skills. Use frontend-design for UIs, Playwright for browser testing (if available), Context7 for documentation.
- **PRD is source of truth**: All features come from the PRD.
- **Sequential development**: ONE feature at a time. Test, review, and approve before moving on. User can pause and resume.
- **RFD-first**: Create the RFD before starting any feature. It tracks the entire lifecycle.
- **Test thoroughly**: Both you and user must test each feature before proceeding.
- **Ask clarifying questions**: Resolve ambiguities before implementing.
- **Understand before acting**: Read existing code patterns first.
- **Read files from agents**: Ask agents to return 5-10 key files.
- **Simple and elegant**: Write readable, maintainable code.
- **Write clearly**: Use `writing-clearly-and-concisely` for RFDs. Active voice, omit needless words, avoid AI-isms.
- **Use TodoWrite**: Track progress throughout.
- **Validate before building**: Test all integrations and connections before writing feature code.
- **Test proactively**: After implementing each feature, test your own work — run endpoints, execute functions, verify behavior. Clean up all test artifacts afterward.
- **Professionalize code**: Before handoff, review all code for professional quality — no redundancies, proper commenting, clean structure, no debug leftovers.

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

**Goal**: Design MVP architecture before implementing features

**Actions**:

1. If existing codebase, launch 2 code-explorer agents (subagents) to understand patterns

2. Launch 2 code-architect agents (subagents by default, or agent team if `--team`):
   - **Foundation Architecture**: Project structure, tech stack, shared components, database schema, API patterns
   - **Feature Architecture Map**: How features fit together, shared code, integration points, build sequence

   *This phase benefits most from agent teams — architects can negotiate shared components, debate schema decisions, and ensure foundation and feature architectures are consistent. With subagents, you synthesize their proposals yourself.*

3. Form recommendation and present to user. Ask for approval.

4. Create Architecture RFD (RFD-0) at `.claude/checkpoints/checkpoint-0/rfd/0-architecture/`

---

## Phase 3: Foundation Setup & Link Validation

**Goal**: Set up project foundation AND validate all connections before implementing features

This phase implements ATLAS **Link** step: validate everything works before building.

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

3. **Link Validation** (CRITICAL — do not skip):
   - [ ] Database connection tested (query returns data or empty, not error)
   - [ ] All API keys verified (make test requests)
   - [ ] MCP servers responding (list tools, test one operation)
   - [ ] OAuth flows working (if applicable)
   - [ ] Environment variables set correctly
   - [ ] Rate limits documented

   Present validation results to user. If anything fails, fix before proceeding.

4. Update Architecture RFD with foundation implementation status and validation results

5. **Commit foundation** (suggest user run /pr:commit-push)

---

## Phase 4: Feature Development Loop

**Goal**: Implement each feature with its own RFD, testing and approval before moving on

Sequential process: complete, test, and approve each feature before starting the next. User can pause and resume later.

---

### For each feature, execute Steps 4.1 through 4.9:

---

### 4.1: Create Feature RFD (Before Any Work)

Create the RFD first—it tracks the entire feature lifecycle.

**Actions**:

1. Announce: "Starting Feature {N}: {Feature Name}"
2. Re-read relevant PRD section
3. Create RFD at `.claude/checkpoints/checkpoint-0/rfd/{N}-{feature-slug}/rfd-{YYYY-MM-DD}-{HHMM}.md`
   - Include: feature request, acceptance criteria (checkboxes), status: Planning
4. Confirm RFD creation with user

---

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
3. **Update RFD** → Add "Context" section with exploration findings

---

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

5. **Update RFD** → Add clarified requirements and out-of-scope items

---

### 4.4: Feature Architecture & Planning

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

3. **Update RFD** → Add complete implementation plan:
   - Chosen architecture
   - Files to create/modify
   - Step-by-step implementation phases (as checkboxes)

4. Present to user:
   - Implementation approach summary
   - Files that will be created/modified
   - **Ask for approval to proceed with implementation**

5. **Update RFD status: In Progress**

---

### 4.5: Feature Implementation

**Actions**:

1. Implement following the chosen architecture
2. Follow codebase conventions strictly
3. Write clean, well-documented code
4. Update todos as you progress
5. **Update RFD progress log** with milestones as you complete implementation phases
6. Check off implementation phases in RFD as they're completed

---

### 4.6: Proactive Testing & Verification

**CRITICAL**: Test your own work before asking the user to test. Do not hand off untested code.

**Actions**:

1. **Self-testing** (do this yourself, proactively):
   - **Backend**: Call API endpoints, invoke functions, run database queries — verify correct responses and data flow
   - **Frontend**: Use Playwright for UI testing, screenshots, behavior verification (if available)
   - **Logic**: Write and run quick validation scripts to confirm business logic works as expected
   - **Integration**: Test that new code works correctly with existing features
   - Run existing test suites and verify all pass

2. **Clean up test artifacts**: After testing passes, remove all temporary test scripts, debug print statements, console.logs, temporary routes, hardcoded test data, and any code added solely for testing purposes. The codebase must contain zero testing residue.

3. Launch 2 code-reviewer agents for bugs, quality, security (confidence >= 80)

4. Fix issues found

5. Check off acceptance criteria in RFD
6. Update RFD with testing results (what was tested, what passed, what was fixed)

---

### 4.7: Code Professionalization

**CRITICAL**: Before any user-facing handoff, review and professionalize all code written in this feature. The code must read as if written by a senior engineer.

**Actions**:

1. **Read every file you created or modified** in this feature — line by line
2. **Check for and fix**:
   - Redundant or duplicated code blocks — consolidate into shared functions where appropriate
   - Dead code, unused imports, unused variables — remove completely
   - Debug artifacts — remove all console.log, print statements, TODO/FIXME/HACK comments left from development
   - Inconsistent naming — ensure variables, functions, and files follow the project's conventions
   - Missing or excessive comments — add comments only where logic is non-obvious; remove obvious or redundant comments
   - Overly complex logic — simplify where possible without changing behavior
   - Inconsistent formatting — ensure consistent indentation, spacing, and style throughout
   - Hardcoded values that should be constants or configuration
   - Error messages that are vague or unhelpful
3. **Verify the code reads cleanly**: A developer opening this file for the first time should find it well-organized, well-named, and easy to follow
4. Update RFD with professionalization notes (what was cleaned up)

---

### 4.8: User Presentation & Feedback

**Actions**:

1. Present to user: summary of what was built, how to test, screenshots if available
2. Wait for user testing and feedback
3. Address any issues or changes requested by user
4. Re-test and re-professionalize after making changes
5. **Update RFD** → Document feedback received and changes made
6. Repeat until user confirms they're satisfied with the feature

---

### 4.9: Feature Completion & Checkpoint

**This is a formal checkpoint before moving to the next feature.**

**Actions**:

1. **Finalize RFD**:
   - Update status: **Completed**
   - Verify all acceptance criteria are checked off
   - Add final progress log entry with completion summary
   - List all files created/modified
   - Document any technical debt or future improvements noted

2. **Present completion summary to user**:
   ```
   ## Feature {N} Complete: {Feature Name}

   ### What was built
   [Summary]

   ### Files created/modified
   [List]

   ### RFD location
   [Path to RFD]

   ### Ready to commit and continue?
   ```

3. **Ask user for permission to commit**:
   - "Ready to commit this feature? (You can run /pr:commit-push)"
   - Wait for user to confirm commit

4. **After commit, ask about next steps**:
   - If more features remain: "Ready to start Feature {N+1}: {Next Feature Name}? Or would you like to pause and continue later?"
   - If this was the last feature: Proceed to Phase 5 (MVP Integration)

5. **If user wants to pause**:
   - Summarize current MVP progress
   - Note which feature is next
   - Inform user: "You can resume MVP development anytime by running /pr:mvp-dev again. I'll detect the existing RFDs and continue from Feature {N+1}."

---

### Resuming MVP Development

When user runs /pr:mvp-dev on a project with existing RFDs:

1. Read all existing RFDs in checkpoint-0
2. Identify completed features (Status: Completed)
3. Identify the next feature to implement
4. Present status: "Found existing MVP progress. Features 1-{N} are complete. Ready to continue with Feature {N+1}: {Feature Name}?"
5. Resume from Step 4.1 for the next feature

---

## Phase 5: MVP Integration

**Goal**: Ensure all features work together as a cohesive MVP

**Actions**:

1. Launch integration review agents (subagents by default, or agent team if `--team`):
   ```
   Review the complete MVP implementation for:
   - Integration between features
   - Consistent patterns across codebase
   - Missing error handling
   - Performance concerns
   - Security vulnerabilities

   Focus on how features interact with each other.
   ```

   *Agent teams add value here — reviewers covering security, performance, and integration can challenge each other's findings and flag cross-cutting issues (e.g., a performance reviewer noticing that a security fix introduces latency). With subagents, you consolidate findings yourself.*

2. Address any integration issues found

3. **Final code professionalization**: Review the entire codebase for consistency across all features — naming conventions, code style, comment quality, and shared abstractions. Fix any cross-feature redundancies or inconsistencies that emerged during sequential development.

4. Run full test suite (if tests exist)

5. Verify MVP meets PRD success criteria

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

## Testing

### Proactive Self-Testing
- [ ] Backend endpoints/functions tested directly
- [ ] Frontend tested with Playwright/screenshots (if applicable)
- [ ] Integration with existing features verified
- [ ] Existing test suites pass
- [ ] All test artifacts cleaned up (no debug code, temporary scripts, or test data remains)
- {Test results and notes}

### Code Review & Professionalization
- [ ] Code review agents run
- [ ] All code read line-by-line for professional quality
- [ ] No redundant code, dead code, or unused imports
- [ ] Comments are appropriate (present where needed, absent where obvious)
- [ ] Naming conventions consistent with project
- [ ] Code reads cleanly — well-organized and easy to follow
- {Issues found and fixed}

### User Testing
- [ ] User tested the feature
- [ ] User approved the feature
- {User feedback and changes made}

## Progress Log

### {Date} - Initial Planning
- Created RFD from PRD requirements
- Clarified requirements with user

### {Date} - Architecture Approved
- User approved implementation plan

### {Date} - Implementation Started
- {Progress notes}

### {Date} - Testing Complete
- All tests passed
- User verified and approved

### {Date} - Feature Complete
- All acceptance criteria met
- Committed with message: {commit message}

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

### Sequential Feature Development
- One feature at a time—complete, test, approve before starting the next
- Each feature ends with a checkpoint: user reviews, approves, commits
- User can pause and resume—RFDs preserve progress
- Always create the RFD before any feature work

### RFD as Central Document
The RFD tracks the entire lifecycle: planning → implementation → testing → completion. Log requirements, progress, test results, and final status.

### RFD Organization
- MVP RFDs go in `checkpoint-0/rfd/` (before first snapshot)
- RFD-0 = Architecture RFD; features numbered 1, 2, 3...
- Post-MVP features go in subsequent checkpoints

### When to Wait for User
- Before starting each feature
- After clarification questions (before designing)
- After architecture design (before implementing)
- After implementation (for user testing)
- Before committing and before next feature

### Testing Requirements
Feature completion requires:
1. Proactive self-testing (run endpoints, execute functions, verify behavior)
2. Cleanup of all test artifacts (temporary scripts, debug statements, test data)
3. Code review agents
4. Code professionalization (no redundancies, proper commenting, clean structure)
5. User testing and confirmation
6. All acceptance criteria checked in RFD

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
