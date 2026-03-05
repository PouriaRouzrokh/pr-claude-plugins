# SVG Best Practices Reference

## ViewBox and Dimensions

Always declare both viewBox and explicit dimensions:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" width="1200" height="600" aria-hidden="true">
```

- `viewBox` defines the internal coordinate system
- `width`/`height` set the default rendered size
- For responsive SVGs, remove `width`/`height` and keep `viewBox`

## Path Optimization

- Minimize anchor points — fewer points = smaller files and smoother curves
- Merge overlapping paths that share the same fill/stroke
- Use relative path commands (`m`, `l`, `c`) over absolute (`M`, `L`, `C`) for smaller file sizes
- Remove unnecessary precision — `d="M10.00 20.00"` → `d="M10 20"`
- Combine consecutive line segments into polylines when possible

## Hero Section Design Patterns

### Gradients
```xml
<defs>
  <linearGradient id="svg-hero-bg" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#0a1628" />
    <stop offset="100%" stop-color="#1e40af" />
  </linearGradient>
</defs>
```

### Geometric Shapes
- Use overlapping circles with low opacity for depth
- Floating geometric elements (triangles, hexagons) at various sizes
- Grid patterns with varying opacity for tech feel
- Diagonal lines for energy and movement

### Negative Space
- Leave 30-40% of the hero as open space for text overlay
- Use gradients to fade elements toward the text zone
- Group decorative elements to the sides/corners

### Large Typography Integration
- Reserve a clear zone (typically center or left-center) for heading text
- Use subtle background shapes to frame the text area
- Ensure contrast ratio >= 4.5:1 against all background areas

## Accessibility

### Decorative SVGs
```xml
<svg aria-hidden="true" role="presentation">
```

### Meaningful SVGs
```xml
<svg role="img" aria-labelledby="svg-title svg-desc">
  <title id="svg-title">Chart showing quarterly growth</title>
  <desc id="svg-desc">Bar chart with Q1 at 20%, Q2 at 35%, Q3 at 50%, Q4 at 65%</desc>
</svg>
```

## Performance

### Inline vs External
- **Inline** (< 4KB): Eliminates network request, renders immediately
- **External** (> 4KB): Cacheable, preload with `<link rel="preload" as="image" href="icon.svg">`

### Compression
- SVG compresses excellently with Brotli (70-80% reduction)
- Use svgo for structural optimization before compression
- Remove metadata, comments, and editor artifacts

### Critical Rendering
- Inline above-the-fold SVGs (heroes, logos) directly in HTML
- Lazy-load below-the-fold SVGs with `loading="lazy"` on `<img>` tags

## Responsive Design

### Fluid SVGs
```css
svg {
  width: 100%;
  height: auto;
}
```

- Preserve `viewBox`, remove fixed `width`/`height`
- Use `preserveAspectRatio="xMidYMid meet"` (default) for uniform scaling
- Use `preserveAspectRatio="none"` for stretching to container

### Breakpoint Variations
- Consider separate SVGs for mobile (simplified) and desktop (detailed)
- Use CSS `@media` inside `<style>` within SVG for responsive internal styles

## Icon Design

### Size Testing
Design icons to work at multiple sizes:
- 16px: Must be recognizable — reduce to essential shape
- 24px: Standard size — include primary details
- 48px: Add secondary details
- 100px+: Full detail level

### Consistency
- Consistent stroke width (typically 1.5-2px at 24x24)
- Consistent corner radius
- Optical alignment (visual center, not mathematical center)
- 2px padding within the viewBox boundary

### Grid System
```
24x24 grid:
- 2px outer padding
- 20x20 active drawing area
- Align to full or half pixels
```

## Color Strategy

### currentColor
```xml
<svg fill="currentColor">
  <path d="..." />
