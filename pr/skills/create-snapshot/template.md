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

## 8. Design & UX

### 8.1 Design System

| Aspect             | Implementation                 |
| ------------------ | ------------------------------ |
| UI Framework       | {shadcn/ui, Material UI, etc.} |
| Component Location | `{path}`                       |
| Design Tokens      | `{path to theme/tokens}`       |

### 8.2 Theming

- **Dark Mode**: {Yes/No} — {Implementation details}
- **Theme Config**: `{path}`
- **CSS Variables**: {Yes/No}

### 8.3 Responsive Design

| Breakpoint | Width  | Target        |
| ---------- | ------ | ------------- |
| sm         | 640px  | Mobile        |
| md         | 768px  | Tablet        |
| lg         | 1024px | Desktop       |
| xl         | 1280px | Large Desktop |

**Approach**: {Mobile-first / Desktop-first}

### 8.4 Accessibility

- [ ] Semantic HTML
- [ ] ARIA labels
- [ ] Keyboard navigation
- [ ] Screen reader tested
- [ ] Color contrast compliant

---

## 9. Development Guidelines

### 9.1 Coding Conventions

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

### 9.2 Patterns & Best Practices

**Error Handling**:

```{language}
// Example error handling pattern
```

**State Management**:

```{language}
// Example state pattern
```

### 9.3 Environment Setup

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

## 10. Testing Strategy

| Type        | Framework                 | Location   | Command     |
| ----------- | ------------------------- | ---------- | ----------- |
| Unit        | {Jest/Pytest/etc.}        | `{path}`   | `{command}` |
| Integration | {Framework}               | `{path}`   | `{command}` |
| E2E         | {Playwright/Cypress/etc.} | `{path}`   | `{command}` |

**Coverage**: {X}% (as of {date})

---

## 11. Deployment & Operations

### 11.1 Build Process

```bash
# Production build
{build command}

# Output location
{output path}
```

### 11.2 Deployment

**Target**: {Platform}

**Process**:

1. {Step 1}
2. {Step 2}
3. {Step 3}

**Rollback**:

```bash
{rollback command or procedure}
```

### 11.3 Monitoring

| Aspect  | Tool          | Configuration |
| ------- | ------------- | ------------- |
| Logging | {Tool}        | `{path}`      |
| Errors  | {Sentry/etc.} | `{path}`      |
| Metrics | {Tool}        | `{path}`      |

---

## 12. Security Considerations

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

## 13. Dependencies & Third-Party Services

### Critical Dependencies

| Package   | Version   | Purpose   |
| --------- | --------- | --------- |
| {package} | {version} | {purpose} |

### External Services

| Service   | Purpose   | Configuration         |
| --------- | --------- | --------------------- |
| {Service} | {Purpose} | `{env var or config}` |

---

## 14. Known Issues & Technical Debt

### Open Issues

- [ ] {Issue description} — `{location}`

### TODOs in Code

- [ ] `{file}:{line}` — {TODO text}

### Technical Debt

| Item   | Priority     | Notes   |
| ------ | ------------ | ------- |
| {Item} | High/Med/Low | {Notes} |

---

## 15. RFD Summary

*All RFDs found in checkpoint documentation:*

| RFD # | Feature   | Status                        | Checkpoint     | File                                   |
| ----- | --------- | ----------------------------- | -------------- | -------------------------------------- |
| 1     | {name}    | Completed/In Progress/Planned | checkpoint-{N} | `rfd/{N}-{name}/rfd-{date}-{time}.md`  |
| ...   | ...       | ...                           | ...            | ...                                    |

---

## 16. References Summary

*All reference documents found in `.claude/references/`:*

| Category        | Document        | Description                             | Path                                        |
| --------------- | --------------- | --------------------------------------- | ------------------------------------------- |
| {folder-name}   | {document-name} | {brief description of what it contains} | `.claude/references/{folder}/{file}.md`     |
| ...             | ...             | ...                                     | ...                                         |

*These references provide context for development but are not directly part of the codebase. New developers should review relevant references before contributing.*

---

## 17. Glossary

| Term           | Definition                                                      |
| -------------- | --------------------------------------------------------------- |
| {Term}         | {Definition}                                                    |
| **PRD**        | Product Requirements Document                                   |
| **RFD**        | Request for Development - feature request and progress document |
| **Checkpoint** | A point-in-time snapshot of project state and documentation     |
| **Reference**  | Supporting documentation not directly part of development       |

---

## 18. Quick Reference

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