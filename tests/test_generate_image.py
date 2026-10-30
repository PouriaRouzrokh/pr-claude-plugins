"""Offline tests for generate_image.py: the Gemini client is replaced by a fake."""

import base64
import importlib.util
import os
import pathlib
import sys
import types

import pytest

from conftest import SKILLS

SCRIPT = SKILLS / "generate-image/scripts/generate_image.py"
PNG = base64.b64encode(b"\x89PNG fake").decode()
JPG = base64.b64encode(b"\xff\xd8 fake").decode()


def load_module():
    spec = importlib.util.spec_from_file_location("generate_image", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ns(**kw):
    return types.SimpleNamespace(**kw)


class FakeInteractions:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def create(self, **request):
        self.calls.append(request)
        r = self.responses.pop(0)
        if isinstance(r, Exception):
            raise r
        return r


def ok(data=PNG, mime="image/png", text=None, steps=None):
    return ns(id="int_123", status="completed", output_text=text,
              output_image=ns(data=data, mime_type=mime), steps=steps or [], errors=None)


@pytest.fixture
def run(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("HOME", str(tmp_path))

    def _run(argv, responses=(ok(),)):
        mod = load_module()
        fake = FakeInteractions(responses)
        monkeypatch.setattr(mod.genai, "Client", lambda api_key: ns(interactions=fake))
        monkeypatch.setattr(mod.time, "sleep", lambda s: None)
        monkeypatch.setattr(sys, "argv", ["generate_image.py", *argv])
        mod.main()
        return fake.calls

    return _run


def test_plain_prompt_defaults(run, tmp_path, capsys):
    calls = run(["A red fox in snow"])
    req = calls[0]
    assert req["model"] == "gemini-nano-banana-2.1"
    assert req["input"] == "A red fox in snow"
    assert req["response_format"] == {"type": "image", "mime_type": "image/png"}
    assert "tools" not in req and "generation_config" not in req
    assert (tmp_path / "generated_image.png").read_bytes() == b"\x89PNG fake"
    out = capsys.readouterr().out
    assert "Interaction ID: int_123" in out


def test_json_wrapper_config(run, tmp_path):
    prompt = '{"prompt": "Poster", "config": {"model": "pro", "size": "2k", "aspect_ratio": "2:3", "output": "out/poster.jpg"}}'
    calls = run([prompt], responses=[ok(JPG, "image/jpeg")])
    req = calls[0]
    assert req["model"] == "gemini-3-pro-image"
    assert req["input"] == "Poster"
    assert req["response_format"] == {"type": "image", "mime_type": "image/jpeg",
                                      "aspect_ratio": "2:3", "image_size": "2K"}
    assert (tmp_path / "out" / "poster.jpg").exists()


def test_structured_json_is_sent_as_json(run):
    calls = run(['{"subject": "cat", "style": "watercolor", "config": {"size": "1K"}}'])
    assert calls[0]["input"] == '{"subject": "cat", "style": "watercolor"}'


def test_edit_images_and_continue(run, tmp_path):
    (tmp_path / "a.png").write_bytes(b"a")
    (tmp_path / "b.jpg").write_bytes(b"b")
    calls = run(["Combine them", "-e", "a.png", "-e", "b.jpg", "--continue", "int_prev"])
    req = calls[0]
    assert [b["type"] for b in req["input"]] == ["image", "image", "text"]
    assert req["input"][1]["mime_type"] == "image/jpeg"
    assert req["previous_interaction_id"] == "int_prev"


def test_search_tools_per_model(run):
    nb = run(["x", "--search"])[0]["tools"]
    assert nb == [{"type": "google_search", "search_types": ["web_search", "image_search"]}]
    pro = run(["x", "--search", "-m", "pro"])[0]["tools"]
    assert pro == [{"type": "google_search"}]


@pytest.mark.parametrize("argv,msg", [
    (["x", "-m", "lite", "--search"], "does not support search"),
    (["x", "-s", "512"], "supports sizes"),
    (["x", "-m", "pro", "-a", "8:1"], "does not support aspect ratio"),
    (["x", "-m", "pro", "--thinking", "high"], "thinking levels"),
    (["x", "-e", "missing.png"], "input image not found"),
    (["x", "-o", "out.webp"], "unsupported output extension"),
    (['{"config": {"size": "1K"}}'], "prompt is empty"),
])
def test_validation_errors(run, argv, msg):
    with pytest.raises(SystemExit) as exc:
        run(argv)
    assert msg in str(exc.value)


def test_nb2_allows_512(run):
    assert run(["x", "-m", "nb2", "-s", "512"])[0]["response_format"]["image_size"] == "512"


def test_unknown_model_skips_validation(run):
    req = run(["x", "-m", "gemini-future-image", "-s", "8K", "--search"])[0]
    assert req["model"] == "gemini-future-image"
    assert req["tools"] == [{"type": "google_search"}]


def test_no_overwrite(run, tmp_path):
    (tmp_path / "img.png").write_bytes(b"old")
    run(["x", "-o", "img.png"])
    assert (tmp_path / "img.png").read_bytes() == b"old"
    assert (tmp_path / "img-1.png").exists()


def test_mime_mismatch_fixes_extension(run, tmp_path):
    run(["x", "-o", "pic.png"], responses=[ok(JPG, "image/jpeg")])
    assert (tmp_path / "pic.jpg").exists()


def test_falls_back_to_last_step_image(run, tmp_path):
    steps = [ns(type="thought", content=[ns(type="image", data=PNG)]),
             ns(type="model_output", content=[ns(type="text", text="hi"), ns(type="image", data=JPG, mime_type="image/jpeg")])]
    resp = ns(id="i", status="completed", output_text=None, output_image=None, steps=steps, errors=None)
    run(["x", "-o", "s.jpg"], responses=[resp])
    assert (tmp_path / "s.jpg").read_bytes() == b"\xff\xd8 fake"


def test_no_image_exits(run):
    resp = ns(id="i", status="failed", output_text=None, output_image=None, steps=[],
              errors=[ns(message="blocked")])
    with pytest.raises(SystemExit) as exc:
        run(["x"], responses=[resp])
    assert "status: failed" in str(exc.value) and "blocked" in str(exc.value)


def test_retry_then_success(run):
    err = Exception("rate limited")
    err.status_code = 429
    calls = run(["x"], responses=[err, ok()])
    assert len(calls) == 2


def test_non_retryable_error(run):
    err = Exception("bad")
    err.status_code = 403
    with pytest.raises(SystemExit) as exc:
        run(["x"], responses=[err])
    assert "lacks access" in str(exc.value)


def test_search_suggestions_saved(run, tmp_path):
    steps = [ns(type="google_search_result", result=[ns(search_suggestions="<div>chip</div>")])]
    run(["x", "--search"], responses=[ok(steps=steps)])
    assert (tmp_path / "generated_image.search.html").read_text() == "<div>chip</div>"


def test_env_file_parsing(tmp_path, monkeypatch):
    mod = load_module()
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / ".env").write_text('# c\nexport GEMINI_API_KEY="abc123"\n')
    assert mod.load_api_key() == "abc123"


def test_missing_key_exits(tmp_path, monkeypatch):
    mod = load_module()
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path))
    with pytest.raises(SystemExit) as exc:
        mod.load_api_key()
    assert "GEMINI_API_KEY not found" in str(exc.value)


