---
description: Generate comprehensive technical snapshot of a codebase for handoff or documentation
argument-hint: "[optional: path/to/project]"
---

# Project Snapshot Generator

Generate a comprehensive technical snapshot of a codebase that serves as a complete handoff document for developers unfamiliar with the project, using code-explorer agents for deep analysis.

**Arguments**: $ARGUMENTS

## Core Principles

- **Read existing context first**: Always read PRDs, previous snapshots, and RFDs before exploring
- **Use agents for depth**: Launch code-explorer agents to understand codebase deeply
- **Be specific**: Use actual file paths, function names, and code references
- **Track evolution**: Note how things have changed from previous checkpoints
- **Clarity over brevity**: Prioritize clear, thorough communication over keeping things concise. A snapshot should be comprehensive enough that any developer can fully understand the project without needing to ask questions. Avoid unnecessary summarization that loses important details.
- **Capture the full picture**: Include UI/UX, design, aesthetics, and multimedia aspects—not just backend logic

---

## Phase 0: Determine Target

**Goal**: Identify project root

**Target Directory**: $ARGUMENTS

- If `$ARGUMENTS` is provided, use that path as the project root
- If no argument is provided, use the current working directory

**Output Location**: `{project_root}/.claude/checkpoints/checkpoint-{N}/snapshot.md`

---

## Phase 1: Checkpoint Setup

**Goal**: Determine checkpoint number and create directory

**Actions**:

1. Check if `.claude/checkpoints/` directory exists

2. If it doesn't exist, create it and use `checkpoint-1`

3. If it exists, count existing checkpoint folders and increment:

```bash
CHECKPOINT_COUNT=$(find {project_root}/.claude/checkpoints -maxdepth 1 -type d -name "checkpoint-*" 2>/dev/null | wc -l)
NEXT_CHECKPOINT=$((CHECKPOINT_COUNT + 1))
```

4. Create the new checkpoint directory: `.claude/checkpoints/checkpoint-{N}/`

---

## Phase 2: Read Existing Documentation

**Goal**: Build context from existing documentation before exploring

**CRITICAL**: This phase must complete before codebase exploration.

**Actions**:

1. **List all existing checkpoints**:

```bash
ls -d {project_root}/.claude/checkpoints/checkpoint-* 2>/dev/null | sort -V
```

2. **For each checkpoint (in order), read**:
   - `prd.md` (if exists, typically in checkpoint-0)
   - `snapshot.md` (if exists)
   - All RFDs in the `rfd/` folder:

   ```bash
   find {project_root}/.claude/checkpoints/checkpoint-*/rfd -name "rfd-*.md" 2>/dev/null | sort
   ```

3. **Read all reference documents**:

```bash
find {project_root}/.claude/references -name "*.md" 2>/dev/null | sort
```

4. **Extract insights from existing documentation**:
   - Project vision and goals (from PRD)
   - Evolution of the codebase (from snapshots)
   - Feature requests and their implementation status (from RFDs)
   - Design decisions made along the way
   - Known issues and technical debt mentioned previously
   - Team guidelines and coding standards (from references)
   - Internal tooling and package usage (from references)
   - Workflow procedures (from references)

---

## Phase 3: Codebase Exploration with Agents

**Goal**: Deep understanding of the current codebase using code-explorer agents

**Actions**:

1. Launch 4 code-explorer agents in parallel with different focuses:

   **Agent 1 - Architecture Overview**:

   ```
   Analyze the overall architecture of this codebase. Focus on:
   - Directory structure and module organization
   - Technology stack (frontend, backend, database, infrastructure)
   - Design patterns and architectural decisions
   - Configuration and build setup
   - Entry points and main execution flow

   Return a list of 5-10 key architectural files to read.
   ```

   **Agent 2 - Feature Analysis**:

   ```
   Identify and analyze all features in this codebase. Focus on:
   - Completed features and their implementation
   - In-progress features (partial implementation, TODOs)
   - Planned features (mentioned in docs/comments)
   - Key components and their responsibilities

   Return a list of 5-10 key feature files to read.
   ```

   **Agent 3 - Development Context**:

   ```
   Analyze the development context of this codebase. Focus on:
   - Testing strategy and coverage
   - Deployment and CI/CD setup
   - Development workflow (scripts, commands)
   - Dependencies and third-party integrations
   - Known issues and technical debt

   Return a list of 5-10 key development files to read.
   ```

   **Agent 4 - UI/UX & Design Analysis**:

   ```
   Analyze the UI, UX, and visual design aspects of this codebase. Focus on:
   - Design system and component library used (e.g., shadcn/ui, Material UI, custom)
   - Color palette, themes, and color variables/tokens
   - Typography: fonts, sizes, weights, line heights
   - Spacing system and layout patterns
   - Button styles, form elements, and interactive components
   - Icons, images, and multimedia assets
   - Animation and transition patterns
   - Responsive design breakpoints and mobile considerations
   - Accessibility features (ARIA, keyboard nav, screen reader support)
   - Dark mode / light mode implementation
   - CSS architecture (Tailwind, CSS modules, styled-components, etc.)
   - Design tokens and theming configuration files

   Return a list of 5-10 key design/style files to read (CSS, theme configs, component files with significant styling).
   ```

