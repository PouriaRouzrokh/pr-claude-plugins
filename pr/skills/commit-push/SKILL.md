---
name: commit-push
description: "Commit changes, prepend an entry to commitlog.md, and push to the remote, optionally merging into main (--merge) or opening a pull request (--pr)."
argument-hint: "[path] [description] [--merge | --pr]"
disable-model-invocation: true
---

# Commit and Push

Commit the user's changes safely, keep `commitlog.md` current, push, and optionally merge or open a PR.

**Arguments**: $ARGUMENTS

| Part | Meaning |
|------|---------|
| A path | Commit only changes under that file or folder (default: all changes) |
| Free text | What changed; use it for the commit message and log entry |
| `--merge` | After pushing, merge the branch into main/master |
| `--pr` | After pushing, open a pull request (if both flags are given, `--pr` wins as the safer choice) |

Examples: `/pr:commit-push`, `/pr:commit-push src/auth`, `/pr:commit-push fixed the session bug --pr`.

Use `writing-clearly-and-concisely` for the commit message, log entry, and PR description.

## 1. Inspect

1. `git status`, `git diff HEAD` (staged and unstaged), and the current branch. Respect the path scope if one was given.
2. Summarize what will be committed and show it to the user.
3. **Check for secrets.** Never commit `.env` files, credentials, private keys, or tokens. Look at both file names and the diff content (patterns such as `API_KEY=`, `sk-`, `AKIA`, `-----BEGIN`, `ghp_`, connection strings with passwords). If gitleaks is installed, stage the files and run `gitleaks git --pre-commit --redact --staged --verbose` (`--redact` keeps secret values out of the output). If anything looks sensitive, stop, show it, and ask; suggest adding it to `.gitignore`.
4. `CLAUDE.md` and the shared parts of `.claude/` (`checkpoints/`, `references/`, `rules/`, `settings.json`) are committed by default because they are the project's shared memory. Exclude them only if the user asks, and then add them to `.gitignore`. Never commit `.claude/settings.local.json` or `CLAUDE.local.md` (personal), or `.claude/worktrees/` (agent worktrees, which git would record as embedded repositories). If they are not ignored yet, offer to add them to `.gitignore`.
5. **Branch first.** If `--pr` was given and you are on main/master, create the branch now (`git switch -c {type}/{short-slug}`), so the log entry below records the right branch.

## 2. Update commitlog.md

1. Standardize the name: if a variant exists (`commit_log.md`, `COMMITLOG.md`, `commit-log.md`) and `commitlog.md` does not, rename it with `git mv`; if both exist, ask which to keep.
2. If none exists, create it:

   ```markdown
   # {Project Name} Commit Log

   This file tracks significant commits and changes to the project.

   ---
   ```

3. Prepend an entry right after the header, grouping related changes under one entry:

   ```markdown
   ### {M/D/YYYY} - {HH:MM} ({branch})

   - **{Category}: {Short title}**
     - {What changed}
     - {Why, when it is not obvious}

   ---
   ```

   Categories: Feature, Fix, Improve, Refactor, Docs, Test, Chore, UI, API.

## 3. Commit

1. Stage specific paths (the scope, or each changed file) plus `commitlog.md`. Avoid `git add -A`, which can sweep in files the user never meant to commit.
2. Commit with a heredoc so formatting survives:

   ```bash
   git commit -m "$(cat <<'EOF'
   {Title, imperative mood, under ~72 characters}

   {Body: what and why, wrapped at ~72 columns}

   {Attribution lines Claude Code provides for this session, if any}
   EOF
   )"
   ```

   Follow the project's convention (check `git log --oneline -20`; use Conventional Commits if the project does).
3. If a pre-commit hook fails, fix the reported problem, re-stage, and create the commit again. Do not bypass hooks with `--no-verify`, and do not amend unless the user asks.

## 4. Push

Push the current branch (`git push -u origin {branch}` if it has no upstream) and confirm it succeeded. Never force-push unless the user explicitly asks; if the push is rejected because the remote moved, pull with rebase (or ask) and push again.

## 5. Merge (`--merge`)

Skip this if you are already on main/master (the push updated it) and say so. Otherwise:

1. `git fetch` and check whether the merge will conflict; if it will, describe the conflicts and ask how to proceed.
2. Switch to main/master, pull, merge the branch (`--no-ff` unless the history shows fast-forward merges), and push.
3. Switch back to the feature branch if the user will keep working on it.

## 6. Pull Request (`--pr`)

```bash
gh pr create --title "{title}" --body "$(cat <<'EOF'
## Summary
{Bullets from the commitlog entry}

## Changes
{Files or areas changed}

## Testing
{How it was verified}

{PR attribution line Claude Code provides, if any}
EOF
)"
```

Return the PR URL. If `gh` is missing or not authenticated, give the user the compare URL instead.

## 7. Report

The commit hash and message, files committed, branch pushed, and the merge result or PR URL.
