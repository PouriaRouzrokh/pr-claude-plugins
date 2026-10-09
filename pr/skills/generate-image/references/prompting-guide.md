# Nano Banana Prompting Guide

Templates and strategies adapted from Google's image-generation guide (ai.google.dev/gemini-api/docs/image-generation, October 2026). Fill the brackets, then expand into natural prose.

## Contents

- [Generation templates](#generation-templates)
- [Editing templates](#editing-templates)
- [Multi-turn refinement](#multi-turn-refinement)
- [Best practices](#best-practices)
- [Choosing size and ratio](#choosing-size-and-ratio)

## Generation templates

### Photorealistic scene

```
A photorealistic [type of shot] of a [subject description] in a [setting description].
[Description of the light]. Shot from a [camera angle] with a [lens type].
```

> A photorealistic close-up portrait of an elderly Japanese ceramicist with deep, sun-etched wrinkles and a warm smile, inspecting a freshly glazed tea bowl in his rustic, sun-drenched workshop. Soft golden-hour light streams through a window, highlighting the texture of the clay. Shot on an 85mm portrait lens with a softly blurred background. Serene, masterful mood.

### Stylized illustration or sticker

```
A [style] of a [subject, with details about accessories or actions] doing [activity].
The design features [visual qualities: bold outlines, cel-shading, ...] and [color/background preference].
```

> A kawaii-style sticker of a happy red panda wearing a tiny bamboo hat, munching on a green bamboo leaf. Bold, clean outlines, simple cel-shading, and a vibrant palette. The background must be white.

### Accurate text (use `-m pro`)

```
Create a [image type] for [brand/concept] with the text "[text to render]" in a [font style].
The design should be [style description], with a [color scheme].
```

> Create a modern, minimalist logo for a coffee shop called "The Daily Grind". The text is in a clean, bold sans-serif. Black and white, set inside a circle, with a coffee bean used cleverly in the mark.

### Product mockup

```
A high-resolution, studio-lit product photograph of a [product] on a [surface/background].
The lighting is a [setup, e.g. three-point softbox] to [purpose]. The camera angle is a
[angle] to showcase [feature]. Ultra-realistic, with sharp focus on [key detail]. [Aspect ratio].
```

### Minimalist background with negative space

```
A minimalist composition featuring a single [subject] positioned in the [bottom-right/top-left/...]
of the frame. The background is a vast, empty [color] canvas, creating significant negative space.
Soft, subtle lighting. [Aspect ratio].
```

Use for hero sections, slides, and banners where text will be overlaid.

### Sequential art (comic or storyboard)

```
Make a [N] panel comic in a [style]. Put the character in a [type of scene].
```

Pass a character reference with `-e`. Use `pro` or `nb2` for the most reliable text and storytelling.

### Search-grounded visual (`--search`)

> Visualize the current five-day weather forecast for San Francisco as a clean, modern chart, with an outfit suggestion for each day.

## Editing templates

### Add or remove an element

```
Using the provided image of [subject], please [add/remove/modify] [element] to/from the scene.
Ensure the change is [how it should integrate: lighting, perspective, style].
```

### Inpainting (semantic mask)

```
Using the provided image, change only the [specific element] to [new element/description].
Keep everything else in the image exactly the same, preserving the original style, lighting, and composition.
```

### Style transfer

```
Transform the provided photograph of [subject] into the artistic style of [artist/style].
Preserve the original composition but render it with [stylistic elements].
```

### Combine images

```
Create a new image by combining the elements from the provided images. Take the [element from image 1]
and place it with/on the [element from image 2]. The final image should be a [description of the scene].
```

### Preserve critical details (faces, logos)

```
Using the provided images, place [element from image 2] onto [element from image 1]. Ensure that the
features of [element from image 1] remain completely unchanged. The added element should [integration].
```

Describe the protected subject in detail (hair, eyes, expression) so the model anchors on it.

### Sketch to finished image

```
Turn this rough [medium] sketch of a [subject] into a [style description] photo.
Keep the [specific features] from the sketch but add [new details/materials].
```

### Character turnaround (360°)

```
A studio portrait of [person] against [background], [looking forward / in profile looking right / ...].
```

Generate one angle at a time and include previous outputs as `-e` references to keep the likeness consistent.

## Multi-turn refinement

Every run prints an Interaction ID. Pass it back to make targeted changes without restating the scene:

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/generate_image.py "Keep everything the same, but make the lighting warmer and the expression more serious." --continue <id> -o portrait-v2.png
```

The API keeps the visual context (thought signatures) between turns, which preserves composition and identity far better than re-prompting from scratch.

## Best practices

- **Hyper-specific beats generic.** Name materials, textures, colors, and era.
- **Give context and intent.** "For a high-end, minimalist skincare brand" changes every decision the model makes.
- **Iterate in small steps.** "That's great, but make the lighting a bit warmer."
- **Use step-by-step instructions** for crowded scenes: background, then foreground, then the focal object.
- **Semantic negatives.** Describe the desired absence: "an empty, deserted street with no signs of traffic."
- **Control the camera.** Wide-angle, macro, low-angle, bird's-eye, shallow depth of field.
- **Text first, image second.** For text-heavy images, settle the exact copy before generating.
- **Languages.** Best results in EN, ar-EG, de-DE, es-MX, fr-FR, hi-IN, id-ID, it-IT, ja-JP, ko-KR, pt-BR, ru-RU, ua-UA, vi-VN, zh-CN.

## Choosing size and ratio

| Destination | Ratio | Size |
|-------------|-------|------|
| Website hero / blog header / YouTube thumbnail | 16:9 or 21:9 | 2K |
| Open Graph / social card | 16:9 (crop to 1.91:1) | 1K |
| Instagram post | 1:1 or 4:5 | 1K–2K |
| Story / Reel / phone wallpaper | 9:16 | 2K |
| Poster / print | 2:3 or 3:4 | 4K |
| App icon or avatar draft | 1:1 | 512 (`nb2`) then 1K |
| Banner strip | 4:1 or 8:1 (`nb`/`nb2` only) | 2K |
