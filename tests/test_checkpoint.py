"""Tests for pr/shared/checkpoint.py (runs the script as a subprocess)."""

import pathlib
import subprocess
import sys

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "pr" / "shared" / "checkpoint.py"


def run(root, *args, ok=True):
    result = subprocess.run([sys.executable, str(SCRIPT), *args, "--root", str(root)],
                            capture_output=True, text=True)
    assert (result.returncode == 0) == ok, result.stderr
    return result.stdout + result.stderr


def test_empty_project(tmp_path):
    assert "No .claude/checkpoints/" in run(tmp_path, "status")
    assert "no checkpoints exist" in run(tmp_path, "new-rfd", "X", ok=False)


def test_mvp_flow(tmp_path):
    run(tmp_path, "init")
    assert (tmp_path / ".claude/references").is_dir()
    out = run(tmp_path, "new-rfd", "MVP architecture", "--checkpoint", "0", "--number", "0", "--type", "Architecture")
    assert "RFD-0 in checkpoint-0" in out
    run(tmp_path, "new-rfd", "User Auth & Sessions!")
    files = sorted((tmp_path / ".claude/checkpoints/checkpoint-0/rfd").glob("*/rfd-*.md"))
    assert [f.parent.name for f in files] == ["0-mvp-architecture", "1-user-auth-sessions"]
    text = files[1].read_text()
    assert text.startswith("# RFD-1: User Auth & Sessions!")
    assert "**Type**: Feature" in text and "**Checkpoint**: checkpoint-0" in text and "{" not in text.split("## Request")[0]
    assert "duplicate" not in run(tmp_path, "status")
    assert "already exists" in run(tmp_path, "new-rfd", "Again", "--checkpoint", "0", "--number", "1", ok=False)


def test_new_checkpoint_and_status(tmp_path):
    run(tmp_path, "init")
    run(tmp_path, "new-checkpoint")
    (tmp_path / ".claude/checkpoints/checkpoint-1/snapshot.md").write_text("# Snapshot")
    run(tmp_path, "new-rfd", "Fix login", "--type", "Bug fix")
    out = run(tmp_path, "status")
    assert "latest: checkpoint-1" in out
    assert "Latest snapshot: .claude/checkpoints/checkpoint-1/snapshot.md" in out
    assert "Next RFD: checkpoint-1, number 2" in out and "Next checkpoint: checkpoint-2" in out
    assert "Planning" in out and "Numbering problems: none" in out


def test_gaps_and_existing_codebase(tmp_path):
    base = tmp_path / ".claude/checkpoints"
    for name in ("checkpoint-1/rfd/1-a", "checkpoint-1/rfd/3-c", "checkpoint-3"):
        (base / name).mkdir(parents=True)
    (base / "checkpoint-1/rfd/1-a/rfd-2026-01-01-1000.md").write_text("# RFD-1: A\n\n- **Status**: Completed\n")
    out = run(tmp_path, "status")
    assert "missing checkpoint numbers: 2" in out
    assert "checkpoint-1 missing RFD numbers: 2" in out
    assert "Completed" in out and "(no rfd-*.md)" in out
