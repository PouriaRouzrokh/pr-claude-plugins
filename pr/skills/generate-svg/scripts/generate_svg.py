#!/usr/bin/env python3
"""
Generate SVG graphics using Gemini 3.1 Pro.

Uses gemini-3.1-pro-preview to generate SVG code as text. All parameters
can be controlled via a JSON prompt with a "config" key, or via CLI flags.

Usage:
    python generate_svg.py "prompt_or_json" [options]

JSON prompt format (config is extracted, rest sent to model):
    {
      "description": "main description",
      "elements": ["geometric shapes", "gradients", ...],
      "colors": {"primary": "#1e40af", "accent": "#06b6d4", ...},
      "layout": {"negative_space": "center-left for text overlay"},
      "style": "glassmorphic | minimal | detailed | organic",
      "config": {
        "output": "hero.svg",
        "type": "hero",
        "width": 1200,
        "height": 600,
        "optimize": true
      }
    }

CLI flags (fallbacks if not in JSON config):
    --output, -o    Output filename (default: generated.svg)
    --type, -t      SVG type: hero, icon, illustration, logo, component
    --width         SVG width in pixels
    --height        SVG height in pixels
    --optimize      Run svgo optimization on output

Environment:
    GEMINI_API_KEY  Required. Loaded from env, .env, or .claude/.env.
"""

import argparse
import json
import os
import pathlib
import re
import subprocess
import sys

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai package not installed.")
    print("Install with: pip install google-genai")
    sys.exit(1)


def load_env_file(filepath):
    """Load KEY=VALUE pairs from an env file into os.environ."""
    try:
        for line in pathlib.Path(filepath).read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())
    except FileNotFoundError:
        pass


def load_api_key():
    """Load GEMINI_API_KEY from env, then .env, then .claude/.env."""
    if os.environ.get("GEMINI_API_KEY"):
        return
    load_env_file(os.path.join(os.getcwd(), ".env"))
    if os.environ.get("GEMINI_API_KEY"):
        return
    load_env_file(os.path.join(os.getcwd(), ".claude", ".env"))


TYPE_DEFAULTS = {
    "hero": {"width": 1200, "height": 600},
    "icon": {"width": 24, "height": 24},
    "illustration": {"width": 800, "height": 600},
    "logo": {"width": 200, "height": 200},
    "component": {"width": 400, "height": 300},
}

SYSTEM_INSTRUCTION = """You are an expert SVG designer. Generate production-quality SVG code.

Rules:
- Always include xmlns="http://www.w3.org/2000/svg" on the root <svg> element
- Always include a viewBox attribute matching the width and height
- Include explicit width and height attributes
- Use meaningful IDs on elements that might be animated (prefix with svg-)
- Keep paths simple — minimize anchor points, merge overlapping paths
- Include aria-hidden="true" on the root element for decorative SVGs
- Use currentColor where appropriate to support theming
- Place reusable definitions (gradients, filters, patterns) in a <defs> block
- Output ONLY the SVG code — no markdown fences, no explanations, no prose
- The SVG must be valid and render correctly in all modern browsers

Animation capabilities (use when the prompt requests animation):
- Prefer CSS @keyframes animations inside a <style> block within the SVG
- Use meaningful animation names prefixed with svg- (e.g., svg-pulse, svg-float, svg-glow-cycle)
- Common animation patterns:
  * Pulse: scale or opacity oscillation (e.g., transform: scale(1) -> scale(1.1))
  * Float: translateY oscillation for hovering elements
  * Glow: opacity or filter cycling for light effects
  * Rotate: continuous rotation for spinners or orbital elements
  * Dash: stroke-dashoffset animation for drawing/flowing line effects
  * Fade-in: opacity 0 -> 1 with staggered delays for sequential reveals
- Use animation-delay to stagger animations across similar elements
- Keep animations smooth: prefer ease-in-out timing, 2-6 second durations
- Use infinite loops for ambient/decorative animations
- Add prefers-reduced-motion media query to disable animations for accessibility:
  @media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation: none !important; } }
- Avoid SMIL <animate> elements — CSS animations have better browser support"""

