---
name: update-docs
description: "Updates project documentation to match the current code: README, API docs, guides, and RFDs. Uses pr:code-explorer agents to find recent changes and documentation gaps, checks that every recent code change is recorded in an RFD, proposes a plan for approval, then applies it. Never edits snapshots, and edits the PRD or reference documents only with consent. Use when documentation has drifted from the code or after a batch of changes."
argument-hint: "[path] [what to document] [--subagents | --team]"
allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/shared/checkpoint.py *)
---

# Update Documentation

Bring the project's documentation back in line with the code. Documentation describes what exists, so every statement you write must be checkable against the code.

**Scope**: $ARGUMENTS. This may be a path, a description of what to document, both, or nothing (everything that changed). Ask if it is ambiguous.

Documentation conventions are in `${CLAUDE_PLUGIN_ROOT}/shared/checkpoint-system.md`; the helper is `python3 ${CLAUDE_PLUGIN_ROOT}/shared/checkpoint.py`. Use the `writing-clearly-and-concisely` skill for prose.

**Ownership**: CLAUDE.md belongs to `handle-claude-md`; docstrings and code comments belong to `clean-codebase`; snapshots are never edited (new ones come from `create-snapshot`).

## Agents

Subagents are the default; the two exploration tasks are independent. `--team` rarely helps here. For a narrow scope (one folder, one feature), explore yourself instead of launching agents.

## Phase 1: Inventory

1. List the documentation: README files, `docs/`, CHANGELOG, CONTRIBUTING, API specs (OpenAPI, GraphQL schemas), ADRs, and other Markdown in scope.
2. Run `checkpoint.py status` for the `.claude/` structure: checkpoints, PRD, snapshots, RFDs with status, and numbering problems. Report numbering problems to the user and ask before renumbering anything.
3. Find the baseline for "recent": the date of the latest snapshot, or the last commit that touched the docs (`git log -1 --format=%cs -- README.md docs/`).

## Phase 2: Explore

Launch two `pr:code-explorer` agents with the scope and the baseline date:

- **Changes**: read `git log --stat` since the baseline and the diffs that matter. Which features, modules, commands, configuration, and APIs were added, changed, or removed? Return the 5–10 files documentation should cover.
- **Gaps**: compare the code with the existing docs. Which documented things no longer exist or behave differently? Which significant things are undocumented? Which examples, commands, or setup steps are stale? Return specific documentation updates needed.

Read the key files they return.

## Phase 3: RFD Coverage

RFDs are the project's long-term memory, so every meaningful code change since the baseline should be traceable to one.

1. Map each change from Phase 2 to the RFD that covers it (by feature, files, and dates).
2. For changes that an RFD covers incompletely, plan updates: status, progress log, decisions, files changed.
3. For changes with no RFD at all, plan either an addition to the closest related RFD or a new retroactive RFD (`checkpoint.py new-rfd "<title>"`), and include that choice in the plan for the user.

## Phase 4: Plan and Approve

Present the plan: each file to update, the sections that change, content to add or remove, and the RFD updates from Phase 3. Ask for approval and adjust as requested. Ask separately before touching the PRD (only if requirements officially changed) or anything in `.claude/references/` (these often reflect team decisions).

## Phase 5: Apply

- **README**: accurate description, installation and setup that actually work (run the commands if practical), current usage examples, and only features that exist.
- **API documentation**: every endpoint or public function present with correct parameters, types, responses, and errors; remove removed APIs; refresh examples.
- **Guides and other docs**: fix stale steps, commands, screenshots references, and links.
- **RFDs**: apply the Phase 3 updates. Be thorough: specific files, functions, decisions with reasons, and what changed; a future session should not need to re-read the diff.

Keep the existing structure and voice unless the user asked for reorganization.

## Phase 6: Check

Verify that every command, path, link, and code sample you touched is correct (run commands and resolve links where possible), terminology is consistent, and nothing documents removed behavior. Then summarize: files updated, major changes, RFDs updated or created, items needing the user's attention, and suggested further documentation.

## Boundaries

- Do not commit or push.
- Do not create new documentation files beyond retroactive RFDs unless the user asks.
- Do not delete documentation files or restructure the docs without asking.
- Stay inside the scope when one was given.
- Document only what exists in the code.
