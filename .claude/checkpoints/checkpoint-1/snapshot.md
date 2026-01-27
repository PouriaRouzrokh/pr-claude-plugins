# Project Snapshot: pr-claude-plugins

> Generated on 2026-01-27 | Checkpoint: checkpoint-1 | Status: Active Development

---

## 1. Executive Summary

| Attribute                      | Value                                                                          |
| ------------------------------ | ------------------------------------------------------------------------------ |
| **Project Name**               | pr-claude-plugins                                                              |
| **One-Line Description**       | Claude Code plugin marketplace containing the pr personal development toolkit  |
| **Current Status**             | Active Development                                                             |
| **Checkpoint**                 | checkpoint-1                                                                   |
| **Previous Checkpoint**        | N/A (first snapshot)                                                           |
| **Snapshot Date**              | 2026-01-27                                                                     |
| **Primary Language(s)**        | Markdown (declarative plugin definitions)                                      |
| **License**                    | Not specified                                                                  |

---

## 2. Changes Since Last Checkpoint

*First codebase snapshot - no previous checkpoint to compare.*

This is the initial snapshot capturing the v1.0.0 release of the pr-claude-plugins marketplace.

---

## 3. User Context

### Target Users

Claude Code users who want systematic, structured workflows for software development tasks including feature development, MVP creation, code cleanup, documentation, and deployment.

### User Needs Addressed

- **Systematic Development**: Structured phase-based workflows prevent ad-hoc development
- **Documentation Management**: Automatic RFD/PRD/checkpoint tracking of project evolution
- **Quality Assurance**: Automated code review with confidence-based filtering
- **Architecture Design**: Multi-agent exploration and design before implementation
- **Git Operations**: Streamlined commit, push, merge, and PR workflows

### Key Use Cases

1. Starting a new project from scratch with PRD generation and MVP development
2. Adding features to existing projects with full exploration and RFD tracking
3. Cleaning up and professionalizing codebases before release
4. Maintaining project documentation as code evolves
5. Committing changes with proper logging and optional PR creation

---

## 4. Project Vision & Goals

### Core Purpose

Provide Claude Code users with a personal development toolkit that brings structure, documentation, and quality assurance to software development through specialized agents and systematic workflows.

### Key Objectives

- Enable systematic feature development with proper documentation
- Provide deep codebase understanding through parallel agent exploration
- Ensure code quality through confidence-based automated review
- Maintain project history through checkpoint and RFD systems
- Support both solo developers and small teams

### Design Philosophy

- **Phase-based workflows**: Every command follows numbered phases with clear goals
- **Agent-driven exploration**: Launch 2-3 specialized agents in parallel for deep understanding
- **Documentation-first**: RFD/PRD/snapshot system ensures requirements are always tracked
- **Ask before acting**: Explicit user confirmation before major changes
- **Read files identified by agents**: Always read the 5-10 key files agents recommend

### Non-Goals

- Not a replacement for project management tools
- Not designed for large team coordination
- Not a CI/CD replacement (though it integrates with git workflows)

---

## 5. Features Inventory

### 5.1 Completed Features

| Feature            | Description                                                        | Location                              | RFD Reference |
| ------------------ | ------------------------------------------------------------------ | ------------------------------------- | ------------- |
| Feature Dev        | Guided feature development with RFD tracking                       | `pr/commands/feature-dev.md`          | N/A           |
| MVP Dev            | Full MVP development from PRD with per-feature RFDs                | `pr/commands/mvp-dev.md`              | N/A           |
| Commit Push        | Git workflow with commitlog.md maintenance                         | `pr/commands/commit-push.md`          | N/A           |
| Clean Codebase     | Code cleanup using automated code-reviewer agents                  | `pr/commands/clean-codebase.md`       | N/A           |
| Update Docs        | Documentation updates using code-explorer agents                   | `pr/commands/update-docs.md`          | N/A           |
| Run Local          | Local development server management                                | `pr/commands/run-local.md`            | N/A           |
| Run Public         | Public deployment management                                       | `pr/commands/run-public.md`           | N/A           |
| Create PRD         | Interactive PRD generation with web research                       | `pr/skills/create-prd/SKILL.md`       | N/A           |
| Create Snapshot    | Technical codebase snapshot generation                             | `pr/skills/create-snapshot/SKILL.md`  | N/A           |
| Code Explorer      | Yellow agent for tracing execution paths                           | `pr/agents/code-explorer.md`          | N/A           |
| Code Architect     | Green agent for designing implementations                          | `pr/agents/code-architect.md`         | N/A           |
| Code Reviewer      | Red agent for quality review with confidence scoring               | `pr/agents/code-reviewer.md`          | N/A           |

