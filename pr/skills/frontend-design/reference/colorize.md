# Colorize

Introduce color as hierarchy, meaning, and atmosphere. Preserve confirmed brand and semantic conventions; do not replace a visual world under the guise of colorizing it.

## Contents

- [Visitor mode](#visitor-mode)
- [Audit before choosing](#audit-before-choosing)
- [Choose a strategy](#choose-a-strategy)
- [Apply at system scale](#apply-at-system-scale)
- [Contrast and perception](#contrast-and-perception)
- [Verify](#verify)
- [Technical reference](#technical-reference)

## Visitor mode

- **Persuade + Experience:** color may carry the voice and own large regions when the selected world calls for it.
- **Operate + Read:** color primarily encodes action, selection, status, wayfinding, and reading hierarchy. Rarity gives an accent force.

## Audit before choosing

Read the project's design context (a `## Design Context` section in CLAUDE.md, or DESIGN.md if the project keeps one), tokens, assets, current themes, and representative states. Identify:

- which colors are confirmed brand commitments;
- current surface, text, action, and semantic roles;
- places where grayscale obscures hierarchy or state;
- contrast failures and color-only communication;
- light/dark or data-visualization requirements;
- whether the task asks for more color or a new identity.

If a new identity is required, use [new-work.md](new-work.md). Ask only when a binding brand decision cannot be inferred.

## Choose a strategy

Name the intended emotional temperature, dominant relationship, contrast range, and color dosage before editing. The strategy may be restrained or immersive; it must follow the brief and selected world rather than a fixed percentage rule.

Build roles, not a bag of swatches:

- canvas and elevated surfaces;
- primary and secondary text;
- action, focus, and selection;
- borders and separators;
- success, warning, error, and information;
- data categories or scales when needed.

Use the project's existing color space. For a new web palette, prefer OKLCH because lightness and chroma can be adjusted predictably. Choose hue from product meaning and visual direction, never from a default category association.

## Apply at system scale

- Let the strongest color own a deliberate region or role instead of scattering tiny accents.
- Keep the primary action easy to find; do not spend its color on decoration.
- Tint neutrals only when the brand hue genuinely creates cohesion. Neutral gray is valid when it serves the world. A faintly tinted near-black or warm off-white used by habit is one of the AI design clusters in SKILL.md; choose the dark or light surface's hue and lightness deliberately.
- On colored surfaces, derive secondary text from the foreground or surface hue rather than using washed-out generic gray.
- Keep semantic meanings consistent, but respect platform and domain conventions instead of assuming fixed hues.
- For data, use distinct lightness, chroma, shape, label, or pattern so color is not the only code.
- In dark mode, design surface elevation and contrast explicitly; do not invert the light theme mechanically.
- Define primitive values and semantic tokens when the project has a token system. Theme changes should normally remap semantic roles.

Decoration without a relationship to hierarchy, state, content, or the visual world is not a color strategy.

## Contrast and perception

Verify computed foreground/background pairs against WCAG 2.2 AA: 4.5:1 for body text, 3:1 for large text and for controls, icons, and focus indicators ([details](#contrast-details)).

Do not rely on eyesight alone. Check interactive states, overlays, text on images, disabled content, and both themes. Simulate common vision deficiencies. Information conveyed by color also needs text, shape, iconography, or position.

When deriving OKLCH ramps, vary lightness and reduce chroma near white and black. Do not keep high chroma at extreme lightness merely to make the math uniform. Prefer explicit colors over chains of translucent overlays when alpha would make contrast context-dependent.

## Verify

- Every color has a stable role or a world-specific atmospheric purpose.
- Attention lands on the intended action, content, or state.
- The palette works across quiet, dense, interactive, error, and empty states.
- Light and dark themes are each composed, not mechanically inverted.
- Contrast and non-color cues pass in all relevant states.
- The result is recognizably this product, not a generic “colorful” treatment.

When the palette earns its place, finish with a polish pass ([polish.md](polish.md)).

## Technical reference

Concrete values and patterns for applying the guidance above.

### OKLCH

OKLCH is perceptually uniform: equal lightness steps look equal, unlike HSL, where 50% lightness yellow looks far brighter than 50% blue.

```css
/* lightness (0-100%), chroma (0-0.4+), hue (0-360) */
--color-primary: oklch(60% 0.15 250);
--color-primary-light: oklch(85% 0.08 250); /* same hue, less chroma near white */
--color-primary-dark: oklch(35% 0.12 250);
```

Reduce chroma as lightness approaches white or black; high chroma at extreme lightness looks garish.

When the brand hue should run through the neutrals, a chroma of 0.005-0.01 is enough to read as cohesive without looking tinted:

```css
--neutral-100: oklch(95% 0.01 60);  /* warm */
--neutral-900: oklch(15% 0.01 250); /* cool */
```

### Palette roles

| Role | Purpose | Typical size |
|------|---------|--------------|
| Primary | Brand, primary actions | 1 color, 3-5 shades |
| Neutral | Text, backgrounds, borders | 9-11 step scale |
| Semantic | Success, error, warning, info | 4 colors, 2-3 shades each |
| Surface | Cards, overlays, panels | 2-3 elevation levels |

Skip secondary and tertiary brand colors unless a real role needs them. For a Restrained strategy, think in visual weight: roughly 60% neutral surfaces, 30% secondary tones (text, borders, inactive states), 10% accent (primary actions, highlights, focus). Accents work because they are rare.

### Contrast details

| Content | AA minimum | AAA target |
|---------|------------|------------|
| Body text | 4.5:1 | 7:1 |
| Large text (24px+, or 18.66px+ bold; WCAG's 18pt / 14pt bold) | 3:1 | 4.5:1 |
| UI components, icons, focus indicators | 3:1 | no AAA level |

Placeholder text still needs 4.5:1. Combinations that commonly fail: light gray on white, gray text on any colored surface (use a darker shade of that surface's hue), red against green, blue on red (vibrates), yellow on white, and thin light text over images. Test with the [WebAIM contrast checker](https://webaim.org/resources/contrastchecker/) and the browser's emulated vision deficiencies.

### Dark themes

| Light theme | Dark theme |
|-------------|------------|
| Shadows convey depth | Lighter surfaces convey depth |
| Dark text on light | Light text on dark; check rendered weight and add a little line height ([typeset.md](typeset.md#apply)) |
| Vibrant accents | Slightly desaturated accents |

```css
:root[data-theme="dark"] {
  --surface-1: oklch(15% 0.01 250);
  --surface-2: oklch(20% 0.01 250); /* "higher" surfaces are lighter */
  --surface-3: oklch(25% 0.01 250);
}
```

Use two token layers: primitives (`--blue-500`) and semantic roles (`--color-primary: var(--blue-500)`). A theme redefines only the semantic layer.

### Modern color functions

- **`light-dark()`** (Baseline 2024) picks a value from the element's `color-scheme`, so one declaration covers both themes. It needs `color-scheme: light dark` on `:root` (or a scoped element), which also themes native controls and scrollbars.
- **`color-mix()`** (Baseline widely available) derives hover states, borders, and tints without new primitives. Mix in `oklch` for predictable results.
- **Relative color syntax** (Baseline 2024) adjusts one channel of an existing token.
- **`contrast-color()`** (Baseline April 2026: Chrome 147, Firefox 146, Safari 26) returns black or white, whichever contrasts more with a given color, so text on a user-supplied or generated background (badges, tags, theme pickers) stays legible without a hand-set pair. It picks only black or white and does not guarantee a ratio, so still verify contrast on brand surfaces and check the result with the real palette.

```css
:root {
  color-scheme: light dark;
  --surface: light-dark(oklch(98% 0.005 80), oklch(17% 0.01 250));
  --text: light-dark(oklch(22% 0.01 250), oklch(93% 0.005 80));
  --accent: oklch(62% 0.17 35);
  --accent-hover: oklch(from var(--accent) calc(l - 0.06) c h);
  --accent-subtle: color-mix(in oklch, var(--accent) 12%, var(--surface));
}
:root[data-theme="light"] { color-scheme: light; } /* manual override */
:root[data-theme="dark"]  { color-scheme: dark; }
```
