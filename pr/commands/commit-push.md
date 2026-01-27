---
description: Commit changes, update commit log, and push to remote with optional merge or PR creation
argument-hint: "[path] [description] [--merge | --pr]"
---

# Commit and Push

Commit changes, update commit log, and push to remote repository.

## Core Principles

- **Show before committing**: Always display what will be committed before taking action
- **Update commitlog.md**: Maintain a running log of all commits for project history
- **Standardize commit log naming**: Automatically rename variations to `commitlog.md`
- **Safe by default**: Never commit sensitive files, never force push without explicit request
- **Respect workflow**: Support both direct merge and PR-based workflows

---

## Phase 0: Argument Parsing

**Goal**: Parse and understand the user's request

**Arguments**: $ARGUMENTS

The arguments may contain any combination of:

1. **A path** (file or folder) - commit only changes in that scope (optional, defaults to all changes)
2. **`--merge` or `-merge`** - after pushing, merge the current branch into main/master
3. **`--pr` or `-pr`** - after pushing, create a Pull Request instead of merging directly
4. **Free text** - description of what was changed (used for commit message context)

**Examples**:
- `/pr:commit-push` → Commit all changes, update commitlog.md, push
- `/pr:commit-push src/auth` → Commit only changes in src/auth folder
- `/pr:commit-push --merge` → Commit, push, then merge to main/master
- `/pr:commit-push --pr` → Commit, push, then create a PR
- `/pr:commit-push fixed the authentication bug --pr` → With description, create PR
- `/pr:commit-push src/api added new search endpoints --merge` → Scoped with merge

If both `--merge` and `--pr` are provided, prefer `--pr` (safer workflow).

---

## Phase 0.5: Handle .claude/ in Version Control

**Goal**: Include Claude documentation in version control by default (for team collaboration)

**Default Behavior**: `.claude/` and `CLAUDE.md` are **included** in git by default.

**Actions**:

1. If the user explicitly requests to ignore `.claude/` (e.g., "ignore .claude", "don't commit .claude", "add .claude to gitignore"):
   - Add `.claude/` to `.gitignore`
   - Inform the user: "Added .claude/ to .gitignore as requested"

2. Otherwise, proceed normally - `.claude/` will be committed along with other project files

**Rationale**: The `.claude/` directory contains valuable project documentation (checkpoints, snapshots, RFDs, PRDs) that helps team members and future Claude sessions understand the project. Sharing this context improves collaboration. Users who prefer to keep it private can explicitly opt out.

---

## Phase 0.6: Standardize Commit Log File

**Goal**: Ensure consistent commit log naming across codebases

**Actions**:

1. Search for existing commit log file variations in the project root:
   - `commit_log.md`
   - `commit-log.md`
   - `COMMIT_LOG.md`
   - `COMMITLOG.md`
   - `CommitLog.md`
   - `Commit_Log.md`
   - `commit_log.MD`
   - Any other case variations

2. If a variation is found (and `commitlog.md` does NOT exist):
   - Rename the existing file to `commitlog.md` using `git mv` (preserves history)
   - Inform the user: "Renamed [old-name] to commitlog.md for consistency"

3. If both a variation AND `commitlog.md` exist:
   - **Ask the user** which file to keep
   - Merge contents if user requests, or delete the duplicate

4. If no commit log file exists, it will be created in Phase 2

```bash
# Example detection
ls -1 | grep -iE '^commit[-_]?log\.md$' | head -1
```

---

## Phase 1: Analyze Changes

**Goal**: Understand what will be committed

**Actions**:

1. Run `git status` to see all changed/staged/untracked files
2. Run `git diff` to see the actual changes (both staged and unstaged)
3. If a path scope was provided, filter to only those changes
4. Identify the current branch name
5. Present a summary of changes to the user

---

## Phase 2: Update commitlog.md

**Goal**: Maintain project commit history

**Actions**:

1. Check if `commitlog.md` exists in the project root

2. **If it does NOT exist**, create it with this template:

```markdown
# [Project Name] Commit Log

This file tracks significant commits and changes to the project.

### [DATE] - [TIME] ([branch name])

- **[Brief Title of Change]**
  - [Detail about what was changed]
  - [Why it was changed if relevant]
  - [Any important notes]
```

3. **If it exists**, add a new entry at the TOP (after the header):

```markdown
### [M/D/YYYY] - [HH:MM] ([branch name])

- **[Category]: [Brief Title of Change]**
  - [Specific detail about what changed]
  - [Additional context or reasoning]
```

**Guidelines for entries**:
- Use the current date and time
- Include the current branch name in parentheses
- Use bold for the main change title
- Include category prefix when applicable (Fix, Feature, Refactor, UI, API, etc.)
- Add sub-bullets for important details
- Keep descriptions concise but informative
- Group related changes under one timestamp if committing multiple things together

---

## Phase 3: Stage and Commit

**Goal**: Create the commit safely

**Actions**:

1. **Stage changes**:
   - If a path scope was provided, stage only files in that scope: `git add [path]`
   - If no scope, stage specific files (avoid `git add -A` to prevent accidentally staging sensitive files)
   - Always include the updated `commitlog.md` in the commit
   - **NEVER stage sensitive files** (.env, credentials, secrets, API keys) - warn and skip them

2. **Create commit** with a clear, descriptive message using HEREDOC format:

```bash
git commit -m "$(cat <<'EOF'
[Commit title]

[Optional body with more details]

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

- Summarize the changes concisely
- Use conventional commit format if the project uses it
- Reference the changes documented in commitlog.md

---

## Phase 4: Push to Remote

**Goal**: Push changes safely

**Actions**:

1. Push the current branch to its remote tracking branch
2. If no upstream is set, use `git push -u origin [branch-name]`
3. Verify the push was successful

---

## Phase 5: Handle --merge Flag (if provided)

**Goal**: Merge to main branch if requested

**Precondition**: Current branch is NOT main/master

**Actions**:

1. **Ask user before merging if there are potential conflicts**
2. Checkout main/master branch
3. Pull latest changes
4. Merge the feature branch into main/master
5. Push main/master to remote
6. Optionally checkout back to the feature branch

---

## Phase 6: Handle --pr Flag (if provided)

**Goal**: Create a Pull Request if requested

**Precondition**: Current branch is NOT main/master

**Actions**:

1. Use `gh pr create` with the commitlog.md entry as basis for PR description:

```bash
gh pr create --title "[PR Title]" --body "$(cat <<'EOF'
## Summary
[Bullet points from commitlog.md entry]

## Changes
[List of changed files/features]

Generated with [Claude Code](https://claude.ai/code)
EOF
)"
```

2. Return the PR URL to the user

---

## Phase 7: Summary

**Goal**: Report completion

**Actions**:

Present to user:
- What was committed (files and summary)
- The commit hash
- What branch was pushed
- If merged: confirmation of merge
- If PR created: the PR URL

---

## Safety Guidelines

**DO NOT:**
- Commit sensitive files (.env, credentials, API keys, secrets)
- Force push (`--force`) unless explicitly requested
- Push to main/master directly if `--pr` flag is used
- Merge without checking for conflicts first
- Skip the commitlog.md update

**ALWAYS:**
- Show the user what will be committed before committing
- Verify git operations succeeded before proceeding to next step
- Warn if trying to push to main/master from a feature branch without --merge or --pr
- Ask for confirmation if anything seems unusual