2. Wait for all agents to complete

3. Read all key files identified by agents

4. Synthesize findings into comprehensive understanding

---

## Phase 4: Compare with Previous Checkpoint

**Goal**: Identify changes since last snapshot

**Actions**:

1. If this is not checkpoint-1:
   - Compare current state with previous snapshot
   - Identify new features implemented
   - Note features modified or refactored
   - List bug fixes
   - Document dependency updates
   - Highlight architecture changes
   - Note configuration changes

2. If this is checkpoint-1:
   - Note: "First codebase snapshot - no previous checkpoint to compare."

---

## Phase 5: Generate Snapshot

**Goal**: Write comprehensive snapshot document

**Actions**:

Generate the snapshot following the template structure below.

Key sections to include:

1. **Executive Summary** - Project overview, status, checkpoint info
2. **Changes Since Last Checkpoint** - What's new since previous snapshot
3. **User Context** - Target users, needs, use cases
4. **Project Vision & Goals** - Core purpose, objectives, philosophy
5. **Features Inventory** - Completed, in-progress, and planned features
6. **Architecture & System Design** - High-level architecture, tech stack, data flow
7. **Key Components Deep Dive** - Detailed component documentation
8. **User Interface (UI) Design** - Visual design system, colors, typography, components, styling architecture
9. **User Experience (UX) Design** - Interaction patterns, user flows, navigation, accessibility, responsive behavior
10. **Development Guidelines** - Coding conventions, patterns, environment setup
11. **Testing Strategy** - Test framework, types, coverage
12. **Deployment & Operations** - Build process, deployment, monitoring
13. **Security Considerations** - Auth, authorization, data protection
14. **Dependencies & Third-Party Services** - Critical dependencies, external services
15. **Known Issues & Technical Debt** - Open issues, TODOs, tech debt
16. **RFD Summary** - Table of all RFDs with status
17. **References Summary** - Table of all reference documents
18. **Glossary** - Project-specific terms
19. **Quick Reference** - Common commands, important files

---

## Phase 6: Save and Report

**Goal**: Write file and confirm completion

**Actions**:

1. Write the snapshot to `{project_root}/.claude/checkpoints/checkpoint-{N}/snapshot.md`

2. Report completion with:
   - File path
   - Checkpoint number
   - Summary of key findings
   - Notable changes since last checkpoint (if applicable)

---

## Writing Guidelines

1. **Be Specific**: Use actual file paths, function names, and code references
2. **Be Honest**: If something is unclear or poorly documented, note it
3. **Be Complete**: Don't skip sections—mark as "N/A" or "Not found" if truly not applicable
4. **Be Practical**: Focus on information a new developer would actually need
5. **Use Code Examples**: Include short code snippets where they clarify understanding
6. **ASCII Diagrams**: Use text diagrams for architecture when helpful
7. **Reference RFDs**: When discussing features, reference their RFD documents if available
8. **Track Evolution**: Note how things have changed from previous checkpoints
9. **Document References**: List all available reference documents so developers know what resources exist
10. **Prioritize Clarity Over Brevity**: Write thorough explanations. Do NOT over-summarize or condense information just to save space. A complete picture is more valuable than a short document. If explaining something fully takes 3 paragraphs, use 3 paragraphs.
11. **Capture Visual/Design Details**: Document colors (with hex codes), fonts, spacing values, animation timings, and other design specifics. Developers recreating the UI need these exact values.
12. **Include Multimedia Context**: Note any images, icons, videos, audio, or other media assets used, where they're stored, and how they're integrated.

---

## .claude Folder Structure Reference

