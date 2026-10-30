#!/usr/bin/env python3
"""Inspect and extend a project's .claude/checkpoints documentation tree.

Single source of truth for checkpoint and RFD numbering used by the pr
plugin's workflow skills. Standard library only; runs on Python 3.8+.

Commands:
    status          Summarize checkpoints, PRD, snapshots, RFDs, and numbering gaps
    new-rfd TITLE   Create the next RFD in the latest checkpoint from the template
    new-checkpoint  Create the next checkpoint directory (for a new snapshot)
    init            Create checkpoint-0/rfd and references/ for a new project

Options:
    --root PATH         Project root (default: current directory)
    --checkpoint N      new-rfd: target checkpoint instead of the latest
    --number N          new-rfd: explicit RFD number (e.g. 0 for an MVP architecture RFD)
    --type TYPE         new-rfd: Feature | Bug fix | Architecture | Refactor (default: Feature)
"""

import argparse
import datetime
import pathlib
import re
import sys

CHECKPOINT_RE = re.compile(r"^checkpoint-(\d+)$")
RFD_DIR_RE = re.compile(r"^(\d+)-(.+)$")
TEMPLATE = pathlib.Path(__file__).resolve().parent / "rfd-template.md"


def checkpoints_dir(root):
    return root / ".claude" / "checkpoints"


def list_checkpoints(root):
    base = checkpoints_dir(root)
    if not base.is_dir():
        return []
    found = []
    for entry in base.iterdir():
        match = CHECKPOINT_RE.match(entry.name)
        if entry.is_dir() and match:
            found.append((int(match.group(1)), entry))
    return sorted(found)


def list_rfds(checkpoint_path):
    rfd_root = checkpoint_path / "rfd"
    if not rfd_root.is_dir():
        return []
    rfds = []
    for entry in rfd_root.iterdir():
        match = RFD_DIR_RE.match(entry.name)
        if not (entry.is_dir() and match):
            continue
        files = sorted(entry.glob("rfd-*.md"))
        doc = files[-1] if files else None
        title, status = "", "unknown"
        if doc:
            text = doc.read_text(errors="replace")
            heading = re.search(r"^#\s+(.+)$", text, re.M)
            state = re.search(r"\*\*Status\*\*:\s*([^\n|]+)", text)
            title = heading.group(1).strip() if heading else ""
            status = state.group(1).strip() if state else "unknown"
        rfds.append({"number": int(match.group(1)), "slug": match.group(2), "dir": entry,
                     "file": doc, "files": len(files), "title": title, "status": status})
    return sorted(rfds, key=lambda r: r["number"])


def gaps(numbers, start):
    expected = set(range(start, max(numbers) + 1)) if numbers else set()
    return sorted(expected - set(numbers))


def slugify(title):
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:60].rstrip("-") or "untitled"


def rel(path, root):
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def cmd_status(root):
    checkpoints = list_checkpoints(root)
    if not checkpoints:
        print("No .claude/checkpoints/ directory. Run `init` for a new project, or create a "
              "snapshot (checkpoint-1) for an existing codebase.")
        return
    numbers = [n for n, _ in checkpoints]
    latest_n, latest_path = checkpoints[-1]
    prd = checkpoints_dir(root) / "checkpoint-0" / "prd.md"
    snapshots = [(n, p / "snapshot.md") for n, p in checkpoints if (p / "snapshot.md").is_file()]

    print(f"Project root: {root}")
    print(f"Checkpoints: {', '.join(str(n) for n in numbers)} (latest: checkpoint-{latest_n})")
    print(f"PRD: {rel(prd, root) if prd.is_file() else 'none'}")
    print("Latest snapshot: " + (rel(snapshots[-1][1], root) if snapshots else "none"))
    missing = [n for n, p in checkpoints if n >= 1 and not (p / "snapshot.md").is_file()]
    if missing:
        print("Checkpoints without snapshot.md: " + ", ".join(f"checkpoint-{n}" for n in missing))

    problems = []
    checkpoint_gaps = gaps(numbers, 0 if 0 in numbers else 1)
    if checkpoint_gaps:
        problems.append("missing checkpoint numbers: " + ", ".join(map(str, checkpoint_gaps)))

    for n, path in checkpoints:
        rfds = list_rfds(path)
        print(f"\ncheckpoint-{n} RFDs ({len(rfds)}):")
        for r in rfds:
            note = f"  [{r['files']} files]" if r["files"] > 1 else ""
            location = rel(r["file"], root) if r["file"] else rel(r["dir"], root) + " (no rfd-*.md)"
            print(f"  {r['number']:>3}  {r['status']:<12} {r['title'] or r['slug']}  -> {location}{note}")
        rfd_numbers = [r["number"] for r in rfds]
        rfd_gaps = gaps(rfd_numbers, 0 if 0 in rfd_numbers else 1)
        if rfd_gaps:
            problems.append(f"checkpoint-{n} missing RFD numbers: " + ", ".join(map(str, rfd_gaps)))
        duplicates = sorted({x for x in rfd_numbers if rfd_numbers.count(x) > 1})
        if duplicates:
            problems.append(f"checkpoint-{n} duplicate RFD numbers: " + ", ".join(map(str, duplicates)))

    latest_rfds = [r["number"] for r in list_rfds(latest_path)]
    print(f"\nNext RFD: checkpoint-{latest_n}, number {max(latest_rfds, default=0) + 1}")
    print(f"Next checkpoint: checkpoint-{latest_n + 1}")
    print("\nNumbering problems: " + ("; ".join(problems) if problems else "none"))


