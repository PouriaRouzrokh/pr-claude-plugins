---
name: generate-svg
description: Generates and edits SVG graphics (hero illustrations, UI icons, logo marks, illustrations, UI component graphics, CSS-animated loaders) by having a Gemini model write the markup, then validates, sanitizes, optionally optimizes with svgo, and renders a PNG preview for review. Use when the user asks for an SVG, a vector graphic, an icon, a logo mark, a scalable illustration, or an animated web graphic. For photographic or painterly images use generate-image instead.
argument-hint: "[description of the SVG to generate or edit]"
allowed-tools: Bash(uv run ${CLAUDE_SKILL_DIR}/scripts/generate_svg.py *) Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/generate_svg.py *)
---

# Generate SVG

Generate SVG markup with Gemini by running the bundled script. **Do not hand-write the SVG yourself** — the user chose this skill to get Gemini's output. You may make small follow-up fixes to the saved file (an id, a color, a stray attribute) after reviewing it.

## Models

| Alias | Model ID | Use for |
|-------|----------|---------|
| `flash` (default) | `gemini-3.8-flash` | Icons, logos, components, most illustrations. Fast and strong at code. |
| `pro` | `gemini-3.1-pro-preview` | Intricate illustrations and layered hero scenes. Slower; paid tier only. A **preview** model, so Google may change or retire it. |
| `argon` | `gemini-4-argon` | Gemini 4 Argon, Google's stable flagship reasoning model ("built for complex software engineering"). Paid tier only. |

Prices per 1M tokens, input / output (ai.google.dev pricing page, checked 2026-10-30): `flash` $0.75 / $3.75 through 2026-12-31, then $1.50 / $7.50; `pro` $2 / $12; `argon` $2 / $10 through 2026-11-30, then **$4 / $20 from 2026-12-01**. `flash` stays the default. Nobody has compared `argon` and `pro` on SVG quality yet, so offer `-m argon` for hard scenes and compare when it matters.

`--thinking low|medium|high` trades latency for care; use `high` for complex scenes.

## Run the Script

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/generate_svg.py - -t hero -o public/hero.svg --preview <<'PROMPT'
Abstract hero for a developer-tools startup: layered translucent ribbons flowing from the
lower right, a fine dot grid fading toward the top left, warm off-white background,
ink-blue and coral accents. Leave the left 45% calm for the headline.
PROMPT
```

`uv run` installs the dependencies (google-genai, resvg-py) automatically. Without uv, use `python3` (3.10+) after `python3 -m pip install -U "google-genai>=2.3,<3" resvg-py`.

| Flag | Values | Notes |
|------|--------|-------|
| `-t` | `hero`, `icon`, `illustration`, `logo`, `component` | Sets default size and type-specific design rules. Default `illustration`. |
| `-o` | path ending `.svg` | Default `generated.svg`. Never overwrites: appends `-1`, `-2`. |
| `--width`, `--height` | px (1-10000) | Defaults: hero 1200×600, icon 24×24, illustration 800×600, logo 200×200, component 400×300. |
| `-m` | `flash`, `pro`, `argon`, or a model ID | |
| `-e` | existing `.svg` | Edit mode: applies the description as changes and keeps the rest. |
| `--preview` | | Renders `<name>.preview.png` (min 512px wide) for visual review; never overwrites an existing preview. If the renderer cannot draw the SVG, the SVG is still saved and a warning is printed. |
| `--optimize` | | Runs `npx svgo` (needs Node.js); typically 20–60% smaller. |

The script rejects output that is not well-formed SVG (after one automatic repair request) and stops with a clear message when the model hits its output limit mid-document. It then parses the SVG and removes:

- the elements `<script>`, `<foreignObject>`, `<iframe>`, `<embed>`, `<object>`, `<audio>`, `<video>`, `<canvas>`, and any `<set>` or `<animate*>` that targets `href`;
- every `on*` event-handler attribute and any attribute value starting with `javascript:`;
- every `href` or `xlink:href` that is not an in-document `#fragment` (inline PNG/JPEG/GIF/WebP data on `<image>` is kept);
- CSS `@import` and external `url(...)` references (`url(#id)` and inline images stay).

