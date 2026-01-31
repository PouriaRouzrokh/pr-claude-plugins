#!/usr/bin/env python3
"""
Generate images using the Gemini Nano Banana API.

Usage:
    python generate_image.py "prompt" [options]

Options:
    --output, -o    Output filename (default: generated_image.png)
    --model, -m     Model: flash (default) or pro
    --aspect, -a    Aspect ratio (1:1, 16:9, 9:16, etc.)
    --size, -s      Image size for pro model: 1K, 2K, 4K
    --edit, -e      Path to input image for editing
    --search        Enable Google Search grounding (pro model only)

Examples:
    python generate_image.py "A cat wearing a hat"
    python generate_image.py "A blog header" -a 16:9 -o header.png
    python generate_image.py "Add sunglasses" -e photo.jpg -o edited.png
    python generate_image.py "Current weather in NYC" -m pro --search

Environment:
    GEMINI_API_KEY  Required. Your Gemini API key.
"""

import argparse
import os
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


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate images with Gemini Nano Banana API"
    )
    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument(
        "-o", "--output", default="generated_image.png", help="Output filename"
    )
    parser.add_argument(
        "-m",
        "--model",
        choices=["flash", "pro"],
        default="flash",
        help="Model to use (flash=fast, pro=high-quality)",
    )
    parser.add_argument(
        "-a",
        "--aspect",
        help="Aspect ratio (1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9)",
    )
    parser.add_argument(
        "-s",
        "--size",
        choices=["1K", "2K", "4K"],
        help="Image size (pro model only)",
    )
    parser.add_argument("-e", "--edit", help="Input image path for editing")
    parser.add_argument(
        "--search", action="store_true", help="Enable Google Search grounding"
    )
    return parser.parse_args()


def get_model_name(model_choice):
    if model_choice == "pro":
        return "gemini-3-pro-image-preview"
    return "gemini-2.5-flash-image"


def load_image(path):
    if Image is None:
        print("Error: Pillow package required for image editing.")
        print("Install with: pip install Pillow")
        sys.exit(1)
    return Image.open(path)


def build_config(args):
    config_kwargs = {"response_modalities": ["TEXT", "IMAGE"]}

    image_config_kwargs = {}
    if args.aspect:
        image_config_kwargs["aspect_ratio"] = args.aspect
    if args.size and args.model == "pro":
        image_config_kwargs["image_size"] = args.size

    if image_config_kwargs:
        config_kwargs["image_config"] = types.ImageConfig(**image_config_kwargs)

    if args.search and args.model == "pro":
        config_kwargs["tools"] = [{"google_search": {}}]

    return types.GenerateContentConfig(**config_kwargs)


def generate(args):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    model_name = get_model_name(args.model)

    contents = []
    if args.edit:
        contents.append(load_image(args.edit))
    contents.append(args.prompt)

    config = build_config(args)

    print(f"Generating with {model_name}...")
    response = client.models.generate_content(
        model=model_name, contents=contents, config=config
    )

    saved = False
    for part in response.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = part.as_image()
            image.save(args.output)
            print(f"Image saved: {args.output}")
            saved = True

    if not saved:
        print("No image was generated. Check your prompt and try again.")
        sys.exit(1)


def main():
    args = parse_args()
    generate(args)


if __name__ == "__main__":
    main()
