---
name: generate-image-nb
description: This skill should be used when the user asks to "generate an image", "create a picture", "make a thumbnail", "design a logo", "draw an illustration", "edit a photo", "add to an image", "remove from an image", or create any visual content including blog headers, icons, diagrams, banners, or graphics. Handles all image generation and editing requests via the Gemini Nano Banana API.
allowed-tools: Bash(python*), Bash(node*), Bash(pip*), Bash(npm*)
---

# Nano Banana Image Generation

Generate and edit images via the Gemini Nano Banana API using Python or JavaScript scripts.

## Setup

Before generating images, verify the API key exists:

```bash
[ -n "$GEMINI_API_KEY" ] && echo "API key configured" || echo "Missing GEMINI_API_KEY"
```

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
| `-m, --model` | flash (fast, default) or pro (high-quality, 4K) |
| `-a, --aspect` | Aspect ratio: 1:1, 16:9, 9:16, 2:3, 3:2, etc. |
| `-s, --size` | Resolution for pro model: 1K, 2K, 4K |
| `-e, --edit` | Input image path for editing |
| `--search` | Enable Google Search grounding (pro only) |

## Generation Examples

### Text to Image

```bash
# Blog header
python scripts/generate_image.py "modern flat illustration of developer coding, purple gradient background, minimalist style, no text" -a 16:9 -o header.png

# YouTube thumbnail
python scripts/generate_image.py "professional editorial photo of coffee on wooden desk, morning sunlight, shallow depth of field" -a 16:9 -o thumbnail.png

# Logo
python scripts/generate_image.py "minimalist logo for coffee shop called 'The Daily Grind', clean sans-serif font, black and white, coffee bean motif" -m pro -a 1:1 -o logo.png

# Icon
python scripts/generate_image.py "kawaii-style app icon of a happy robot, bold outlines, vibrant colors, white background" -a 1:1 -o icon.png
```

### Image Editing

```bash
# Add element
python scripts/generate_image.py "Add a small wizard hat on the cat's head, matching the soft lighting" -e cat.jpg -o cat_wizard.png

# Style transfer
python scripts/generate_image.py "Transform into Van Gogh's Starry Night style with swirling brushstrokes" -e city.png -o city_art.png

# Modify element
python scripts/generate_image.py "Change the blue sofa to a brown leather chesterfield, keep everything else unchanged" -e room.jpg -o room_edited.png
```

### Real-Time Content (Pro Model)

```bash
# Weather visualization
python scripts/generate_image.py "Current 5-day weather forecast for San Francisco as a modern chart" -m pro --search -a 16:9 -o weather.png

# Sports graphic
python scripts/generate_image.py "Stylish graphic of last night's game score" -m pro --search -o score.png
```

## Model Selection

| Model | Use Case | Resolution | Cost |
|-------|----------|------------|------|
| flash | Fast generation, high volume | 1024px | ~$0.04/image |
| pro | Professional assets, text rendering, 4K | Up to 4K | Higher |

Use `pro` for:
- Accurate text in images (logos, infographics)
- High-resolution output (2K, 4K)
- Real-time data with Google Search
- Complex multi-turn editing

Use `flash` for:
- Quick iterations
- High-volume generation
- Standard resolution needs

## Aspect Ratios

| Use Case | Ratio | Example |
|----------|-------|---------|
| YouTube thumbnail | 16:9 | 1344x768 |
| Blog featured image | 16:9 | 1344x768 |
| Instagram square | 1:1 | 1024x1024 |
| Story/Reels | 9:16 | 768x1344 |
| Twitter header | 21:9 | 1536x672 |
| Portrait | 2:3 | 832x1248 |

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

## Limitations

- Supported languages: EN, ar-EG, de-DE, es-MX, fr-FR, hi-IN, id-ID, it-IT, ja-JP, ko-KR, pt-BR, ru-RU, ua-UA, vi-VN, zh-CN
- No audio or video inputs
- flash: up to 3 input images; pro: up to 14 input images
- Output count may vary from request
- All images include SynthID watermark

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Missing API key | Set `GEMINI_API_KEY` environment variable |
| Package not found | Run pip/npm install commands |
| No image generated | Simplify prompt, check for policy violations |
| Poor text rendering | Use pro model for text-heavy images |
| Wrong aspect ratio | Explicitly set `-a` option |

## Reference

For complete API documentation, prompting strategies, and code examples in multiple languages, see `references/nano-banana-docs.md`.
