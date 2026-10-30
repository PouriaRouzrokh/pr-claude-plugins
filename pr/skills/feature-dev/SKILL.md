---
name: feature-dev
description: "Guided feature development for an existing codebase: loads project context from .claude/checkpoints, explores the code with agents, asks clarifying questions, designs and gets the architecture approved, implements, verifies with evidence, reviews with Claude Code's /code-review and /simplify, and records everything in an RFD. Use when the user wants to build or substantially change a feature."
argument-hint: "[feature description] [--subagents | --team]"
allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/shared/checkpoint.py *)
---

# Feature Development

Build one feature from request to reviewed, documented code. The RFD written along the way is the project's memory of this work: future sessions read it instead of re-exploring the code, so keep it specific and current.

**Request**: $ARGUMENTS

Project documentation conventions (checkpoints, RFD numbering, the template, permissions) are in `${CLAUDE_PLUGIN_ROOT}/shared/checkpoint-system.md`. Read it once per session before creating or editing RFDs. The helper used below is `python3 ${CLAUDE_PLUGIN_ROOT}/shared/checkpoint.py`.

## Match Depth to the Task

| Task | Process |
|------|---------|
| New feature with integrations, schema changes, or architectural decisions | All phases, with parallel agents |
| Feature that follows existing patterns and touches a few files | All phases, but explore and design yourself instead of launching agents, and keep the RFD brief |
| Bug fix | Use the `systematic-debugging` skill. Create a bug-fix RFD only when the fix is non-trivial |
| One-line change | Make it, verify it, mention it in the summary |

This mirrors ATLAS (see `atlas-development`): trace before linking, link before assembling, stress-test before handing off.

## Agents

Explorer, architect, and reviewer agents keep large reads out of the main conversation and give independent perspectives. Launch them only when the task is big enough to benefit; for small changes, reading the files yourself is faster and cheaper. This plugin's agents are `pr:code-explorer`, `pr:code-architect`, and `pr:code-reviewer`; use the full names, since other plugins ship agents with the same short names.

