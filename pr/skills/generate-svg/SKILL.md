---
name: generate-svg
description: Generate SVG graphics (hero sections, icons, illustrations, logos, UI components) using Gemini 3.1 Pro. Triggers on "generate an SVG", "create a vector", "make an icon as SVG", "design a hero illustration", or any scalable vector content request.
allowed-tools: Bash(python*), Bash(node*), Bash(pip*), Bash(npm*), Bash(npx*)
---

# SVG Generation with Gemini 3.1 Pro

Generate production-quality SVG graphics using `gemini-3.1-pro-preview` as a text model. The model generates SVG code directly — no image generation API needed.

## IMPORTANT: Default Prompting Behavior

**When invoking this skill, ALWAYS construct a JSON prompt that includes BOTH the creative description AND a `config` key** to control all generation parameters. The script extracts `config` before sending the rest to the model. This gives Claude full control over type, dimensions, output path, and optimization — nothing is hardcoded.

Build a single JSON object from the user's request:

```python
import json
prompt = json.dumps({
    "description": "main visual description",
    "elements": ["geometric shapes", "gradients", "floating particles"],
    "colors": {
        "primary": "#1e40af",
        "secondary": "#7c3aed",
        "accent": "#06b6d4",
        "background": "deep navy to purple gradient"
    },
    "layout": {
        "negative_space": "center-left for text overlay",
        "depth": "3 layers: background grid, mid shapes, foreground bokeh"
    },
    "style": "glassmorphic with geometric patterns",
    "config": {
        "output": "hero.svg",
        "type": "hero",
        "width": 1200,
        "height": 600,
        "optimize": False
    }
})
```

Then pass the serialized JSON string as the single prompt argument:

```bash
python scripts/generate_svg.py '<json_string>'
```

