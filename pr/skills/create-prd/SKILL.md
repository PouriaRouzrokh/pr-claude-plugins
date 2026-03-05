---
name: create-prd
description: Generate comprehensive Product Requirements Document (PRD) through interactive discovery and research. Interviews the user, conducts web research for best practices and current tech specs, and produces a professional PRD. Use when starting a new project, web app, codebase, ML pipeline, or any development initiative.
argument-hint: "[optional: path/to/ideas.md or free-text description]"
---

# Product Requirements Document Generator

Generate a PRD through interactive discovery, web research, and synthesis. Interview users, research best practices, then produce a professional requirements document.

## ATLAS Foundation

This skill implements the **Architect** phase of ATLAS development.

**When to create a PRD:**
- Starting a new project, application, or MVP
- Major new product initiatives
- Projects requiring stakeholder alignment

**When NOT to create a PRD:**
- Single feature additions (use `/pr:feature-dev` with RFD)
- Bug fixes or small changes
- Extending existing functionality

A PRD answers the core questions that prevent building failures:

1. **What problem does this solve?** — One sentence. If you can't say it simply, you don't understand it.
2. **Who is this for?** — Be specific, not "everyone."
3. **What does success look like?** — Measurable outcomes, not vague goals.
4. **What are the constraints?** — Budget, time, technical requirements.

The PRD also begins the **Trace** phase by documenting:
- Data schema requirements
- Integration dependencies
- Technology stack decisions
- Edge cases and risks

For complete ATLAS framework details, see `atlas-development` skill.

## Multi-Agent Strategy

PRD creation is primarily an interactive interview process, so multi-agent approaches apply mainly to the research phase (Phase 2).

**When to use subagents**: During deep research, dispatch subagents to research different domains in parallel — one for tech stack analysis, one for security/compliance, one for competitive landscape. Each returns findings independently. This is the default and sufficient approach.

**When agent teams could help**: For PRDs covering very complex domains with many interacting technology choices (e.g., a full-stack application with multiple external integrations, compliance requirements, and competing architectural approaches). In this case, research agents could challenge each other's technology recommendations and surface conflicts. In practice, PRD research tasks are independent enough that subagents work well.

If the calling command passes `--team`, respect that flag. Otherwise, default to subagents for research phases.

---

## Core Principles

- **Interview first**: Focused questions, one topic at a time.
- **Research while interviewing**: Search for context when user mentions something.
- **Accept uncertainty**: "Use your judgment" is valid.
- **Synthesize**: Provide recommendations, not just search results.
- **Measurable success**: Every PRD must define what success looks like in concrete terms.

---

## Phase 0: Input Processing

**Goal**: Process any provided input

**Arguments**: $ARGUMENTS

**Actions**:

1. **If arguments provided**, read and analyze:
   - Markdown files with rough ideas
   - Text descriptions
   - Search results or research
   - Reference documents
   - Existing specifications

2. Extract key information:
   - Core concept and purpose
   - Target users (if mentioned)
   - Feature ideas
   - Technical preferences
   - Constraints or requirements

3. **If no arguments**, proceed directly to discovery interview

---

## Phase 1: Discovery Interview

**Goal**: Understand what the user wants to build

### Interview Philosophy

- Focused questions, one topic at a time
- Don't overwhelm with multiple questions
- Offer suggestions when user seems uncertain
- Accept "use your judgment" as valid
- Research while interviewing—search for context

### Interview Stages

**Stage 1: Core Vision**
- What problem does this solve?
- Who is this for? (may be N/A for some projects)
- What's the single most important outcome?

*Research: Search for existing solutions, market landscape, user demographics*

**Stage 2: Scope Definition**
- What must be in the first version (MVP)?
- What's explicitly out of scope for now?
- What might be added later?

*Research: Search for MVP best practices in the domain, feature prioritization frameworks*

**Stage 3: Technical Direction**
- Any technology preferences or constraints?
- Existing systems to integrate with?
- Deployment environment preferences?

*Research: Verify latest versions, search for recommended tech stacks, compatibility issues*

**Stage 4: Design & Experience** (if applicable)
- Visual style preferences?
- Key UX principles?
- Accessibility requirements?

