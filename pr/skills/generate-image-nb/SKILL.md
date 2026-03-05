---
name: generate-image-nb
description: This skill should be used when the user asks to "generate an image", "create a picture", "make a thumbnail", "design a logo", "draw an illustration", "edit a photo", "add to an image", "remove from an image", or create any visual content including blog headers, icons, diagrams, banners, or graphics. Handles all image generation and editing requests via the Gemini Nano Banana 2 API (gemini-3.1-flash-image-preview).
allowed-tools: Bash(python*), Bash(node*), Bash(pip*), Bash(npm*)
---

# Nano Banana 2 Image Generation

For scalable vector graphics (icons, logos, hero illustrations), use `generate-svg` instead.

Generate and edit images via **Nano Banana 2** (`gemini-3.1-flash-image-preview`) — Google's fastest image generation model. 2x faster than the original, 50% cheaper, supports 512px–4K, image search grounding, and achieves ~95% of Pro quality.

## IMPORTANT: Default Prompting Behavior

**When invoking this skill, ALWAYS construct a JSON prompt that includes BOTH the creative prompt AND a `config` key** to control all generation parameters. The script extracts `config` before sending the rest to the model. This gives Claude full control over resolution, aspect ratio, output path, and search — nothing is hardcoded.

Build a single JSON object from the user's request:

```python
import json
prompt = json.dumps({
    "task": "generate_image",
    "subject": {"primary": "...", "details": "..."},
    "style": {"primary": "...", "rendering_quality": "..."},
    "composition": {"framing": "...", "perspective": "..."},
    "technical": {"camera": {"focal_length": "..."}, "lighting": "..."},
    "environment": {"atmosphere": "..."},
    "quality": {"include": ["..."], "avoid": ["..."]},
    "config": {
        "output": "filename.png",
        "size": "4K",
        "aspect_ratio": "16:9",
        "search": False,
        "edit": None
    }
})
```

Then pass the serialized JSON string as the single prompt argument:

```bash
python scripts/generate_image.py '<json_string>'
```