```
.claude/
├── checkpoints/                     # Project checkpoints (snapshots over time)
│   ├── checkpoint-0/                # Initial checkpoint (before development)
│   │   ├── prd.md                   # Product Requirements Document
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
└── references/                      # Reference documents
    ├── team-guidelines/
    ├── package-docs/
    ├── workflows/
    ├── api-specs/
    └── {other-reference-folders}/
```

### Document Types

- **prd.md**: Product Requirements Document - exists in checkpoint-0, describes product vision and requirements
- **snapshot.md**: Technical snapshot of the codebase at a point in time (this is what you're creating)
- **rfd/**: Request for Development documents
  - Each RFD is in a numbered folder: `{N}-{feature-name}/`
  - Inside each folder: `rfd-{YYYY-MM-DD}-{HHMM}.md` with timestamp of creation
  - RFDs describe: user's feature request, implementation progress, current status
- **references/**: Reference documents providing context but not directly part of development

---

## Snapshot Template (the example below is overcondensed for brevity. Yours does not need to be this short. The template aims to show you an example structure; not the desired level of brevity)

# Project Snapshot: {PROJECT_NAME}

> Generated on {DATE} | Checkpoint: checkpoint-{N} | Status: {STATUS}

---

## 1. Executive Summary

| Attribute                | Value                                   |
| ------------------------ | --------------------------------------- |
| **Project Name**         | {name}                                  |
| **One-Line Description** | {description}                           |
| **Current Status**       | {Active Development / MVP / Production} |
| **Checkpoint**           | checkpoint-{N}                          |
| **Snapshot Date**        | {YYYY-MM-DD}                            |
| **Primary Language(s)**  | {languages}                             |

---

## 2. Changes Since Last Checkpoint

_If checkpoint-1: "First codebase snapshot - no previous checkpoint to compare."_

- **New Features**: {Feature} (RFD #{N}) — {description}
- **Modified**: {changes}
- **Bug Fixes**: {fixes}
- **Dependencies**: {updates}
- **Config Changes**: {new env vars, modified configs}

---

## 3. User Context

**Target Users**: {Who uses this?}
**Needs Addressed**: {What problems solved?}
**Key Use Cases**: 1) {case 1} 2) {case 2} 3) {case 3}

---

## 4. Project Vision & Goals

**Core Purpose**: {Why does this exist?}
**Key Objectives**: {objectives}
**Design Philosophy**: {principles}
**Non-Goals**: {what this does NOT do}

---

## 5. Features Inventory

| Feature | Description | Location | Status                        | RFD  |
| ------- | ----------- | -------- | ----------------------------- | ---- |
| {name}  | {desc}      | `{path}` | Completed/In-Progress/Planned | #{N} |

---

## 6. Architecture & System Design

### 6.1 High-Level Architecture

**Pattern**: {Monolith / Microservices / Serverless}

```
[System Diagram - Client → Server → Database]
```

### 6.2 Directory Structure

```
{project}/
├── src/           # Source code
├── tests/         # Test files
├── .claude/       # Checkpoints & references
└── config/        # Configuration
```

### 6.3 Technology Stack

| Layer    | Technology         | Version |
| -------- | ------------------ | ------- |
| Frontend | {React/Vue/etc.}   | {ver}   |
| Backend  | {Node/Python/etc.} | {ver}   |
| Database | {PostgreSQL/etc.}  | {ver}   |
| Hosting  | {Vercel/AWS/etc.}  | —       |

### 6.4 API Design

**Base URL**: `{/api/v1}` | **Auth**: {method}

| Method              | Endpoint    | Purpose   |
| ------------------- | ----------- | --------- |
| GET/POST/PUT/DELETE | `/resource` | {purpose} |

---

## 7. Key Components Deep Dive

### {Component Name}

**Purpose**: {what it does} | **Location**: `{path}`
**Dependencies**: `{deps}` | **Key Exports**: `{exports}`

---

## 8. User Interface (UI) Design

### 8.1 Design System

| Aspect           | Implementation                 |
| ---------------- | ------------------------------ |
| UI Framework     | {shadcn/ui, Material UI, etc.} |
| CSS Architecture | {Tailwind, CSS Modules, etc.}  |
| Design Tokens    | `{path}`                       |

### 8.2 Color Palette

| Type     | Colors (Name: Hex, CSS Var)                                       |
| -------- | ----------------------------------------------------------------- |
| Primary  | Primary: #{hex} `--primary`, Secondary: #{hex}, Accent: #{hex}    |
| Neutral  | Background: #{hex}, Surface: #{hex}, Text: #{hex}, Border: #{hex} |
| Semantic | Success: #{hex}, Warning: #{hex}, Error: #{hex}, Info: #{hex}     |

### 8.3 Typography

| Purpose  | Font   | Sizes                                                    |
| -------- | ------ | -------------------------------------------------------- |
| Headings | {font} | xs:12px, sm:14px, base:16px, lg:18px, xl:20px, 2xl:24px  |
| Body     | {font} | Weights: 400 regular, 500 medium, 600 semibold, 700 bold |

### 8.4 Component Styles

**Buttons**: Primary/Secondary/Ghost/Danger — Sizes: sm:32px, md:40px, lg:48px
**Form Elements**: Input, Select, Checkbox — Border: {style}, Focus: {ring}, Error: {color}
**Cards**: Background: {color}, Shadow: {values}, Radius: {px}

### 8.5 Icons & Assets

| Type   | Library/Location            | Format   |
| ------ | --------------------------- | -------- |
| Icons  | {Lucide/Heroicons} `{path}` | SVG      |
| Images | `{path}`                    | WebP/PNG |

### 8.6 Animations

**Transitions**: All: 150ms ease-in-out, Transform: 200ms, Opacity: 150ms
**Patterns**: fadeIn: 200ms, slideUp: 300ms, scaleIn: 150ms

### 8.7 Theming

**Implementation**: {CSS variables / Tailwind dark:}
**Toggle Location**: `{path}`

---

## 9. User Experience (UX) Design

### 9.1 Navigation

| Element    | Type               | Behavior           |
| ---------- | ------------------ | ------------------ |
| Main Nav   | {Top bar/Sidebar}  | {Sticky/Fixed}     |
| Mobile Nav | {Hamburger/Bottom} | {Slide-in/Overlay} |

### 9.2 Interaction Patterns

**Loading**: {Skeleton/Spinner} | **Empty States**: {message + CTA} | **Feedback**: Toast/Inline

### 9.3 Responsive Behavior

**Breakpoints**: sm:640px, md:768px, lg:1024px, xl:1280px | **Approach**: {Mobile-first}

### 9.4 Accessibility

**Target**: {WCAG 2.1 AA}
**Features**: Semantic HTML, ARIA labels, Keyboard nav, Focus indicators, Color contrast 4.5:1

---

## 10. Development Guidelines

**Style Config**: `{.eslintrc, .prettierrc}`
**Naming**: Files: kebab-case, Components: PascalCase, Functions: camelCase

**Commands**:

```bash
{dev command}      # Start dev
{test command}     # Run tests
{build command}    # Build
```

**Environment Variables**: `{VAR_NAME}` — {purpose}

---

## 11. Testing Strategy

| Type                 | Framework         | Location | Command |
| -------------------- | ----------------- | -------- | ------- |
| Unit/Integration/E2E | {Jest/Playwright} | `{path}` | `{cmd}` |

---

## 12. Deployment & Operations

**Target**: {Platform} | **Build**: `{command}` → `{output path}`
**Monitoring**: Logging: {tool}, Errors: {Sentry}, Metrics: {tool}

---

## 13. Security Considerations

| Area       | Implementation        |
| ---------- | --------------------- |
| Auth       | {method}              |
| Data       | {encryption approach} |
| Validation | {library/method}      |

---

## 14. Dependencies & External Services

| Package/Service | Version | Purpose   |
| --------------- | ------- | --------- |
| {name}          | {ver}   | {purpose} |

---

## 15. Known Issues & Technical Debt

- [ ] {Issue} — `{location}` — Priority: {High/Med/Low}

---

## 16. RFD Summary

| RFD # | Feature | Status   | Checkpoint     |
| ----- | ------- | -------- | -------------- |
| {N}   | {name}  | {status} | checkpoint-{N} |

---

## 17. References Summary

| Category | Document | Path                        |
| -------- | -------- | --------------------------- |
| {folder} | {name}   | `.claude/references/{path}` |

---

## 18. Glossary

**PRD**: Product Requirements Document | **RFD**: Request for Development | **Checkpoint**: Point-in-time snapshot

---

## 19. Quick Reference

**Commands**: `{dev}` | `{test}` | `{build}` | `{deploy}`
**Key Files**: `{path}` — {purpose}
**Resources**: Repo: {URL} | Docs: {URL}

---

_Generated on {DATE} for checkpoint-{N}_
