"""Offline tests for generate_svg.py: the Gemini client is replaced by a fake."""

import importlib.util
import os
import pathlib
import sys
import types

import pytest

from conftest import SKILLS

SCRIPT = SKILLS / "generate-svg/scripts/generate_svg.py"
GOOD = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><circle cx="12" cy="12" r="10"/></svg>'


def load_module():
    spec = importlib.util.spec_from_file_location("generate_svg", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class FakeModels:
    def __init__(self, texts):
        self.texts = list(texts)
        self.calls = []

    def generate_content(self, model, contents, config):
        self.calls.append({"model": model, "contents": contents, "config": config})
        t = self.texts.pop(0)
        if isinstance(t, Exception):
            raise t
        return types.SimpleNamespace(text=t)


@pytest.fixture
def run(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GEMINI_API_KEY", "k")

    def _run(argv, texts=(GOOD,)):
        mod = load_module()
        fake = FakeModels(texts)
        monkeypatch.setattr(mod.genai, "Client", lambda api_key: types.SimpleNamespace(models=fake))
        monkeypatch.setattr(mod.time, "sleep", lambda s: None)
        monkeypatch.setattr(sys, "argv", ["generate_svg.py", *argv])
        mod.main()
        return fake.calls

    return _run


def test_defaults(run, tmp_path):
    calls = run(["gear icon", "-t", "icon"])
    c = calls[0]
    assert c["model"] == "gemini-3.8-flash"
    assert "Lucide" in c["contents"] and 'viewBox="0 0 24 24"' in c["contents"]
    assert c["config"].system_instruction.startswith("You are an expert SVG designer")
    assert c["config"].thinking_config is None
    assert (tmp_path / "generated.svg").read_text().strip() == GOOD


def test_fenced_output_and_json_prompt(run, tmp_path):
    text = "Here you go:\n```svg\n" + GOOD + "\n```\nEnjoy"
    prompt = '{"description": "hero", "colors": {"primary": "#123"}, "config": {"type": "hero", "output": "a/hero.svg", "model": "pro", "thinking": "high"}}'
    calls = run([prompt], texts=[text])
    c = calls[0]
    assert c["model"] == "gemini-3.1-pro-preview"
    assert c["config"].thinking_config.thinking_level.value.lower() == "high"
    assert '"primary": "#123"' in c["contents"] and "1200x600" in c["contents"]
    assert (tmp_path / "a" / "hero.svg").read_text().strip() == GOOD


def test_repair_attempt(run, tmp_path):
    calls = run(["x"], texts=['<svg xmlns="http://www.w3.org/2000/svg"><g></svg>', GOOD])
    assert len(calls) == 2
    assert "not a valid SVG" in calls[1]["contents"]
    assert (tmp_path / "generated.svg").exists()


def test_repair_fails(run):
    with pytest.raises(SystemExit) as exc:
        run(["x"], texts=["no svg here", "still none"])
    assert "did not return a valid SVG" in str(exc.value)


def test_sanitize(run, tmp_path):
    bad = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10" onload="alert(1)">'
           '<script>alert(2)</script><a href="javascript:alert(3)"><rect onclick=\'x()\' width="5" height="5"/></a></svg>')
    run(["x"], texts=[bad])
    out = (tmp_path / "generated.svg").read_text()
    assert "script" not in out and "onload" not in out and "onclick" not in out and "javascript" not in out
    assert 'href="#"' in out


def test_edit_includes_existing(run, tmp_path):
    (tmp_path / "old.svg").write_text(GOOD)
    calls = run(["make it blue", "-e", "old.svg", "-o", "new.svg"])
    assert "Modify the existing SVG" in calls[0]["contents"] and GOOD in calls[0]["contents"]
    assert "Requested changes:\nmake it blue" in calls[0]["contents"]


@pytest.mark.parametrize("argv,msg", [
    (["x", "--thinking", "minimal"], "thinking levels"),
    (["x", "-e", "nope.svg"], "not found"),
    (["x", "-o", "x.png"], "must end in .svg"),
    (['{"config": {"type": "banner"}}'], "description is empty"),
    (['{"description": "d", "config": {"type": "banner"}}'], "unknown type"),
])
def test_validation(run, argv, msg):
    with pytest.raises(SystemExit) as exc:
        run(argv)
    assert msg in str(exc.value)


def test_no_overwrite_and_preview(run, tmp_path):
    (tmp_path / "generated.svg").write_text("old")
    run(["x", "--preview"])
    assert (tmp_path / "generated.svg").read_text() == "old"
    assert (tmp_path / "generated-1.svg").exists()
    png = (tmp_path / "generated-1.preview.png").read_bytes()
    assert png.startswith(b"\x89PNG")


def test_retry(run):
    err = Exception("busy")
    err.code = 503
    assert len(run(["x"], texts=[err, GOOD])) == 2