</svg>
```
Inherits the CSS `color` property — perfect for icons that should match text color.

### CSS Custom Properties
```xml
<svg>
  <style>
    .primary { fill: var(--color-primary, #1e40af); }
    .accent { fill: var(--color-accent, #06b6d4); }
  </style>
  <rect class="primary" ... />
  <circle class="accent" ... />
</svg>
```

### Dark Mode Support
```xml
<style>
  @media (prefers-color-scheme: dark) {
    .bg { fill: #1a1a2e; }
    .text { fill: #e2e8f0; }
  }
</style>
```

## CSS Animation Patterns

Always prefer CSS `@keyframes` inside a `<style>` block over SMIL `<animate>`. Prefix all animation names with `svg-`.

### Pulse (Scale/Opacity Oscillation)
```xml
<style>
  @keyframes svg-pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.15); opacity: 0.7; }
  }
  .svg-pulse { animation: svg-pulse 3s ease-in-out infinite; transform-origin: center; }
  .svg-pulse-delay-1 { animation-delay: 0.4s; }
  .svg-pulse-delay-2 { animation-delay: 0.8s; }
</style>
<circle class="svg-pulse" cx="100" cy="100" r="8" fill="#06b6d4" />
<circle class="svg-pulse svg-pulse-delay-1" cx="200" cy="100" r="8" fill="#06b6d4" />
```
Best for: network nodes, buttons, notification dots, highlight elements.

### Float (Vertical Hover)
```xml
<style>
  @keyframes svg-float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-12px); }
  }
  .svg-float { animation: svg-float 4s ease-in-out infinite; }
  .svg-float-slow { animation: svg-float 6s ease-in-out infinite; }
</style>
<g class="svg-float" transform="translate(500, 200)">
  <rect width="200" height="120" rx="12" fill="..." />
</g>
```
Best for: floating cards, UI elements, decorative shapes.

### Glow Cycle (Light Effects)
```xml
<style>
  @keyframes svg-glow-cycle {
    0%, 100% { opacity: 0.3; filter: blur(4px); }
    50% { opacity: 0.8; filter: blur(8px); }
  }
  .svg-glow { animation: svg-glow-cycle 3s ease-in-out infinite; }
</style>
<circle class="svg-glow" cx="600" cy="300" r="80" fill="#00f5ff" />
```
Best for: orbs, neon accents, ambient light effects, halos.

### Dash Flow (Line Drawing / Data Flow)
```xml
<style>
  @keyframes svg-dash-flow {
    0% { stroke-dashoffset: 200; }
    100% { stroke-dashoffset: 0; }
  }
  .svg-dash { stroke-dasharray: 10 15; animation: svg-dash-flow 4s linear infinite; }
</style>
<path class="svg-dash" d="M100,300 C300,100 500,500 700,300" stroke="#06b6d4" fill="none" />
```
Best for: network connections, data flow lines, progress indicators.

### Rotate (Continuous Spin)
```xml
<style>
  @keyframes svg-rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
  .svg-rotate { animation: svg-rotate 20s linear infinite; transform-origin: center; }
</style>
<g class="svg-rotate" transform="translate(600, 300)">
  <circle r="100" fill="none" stroke="#1e40af" stroke-dasharray="20 10" />
</g>
```
Best for: orbital rings, loading spinners, decorative rotating elements.

### Fade-in with Stagger (Sequential Reveal)
```xml
<style>
  @keyframes svg-fade-in {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .svg-stagger { opacity: 0; animation: svg-fade-in 0.6s ease-out forwards; }
  .svg-stagger:nth-child(1) { animation-delay: 0s; }
  .svg-stagger:nth-child(2) { animation-delay: 0.15s; }
  .svg-stagger:nth-child(3) { animation-delay: 0.3s; }
</style>
```
Best for: particles appearing, list items, sequential element reveals.

### Accessibility: Reduced Motion
**Always include this** when using animations:
```xml
<style>
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation: none !important;
      transition: none !important;
    }
  }
</style>
```

### Animation Timing Guidelines
| Duration | Use Case |
|----------|----------|
| 0.3-0.6s | Micro-interactions, fade-ins, hovers |
| 1-2s | Loading spinners, progress indicators |
| 2-4s | Ambient pulse, glow cycling |
| 4-6s | Floating elements, slow rotations |
| 10-20s+ | Very slow orbital rotations, background drift |

Use `ease-in-out` for most animations. Use `linear` for continuous rotations and dash flows.

## svgo Configuration

Recommended svgo settings for production:

```yaml
# svgo.config.js
export default {
  plugins: [
    'preset-default',
    'removeDimensions',      # For responsive SVGs
    'sortAttrs',
    { name: 'removeAttrs', params: { attrs: ['data-name'] } }
  ]
}
```

For icons, keep `removeViewBox` disabled (it's disabled by default in preset-default).
