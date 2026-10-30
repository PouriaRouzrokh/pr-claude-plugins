---
name: create-prd
description: "Generates a Product Requirements Document through an interactive interview and current web research, then saves it to .claude/checkpoints/checkpoint-0/prd.md. Works from notes, an ideas file, or an existing codebase. Covers problem, users, success metrics, MVP scope, architecture, verified stack versions, design, security, risks, and open questions, with a variant for ML and data projects. Use when starting a new project, web app, codebase, ML pipeline, or other initiative, or when an existing project needs a PRD."
argument-hint: "[optional: path/to/ideas.md or free-text description]"
allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/shared/checkpoint.py *)
---

# Create PRD

Produce a PRD that the rest of the toolkit can build from: `mvp-dev` turns its MVP features into RFDs, and every later session reads it for the project's intent. This is ATLAS's Architect step (see `atlas-development`): a clear problem, a specific user, a measurable definition of success, and the constraints, plus the start of Trace (data, integrations, stack, risks).

**Input**: $ARGUMENTS (a file path, a description, or nothing)

Not every task needs a PRD. For a single feature use `/pr:feature-dev`; for a bug, `systematic-debugging`.

## Phase 0: Gather Input

1. If a file or description was given, read it and extract the concept, users, feature ideas, technical preferences, and constraints.
2. If the project already has code, explore it first (directly, or with a `pr:code-explorer` agent for a large codebase) so the PRD describes the real starting point and the interview only asks what the code cannot answer.
3. Run `python3 ${CLAUDE_PLUGIN_ROOT}/shared/checkpoint.py status`. If `checkpoint-0/prd.md` already exists, ask whether to revise it or replace it; do not overwrite it silently.

## Phase 1: Interview

Ask what you cannot infer, one stage at a time. Use `AskUserQuestion` for choices (up to four questions per call, each with concrete options and your recommended option first), and plain questions for open-ended answers. When the user is unsure, research and recommend rather than pressing them. "Use your judgment" is a valid answer: decide, and record the decision as an assumption.

1. **Vision**: the problem in one sentence, who has it, the single most important outcome.
2. **Scope**: what must be in the first version, what is explicitly out, what comes later.
3. **Technical direction**: preferred or required stack, systems to integrate, where it will run, existing accounts and services.
4. **Design and experience** (when there is a UI): audience, tone, references the user likes or dislikes, accessibility needs.
5. **Constraints**: timeline, budget (including API and compute costs), team, compliance (HIPAA, GDPR, ...).

For ML and data projects, replace stage 4 with: the decision the model supports, the evaluation metric and threshold, the baseline, data sources and labeling, splits, compute budget, and how predictions will be consumed.

Stop when the critical sections have enough information or the user signals they have shared everything.

## Phase 2: Research

Research while interviewing whenever the user mentions something you should verify, and do a focused pass before proposing the stack. Use today's date in searches, and confirm versions and APIs with Context7 (when available) or official docs rather than memory.

- **Stack**: current stable versions, recommended stacks for this kind of project, head-to-head comparisons where the choice is open.
- **Integrations**: official API docs, auth setup, rate limits, pricing.
- **Security and compliance** (when relevant): requirements checklists for the regulation or domain.
- **Prior art**: existing products or open-source projects solving the same problem.

For broad research, launch 2–3 subagents in parallel (stack, integrations and compliance, prior art) and synthesize their findings. Cite sources in the PRD.

## Phase 3: Propose and Confirm

Present the key decisions with their rationale and trade-offs: MVP scope, stack with versions, architecture outline, major risks. Get the user's confirmation, and record anything they want to defer as an open question.

## Phase 4: Write the PRD

1. If `.claude/checkpoints/checkpoint-0/` does not exist, run `checkpoint.py init`.
2. Fill the template at `${CLAUDE_SKILL_DIR}/references/prd-template.md` section by section. Give every MVP feature acceptance criteria and a priority; diagram the architecture; list research sources with the versions verified. For ML projects, cover data, evaluation, baselines, and experiment tracking in the architecture and features sections.
3. Use `writing-clearly-and-concisely` for the prose sections.
4. Save to `.claude/checkpoints/checkpoint-0/prd.md` (writing under `.claude/` may prompt for permission).

## Quality Check

- [ ] Problem, user, and a measurable success metric are explicit
- [ ] MVP features are separated from later features, each with acceptance criteria
- [ ] Stack versions were verified during this session, with sources
- [ ] Integrations list auth, limits, and costs, with links to docs
- [ ] Security and compliance needs are addressed (or marked not applicable)
- [ ] Risks have mitigations; open questions and assumptions are listed

## Report

Give the PRD path, the key decisions, notable research findings, and the open questions. Suggest next steps: `/pr:handle-claude-md` (if the project has no CLAUDE.md) and `/pr:mvp-dev`.
