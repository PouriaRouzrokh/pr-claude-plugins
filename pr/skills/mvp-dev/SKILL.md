---
name: mvp-dev
description: "Builds an MVP from the PRD at .claude/checkpoints/checkpoint-0/prd.md: extracts and orders the features, designs and validates the foundation (architecture RFD, Link checks), then implements one feature at a time, each with its own RFD, tests, review, and user sign-off. Resumes from existing RFDs. Use when the user wants to implement or continue an MVP from a PRD."
argument-hint: "[optional: focus or priority features] [--subagents | --team]"
allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/shared/checkpoint.py *)
---

# MVP Development

Turn the PRD into a working MVP, one approved feature at a time. Each feature gets an RFD that records its plan, decisions, tests, and files, so development can pause and resume across sessions without losing context.

**Focus**: $ARGUMENTS

Project documentation conventions are in `${CLAUDE_PLUGIN_ROOT}/shared/checkpoint-system.md`; read it once per session. The helper used below is `python3 ${CLAUDE_PLUGIN_ROOT}/shared/checkpoint.py`. MVP RFDs live in checkpoint-0: RFD-0 is the architecture, features are 1, 2, 3...

This skill applies the full ATLAS framework (see `atlas-development`). For a single feature in an existing product, use `feature-dev` instead.

## Agents

This plugin's agents are `pr:code-explorer`, `pr:code-architect`, and `pr:code-reviewer`; use the full names, since other plugins ship agents with the same short names.