Clean output is saved unchanged. This is a safety net, not a full sanitizer: review the file before embedding SVG from an untrusted prompt.

## Workflow

1. **Pick the type and size** from where the graphic will live. Match an existing icon set's grid and stroke width when the project has one.
2. **Write the description** (see below). For brand work, pass exact hex colors.
3. **Generate with `--preview`**, then open the PNG with the Read tool. Check composition, balance, legibility at the target size, and that negative space sits where text will go.
4. **Iterate with `-e <file.svg>`** for targeted changes ("thinner strokes", "move the orb left", "use the brand coral #F0644B"), or regenerate when the direction is wrong.
5. **Integrate**: inline small icons as React components or `<svg>` markup so `currentColor` works; reference large illustrations as files (`<img src>` or CSS background). Run `--optimize` on final assets.
6. **Clean up** the `.preview.png` files unless the user wants them.

## Writing the Description

Plain prose works for simple requests ("settings gear icon"). For richer pieces, a JSON prompt keeps the details organized; every key except `config` is sent to the model:

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/generate_svg.py - <<'PROMPT'
{
  "description": "AI dashboard hero with a quiet neural-network motif",
  "elements": ["5-7 nodes connected by thin curved lines", "two floating glass cards", "soft radial glow behind the cluster"],
  "colors": {"background": "#F7F5F2", "primary": "#1F3A5F", "accent": "#E86A33"},
  "layout": {"negative_space": "left half for the headline", "depth": "background grid, mid nodes, foreground cards"},
  "style": "editorial, restrained, precise geometry",
  "animation": {"nodes": "gentle pulse, staggered", "lines": "dash flow along paths, 4s"},
  "config": {"type": "hero", "output": "public/hero.svg", "preview": true}
}
PROMPT
```

`config` keys mirror the flags: `type`, `output`, `width`, `height`, `model`, `thinking`, `edit`, `optimize`, `preview`.

Guidance that produces better SVGs:

- **Name the role**: decorative backgrounds get `aria-hidden`; logos and standalone illustrations get `role="img"` and a `<title>` (the script's system prompt enforces this; say which it is when ambiguous).
- **Constrain the palette**: 3–5 colors with roles. Avoid the overused purple-to-blue "AI gradient" unless the brand calls for it.
- **Say where text goes** for heroes and banners.
- **Prefer geometry over detail**: SVG excels at clean shapes, gradients, and patterns. Photorealism belongs in `generate-image`.
- **Ask for animation explicitly** when you want it, and say which elements move. The script requires CSS keyframes and a `prefers-reduced-motion` fallback.

## Animation Patterns

| Pattern | Effect | Good for |
|---------|--------|----------|
| pulse | scale or opacity oscillation | nodes, highlights |
| float | slow translateY | cards, floating shapes |
| glow-cycle | opacity cycling on blurred shapes | orbs, accents |
| rotate | continuous rotation (`transform-box: fill-box`) | spinners, orbits |
| dash | `stroke-dashoffset` flow or draw-on | data lines, signatures |
| fade-in | staggered opacity reveal | particles, sequential reveals |

Keep loops at 2–6 s with ease-in-out, stagger repeated elements, and reserve infinite loops for ambient motion.

## References

- [references/svg-best-practices.md](references/svg-best-practices.md): viewBox, path optimization, accessibility, gradients, animation, and responsive techniques.
- [references/example_hero_output.svg](references/example_hero_output.svg): a sample hero output showing layered defs, gradients, and animation structure.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `GEMINI_API_KEY not found` | Add it to the environment, `.env`, `.claude/.env`, or `~/.claude/.env`. |
| `did not return a valid SVG` | Simplify the description or switch to `-m pro`; very long JSON prompts can truncate output. |
| Looks wrong at small sizes | Regenerate as `-t icon` (24×24 grid, 2px strokes) and preview at the real size. |
| Text renders in the wrong font | SVG text uses the viewer's fonts. Avoid text in logos, or convert it to outlined paths in a design tool. |
| Preview skipped | Run with `uv run` so resvg-py is available. |

## Related Skills

- **`generate-image`**: raster images (photos, painterly scenes, textures, text-heavy posters).
- **`frontend-design`**: art direction and integrating graphics into a page.