TYPE_INSTRUCTIONS = {
    "hero": """Design a hero section illustration:
- Use rich gradients (linear and radial) for depth
- Include geometric shapes for visual interest
- Create layered compositions with foreground/background separation
- Use negative space effectively
- Ensure the design works well as a background with text overlay
- Include subtle decorative elements (dots, lines, circles)""",
    "icon": """Design a clean icon:
- Use consistent stroke width throughout
- Design on a 24x24 grid with 2px padding
- Keep the design simple and recognizable at small sizes
- Use rounded line caps and joins for a friendly feel
- Test visual clarity: would this read at 16px?""",
    "illustration": """Create a detailed illustration:
- Use a coherent color palette (3-5 colors max)
- Include both geometric and organic shapes
- Create visual hierarchy with size and color contrast
- Add subtle details that reward closer inspection""",
    "logo": """Design a logo mark:
- Keep it simple — should work at 16px and 1000px
- Use a maximum of 2-3 colors
- Ensure it works in monochrome (single color)
- Create a distinctive, memorable shape
- Avoid fine details that disappear at small sizes""",
    "component": """Create a UI component:
- Use clean, modern design language
- Include appropriate padding and spacing
- Use CSS custom properties for colors where possible
- Design for light and dark theme compatibility
- Include meaningful class names for styling""",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate SVG graphics with Gemini 3.1 Pro"
    )
    parser.add_argument("prompt", help="Description or JSON prompt for SVG generation")
    parser.add_argument(
        "-o", "--output", default="generated.svg", help="Output filename"
    )
    parser.add_argument(
        "-t", "--type",
        choices=["hero", "icon", "illustration", "logo", "component"],
        default="illustration",
        help="SVG type (affects dimensions and style guidance)",
    )
    parser.add_argument("--width", type=int, help="SVG width in pixels")
    parser.add_argument("--height", type=int, help="SVG height in pixels")
    parser.add_argument(
        "--optimize", action="store_true", help="Run svgo optimization on output"
    )
    return parser.parse_args()


def extract_config(prompt_str):
    """If prompt is JSON with a 'config' key, extract config and return (prompt_str, config)."""
    try:
        data = json.loads(prompt_str)
        if isinstance(data, dict) and "config" in data:
            config = data.pop("config")
            return json.dumps(data), config
        return prompt_str, {}
    except (json.JSONDecodeError, TypeError):
        return prompt_str, {}


def extract_svg(text):
    """Extract SVG content from model response, stripping any markdown fences."""
    text = re.sub(r"```(?:svg|xml|html)?\s*\n?", "", text)
    text = re.sub(r"\n?```\s*$", "", text.strip())
    match = re.search(r"(<svg[\s\S]*?</svg>)", text, re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def optimize_svg(filepath):
    """Run svgo on the SVG file if available."""
    try:
        result = subprocess.run(
            ["npx", "svgo", filepath, "-o", filepath],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            print("SVG optimized with svgo.")
        else:
            print(f"svgo warning: {result.stderr.strip()}")
    except FileNotFoundError:
        print("svgo not found. Install with: npm install -g svgo")
    except subprocess.TimeoutExpired:
        print("svgo optimization timed out.")


def generate(args):
    load_api_key()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    # Extract config from JSON prompt if present
    prompt_str, json_config = extract_config(args.prompt)

    # JSON config overrides CLI flags
    output = json_config.get("output", args.output)
    svg_type = json_config.get("type", args.type)
    width = json_config.get("width", args.width)
    height = json_config.get("height", args.height)
    do_optimize = json_config.get("optimize", args.optimize)

    defaults = TYPE_DEFAULTS.get(svg_type, {"width": 800, "height": 600})
    width = width or defaults["width"]
    height = height or defaults["height"]

    client = genai.Client(api_key=api_key)

    type_instruction = TYPE_INSTRUCTIONS.get(svg_type, "")
    prompt = f"""{type_instruction}

Dimensions: {width}x{height}px (viewBox="0 0 {width} {height}")

Description: {prompt_str}"""

    config = types.GenerateContentConfig(
        response_modalities=["TEXT"],
        system_instruction=SYSTEM_INSTRUCTION,
    )

    print(f"Generating {svg_type} SVG ({width}x{height})...")
    response = client.models.generate_content(
        model="gemini-3.1-pro-preview",
        contents=[prompt],
        config=config,
    )

    if not response.text:
        print("No response from model. Try a different prompt.")
        sys.exit(1)

    svg_content = extract_svg(response.text)
    if not svg_content:
        print("Could not extract SVG from response. Raw output:")
        print(response.text[:500])
        sys.exit(1)

    with open(output, "w") as f:
        f.write(svg_content)
    print(f"SVG saved: {output}")

    if do_optimize:
        optimize_svg(output)


def main():
    args = parse_args()
    generate(args)


if __name__ == "__main__":
    main()
