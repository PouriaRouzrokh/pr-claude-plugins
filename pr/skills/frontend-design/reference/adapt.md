# Adapt

Adapt an existing design to a different context: another screen size, input method, or medium. Adaptation is rethinking the experience for the new context, not scaling pixels. Before starting, establish the target devices and usage context from the brief or the design context; ask only if they cannot be inferred.

This file covers the web, mobile web included. For native iOS or Android apps, follow the platform's own guidelines (Apple Human Interface Guidelines, Material Design).

## Contents

- [Assess](#assess)
- [Strategies by context](#strategies-by-context)
- [Techniques](#techniques)
- [Verify](#verify)

## Assess

1. **Source context:** what was it designed for, and what did that assume (large screen, mouse, fast connection)? What works well now?
2. **Target context:** device, input method (touch, mouse, keyboard, stylus), screen size and orientation, connection quality, and usage (on the go vs. at a desk, glance vs. focused reading).
3. **Challenges:** what won't fit, what won't work (hover on touch, small targets), and which patterns are wrong for the target.

## Strategies by context

| Context | Layout | Interaction | Content and navigation |
|---------|--------|-------------|------------------------|
| **Phone** | Single column, full-width components, vertical stacking | Targets of 44×44px where possible (24×24px is the WCAG 2.2 AA minimum), primary actions within thumb reach, bottom sheets for option lists | Progressive disclosure; primary content first; bottom navigation or a drawer; nothing core removed, only reorganized |
| **Tablet** | Two columns, master-detail, layouts that change with orientation | Touch and pointer both supported | Side panels for secondary content |
| **Desktop** | Multi-column, persistent side navigation, a max-width so content doesn't stretch across 4K screens | Hover for supplementary information (never essential), keyboard shortcuts, drag and drop, multi-select | More information up front; denser tables |
| **Print** | Logical page breaks (`break-inside: avoid` on figures and cards); hide navigation and interactive chrome | — | Print full URLs after links, expand collapsed sections, add title and date; use `@media print` and `@page` |
| **Email** | 600px wide, single column, table-based layout, inline CSS | Large button-style CTAs; no reliance on hover or scripts | Deep links into the app for anything complex |

Keep the same information architecture across contexts; users moving between devices should find things where they expect them.

## Techniques

### Mobile-first and content-driven breakpoints

Write base styles for the narrowest layout and layer complexity with `min-width` queries; additive overrides are simpler to reason about than undoing desktop styles. Let content choose breakpoints: widen the viewport until the design breaks and add one there. Three or so usually suffice (around 640, 768, and 1024px is a common starting set). Use `clamp()` for values that should scale smoothly, and container queries for components that appear in different-width slots ([layout.md](layout.md#container-queries)).

### Viewport units

Use the dynamic viewport units for full-height mobile layouts; `100vh` ignores the collapsing browser toolbar. These are Baseline widely available.

```css
.hero { min-height: 100svh; }      /* small viewport: never hidden behind browser UI */
.app-shell { height: 100dvh; }     /* tracks toolbar show/hide */
```

### Input method, not screen size

A touchscreen laptop and a tablet with a keyboard break the "small screen = touch" assumption. Query capabilities instead:

```css
@media (pointer: coarse) { .button { min-height: 44px; padding-inline: 20px; } }
@media (hover: hover) and (pointer: fine) { .card:hover { translate: 0 -2px; } }
```

Never put essential functionality behind hover; touch users cannot hover, and keyboard users need the same content on focus.

### Safe areas

Handle notches, rounded corners, and home indicators with `env()` once the viewport opts in:

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

```css
.footer { padding-bottom: max(1rem, env(safe-area-inset-bottom)); }
.header { padding-inline: max(1rem, env(safe-area-inset-left)) max(1rem, env(safe-area-inset-right)); }
```

### Responsive images

Use `srcset` with width descriptors and an accurate `sizes` so the browser picks a file for the layout width and pixel density; use `<picture>` only when the crop or composition changes (art direction).

```html
<img src="hero-800.jpg"
     srcset="hero-400.jpg 400w, hero-800.jpg 800w, hero-1200.jpg 1200w"
     sizes="(max-width: 768px) 100vw, 50vw"
     width="1200" height="800" alt="…">

<picture>
  <source media="(min-width: 768px)" srcset="wide.jpg">
  <img src="tall.jpg" width="800" height="1000" alt="…">
</picture>
```

### Layout patterns

- **Navigation:** drawer or bottom bar on phones, compact horizontal on tablets, full labels on desktop.
- **Tables:** on narrow screens, let the table scroll horizontally inside a labeled region with a sticky first column, or reflow rows into cards using `data-label` attributes.
- **Collapsible content:** `<details>`/`<summary>` for sections that can fold on small screens; `display: none` removes content from the accessibility tree and images inside it may still download.
- **Avoid:** separate mobile and desktop codebases, user-agent sniffing, and forgetting landscape phones and tablets.

## Verify

- Check widths from 320px to wide desktop, both orientations, and 200% zoom, in the browser tools available (Playwright MCP or the session's browser). Emulation verifies layout but not real touch behavior, CPU limits, font rendering, or on-screen keyboards; report which of those stayed unverified.
- Test touch, mouse, and keyboard paths. Check the main engines the project supports (Chromium, WebKit, Gecko); Chromium emulation is not Safari.
- **Custom controls** (sliders, drag surfaces, scrollable strips) can pass every width check and still refuse to drag on iOS. For each one in scope: tap it and confirm the response, then drag with the target input and confirm the drag completes; swipe across it along the page's scroll axis and confirm the page scrolls without activating the control; drag along the control's own axis and confirm the control moves, not the page. Say what produced the evidence (emulated viewport, synthesized touch, which engine, physical device) and name what stayed untested; unreachable hardware is a reported gap, not a blocker.

When the adaptation feels native to each context, finish with a polish pass ([polish.md](polish.md)).
