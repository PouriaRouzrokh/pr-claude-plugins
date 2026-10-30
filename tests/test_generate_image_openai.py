"""Offline tests for the OpenAI (GPT Image) backend of generate_image.py."""

import base64
import importlib.util
import sys
import types

import pytest

from conftest import SKILLS

SCRIPT = SKILLS / "generate-image/scripts/generate_image.py"
PNG = base64.b64encode(b"\x89PNG gpt").decode()
ns = types.SimpleNamespace


def load_module():
    spec = importlib.util.spec_from_file_location("generate_image", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def response(count=1, revised=None):
    usage = ns(total_tokens=6400, output_tokens=6000,
               input_tokens_details=ns(text_tokens=100, image_tokens=300))
    return ns(data=[ns(b64_json=PNG, revised_prompt=revised) for _ in range(count)], usage=usage)


class FakeImages:
    def __init__(self, result):
        self.result, self.calls = result, []

    def generate(self, **params):
        self.calls.append(("generate", params))
        if isinstance(self.result, Exception):
            raise self.result
        return self.result

    def edit(self, **params):
        self.calls.append(("edit", params))
        return self.result


@pytest.fixture
def run(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv("HOME", str(tmp_path))

    def _run(argv, result=None):
        mod = load_module()
        images = FakeImages(result or response())
        monkeypatch.setattr(mod, "OpenAI", lambda api_key: ns(images=images))
        monkeypatch.setattr(mod.time, "sleep", lambda s: None)
        monkeypatch.setattr(sys, "argv", ["generate_image.py", *argv])
        mod.main()
        return images.calls

    return _run


def test_generate_defaults(run, tmp_path, capsys):
    (method, params), = run(["A fox sticker", "-m", "gpt"])
    assert method == "generate"
    assert params == {"model": "gpt-image-2.5-sunburst", "prompt": "A fox sticker",
                      "output_format": "png", "n": 1}
    assert (tmp_path / "generated_image.png").read_bytes() == b"\x89PNG gpt"
    out = capsys.readouterr().out
    assert "6,400 tokens" in out and "$0.183" in out  # (100*5 + 300*8 + 6000*30) / 1M


def test_transparent_variations_webp(run, tmp_path):
    (_, params), = run(["Logo mark", "-m", "gpt-fast", "--background", "transparent",
                        "-n", "3", "-o", "logo.webp", "--quality", "high"], result=response(3))
    assert params["model"] == "gpt-image-2.5-flare"
    assert params["background"] == "transparent" and params["output_format"] == "webp"
    assert params["n"] == 3 and params["quality"] == "high"
    assert sorted(p.name for p in tmp_path.glob("logo*.webp")) == ["logo-1.webp", "logo-2.webp", "logo.webp"]


def test_edit_with_mask_and_references(run, tmp_path):
    for name in ("room.png", "sofa.jpg", "mask.png"):
        (tmp_path / name).write_bytes(b"x")
    (method, params), = run(["Replace the sofa", "-m", "gpt", "-e", "room.png", "-e", "sofa.jpg",
                             "--mask", "mask.png"])
    assert method == "edit"
    assert [t[0] for t in params["image"]] == ["room.png", "sofa.jpg"]
    assert params["image"][1][2] == "image/jpeg"
    assert params["mask"][0] == "mask.png"


@pytest.mark.parametrize("size,aspect,expected", [
    (None, None, None),
    (None, "16:9", "1680x944"),
    ("1K", "3:2", "1536x1024"),
    ("2K", "16:9", "2560x1440"),
    ("4K", "16:9", "3840x2160"),
    ("auto", None, "auto"),
    ("1536x864", None, "1536x864"),
    ("2K", "1:1", "1920x1920"),
])
def test_size_translation(size, aspect, expected):
    mod = load_module()
    assert mod.gpt_size(size.upper() if size else None, aspect) == expected


@pytest.mark.parametrize("argv,msg", [
    (["x", "-m", "gpt", "--search"], "only available with Google models"),
    (["x", "-m", "gpt", "--continue", "abc"], "passing it back with -e"),
    (["x", "-m", "gpt", "-a", "4:1"], "between 1:3 and 3:1"),
    (["x", "-m", "gpt", "-s", "1000x1000"], "multiples of 16"),
    (["x", "-m", "gpt", "-s", "512"], "GPT sizes are"),
    (["x", "-m", "gpt", "-n", "11"], "between 1 and 10"),
    (["x", "-m", "gpt", "--mask", "m.png"], "input image not found"),
    (["x", "-m", "gpt", "--background", "transparent", "-o", "a.jpg"], "need a .png or .webp"),
    (["x", "-m", "gpt-image-2", "--quality", "max"], "quality levels"),
    (["x", "--background", "transparent"], "only available with GPT models"),
    (["x", "-n", "4"], "only available with GPT models"),
    (["x", "-o", "a.webp"], "unsupported output extension"),
])
def test_validation(run, tmp_path, argv, msg):
    with pytest.raises(SystemExit) as exc:
        run(argv)
    assert msg in str(exc.value)


def test_mask_requires_edit(run, tmp_path):
    (tmp_path / "m.png").write_bytes(b"x")
    with pytest.raises(SystemExit) as exc:
        run(["x", "-m", "gpt", "--mask", "m.png"])
    assert "--mask needs the image" in str(exc.value)


def test_full_model_id_routes_to_openai(run):
    (_, params), = run(["x", "-m", "chatgpt-image-latest"])
    assert params["model"] == "chatgpt-image-latest"


def test_revised_prompt_and_empty_result(run, capsys):
    run(["x", "-m", "gpt"], result=response(1, revised="A detailed fox"))
    assert "Revised prompt: A detailed fox" in capsys.readouterr().out
    with pytest.raises(SystemExit) as exc:
        run(["x", "-m", "gpt"], result=ns(data=[], usage=None))
    assert "No image was returned" in str(exc.value)


def test_retry_then_error_hint(run):
    err = Exception("forbidden")
    err.status_code = 403
    with pytest.raises(SystemExit) as exc:
        run(["x", "-m", "gpt"], result=err)
    assert "organization verification" in str(exc.value)


def test_missing_openai_key(tmp_path, monkeypatch):
    mod = load_module()
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path))
    with pytest.raises(SystemExit) as exc:
        mod.load_api_key(("OPENAI_API_KEY",))
    assert "OPENAI_API_KEY not found" in str(exc.value) and "platform.openai.com" in str(exc.value)


