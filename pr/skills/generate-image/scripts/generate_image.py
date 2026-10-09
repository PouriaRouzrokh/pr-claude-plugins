#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["google-genai>=2.3,<3", "openai>=2,<4"]
# ///
"""Generate and edit images with Google Nano Banana or OpenAI GPT Image models.

One interface, two providers, chosen by model alias:
  Google (Interactions API): nb (default), pro, nb2, lite
  OpenAI (Images API):       gpt (GPT Image 2.5 Sunburst), gpt-fast (GPT Image 2.5 Flare)

Run with `uv run generate_image.py ...` (installs dependencies automatically)
or with `python3` after `pip install -U "google-genai>=2.3,<3" "openai>=2,<4"`.

Prompting: send a rich narrative description of the scene. An optional JSON
wrapper carries script parameters in a "config" key; everything else in the
wrapper is sent to the model.

Usage:
    generate_image.py "narrative prompt" [options]
    generate_image.py - [options] < prompt.txt
    generate_image.py '{"prompt": "...", "config": {"model": "gpt", "background": "transparent"}}'

Config keys (JSON) / CLI flags:
    model         -m  nb (default) | pro | nb2 | lite | gpt | gpt-fast | full model ID
    output        -o  Output path: .png, .jpg/.jpeg (.webp for GPT models)
    size          -s  Google: 512 | 1K | 2K | 4K.  GPT: 1K | 2K | 4K | auto | WIDTHxHEIGHT
    aspect_ratio  -a  e.g. 1:1, 16:9, 9:16, 21:9
    edit          -e  Input/reference image path(s); repeat the flag for several
    search            Google Search grounding (Google models)
    thinking          minimal | low | medium | high (Google models)
    continue          Interaction ID to refine (Google models)
    quality           low | medium | high | xhigh | max | auto (GPT models)
    background        transparent | opaque | auto (GPT models)
    mask              PNG with alpha marking the area of the first input to repaint (GPT models)
    n             -n  Number of variations, 1-10 (GPT models)

Environment:
    Google: GEMINI_API_KEY (or GOOGLE_API_KEY).  OpenAI: OPENAI_API_KEY.
    Read from the environment, then ./.env, ./.claude/.env, then ~/.claude/.env.
"""

from __future__ import annotations

import argparse
import base64
import json
import math
import mimetypes
import os
import pathlib
import re
import sys
import time

if sys.version_info < (3, 10):
    sys.exit(
        "Error: Python 3.10+ is required (found %d.%d). Run this script with "
        "`uv run`, which provisions a suitable Python automatically." % sys.version_info[:2]
    )

# Each provider's SDK is imported optionally so either works without the other.
try:
    from google import genai
except ImportError:
    genai = None
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# Model aliases (verified against ai.google.dev and developers.openai.com, Oct 2026).
MODELS = {
    "nb": "gemini-nano-banana-2.1",          # Nano Banana 2.1: default, best quality per dollar
    "pro": "gemini-3-pro-image",             # Nano Banana Pro: dense text, style references
    "nb2": "gemini-3.1-flash-image",         # Nano Banana 2: only model with 512px output
    "lite": "gemini-3.1-flash-lite-image",   # Nano Banana 2 Lite: cheapest, 1K only
    "gpt": "gpt-image-2.5-sunburst",         # GPT Image 2.5 Sunburst: OpenAI's most capable
    "chatgpt": "gpt-image-2.5-sunburst",
    "gpt-fast": "gpt-image-2.5-flare",       # GPT Image 2.5 Flare: fastest high-quality
}
DEFAULT_MODEL = "nb"

BASE_RATIOS = {"1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"}
EXTREME_RATIOS = {"1:4", "4:1", "1:8", "8:1"}

