#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["google-genai>=2.3,<3"]
# ///
"""Generate and edit images with Google's Nano Banana models (Gemini API).

Uses the Interactions API, Google's recommended interface for image models.
Run with `uv run generate_image.py ...` (installs dependencies automatically)
or with `python3` after `pip install -U "google-genai>=2.3,<3"`.

Prompting: send a rich narrative description of the scene. An optional JSON
wrapper carries script parameters in a "config" key; everything else in the
wrapper is sent to the model.

Usage:
    generate_image.py "narrative prompt" [options]
    generate_image.py '{"prompt": "...", "config": {"model": "pro", "output": "hero.png"}}'

Config keys (JSON) / CLI flags:
    model         -m  nb (default) | nb2 | pro | lite | full model ID
    output        -o  Output path; .png, .jpg/.jpeg (default: generated_image.png)
    size          -s  512 | 1K | 2K | 4K
    aspect_ratio  -a  e.g. 1:1, 16:9, 9:16, 21:9
    edit          -e  Input/reference image path(s); repeat the flag for several
    search            Ground on Google Search (web + image where supported)
    thinking          minimal | low | medium | high
    continue          Interaction ID to refine (multi-turn editing)

Environment:
    GEMINI_API_KEY (or GOOGLE_API_KEY), read from the environment, then ./.env,
    ./.claude/.env, then ~/.claude/.env.
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

# Aliases for the current Nano Banana models (verified against ai.google.dev, Oct 2026).
MODELS = {
    "nb": "gemini-nano-banana-2.1",        # Nano Banana 2.1: default, best quality per dollar
    "nb2": "gemini-3.1-flash-image",       # Nano Banana 2: only model with 512px output
    "pro": "gemini-3-pro-image",           # Nano Banana Pro: best text rendering, style references
    "lite": "gemini-3.1-flash-lite-image",  # Nano Banana 2 Lite: cheapest, 1K only, no grounding
}
DEFAULT_MODEL = "nb"

BASE_RATIOS = {"1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"}
EXTREME_RATIOS = {"1:4", "4:1", "1:8", "8:1"}

# Per-model limits from the image-generation docs. Unknown model IDs skip validation.
CAPABILITIES = {
    "gemini-nano-banana-2.1": {
        "sizes": {"1K", "2K", "4K"},
        "ratios": BASE_RATIOS | EXTREME_RATIOS,
        "search": ["web_search", "image_search"],
        "thinking": {"minimal", "medium", "high"},
    },
    "gemini-3.1-flash-image": {
        "sizes": {"512", "1K", "2K", "4K"},
        "ratios": BASE_RATIOS | EXTREME_RATIOS,
        "search": ["web_search", "image_search"],
        "thinking": {"minimal", "high"},
    },
    "gemini-3-pro-image": {
        "sizes": {"1K", "2K", "4K"},
        "ratios": BASE_RATIOS,
        "search": ["web_search"],
        "thinking": set(),
    },
    "gemini-3.1-flash-lite-image": {
        "sizes": {"1K"},
        "ratios": BASE_RATIOS,
        "search": [],
        "thinking": {"minimal", "high"},
    },
}

MAX_REFERENCE_IMAGES = 14
OUTPUT_MIME_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}
EXTENSION_FOR_MIME = {"image/png": ".png", "image/jpeg": ".jpg"}
RETRYABLE_STATUS = {429, 500, 502, 503, 504}
RETRY_DELAYS = (10, 30)


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
    parser = argparse.ArgumentParser(description="Generate and edit images with Nano Banana models.")
    parser.add_argument("prompt", help="Narrative prompt, or a JSON wrapper with a 'config' key (use - to read it from stdin)")
    parser.add_argument("-m", "--model", help="nb (default), nb2, pro, lite, or a full model ID")
    parser.add_argument("-o", "--output", help="Output path (.png, .jpg, .jpeg)")
    parser.add_argument("-s", "--size", help="512, 1K, 2K, or 4K")
    parser.add_argument("-a", "--aspect", help="Aspect ratio, e.g. 16:9")
    parser.add_argument("-e", "--edit", action="append", help="Input image (repeatable)")
    parser.add_argument("--search", action="store_true", help="Ground on Google Search")
    parser.add_argument("--thinking", help="minimal, low, medium, or high")
    parser.add_argument("--continue", dest="continue_id", metavar="INTERACTION_ID",
                        help="Refine the result of a previous interaction")
    return parser.parse_args()


def split_prompt(raw: str) -> tuple[str, dict]:
    """Return (prompt text, config) from plain text or a JSON wrapper.

    A wrapper holding only "prompt" (plus "config") unwraps to that text; any
    other keys are serialized back to JSON and sent as a structured prompt.
    """
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
    """Merge JSON config over CLI flags and normalize values."""
    def pick(key, flag):
        return config[key] if config.get(key) is not None else flag

    edits = pick("edit", args.edit) or []
    if isinstance(edits, str):
        edits = [edits]
    size = pick("size", args.size)
    model_name = pick("model", args.model) or DEFAULT_MODEL
    return {
        "model": MODELS.get(model_name, model_name),
        "output": pick("output", args.output) or "generated_image.png",
        "size": str(size).upper() if size is not None else None,
        "aspect": pick("aspect_ratio", args.aspect),
        "edits": [str(e) for e in edits],
        "search": bool(pick("search", args.search)),
        "thinking": pick("thinking", args.thinking),
        "continue_id": pick("continue", args.continue_id),
    }


def validate(settings: dict) -> None:
    """Catch unsupported combinations before spending an API call."""
    if len(settings["edits"]) > MAX_REFERENCE_IMAGES:
        sys.exit(f"Error: at most {MAX_REFERENCE_IMAGES} input images are supported.")
    for path in settings["edits"]:
        if not pathlib.Path(path).is_file():
            sys.exit(f"Error: input image not found: {path}")

    caps = CAPABILITIES.get(settings["model"])
    if caps is None:
        return
    model = settings["model"]
    if settings["size"] and settings["size"] not in caps["sizes"]:
        sys.exit(f"Error: {model} supports sizes {sorted(caps['sizes'])}, not {settings['size']}.")
    if settings["aspect"] and settings["aspect"] not in caps["ratios"]:
        sys.exit(f"Error: {model} does not support aspect ratio {settings['aspect']}. "
                 f"Supported: {', '.join(sorted(caps['ratios']))}.")
    if settings["search"] and not caps["search"]:
        sys.exit(f"Error: {model} does not support search grounding. Use -m nb or -m pro.")
    if settings["thinking"] and settings["thinking"] not in caps["thinking"]:
        supported = sorted(caps["thinking"]) or ["none (thinking is fixed for this model)"]
        sys.exit(f"Error: {model} thinking levels: {', '.join(supported)}.")


def output_format(output: str) -> tuple[pathlib.Path, str]:
    path = pathlib.Path(output).expanduser()
    mime = OUTPUT_MIME_TYPES.get(path.suffix.lower())
    if mime is None:
        sys.exit(f"Error: unsupported output extension '{path.suffix}'. Use .png, .jpg, or .jpeg.")
    return path, mime


def unique_path(path: pathlib.Path) -> pathlib.Path:
    """Avoid overwriting an existing file by appending -1, -2, ... to the stem."""
    candidate, n = path, 1
    while candidate.exists():
        candidate = path.with_name(f"{path.stem}-{n}{path.suffix}")
        n += 1
    return candidate


def image_block(path: str) -> dict:
    mime = mimetypes.guess_type(path)[0] or "image/png"
    data = pathlib.Path(path).read_bytes()
    return {"type": "image", "mime_type": mime, "data": base64.b64encode(data).decode("ascii")}


def build_request(settings: dict, prompt: str, mime: str) -> dict:
    if settings["edits"]:
        content = [image_block(p) for p in settings["edits"]]
        content.append({"type": "text", "text": prompt})
    else:
        content = prompt

    response_format = {"type": "image", "mime_type": mime}
    if settings["aspect"]:
        response_format["aspect_ratio"] = settings["aspect"]
    if settings["size"]:
        response_format["image_size"] = settings["size"]

    request = {"model": settings["model"], "input": content, "response_format": response_format}
    if settings["thinking"]:
        request["generation_config"] = {"thinking_level": settings["thinking"]}
    if settings["continue_id"]:
        request["previous_interaction_id"] = settings["continue_id"]
    if settings["search"]:
        tool = {"type": "google_search"}
        caps = CAPABILITIES.get(settings["model"])
        if caps and "image_search" in caps["search"]:
            tool["search_types"] = caps["search"]  # web search alone is the API default
        request["tools"] = [tool]
    return request


def status_code(error: Exception) -> int | None:
    code = getattr(error, "status_code", None) or getattr(error, "code", None)
    return code if isinstance(code, int) else None


def create_interaction(client, request: dict):
    for attempt in range(len(RETRY_DELAYS) + 1):
        try:
            return client.interactions.create(**request)
        except Exception as error:  # SDK raises several unrelated error hierarchies
            code = status_code(error)
            if code in RETRYABLE_STATUS and attempt < len(RETRY_DELAYS):
                delay = RETRY_DELAYS[attempt]
                print(f"HTTP {code}; retrying in {delay}s...", file=sys.stderr)
                time.sleep(delay)
                continue
            hint = {
                400: "Check the prompt and parameters; safety blocks also return 400.",
                401: "The API key is invalid.",
                403: "The API key lacks access to this model, or the region is unsupported.",
                404: "Unknown model ID. Check the model name.",
                429: "Rate limit or quota exceeded. Wait and retry, or check billing.",
            }.get(code, "")
            sys.exit(f"Error: {error}\n{hint}".rstrip())


def final_image(interaction):
    """Return the final rendered image block, skipping interim thought images."""
    if getattr(interaction, "output_image", None) and interaction.output_image.data:
        return interaction.output_image
    image = None
    for step in getattr(interaction, "steps", None) or []:
        if getattr(step, "type", None) != "model_output":
            continue
        for block in getattr(step, "content", None) or []:
            if getattr(block, "type", None) == "image" and getattr(block, "data", None):
                image = block
    return image


def search_suggestions(interaction) -> list[str]:
    html = []
    for step in getattr(interaction, "steps", None) or []:
        for result in getattr(step, "result", None) or []:
            snippet = getattr(result, "search_suggestions", None)
            if snippet:
                html.append(snippet)
    return html


def main() -> None:
    args = parse_args()
    prompt, config = split_prompt(sys.stdin.read().strip() if args.prompt == "-" else args.prompt)
    if not prompt.strip():
        sys.exit("Error: the prompt is empty.")
    settings = resolve_settings(args, config)
    validate(settings)
    requested_path, mime = output_format(settings["output"])

    client = genai.Client(api_key=load_api_key())
    if not hasattr(client, "interactions"):
        sys.exit('Error: google-genai is too old. Upgrade with: pip install -U "google-genai>=2.3,<3"')

    details = [f"model={settings['model']}"]
    for label, key in (("size", "size"), ("aspect", "aspect"), ("thinking", "thinking")):
        if settings[key]:
            details.append(f"{label}={settings[key]}")
    if settings["edits"]:
        details.append(f"inputs={len(settings['edits'])}")
    if settings["search"]:
        details.append("search=on")
    if settings["continue_id"]:
        details.append(f"continue={settings['continue_id']}")
    print("Generating: " + ", ".join(details), file=sys.stderr)

    interaction = create_interaction(client, build_request(settings, prompt, mime))

    if getattr(interaction, "output_text", None):
        print(interaction.output_text)
    image = final_image(interaction)
    if image is None:
        status = getattr(interaction, "status", "unknown")
        errors = "; ".join(getattr(e, "message", str(e)) for e in getattr(interaction, "errors", None) or [])
        sys.exit(f"No image was returned (status: {status}). {errors}".strip() +
                 "\nThe prompt may have been blocked by safety filters; rephrase and retry.")

    returned_mime = getattr(image, "mime_type", None) or mime
    path = requested_path
    if returned_mime != mime and returned_mime in EXTENSION_FOR_MIME:
        path = path.with_suffix(EXTENSION_FOR_MIME[returned_mime])
        print(f"Note: model returned {returned_mime}; saving as {path.suffix}.", file=sys.stderr)
    path = unique_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(image.data))
    print(f"Image saved: {path}")

    suggestions = search_suggestions(interaction)
    if suggestions:
        sources = path.with_name(path.stem + ".search.html")
        sources.write_text("\n".join(suggestions))
        print(f"Search suggestions (show these to the user): {sources}")

    if getattr(interaction, "id", None):
        print(f"Interaction ID: {interaction.id}  (pass --continue {interaction.id} to refine)")


if __name__ == "__main__":
    main()