**Config keys** (all optional — omit any that aren't needed):
| Key | Values | Description |
|-----|--------|-------------|
| `output` | any filename | Output path (default: generated.svg) |
| `type` | `hero`, `icon`, `illustration`, `logo`, `component` | SVG type (affects style guidance) |
| `width` | integer | SVG width in pixels |
| `height` | integer | SVG height in pixels |
| `optimize` | `true`/`false` | Run svgo optimization |

**Creative prompt keys** (include all that are relevant):
| Key | Purpose |
|-----|---------|
| `description` | Main visual description of what to generate |
| `elements` | List of specific shapes, patterns, objects to include |
| `colors` | Color palette with named roles (primary, accent, background) |
| `layout` | Spatial arrangement, negative space, depth layers |
| `style` | Design language (glassmorphic, minimal, organic, detailed) |
| `animation` | Animation instructions (see Animation section below) |

For simple requests (e.g., "gear icon"), a plain text prompt is acceptable — the script handles both JSON and plain text. Always infer appropriate type and dimensions from context.

## Setup

The scripts automatically load `GEMINI_API_KEY` from: environment variable → `.env` in the project root → `.claude/.env` in the project root → `~/.claude/.env`. If none found, ask the user for their API key.

Verify the API key:

```bash
[ -n "$GEMINI_API_KEY" ] && echo "API key configured" || echo "Missing GEMINI_API_KEY"
```

Install dependencies:

```bash
# Python
pip install google-genai

# JavaScript
npm install @google/genai

# Optional: SVG optimization
npm install -g svgo
```

## Script Usage

### Python

```bash
python scripts/generate_svg.py "description" [options]
```

### JavaScript

```bash
node scripts/generate_svg.mjs "description" [options]
```

### Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Output filename (default: generated.svg) |
| `-t, --type` | SVG type: hero, icon, illustration, logo, component |
| `--width` | SVG width in pixels (default varies by type) |
| `--height` | SVG height in pixels (default varies by type) |
| `--optimize` | Run svgo optimization on output |

## Type Defaults

| Type | Width | Height | Description |
|------|-------|--------|-------------|
| hero | 1200 | 600 | Hero section illustrations with gradients and geometry |
| icon | 24 | 24 | Minimal icons, consistent stroke width |
| illustration | 800 | 600 | General illustrations |
| logo | 200 | 200 | Logo marks and wordmarks |
| component | 400 | 300 | UI components and widgets |

## Examples

### Hero Section

```bash
python scripts/generate_svg.py \
  "Modern tech startup hero: abstract geometric shapes, gradient circles, floating code brackets, central glowing orb. Deep navy to electric blue gradient with cyan and white accents." \
  -t hero -o hero.svg --width 1200 --height 600
```

### Icon

```bash
python scripts/generate_svg.py \
  "Settings gear icon, clean lines, rounded corners" \
  -t icon -o settings.svg
```

### Logo

```bash
python scripts/generate_svg.py \
  "Minimalist mountain peak logo for an outdoor brand, single continuous line" \
  -t logo -o mountain_logo.svg --width 300 --height 300
```

### UI Component

```bash
python scripts/generate_svg.py \
  "Loading spinner with three rotating dots, CSS animation ready" \
  -t component -o spinner.svg
```

## Animation

SVGs can include CSS animations via a `<style>` block. Animation is **not mandatory** — include it when it adds value (hero sections, loading spinners, interactive elements). Skip it for static assets (logos, icons for print).

### Requesting Animation via JSON

Add an `animation` key to the creative prompt:

```python
import json
prompt = json.dumps({
    "description": "AI dashboard hero with neural network",
    "elements": ["pulsing nodes", "flowing data lines", "floating cards"],
    "animation": {
        "nodes": "pulse — gentle scale oscillation, staggered delays",
        "data_lines": "dash — stroke-dashoffset flow along paths",
        "cards": "float — subtle vertical hover, 3-5s duration",
        "particles": "fade-in — opacity 0 to 1 with staggered 0.2s delays",
        "glow": "glow-cycle — opacity oscillation on light effects"
    },
    "config": {"type": "hero", "width": 1200, "height": 600, "output": "hero.svg"}
})
```

### Available Animation Patterns

| Pattern | Effect | Best For |
|---------|--------|----------|
| `pulse` | Scale or opacity oscillation | Nodes, buttons, highlights |
| `float` | Vertical translateY oscillation | Cards, floating elements |
| `glow-cycle` | Opacity cycling on glow effects | Light orbs, neon accents |
| `rotate` | Continuous rotation | Spinners, orbital elements |
| `dash` | stroke-dashoffset animation | Data flow lines, drawing effects |
| `fade-in` | Opacity 0 → 1 with delay | Sequential reveals, particles |

### Animation Best Practices

- Use CSS `@keyframes` inside `<style>`, not SMIL `<animate>`
- Prefix animation names with `svg-` (e.g., `svg-pulse`, `svg-float`)
- Keep durations smooth: 2-6 seconds with `ease-in-out`
- Stagger similar elements with `animation-delay`
- Always include accessibility: `@media (prefers-reduced-motion: reduce) { ... }`
- Use `infinite` for ambient animations, finite counts for one-time effects

## SVG Best Practices

The scripts enforce these practices via system instructions:

- Always include `viewBox`, `xmlns`, and explicit dimensions
- Use meaningful IDs for animation support
- Keep paths simple and optimized
- Include `aria-hidden="true"` for decorative SVGs
- Use `currentColor` where appropriate for theme support
- Test icons at 16px, 24px, 48px, and 100px+

## Optimization

Use `--optimize` to run svgo on the output:

```bash
python scripts/generate_svg.py "chart icon" -t icon -o chart.svg --optimize
```

This reduces file size by 20-60% while preserving visual fidelity.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Missing API key | Set `GEMINI_API_KEY` in env, `.env`, `.claude/.env`, or `~/.claude/.env` |
| No SVG extracted | Model may have returned prose — retry with simpler prompt |
| svgo not found | Install with `npm install -g svgo` |
| Broken rendering | Check viewBox matches width/height dimensions |
| Missing gradients | Ensure `<defs>` block is present in output |

## Related Skills

- **`frontend-design`**: Use for design direction, layout decisions, and integrating SVGs into a larger frontend. Includes a raster vs vector decision table.
- **`generate-image-nb`**: Use for raster images (photos, textures, complex diagrams) via Gemini's image generation API.

## Reference

See `references/svg-best-practices.md` for detailed SVG design patterns and optimization techniques.