- **Default**: subagents. They work independently and report back; you synthesize. If a report leaves a gap, continue that agent with `SendMessage` instead of launching a new one: it keeps its context.
- **`--subagents`**: always subagents.
- **`--team`**: an agent team, whose members message each other. Teams are experimental, need `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, work only in interactive sessions, and cost several times more. For architects debating trade-offs, a cheaper option usually works: launch them as named subagents and have them challenge each other with `SendMessage`, which does not need teams. If the task is small, say so and confirm before using a team.

## Phase 1: Load Context

1. Run `checkpoint.py status` to see checkpoints, the PRD, the latest snapshot, and every RFD with its status.
2. Read the PRD (if any) and the latest snapshot. Read RFDs whose titles relate to this request.
3. Decide whether this work **updates an existing RFD** (it refines or extends tracked work) or needs **a new one**. Ask if unclear.
4. If the request itself is unclear, ask what problem it solves and what the feature should do before exploring.

## Phase 2: Explore the Code

For a full-depth task, launch 2–3 `pr:code-explorer` agents in parallel, each with a different focus: similar features and how they are built; the architecture and abstractions this feature will touch; UI patterns, tests, or extension points. Ask each to return the 5–10 files most essential to its topic.

Read the files they return, then summarize the relevant patterns, conventions, and constraints in a few bullets.

## Phase 3: Clarify

Before designing, resolve what the request leaves open: edge cases, error handling, permissions, integration points, scope boundaries, backward compatibility, performance expectations. Ask all questions at once, using `AskUserQuestion` for discrete choices. Wait for answers; designing on guesses produces rework.

If the user says "use your judgment", state your recommendations and get a quick confirmation.

## Phase 4: Open the RFD

Create it with `checkpoint.py new-rfd "<feature title>"` (or open the existing RFD). Fill **Request** (the original request verbatim, clarified requirements, acceptance criteria as checkboxes, out of scope) and **Context** (related features and RFDs, key files, constraints). Set status to Planning.

If this session is in plan mode, `.claude/` writes are blocked: keep the RFD content in your plan and write the file after approval.

## Phase 5: Design and Approve

For a full-depth task, launch 2–3 `pr:code-architect` agents with different briefs: smallest change that works; cleanest long-term design; pragmatic balance. To have them challenge each other before reporting, name them and ask each to critique the others' proposals with `SendMessage` (or, with `--team`, run them as a team).

Then present to the user:
- each approach in two or three sentences, with its trade-offs and the files it touches
- your recommendation and why
- the implementation checklist for the recommended approach

Ask for a decision with `AskUserQuestion` (approve / choose another option / revise). If the session is in plan mode, present the plan with `ExitPlanMode` instead; approval switches the session out of plan mode.

Record the chosen approach, the alternatives with why they lost, and the checklist in the RFD. Set status to In Progress.

## Phase 6: Implement

Start only after approval.

- Follow the codebase's conventions over your own preferences.
- Use the `test-driven-development` skill for logic: write the failing test, then the code.
- Track progress against the RFD checklist (use the session's task tools as well if it has them). Add a Progress Log entry at each milestone so an interrupted session can resume.
- If library behavior matters, check current documentation (Context7 MCP if available) rather than memory.

**Parallel implementation** pays off only when the work splits into units that own separate files. Launch one agent per unit with `isolation: "worktree"`, ask each to commit its work on its worktree branch, then merge the branches yourself and run the full test suite. Worktrees branch from the remote default branch unless the project sets `"worktree": {"baseRef": "head"}` in its settings, and they contain only tracked files, so an agent would otherwise miss your uncommitted and unpushed work. Before launching, commit the work so far (including the RFD), confirm `baseRef` is `head` (ask before changing settings), and tell each agent to install dependencies first. Gitignored files such as `.env` reach a worktree only through a `.worktreeinclude` file at the project root. For large mechanical changes across many files, suggest Claude Code's `/batch` instead. Otherwise implement sequentially; coordination costs more than it saves on small features.

## Phase 7: Verify

Prove the feature works before asking the user to look at it.

- Run the project's full test suite and the new tests. Report the actual results.
- Exercise the behavior directly: call the endpoints, run the functions, query the data.
- For UI, use Playwright or the session's browser tools: check the main flow, error and empty states, keyboard focus, and both mobile and desktop widths. For a substantial UI change, offer `web-quality-audit`.
- Apply the verification gate from `test-driven-development`: claim only what fresh command output shows.
- Remove temporary artifacts (scratch scripts, debug logging, temporary routes, test data). Keep real tests.

Record what you tested and the results in the RFD.

## Phase 8: Review and Professionalize

1. **Quality**: run `/simplify` on the changed code. It applies reuse, simplification, and efficiency fixes directly, so re-run the tests afterwards. Running it first means the bug review sees the final code.
2. **Bugs**: run `/code-review high` (type the level: without one, it reuses whatever level the user typed last). The review runs as a background agent, so wait for its findings before editing the files it covers, then fix every confirmed finding and re-run the tests.
3. **Security**: if the feature touches authentication, authorization, payments, file uploads, or user data, also run `/security-review`. It compares against the `origin` remote's default branch, so when the repository has no `origin` remote, launch a `pr:code-reviewer` agent with a security brief instead.
4. If those built-ins are unavailable, launch three `pr:code-reviewer` agents instead (correctness, simplicity and duplication, project conventions) and fix what they report.
5. Read every file you created or modified once more as its future maintainer would: clear names, no dead code or leftover debugging, comments only where the reasoning is not obvious, no hard-coded values that belong in configuration, helpful error messages.

Present anything you chose not to fix and ask whether to fix it now or record it as a follow-up. Note review findings and resolutions in the RFD.

## Phase 9: Finish

1. Finalize the RFD: status Completed, acceptance criteria checked, every file created or modified with what changed and why, decisions, test evidence, follow-ups. Cross-check against `git status` and `git diff` so nothing is missing.
2. If the feature changed something the latest snapshot describes (architecture, stack, data model, major flows), say so and suggest `/pr:create-snapshot`.
3. Summarize for the user: what was built, key decisions, files changed, how it was verified, the RFD path, and suggested next steps (usually `/pr:commit-push`).
