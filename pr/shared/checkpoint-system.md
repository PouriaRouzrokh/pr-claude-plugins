# Checkpoint System

The pr plugin keeps a project's long-term memory in `.claude/`. Every workflow skill follows these conventions so documents written by one skill are found by the others.

## Contents

- [Layout](#layout)
- [Documents](#documents)
- [Rules](#rules)
- [The helper script](#the-helper-script)
- [Bug-fix RFDs](#bug-fix-rfds)
- [Permissions](#permissions)

## Layout

```
.claude/
├── checkpoints/
│   ├── checkpoint-0/                 # Before the first snapshot (new projects)
│   │   ├── prd.md                    # Product Requirements Document
│   │   └── rfd/
│   │       ├── 0-architecture/rfd-2026-10-09-1400.md   # MVP architecture (mvp-dev)
│   │       └── 1-user-auth/rfd-2026-10-09-1530.md
│   ├── checkpoint-1/
│   │   ├── snapshot.md               # State of the code when checkpoint-1 was created
│   │   └── rfd/                      # Work done after that snapshot
│   └── checkpoint-N/
└── references/                       # Guidelines, specs, package docs (not tied to code changes)
```

A checkpoint is a snapshot followed by the RFDs for work done after it. Existing codebases that adopt the system start at checkpoint-1 (there is no checkpoint-0 unless a PRD is added).

## Documents

| Document | Written by | Changes after creation? |
|----------|-----------|-------------------------|
| `prd.md` | `create-prd`, `handle-claude-md` | Only when the user confirms requirements changed |
| `snapshot.md` | `create-snapshot` | Never. Snapshots are point-in-time records; create a new checkpoint instead |
| RFD | `feature-dev`, `mvp-dev`, `systematic-debugging`, `update-docs` | Yes, edited in place throughout its lifecycle |
| `references/*` | The user | Only with the user's confirmation |

## Rules

- **New RFDs go in the latest checkpoint.** Number them per checkpoint, starting at 1; `0` is reserved for an MVP architecture RFD in checkpoint-0.
- **One file per RFD**: `rfd/{N}-{slug}/rfd-{YYYY-MM-DD}-{HHMM}.md`, timestamped at creation. Update that file in place and bump **Last Updated**; do not add a second file for the same RFD.
- **Create or update?** Update an RFD when the work refines, fixes, or extends what it tracks; create a new one for a distinct feature, a significant fix, or an architectural change. Keep unrelated changes in separate RFDs. Ask the user when unsure.
- **Status values**: Planning, In Progress, Completed, On Hold.
- **Thoroughness**: RFDs are what future sessions read instead of re-exploring the code. Record specific file paths, function names, decisions with their reasons, alternatives rejected, test evidence, and every file changed. A reader should understand what happened without opening the diff.
- **Numbering gaps**: report gaps or duplicates to the user rather than renumbering silently; other documents may reference the existing numbers.

## The helper script

`checkpoint.py` (in the same folder as this document; Python 3, standard library) applies these rules so skills do not hand-roll shell snippets. The skill that sent you here gives its full path; it is shortened to `checkpoint.py` below:

```bash
python3 checkpoint.py status                     # checkpoints, PRD, snapshots, RFDs with status, next numbers, gaps
python3 checkpoint.py new-rfd "User authentication"   # creates the next RFD from the template and prints its path
python3 checkpoint.py new-rfd "Login fails on Safari" --type "Bug fix"
python3 checkpoint.py new-rfd "MVP architecture" --checkpoint 0 --number 0 --type Architecture
python3 checkpoint.py new-checkpoint             # next checkpoint directory for a snapshot
python3 checkpoint.py init                       # checkpoint-0/rfd and references/ for a new project
```

All commands accept `--root PATH` when the project is not the current directory. The RFD template lives next to the script (`rfd-template.md`); fill every section, writing "N/A — reason" rather than deleting one.

## Bug-fix RFDs

For a non-trivial bug, create the RFD with `--type "Bug fix"` and use the Request and Plan sections for: the symptom and how to reproduce it, the root cause with the evidence that proved it, the fix, and the regression test.

## Permissions

Claude Code treats `.claude/` as a protected path, so writing RFDs and snapshots asks for permission even when other edits are pre-approved, and plan mode blocks those writes. When the first prompt appears, the user can allow edits to the project's `.claude/` folder for the session. If the session is in plan mode, finish planning, get approval, and write the RFD afterwards.
