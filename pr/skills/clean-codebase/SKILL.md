---
name: clean-codebase
description: "Cleans and professionalizes code without changing behavior: records a test/lint/build baseline, finds dead code with project tooling (knip, ruff, vulture, tsc) and pr:code-reviewer agents, confirms the plan with the user, then removes dead code, fixes stale comments and docstrings, applies /simplify, formats, and proves nothing broke. Use when the user asks to clean up, tidy, de-cruft, or professionalize a codebase, folder, or file."
argument-hint: "[optional: path/to/scope] [--subagents | --team]"
---

# Clean Codebase

Make the code read as if a careful senior engineer wrote it, without changing what it does. Every removal must be justified by evidence, and the result must pass the same checks as before.

**Scope**: $ARGUMENTS (a file, a folder, or empty for the whole repository)

## Agents

Cleanup reviews split into independent dimensions, so subagents are the right default. Pass `--team` only if the user wants reviewers to cross-reference findings; say that it costs more and rarely helps here. For a single file, skip agents and review it yourself.

## Phase 1: Baseline

Cleanup is only safe if you can show behavior did not change.

1. Check `git status`. If there are uncommitted changes, suggest committing or stashing first so the cleanup is a separate, reviewable diff.
2. Identify the project's checks: test command, linter, formatter, type checker, build. Run them on the scope and record the results, including failures that already exist. Those are not yours to fix unless the user asks, but they must not get worse.
3. For a whole-repository scope on a large codebase, propose an order (for example, one package at a time) and confirm.

## Phase 2: Find Issues

Prefer tool output over judgment; tools prove that code is unused.

| Ecosystem | Dead code and unused imports | Types |
|-----------|------------------------------|-------|
| TypeScript/JavaScript | `npx knip` (unused files, exports, dependencies), ESLint `no-unused-vars` | `npx tsc --noEmit` |
| Python | `ruff check --select F401,F841,ERA001`, `vulture` (with a confidence threshold) | `mypy` or `pyright` if configured |
| Others | The language's linter (`go vet`, `cargo clippy`, ...) | Compiler warnings |

Use what the project already has; ask before adding a new dev dependency.

Then launch two `pr:code-reviewer` agents on the scope:

- **Dead code**: unused functions, variables, branches, feature flags that are always on or off, commented-out code, duplicated logic. Verify every candidate by searching for references, including dynamic use (string-based imports, reflection, registries, framework conventions such as route files or decorators), configuration, scripts, and tests.
- **Comments and documentation**: comments that restate the code, outdated or wrong comments, completed TODOs, references to old versions, missing docstrings on public APIs or non-obvious logic, docstrings whose parameters or return types no longer match.

Ask each for findings at ≥80% confidence with file and line, and the evidence.

## Phase 3: Confirm the Plan

Present the findings grouped by type (dead code, comments, documentation, other), with the evidence for each removal. List anything uncertain separately and ask about it. Removing exported or public APIs always needs explicit confirmation, since callers outside this repository may depend on them.

Wait for approval before editing.

## Phase 4: Clean

1. **Remove confirmed dead code**: unused imports, variables, functions, files, and commented-out blocks.
2. **Fix comments**: delete comments that restate code, correct outdated ones, and keep comments that explain why, warn about pitfalls, document public APIs, or carry license headers.
3. **Fix documentation in code**: make docstrings, JSDoc, and type annotations match the actual signatures and behavior; add them where public APIs or non-obvious logic lack them.
4. **Simplify**: run Claude Code's `/simplify` on the scope for duplication, reuse, and efficiency fixes (it edits files directly). Keep only changes that preserve behavior. If `/simplify` is unavailable, consolidate obvious duplication yourself.

Work in small batches and re-run the relevant tests between batches, so a failure points at a small change.

## Phase 5: Format and Lint

Run the project's formatter and linter with their existing configuration, and fix new warnings in the scope. Do not reformat files outside the scope or change lint rules.

## Phase 6: Verify

Re-run every check from Phase 1 and compare with the baseline. Everything that passed must still pass; anything that newly fails is a regression to fix or revert. Report the before and after results.

## Phase 7: Summary

Report:
- what was removed (counts and notable items), comments and docs fixed, and files touched
- `/simplify` changes kept
- baseline versus final check results
- items skipped and why, including pre-existing failures

Remind the user to review the diff and commit it (`/pr:commit-push`).

## Boundaries

- Change behavior, configuration, or architecture: no. This skill only removes and clarifies.
- Edit standalone documentation (README, `docs/`): leave it to `update-docs`.
- Commit or push: leave it to the user.
- Code used dynamically, by external consumers, or by environment-specific paths: keep it unless the user confirms.
