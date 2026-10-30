# SVG Best Practices

Read this reference when writing, editing, or reviewing SVG output. It follows the same rules as the system prompt in `scripts/generate_svg.py`, so generated files and hand edits stay consistent.

## Contents

- [Root element and scaling](#root-element-and-scaling)
- [Delivery: inline, img, or CSS](#delivery-inline-img-or-css)
- [Accessibility](#accessibility)
- [Structure and paths](#structure-and-paths)
- [Hero composition](#hero-composition)
- [Icons](#icons)
- [Color and theming](#color-and-theming)
- [CSS animation](#css-animation)
- [Animation patterns](#animation-patterns)
- [Optimizing with svgo](#optimizing-with-svgo)
- [Performance](#performance)

## Root element and scaling

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" width="1200" height="600"
     aria-hidden="true" focusable="false">
```

- `viewBox` defines the internal coordinate system and is what makes the graphic scale. Never remove it.
- `width` and `height` give the default rendered size and the intrinsic aspect ratio. Keep them on files used as `<img>`, where they let the browser reserve space before load and avoid layout shift.
- For fluid inline SVGs, keep the attributes and override them in CSS (`width: 100%; height: auto;`), or remove them when the container always sets the size.
- `preserveAspectRatio` defaults to `xMidYMid meet` (fit inside, uniform scale). Use `xMidYMid slice` for hero backgrounds that must cover their box. `none` distorts shapes; reserve it for patterns and shapes meant to stretch.
- Strokes scale with the `viewBox`. Add `vector-effect="non-scaling-stroke"` when a line must keep a constant width at any size.

## Delivery: inline, img, or CSS

| Method | Use for | Trade-offs |
|--------|---------|------------|
| Inline `<svg>` | Icons, logos, and graphics that follow page styles or are animated from page CSS | Inherits `currentColor` and CSS custom properties; adds HTML bytes and is not cached separately; ids must be unique across the page |
| `<img src="file.svg">` | Larger illustrations and heroes | Cached and lazy-loadable; isolated from page CSS, so `currentColor` and page custom properties do not reach inside; its own `<style>` animations still run; needs `alt` |
| CSS `background-image` | Purely decorative textures | No accessible name possible; not part of the LCP image discovery path |

## Accessibility

- **Decorative inline SVG** (hero backgrounds, patterns, icons next to visible text): `aria-hidden="true"` on the root, plus `focusable="false"` as the generator emits it. `focusable` only matters to legacy Edge and Internet Explorer, and svgo removes it as an unknown attribute; neither outcome causes harm. `role="presentation"` adds nothing next to `aria-hidden`.
- **Meaningful inline SVG** (logos, standalone icons, illustrations that carry information): `role="img"` on the root and a `<title>` as its first child. For a longer description, reference both elements with unique ids:

  ```xml
  <svg role="img" aria-labelledby="svg-growth-title svg-growth-desc" viewBox="0 0 400 300">
    <title id="svg-growth-title">Quarterly growth</title>
    <desc id="svg-growth-desc">Bar chart: Q1 20%, Q2 35%, Q3 50%, Q4 65%.</desc>
    <!-- ... -->
  </svg>
  ```

- **SVG as `<img>`**: the `alt` attribute is the accessible name, and the file's `<title>` is ignored. Use `alt=""` for decorative images.
- **Icon-only buttons**: hide the icon and name the button (`<button aria-label="Close"><svg aria-hidden="true" ...>`).
- **Text over a hero**: body text needs 4.5:1 contrast and large text (24 px, or 18.66 px bold) needs 3:1 against the busiest part of the graphic behind it. Meaningful graphic parts, such as chart lines, need 3:1 against their background.

## Structure and paths

- Put gradients, filters, patterns, clipPaths, and symbols in one `<defs>` block with descriptive ids (`svg-hero-bg`, not `a`).
- Use primitives (`circle`, `rect`, `line`, `polygon`) where they suffice; they are easier to read and edit than paths.
- Draw paths with as few anchor points as the shape needs, and round coordinates to at most 2 decimals.
- Leave relative commands and number formatting to svgo; it rewrites path data more reliably than hand edits.
- Merge paths only when they share fill and stroke and do not overlap with transparency, since overlapping translucent shapes look different once merged.

## Hero composition

- **Layers**: background (gradient), midground (shapes, patterns), foreground (focal elements), each in its own `<g>`.
- **Negative space**: leave 30–40% of the area open where the headline will sit (the generator defaults to the left half). Fade decorative elements toward that zone and cluster detail toward the opposite side or corners.
- **Contrast behind text**: keep shapes in the text zone low-contrast so the headline passes the ratios above.
- **Palette**: start from the product's brand colors. Without one, choose a deliberate palette rather than the default navy-to-electric-blue "tech" gradient with cyan and magenta glows. The bundled example uses ink `#16110f`, umber `#5b4a44`, terracotta `#e07a5f`, saffron `#f2cc8f`, and sage `#81b29a`:

```xml
<defs>
  <linearGradient id="svg-hero-bg" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#16110f" />
    <stop offset="100%" stop-color="#3a2622" />
  </linearGradient>
</defs>
```

See [example_hero_output.svg](example_hero_output.svg) for a complete layered, animated hero.

## Icons

The generator draws icons in the Lucide and Feather style:

- `viewBox="0 0 24 24"` with about 2 units of padding, leaving a 20×20 drawing area.
- `fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"` on the root.
- One to four simple paths or primitives. No text, gradients, or hard-coded colors.
- Check the result at 16 px (essential silhouette only), 24 px (standard), and 48 px. Keep stroke width and corner radius consistent across a set, and center shapes optically rather than mathematically.

## Color and theming

**currentColor** makes an inline icon follow the surrounding text color:

```xml
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
  <path d="..." />
</svg>
```

**CSS custom properties** with fallbacks make an inline component themable from page CSS (the generator's `component` type uses this form):

```xml
<svg viewBox="0 0 400 300">
  <rect class="svg-surface" fill="var(--svg-surface, #fff4e6)" ... />
  <circle class="svg-accent" fill="var(--svg-accent, #e07a5f)" ... />
</svg>
```

**Dark mode** inside the file responds to the user's color-scheme preference:

```xml
<style>
  @media (prefers-color-scheme: dark) {
    .svg-surface { fill: #16110f; }
    .svg-label { fill: #f2e8dc; }
  }
</style>
```

## CSS animation

The generator animates only when the description asks for motion, and follows these rules:

- **CSS, not SMIL.** Write `@keyframes` inside a `<style>` element. CSS animations can be switched off with `prefers-reduced-motion`; SMIL (`<animate>`) ignores it. SMIL is not deprecated and works in current browsers, so keep it for what CSS cannot do everywhere, such as morphing a path's `d` attribute, and provide a static fallback for reduced motion.
- **Prefix names** with `svg-` (`svg-pulse`, `svg-float`) so they do not collide with page CSS when inlined.
- **Animate cheap properties**: `transform`, `opacity`, and `stroke-dashoffset`. Animating `filter` (such as `blur()`) repaints every frame; apply a static `<filter>` once and animate `opacity` instead.
- **Set the transform origin.** SVG elements default to `transform-box: view-box`, so `transform-origin: center` means the center of the whole canvas. To scale or rotate a shape around its own center, set `transform-box: fill-box; transform-origin: center;`. For a group whose bounding box is off-center (a ring with a satellite), keep `view-box` and give the origin in user units (`transform-origin: 850px 300px`).
- **Keep transform attributes off animated elements.** A CSS `transform` animation replaces the element's `transform` attribute, so `<g class="svg-float" transform="translate(500 200)">` jumps to the origin. Wrapping it in a translated parent group is not reliable either, because svgo's `collapseGroups` moves the parent's transform onto a single child. Draw the shape at its final coordinates instead.
- **Make the resting state visible.** Reduced motion removes every animation, so an element whose base style is `opacity: 0` would never appear. Leave the base style visible and use `animation-fill-mode: both` (or `backwards`) to hide it during a delay.
- **Timing**: `ease-in-out` and 2–6 s for ambient motion, `linear` for rotations and dash flows, staggered `animation-delay` for repeated elements, and `infinite` only for ambient motion.

Always include the reduced-motion rule the generator uses:

```xml
<style>
  @media (prefers-reduced-motion: reduce) {
    * { animation: none !important; }
  }
</style>
```

| Duration | Use |
|----------|-----|
| 0.3–0.6 s | Entrance fades, hover feedback |
| 1–2 s | Spinners, progress indicators |
| 2–4 s | Ambient pulse, glow |
| 4–6 s | Floating elements |
| 10 s and longer | Slow orbits, background drift |

## Animation patterns

Each pattern below follows the rules above and works with the reduced-motion rule.

**Pulse** (network nodes, notification dots):

```xml
<style>
  @keyframes svg-pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.15); opacity: 0.7; }
  }
  .svg-pulse { animation: svg-pulse 3s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
  .svg-delay-1 { animation-delay: 0.4s; }
</style>
<circle class="svg-pulse" cx="100" cy="100" r="8" fill="#e07a5f" />
<circle class="svg-pulse svg-delay-1" cx="200" cy="100" r="8" fill="#e07a5f" />
```

**Float** (cards, decorative shapes), drawn at final coordinates with no `transform` attribute:

```xml
<style>
  @keyframes svg-float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-12px); }
  }
  .svg-float { animation: svg-float 4s ease-in-out infinite; }
</style>
<g class="svg-float">
  <rect x="500" y="200" width="200" height="120" rx="12" fill="#5b4a44" />
</g>
```

**Glow** (orbs, halos): blur once with a filter, animate only opacity:

```xml
<defs>
  <filter id="svg-soft-blur" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="8" />
  </filter>
</defs>
<style>
  @keyframes svg-glow { 0%, 100% { opacity: 0.3; } 50% { opacity: 0.8; } }
  .svg-glow { animation: svg-glow 3s ease-in-out infinite; }
</style>
<circle class="svg-glow" cx="600" cy="300" r="80" fill="#f2cc8f" filter="url(#svg-soft-blur)" />
```

**Dash flow** (connections, data lines). The offset distance is a multiple of the dash period (10 + 15 = 25), so the loop is seamless:

```xml
<style>
  @keyframes svg-dash-flow { to { stroke-dashoffset: -200; } }
  .svg-dash { stroke-dasharray: 10 15; animation: svg-dash-flow 4s linear infinite; }
</style>
<path class="svg-dash" d="M100 300C300 100 500 500 700 300" stroke="#e07a5f" fill="none" />
```

**Rotate** (orbital rings, spinners):

```xml
<style>
  @keyframes svg-rotate { to { transform: rotate(360deg); } }
  .svg-rotate { animation: svg-rotate 20s linear infinite; transform-box: fill-box; transform-origin: center; }
</style>
<circle class="svg-rotate" cx="600" cy="300" r="100" fill="none" stroke="#81b29a" stroke-dasharray="20 10" />
```

**Staggered entrance** (particles, sequential reveals). The base style stays visible; `both` hides each element only until its delay ends:

```xml
<style>
  @keyframes svg-fade-in {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .svg-stagger { animation: svg-fade-in 0.6s ease-out both; }
</style>
<circle class="svg-stagger" cx="80" cy="60" r="6" fill="#f2cc8f" />
<circle class="svg-stagger" cx="120" cy="60" r="6" fill="#f2cc8f" style="animation-delay: 0.15s" />
<circle class="svg-stagger" cx="160" cy="60" r="6" fill="#f2cc8f" style="animation-delay: 0.3s" />
```

## Optimizing with svgo

`generate_svg.py --optimize` runs `npx --yes svgo` with its default `preset-default` (svgo 4.x). Since svgo 4, that preset no longer includes `removeViewBox` or `removeTitle`, so scaling and accessible names survive; do not add either plugin back. `sortAttrs` is already part of the preset.

The defaults also:

- Remove `focusable="false"` (harmless, see [Accessibility](#accessibility)).
- Move CSS rules that match a single element into `style` attributes. Animations keep working, and the reduced-motion `!important` rule still overrides them.
- Merge a group's attributes into its single child (`collapseGroups`), which is why animated elements should not rely on a translated wrapper.
- Shorten ids only in files without a `<style>` element, so several inlined SVGs on one page can end up sharing ids such as `a`. Add `prefixIds` when inlining more than one.

For a project-level config:

```js
// svgo.config.mjs
export default {
  multipass: true,
  plugins: [
    'preset-default',
    'prefixIds', // unique ids and classes when several SVGs are inlined on one page
    // 'removeDimensions', // only when page CSS always sizes the SVG; keeps viewBox
  ],
};
```

Run it with `npx svgo --config svgo.config.mjs input.svg -o output.svg`, then re-check animations and the `--preview` render.

## Performance

- Serve SVG with Brotli or gzip; markup compresses very well.
- Inline small, above-the-fold graphics such as logos and icons. Serve large heroes as `<img>` with `width` and `height`, and add `fetchpriority="high"` only when the image is the page's LCP element.
- Lazy-load below-the-fold SVG images with `loading="lazy"`.
- Large blurred areas and many filtered, animated elements cost paint time on every frame. Limit how many animate at once, and check frame rate on a mid-range phone.