def cmd_new_rfd(root, title, checkpoint, number, rfd_type):
    checkpoints = list_checkpoints(root)
    if checkpoint is None:
        if not checkpoints:
            sys.exit("Error: no checkpoints exist yet. Run `init` (new project) or create a snapshot first.")
        checkpoint, target = checkpoints[-1]
    else:
        target = checkpoints_dir(root) / f"checkpoint-{checkpoint}"
        if not target.is_dir():
            sys.exit(f"Error: {rel(target, root)} does not exist.")
    existing = list_rfds(target)
    if number is None:
        number = max((r["number"] for r in existing), default=0) + 1
    elif any(r["number"] == number for r in existing):
        sys.exit(f"Error: RFD {number} already exists in checkpoint-{checkpoint}.")

    now = datetime.datetime.now()
    folder = target / "rfd" / f"{number}-{slugify(title)}"
    path = folder / f"rfd-{now:%Y-%m-%d}-{now:%H%M}.md"
    folder.mkdir(parents=True, exist_ok=False)
    text = TEMPLATE.read_text()
    for key, value in {"{N}": str(number), "{TITLE}": title, "{DATETIME}": f"{now:%Y-%m-%d %H:%M}",
                       "{CHECKPOINT}": str(checkpoint), "{TYPE}": rfd_type}.items():
        text = text.replace(key, value)
    path.write_text(text)
    print(f"Created RFD-{number} in checkpoint-{checkpoint}: {rel(path, root)}")


def cmd_new_checkpoint(root):
    checkpoints = list_checkpoints(root)
    number = checkpoints[-1][0] + 1 if checkpoints else 1
    path = checkpoints_dir(root) / f"checkpoint-{number}"
    (path / "rfd").mkdir(parents=True)
    print(f"Created checkpoint-{number}: {rel(path, root)}")


def cmd_init(root):
    created = []
    for path in (checkpoints_dir(root) / "checkpoint-0" / "rfd", root / ".claude" / "references"):
        if not path.is_dir():
            path.mkdir(parents=True)
            created.append(rel(path, root))
    print("Created: " + ", ".join(created) if created else "Structure already exists.")


def main():
    parser = argparse.ArgumentParser(description="Manage .claude/checkpoints for the pr plugin.")
    parser.add_argument("command", choices=["status", "new-rfd", "new-checkpoint", "init"])
    parser.add_argument("title", nargs="?", help="RFD title (new-rfd)")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--checkpoint", type=int, help="Target checkpoint for new-rfd")
    parser.add_argument("--number", type=int, help="Explicit RFD number for new-rfd")
    parser.add_argument("--type", default="Feature", help="RFD type for new-rfd")
    args = parser.parse_args()
    root = pathlib.Path(args.root).expanduser().resolve()

    if args.command == "status":
        cmd_status(root)
    elif args.command == "new-rfd":
        if not args.title:
            sys.exit("Error: new-rfd needs a title, e.g. new-rfd \"User authentication\"")
        cmd_new_rfd(root, args.title, args.checkpoint, args.number, args.type)
    elif args.command == "new-checkpoint":
        cmd_new_checkpoint(root)
    else:
        cmd_init(root)


if __name__ == "__main__":
    main()
