# Project Snapshot: {PROJECT_NAME}

> Generated on {DATE} | Checkpoint: checkpoint-{N} | Status: {STATUS}

---

## 1. Executive Summary

| Attribute                      | Value                                                 |
| ------------------------------ | ----------------------------------------------------- |
| **Project Name**               | {name}                                                |
| **One-Line Description**       | {description}                                         |
| **Current Status**             | {Active Development / Maintenance / MVP / Production} |
| **Checkpoint**                 | checkpoint-{N}                                        |
| **Previous Checkpoint**        | checkpoint-{N-1} ({date}) or N/A if first             |
| **Snapshot Date**              | {YYYY-MM-DD}                                          |
| **Primary Language(s)**        | {languages}                                           |
| **License**                    | {license}                                             |

---

## 2. Changes Since Last Checkpoint

*If this is not the first checkpoint, summarize what has changed since the previous snapshot:*

### New Features Implemented

- {Feature name} (RFD #{N}) — {brief description}

### Features Modified or Refactored

- {Description of changes}

### Bug Fixes

- {Bug fix description}

### Dependency Updates

- {Package} updated from {old version} to {new version}

### Architecture Changes

- {Description of architectural changes}

### Configuration Changes

- New environment variables: {list}
- Modified configs: {list}

*If this is checkpoint-1, note: "First codebase snapshot - no previous checkpoint to compare."*

---

## 3. User Context

### Target Users

{Who uses this software?}

### User Needs Addressed

{What problems does this solve?}

### Key Use Cases

1. {Use case 1}
2. {Use case 2}
3. {Use case 3}

---

## 4. Project Vision & Goals

### Core Purpose

{Why does this project exist?}

### Key Objectives

- {Objective 1}
- {Objective 2}
- {Objective 3}

### Design Philosophy

{Guiding principles}

### Non-Goals

- {What this project explicitly does NOT try to do}

---

## 5. Features Inventory

### 5.1 Completed Features

| Feature     | Description   | Location   | RFD Reference |
| ----------- | ------------- | ---------- | ------------- |
| {Feature 1} | {Description} | `{path}`   | RFD #{N}      |
| {Feature 2} | {Description} | `{path}`   | RFD #{N}      |

### 5.2 In-Progress Features

| Feature   | Current State | Remaining Work | RFD Reference |
| --------- | ------------- | -------------- | ------------- |
| {Feature} | {State}       | {TODO}         | RFD #{N}      |

### 5.3 Planned Features

| Feature   | Source                 | Notes   | RFD Reference |
| --------- | ---------------------- | ------- | ------------- |
| {Feature} | {PRD/README/Issue/etc} | {Notes} | Planned / —   |

---

## 6. Architecture & System Design

### 6.1 High-Level Architecture

**Pattern**: {Monolith / Microservices / Serverless / etc.}

```
┌─────────────────────────────────────────────────────────┐
│                    System Diagram                        │
│                                                          │
│   ┌──────────┐      ┌──────────┐      ┌──────────┐      │
│   │  Client  │─────▶│  Server  │─────▶│ Database │      │
│   └──────────┘      └──────────┘      └──────────┘      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 6.2 Directory Structure

```
{project-name}/
├── .claude/
│   ├── checkpoints/            # Project checkpoints
│   │   ├── checkpoint-0/
│   │   │   ├── prd.md          # Initial product requirements
│   │   │   └── rfd/
│   │   │       └── {N}-{feature-name}/
│   │   │           └── rfd-{YYYY-MM-DD}-{HHMM}.md
│   │   ├── checkpoint-1/
│   │   │   ├── snapshot.md
│   │   │   └── rfd/
│   │   │       └── ...
│   │   └── checkpoint-{N}/
│   │       ├── snapshot.md     # This snapshot
│   │       └── rfd/
│   │           └── ...
│   └── references/             # Reference documents
│       ├── {category}/
│       │   └── {document}.md
│       └── ...
├── src/                    # Source code
│   ├── components/         # UI components
│   ├── services/           # Business logic
│   ├── utils/              # Utility functions
│   └── index.{ext}         # Entry point
├── tests/                  # Test files
├── docs/                   # Documentation
├── config/                 # Configuration files
└── {other directories}
```

### 6.3 Technology Stack

#### Frontend

| Category         | Technology                  | Notes     |
| ---------------- | --------------------------- | --------- |
| Framework        | {React/Vue/Svelte/etc.}     | {version} |
| State Management | {Redux/Zustand/etc.}        |           |
| Styling          | {Tailwind/CSS Modules/etc.} |           |
| Build Tool       | {Vite/Webpack/etc.}         |           |

#### Backend

| Category  | Technology                 | Notes     |
| --------- | -------------------------- | --------- |
| Runtime   | {Node.js/Python/Go/etc.}   | {version} |
| Framework | {Express/FastAPI/Gin/etc.} |           |
| API Style | {REST/GraphQL/gRPC}        |           |
| Auth      | {JWT/OAuth/Sessions}       |           |

#### Database

| Category   | Technology                | Notes |
| ---------- | ------------------------- | ----- |
| Database   | {PostgreSQL/MongoDB/etc.} |       |
| ORM        | {Prisma/SQLAlchemy/etc.}  |       |
| Migrations | {Tool/Method}             |       |

#### Infrastructure

| Category   | Technology            | Notes |
| ---------- | --------------------- | ----- |
| Hosting    | {Vercel/AWS/etc.}     |       |
| CI/CD      | {GitHub Actions/etc.} |       |
| Containers | {Docker/K8s/etc.}     |       |

### 6.4 Data Flow

```
1. User Action
       │
       ▼
2. {Component/Route}
       │
       ▼
3. {API/Service Layer}
       │
       ▼
4. {Database/External Service}
       │
       ▼
5. Response → UI Update
```

### 6.5 API Design

**Base URL**: `{/api/v1/...}`

**Authentication**: {Method}

| Method | Endpoint          | Purpose             |
| ------ | ----------------- | ------------------- |
| GET    | `/resource`       | List resources      |
| POST   | `/resource`       | Create resource     |
| GET    | `/resource/:id`   | Get single resource |
| PUT    | `/resource/:id`   | Update resource     |
| DELETE | `/resource/:id`   | Delete resource     |

### 6.6 Database Schema

```
┌─────────────┐       ┌─────────────┐
│   Entity A  │──────▶│   Entity B  │
├─────────────┤       ├─────────────┤
│ id          │       │ id          │
│ field_1     │       │ entity_a_id │
│ field_2     │       │ field_1     │
└─────────────┘       └─────────────┘
```

---

## 7. Key Components Deep Dive

### {Component/Module Name}

**Purpose**: {What it does}

**Location**: `{file path}`

**Dependencies**:

- `{dependency 1}`
- `{dependency 2}`

**Key Exports**:

```{language}
// Example of main exports
export { mainFunction, HelperClass, CONSTANTS };
```

**Usage Example**:

```{language}
// How to use this component
import { mainFunction } from './component';
mainFunction(params);
```

---

## 8. User Interface (UI) Design

This section documents all visual design aspects that developers need to recreate or maintain the UI.

### 8.1 Design System Overview

| Aspect               | Implementation                 | Notes                          |
| -------------------- | ------------------------------ | ------------------------------ |
| UI Framework/Library | {shadcn/ui, Material UI, etc.} | {version}                      |
| Component Location   | `{path}`                       |                                |
| Design Tokens        | `{path to theme/tokens}`       |                                |
| CSS Architecture     | {Tailwind, CSS Modules, etc.}  | {Configuration file location}  |

### 8.2 Color Palette

**Primary Colors**:

| Name      | Hex Code    | CSS Variable          | Usage                        |
| --------- | ----------- | --------------------- | ---------------------------- |
| Primary   | `#{hex}`    | `--color-primary`     | Main brand color, CTAs       |
| Secondary | `#{hex}`    | `--color-secondary`   | Secondary actions            |
| Accent    | `#{hex}`    | `--color-accent`      | Highlights, notifications    |

**Neutral Colors**:

| Name       | Hex Code    | CSS Variable           | Usage                        |
| ---------- | ----------- | ---------------------- | ---------------------------- |
| Background | `#{hex}`    | `--color-background`   | Page backgrounds             |
| Surface    | `#{hex}`    | `--color-surface`      | Card/container backgrounds   |
| Border     | `#{hex}`    | `--color-border`       | Dividers, borders            |
| Text       | `#{hex}`    | `--color-text`         | Primary text                 |
| Text Muted | `#{hex}`    | `--color-text-muted`   | Secondary/helper text        |

**Semantic Colors**:

| Name    | Hex Code    | CSS Variable        | Usage                     |
| ------- | ----------- | ------------------- | ------------------------- |
| Success | `#{hex}`    | `--color-success`   | Success states, confirms  |
| Warning | `#{hex}`    | `--color-warning`   | Warnings, cautions        |
| Error   | `#{hex}`    | `--color-error`     | Errors, destructive       |
| Info    | `#{hex}`    | `--color-info`      | Informational messages    |

**Theme Configuration File**: `{path to where colors are defined}`

### 8.3 Typography

**Font Families**:

| Purpose    | Font Family                  | Fallback Stack                        | CSS Variable       |
| ---------- | ---------------------------- | ------------------------------------- | ------------------ |
| Headings   | {Inter, Roboto, etc.}        | `-apple-system, sans-serif`           | `--font-heading`   |
| Body       | {Inter, system-ui, etc.}     | `-apple-system, sans-serif`           | `--font-body`      |
| Monospace  | {Fira Code, JetBrains, etc.} | `monospace`                           | `--font-mono`      |

**Font Sizes**:

| Name  | Size    | Line Height | Usage                          |
| ----- | ------- | ----------- | ------------------------------ |
| xs    | {12px}  | {1.4}       | Small labels, captions         |
| sm    | {14px}  | {1.5}       | Secondary text, inputs         |
| base  | {16px}  | {1.6}       | Body text                      |
| lg    | {18px}  | {1.6}       | Large body, subheadings        |
| xl    | {20px}  | {1.5}       | Small headings                 |
| 2xl   | {24px}  | {1.4}       | Section headings               |
| 3xl   | {30px}  | {1.3}       | Page headings                  |
| 4xl   | {36px}  | {1.2}       | Hero headings                  |

**Font Weights**: `{300 light, 400 regular, 500 medium, 600 semibold, 700 bold}`

### 8.4 Spacing System

**Base Unit**: `{4px / 0.25rem}`

| Token | Value   | Usage                            |
| ----- | ------- | -------------------------------- |
| 1     | {4px}   | Tight spacing, icon gaps         |
| 2     | {8px}   | Related elements                 |
| 3     | {12px}  | Form field gaps                  |
| 4     | {16px}  | Standard padding                 |
| 6     | {24px}  | Section padding                  |
| 8     | {32px}  | Large gaps                       |
| 12    | {48px}  | Section margins                  |
| 16    | {64px}  | Page sections                    |

### 8.5 Component Styles

#### Buttons

| Variant   | Background    | Text Color    | Border        | Hover State                   |
| --------- | ------------- | ------------- | ------------- | ----------------------------- |
| Primary   | `{color}`     | `{color}`     | none          | {Darken 10%, scale up 1.02}   |
| Secondary | `{color}`     | `{color}`     | `{1px solid}` | {Background opacity change}   |
| Ghost     | transparent   | `{color}`     | none          | {Light background}            |
| Danger    | `{color}`     | white         | none          | {Darken red}                  |

**Button Sizes**: `{sm: 32px, md: 40px, lg: 48px height}`

**Border Radius**: `{4px / 8px / full for pills}`

#### Form Elements

| Element      | Border        | Focus State              | Error State            |
| ------------ | ------------- | ------------------------ | ---------------------- |
| Input        | `{1px solid}` | `{ring color/width}`     | `{border color}`       |
| Select       | `{1px solid}` | `{ring color/width}`     | `{border color}`       |
| Checkbox     | `{radius}`    | `{ring color/width}`     | `{styling}`            |
| Radio        | `{styling}`   | `{ring color/width}`     | `{styling}`            |

#### Cards & Containers

| Element  | Background    | Border        | Shadow                      | Border Radius |
| -------- | ------------- | ------------- | --------------------------- | ------------- |
| Card     | `{color}`     | `{styling}`   | `{shadow values}`           | `{radius}`    |
| Modal    | `{color}`     | `{styling}`   | `{shadow values}`           | `{radius}`    |
| Dropdown | `{color}`     | `{styling}`   | `{shadow values}`           | `{radius}`    |

### 8.6 Icons & Visual Assets

**Icon System**:

| Aspect        | Implementation                    |
| ------------- | --------------------------------- |
| Icon Library  | {Lucide, Heroicons, custom, etc.} |
| Default Size  | `{24px}`                          |
| Location      | `{path}`                          |
| Usage Pattern | `{<IconName className="..." />}`  |

**Image Assets**:

| Type      | Location                | Format             | Notes              |
| --------- | ----------------------- | ------------------ | ------------------ |
| Logo      | `{path}`                | {SVG/PNG}          | {Variants}         |
| Icons     | `{path}`                | {SVG}              |                    |
| Images    | `{path}`                | {WebP/PNG/JPG}     | {Optimization}     |
| Favicons  | `{path}`                | {ICO/PNG/SVG}      |                    |

### 8.7 Animations & Transitions

**Transition Defaults**:

| Property     | Duration | Easing                      | Usage               |
| ------------ | -------- | --------------------------- | ------------------- |
| All          | {150ms}  | `{ease-in-out}`             | General transitions |
| Transform    | {200ms}  | `{cubic-bezier(...)}`       | Scale, rotate       |
| Opacity      | {150ms}  | `{ease-out}`                | Fade effects        |
| Colors       | {100ms}  | `{ease}`                    | Hover states        |

**Animation Patterns**:

| Animation     | Duration | Description                          |
| ------------- | -------- | ------------------------------------ |
| fadeIn        | {200ms}  | Opacity 0 → 1                        |
| slideUp       | {300ms}  | Translate Y with fade                |
| scaleIn       | {150ms}  | Scale from 0.95 to 1                 |
| {custom}      | {time}   | {description}                        |

### 8.8 Theming (Light/Dark Mode)

**Implementation**: {CSS variables / Tailwind dark: / Theme provider}

**Light Theme**:
```css
/* Key light theme values */
--background: {value};
--foreground: {value};
--card: {value};
/* etc. */
```

**Dark Theme**:
```css
/* Key dark theme values */
--background: {value};
--foreground: {value};
--card: {value};
/* etc. */
```

**Theme Toggle**: `{Location and method of theme switching}`

---

## 9. User Experience (UX) Design

This section documents interaction patterns, user flows, and experience considerations.

### 9.1 Navigation Patterns

**Primary Navigation**:

| Element        | Type                    | Location         | Behavior                    |
| -------------- | ----------------------- | ---------------- | --------------------------- |
| Main Nav       | {Top bar / Sidebar}     | `{component}`    | {Sticky / Fixed / Static}   |
| Mobile Nav     | {Hamburger / Bottom}    | `{component}`    | {Slide-in / Overlay}        |
| Breadcrumbs    | {Yes/No}                | `{component}`    | {Auto-generated / Manual}   |

**Navigation Structure**:

```
├── Home
├── {Section 1}
│   ├── {Subsection}
│   └── {Subsection}
├── {Section 2}
└── {Settings / Profile}
```

### 9.2 User Flows

**Primary User Journey**:

```
{Start} → {Step 1} → {Step 2} → {Step 3} → {Goal}
   │
   └──[Alternative path]──→ {Alternative outcome}
```

**Key Flows Documented**:

| Flow Name        | Entry Point     | Steps | Success Criteria            |
| ---------------- | --------------- | ----- | --------------------------- |
| {Onboarding}     | {Landing page}  | {N}   | {User completes setup}      |
| {Core Action}    | {Dashboard}     | {N}   | {Action completed}          |
| {Authentication} | {Login page}    | {N}   | {User authenticated}        |

### 9.3 Interaction Patterns

**Loading States**:

| Context          | Pattern                  | Implementation        |
| ---------------- | ------------------------ | --------------------- |
| Page Load        | {Skeleton / Spinner}     | `{component}`         |
| Button Action    | {Spinner / Disabled}     | {Inline / Replace}    |
| Data Fetch       | {Skeleton / Placeholder} | `{component}`         |

**Empty States**:

| Context          | Content                         | Action Provided       |
| ---------------- | ------------------------------- | --------------------- |
| No Data          | {Illustration + message}        | {CTA to create}       |
| Search No Result | {Message + suggestions}         | {Clear / Modify}      |
| Error            | {Error message}                 | {Retry / Contact}     |

**Feedback Patterns**:

| Action Type      | Feedback Method               | Duration / Behavior   |
| ---------------- | ----------------------------- | --------------------- |
| Success          | {Toast / Inline message}      | {3s auto-dismiss}     |
| Error            | {Toast / Modal / Inline}      | {Persistent / 5s}     |
| Warning          | {Toast / Confirmation modal}  | {User dismisses}      |
| Progress         | {Progress bar / Spinner}      | {Until complete}      |

### 9.4 Responsive Behavior

**Breakpoints**:

| Name   | Width     | Target Device     | Layout Changes                         |
| ------ | --------- | ----------------- | -------------------------------------- |
| sm     | {640px}   | Mobile            | {Single column, stacked nav}           |
| md     | {768px}   | Tablet            | {2-column where appropriate}           |
| lg     | {1024px}  | Desktop           | {Full layout, sidebar visible}         |
| xl     | {1280px}  | Large Desktop     | {Max-width container, wider spacing}   |
| 2xl    | {1536px}  | Extra Large       | {Optional wider content}               |

**Approach**: {Mobile-first / Desktop-first}

**Responsive Patterns**:

| Component    | Mobile                | Tablet              | Desktop              |
| ------------ | --------------------- | ------------------- | -------------------- |
| Navigation   | {Hamburger menu}      | {Collapsed sidebar} | {Full sidebar}       |
| Grid         | {1 column}            | {2 columns}         | {3-4 columns}        |
| Tables       | {Card view / Scroll}  | {Horizontal scroll} | {Full table}         |

### 9.5 Accessibility

**Compliance Target**: {WCAG 2.1 AA / AAA}

**Implemented Features**:

| Feature                | Status | Implementation Notes                  |
| ---------------------- | ------ | ------------------------------------- |
| Semantic HTML          | {✓/○}  | {Details}                             |
| ARIA Labels            | {✓/○}  | `{aria-label, aria-describedby}`      |
| Keyboard Navigation    | {✓/○}  | {Tab order, focus management}         |
| Focus Indicators       | {✓/○}  | `{outline / ring styles}`             |
| Screen Reader Support  | {✓/○}  | {Tested with: VoiceOver, NVDA, etc.}  |
| Color Contrast         | {✓/○}  | {Ratio: 4.5:1 minimum}                |
| Reduced Motion         | {✓/○}  | `{prefers-reduced-motion support}`    |
| Alt Text               | {✓/○}  | {All images have descriptive alt}     |

**Skip Links**: `{Yes/No - location}`

**Focus Management**: `{How focus is managed during navigation, modals, etc.}`

### 9.6 Error Handling UX

**Error Display Patterns**:

| Error Type       | Display Method          | User Actions Available      |
| ---------------- | ----------------------- | --------------------------- |
| Form Validation  | {Inline below field}    | {Correct and resubmit}      |
| API Error        | {Toast / Error page}    | {Retry / Go back}           |
| 404 Not Found    | {Custom 404 page}       | {Go home / Search}          |
| 500 Server Error | {Error page}            | {Retry / Contact support}   |
| Network Error    | {Inline / Toast}        | {Retry when online}         |

### 9.7 Multimedia Components

**Audio/Video**:

| Type    | Implementation           | Controls                    | Location        |
| ------- | ------------------------ | --------------------------- | --------------- |
| Video   | {Native / YouTube / etc} | {Custom / Native controls}  | `{path}`        |
| Audio   | {Native / Custom player} | {Play/pause, volume, etc.}  | `{path}`        |

**Other Media**:

| Component   | Purpose              | Implementation          |
| ----------- | -------------------- | ----------------------- |
| Image Zoom  | {Product images}     | {Library used}          |
| Carousel    | {Image galleries}    | {Library / Custom}      |
| Maps        | {Location display}   | {Google Maps / Mapbox}  |

---

## 10. Development Guidelines

### 10.1 Coding Conventions

**Style Configuration**: `{.eslintrc / .prettierrc / etc.}`

**Naming Conventions**:

- Files: `{kebab-case / PascalCase / etc.}`
- Functions: `{camelCase / snake_case}`
- Components: `{PascalCase}`
- Constants: `{SCREAMING_SNAKE_CASE}`

**Import Order**:

1. External libraries
2. Internal modules
3. Components
4. Utils/helpers
5. Types
6. Styles

### 10.2 Patterns & Best Practices

**Error Handling**:

```{language}
// Example error handling pattern
```

**State Management**:

```{language}
// Example state pattern
```

### 10.3 Environment Setup

**Prerequisites**:

- {Tool} >= {version}
- {Tool} >= {version}

**Installation**:

```bash
# Clone and install
git clone {repo}
cd {project}
{install command}
```

**Environment Variables**:

| Variable       | Purpose   | Required |
| -------------- | --------- | -------- |
| `{VAR_NAME}`   | {Purpose} | Yes/No   |

**Development Commands**:

```bash
{dev start command}    # Start dev server
{test command}         # Run tests
{build command}        # Build for production
```

---

## 11. Testing Strategy

| Type        | Framework                 | Location   | Command     |
| ----------- | ------------------------- | ---------- | ----------- |
| Unit        | {Jest/Pytest/etc.}        | `{path}`   | `{command}` |
| Integration | {Framework}               | `{path}`   | `{command}` |
| E2E         | {Playwright/Cypress/etc.} | `{path}`   | `{command}` |

**Coverage**: {X}% (as of {date})

---

## 12. Deployment & Operations

### 12.1 Build Process

```bash
# Production build
{build command}

# Output location
{output path}
```

### 12.2 Deployment

**Target**: {Platform}

**Process**:

1. {Step 1}
2. {Step 2}
3. {Step 3}

**Rollback**:

```bash
{rollback command or procedure}
```

### 12.3 Monitoring

| Aspect  | Tool          | Configuration |
| ------- | ------------- | ------------- |
| Logging | {Tool}        | `{path}`      |
| Errors  | {Sentry/etc.} | `{path}`      |
| Metrics | {Tool}        | `{path}`      |

---

## 13. Security Considerations

| Area             | Implementation         |
| ---------------- | ---------------------- |
| Authentication   | {Method and location}  |
| Authorization    | {RBAC/ABAC/etc.}       |
| Data Encryption  | {At rest / In transit} |
| Input Validation | {Library/method}       |
| Rate Limiting    | {Yes/No — details}     |
| CORS             | {Configuration}        |
| CSP              | {Yes/No}               |

---

## 14. Dependencies & Third-Party Services

### Critical Dependencies

| Package   | Version   | Purpose   |
| --------- | --------- | --------- |
| {package} | {version} | {purpose} |

### External Services

| Service   | Purpose   | Configuration         |
| --------- | --------- | --------------------- |
| {Service} | {Purpose} | `{env var or config}` |

---

## 15. Known Issues & Technical Debt

### Open Issues

- [ ] {Issue description} — `{location}`

### TODOs in Code

- [ ] `{file}:{line}` — {TODO text}

### Technical Debt

| Item   | Priority     | Notes   |
| ------ | ------------ | ------- |
| {Item} | High/Med/Low | {Notes} |

---

## 16. RFD Summary

*All RFDs found in checkpoint documentation:*

| RFD # | Feature   | Status                        | Checkpoint     | File                                   |
| ----- | --------- | ----------------------------- | -------------- | -------------------------------------- |
| 1     | {name}    | Completed/In Progress/Planned | checkpoint-{N} | `rfd/{N}-{name}/rfd-{date}-{time}.md`  |
| ...   | ...       | ...                           | ...            | ...                                    |

---

## 17. References Summary

*All reference documents found in `.claude/references/`:*

| Category        | Document        | Description                             | Path                                        |
| --------------- | --------------- | --------------------------------------- | ------------------------------------------- |
| {folder-name}   | {document-name} | {brief description of what it contains} | `.claude/references/{folder}/{file}.md`     |
| ...             | ...             | ...                                     | ...                                         |

*These references provide context for development but are not directly part of the codebase. New developers should review relevant references before contributing.*

---

## 18. Glossary

| Term           | Definition                                                      |
| -------------- | --------------------------------------------------------------- |
| {Term}         | {Definition}                                                    |
| **PRD**        | Product Requirements Document                                   |
| **RFD**        | Request for Development - feature request and progress document |
| **Checkpoint** | A point-in-time snapshot of project state and documentation     |
| **Reference**  | Supporting documentation not directly part of development       |

---

## 19. Quick Reference

### Common Commands

```bash
# Development
{dev command}

# Testing
{test command}

# Building
{build command}

# Deployment
{deploy command}
```

### Important Files

| File     | Purpose   |
| -------- | --------- |
| `{path}` | {Purpose} |

### Key Contacts/Resources

- **Repository**: {URL}
- **Documentation**: {URL}
- **Issue Tracker**: {URL}

### Checkpoint History

| Checkpoint     | Date   | Type     | Description                    |
| -------------- | ------ | -------- | ------------------------------ |
| checkpoint-0   | {date} | PRD      | Initial requirements           |
| checkpoint-1   | {date} | Snapshot | {Brief description}            |
| checkpoint-{N} | {date} | Snapshot | {Brief description - this one} |

---

*This snapshot was automatically generated on {DATE} for checkpoint-{N}. For the most current information, always refer to the source code and official documentation.*