def test_params_match_sdk_signature(run, tmp_path):
    """Every parameter the script sends must exist on the SDK's generate/edit methods."""
    import inspect
    from openai import OpenAI
    client = OpenAI(api_key="x")
    (tmp_path / "a.png").write_bytes(b"x")
    (tmp_path / "m.png").write_bytes(b"x")
    for argv, method in ((["x", "-m", "gpt", "-s", "2K", "-a", "16:9", "--quality", "max",
                           "--background", "opaque", "-n", "2"], "generate"),
                         (["x", "-m", "gpt", "-e", "a.png", "--mask", "m.png"], "edit")):
        (name, params), = run(argv, result=response(2))
        assert name == method
        assert set(params) <= set(inspect.signature(getattr(client.images, method)).parameters)


@pytest.mark.parametrize("model,cost", [("gpt-image-1.5", "$0.195"), ("chatgpt-image-latest", "$0.195"),
                                        ("gpt-image-2", "$0.183")])
def test_cost_for_priced_models(run, capsys, model, cost):
    run(["x", "-m", model])
    assert f"≈ {cost}" in capsys.readouterr().out


def test_unknown_openai_model_shows_tokens_without_cost(run, capsys):
    run(["x", "-m", "gpt-image-9"])
    out = capsys.readouterr().out
    assert "6,400 tokens" in out and "cost unknown for gpt-image-9" in out