### 5.2 In-Progress Features

| Feature   | Current State | Remaining Work | RFD Reference |
| --------- | ------------- | -------------- | ------------- |
| —         | —             | —              | —             |

*No features currently in progress.*

### 5.3 Planned Features

| Feature   | Source                 | Notes   | RFD Reference |
| --------- | ---------------------- | ------- | ------------- |
| —         | —                      | —       | —             |

*No features explicitly planned in documentation.*

---

## 6. Architecture & System Design

### 6.1 High-Level Architecture

**Pattern**: Declarative Markdown-based Plugin System

```
┌─────────────────────────────────────────────────────────────────┐
│                    pr-claude-plugins                             │
│                    (Marketplace Root)                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                     pr Plugin                            │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │    │
│  │  │  Commands   │  │   Skills    │  │   Agents    │      │    │
│  │  │  (9 files)  │  │  (2 skills) │  │  (3 agents) │      │    │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘      │    │
│  │         │                │                │              │    │
│  │         └────────────────┼────────────────┘              │    │
│  │                          │                               │    │
│  │                          ▼                               │    │
│  │         ┌────────────────────────────────┐               │    │
│  │         │  Claude Code Runtime Tools     │               │    │
│  │         │  (Glob, Grep, Read, WebSearch) │               │    │
│  │         └────────────────────────────────┘               │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Directory Structure

```
pr-claude-plugins/
├── .claude-plugin/
│   └── marketplace.json     # Marketplace manifest
├── pr/                       # The pr plugin
│   ├── .claude-plugin/
│   │   └── plugin.json      # Plugin manifest
│   ├── agents/              # Subagent definitions (3 files)
│   │   ├── code-explorer.md # Yellow - traces execution paths
│   │   ├── code-architect.md # Green - designs implementations
│   │   └── code-reviewer.md # Red - reviews with confidence scoring
│   ├── commands/            # Slash commands (9 files)
│   │   ├── feature-dev.md   # /pr:feature-dev
│   │   ├── mvp-dev.md       # /pr:mvp-dev
│   │   ├── commit-push.md   # /pr:commit-push
│   │   ├── clean-codebase.md # /pr:clean-codebase
│   │   ├── update-docs.md   # /pr:update-docs
│   │   ├── run-local.md     # /pr:run-local
│   │   ├── run-public.md    # /pr:run-public
│   │   ├── create-prd.md    # /pr:create-prd (wrapper)
│   │   └── create-snapshot.md # /pr:create-snapshot (wrapper)
│   ├── skills/              # Reusable workflows
│   │   ├── create-prd/
│   │   │   └── SKILL.md     # PRD generation workflow
│   │   └── create-snapshot/
│   │       ├── SKILL.md     # Snapshot generation workflow
│   │       └── template.md  # Snapshot template
│   └── README.md            # Plugin documentation
├── .claude/
│   └── checkpoints/
│       └── checkpoint-1/
│           └── snapshot.md  # This file
├── CLAUDE.md                # Project guidelines
├── commitlog.md             # Commit history
└── README.md                # Marketplace installation docs
```

### 6.3 Technology Stack

#### Core Technology

| Category         | Technology                  | Notes                                      |
| ---------------- | --------------------------- | ------------------------------------------ |
| Implementation   | Markdown + YAML frontmatter | 100% declarative, no runtime code          |
| Platform         | Claude Code Plugin System   | Marketplace distribution                   |
| Version Control  | Git                         | GitHub repository as marketplace source    |

#### No Build System Required

- No npm/pip/etc dependencies
- Direct file reading by Claude Code
- Pure markdown configuration

### 6.4 Data Flow

```
1. User invokes /pr:command
       │
       ▼
2. Claude Code loads command markdown file
       │
       ▼
3. Command executes phase-by-phase
       │
       ├──────────────────────────────────────┐
       │                                      │
       ▼                                      ▼
4a. Launch agents in parallel        4b. Interact with user
    (2-3 code-explorer/architect/        (clarifying questions,
     reviewer agents)                     confirmations)
       │                                      │
       ▼                                      │
5. Agents return findings +           ◄───────┘
   5-10 key files to read
       │
       ▼
