---
description: Update CLAUDE.md files with current project state and development principles
argument-hint: "[optional: path/to/project]"
---

# Update CLAUDE.md

Update all CLAUDE.md files in the project with the current project state while maintaining conciseness and emphasizing development principles that help Claude assist effectively.

## Core Philosophy

**Writing Quality**: When writing or updating CLAUDE.md content, use the `writing-clearly-and-concisely` skill. Apply Strunk's principles: use active voice, omit needless words, be specific and concrete. Avoid AI-isms (pivotal, crucial, leverage, robust, seamless). Write clear, direct prose.

CLAUDE.md files should be **concise but complete** - they provide quick reference for Claude without bloating the context window. They should contain:

1. **Project overview** - What the project is and does
2. **Key commands** - How to build, test, run, and deploy
3. **Code conventions** - Patterns and standards to follow
4. **Development principles** - Critical workflows and practices
5. **Documentation hierarchy** - Where to find detailed information

CLAUDE.md is NOT a comprehensive documentation file. It's a quick reference that points Claude to more detailed docs when needed.

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

2. Common locations to check:

   - Project root: `CLAUDE.md`
   - Subdirectories: `*/CLAUDE.md`
   - Nested packages: `packages/*/CLAUDE.md`
   - Workspace roots in monorepos

3. For each CLAUDE.md found, note:
   - Its location
   - What scope it covers (whole project, specific package, etc.)

**IMPORTANT**: All CLAUDE.md files must include the core development principles (see Phase 4).

---

## Phase 2: Read Existing CLAUDE.md Files

**Goal**: Understand current state of each file

**Actions**:

1. Read each CLAUDE.md file found in Phase 1
2. Note existing sections and structure
3. Identify what needs updating vs. what's still accurate
4. Preserve project-specific customizations

---

## Phase 3: Read Project Context from Checkpoints

**Goal**: Gather information needed to update CLAUDE.md from existing documentation

**Actions**:

1. Find the latest checkpoint:

```bash
ls -d .claude/checkpoints/checkpoint-* 2>/dev/null | sort -V | tail -1
```

2. Read key documents (in order of priority):

   - **Latest snapshot.md**: Contains comprehensive project state, tech stack, architecture, commands
   - **PRD** (`.claude/checkpoints/checkpoint-0/prd.md`): Project vision and goals
   - **Recent RFDs**: Current feature status and implementation details

3. Extract from these documents:

   - Project overview and purpose
   - Technology stack
   - Key commands (build, test, run, deploy)
   - Code conventions and patterns
   - Current development status

4. If no checkpoints exist, check:
   - `README.md` for project overview
   - `package.json` or `Makefile` for commands
   - Existing CLAUDE.md content to preserve

**NOTE**: Do NOT run code-explorer agents. The checkpoint system already contains the necessary context.

---

## Phase 4: Update CLAUDE.md Files

**Goal**: Update each CLAUDE.md with current state and essential principles

**For each CLAUDE.md file**, ensure it contains these sections:

### Required Sections

1. **Project Overview** (brief - 2-3 sentences max)
2. **Key Commands** (only the most essential)
3. **Development Principles** (ALWAYS include - see template below)
4. **Documentation Hierarchy** (where to find detailed docs)

### Development Principles Section (REQUIRED)

**This section MUST be included in every CLAUDE.md file:**

```markdown
## Development Principles

### Leveraging Available Tools

Before starting any task, check what skills and MCP servers are available in your current context:

- Review the available skills list for specialized capabilities that can help with the task
- Check available MCP servers for tools that provide enhanced functionality
- Use the most appropriate tools for each task rather than doing everything manually

### RFD Documentation

For any significant change (new features, bug fixes, architectural changes - not simple one-line fixes or renames), create or update an RFD (Request for Development) document:

- **Location**: `.claude/checkpoints/checkpoint-{N}/rfd/{N}-{feature-slug}/rfd-{YYYY-MM-DD}-{HHMM}.md`
- **Workflow**:
  1. Write the question/problem being addressed
  2. Document your plan for addressing it
  3. Implement the solution
  4. Update the RFD with what was done, problems encountered, and how they were solved

### Planning First

Always start with planning before implementation:

- For features requiring RFDs, write the RFD first
- For simpler tasks, think through the approach before coding
- Consider edge cases, error handling, and testing strategy upfront

### Package Documentation

When working with unfamiliar packages or libraries:

1. **First**: Check available MCP servers for documentation tools. If available, always use Context7 MCP when I need library/API documentation, code generation, setup or configuration steps without me having to explicitly ask.
2. **Second**: Search online for documentation
3. **Third**: Ask the user for clarification

### UI/Web Testing

For frontend development and web applications:

- Check available skills for browser automation/testing capabilities
- Take screenshots to verify visual changes
- Test user flows and form interactions

### Testing Requirements

Before handing off any work to the user:

- Run all relevant tests
- Verify the changes work as expected
- Fix any failures or regressions
- If tests don't exist for the changed code, consider adding them
```

