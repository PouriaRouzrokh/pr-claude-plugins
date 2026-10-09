---
name: generate-image
description: Generates and edits raster images (photos, illustrations, product shots, blog headers, thumbnails, banners, posters, infographics, stickers, logos with transparent backgrounds, textures) with two model families - Google's Nano Banana (2.1 and Pro) and OpenAI's GPT Image 2.5 (the ChatGPT image model family) - and routes each request to the better fit. Supports multi-image composition, masked and unmasked edits, style transfer, accurate in-image text, transparent backgrounds, batches of variations, Google Search grounding, and conversational refinement. Use when the user asks to generate, create, draw, design, edit, retouch, or restyle an image or picture. For scalable vector graphics (icons, logos, UI illustrations) use generate-svg instead.
argument-hint: "[description of the image to generate or edit]"
allowed-tools: Bash(uv run ${CLAUDE_SKILL_DIR}/scripts/generate_image.py *) Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/generate_image.py *)
---

# Generate Image (Nano Banana + GPT Image)

Generate and edit images by running the bundled script. **Never draw the image yourself** (no ASCII art, no hand-written SVG, no canvas code); always call an image model through the script. One script and one set of flags serve both providers; the model alias picks the provider.

## Models

| Alias | Model ID | Provider | Strengths |
|-------|----------|----------|-----------|
| `nb` (default) | `gemini-nano-banana-2.1` | Google | Best quality per dollar; photorealism; 1K–4K; extreme banner ratios; web + image search grounding; 14 references with consistent characters; conversational refinement. |
| `pro` | `gemini-3-pro-image` | Google | Dense, accurate text (posters, menus, infographics, diagrams); style references; maximum fidelity. |
| `gpt` (alias `chatgpt`) | `gpt-image-2.5-sunburst` | OpenAI | OpenAI's most capable model (the ChatGPT image family): precise edits, masks, transparent backgrounds, strong instruction following, distinctive illustration style. |
| `gpt-fast` | `gpt-image-2.5-flare` | OpenAI | OpenAI's fastest high-quality model: drafts, variations, everyday images. |
| `nb2` / `lite` | `gemini-3.1-flash-image` / `gemini-3.1-flash-lite-image` | Google | 512px drafts (`nb2`); bulk throwaway images (`lite`). |

Full model IDs also work (`gpt-image-2`, `chatgpt-image-latest`, ...); IDs starting with `gpt-image` or `chatgpt-image` go to OpenAI, everything else to Google.

## Choosing a Model

Pick from the first row that matches the request. If none does, use `nb`.

| The request needs... | Use | Why |
|----------------------|-----|-----|
| A transparent background (logo, sticker, icon, cutout, game sprite, UI asset) | `gpt` | Nano Banana cannot output transparency. |
| A change to one region of an existing image while everything else stays pixel-stable | `gpt` with `--mask` | Masked editing; Sunburst is tuned for editing precision. |
| Several options to choose from in one go | `gpt-fast -n 4` | Batches of up to 10 variations; Nano Banana returns one image per call. |
| Facts from the real world: current events, weather, real products or places | `nb --search` | Only Nano Banana has Google Search grounding. |
| The same character or product across a series, or many reference images | `nb` | Up to 14 references, consistent likeness for up to 4 people. |
| Lots of legible text: infographics, menus, posters with body copy, labeled diagrams | `pro` | Google's recommendation for professional text-heavy assets. |
| Ultra-wide or tall strips (4:1, 8:1, 1:4, 1:8) or true 4K | `nb` | GPT sizes are limited to ratios between 1:3 and 3:1. |
| Iterating on a result over several turns ("warmer light, keep everything else") | `nb --continue <id>` | Server-side context carries composition and identity between turns. |
| An exact pixel size (e.g. `1536x864`) or WebP output | `gpt` | Custom `WIDTHxHEIGHT` sizes and `.webp` are GPT-only. |
| The ChatGPT look, or the user names ChatGPT, DALL-E, GPT, or OpenAI | `gpt` | |
| Cost-sensitive bulk generation | `nb` (or `lite`) | Cheapest per image. |

