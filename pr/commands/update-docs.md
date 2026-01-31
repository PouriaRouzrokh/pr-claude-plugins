---
description: Update project documentation using code exploration to understand changes since last update
argument-hint: "[path] [description of what to document]"
---

# Update Documentation

Update project documentation to reflect current codebase state, using code-explorer agents to understand changes.

## Core Principles

- **Write clearly**: Use `writing-clearly-and-concisely`. Active voice, omit needless words, avoid AI-isms.
- **Explore before updating**: Use code-explorer agents to understand changes.
- **Accuracy over completeness**: Only document what exists in code.
- **Respect existing structure**: Don't reorganize without asking.
- **Checkpoint awareness**: Maintain `.claude/checkpoints/` structure.

---

## Phase 0: Parse Arguments

**Goal**: Understand the scope of documentation update

**Target scope**: $ARGUMENTS

The arguments may contain:
1. **A path** (file or folder) - scope the documentation update to that area
2. **Free text describing what to document** - specific features or aspects to focus on
3. **Both** - a path followed by description of what to document
4. **Nothing** - update all documentation based on recent changes and current codebase state

**Examples**:
- `/pr:update-docs` → Update all docs based on recent changes
- `/pr:update-docs src/auth` → Update docs related to the auth folder
- `/pr:update-docs authentication and user sessions` → Focus on these features
- `/pr:update-docs src/api add the new endpoints we created` → Scope + focus

If arguments are ambiguous, ask the user to clarify.

---

## Phase 1: Documentation Discovery

**Goal**: Identify all documentation sources in the project

**Actions**:

1. **Note about CLAUDE.md**:
   - CLAUDE.md updates are handled by the `/pr:update-claude-md` skill
   - This command focuses on project documentation (README, API docs, checkpoints, references)

2. **Check standard locations**:
   - `README.md` at project root
   - `docs/` folder
   - `CHANGELOG.md`, `CONTRIBUTING.md`, `API.md`

3. **Check Claude-specific documentation structure**:

```
.claude/
├── checkpoints/                     # Project checkpoints (snapshots over time)
│   ├── checkpoint-0/                # Initial checkpoint (before development)
│   │   ├── prd.md                   # Product Requirements Document (no code yet)
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
└── references/                      # Reference documents (not directly part of development)
    ├── team-guidelines/
    ├── package-docs/
    ├── workflows/
    ├── api-specs/
    └── {other-reference-folders}/
```

4. **Document types**:
   - **prd.md**: Product Requirements Document (checkpoint-0 only)
   - **snapshot.md**: Technical snapshot of codebase at a point in time
   - **rfd/**: Request for Development documents tracking feature requests
   - **references/**: Reference documents providing context but not part of development

5. **Check other documentation**:
   - API documentation (Swagger, OpenAPI specs)
   - Wiki or knowledge base files
   - Architecture decision records (ADRs)
   - Any `.md` files in the project

6. **Note**: Track whether this is a global update (no path scope) or scoped update

---

## Phase 2: Codebase Exploration

**Goal**: Understand what has changed and needs documentation

**Actions**:

1. Launch 2 code-explorer agents in parallel:

   **Agent 1 - Recent Changes Analysis**:
   ```
   Analyze recent changes in the codebase. Look at:
   - Git history (recent commits, changed files)
   - New features or modules added
   - Modified functionality
   - Removed features

   Compare with existing documentation to identify gaps.
   Return a list of 5-10 key files that documentation should cover.
   ```

   **Agent 2 - Documentation Gap Analysis**:
   ```
   Compare the current codebase against existing documentation. Identify:
   - Features that exist in code but not in docs
   - Documentation that references removed/changed code
   - Outdated examples or API references
   - Missing setup or configuration documentation

   Return a list of specific documentation updates needed.
   ```

2. Wait for both agents to complete

3. Read all key files identified by agents to understand the current state

4. Consolidate findings into a documentation update plan

---

## Phase 3: Present Update Plan

**Goal**: Get user approval for documentation changes

**Actions**:

1. Present a summary of planned documentation updates:
   - Which files will be updated
   - What sections will change
   - What new content will be added
   - What outdated content will be removed

2. Ask user for approval before proceeding

---

## Phase 4: Update README.md

**Goal**: Keep main README accurate

**Actions**:

- Ensure project description is accurate
- Update installation/setup instructions if changed
- Update usage examples if APIs changed
- Verify all documented features still exist
- Add any new significant features

---

## Phase 5: Update API Documentation

**Goal**: Keep API docs in sync with code

**Actions**:

- Ensure all endpoints/functions are documented
- Verify parameters and return types are correct
- Update examples to reflect current behavior
- Remove documentation for removed APIs

---

## Phase 6: Update Checkpoint Documents

**Goal**: Maintain .claude/checkpoints/ documentation

**Actions**:

**snapshot.md**:
- Update to reflect current codebase state
- Note changes since last checkpoint

**rfd/**:
- Ensure RFD status reflects actual implementation state (Planning/In Progress/Completed)
- Update progress logs for active features
- Mark completed features appropriately

**prd.md**:
- **Generally should NOT be modified** unless requirements have officially changed
- Ask user before making any changes to PRD

---

## Phase 7: Update Reference Documents

**Goal**: Keep `.claude/references/` current (with caution)

References provide context but aren't tied to code changes. Update only when:
- User explicitly requests it
- A described process has clearly changed
- Package docs are outdated

**Ask user before updating references**—they often reflect team decisions.

---

## Phase 8: Consistency Check

**Goal**: Ensure documentation quality

**Actions**:

Verify documentation is:
- **Accurate**: Reflects what the code actually does
- **Complete**: All significant features are documented
- **Consistent**: Terminology and style are uniform
- **Current**: No references to removed/changed features

---

## Phase 9: Summary

**Goal**: Report what was updated

**Actions**:

Summarize to user:
- Files that were updated
- Major changes made
- Any items that need user attention
- Suggestions for additional documentation that could be added

---

## Safety Guidelines

**DO NOT:**
- Make any git commits or push changes
- Create new documentation files unless explicitly requested
- Delete documentation files
- Change the documentation structure/organization without asking
- Modify prd.md unless the user explicitly confirms requirements changed
- Modify reference documents (.claude/references/) without user confirmation
- Update documentation for code outside the specified scope (if scope was provided)
- Fabricate features - only document what actually exists in the code

**NOTE**: This command focuses on standalone documentation files (markdown, etc.). For CLAUDE.md updates, use `/pr:update-claude-md`. Inline documentation within code files (JSDoc, TSDoc, docstrings) is handled by the `/pr:clean-codebase` command as part of code maintenance.