### Documentation Hierarchy Section

```markdown
## Documentation Hierarchy

This project uses a structured documentation system in `.claude/`:

### Checkpoints (`.claude/checkpoints/`)

Point-in-time documentation of project state:

- **checkpoint-0/**: Pre-development (contains PRD)
- **checkpoint-N/**: Development milestones (contain snapshots and RFDs)

### Key Documents

- **prd.md**: Product Requirements Document (checkpoint-0) - project vision and requirements
- **snapshot.md**: Technical codebase snapshot - comprehensive project state at a checkpoint
- **rfd/**: Request for Development documents - feature requests and implementation tracking

### References (`.claude/references/`)

Supporting documentation not tied to specific checkpoints:

- Team guidelines, package docs, workflows, API specs

### Document Relationships
```

PRD (vision) → RFDs (features) → Snapshots (state) → CLAUDE.md (quick reference)

```

For full project context, read the latest snapshot. For specific features, check relevant RFDs.
```

---

## Phase 5: Customize Per-Project Content

**Goal**: Add project-specific information without bloat

**Actions**:

1. Add any project-specific conventions or patterns:

   - Code organization rules
   - Naming conventions
   - Required patterns or anti-patterns

2. **Keep it concise**: If a section would be more than 10 lines, consider whether it belongs in a reference document instead

---

## Phase 6: Verify Conciseness

**Goal**: Ensure CLAUDE.md doesn't bloat the context window

**Actions**:

1. Review the updated CLAUDE.md file(s)
2. Target length: **under 200 lines** per file
3. If longer, move detailed content to:

   - `.claude/references/` for guidelines and detailed docs
   - README.md for user-facing documentation
   - Inline comments for code-specific details

4. CLAUDE.md should be scannable:
   - Use headers for organization
   - Use bullet points for lists
   - Use tables for structured data
   - Avoid long paragraphs

---

## Phase 7: Save and Report

**Goal**: Apply changes and summarize

**Actions**:

1. Save updates to each CLAUDE.md file

2. Report to user:
   - Which CLAUDE.md files were updated
   - Summary of changes made
   - Any recommendations for additional documentation

---

## What NOT to Include in CLAUDE.md

To keep CLAUDE.md concise:

- **NO** comprehensive API documentation (use snapshots or dedicated docs)
- **NO** detailed tutorials or guides (use references or README)
- **NO** full command reference (only essential commands)
- **NO** change history (use git/RFDs for that)
- **NO** duplicate information from other docs (reference them instead)
- **NO** information Claude can easily discover from the code

---

## Example CLAUDE.md Structure

```markdown
# CLAUDE.md

Brief description of what this project is.

## Quick Commands

| Task    | Command         |
| ------- | --------------- |
| Install | `npm install`   |
| Dev     | `npm run dev`   |
| Test    | `npm test`      |
| Build   | `npm run build` |

## Development Principles

[Include the full Development Principles section from Phase 4]

## Code Conventions

- Brief convention 1
- Brief convention 2

## Documentation Hierarchy

[Include the hierarchy section from Phase 4]

## Key Files

- `src/index.ts` - Main entry point
- `src/config/` - Configuration files
```

---

## Safety Guidelines

**DO NOT:**

- Make CLAUDE.md excessively long (target < 200 lines)
- Duplicate information that exists elsewhere
- Remove project-specific customizations without asking
- Create new CLAUDE.md files (only update existing ones)

**DO:**

- Ensure all CLAUDE.md files have the Development Principles section
- Keep information scannable and well-organized
- Reference detailed docs rather than duplicating content
- Preserve the user's existing structure when possible
