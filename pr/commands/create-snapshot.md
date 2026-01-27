---
description: Generate comprehensive technical snapshot of a codebase for handoff or documentation
argument-hint: "[optional: path/to/project]"
---

# Create Snapshot Command

You are helping the user create a comprehensive technical snapshot of a codebase.

**Arguments**: $ARGUMENTS

## Instructions

Follow the complete workflow defined in the `create-snapshot` skill located at `skills/create-snapshot/SKILL.md`.

The skill guides you through:

1. **Phase 0: Determine Target** - Identify project root (from arguments or current directory)
2. **Phase 1: Checkpoint Setup** - Determine next checkpoint number and create directory
3. **Phase 2: Read Existing Documentation** - Read PRDs, previous snapshots, RFDs, and references
4. **Phase 3: Codebase Exploration with Agents** - Launch 3 code-explorer agents (architecture, features, development context)
5. **Phase 4: Compare with Previous Checkpoint** - Identify changes since last snapshot
6. **Phase 5: Generate Snapshot** - Write comprehensive snapshot using the template
7. **Phase 6: Save and Report** - Write to `.claude/checkpoints/checkpoint-{N}/snapshot.md` and report

## Key Principles

- **Read existing context first**: Always read PRDs, previous snapshots, and RFDs before exploring
- **Use agents for depth**: Launch code-explorer agents to understand codebase deeply
- **Be specific**: Use actual file paths, function names, and code references
- **Track evolution**: Note how things have changed from previous checkpoints

The snapshot template is located at `skills/create-snapshot/template.md`.

Read the full skill file for detailed instructions, agent prompts, and writing guidelines.