def test_request_validates_against_sdk_types(run):
    """The request dict must parse as the SDK's CreateModelInteraction model."""
    from google.genai._gaos.types.interactions.createmodelinteraction import CreateModelInteraction
    calls = run(["x", "-s", "2K", "-a", "16:9", "--search", "--thinking", "high", "--continue", "p"])
    CreateModelInteraction.model_validate(calls[0])


@pytest.mark.parametrize("argv,expected", [
    (["x"], "about $0.034 for the 1K image"),
    (["x", "-s", "4k"], "about $0.113 for the 4K image"),
    (["x", "-m", "pro", "-s", "2K"], "about $0.134 for the 2K image"),
    (["x", "-m", "nb2", "-s", "512"], "about $0.045 for the 512 image"),
    (["x", "-m", "lite"], "about $0.034 for the 1K image"),
])
def test_google_cost_line(run, capsys, argv, expected):
    run(argv)
    out = capsys.readouterr().out
    assert expected in out and "Interaction ID: int_123" in out


def test_google_cost_line_skipped_for_unknown_model(run, capsys):
    run(["x", "-m", "gemini-2.5-flash-image"])
    out = capsys.readouterr().out
    assert "Estimated cost" not in out and "Interaction ID" in out


def test_search_html_does_not_overwrite(run, tmp_path):
    (tmp_path / "generated_image.search.html").write_text("old")
    steps = [ns(type="google_search_result", result=[ns(search_suggestions="<div>new</div>")])]
    run(["x", "--search"], responses=[ok(steps=steps)])
    assert (tmp_path / "generated_image.search.html").read_text() == "old"
    assert (tmp_path / "generated_image.search-1.html").read_text() == "<div>new</div>"
