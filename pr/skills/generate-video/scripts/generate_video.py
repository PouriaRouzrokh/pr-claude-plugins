#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["google-genai>=2.3,<3"]
# ///
# Pins verified against PyPI on 2026-10-30: google-genai 2.34.0.
"""Generate, edit, and extend videos with Gemini Omni Flash (Gemini API).

Uses the Interactions API. Generation is synchronous and can take several
minutes, so run it in the background or with a long timeout.

Run with `uv run generate_video.py ...` (installs dependencies automatically)
or with `python3` after `pip install -U "google-genai>=2.3,<3"`.

Usage:
    generate_video.py "narrative prompt" [options]
    generate_video.py '{"prompt": "...", "config": {"aspect_ratio": "9:16", "output": "clip.mp4"}}'

Config keys (JSON) / CLI flags:
    model         -m  omni (default) | full model ID
    output        -o  Output .mp4 path (default: generated_video.mp4)
    aspect_ratio  -a  16:9 (default) | 9:16
    resolution    -r  360p | 720p (default) | 1080p | 4k (1080p and 4k are upscaled)
    image         -i  Image input(s): first frame, first+last frame, or references (repeatable)
    video         -v  Video to edit or extend (uploaded via the Files API; 10 s max)
    task              text_to_video | image_to_video | reference_to_video | edit | extend
    continue          Interaction ID of a previous video to edit or extend
    timeout           Seconds to wait for generation (default: 900)

Environment:
    GEMINI_API_KEY (or GOOGLE_API_KEY), read from the environment, then ./.env,
    ./.claude/.env, then ~/.claude/.env. Omni Flash requires a paid-tier key.
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import pathlib
import sys
import time

if sys.version_info < (3, 10):
    sys.exit(
        "Error: Python 3.10+ is required (found %d.%d). Run this script with "
        "`uv run`, which provisions a suitable Python automatically." % sys.version_info[:2]
    )

try:
    from google import genai
except ImportError:
    sys.exit(
        "Error: google-genai is not installed. Run with `uv run`, or install it with:\n"
        '  python3 -m pip install -U "google-genai>=2.3,<3"'
    )

# Current video model (verified against ai.google.dev, Oct 2026). Veo 3.1 previews shut down 2026-10-22.
MODELS = {"omni": "gemini-omni-1.1-flash"}
DEFAULT_MODEL = "omni"
ASPECT_RATIOS = {"16:9", "9:16"}
RESOLUTIONS = {"360p", "720p", "1080p", "4k"}
URI_DELIVERY = {"1080p", "4k"}  # large outputs exceed the 4 MB inline limit
TASKS = {"text_to_video", "image_to_video", "reference_to_video", "edit", "extend"}
# Only 429 and 503 are retried: they mean the request was rejected before generation started.
# A 500/502/504 can arrive after the server has already rendered (and billed) the clip, so a
# blind retry could pay twice.
RETRYABLE_STATUS = {429, 503}
# Source: ai.google.dev/gemini-api/docs/pricing, checked 2026-10-30: about $0.10 per second of
# 720p output for gemini-omni-1.1-flash. The page lists no other rate, so the estimate uses it
# for every resolution.
PRICE_PER_SECOND = {"gemini-omni-1.1-flash": 0.10}
RETRY_DELAYS = (15, 45)
POLL_SECONDS = 5


def load_env_file(path: pathlib.Path) -> None:
    """Load KEY=VALUE lines into os.environ without overriding existing values."""
    try:
        lines = path.read_text().splitlines()
    except (FileNotFoundError, IsADirectoryError, PermissionError):
        return
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.removeprefix("export ").partition("=")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        os.environ.setdefault(key.strip(), value)


def load_api_key() -> str:
    for path in (
        pathlib.Path.cwd() / ".env",
        pathlib.Path.cwd() / ".claude" / ".env",
        pathlib.Path.home() / ".claude" / ".env",
    ):
        if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
            break
        load_env_file(path)
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        sys.exit(
            "Error: GEMINI_API_KEY not found in the environment, ./.env, ./.claude/.env, "
            "or ~/.claude/.env. Get a key at https://aistudio.google.com/apikey."
        )
    return key


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate, edit, and extend videos with Gemini Omni Flash.")
    parser.add_argument("prompt", help="Narrative prompt, or a JSON wrapper with a 'config' key (use - to read it from stdin)")
    parser.add_argument("-m", "--model", help="omni (default) or a full model ID")
    parser.add_argument("-o", "--output", help="Output .mp4 path")
    parser.add_argument("-a", "--aspect", help="16:9 or 9:16")
    parser.add_argument("-r", "--resolution", help="360p, 720p, 1080p, or 4k")
    parser.add_argument("-i", "--image", action="append", help="Image input (repeatable)")
    parser.add_argument("-v", "--video", help="Video to edit or extend (10 s max)")
    parser.add_argument("--task", help="Explicit task mode")
    parser.add_argument("--continue", dest="continue_id", metavar="INTERACTION_ID",
                        help="Edit or extend the video from a previous interaction")
    parser.add_argument("--timeout", type=int, help="Seconds to wait (default: 900)")
    return parser.parse_args()


def split_prompt(raw: str) -> tuple[str, dict]:
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return raw, {}
    if not isinstance(data, dict):
        return raw, {}
    config = data.pop("config", None) or {}
    if not isinstance(config, dict):
        sys.exit("Error: 'config' must be a JSON object.")
    if set(data) <= {"prompt"}:
        return str(data.get("prompt", "")), config
    return json.dumps(data), config


def resolve_settings(args: argparse.Namespace, config: dict) -> dict:
    def pick(key, flag):
        return config[key] if config.get(key) is not None else flag

    images = pick("image", args.image) or []
    if isinstance(images, str):
        images = [images]
    model_name = pick("model", args.model) or DEFAULT_MODEL
    resolution = pick("resolution", args.resolution)
    settings = {
        "model": MODELS.get(model_name, model_name),
        "output": pick("output", args.output) or "generated_video.mp4",
        "aspect": pick("aspect_ratio", args.aspect),
        "resolution": str(resolution).lower() if resolution else None,
        "images": [str(i) for i in images],
        "video": pick("video", args.video),
        "task": pick("task", args.task),
        "continue_id": pick("continue", args.continue_id),
        "timeout": int(pick("timeout", args.timeout) or 900),
    }
    if settings["aspect"] and settings["aspect"] not in ASPECT_RATIOS:
        sys.exit(f"Error: aspect ratio must be one of {sorted(ASPECT_RATIOS)}.")
    if settings["resolution"] and settings["resolution"] not in RESOLUTIONS:
        sys.exit(f"Error: resolution must be one of {sorted(RESOLUTIONS)}.")
    if settings["task"] and settings["task"] not in TASKS:
        sys.exit(f"Error: task must be one of {sorted(TASKS)}.")
    for path in settings["images"] + ([settings["video"]] if settings["video"] else []):
        if not pathlib.Path(path).is_file():
            sys.exit(f"Error: input file not found: {path}")
    if pathlib.Path(settings["output"]).suffix.lower() != ".mp4":
        sys.exit("Error: output path must end in .mp4")
    return settings


def unique_path(path: pathlib.Path) -> pathlib.Path:
    candidate, n = path, 1
    while candidate.exists():
        candidate = path.with_name(f"{path.stem}-{n}{path.suffix}")
        n += 1
    return candidate


def state_name(file) -> str:
    state = getattr(file, "state", None)
    return str(getattr(state, "name", state) or "").upper()


def wait_for_file(client, name: str, deadline: float):
    while True:
        file = client.files.get(name=name)
        state = state_name(file)
        if state == "ACTIVE":
            return file
        if state == "FAILED":
            sys.exit(f"Error: file processing failed for {name}.")
        if time.time() > deadline:
            sys.exit(f"Error: timed out waiting for {name} to become ACTIVE.")
        time.sleep(POLL_SECONDS)


def upload_video(client, path: str, deadline: float) -> dict:
    print(f"Uploading {path}...", file=sys.stderr)
    file = client.files.upload(file=path)
    file = wait_for_file(client, file.name, deadline)
    return {"type": "video", "uri": file.uri, "mime_type": getattr(file, "mime_type", None) or "video/mp4"}


def image_block(path: str) -> dict:
    mime = mimetypes.guess_type(path)[0] or "image/png"
    data = base64.b64encode(pathlib.Path(path).read_bytes()).decode("ascii")
    return {"type": "image", "mime_type": mime, "data": data}


def build_request(settings: dict, prompt: str, video_block: dict | None) -> dict:
    media = ([video_block] if video_block else []) + [image_block(p) for p in settings["images"]]
    content = media + [{"type": "text", "text": prompt}] if media else prompt

    response_format = {"type": "video"}
    if settings["aspect"]:
        response_format["aspect_ratio"] = settings["aspect"]
    if settings["resolution"]:
        response_format["resolution"] = settings["resolution"]
        if settings["resolution"] in URI_DELIVERY:
            response_format["delivery"] = "uri"

    request = {"model": settings["model"], "input": content, "response_format": response_format}
    if settings["task"]:
        request["generation_config"] = {"video_config": {"task": settings["task"]}}
    if settings["continue_id"]:
        request["previous_interaction_id"] = settings["continue_id"]
    return request


def status_code(error: Exception) -> int | None:
    code = getattr(error, "status_code", None) or getattr(error, "code", None)
    return code if isinstance(code, int) else None


def create_interaction(client, request: dict, timeout: int):
    for attempt in range(len(RETRY_DELAYS) + 1):
        try:
            return client.interactions.create(**request, timeout=timeout)
        except Exception as error:  # SDK raises several unrelated error hierarchies
            code = status_code(error)
            if code in RETRYABLE_STATUS and attempt < len(RETRY_DELAYS):
                delay = RETRY_DELAYS[attempt]
                print(f"HTTP {code}; retrying in {delay}s...", file=sys.stderr)
                time.sleep(delay)
                continue
            hint = {
                400: "Check the prompt and inputs; safety blocks and unsupported regions also return 400.",
                403: "Omni Flash needs a paid-tier key, and video editing is unavailable in the EEA, UK, and Switzerland.",
                429: "Rate limit or quota exceeded. Wait and retry, or check billing.",
                500: "Server error, not retried automatically: the clip may already have been generated and billed. Check your usage before retrying.",
                502: "Server error, not retried automatically: the clip may already have been generated and billed. Check your usage before retrying.",
                504: "Gateway timeout, not retried automatically: the clip may already have been generated and billed. Check your usage before retrying.",
            }.get(code, "")
            sys.exit(f"Error: {error}\n{hint}".rstrip())


def video_seconds(path: pathlib.Path) -> float | None:
    """Clip length from the MP4 movie header (mvhd box), or None when it cannot be read."""
    try:
        data = path.read_bytes()
        i = data.find(b"mvhd")
        if i < 0:
            return None
        version = data[i + 4]
        offset = i + 4 + (20 if version == 1 else 12)
        timescale = int.from_bytes(data[offset:offset + 4], "big")
        size = 8 if version == 1 else 4
        duration = int.from_bytes(data[offset + 4:offset + 4 + size], "big")
        return duration / timescale if timescale else None
    except (OSError, IndexError):
        return None


def cost_line(model: str, path: pathlib.Path) -> str | None:
    rate = PRICE_PER_SECOND.get(model)
    seconds = video_seconds(path)
    if rate is None or not seconds:
        return None
    return f"Estimated cost: about ${rate * seconds:.2f} ({seconds:.0f} s at ${rate:.2f}/s, 720p rate)"


def save_video(client, video, path: pathlib.Path, deadline: float) -> None:
    if getattr(video, "data", None):
        path.write_bytes(base64.b64decode(video.data))
        return
    uri = getattr(video, "uri", None)
    if not uri:
        sys.exit("Error: the response contained no video data or URI.")
    wait_for_file(client, "files/" + uri.rstrip("/").split("/")[-1], deadline)
    data = client.files.download(file=uri)
    path.write_bytes(data)


def main() -> None:
    args = parse_args()
    prompt, config = split_prompt(sys.stdin.read().strip() if args.prompt == "-" else args.prompt)
    if not prompt.strip():
        sys.exit("Error: the prompt is empty.")
    settings = resolve_settings(args, config)
    deadline = time.time() + settings["timeout"]

    client = genai.Client(api_key=load_api_key())
    if not hasattr(client, "interactions"):
        sys.exit('Error: google-genai is too old. Upgrade with: pip install -U "google-genai>=2.3,<3"')

    video_block = upload_video(client, settings["video"], deadline) if settings["video"] else None
    details = [f"model={settings['model']}"]
    for key in ("aspect", "resolution", "task"):
        if settings[key]:
            details.append(f"{key}={settings[key]}")
    if settings["images"]:
        details.append(f"images={len(settings['images'])}")
    if settings["continue_id"]:
        details.append(f"continue={settings['continue_id']}")
    print("Generating video (this can take several minutes): " + ", ".join(details), file=sys.stderr)

    started = time.time()
    interaction = create_interaction(client, build_request(settings, prompt, video_block), settings["timeout"])

    if getattr(interaction, "output_text", None):
        print(interaction.output_text)
    video = getattr(interaction, "output_video", None)
    if video is None:
        status = getattr(interaction, "status", "unknown")
        errors = "; ".join(getattr(e, "message", str(e)) for e in getattr(interaction, "errors", None) or [])
        sys.exit(f"No video was returned (status: {status}). {errors}".strip() +
                 "\nThe prompt may have been blocked by safety filters; rephrase and retry.")

    path = unique_path(pathlib.Path(settings["output"]).expanduser())
    path.parent.mkdir(parents=True, exist_ok=True)
    save_video(client, video, path, deadline)
    print(f"Video saved: {path} ({path.stat().st_size / 1e6:.1f} MB, {time.time() - started:.0f}s)")
    estimate = cost_line(settings["model"], path)
    if estimate:
        print(estimate)
    if getattr(interaction, "id", None):
        print(f"Interaction ID: {interaction.id}  (pass --continue {interaction.id} to edit or extend)")


if __name__ == "__main__":
    main()
