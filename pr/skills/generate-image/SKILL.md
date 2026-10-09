---
name: generate-image
description: Generates and edits raster images (photos, illustrations, product shots, blog headers, thumbnails, banners, posters, infographics, stickers, textures) with Google's Nano Banana models through the Gemini API. Supports multi-image composition, inpainting-style edits, style transfer, accurate in-image text, Google Search grounding, and conversational refinement. Use when the user asks to generate, create, draw, design, edit, retouch, or restyle an image or picture. For scalable vector graphics (icons, logos, UI illustrations) use generate-svg instead.
argument-hint: "[description of the image to generate or edit]"
allowed-tools: Bash(uv run ${CLAUDE_SKILL_DIR}/scripts/generate_image.py *) Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/generate_image.py *)
---

# Generate Image (Nano Banana)

Generate and edit images by running the bundled script. **Never draw the image yourself** (no ASCII art, no hand-written SVG, no canvas code) — always call the Gemini API through the script.

## Models

| Alias | Model ID | Use for |
|-------|----------|---------|
| `nb` (default) | `gemini-nano-banana-2.1` | Almost everything. Best quality per dollar; 1K–4K; web + image search grounding. |
| `pro` | `gemini-3-pro-image` | Text-heavy work (posters, menus, infographics, wordmarks), style references, maximum fidelity. ~3× the cost. |
| `nb2` | `gemini-3.1-flash-image` | The only model with cheap 512px drafts (`-s 512`). |
| `lite` | `gemini-3.1-flash-lite-image` | Bulk or throwaway images; 1K only, no grounding. |

Approximate prices per image (Oct 2026): `nb` $0.034 at 1K / $0.11 at 4K; `pro` $0.13 at 1K–2K / $0.24 at 4K; `nb2` $0.045 at 512. Every image carries an invisible SynthID watermark.

## Run the Script

Prefer a heredoc so quotes and apostrophes in the prompt never break the shell:

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/generate_image.py - -o public/images/hero.png -a 16:9 -s 2K <<'PROMPT'
A wide editorial photograph of a ceramicist's sunlit studio at golden hour...
PROMPT
```

`uv run` installs the script's dependencies automatically. Without uv, use `python3` (3.10+) after `python3 -m pip install -U "google-genai>=2.3,<3"`.

| Flag | Values | Notes |
|------|--------|-------|
| `-o` | path ending `.png`, `.jpg`, `.jpeg` | Default `generated_image.png`. Never overwrites: appends `-1`, `-2`. Creates folders. |
| `-m` | `nb`, `pro`, `nb2`, `lite`, or a model ID | Default `nb`. |
| `-s` | `512` (nb2 only), `1K`, `2K`, `4K` | Default 1K. Use 2K for hero images, 4K only for print. |
| `-a` | `1:1 2:3 3:2 3:4 4:3 4:5 5:4 9:16 16:9 21:9`; `nb`/`nb2` also `1:4 4:1 1:8 8:1` | |
| `-e` | image path, repeatable (max 14) | Inputs to edit, combine, or use as references. |
| `--search` | | Ground on Google Search (current events, real products, weather). |
| `--thinking` | `nb`: `minimal medium high`; `nb2`/`lite`: `minimal high` | Higher helps complex compositions. |
| `--continue` | interaction ID | Refine the previous result conversationally. |

The script validates model/size/ratio combinations before calling the API, retries on rate limits, and prints the saved path plus an **Interaction ID**.

## Workflow

1. **Clarify only what matters**: purpose (where the image will appear), aspect ratio, and style. Infer sensible defaults rather than interrogating the user. Save into the project's asset folder (`public/`, `assets/`, `static/`) when building a site.
2. **Write a narrative prompt** (see below), pick the model, run the script.
3. **Look at the result**: open the saved file with the Read tool and check it against the request (composition, text spelling, artifacts, unwanted elements).
4. **Refine with `--continue <id>`** for targeted changes ("make the lighting warmer, keep everything else"). Thought signatures keep the context, so each turn only needs the change. Start fresh only when the direction is wrong.
5. **Report** the file path(s) and any trade-offs. When `--search` produced a `.search.html` file, tell the user it contains the required Google Search attribution.

## Prompting

Describe the scene in flowing prose; never send a keyword list. Weave in what matters:

`[subject + materials] + [action] + [setting] + [composition / camera] + [lighting] + [style / medium / color grade] + [purpose]`

- **Be hyper-specific**: "ornate elven plate armor etched with silver leaf, high collar, falcon-wing pauldrons", not "fantasy armor".
- **State the purpose**: "a hero image for a minimalist skincare brand's landing page" steers the whole result.
- **Use camera language**: wide-angle, macro, low-angle, 85mm portrait lens, shallow depth of field (f/1.8), medium-format film grain.
- **Phrase negatives positively**: "an empty, deserted street", not "no cars".
- **Text in images**: quote the exact words, describe the font, and use `-m pro`. For long copy, decide the text first, then request the image.
- **Leave room for UI**: "generous negative space on the left third for a headline" for hero and banner images.
- **Complex scenes**: give step-by-step instructions (background first, then foreground, then focal object).

For edits, lead with the action and protect what must not change: "Using the provided image, change only the blue sofa to a brown leather Chesterfield. Keep everything else exactly the same, preserving the lighting and composition."

Templates for photorealism, stickers, text and logos, product shots, minimalist backgrounds, comics, inpainting, style transfer, composition, detail preservation, and character turnarounds are in [references/prompting-guide.md](references/prompting-guide.md).

## JSON Wrapper (optional)

Settings can travel inside the prompt as JSON; `config` keys mirror the flags (`model`, `output`, `size`, `aspect_ratio`, `edit`, `search`, `thinking`, `continue`):

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/generate_image.py - <<'PROMPT'
{"prompt": "A bold event poster on a deep cherry background with the words \"URBAN EXPLORER\" in a heavy condensed sans-serif.",
 "config": {"model": "pro", "aspect_ratio": "2:3", "size": "2K", "output": "poster.png"}}
PROMPT
```

## Limits

- Up to 14 input images. `nb`/`nb2`: up to 10 objects and 4 people with consistent likeness. `pro`: up to 6 objects, 5 people, 3 style references.
- No transparent backgrounds, seeds, or multi-image batches: ask for "on a plain white background" and remove the background separately if needed.
- Search grounding on `nb`/`nb2` cannot use web images of real people.
- Requests involving real people, minors, or explicit content may be refused; rephrase rather than retrying unchanged.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `GEMINI_API_KEY not found` | Add it to the environment, `.env`, `.claude/.env`, or `~/.claude/.env` ([get a key](https://aistudio.google.com/apikey)). |
| `Python 3.10+ is required` / `google-genai is too old` | Use `uv run`, or `pip install -U "google-genai>=2.3,<3"`. |
| `No image was returned` | Usually a safety block; rephrase. The script prints any model text that explains why. |
| HTTP 404 on a model | The model ID was retired. Check https://ai.google.dev/gemini-api/docs/models and update `MODELS` in the script. |
| Misspelled text | Switch to `-m pro`, quote the exact words, keep text short. |

## Related Skills

- **`generate-svg`**: icons, logos, and illustrations that must scale or be themed with CSS.
- **`generate-video`**: animate a generated image into a short clip (pass it with `-i`).
- **`frontend-design`**: art direction and integrating images into a page.