6. Read identified files, synthesize understanding
       │
       ▼
7. Implementation / Documentation / Git operations
       │
       ▼
8. Update RFD, commitlog.md, or other docs
       │
       ▼
9. Summary report to user
```

### 6.5 Component Relationships

**Commands** orchestrate **Agents** and may delegate to **Skills**:

```
Commands (User Entry Points)
    │
    ├── Launch Agents (parallel, different focuses)
    │       │
    │       ├── code-explorer (yellow) → returns key files
    │       ├── code-architect (green) → returns blueprints
    │       └── code-reviewer (red) → returns issues ≥80% confidence
    │
    └── Delegate to Skills (for complex workflows)
            │
            └── create-prd, create-snapshot
```

---

## 7. Key Components Deep Dive

### Commands

**Purpose**: User-facing entry points that orchestrate workflows

**Location**: `pr/commands/*.md`

**Structure**:
```yaml
---
description: Brief description
argument-hint: "[optional: hint text]"
---
```

**Key Pattern**: Phase-based execution with numbered phases, each with a goal and specific actions.

### Agents

**Purpose**: Specialized AI subagents launched by commands for deep analysis

**Location**: `pr/agents/*.md`

**Structure**:
```yaml
---
name: agent-name
description: Description
tools: Glob, Grep, Read, ...
model: sonnet
color: yellow|green|red
---
```

| Agent | Color | Specialization |
|-------|-------|----------------|
| code-explorer | Yellow | Traces execution paths, maps architecture, returns 5-10 key files |
| code-architect | Green | Designs implementations with complete blueprints suitable for RFDs |
| code-reviewer | Red | Reviews code with confidence scoring, only reports issues ≥80% |

### Skills

**Purpose**: Complex multi-phase workflows with supporting files

**Location**: `pr/skills/{skill-name}/SKILL.md`

**Structure**:
```yaml
---
name: skill-name
description: Description
argument-hint: "[hint]"
---
```

**Supporting Files**: Templates, reference documents in same directory

---

## 8. Design & UX

### 8.1 Design System

This is a CLI plugin with no visual UI. Design considerations focus on:

| Aspect             | Implementation                        |
| ------------------ | ------------------------------------- |
| Output Format      | Markdown (tables, code blocks, lists) |
| Color Coding       | Agents have colors (yellow/green/red) |
| Progress Tracking  | TodoWrite tool for phase tracking     |

### 8.2 Interaction Patterns

- **Phase-based disclosure**: Information revealed progressively through phases
- **Confirmation gates**: User approval required before major actions
- **Question-answer loops**: Clarifying questions before implementation
- **Summary reports**: Completion summaries at end of each command

---

## 9. Development Guidelines

### 9.1 Component Conventions

**Commands**:
- Use imperative descriptions: "Commit changes" not "Commits changes"
- Structure as phases with clear goals
- Include "DO NOT" and "ALWAYS" safety guidelines
- Support $ARGUMENTS for user input

**Agents**:
- Return 5-10 key files for commands to read
- Use confidence scoring for code-reviewer (≥80% threshold)
- Include specific file:line references

**Skills**:
- Name file as SKILL.md in dedicated folder
- Include template files as needed
- Support wrapper commands for invocation

### 9.2 Documentation Structure

The plugin creates this structure in target projects:

```
.claude/
├── checkpoints/
│   ├── checkpoint-0/           # Pre-development
│   │   ├── prd.md              # Product Requirements Document
│   │   └── rfd/                # Request for Development documents
│   │       └── {N}-{feature-slug}/
│   │           └── rfd-{YYYY-MM-DD}-{HHMM}.md
│   ├── checkpoint-1/           # First development checkpoint
│   │   ├── snapshot.md         # Technical snapshot
│   │   └── rfd/
│   └── checkpoint-{N}/         # Additional checkpoints
└── references/                 # Reference documents
```

### 9.3 RFD Status Values

- **Planning**: Initial request captured, exploring and clarifying
- **In Progress**: Implementation actively underway
- **Completed**: Feature fully implemented and reviewed
- **On Hold**: Paused due to blockers or priority changes

---

## 10. Testing Strategy

| Type        | Framework                 | Location   | Command     |
| ----------- | ------------------------- | ---------- | ----------- |
| —           | —                         | —          | —           |

*No automated tests exist for this plugin. The plugin is tested through manual usage.*

---

## 11. Deployment & Operations

### 11.1 Installation

```bash
# Add the marketplace
/plugin marketplace add PouriaRouzrokh/pr-claude-plugins

# Install the plugin
/plugin install pr@pr-cloud-plugins
```

### 11.2 Updating

```bash
/plugin marketplace update pr-cloud-plugins
```

### 11.3 Distribution

- **Source**: GitHub repository
- **Marketplace**: pr-cloud-plugins
- **Plugin**: pr

---

## 12. Security Considerations

| Area             | Implementation                          |
| ---------------- | --------------------------------------- |
| Credentials      | Never committed (.env in .gitignore)    |
| Sensitive Files  | commit-push warns about sensitive files |
| Production Data  | run-local never uses production env     |
| Secrets in Logs  | run-public never exposes secrets        |

---

## 13. Dependencies & Third-Party Services

### Critical Dependencies

| Package   | Version   | Purpose                       |
| --------- | --------- | ----------------------------- |
| —         | —         | No package dependencies       |

This is a **zero-dependency** plugin relying only on:
- Claude Code's built-in tools
- Git (for version control operations)
- GitHub CLI `gh` (optional, for PR creation)

### External Services

| Service   | Purpose              | Required |
| --------- | -------------------- | -------- |
| GitHub    | Repository hosting   | Yes      |
| gh CLI    | PR creation          | Optional |

---

## 14. Known Issues & Technical Debt

### Open Issues

- No automated tests for plugin commands/agents/skills

### TODOs in Code

*No TODO comments found in implementation files.*

### Technical Debt

| Item                        | Priority | Notes                                    |
| --------------------------- | -------- | ---------------------------------------- |
| No automated testing        | Low      | Manual testing sufficient for now        |
| No version pinning          | Low      | Single-developer project                 |

---

## 15. RFD Summary

*No RFDs found - this is a plugin repository, not a project using the plugin.*

| RFD # | Feature   | Status | Checkpoint     | File |
| ----- | --------- | ------ | -------------- | ---- |
| —     | —         | —      | —              | —    |

---

## 16. References Summary

*No reference documents found in `.claude/references/`.*

| Category | Document | Description | Path |
| -------- | -------- | ----------- | ---- |
| —        | —        | —           | —    |

---

## 17. Glossary

| Term           | Definition                                                      |
| -------------- | --------------------------------------------------------------- |
| **PRD**        | Product Requirements Document - product vision and requirements |
| **RFD**        | Request for Development - feature request and progress tracking |
| **Checkpoint** | Point-in-time snapshot of project state and documentation       |
| **Snapshot**   | Technical codebase documentation at a checkpoint                |
| **Agent**      | Specialized AI subagent launched by commands for deep analysis  |
| **Skill**      | Reusable multi-phase workflow with supporting files             |
| **Command**    | User-facing slash command (e.g., /pr:feature-dev)               |

---

## 18. Quick Reference

### Common Commands

```bash
# Feature development
/pr:feature-dev [description]

# MVP development from PRD
/pr:mvp-dev [focus]

# Git operations
/pr:commit-push [path] [--merge|--pr]

# Code cleanup
/pr:clean-codebase [path]

# Documentation
/pr:update-docs [path] [focus]
/pr:create-prd [ideas]
/pr:create-snapshot [path]

# Running the app
/pr:run-local [instructions]
/pr:run-public [instructions]
```

### Important Files

| File                                 | Purpose                                     |
| ------------------------------------ | ------------------------------------------- |
| `.claude-plugin/marketplace.json`    | Marketplace manifest                        |
| `pr/.claude-plugin/plugin.json`      | Plugin manifest (name, version, author)     |
| `pr/commands/*.md`                   | Command definitions                         |
| `pr/agents/*.md`                     | Agent definitions                           |
| `pr/skills/*/SKILL.md`               | Skill definitions                           |
| `CLAUDE.md`                          | Project guidelines for Claude Code          |
| `commitlog.md`                       | Project commit history                      |

### Key Resources

- **Repository**: https://github.com/PouriaRouzrokh/pr-claude-plugins
- **Author**: Pouria Rouzrokh

### Checkpoint History

| Checkpoint     | Date       | Type     | Description                |
| -------------- | ---------- | -------- | -------------------------- |
| checkpoint-1   | 2026-01-27 | Snapshot | Initial codebase snapshot  |

---

*This snapshot was automatically generated on 2026-01-27 for checkpoint-1 using the /pr:create-snapshot command.*