**Bake-off for important assets.** For a hero image, brand illustration, or anything the user will publish, generate with both `nb` and `gpt` from the same prompt (`-o hero-nb.png` and `-o hero-gpt.png`), look at both, and present them side by side with your recommendation. The two families have different strengths and aesthetics, so a comparison is often worth the extra call.

If only one provider's API key is configured, use that provider and mention what the other would have added when it matters (for example, transparency).

## Run the Script

Prefer a heredoc so quotes and apostrophes in the prompt never break the shell:

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/generate_image.py - -o public/images/hero.png -a 16:9 -s 2K <<'PROMPT'
A wide editorial photograph of a ceramicist's sunlit studio at golden hour...
PROMPT
```

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/generate_image.py - -m gpt --background transparent -o public/logo.png <<'PROMPT'
A friendly fox-head mascot logo, flat vector style, warm orange and cream, bold clean outlines.
PROMPT
```

`uv run` installs both SDKs automatically. Without uv, use `python3` (3.10+) after `python3 -m pip install -U "google-genai>=2.3,<3" "openai>=2,<4"`.

### Flags for both providers

| Flag | Values | Notes |
|------|--------|-------|
| `-m` | `nb`, `pro`, `gpt`, `gpt-fast`, `nb2`, `lite`, or a model ID | Default `nb`. |
| `-o` | `.png`, `.jpg`, `.jpeg` (`.webp` for GPT) | Default `generated_image.png`. Never overwrites: appends `-1`, `-2`. Creates folders. |
| `-a` | `1:1 2:3 3:2 3:4 4:3 4:5 5:4 9:16 16:9 21:9`; Nano Banana also `1:4 4:1 1:8 8:1` | |
| `-s` | Google: `512` (nb2 only), `1K`, `2K`, `4K`. GPT: `1K`, `2K`, `4K`, `auto`, or `WIDTHxHEIGHT` | GPT presets: 1K ≈ 1.5 MP, 2K = 2560×1440 area, 4K = 3840×2160 (above 2560×1440 is experimental). Custom sizes need multiples of 16. |
| `-e` | image path, repeatable | Inputs to edit, combine, or use as references (Google up to 14, GPT up to 16). |

### Google-only flags

| Flag | Values | Notes |
|------|--------|-------|
| `--search` | | Google Search grounding. Writes a `.search.html` attribution file to show the user. |
| `--thinking` | `nb`: `minimal medium high`; `nb2`/`lite`: `minimal high` | Higher helps complex compositions. |
| `--continue` | interaction ID | Refine the previous result conversationally. |

### GPT-only flags

| Flag | Values | Notes |
|------|--------|-------|
| `--background` | `transparent`, `opaque`, `auto` | Transparent needs `.png` or `.webp` output. |
| `--mask` | PNG with an alpha channel, same size as the first `-e` image | Transparent pixels mark the area to repaint. Masks guide the model; edges are not pixel-exact. |
| `--quality` | `low`, `medium`, `high`, `xhigh`, `max`, `auto` | Default `auto`. `low` for drafts; `xhigh`/`max` only on the 2.5 models and cost more tokens. |
| `-n` | 1–10 | Variations, saved as `name.png`, `name-1.png`, ... |

The script validates every combination before calling an API, retries on rate limits, and prints the saved paths plus either an **Interaction ID** (Google) or the **token usage and estimated cost** (GPT).

## Workflow

1. **Clarify only what matters**: purpose (where the image will appear), aspect ratio, style, and whether it needs transparency. Infer sensible defaults rather than interrogating the user. Save into the project's asset folder (`public/`, `assets/`, `static/`) when building a site.
2. **Choose the model** with the table above, write a narrative prompt, run the script.
3. **Look at the result**: open each saved file with the Read tool and check it against the request (composition, text spelling, artifacts, edges of transparent cutouts).
4. **Refine**:
   - Nano Banana: `--continue <id>` with only the change.
   - GPT: pass the image back with `-e`, describe the change and what must stay the same; add `--mask` to confine it to one region.
   - Start fresh when the direction is wrong, or switch families if one keeps missing.
5. **Report** the file paths, which model you used and why, and any trade-offs.

## Prompting

