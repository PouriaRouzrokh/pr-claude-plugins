"""Offline tests for generate_video.py with a fake client."""
import base64, importlib.util, os, pathlib, sys, types
import pytest

from conftest import SKILLS

SCRIPT = SKILLS / "generate-video/scripts/generate_video.py"
MP4 = base64.b64encode(b"MP4DATA").decode()
ns = types.SimpleNamespace

def load():
    spec = importlib.util.spec_from_file_location("generate_video", SCRIPT)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

class FakeClient:
    def __init__(self, response):
        self.calls, self.files_get, self.response = [], [], response
        outer = self
        class I:
            def create(self, **req): outer.calls.append(req); return outer.response
        class F:
            def upload(self, file): return ns(name="files/up1", state=ns(name="PROCESSING"))
            def get(self, name):
                outer.files_get.append(name)
                return ns(name=name, state=ns(name="ACTIVE"), uri="https://g/files/up1", mime_type="video/mp4")
            def download(self, file): return b"URIDATA"
        self.interactions, self.files = I(), F()

@pytest.fixture
def run(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path); monkeypatch.setenv("GEMINI_API_KEY", "k")
    def _run(argv, response=None):
        m = load()
        fake = FakeClient(response or ns(id="v1", status="completed", output_text=None,
                                          output_video=ns(data=MP4, uri=None), errors=None))
        monkeypatch.setattr(m.genai, "Client", lambda api_key: fake)
        monkeypatch.setattr(m.time, "sleep", lambda s: None)
        monkeypatch.setattr(sys, "argv", ["generate_video.py", *argv])
        m.main(); return fake
    return _run

def test_text_to_video(run, tmp_path, capsys):
    f = run(["A marble on a track", "-a", "9:16"])
    req = f.calls[0]
    assert req["model"] == "gemini-omni-1.1-flash" and req["input"] == "A marble on a track"
    assert req["response_format"] == {"type": "video", "aspect_ratio": "9:16"}
    assert req["timeout"] == 900
    assert (tmp_path / "generated_video.mp4").read_bytes() == b"MP4DATA"
    assert "Interaction ID: v1" in capsys.readouterr().out

def test_frames_task_and_validation_against_sdk(run, tmp_path):
    (tmp_path / "first.jpg").write_bytes(b"1"); (tmp_path / "last.png").write_bytes(b"2")
    f = run(["Transition", "-i", "first.jpg", "-i", "last.png", "--task", "image_to_video", "-r", "720p", "--continue", "prev"])
    req = dict(f.calls[0]); req.pop("timeout")
    assert [b["type"] for b in req["input"]] == ["image", "image", "text"]
    assert req["generation_config"] == {"video_config": {"task": "image_to_video"}}
    from google.genai._gaos.types.interactions.createmodelinteraction import CreateModelInteraction
    CreateModelInteraction.model_validate(req)

def test_upload_and_uri_delivery(run, tmp_path):
    (tmp_path / "in.mp4").write_bytes(b"v")
    resp = ns(id="v2", status="completed", output_text=None, output_video=ns(data=None, uri="https://g/files/abc"), errors=None)
    f = run(["Make it rain", "-v", "in.mp4", "-r", "1080p", "-o", "out/rain.mp4"], response=resp)
    req = f.calls[0]
    assert req["input"][0] == {"type": "video", "uri": "https://g/files/up1", "mime_type": "video/mp4"}
    assert req["response_format"]["delivery"] == "uri"
    assert "files/abc" in f.files_get
    assert (tmp_path / "out" / "rain.mp4").read_bytes() == b"URIDATA"

@pytest.mark.parametrize("argv,msg", [
    (["x", "-a", "1:1"], "aspect ratio"), (["x", "-r", "8k"], "resolution"),
    (["x", "--task", "dance"], "task must be"), (["x", "-i", "nope.png"], "not found"),
    (["x", "-o", "a.mov"], ".mp4"),
])
def test_validation(run, argv, msg):
    with pytest.raises(SystemExit) as e: run(argv)
    assert msg in str(e.value)

def test_no_video(run):
    with pytest.raises(SystemExit) as e:
        run(["x"], response=ns(id="v", status="failed", output_text=None, output_video=None, errors=[ns(message="unsafe")]))
    assert "status: failed" in str(e.value) and "unsafe" in str(e.value)
