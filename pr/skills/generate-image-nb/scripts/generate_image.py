#!/usr/bin/env python3
"""
Generate images using the Gemini Nano Banana 2 API.

Uses gemini-3.1-flash-image-preview (Nano Banana 2). All generation
parameters can be controlled via a JSON prompt with a "config" key,
or via CLI flags as fallbacks.

Usage:
    python generate_image.py "prompt_or_json" [options]

JSON prompt format (config is extracted, rest sent to model):
    {
      "task": "generate_image",
      "subject": {"primary": "...", "details": "..."},
      "style": {"primary": "...", "rendering_quality": "..."},
      "composition": {...},
      "technical": {...},
      "environment": {...},
      "quality": {"include": [...], "avoid": [...]},
      "config": {
        "output": "filename.png",
        "size": "4K",
        "aspect_ratio": "16:9",
        "search": true,
        "edit": "input.jpg"
      }
    }

CLI flags (used as fallbacks if not in JSON config):
    --output, -o    Output filename (default: generated_image.png)
    --aspect, -a    Aspect ratio (1:1, 16:9, 9:16, etc.)
    --size, -s      Image size: 512, 1K, 2K, 4K
    --edit, -e      Path to input image for editing
    --search        Enable image search grounding

Environment:
    GEMINI_API_KEY  Required. Loaded from env, .env, .claude/.env, or ~/.claude/.env.
"""

import argparse
import json
import os
import pathlib
import sys

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai package not installed.")
    print("Install with: pip install google-genai")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    Image = None

MODEL = "gemini-3.1-flash-image-preview"


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
    """Load GEMINI_API_KEY from env, then .env, then .claude/.env, then ~/.claude/.env."""
    if os.environ.get("GEMINI_API_KEY"):
        return
    load_env_file(os.path.join(os.getcwd(), ".env"))
    if os.environ.get("GEMINI_API_KEY"):
        return
    load_env_file(os.path.join(os.getcwd(), ".claude", ".env"))
    if os.environ.get("GEMINI_API_KEY"):
        return
    load_env_file(os.path.join(os.path.expanduser("~"), ".claude", ".env"))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate images with Gemini Nano Banana 2"
    )
    parser.add_argument("prompt", help="Text prompt or JSON prompt for image generation")
    parser.add_argument(
        "-o", "--output", default="generated_image.png", help="Output filename"
    )
    parser.add_argument(
        "-a", "--aspect",
        help="Aspect ratio (1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9)",
    )
    parser.add_argument(
        "-s", "--size", choices=["512", "1K", "2K", "4K"],
        help="Image size (512=preview, 1K=default, 2K, 4K)",
    )
    parser.add_argument("-e", "--edit", help="Input image path for editing")
    parser.add_argument(
        "--search", action="store_true", help="Enable image search grounding"
    )
    return parser.parse_args()


def extract_config(prompt_str):
    """If prompt is JSON with a 'config' key, extract config and return (prompt_str, config).
    Config values override CLI defaults. The config key is removed from the prompt sent to the model."""
    try:
        data = json.loads(prompt_str)
        if isinstance(data, dict) and "config" in data:
            config = data.pop("config")
            return json.dumps(data), config
        return prompt_str, {}
    except (json.JSONDecodeError, TypeError):
        return prompt_str, {}


def load_image(path):
    if Image is None:
        print("Error: Pillow package required for image editing.")
        print("Install with: pip install Pillow")
        sys.exit(1)
    return Image.open(path)


def build_config(size, aspect, search):
    config_kwargs = {"response_modalities": ["TEXT", "IMAGE"]}

    image_config_kwargs = {}
    if aspect:
        image_config_kwargs["aspect_ratio"] = aspect
    if size:
        image_config_kwargs["image_size"] = size

    if image_config_kwargs:
        config_kwargs["image_config"] = types.ImageConfig(**image_config_kwargs)

    if search:
        config_kwargs["tools"] = [{"image_search": {}}]

    return types.GenerateContentConfig(**config_kwargs)


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
    size = json_config.get("size", args.size)
    aspect = json_config.get("aspect_ratio", args.aspect)
    search = json_config.get("search", args.search)
    edit = json_config.get("edit", args.edit)

    client = genai.Client(api_key=api_key)

    contents = []
    if edit:
        contents.append(load_image(edit))
    contents.append(prompt_str)

    config = build_config(size, aspect, search)

    print(f"Generating with {MODEL}...")
    if size:
        print(f"  Size: {size}")
    if aspect:
        print(f"  Aspect ratio: {aspect}")
    if search:
        print(f"  Image search: enabled")

    response = client.models.generate_content(
        model=MODEL, contents=contents, config=config
    )

    saved = False
    for part in response.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = part.as_image()
            image.save(output)
            print(f"Image saved: {output}")
            saved = True

    if not saved:
        print("No image was generated. Check your prompt and try again.")
        sys.exit(1)


def main():
    args = parse_args()
    generate(args)


if __name__ == "__main__":
    main()