*Research: Search for UX patterns in the domain, accessibility standards, design system options*

**Stage 5: Constraints & Context**
- Timeline expectations?
- Team size/composition?
- Budget considerations?
- Regulatory or compliance needs?

*Research: Search for compliance requirements, industry regulations if applicable*

### When to Stop Interviewing

Stop when: user says "use your judgment", indicates they've shared everything, critical sections have enough information, or continuing adds no value.

---

## Phase 2: Deep Research

**Goal**: Research technology choices and best practices

**Actions**:

1. **Technology Stack Research**:
```
Search: "recommended tech stack [project type] 2024"
Search: "[framework] latest stable version"
Search: "[framework A] vs [framework B] for [use case]"
```

2. **Integration Research** (when applicable):
```
Search: "[service] API documentation"
Search: "[service] [framework] integration guide"
Search: "[service] authentication oauth setup"
Search: "[service] rate limits pricing"
```

3. **Security & Compliance Research** (when relevant):
```
Search: "[compliance standard] requirements checklist"
Search: "[industry] data protection requirements"
Search: "authentication best practices [year]"
Search: "[framework] security best practices"
```

---

## Phase 3: Propose and Confirm

**Goal**: Share research findings and confirm decisions

**Actions**:

1. Present technology recommendations with rationale
2. Explain trade-offs discovered in research
3. Get user confirmation on major decisions
4. Document any decisions user wants to defer

---

## Phase 4: Generate PRD

**Goal**: Create comprehensive PRD document

**Output Location**: `{project_root}/.claude/checkpoints/checkpoint-0/prd.md`

Create directory if needed:
```bash
mkdir -p {project_root}/.claude/checkpoints/checkpoint-0
```

**PRD Structure** (see embedded template below):

1. **Executive Summary** - Project essence in one paragraph
2. **Problem Statement** - The problem, current alternatives, opportunity
3. **Target Users** - Primary/secondary users, user needs
4. **Product Vision** - Mission, core principles, success metrics
5. **Features & Requirements** - MVP features, future features, out of scope
6. **System Architecture** - High-level overview, tech stack, data model, API design
7. **Design Guidelines** - UX principles, visual design, theming, accessibility
8. **Security & Compliance** - Auth, data protection, compliance requirements
9. **Development Phases** - Foundation, enhancement, scale phases
10. **Risks & Mitigations** - Identified risks and strategies
11. **Research References** - Sources consulted, version information
12. **Open Questions** - Items needing resolution
13. **Appendix** - Glossary, revision history

---

## Phase 5: Save and Report

**Goal**: Write file and confirm completion

**Actions**:

1. Write PRD to `.claude/checkpoints/checkpoint-0/prd.md`

2. Report completion with:
   - File path
   - Key decisions made
   - Research findings summary
   - Open questions that need resolution

---

## PRD Template

Use the template at `references/prd-template.md`. Copy and fill in each section based on discovery and research findings.

Apply the `writing-clearly-and-concisely` skill when drafting prose sections (Executive Summary, Problem Statement, etc.) to ensure clear, direct writing.

---

## Interview Tips

**When user is uncertain:**
> "For [topic], let me search for current best practices... Based on my research, [finding]. Does that approach work for you?"

**When user wants to defer:**
> "I'll research this and use the current best practices for [topic]. You can always refine this later."

**When scope is creeping:**
> "That's a great idea. Should we include it in the MVP, or save it for a future version?"

**When proposing technologies:**
> "Based on my research, [framework] v[X.Y.Z] is the current stable version and is well-suited for [reason]. Would you like me to explore alternatives?"

---

## Quality Checklist

Before finalizing, verify:
- [ ] MVP features are clearly distinguished from future features
- [ ] Each MVP feature has acceptance criteria
- [ ] Tech stack is specified with current versions verified via search
- [ ] Best practices from research are incorporated
- [ ] System architecture is diagrammed
- [ ] Design guidelines are actionable
- [ ] Security/compliance requirements are researched (if applicable)
- [ ] Integration requirements are documented with links to docs
- [ ] Open questions are documented
- [ ] Research sources are referenced
