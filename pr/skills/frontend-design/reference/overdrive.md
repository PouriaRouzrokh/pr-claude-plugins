# Overdrive

Push an interface past conventional limits using the full power of the browser: a table that handles a million rows, a dialog that morphs from its trigger, validation that streams feedback as you type, a page transition that feels cinematic.

Context decides what "extraordinary" means. A particle system on a creative portfolio is impressive; the same particle system on a settings page is embarrassing. A settings page with instant optimistic saves and smooth state transitions is extraordinary too. Understand the project's personality and goals before choosing a technique.

## Contents

- [Propose before building](#propose-before-building)
- [What "extraordinary" means here](#what-extraordinary-means-here)
- [The toolkit](#the-toolkit)
- [Browser support snapshot](#browser-support-snapshot)
- [Implement with discipline](#implement-with-discipline)
- [Verify](#verify)

## Propose before building

This pass misfires more than any other, and an ambitious effect built in the wrong direction is expensive to throw away. So, unless the user already specified the effect:

1. Think through two or three directions that differ in technique, ambition, and aesthetic, and describe what each would look and feel like.
2. Ask the user to pick one with the AskUserQuestion tool. Put each direction's description and trade-offs (browser support, performance cost, complexity) in the option itself.
3. Build only the confirmed direction.

Ambitious effects rarely look right on the first try, so verify visually: preview in the browser (Playwright MCP or the session's browser tools), screenshot, and refine. Keep this bounded like any other inspection: a round to build and capture, a round of fixes, one confirming capture.

## What "extraordinary" means here

Ask what would make a user of this specific interface say "that's nice":

- **Visual and marketing surfaces** (heroes, landing pages, portfolios): often sensory. A scroll-driven reveal, a shader background, a cinematic page transition, generative art that responds to the cursor.
- **Functional UI** (tables, forms, dialogs, navigation): how it feels. A dialog that morphs out of its button through a view transition, a table that scrolls 100k rows smoothly through virtualization, validation that feels instant, drag and drop with spring physics.
- **Performance-critical UI:** invisible but felt. Search that filters 50k items without a flicker, a complex form that never blocks the main thread.
- **Data-heavy interfaces:** fluidity. Canvas or WebGL rendering for large datasets, animated transitions between data states, force-directed layouts that settle naturally.

The technique serves the experience, not the other way around.

## The toolkit

**Cinematic transitions**
- **View Transitions API:** shared-element morphing between states (a list item expanding into a detail view, a button becoming a dialog). The closest thing to native FLIP. In React 19.3+, use `<ViewTransition>` rather than calling the API yourself ([react-view-transitions.md](react-view-transitions.md)).
- **`@starting-style`:** CSS-only entry animations from `display: none` ([animate.md](animate.md#entry-and-exit-with-css)).
- **Spring physics:** natural motion with mass, tension, and damping, via Motion (formerly Framer Motion), GSAP, or CSS `linear()` approximations.

**Scroll-linked motion**
- **Scroll-driven animations** (`animation-timeline: scroll()` / `view()`): CSS-only parallax, progress indicators, and reveal sequences, off the main thread.

**Rendering beyond CSS**
- **WebGL:** shaders, post-processing, particles (Three.js, OGL, regl).
- **WebGPU:** GPU compute and modern rendering; fall back to WebGL2.
- **Canvas 2D and OffscreenCanvas:** custom drawing and pixel work, optionally in a worker so the main thread stays free.
- **SVG filters:** displacement, morphology, and lighting for organic distortion.

**Data that feels alive**
- **Virtual scrolling** for tens of thousands of rows (TanStack Virtual for complex cases).
- **GPU-rendered charts** (deck.gl or custom WebGL) for datasets too large for SVG or DOM.
- **Animated data transitions:** morph between chart states with D3 transitions or view transitions instead of replacing.

**Complex property animation**
- **`@property`:** registers typed custom properties so gradients, angles, and colors can interpolate.
- **Web Animations API:** scripted animations that are composable, cancellable, and reversible.

**Performance headroom**
- **Web Workers** for heavy data processing, image work, and search indexing; **WebAssembly** for codecs, physics, and image processing.

**Device**
- **Web Audio** for sonic feedback and audio-reactive visuals (requires a user gesture and explicit opt-in to sound).
- **Device sensors** (orientation, geolocation): sparingly, and always with permission.

This pass changes how existing features feel, not what the product does. Real-time collaboration, offline support, or new backend capabilities are product decisions.

## Browser support snapshot

Status as of October 2026; check [Baseline](https://web.dev/baseline) or MDN before relying on anything marked partial.

| Feature | Status |
|---------|--------|
| Same-document view transitions (`document.startViewTransition`) | Baseline since October 2025 (Firefox 144) |
| Cross-document view transitions (`@view-transition { navigation: auto }`) | Chromium 126+, Safari 18.2+; not in Firefox |
| `@starting-style`, `transition-behavior: allow-discrete` | Baseline 2024 |
| `field-sizing: content` | Baseline June 2026 (Firefox 152) |
| `contrast-color()` | Baseline April 2026 (Chrome 147, Firefox 146, Safari 26) |
| `@property`, Web Animations API, WebGL2 | Baseline |
| Scroll-driven animations | Chromium 115+, Safari 26+; not in stable Firefox (MDN lists Firefox 159) |
| `interpolate-size` / `calc-size()` | Chromium only |
| CSS anchor positioning (`anchor-name`, `position-area`, `anchor()`, `position-try-fallbacks`) | Chrome 125, Safari 26, Firefox 147 (January 2026). Not yet Baseline as a whole feature: Baseline data waits on Safari 27 for the remaining parts, so keep a fallback position |
| Customizable `<select>` (`appearance: base-select`) | Chromium 135+, Safari 27; Firefox behind a flag |
| WebGPU | Chromium, Safari 26+; Firefox partial (by platform) |

## Implement with discipline

**Progressive enhancement.** Every technique degrades gracefully, and the experience without it must still be good:

```css
@supports (animation-timeline: view()) {
  .reveal { animation: reveal linear both; animation-timeline: view(); animation-range: entry 0% cover 30%; }
}
```

```js
if (navigator.gpu) { /* WebGPU path */ }
else if (canvas.getContext('webgl2')) { /* WebGL2 fallback */ }
else { /* static image or CSS treatment that still looks intentional */ }

if (document.startViewTransition) document.startViewTransition(update);
else update();
```

Respect `prefers-reduced-motion` on every effect: replace large spatial movement with a crossfade or a static state.

**Performance.** Hold 60fps on mid-range hardware and simplify when it drops. Initialize heavy resources (WebGL contexts, WASM modules) only when they approach the viewport, pause rendering offscreen, and release contexts you no longer need.

**Polish.** The gap between "cool" and "extraordinary" is in the last 20%: the easing on a spring, the timing offset in a stagger, the secondary motion that makes a transition feel physical.

**Avoid:** effects that jank on mid-range devices; bleeding-edge APIs without a functional fallback; sound without opt-in; technical ambition masking weak fundamentals (fix those first with the other references); several competing showpieces on one surface.

## Verify

- **Removal test:** take the effect away. Does the experience feel diminished, or does nobody notice?
- **Device test:** throttle the CPU in DevTools and check a mobile viewport; say which real devices were not tested.
- **Fallback test:** disable the feature (or use a browser without it) and confirm the fallback looks intentional.
- **Context test:** does this make sense for this brand and audience?

When the effect earns its place, finish with a polish pass ([polish.md](polish.md)).