# Per-model limits for Google models. Unknown model IDs skip validation.
GEMINI_CAPABILITIES = {
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

# OpenAI: target pixel areas for size presets and the documented size constraints.
GPT_AREAS = {"1K": 1536 * 1024, "2K": 2560 * 1440, "4K": 3840 * 2160}
GPT_STANDARD_SIZES = {"1:1": "1024x1024", "3:2": "1536x1024", "2:3": "1024x1536"}
GPT_MIN_PIXELS, GPT_MAX_PIXELS, GPT_MAX_EDGE = 655_360, 8_294_400, 3840
GPT_QUALITIES = {"low", "medium", "high", "xhigh", "max", "auto"}
GPT_BASIC_QUALITIES = {"low", "medium", "high", "auto"}
GPT_25_MODELS = {"gpt-image-2.5-sunburst", "gpt-image-2.5-flare"}
# USD per 1M tokens: (text input, image input, image output), standard processing.
GPT_PRICES = {
    "gpt-image-2.5-sunburst": (5.0, 8.0, 30.0),
    "gpt-image-2.5-flare": (5.0, 8.0, 30.0),
    "gpt-image-2": (5.0, 8.0, 30.0),
}

MAX_INPUTS = {"google": 14, "openai": 16}
OUTPUT_MIME_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
EXTENSION_FOR_MIME = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp"}
RETRYABLE_STATUS = {429, 500, 502, 503, 504}
RETRY_DELAYS = (10, 30)
HINTS = {
    400: "Check the prompt and parameters; safety blocks also return 400.",
    401: "The API key is invalid.",
    403: "The key lacks access to this model (OpenAI may require organization verification), "
         "or the region is unsupported.",
    404: "Unknown model ID. Check the model name.",
    429: "Rate limit or quota exceeded. Wait and retry, or check billing.",
}


def provider_for(model: str) -> str:
    return "openai" if model.startswith(("gpt-image", "chatgpt-image")) else "google"


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


def load_api_key(names: tuple[str, ...] = ("GEMINI_API_KEY", "GOOGLE_API_KEY")) -> str:
    def found() -> str | None:
        return next((os.environ[n] for n in names if os.environ.get(n)), None)

    for path in (
        pathlib.Path.cwd() / ".env",
        pathlib.Path.cwd() / ".claude" / ".env",
        pathlib.Path.home() / ".claude" / ".env",
    ):
        if found():
            break
        load_env_file(path)
    key = found()
    if not key:
        where = ("https://platform.openai.com/api-keys" if "OPENAI_API_KEY" in names
                 else "https://aistudio.google.com/apikey")
        sys.exit(f"Error: {names[0]} not found in the environment, ./.env, ./.claude/.env, "
                 f"or ~/.claude/.env. Get a key at {where}.")
    return key


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate and edit images with Nano Banana (Google) or GPT Image (OpenAI) models.")
    parser.add_argument("prompt", help="Narrative prompt, or a JSON wrapper with a 'config' key (use - to read it from stdin)")
    parser.add_argument("-m", "--model", help="nb (default), pro, nb2, lite, gpt, gpt-fast, or a full model ID")
    parser.add_argument("-o", "--output", help="Output path (.png, .jpg, .jpeg; .webp for GPT)")
    parser.add_argument("-s", "--size", help="512, 1K, 2K, 4K; GPT also auto or WIDTHxHEIGHT")
    parser.add_argument("-a", "--aspect", help="Aspect ratio, e.g. 16:9")
    parser.add_argument("-e", "--edit", action="append", help="Input image (repeatable)")
    parser.add_argument("--search", action="store_true", help="Ground on Google Search (Google)")
    parser.add_argument("--thinking", help="minimal, low, medium, or high (Google)")
    parser.add_argument("--continue", dest="continue_id", metavar="INTERACTION_ID",
                        help="Refine the result of a previous interaction (Google)")
    parser.add_argument("--quality", help="low, medium, high, xhigh, max, or auto (GPT)")
    parser.add_argument("--background", help="transparent, opaque, or auto (GPT)")
    parser.add_argument("--mask", help="PNG mask with alpha; transparent areas get repainted (GPT)")
    parser.add_argument("-n", type=int, help="Number of variations, 1-10 (GPT)")
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
    model = MODELS.get(model_name, model_name)
    return {
        "model": model,
        "provider": provider_for(model),
        "output": pick("output", args.output) or "generated_image.png",
        "size": str(size).upper() if size is not None else None,
        "aspect": pick("aspect_ratio", args.aspect),
        "edits": [str(e) for e in edits],
        "search": bool(pick("search", args.search)),
        "thinking": pick("thinking", args.thinking),
        "continue_id": pick("continue", args.continue_id),
        "quality": pick("quality", args.quality),
        "background": pick("background", args.background),
        "mask": pick("mask", args.mask),
        "n": int(pick("n", args.n) or 1),
    }


def validate_common(settings: dict) -> None:
    limit = MAX_INPUTS[settings["provider"]]
    if len(settings["edits"]) > limit:
        sys.exit(f"Error: at most {limit} input images are supported for {settings['model']}.")
    for path in settings["edits"] + ([settings["mask"]] if settings["mask"] else []):
        if not pathlib.Path(path).is_file():
            sys.exit(f"Error: input image not found: {path}")


def validate_google(settings: dict) -> None:
    """Catch unsupported combinations before spending an API call."""
    gpt_only = [flag for flag, key in (("--quality", "quality"), ("--background", "background"),
                                       ("--mask", "mask")) if settings[key]]
    if settings["n"] != 1:
        gpt_only.append("-n")
    if gpt_only:
        sys.exit(f"Error: {', '.join(gpt_only)} {'is' if len(gpt_only) == 1 else 'are'} only "
                 "available with GPT models (-m gpt or -m gpt-fast). "
                 "For a transparent background, use -m gpt --background transparent.")

    caps = GEMINI_CAPABILITIES.get(settings["model"])
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


def validate_openai(settings: dict) -> None:
    google_only = [flag for flag, key in (("--search", "search"), ("--thinking", "thinking"),
                                          ("--continue", "continue_id")) if settings[key]]
    if google_only:
        sys.exit(f"Error: {', '.join(google_only)} {'is' if len(google_only) == 1 else 'are'} only "
                 "available with Google models. With GPT models, refine a result by passing it "
                 "back with -e and describing the change.")
    if not 1 <= settings["n"] <= 10:
        sys.exit("Error: -n must be between 1 and 10.")
    if settings["mask"] and not settings["edits"]:
        sys.exit("Error: --mask needs the image to edit, passed with -e.")
    if settings["background"] and settings["background"] not in {"transparent", "opaque", "auto"}:
        sys.exit("Error: --background must be transparent, opaque, or auto.")
    quality = settings["quality"]
    if quality:
        allowed = GPT_QUALITIES if settings["model"] in GPT_25_MODELS else GPT_BASIC_QUALITIES
        if quality not in allowed:
            sys.exit(f"Error: {settings['model']} quality levels: {', '.join(sorted(allowed))}.")


def gpt_size(size: str | None, aspect: str | None) -> str | None:
    """Translate size/aspect flags into an OpenAI WIDTHxHEIGHT string (None = API default)."""
    if size and re.fullmatch(r"\d+X\d+", size):
        width, height = (int(v) for v in size.split("X"))
    elif size == "AUTO":
        return "auto"
    elif size is None and aspect is None:
        return None
    else:
        if size not in (None, *GPT_AREAS):
            sys.exit(f"Error: GPT sizes are 1K, 2K, 4K, auto, or WIDTHxHEIGHT, not {size}.")
        ratio_text = aspect or "1:1"
        if size in (None, "1K") and ratio_text in GPT_STANDARD_SIZES:
            return GPT_STANDARD_SIZES[ratio_text]
        try:
            w, h = (float(v) for v in ratio_text.split(":"))
            ratio = w / h
        except ValueError:
            sys.exit(f"Error: invalid aspect ratio {ratio_text}.")
        area = GPT_AREAS[size or "1K"]
        height = max(16, round(math.sqrt(area / ratio) / 16) * 16)
        width = max(16, round(height * ratio / 16) * 16)
        while width * height > GPT_MAX_PIXELS or max(width, height) > GPT_MAX_EDGE:
            width, height = width - 16 * (width >= height), height - 16 * (height > width)
    if width % 16 or height % 16:
        sys.exit(f"Error: GPT image width and height must be multiples of 16 (got {width}x{height}).")
    if not 1 / 3 <= width / height <= 3:
        sys.exit("Error: GPT image aspect ratio must be between 1:3 and 3:1; use -m nb for wider banners.")
    if not GPT_MIN_PIXELS <= width * height <= GPT_MAX_PIXELS or max(width, height) > GPT_MAX_EDGE:
        sys.exit(f"Error: {width}x{height} is outside GPT limits (655,360 to 8,294,400 pixels, "
                 f"edges up to {GPT_MAX_EDGE}).")
    return f"{width}x{height}"


def output_format(output: str, provider: str) -> tuple[pathlib.Path, str]:
    path = pathlib.Path(output).expanduser()
    mime = OUTPUT_MIME_TYPES.get(path.suffix.lower())
    if mime is None or (mime == "image/webp" and provider == "google"):
        allowed = ".png, .jpg, .jpeg" + (", .webp" if provider == "openai" else "")
        sys.exit(f"Error: unsupported output extension '{path.suffix}'. Use {allowed}.")
    return path, mime


def unique_path(path: pathlib.Path) -> pathlib.Path:
    """Avoid overwriting an existing file by appending -1, -2, ... to the stem."""
    candidate, n = path, 1
    while candidate.exists():
        candidate = path.with_name(f"{path.stem}-{n}{path.suffix}")
        n += 1
    return candidate


def status_code(error: Exception) -> int | None:
    code = getattr(error, "status_code", None) or getattr(error, "code", None)
    return code if isinstance(code, int) else None


def call_with_retries(fn):
    for attempt in range(len(RETRY_DELAYS) + 1):
        try:
            return fn()
        except Exception as error:  # SDKs raise several unrelated error hierarchies
            code = status_code(error)
            if code in RETRYABLE_STATUS and attempt < len(RETRY_DELAYS):
                delay = RETRY_DELAYS[attempt]
                print(f"HTTP {code}; retrying in {delay}s...", file=sys.stderr)
                time.sleep(delay)
                continue
            sys.exit(f"Error: {error}\n{HINTS.get(code, '')}".rstrip())


# --- Google (Nano Banana) -------------------------------------------------------


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
        caps = GEMINI_CAPABILITIES.get(settings["model"])
        if caps and "image_search" in caps["search"]:
            tool["search_types"] = caps["search"]  # web search alone is the API default
        request["tools"] = [tool]
    return request


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


def run_google(settings: dict, prompt: str, mime: str) -> dict:
    if genai is None:
        sys.exit('Error: google-genai is not installed. Use `uv run`, or pip install -U "google-genai>=2.3,<3".')
    client = genai.Client(api_key=load_api_key())
    if not hasattr(client, "interactions"):
        sys.exit('Error: google-genai is too old. Upgrade with: pip install -U "google-genai>=2.3,<3"')
    request = build_request(settings, prompt, mime)
    interaction = call_with_retries(lambda: client.interactions.create(**request))

    image = final_image(interaction)
    if image is None:
        status = getattr(interaction, "status", "unknown")
        errors = "; ".join(getattr(e, "message", str(e)) for e in getattr(interaction, "errors", None) or [])
        sys.exit(f"No image was returned (status: {status}). {errors}".strip() +
                 "\nThe prompt may have been blocked by safety filters; rephrase and retry.")
    return {
        "images": [(base64.b64decode(image.data), getattr(image, "mime_type", None) or mime)],
        "text": getattr(interaction, "output_text", None),
        "suggestions": search_suggestions(interaction),
        "footer": (f"Interaction ID: {interaction.id}  (pass --continue {interaction.id} to refine)"
                   if getattr(interaction, "id", None) else None),
    }


# --- OpenAI (GPT Image) ---------------------------------------------------------


def upload_tuple(path: str) -> tuple[str, bytes, str]:
    return (pathlib.Path(path).name, pathlib.Path(path).read_bytes(),
            mimetypes.guess_type(path)[0] or "image/png")


def openai_params(settings: dict, prompt: str, mime: str) -> dict:
    params = {"model": settings["model"], "prompt": prompt,
              "output_format": mime.split("/")[1], "n": settings["n"]}
    size = gpt_size(settings["size"], settings["aspect"])
    if size:
        params["size"] = size
    if settings["quality"]:
        params["quality"] = settings["quality"]
    if settings["background"]:
        params["background"] = settings["background"]
    return params


def estimate_cost(model: str, usage) -> str | None:
    prices = GPT_PRICES.get(model)
    if not prices or usage is None:
        return None
    details = getattr(usage, "input_tokens_details", None)
    text_in = getattr(details, "text_tokens", None) or 0
    image_in = getattr(details, "image_tokens", None) or 0
    output = getattr(usage, "output_tokens", None) or 0
    cost = (text_in * prices[0] + image_in * prices[1] + output * prices[2]) / 1_000_000
    return f"Usage: {getattr(usage, 'total_tokens', 0):,} tokens (≈ ${cost:.3f})"


def run_openai(settings: dict, prompt: str, mime: str) -> dict:
    if OpenAI is None:
        sys.exit('Error: openai is not installed. Use `uv run`, or pip install -U "openai>=2,<4".')
    if settings["background"] == "transparent" and mime == "image/jpeg":
        sys.exit("Error: transparent backgrounds need a .png or .webp output path.")
    client = OpenAI(api_key=load_api_key(("OPENAI_API_KEY",)))
    params = openai_params(settings, prompt, mime)
    if settings["edits"]:
        params["image"] = [upload_tuple(p) for p in settings["edits"]]
        if settings["mask"]:
            params["mask"] = upload_tuple(settings["mask"])
        response = call_with_retries(lambda: client.images.edit(**params))
    else:
        response = call_with_retries(lambda: client.images.generate(**params))

    images = [(base64.b64decode(item.b64_json), mime) for item in response.data or [] if item.b64_json]
    if not images:
        sys.exit("No image was returned. The prompt may have been blocked by moderation; rephrase and retry.")
    revised = [item.revised_prompt for item in response.data if getattr(item, "revised_prompt", None)]
    return {
        "images": images,
        "text": f"Revised prompt: {revised[0]}" if revised else None,
        "suggestions": [],
        "footer": estimate_cost(settings["model"], getattr(response, "usage", None)),
    }


# --- Main -------------------------------------------------------------------------


def describe(settings: dict) -> str:
    details = [f"model={settings['model']}"]
    for key in ("size", "aspect", "thinking", "quality", "background"):
        if settings[key]:
            details.append(f"{key}={settings[key]}")
    if settings["edits"]:
        details.append(f"inputs={len(settings['edits'])}")
    for flag, key in (("mask=on", "mask"), ("search=on", "search")):
        if settings[key]:
            details.append(flag)
    if settings["n"] > 1:
        details.append(f"n={settings['n']}")
    if settings["continue_id"]:
        details.append(f"continue={settings['continue_id']}")
    return ", ".join(details)


def main() -> None:
    args = parse_args()
    prompt, config = split_prompt(sys.stdin.read().strip() if args.prompt == "-" else args.prompt)
    if not prompt.strip():
        sys.exit("Error: the prompt is empty.")
    settings = resolve_settings(args, config)
    validate_common(settings)
    (validate_openai if settings["provider"] == "openai" else validate_google)(settings)
    requested_path, mime = output_format(settings["output"], settings["provider"])

    print("Generating: " + describe(settings), file=sys.stderr)
    run = run_openai if settings["provider"] == "openai" else run_google
    result = run(settings, prompt, mime)

    if result["text"]:
        print(result["text"])
    saved = []
    for data, returned_mime in result["images"]:
        path = requested_path
        if returned_mime != mime and returned_mime in EXTENSION_FOR_MIME:
            path = path.with_suffix(EXTENSION_FOR_MIME[returned_mime])
            print(f"Note: model returned {returned_mime}; saving as {path.suffix}.", file=sys.stderr)
        path = unique_path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        saved.append(path)
        print(f"Image saved: {path}")

    if result["suggestions"]:
        sources = saved[0].with_name(saved[0].stem + ".search.html")
        sources.write_text("\n".join(result["suggestions"]))
        print(f"Search suggestions (show these to the user): {sources}")
    if result["footer"]:
        print(result["footer"])


if __name__ == "__main__":
    main()