- **Default**: subagents for exploration, architecture proposals, and review. To have architects or reviewers challenge each other, name them and let them exchange critiques with `SendMessage`; that does not need agent teams.
- **`--subagents`**: always subagents.
- **`--team`**: an agent team, most useful in Phase 2 (architects negotiating shared schema and APIs) and Phase 5 (reviewers cross-checking integration). Experimental; needs `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, works only interactively, and costs several times more. For a small MVP, say so and confirm first.

## Phase 0: Load the PRD and Progress

1. Run `checkpoint.py status`.
2. If there is no `checkpoint-0/prd.md`, stop and offer `/pr:create-prd`; the PRD is the source of truth for scope.
3. Read the PRD: vision, users, MVP features (P0/must-have), stack, design direction, success metrics, constraints, out-of-scope items.
4. **Resuming?** If checkpoint-0 already has RFDs, read them. Completed features are done; an In Progress RFD is where to pick up. Tell the user where things stand and confirm before continuing with Phase 4 for the next feature.
5. Note whether code already exists (PRD for an existing project) or this is greenfield.

## Phase 1: Plan the Features

Extract the MVP features and propose an order:

| # | Feature | Priority | Depends on | Complexity |
|---|---------|----------|------------|------------|

Order by dependencies first, then foundational before advanced, then user value. Present the list and ask the user to confirm or adjust the order and scope.

## Phase 2: Design the Architecture

1. If code exists, launch 2 `pr:code-explorer` agents to map its structure and conventions.
2. Launch 2 `pr:code-architect` agents: one for the **foundation** (project structure, stack, shared components, database schema, API conventions, auth), one for the **feature map** (how features share code, integration points, build sequence).
3. Synthesize one recommendation and present it with its main trade-offs. Ask for approval with `AskUserQuestion`; if the session is in plan mode, use `ExitPlanMode` and write the RFD afterwards.
4. Create the architecture RFD: `checkpoint.py new-rfd "MVP architecture" --checkpoint 0 --number 0 --type Architecture`, and record the design, schema, integrations, and rejected alternatives.

## Phase 3: Foundation and Link Validation

1. Set up or adapt the foundation: project scaffolding with current tooling (check versions with Context7 or official docs), directory structure, linting, formatting, test runner, configuration, and the database schema.
2. **Validate every connection before building features** (ATLAS Link). Problems found now cost minutes; found mid-feature they cost hours.
   - [ ] Database connects and a trivial query succeeds
   - [ ] Each external API key works with a real test request
   - [ ] Auth/OAuth flow completes end to end (if applicable)
   - [ ] MCP servers or third-party SDKs respond
   - [ ] Environment variables load in every runtime (dev server, tests, scripts)
   - [ ] Rate limits and quotas are known
3. Report the results, fix failures before continuing, and record them in RFD-0.
4. Suggest committing the foundation (`/pr:commit-push`).

## Phase 4: Feature Loop

Build features one at a time. Each ends with the user's approval and a commit, which keeps every change reviewable and makes pausing safe.

### 4.1 Open the feature RFD

Announce "Starting feature N: name", re-read its PRD section, and run `checkpoint.py new-rfd "<feature name>"`. It lands in the latest checkpoint: checkpoint-0 for a greenfield MVP, or the current checkpoint when the project already has snapshots. Set **PRD Reference** to the PRD section, fill the request and acceptance criteria, and confirm the criteria with the user.

### 4.2 Explore (when code exists)

Launch 1–2 `pr:code-explorer` agents focused on patterns to follow, components to reuse, and integration points; read the files they return. Skip this for features that only extend code you just wrote.

### 4.3 Clarify

Ask about what the PRD leaves open for this feature: edge cases, errors, design details, integration specifics. Wait for answers and record them in the RFD.

### 4.4 Design and approve

Launch 1–2 `pr:code-architect` agents (or design it yourself for simple features) within the approved architecture. Present the approach, the files it touches, and the checklist; get approval (`AskUserQuestion`, or `ExitPlanMode` in plan mode). Record the plan and set the RFD to In Progress.

### 4.5 Implement

Follow the architecture and conventions, write tests first for logic (`test-driven-development`), track the RFD checklist (plus the session's task tools if available), and log milestones in the RFD.

If several upcoming features are truly independent (separate files, no shared schema changes) and the user wants speed, they can be built in parallel by agents launched with `isolation: "worktree"`, each committing on its own branch; merge them one at a time and run the full suite after each merge. Approval and user testing still happen per feature. Worktrees branch from the remote default branch unless the project sets `"worktree": {"baseRef": "head"}` in its settings, and they contain only tracked files. Before launching, commit the foundation and the feature RFDs, confirm `baseRef` is `head` (ask before changing settings), and tell each agent to install dependencies first; gitignored files such as `.env` reach a worktree only through a `.worktreeinclude` file at the project root.

### 4.6 Verify

- Run the full test suite and the new tests; report actual results.
- Exercise the feature: endpoints, functions, data, and for UI the browser at mobile and desktop widths (Playwright or the session's browser tools).
- Use `systematic-debugging` for any failure rather than guessing.
- Apply the verification gate: claim only what fresh output shows.
- Remove temporary scripts, debug output, and test data; keep real tests.

### 4.7 Review and professionalize

Run `/simplify` first and re-run the tests, so the bug review sees the final code. Then run `/code-review high` (type the level: without one, it reuses whatever level the user typed last); it runs as a background agent, so wait for its findings before editing, fix the confirmed ones, and re-run the tests. Run `/security-review` for auth, payments, uploads, or personal data; it needs an `origin` remote, so without one launch a `pr:code-reviewer` agent with a security brief instead. Without the built-ins, launch `pr:code-reviewer` agents for correctness, simplicity, and conventions. Finish by reading every changed file as its future maintainer would.

### 4.8 User acceptance

Present what was built, how to try it (URL, commands, test accounts), and screenshots for UI. Wait for the user to test. Address feedback, re-verify, and repeat until they approve. Record the feedback and changes in the RFD.

### 4.9 Complete

1. Finalize the RFD: Completed, criteria checked, every file changed with what and why (cross-check `git status`), decisions, test evidence, follow-ups.
2. Ask whether to commit (`/pr:commit-push`).
3. Offer to continue with the next feature or pause. On pause, summarize progress and note that running `/pr:mvp-dev` again resumes from the RFDs.

## Phase 5: Integration

After the last feature:

1. Review the whole MVP for how features interact. The features are committed by now, so give `/code-review` a range: `/code-review high <first-MVP-commit>..HEAD` (or launch `pr:code-reviewer` agents for integration, security, and performance; they can challenge each other through `SendMessage`, or as a team with `--team`). Add `/security-review`, or a security-focused `pr:code-reviewer` agent when there is no `origin` remote. Offer the user `/code-review ultra` as well, a deeper multi-agent review in the cloud (a few free runs on Pro and Max, then usage credits); run it only if they agree.
2. Make conventions consistent across features: naming, error handling, shared abstractions, duplicated helpers.
3. Run the full test suite; for web apps, run `web-quality-audit`.
4. Check the PRD's success metrics one by one and report which are met.

## Phase 6: Wrap Up

1. Confirm every MVP RFD is Completed and complete.
2. Present a summary: features with their RFD paths, key decisions, notable files, deviations from the PRD, and recommended post-MVP work.
3. Recommend `/pr:create-snapshot` to capture the MVP as checkpoint-1 (future feature RFDs then go there), and a final commit.
