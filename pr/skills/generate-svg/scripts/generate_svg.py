#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["google-genai>=2.3,<3", "resvg-py>=0.5,<1"]
# ///
"""Generate or edit SVG graphics with a Gemini text model.

The model writes SVG markup. The script validates it as XML (with one
automatic repair attempt), strips scripts and event handlers, saves it without
overwriting existing files, and can optimize it with svgo and render a PNG
preview for visual review.

Run with `uv run generate_svg.py ...` (installs dependencies automatically)
or with `python3` after `pip install -U "google-genai>=2.3,<3" resvg-py`.

Usage:
    generate_svg.py "description" [options]
    generate_svg.py '{"description": "...", "colors": {...}, "config": {"type": "hero"}}'

Config keys (JSON) / CLI flags:
    output    -o  Output path (default: generated.svg)
    type      -t  hero | icon | illustration | logo | component (default: illustration)
    width         Width in px (default depends on type)
    height        Height in px (default depends on type)
    model     -m  flash (default) | pro | full model ID
    thinking      low | medium | high
    edit      -e  Existing SVG to modify according to the description
    optimize      Run svgo on the result (needs Node.js)
    preview       Render <output>.preview.png for visual review

Environment:
    GEMINI_API_KEY (or GOOGLE_API_KEY), read from the environment, then ./.env,
    ./.claude/.env, then ~/.claude/.env.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

if sys.version_info < (3, 10):
    sys.exit(
        "Error: Python 3.10+ is required (found %d.%d). Run this script with "
        "`uv run`, which provisions a suitable Python automatically." % sys.version_info[:2]
    )

try:
    from google import genai
    from google.genai import types
except ImportError:
    sys.exit(
        "Error: google-genai is not installed. Run with `uv run`, or install it with:\n"
        '  python3 -m pip install -U "google-genai>=2.3,<3"'
    )

# Aliases for current Gemini text models (verified against ai.google.dev, Oct 2026).
MODELS = {
    "flash": "gemini-3.8-flash",       # default: strongest Flash model for code
    "pro": "gemini-3.1-pro-preview",   # deeper reasoning for intricate illustrations
}
DEFAULT_MODEL = "flash"
THINKING_LEVELS = {
    "gemini-3.8-flash": {"low", "medium", "high"},
    "gemini-3.1-pro-preview": {"low", "medium", "high"},
}

TYPE_DEFAULTS = {
    "hero": (1200, 600),
    "icon": (24, 24),
    "illustration": (800, 600),
    "logo": (200, 200),
    "component": (400, 300),
}

SYSTEM_INSTRUCTION = """You are an expert SVG designer and front-end engineer. Produce production-quality, hand-optimized SVG code.

Output rules:
- Output ONLY the SVG document: no markdown fences, no explanations, no prose.
- The root <svg> has xmlns="http://www.w3.org/2000/svg", a viewBox matching the requested dimensions, and explicit width and height.
- The markup must be well-formed XML and render identically in Chrome, Firefox, and Safari.
- Never use <script>, event-handler attributes (onclick, onload, ...), external resources, or embedded raster images.

Construction:
- Put gradients, filters, patterns, clipPaths, and symbols in a single <defs> block with descriptive ids.
- Keep paths lean: few anchor points, merged shapes, coordinates rounded to at most 2 decimals.
- Prefer geometric primitives (circle, rect, line, polygon) where they suffice.
- Use a coherent palette. Use currentColor where the graphic should inherit the surrounding text color (icons, monochrome logos).
- Avoid <text> unless the description asks for words; when used, set a generic font stack (e.g. font-family="system-ui, sans-serif").

Accessibility:
- Decorative graphics (hero backgrounds, patterns, ornaments): add aria-hidden="true" and focusable="false" to the root.
- Meaningful graphics (logos, standalone icons, illustrations that convey content): add role="img" to the root and a <title> as its first child.

Animation (only when the description asks for it):
- Use CSS @keyframes inside a <style> element, not SMIL.
- Prefix keyframe names and animated ids/classes with svg- (svg-pulse, svg-float, svg-dash).
- Animate transform and opacity (and stroke-dashoffset for drawing effects); set transform-box: fill-box and transform-origin for rotations and scales.
- Smooth timing: ease-in-out, 2-6 s, staggered animation-delay for repeated elements, infinite only for ambient motion.
- Always include: @media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"""

TYPE_INSTRUCTIONS = {
    "hero": """Design a hero-section illustration:
- Layered composition (background, midground, foreground) with depth from linear and radial gradients.
- Leave generous negative space where a headline will sit (the description says where; default: left half).
- It will sit behind text, so keep contrast moderate in the text area.
- Decorative: aria-hidden on the root.""",
    "icon": """Design a UI icon in the style of modern icon sets (Lucide/Feather):
- viewBox 0 0 24 24 drawn on a 24-unit grid with ~2 units of padding.
- Stroke-based: fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" on the root.
- One to four simple paths or primitives; must read clearly at 16px.
- No text, no gradients, no hard-coded colors.""",
    "illustration": """Create an illustration:
- A palette of 3-5 harmonious colors; clear focal point and visual hierarchy through size and contrast.
- Mix geometric and organic shapes; add a few details that reward a closer look without clutter.""",
    "logo": """Design a logo mark:
- Simple, distinctive silhouette that works from 16px favicon to large display.
- At most 2-3 colors, and it must still work in a single color.
- No fine details that disappear at small sizes. Avoid text unless the brand name is explicitly requested.""",
    "component": """Create a UI component graphic:
- Clean, modern design with consistent spacing and corner radii.
- Expose colors as CSS custom properties with fallbacks (e.g. fill="var(--svg-accent, #4f46e5)") so it can be themed.
- Works on both light and dark backgrounds; use meaningful class names.""",
}

RETRYABLE_STATUS = {429, 500, 502, 503, 504}
RETRY_DELAYS = (10, 30)
SVG_NS = "{http://www.w3.org/2000/svg}"


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
    parser = argparse.ArgumentParser(description="Generate or edit SVG graphics with Gemini.")
    parser.add_argument("prompt", help="Description, or a JSON prompt with a 'config' key (use - to read it from stdin)")
    parser.add_argument("-o", "--output", help="Output path (default: generated.svg)")
    parser.add_argument("-t", "--type", choices=sorted(TYPE_DEFAULTS), help="Graphic type")
    parser.add_argument("--width", type=int, help="Width in px")
    parser.add_argument("--height", type=int, help="Height in px")
    parser.add_argument("-m", "--model", help="flash (default), pro, or a full model ID")
    parser.add_argument("--thinking", help="low, medium, or high")
    parser.add_argument("-e", "--edit", help="Existing SVG to modify")
    parser.add_argument("--optimize", action="store_true", help="Run svgo on the result")
    parser.add_argument("--preview", action="store_true", help="Render a PNG preview")
    return parser.parse_args()


def split_prompt(raw: str) -> tuple[str, dict]:
    """Return (description, config). JSON prompts keep all creative keys."""
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return raw, {}
    if not isinstance(data, dict):
        return raw, {}
    config = data.pop("config", None) or {}
    if not isinstance(config, dict):
        sys.exit("Error: 'config' must be a JSON object.")
    if set(data) <= {"description"}:
        return str(data.get("description", "")), config
    return json.dumps(data, indent=2), config


def resolve_settings(args: argparse.Namespace, config: dict) -> dict:
    def pick(key, flag):
        return config[key] if config.get(key) is not None else flag

    svg_type = pick("type", args.type) or "illustration"
    if svg_type not in TYPE_DEFAULTS:
        sys.exit(f"Error: unknown type '{svg_type}'. Choose from {', '.join(sorted(TYPE_DEFAULTS))}.")
    default_w, default_h = TYPE_DEFAULTS[svg_type]
    model_name = pick("model", args.model) or DEFAULT_MODEL
    settings = {
        "type": svg_type,
        "width": int(pick("width", args.width) or default_w),
        "height": int(pick("height", args.height) or default_h),
        "model": MODELS.get(model_name, model_name),
        "thinking": pick("thinking", args.thinking),
        "edit": pick("edit", args.edit),
        "output": pick("output", args.output) or "generated.svg",
        "optimize": bool(pick("optimize", args.optimize)),
        "preview": bool(pick("preview", args.preview)),
    }
    levels = THINKING_LEVELS.get(settings["model"])
    if settings["thinking"] and levels and settings["thinking"] not in levels:
        sys.exit(f"Error: {settings['model']} thinking levels: {', '.join(sorted(levels))}.")
    if settings["edit"] and not pathlib.Path(settings["edit"]).is_file():
        sys.exit(f"Error: SVG to edit not found: {settings['edit']}")
    if not settings["output"].lower().endswith(".svg"):
        sys.exit("Error: output path must end in .svg")
    return settings


def build_prompt(settings: dict, description: str) -> str:
    w, h = settings["width"], settings["height"]
    parts = [TYPE_INSTRUCTIONS[settings["type"]], f'Dimensions: {w}x{h}px (viewBox="0 0 {w} {h}").']
    if settings["edit"]:
        existing = pathlib.Path(settings["edit"]).read_text()
        parts.append("Modify the existing SVG below. Apply the requested changes, keep everything "
                     "else as it is, and return the complete updated SVG.\n\n" + existing)
        parts.append(f"Requested changes:\n{description}")
    else:
        parts.append(f"Description:\n{description}")
    return "\n\n".join(parts)


def status_code(error: Exception) -> int | None:
    code = getattr(error, "status_code", None) or getattr(error, "code", None)
    return code if isinstance(code, int) else None


def generate_text(client, model: str, contents, config) -> str:
    for attempt in range(len(RETRY_DELAYS) + 1):
        try:
            response = client.models.generate_content(model=model, contents=contents, config=config)
            return response.text or ""
        except Exception as error:  # SDK error classes differ across versions
            code = status_code(error)
            if code in RETRYABLE_STATUS and attempt < len(RETRY_DELAYS):
                delay = RETRY_DELAYS[attempt]
                print(f"HTTP {code}; retrying in {delay}s...", file=sys.stderr)
                time.sleep(delay)
                continue
            sys.exit(f"Error: {error}")
    return ""


def extract_svg(text: str) -> str | None:
    match = re.search(r"<svg\b[\s\S]*</svg>", text, re.IGNORECASE)
    return match.group(0) if match else None


def xml_error(svg: str) -> str | None:
    """Return a parse error message, or None when the SVG is well-formed with an <svg> root."""
    try:
        root = ET.fromstring(svg)
    except ET.ParseError as error:
        return str(error)
    if root.tag not in ("svg", SVG_NS + "svg"):
        return f"root element is <{root.tag}>, expected <svg>"
    return None


def sanitize(svg: str) -> tuple[str, int]:
    """Remove scripts, event-handler attributes, and javascript: URLs."""
    patterns = [
        (r"<script\b[\s\S]*?</script\s*>", ""),
        (r"<script\b[^>]*/>", ""),
        (r"\s+on[a-zA-Z]+\s*=\s*(\"[^\"]*\"|'[^']*')", ""),
        (r"((?:xlink:)?href\s*=\s*[\"'])\s*javascript:[^\"']*", r"\1#"),
    ]
    removed = 0
    for pattern, replacement in patterns:
        svg, count = re.subn(pattern, replacement, svg, flags=re.IGNORECASE)
        removed += count
    return svg, removed


def unique_path(path: pathlib.Path) -> pathlib.Path:
    candidate, n = path, 1
    while candidate.exists():
        candidate = path.with_name(f"{path.stem}-{n}{path.suffix}")
        n += 1
    return candidate


def optimize(path: pathlib.Path) -> None:
    if not shutil.which("npx"):
        print("Skipping svgo: Node.js (npx) not found.", file=sys.stderr)
        return
    result = subprocess.run(["npx", "--yes", "svgo", str(path), "-o", str(path)],
                            capture_output=True, text=True, timeout=120)
    if result.returncode == 0:
        print("Optimized with svgo.")
    else:
        print(f"svgo failed: {result.stderr.strip()[:300]}", file=sys.stderr)


def render_preview(path: pathlib.Path, width: int) -> None:
    try:
        import resvg_py
    except ImportError:
        print("Skipping preview: resvg-py not installed (run with `uv run`).", file=sys.stderr)
        return
    preview = path.with_name(path.stem + ".preview.png")
    png = resvg_py.svg_to_bytes(svg_path=str(path), width=max(width, 512), background="white")
    preview.write_bytes(bytes(png))
    print(f"Preview: {preview}")


def main() -> None:
    args = parse_args()
    description, config = split_prompt(sys.stdin.read().strip() if args.prompt == "-" else args.prompt)
    if not description.strip():
        sys.exit("Error: the description is empty.")
    settings = resolve_settings(args, config)

    client = genai.Client(api_key=load_api_key())
    gen_config = {"system_instruction": SYSTEM_INSTRUCTION}
    if settings["thinking"]:
        gen_config["thinking_config"] = types.ThinkingConfig(thinking_level=settings["thinking"])
    gen_config = types.GenerateContentConfig(**gen_config)

    action = "Editing" if settings["edit"] else "Generating"
    print(f"{action} {settings['type']} SVG ({settings['width']}x{settings['height']}) "
          f"with {settings['model']}...", file=sys.stderr)
    prompt = build_prompt(settings, description)
    text = generate_text(client, settings["model"], prompt, gen_config)
    svg = extract_svg(text)
    error = xml_error(svg) if svg else "no <svg> element in the response"

    if error:
        print(f"Invalid SVG ({error}); asking the model to repair it...", file=sys.stderr)
        repair = (f"{prompt}\n\nYour previous answer was not a valid SVG document ({error}). "
                  f"Return the complete, corrected SVG only.\n\nPrevious answer:\n{text[:20000]}")
        text = generate_text(client, settings["model"], repair, gen_config)
        svg = extract_svg(text)
        error = xml_error(svg) if svg else "no <svg> element in the response"
        if error:
            sys.exit(f"Error: the model did not return a valid SVG ({error}). Raw output starts:\n{text[:500]}")

    svg, removed = sanitize(svg)
    if removed:
        print(f"Removed {removed} script/event-handler construct(s).", file=sys.stderr)
    if "viewBox" not in svg[:svg.find(">") + 1]:
        print("Warning: the root <svg> has no viewBox; it will not scale cleanly.", file=sys.stderr)

    path = unique_path(pathlib.Path(settings["output"]).expanduser())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg + "\n")
    print(f"SVG saved: {path} ({path.stat().st_size:,} bytes)")

    if settings["optimize"]:
        optimize(path)
    if settings["preview"]:
        render_preview(path, settings["width"])


if __name__ == "__main__":
    main()
