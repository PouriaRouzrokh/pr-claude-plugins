---
description: Generate comprehensive Product Requirements Document (PRD) through interactive discovery and research
argument-hint: "[optional: path/to/ideas.md or free-text description]"
---

# Create PRD Command

You are helping the user create a Product Requirements Document for a new project.

**Arguments**: $ARGUMENTS

## Instructions

Follow the complete workflow defined in the `create-prd` skill located at `skills/create-prd/SKILL.md`.

The skill guides you through:

1. **Phase 0: Input Processing** - Read any provided ideas file or description
2. **Phase 1: Discovery Interview** - Interview the user about their project vision, scope, tech preferences, design, and constraints
3. **Phase 2: Deep Research** - Research technology choices, integrations, and best practices using web search
4. **Phase 3: Propose and Confirm** - Present recommendations and get user confirmation
5. **Phase 4: Generate PRD** - Create comprehensive PRD using the embedded template
6. **Phase 5: Save and Report** - Write to `.claude/checkpoints/checkpoint-0/prd.md` and report completion

## Key Principles

- **Interview first**: Ask focused questions, one topic at a time
- **Research while interviewing**: When user mentions something, search for context
- **Accept uncertainty**: "Use your best judgment" is a valid answer
- **Synthesize intelligently**: Don't just list search results, provide recommendations

Read the full skill file for detailed instructions, interview stages, the PRD template, and quality checklist.