**Config keys** (all optional — omit any that aren't needed):
| Key | Values | Description |
|-----|--------|-------------|
| `output` | any filename | Output path (default: generated_image.png) |
| `size` | `512`, `1K`, `2K`, `4K` | Image resolution |
| `aspect_ratio` | `1:1`, `16:9`, `9:16`, `2:3`, `3:2`, `21:9`, etc. | Aspect ratio |
| `search` | `true`/`false` | Enable image search grounding |
| `edit` | file path | Input image for editing |

**Creative prompt keys** (omit any that aren't relevant):
| Key | Purpose |
|-----|---------|
| `task` | Always `"generate_image"` |
| `subject` | Primary subject and details |
| `style` | Art style and rendering quality |
| `composition` | Framing and perspective |
| `technical` | Camera settings and lighting |
| `environment` | Atmosphere and mood |
| `quality` | Include/avoid lists |

For trivially simple requests (e.g., "a cat in a hat"), a plain text prompt is acceptable — the script handles both JSON and plain text.

## Setup

Before generating images, verify the API key exists:

```bash
[ -n "$GEMINI_API_KEY" ] && echo "API key configured" || echo "Missing GEMINI_API_KEY"
```

The scripts automatically load `GEMINI_API_KEY` from: environment variable, then `.env` in the project root, then `.claude/.env`.

Install dependencies based on the user's environment:

```bash
# Python
pip install google-genai Pillow

# JavaScript
npm install @google/genai
```

## Script Usage

### Python

```bash
python scripts/generate_image.py "prompt" [options]
```

### JavaScript

```bash
node scripts/generate_image.mjs "prompt" [options]
```

### Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Output filename (default: generated_image.png) |
| `-a, --aspect` | Aspect ratio: 1:1, 16:9, 9:16, 2:3, 3:2, etc. |
| `-s, --size` | Resolution: 512 (preview), 1K, 2K, 4K |
| `-e, --edit` | Input image path for editing |
| `--search` | Enable image search grounding for real-time visual content |

## NB2 Capabilities

- **Speed**: 2x faster than original Nano Banana, 4-6 seconds per image
- **Resolution**: 512px preview mode up to 4K
- **References**: Up to 10 object refs, 4 character refs per prompt
- **Search**: `image_search` tool for real-time visual grounding
- **Quality**: ~95% of Pro quality for most tasks
- **Cost**: ~$0.02/image at 1K, ~$0.07/image at 4K

## Generation Examples

### Text to Image

```bash
# Blog header
python scripts/generate_image.py "modern flat illustration of developer coding, purple gradient background, minimalist style, no text" -a 16:9 -o header.png

# High-res landscape
python scripts/generate_image.py "Mountain landscape at golden hour" -s 2K -a 16:9 -o landscape.png

# Quick 512px preview
python scripts/generate_image.py "kawaii robot app icon" -s 512 -a 1:1 -o icon_preview.png

# Logo
python scripts/generate_image.py "minimalist logo for coffee shop called 'The Daily Grind', clean sans-serif font, black and white, coffee bean motif" -a 1:1 -o logo.png
```

### Image Editing

```bash
# Add element
python scripts/generate_image.py "Add a small wizard hat on the cat's head, matching the soft lighting" -e cat.jpg -o cat_wizard.png

# Style transfer
python scripts/generate_image.py "Transform into Van Gogh's Starry Night style with swirling brushstrokes" -e city.png -o city_art.png
```

### Real-Time Content (Image Search)

```bash
# Photo of a real product
python scripts/generate_image.py "Photo of the latest iPhone model on a wooden desk" --search -o iphone.png

# Current events visualization
python scripts/generate_image.py "Infographic of today's top news headlines" --search -a 16:9 -o news.png
```

## JSON-Structured Prompting

For complex scenes with multiple elements, JSON-structured prompts improve results by 60-80% compared to plain text. The JSON is serialized as a string via `json.dumps()` / `JSON.stringify()` and passed as the text prompt — it is NOT used as `responseSchema`.

### JSON Prompt Template

```json
{
  "task": "generate_image",
  "subject": {
    "primary": "main subject",
    "details": "specific details about the subject"
  },
  "style": {
    "primary": "photorealistic | illustration | watercolor | etc.",
    "rendering_quality": "4K | 2K | 1K"
  },
  "composition": {
    "framing": "rule of thirds | centered | etc.",
    "perspective": "wide-angle | close-up | bird's eye | etc."
  },
  "technical": {
    "camera": { "focal_length": "24mm | 50mm | 85mm" },
    "lighting": "golden hour | studio | dramatic | natural"
  },
  "environment": {
    "atmosphere": "misty | clear | moody | vibrant"
  },
  "quality": {
    "include": ["desired elements"],
    "avoid": ["unwanted elements"]
  }
}
```

### When to Use JSON vs Plain Text

- **JSON**: Complex scenes with 3+ elements, specific technical requirements, multiple style constraints
- **Plain text**: Simple requests, single-subject images, quick iterations

### Python Example

```python
import json

prompt = json.dumps({
    "task": "generate_image",
    "subject": {"primary": "mountain landscape", "details": "snow-capped peaks reflected in alpine lake"},
    "style": {"primary": "photorealistic", "rendering_quality": "4K"},
    "composition": {"framing": "rule of thirds", "perspective": "wide-angle panoramic"},
    "technical": {"camera": {"focal_length": "24mm"}, "lighting": "golden hour"},
    "environment": {"atmosphere": "crisp morning mist"},
    "quality": {"include": ["sharp details", "natural colors"], "avoid": ["text", "people"]}
})

# Pass as: python scripts/generate_image.py '<json_string>' -s 2K -a 16:9
```

## Aspect Ratios

| Use Case | Ratio | Example |
|----------|-------|---------|
| YouTube thumbnail | 16:9 | 1344x768 |
| Blog featured image | 16:9 | 1344x768 |
| Instagram square | 1:1 | 1024x1024 |
| Story/Reels | 9:16 | 768x1344 |
| Twitter header | 21:9 | 1536x672 |
| Portrait | 2:3 | 832x1248 |
| Ultra-wide | 1:4 or 4:1 | NB2 exclusive |

## Prompt Guidelines

Write descriptive scenes, not keyword lists:

**Effective**: "A photorealistic close-up portrait of a ceramicist with sun-etched wrinkles, inspecting a glazed tea bowl in a sunlit workshop. Soft golden hour light from a window, 85mm lens with bokeh."

**Weak**: "old man, pottery, workshop, golden hour"

### Tips

- Describe the scene narratively
- Specify style: "editorial photography", "flat illustration", "watercolor"
- Include lighting, camera angle, mood
- Add "no text" if unwanted text appears
- Use "white background" or "transparent background" for assets
- Use JSON-structured prompts for complex multi-element scenes

## Limitations

- Supported languages: EN, ar-EG, de-DE, es-MX, fr-FR, hi-IN, id-ID, it-IT, ja-JP, ko-KR, pt-BR, ru-RU, ua-UA, vi-VN, zh-CN
- No audio or video inputs
- Up to 10 object reference images, 4 character references
- Output count may vary from request
- All images include SynthID watermark

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Missing API key | Set `GEMINI_API_KEY` in env, `.env`, or `.claude/.env` |
| Package not found | Run pip/npm install commands |
| No image generated | Simplify prompt, check for policy violations |
| Poor text rendering | Use detailed prompts with font/style specifications |
| Wrong aspect ratio | Explicitly set `-a` option |
| HTTP 429 (rate limit) | Wait 30-60 seconds and retry, or reduce request frequency |
| HTTP 400 / SAFETY block | Rephrase prompt to avoid policy-triggering content |
| HTTP 403 (forbidden) | Verify `GEMINI_API_KEY` is valid and has API access enabled |
| Request timeout | Reduce resolution (`-s 1K` or `-s 512`) and retry |

## Reference

For complete API documentation, prompting strategies, and code examples, see `references/nano-banana-docs.md`.
