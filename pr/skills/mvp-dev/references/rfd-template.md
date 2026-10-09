# MVP Feature RFD Template

Use this structure for every feature RFD created in Step 4.1 of `mvp-dev`. Fill sections as the feature progresses; never delete a section, write "N/A" with a reason instead.

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

## MVP Completion Summary

Present this to the user at the end of Phase 6.

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