Both families respond best to a flowing description, never a keyword list. Weave in what matters:

`[subject + materials] + [action] + [setting] + [composition / camera] + [lighting] + [style / medium / color grade] + [purpose]`

- **Be hyper-specific**: "ornate elven plate armor etched with silver leaf, high collar, falcon-wing pauldrons", not "fantasy armor".
- **State the purpose**: "a hero image for a minimalist skincare brand's landing page" steers the whole result.
- **Use camera language**: wide-angle, macro, low-angle, 85mm portrait lens, shallow depth of field (f/1.8), medium-format film grain.
- **Phrase negatives positively**: "an empty, deserted street", not "no cars".
- **Text in images**: quote the exact words and describe the font. Keep it short with `nb` and `gpt`; use `pro` for dense copy.
- **Leave room for UI**: "generous negative space on the left third for a headline" for hero and banner images.
- **Transparent assets** (GPT): describe the subject alone ("a single isolated mascot, no backdrop"), set `--background transparent`, and check the edges after generation.

For edits, lead with the action and protect what must not change: "Using the provided image, change only the blue sofa to a brown leather Chesterfield. Keep everything else exactly the same, preserving the lighting and composition."

Templates for photorealism, stickers, text and logos, product shots, minimalist backgrounds, comics, inpainting, style transfer, composition, detail preservation, and character turnarounds are in [references/prompting-guide.md](references/prompting-guide.md). They work with both families.

## JSON Wrapper (optional)

Settings can travel inside the prompt as JSON; `config` keys mirror the flags (`model`, `output`, `size`, `aspect_ratio`, `edit`, `search`, `thinking`, `continue`, `quality`, `background`, `mask`, `n`):

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/generate_image.py - <<'PROMPT'
{"prompt": "A bold event poster on a deep cherry background with the words \"URBAN EXPLORER\" in a heavy condensed sans-serif.",
 "config": {"model": "pro", "aspect_ratio": "2:3", "size": "2K", "output": "poster.png"}}
PROMPT
```

## Cost

- **Nano Banana** (per image, Oct 2026): `nb` about $0.034 at 1K and $0.11 at 4K; `pro` about $0.13 at 1K–2K and $0.24 at 4K; `nb2` $0.045 at 512px.
- **GPT Image 2.5** is billed by tokens: $30 per 1M image output tokens, $8 per 1M image input tokens, $5 per 1M text input tokens. Cost grows with size, quality, and `-n`. The script prints the actual usage and estimate after each call; use `--quality low` while exploring.

## Limits

- No seeds on either provider.
- Nano Banana has no transparency or batches; GPT has no search grounding, no multi-turn `--continue`, and no ratios beyond 3:1.
- GPT Image can take up to two minutes for complex prompts. OpenAI may require **organization verification** before GPT Image models work on an API key.
- Both providers refuse some requests involving real people, minors, or explicit content; rephrase rather than retrying unchanged.
- All Nano Banana output carries an invisible SynthID watermark.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `GEMINI_API_KEY not found` / `OPENAI_API_KEY not found` | Add the key to the environment, `.env`, `.claude/.env`, or `~/.claude/.env` ([Google key](https://aistudio.google.com/apikey), [OpenAI key](https://platform.openai.com/api-keys)). |
| `Python 3.10+ is required` / SDK not installed or too old | Use `uv run`, or reinstall the SDKs with the pip command above. |
| HTTP 403 with a GPT model | Complete organization verification in the OpenAI dashboard, then retry. |
| `No image was returned` | Usually a safety or moderation block; rephrase. |
| HTTP 404 on a model | The model ID was retired. Check https://ai.google.dev/gemini-api/docs/models or https://developers.openai.com/api/docs/models and update `MODELS` in the script. |
| Misspelled text | Switch to `-m pro`, quote the exact words, keep text short. |
| Halo or fringe around a transparent cutout | Regenerate with `--quality high` and describe a clean, isolated subject. |

## Related Skills

- **`generate-svg`**: icons, logos, and illustrations that must scale or be themed with CSS.
- **`generate-video`**: animate a generated image into a short clip (pass it with `-i`).
- **`frontend-design`**: art direction and integrating images into a page.
